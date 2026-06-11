#!/usr/bin/env python3
"""Generate 7-day KB analytics dashboard from Langfuse traces + local analytics."""
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

def fetch_langfuse_traces_7day(limit: int = 200) -> List[Dict[str, Any]]:
    """Fetch kb_answer traces from Langfuse for last 7 days."""
    pub_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")

    if not pub_key or not secret_key:
        print("⚠️  LANGFUSE credentials not set, skipping Langfuse data", file=sys.stderr)
        return []

    cmd = ["lf", "--json", "traces", "list", "--name", "kb_answer", "--limit", str(limit)]

    print(f"Fetching {limit} traces from Langfuse...", file=sys.stderr)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if proc.returncode != 0:
        if limit > 50:
            return fetch_langfuse_traces_7day(limit=50)
        print(f"⚠️  Langfuse API error: {proc.stderr[:100]}", file=sys.stderr)
        return []

    try:
        return json.loads(proc.stdout)
    except:
        return []

def analyze_langfuse_traces(traces: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze KB answer traces."""
    if not traces:
        return {"trace_count": 0}

    modules = Counter()
    modes = Counter()
    intents = Counter()
    channels = Counter()
    answered = 0
    unanswered = 0
    video_attached = 0
    latencies = []
    scores = []
    queries = []

    for t in traces:
        meta = t.get("metadata") or {}
        output = t.get("output") or {}

        # Module
        modules[meta.get("module_label") or "General"] += 1

        # Mode
        modes[meta.get("selected_answer_mode") or "unknown"] += 1

        # Intent
        for lab in meta.get("intent_labels") or []:
            intents[str(lab)] += 1

        # Channel
        channel = meta.get("channel_type")
        if channel:
            channels[channel] += 1

        # Answer status
        answer = output.get("answer", "") if isinstance(output, dict) else ""
        is_answered = bool("i don't know" not in answer.lower() and answer.strip())

        if is_answered:
            answered += 1
        else:
            unanswered += 1

        # Video
        if meta.get("video_attached"):
            video_attached += 1

        # Latency
        try:
            lat = int(meta.get("latency_ms") or 0)
            if lat > 0:
                latencies.append(lat)
        except:
            pass

        # Confidence
        conf = meta.get("confidence")
        if conf:
            try:
                scores.append(float(conf))
            except:
                pass

        # Query
        query = meta.get("query", "")
        if query:
            queries.append({
                "query": query[:80],
                "answered": is_answered,
                "module": meta.get("module_label") or "General",
                "confidence": conf,
                "mode": meta.get("selected_answer_mode"),
            })

    latencies.sort()
    p50 = latencies[len(latencies) // 2] if latencies else None
    p95 = latencies[int(len(latencies) * 0.95)] if len(latencies) >= 20 else None
    avg_lat = sum(latencies) / len(latencies) if latencies else None

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
        "latency_avg_ms": round(avg_lat, 0) if avg_lat else None,
        "by_module": dict(modules.most_common(15)),
        "by_mode": dict(modes.most_common(10)),
        "by_intent": dict(intents.most_common(15)),
        "by_channel": dict(channels.most_common()),
        "top_queries": sorted(queries, key=lambda q: (q["answered"], float(q["confidence"] or 0)), reverse=True)[:20],
    }

def analyze_local_analytics() -> Dict[str, Any]:
    """Analyze local video delivery analytics."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    videos = defaultdict(lambda: {"count": 0, "modules": Counter(), "intents": Counter()})
    total_video_events = 0

    for path in sorted(ANALYTICS_DIR.glob("*.ndjson")):
        with open(path, 'r') as f:
            for line in f:
                try:
                    event = json.loads(line)
                    if event.get("event") == "video.delivered":
                        ts = _parse_iso(str(event.get("ts") or ""))
                        if ts and ts >= cutoff:
                            total_video_events += 1
                            payload = event.get("payload") or {}
                            module = payload.get("module", "Unknown")
                            intent = payload.get("intent", "unknown")
                            videos[module]["count"] += 1
                            videos[module]["modules"][module] += 1
                            videos[module]["intents"][intent] += 1
                except:
                    pass

    by_module = {m: d["count"] for m, d in videos.items()}
    by_intent = Counter()
    for m, d in videos.items():
        by_intent.update(d["intents"])

    return {
        "total_video_events": total_video_events,
        "by_module": dict(sorted(by_module.items(), key=lambda x: -x[1])),
        "by_intent": dict(by_intent.most_common(15)),
    }

def build_dashboard_html(langfuse: Dict, local: Dict) -> str:
    """Build comprehensive 7-day dashboard HTML."""

    lf_trace_count = langfuse.get("trace_count", 0)
    lf_answer_rate = langfuse.get("answer_rate_pct", 0)
    lf_video_rate = langfuse.get("video_attach_rate_pct", 0)
    lf_avg_conf = langfuse.get("avg_confidence", "N/A")

    local_video_count = local.get("total_video_events", 0)

    by_module = langfuse.get("by_module", {})
    by_intent = langfuse.get("by_intent", {})
    by_channel = langfuse.get("by_channel", {})
    top_queries = langfuse.get("top_queries", [])

    module_rows = "\n".join([
        f"<tr><td>{m}</td><td align='right'>{c}</td></tr>"
        for m, c in list(by_module.items())[:15]
    ])

    intent_rows = "\n".join([
        f"<tr><td>{i}</td><td align='right'>{c}</td></tr>"
        for i, c in list(by_intent.items())[:15]
    ])

    channel_rows = "\n".join([
        f"<tr><td>{c}</td><td align='right'>{cnt}</td></tr>"
        for c, cnt in list(by_channel.items())
    ])

    query_rows = "\n".join([
        f"<tr><td>{q['query']}</td><td align='center'>{'✅' if q['answered'] else '❌'}</td><td align='right'>{q['confidence'] or 'N/A'}</td><td>{q['module']}</td></tr>"
        for q in top_queries[:25]
    ])

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>7-Day KB Analytics Dashboard</title>
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
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ color: white; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.1em; opacity: 0.9; }}

        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .card:hover {{ transform: translateY(-5px); }}

        .metric {{ margin-bottom: 20px; }}
        .metric-label {{ font-size: 0.85em; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
        .metric-value {{ font-size: 2.5em; font-weight: bold; color: #333; }}
        .metric-unit {{ font-size: 0.5em; color: #999; margin-left: 5px; }}

        .status-good {{ color: #2ecc71; }}
        .status-warning {{ color: #f39c12; }}
        .status-critical {{ color: #e74c3c; }}

        .section {{ background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
        .section h2 {{ font-size: 1.5em; margin-bottom: 20px; color: #333; }}

        table {{ width: 100%; border-collapse: collapse; }}
        th {{
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #555;
            border-bottom: 2px solid #ddd;
        }}
        td {{ padding: 12px; border-bottom: 1px solid #eee; }}
        tr:hover {{ background: #f8f9fa; }}

        .footer {{ text-align: center; color: white; margin-top: 40px; font-size: 0.9em; opacity: 0.8; }}

        .stats-row {{
            display: flex;
            justify-content: space-around;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .stat-badge {{
            background: #f0f0f0;
            padding: 12px 20px;
            border-radius: 8px;
            text-align: center;
            flex: 1;
            min-width: 150px;
        }}
        .stat-number {{
            font-size: 1.8em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            font-size: 0.85em;
            color: #666;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 7-Day KB Analytics Dashboard</h1>
            <p>Usage, performance, and video attachment metrics (Last 7 days)</p>
        </div>

        <!-- Quick Stats -->
        <div class="grid">
            <div class="card">
                <div class="metric">
                    <div class="metric-label">KB Queries (Langfuse)</div>
                    <div class="metric-value">{lf_trace_count}</div>
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">Answer Rate</div>
                    <div class="metric-value status-{'good' if lf_answer_rate >= 80 else 'warning' if lf_answer_rate >= 60 else 'critical'}">
                        {lf_answer_rate}%
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">Video Attachment Rate</div>
                    <div class="metric-value status-{'good' if lf_video_rate >= 50 else 'warning' if lf_video_rate >= 25 else 'critical'}">
                        {lf_video_rate}%
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">Avg Confidence</div>
                    <div class="metric-value">{lf_avg_conf}</div>
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">Video Events (Local)</div>
                    <div class="metric-value">{local_video_count}</div>
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">P50 Latency</div>
                    <div class="metric-value">{langfuse.get('latency_p50_ms') or 'N/A'}<span class="metric-unit">ms</span></div>
                </div>
            </div>
        </div>

        <!-- Latency Details -->
        <div class="section">
            <h2>⏱️ Latency Metrics</h2>
            <div class="stats-row">
                <div class="stat-badge">
                    <div class="stat-number">{langfuse.get('latency_p50_ms') or 'N/A'}</div>
                    <div class="stat-label">P50 (Median)</div>
                </div>
                <div class="stat-badge">
                    <div class="stat-number">{langfuse.get('latency_p95_ms') or 'N/A'}</div>
                    <div class="stat-label">P95</div>
                </div>
                <div class="stat-badge">
                    <div class="stat-number">{langfuse.get('latency_avg_ms') or 'N/A'}</div>
                    <div class="stat-label">Average</div>
                </div>
            </div>
        </div>

        <!-- Modules -->
        <div class="section">
            <h2>📦 Distribution by Module</h2>
            <table>
                <thead><tr><th>Module</th><th>KB Queries</th></tr></thead>
                <tbody>
                {module_rows if module_rows else "<tr><td colspan='2'><em>No data</em></td></tr>"}
                </tbody>
            </table>
        </div>

        <!-- Intents -->
        <div class="section">
            <h2>🎯 Top Intents</h2>
            <table>
                <thead><tr><th>Intent</th><th>Count</th></tr></thead>
                <tbody>
                {intent_rows if intent_rows else "<tr><td colspan='2'><em>No data</em></td></tr>"}
                </tbody>
            </table>
        </div>

        <!-- Channels -->
        <div class="section">
            <h2>📡 Channels</h2>
            <table>
                <thead><tr><th>Channel</th><th>Queries</th></tr></thead>
                <tbody>
                {channel_rows if channel_rows else "<tr><td colspan='2'><em>No channel data yet</em></td></tr>"}
                </tbody>
            </table>
        </div>

        <!-- Top Queries -->
        <div class="section">
            <h2>💬 Top Queries</h2>
            <table>
                <thead>
                    <tr>
                        <th>Query</th>
                        <th>Status</th>
                        <th>Confidence</th>
                        <th>Module</th>
                    </tr>
                </thead>
                <tbody>
                {query_rows if query_rows else "<tr><td colspan='4'><em>No query data</em></td></tr>"}
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <p>Data sources: Langfuse API (KB answers) + local analytics (video events)</p>
        </div>
    </div>
</body>
</html>"""

    return html

def main():
    print("🔄 Generating 7-day analytics dashboard...", file=sys.stderr)
    print()

    # Fetch Langfuse traces
    print("1️⃣ Fetching Langfuse traces...", file=sys.stderr)
    traces = fetch_langfuse_traces_7day(limit=200)
    langfuse_analysis = analyze_langfuse_traces(traces)
    print(f"   ✅ {langfuse_analysis.get('trace_count', 0)} traces analyzed", file=sys.stderr)

    # Analyze local analytics
    print("2️⃣ Analyzing local video events...", file=sys.stderr)
    local_analysis = analyze_local_analytics()
    print(f"   ✅ {local_analysis.get('total_video_events', 0)} video events loaded", file=sys.stderr)

    # Build HTML
    print("3️⃣ Building dashboard...", file=sys.stderr)
    html = build_dashboard_html(langfuse_analysis, local_analysis)

    # Save JSON
    combined = {
        "date_range": f"{(datetime.now(timezone.utc) - timedelta(days=7)).date()} to {datetime.now(timezone.utc).date()}",
        "langfuse": langfuse_analysis,
        "local_analytics": local_analysis,
    }
    json_file = REPORTS_DIR / "7day_analytics.json"
    json_file.write_text(json.dumps(combined, indent=2), encoding="utf-8")
    print(f"   ✅ Saved: {json_file}", file=sys.stderr)

    # Save HTML
    html_file = REPORTS_DIR / "7day_dashboard.html"
    html_file.write_text(html, encoding="utf-8")
    print(f"   ✅ Saved: {html_file}", file=sys.stderr)

    print()
    print("=" * 70)
    print("7-DAY ANALYTICS SUMMARY")
    print("=" * 70)
    print(f"KB Queries: {langfuse_analysis.get('trace_count', 0)}")
    print(f"Answer Rate: {langfuse_analysis.get('answer_rate_pct', 0)}%")
    print(f"Video Attachment: {langfuse_analysis.get('video_attach_rate_pct', 0)}%")
    print(f"Local Video Events: {local_analysis.get('total_video_events', 0)}")
    print(f"P50 Latency: {langfuse_analysis.get('latency_p50_ms', 'N/A')}ms")
    print("=" * 70)

if __name__ == "__main__":
    main()
