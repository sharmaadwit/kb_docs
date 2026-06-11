#!/usr/bin/env python3
"""
Comprehensive KB Analytics Dashboard v2
Consolidates: Langfuse (KB answers) + Local NDJSON (video events)
Tracks: All channels (RCS, WhatsApp, Instagram, Web, SMS, etc.)
Timeline: 7-day rolling window
"""
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "local" / "reports"
ANALYTICS_DIR = ROOT / "kb" / "analytics"

def _parse_iso(s: str) -> Optional[datetime]:
    if not s:
        return None
    s = s.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s)
    except:
        return None

def fetch_langfuse_traces(limit: int = 200) -> List[Dict[str, Any]]:
    """Fetch all kb_answer traces from Langfuse (no channel filter)."""
    pub_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")

    if not pub_key or not secret_key:
        print("⚠️  Langfuse credentials missing", file=sys.stderr)
        return []

    cmd = ["lf", "--json", "traces", "list", "--name", "kb_answer", "--limit", str(limit)]

    print(f"Fetching Langfuse traces (limit={limit})...", file=sys.stderr)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if proc.returncode != 0:
        if limit > 50:
            return fetch_langfuse_traces(limit=50)
        print(f"⚠️  Langfuse error: {proc.stderr[:100]}", file=sys.stderr)
        return []

    try:
        return json.loads(proc.stdout)
    except:
        return []

def analyze_langfuse_traces(traces: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze KB answer traces by channel, module, and intent."""
    if not traces:
        return {"trace_count": 0}

    # Global counters
    answered = 0
    unanswered = 0
    video_attached = 0
    latencies = []
    scores = []

    # Per-channel breakdown
    channels = defaultdict(lambda: {
        "count": 0, "answered": 0, "unanswered": 0, "video_attached": 0,
        "scores": [], "latencies": [], "modules": Counter(), "intents": Counter()
    })

    # Per-module breakdown
    modules = defaultdict(lambda: {
        "count": 0, "answered": 0, "unanswered": 0, "video_attached": 0,
        "channels": Counter()
    })

    # Per-intent breakdown
    intents = defaultdict(lambda: {"count": 0, "answered": 0, "unanswered": 0})

    # Top queries by channel
    queries_by_channel = defaultdict(list)

    for t in traces:
        meta = t.get("metadata") or {}
        output = t.get("output") or {}

        # Detect channel from Langfuse metadata
        # Rule: If channel_type is detected (rcs, whatsapp, instagram, web, sms), use it.
        # If not set (null), treat as "whatsapp" for new data or "untagged" for historical.
        # Historical (pre-2026-06-11): channel_type=null → "untagged" (honest to timeline)
        # Future (post-2026-06-11): channel_type always set → "whatsapp" default, never null
        channel = meta.get("channel_type") or "untagged"

        # Module
        module = meta.get("module_label") or "General"

        # Intents
        intents_list = meta.get("intent_labels") or []

        # Answer status
        answer = output.get("answer", "") if isinstance(output, dict) else ""
        is_answered = bool("i don't know" not in answer.lower() and answer.strip())

        # Update global counters
        if is_answered:
            answered += 1
        else:
            unanswered += 1

        if meta.get("video_attached"):
            video_attached += 1

        # Channel breakdown
        ch_data = channels[channel]
        ch_data["count"] += 1
        ch_data["modules"][module] += 1
        if is_answered:
            ch_data["answered"] += 1
        else:
            ch_data["unanswered"] += 1
        if meta.get("video_attached"):
            ch_data["video_attached"] += 1

        # Module breakdown
        mod_data = modules[module]
        mod_data["count"] += 1
        mod_data["channels"][channel] += 1
        if is_answered:
            mod_data["answered"] += 1
        else:
            mod_data["unanswered"] += 1
        if meta.get("video_attached"):
            mod_data["video_attached"] += 1

        # Intent breakdown
        for intent in intents_list:
            intent_key = str(intent)
            intents[intent_key]["count"] += 1
            if is_answered:
                intents[intent_key]["answered"] += 1
            else:
                intents[intent_key]["unanswered"] += 1

        # Scores & latency
        conf = meta.get("confidence")
        if conf:
            try:
                score = float(conf)
                scores.append(score)
                ch_data["scores"].append(score)
            except:
                pass

        try:
            lat = int(meta.get("latency_ms") or 0)
            if lat > 0:
                latencies.append(lat)
                ch_data["latencies"].append(lat)
        except:
            pass

        # Track queries per channel
        query = meta.get("query", "")
        if query:
            queries_by_channel[channel].append({
                "query": query[:80],
                "answered": is_answered,
                "module": module,
                "confidence": conf,
            })

    # Compute percentiles
    latencies.sort()
    p50 = latencies[len(latencies) // 2] if latencies else None
    p95 = latencies[int(len(latencies) * 0.95)] if len(latencies) >= 20 else None

    # Compute per-channel stats
    channel_stats = {}
    for ch, data in channels.items():
        total = data["count"]
        scores = data["scores"]
        lats = data["latencies"]

        lats.sort()
        ch_p50 = lats[len(lats) // 2] if lats else None

        channel_stats[ch] = {
            "count": total,
            "answered": data["answered"],
            "unanswered": data["unanswered"],
            "answer_rate_pct": round(100.0 * data["answered"] / total, 1) if total else 0,
            "video_attach_rate_pct": round(100.0 * data["video_attached"] / data["answered"], 1) if data["answered"] else 0,
            "avg_confidence": round(sum(scores) / len(scores), 2) if scores else None,
            "latency_p50_ms": ch_p50,
            "top_module": data["modules"].most_common(1)[0][0] if data["modules"] else "N/A",
            "top_queries": sorted(queries_by_channel[ch], key=lambda q: (q["answered"], q["confidence"] or 0), reverse=True)[:5],
        }

    # Compute per-module stats
    module_stats = {}
    for mod, data in modules.items():
        total = data["count"]
        module_stats[mod] = {
            "count": total,
            "answered": data["answered"],
            "unanswered": data["unanswered"],
            "answer_rate_pct": round(100.0 * data["answered"] / total, 1) if total else 0,
            "video_attach_rate_pct": round(100.0 * data["video_attached"] / data["answered"], 1) if data["answered"] else 0,
            "top_channel": data["channels"].most_common(1)[0][0] if data["channels"] else "N/A",
        }

    total = answered + unanswered

    return {
        "trace_count": len(traces),
        "answered": answered,
        "unanswered": unanswered,
        "answer_rate_pct": round(100.0 * answered / total, 1) if total else 0,
        "video_attach_rate_pct": round(100.0 * video_attached / answered, 1) if answered else 0,
        "avg_confidence": round(sum(scores) / len(scores), 2) if scores else None,
        "latency_p50_ms": p50,
        "latency_p95_ms": p95,
        "latency_avg_ms": round(sum(latencies) / len(latencies), 0) if latencies else None,
        "by_channel": channel_stats,
        "by_module": module_stats,
        "by_intent": dict((k, {
            "count": v["count"],
            "answer_rate_pct": round(100.0 * v["answered"] / v["count"], 1) if v["count"] else 0
        }) for k, v in intents.items()),
    }

def analyze_local_video_analytics() -> Dict[str, Any]:
    """Analyze local NDJSON video delivery events."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    videos = defaultdict(lambda: {"count": 0, "modules": Counter(), "intents": Counter()})
    total_videos = 0

    for path in sorted(ANALYTICS_DIR.glob("*.ndjson")):
        with open(path, 'r') as f:
            for line in f:
                try:
                    event = json.loads(line)
                    if event.get("event") == "video.delivered":
                        ts = _parse_iso(str(event.get("ts") or ""))
                        if ts and ts >= cutoff:
                            total_videos += 1
                            payload = event.get("payload") or {}
                            module = payload.get("module", "Unknown")
                            intent = payload.get("intent", "unknown")
                            videos[module]["count"] += 1
                            videos[module]["modules"][module] += 1
                            videos[module]["intents"][intent] += 1
                except:
                    pass

    return {
        "total_video_events": total_videos,
        "by_module": {m: d["count"] for m, d in videos.items()},
    }

def build_dashboard_html(langfuse: Dict, local: Dict) -> str:
    """Build comprehensive multi-channel analytics dashboard."""

    trace_count = langfuse.get("trace_count", 0)
    answer_rate = langfuse.get("answer_rate_pct", 0)
    video_rate = langfuse.get("video_attach_rate_pct", 0)
    avg_conf = langfuse.get("avg_confidence", "N/A")
    by_channel = langfuse.get("by_channel", {})
    by_module = langfuse.get("by_module", {})
    by_intent = langfuse.get("by_intent", {})

    # Channel breakdown rows
    channel_rows = "\n".join([
        f"""<tr>
            <td>{ch}</td>
            <td align='right'>{data['count']}</td>
            <td align='right'>{data['answer_rate_pct']}%</td>
            <td align='right'>{data['video_attach_rate_pct']}%</td>
            <td align='right'>{data['avg_confidence'] or 'N/A'}</td>
            <td align='right'>{data['latency_p50_ms'] or 'N/A'}ms</td>
            <td>{data['top_module']}</td>
        </tr>"""
        for ch, data in sorted(by_channel.items(), key=lambda x: -x[1]["count"])
    ])

    # Module breakdown rows
    module_rows = "\n".join([
        f"""<tr>
            <td>{mod}</td>
            <td align='right'>{data['count']}</td>
            <td align='right'>{data['answer_rate_pct']}%</td>
            <td align='right'>{data['video_attach_rate_pct']}%</td>
            <td>{data['top_channel']}</td>
        </tr>"""
        for mod, data in sorted(by_module.items(), key=lambda x: -x[1]["count"])
    ])

    # Intent breakdown rows
    intent_rows = "\n".join([
        f"<tr><td>{intent}</td><td align='right'>{data['count']}</td><td align='right'>{data['answer_rate_pct']}%</td></tr>"
        for intent, data in sorted(by_intent.items(), key=lambda x: -x[1]["count"])
    ])

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Comprehensive KB Analytics Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            color: #333;
        }}
        .container {{ max-width: 1600px; margin: 0 auto; }}
        .header {{ color: white; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.8em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.1em; opacity: 0.9; }}

        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .card:hover {{ transform: translateY(-5px); }}

        .metric {{ margin-bottom: 20px; }}
        .metric-label {{ font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
        .metric-value {{ font-size: 2.2em; font-weight: bold; color: #333; }}
        .metric-unit {{ font-size: 0.45em; color: #999; margin-left: 5px; }}

        .status-good {{ color: #2ecc71; }}
        .status-warning {{ color: #f39c12; }}
        .status-critical {{ color: #e74c3c; }}

        .section {{ background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
        .section h2 {{ font-size: 1.6em; margin-bottom: 20px; color: #333; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}

        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th {{
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #555;
            border-bottom: 2px solid #ddd;
            font-size: 0.9em;
        }}
        td {{ padding: 12px; border-bottom: 1px solid #eee; font-size: 0.95em; }}
        tr:hover {{ background: #f8f9fa; }}

        .footer {{ text-align: center; color: white; margin-top: 40px; font-size: 0.9em; opacity: 0.8; }}
        .data-source {{ background: rgba(255,255,255,0.1); padding: 12px; border-radius: 6px; margin-top: 10px; }}

        .health-indicator {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.85em;
            font-weight: 600;
            margin-right: 8px;
            margin-bottom: 8px;
        }}
        .health-good {{ background: #d4edda; color: #155724; }}
        .health-warning {{ background: #fff3cd; color: #856404; }}
        .health-critical {{ background: #f8d7da; color: #721c24; }}

        .chart-bar {{
            display: inline-block;
            height: 20px;
            background: #667eea;
            border-radius: 3px;
            margin-right: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Comprehensive KB Analytics Dashboard</h1>
            <p>All channels • 7-day rolling window • Real-time Langfuse + Local analytics</p>
        </div>

        <!-- Global Metrics -->
        <div class="grid">
            <div class="card">
                <div class="metric">
                    <div class="metric-label">Total Queries</div>
                    <div class="metric-value">{trace_count}</div>
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">Overall Answer Rate</div>
                    <div class="metric-value status-{'good' if answer_rate >= 80 else 'warning' if answer_rate >= 60 else 'critical'}">
                        {answer_rate}%
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">Video Attachment Rate</div>
                    <div class="metric-value status-{'good' if video_rate >= 50 else 'warning' if video_rate >= 25 else 'critical'}">
                        {video_rate}%
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">Avg Confidence</div>
                    <div class="metric-value">{avg_conf}</div>
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">P50 Latency</div>
                    <div class="metric-value">{langfuse.get('latency_p50_ms') or 'N/A'}<span class="metric-unit">ms</span></div>
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">P95 Latency</div>
                    <div class="metric-value status-{'critical' if (langfuse.get('latency_p95_ms') or 0) > 5000 else 'warning' if (langfuse.get('latency_p95_ms') or 0) > 3000 else 'good'}">
                        {langfuse.get('latency_p95_ms') or 'N/A'}<span class="metric-unit">ms</span>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">Video Events</div>
                    <div class="metric-value">{local.get('total_video_events', 0)}</div>
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">Channels Active</div>
                    <div class="metric-value">{len(by_channel)}</div>
                </div>
            </div>
        </div>

        <!-- Channel Breakdown -->
        <div class="section">
            <h2>📡 Performance by Channel</h2>
            <div class="data-source">
                <strong>Source:</strong> Langfuse traces with channel_type metadata (RCS, WhatsApp, Instagram, Web, SMS, etc.)
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Channel</th>
                        <th>Queries</th>
                        <th>Answer Rate</th>
                        <th>Video Attach %</th>
                        <th>Avg Confidence</th>
                        <th>P50 Latency</th>
                        <th>Top Module</th>
                    </tr>
                </thead>
                <tbody>
                {channel_rows if channel_rows else "<tr><td colspan='7'><em>No channel data</em></td></tr>"}
                </tbody>
            </table>
        </div>

        <!-- Module Breakdown -->
        <div class="section">
            <h2>📦 Performance by Module</h2>
            <div class="data-source">
                <strong>Source:</strong> Langfuse module_label metadata
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Module</th>
                        <th>Queries</th>
                        <th>Answer Rate</th>
                        <th>Video Attach %</th>
                        <th>Primary Channel</th>
                    </tr>
                </thead>
                <tbody>
                {module_rows if module_rows else "<tr><td colspan='5'><em>No module data</em></td></tr>"}
                </tbody>
            </table>
        </div>

        <!-- Intent Breakdown -->
        <div class="section">
            <h2>🎯 Query Intent Analysis</h2>
            <div class="data-source">
                <strong>Source:</strong> Langfuse intent_labels (setup, definition, overview, etc.)
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Intent</th>
                        <th>Count</th>
                        <th>Answer Rate</th>
                    </tr>
                </thead>
                <tbody>
                {intent_rows if intent_rows else "<tr><td colspan='3'><em>No intent data</em></td></tr>"}
                </tbody>
            </table>
        </div>

        <!-- Health Dashboard -->
        <div class="section">
            <h2>🏥 System Health</h2>
            <div style="margin: 20px 0;">
                <div class="health-indicator health-{'good' if answer_rate >= 80 else 'warning' if answer_rate >= 60 else 'critical'}">
                    Answer Rate: {answer_rate}% {'✓' if answer_rate >= 80 else '⚠️' if answer_rate >= 60 else '✗'}
                </div>
                <div class="health-indicator health-{'good' if video_rate >= 50 else 'warning' if video_rate >= 25 else 'critical'}">
                    Video Attachment: {video_rate}% {'✓' if video_rate >= 50 else '⚠️' if video_rate >= 25 else '✗'}
                </div>
                <div class="health-indicator health-{'good' if (langfuse.get('latency_p95_ms') or 0) < 3000 else 'warning' if (langfuse.get('latency_p95_ms') or 0) < 5000 else 'critical'}">
                    P95 Latency: {langfuse.get('latency_p95_ms') or 'N/A'}ms {'✓' if (langfuse.get('latency_p95_ms') or 0) < 3000 else '⚠️' if (langfuse.get('latency_p95_ms') or 0) < 5000 else '✗'}
                </div>
                <div class="health-indicator health-{'good' if avg_conf != 'N/A' and float(str(avg_conf).split('/')[0]) > 5 else 'warning' if avg_conf != 'N/A' else 'critical'}">
                    Confidence: {avg_conf} {'✓' if avg_conf != 'N/A' and float(str(avg_conf)) > 5 else '⚠️'}
                </div>
            </div>
        </div>

        <!-- Data Sources -->
        <div class="section">
            <h2>📊 Data Sources & Coverage</h2>
            <table style="font-size: 0.9em;">
                <thead>
                    <tr>
                        <th>Source</th>
                        <th>Events</th>
                        <th>Type</th>
                        <th>Coverage</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Langfuse</strong></td>
                        <td>{trace_count}</td>
                        <td>KB answer traces</td>
                        <td>Answer quality, confidence, latency, video attachment by query</td>
                    </tr>
                    <tr>
                        <td><strong>Local NDJSON</strong></td>
                        <td>{local.get('total_video_events', 0)}</td>
                        <td>Video delivery events</td>
                        <td>Video manifest accuracy, module/intent distribution</td>
                    </tr>
                    <tr>
                        <td><strong>Combined</strong></td>
                        <td>—</td>
                        <td>Correlation</td>
                        <td>Answer rate + video attachment by channel/module</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <p>Data sources: Langfuse API (real-time KB traces) + Local NDJSON files (video events)</p>
            <p>Dashboard auto-updates every run. Use this for trend tracking, performance monitoring, and multi-channel analysis.</p>
        </div>
    </div>
</body>
</html>"""

    return html

def main():
    print("=" * 80)
    print("🚀 COMPREHENSIVE KB ANALYTICS DASHBOARD v2")
    print("=" * 80)
    print()

    # Fetch Langfuse traces (all channels)
    print("1️⃣ Fetching Langfuse traces (all channels)...", file=sys.stderr)
    traces = fetch_langfuse_traces(limit=200)
    langfuse_analysis = analyze_langfuse_traces(traces)
    print(f"   ✅ {langfuse_analysis.get('trace_count', 0)} traces analyzed", file=sys.stderr)

    # Analyze local video events
    print("2️⃣ Analyzing local NDJSON video events...", file=sys.stderr)
    local_analysis = analyze_local_video_analytics()
    print(f"   ✅ {local_analysis.get('total_video_events', 0)} video events loaded", file=sys.stderr)

    # Build HTML dashboard
    print("3️⃣ Building comprehensive dashboard...", file=sys.stderr)
    html = build_dashboard_html(langfuse_analysis, local_analysis)

    # Save JSON (structured data)
    combined = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "period": "7-day rolling",
        "langfuse": langfuse_analysis,
        "local_analytics": local_analysis,
    }
    json_file = REPORTS_DIR / "comprehensive_analytics.json"
    json_file.write_text(json.dumps(combined, indent=2), encoding="utf-8")
    print(f"   ✅ Saved: comprehensive_analytics.json", file=sys.stderr)

    # Save HTML
    html_file = REPORTS_DIR / "comprehensive_dashboard.html"
    html_file.write_text(html, encoding="utf-8")
    print(f"   ✅ Saved: comprehensive_dashboard.html", file=sys.stderr)

    print()
    print("=" * 80)
    print("📊 DASHBOARD SUMMARY")
    print("=" * 80)

    # Channel summary
    by_channel = langfuse_analysis.get("by_channel", {})
    print(f"\n📡 Channels Active: {len(by_channel)}")
    for ch, data in sorted(by_channel.items(), key=lambda x: -x[1]["count"]):
        print(f"   {ch:15s}: {data['count']:3d} queries | {data['answer_rate_pct']:5.1f}% answer | {data['video_attach_rate_pct']:5.1f}% video")

    # Overall stats
    print(f"\n🎯 Overall Metrics")
    print(f"   Answer Rate: {langfuse_analysis.get('answer_rate_pct', 0)}%")
    print(f"   Video Attachment: {langfuse_analysis.get('video_attach_rate_pct', 0)}%")
    print(f"   Avg Confidence: {langfuse_analysis.get('avg_confidence', 'N/A')}")
    print(f"   P50 Latency: {langfuse_analysis.get('latency_p50_ms', 'N/A')}ms")
    print(f"   P95 Latency: {langfuse_analysis.get('latency_p95_ms', 'N/A')}ms")

    print()
    print("=" * 80)
    print("✅ Dashboard ready at: local/reports/comprehensive_dashboard.html")
    print("=" * 80)

if __name__ == "__main__":
    main()
