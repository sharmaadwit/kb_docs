#!/usr/bin/env python3
"""Fetch RCS traces from Langfuse and generate performance dashboard."""
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[2]
ANALYTICS_DIR = ROOT / "kb" / "analytics"
REPORTS_DIR = ROOT / "local" / "reports"

def _parse_iso(s: str) -> Optional[datetime]:
    """Parse ISO datetime string."""
    if not s:
        return None
    s = s.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None

def fetch_langfuse_rcs_traces(limit: int = 100) -> List[Dict[str, Any]]:
    """Fetch all kb_answer traces from Langfuse, filter for RCS channel."""
    host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")
    pub_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")

    if not pub_key or not secret_key:
        raise RuntimeError("LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY must be set")

    # Use lf CLI to fetch kb_answer traces (with smaller default limit to avoid 502)
    cmd = [
        "lf", "--json", "traces", "list",
        "--name", "kb_answer",
        "--limit", str(limit),
    ]

    print(f"Fetching traces from Langfuse (limit={limit})...", file=sys.stderr)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if proc.returncode != 0:
        err = proc.stderr.strip() or proc.stdout.strip() or "lf failed"
        # Try with smaller limit on error
        if limit > 50:
            print(f"Retrying with smaller limit...", file=sys.stderr)
            return fetch_langfuse_rcs_traces(limit=50)
        raise RuntimeError(err)

    data = json.loads(proc.stdout)
    if not isinstance(data, list):
        raise RuntimeError("unexpected lf output (expected JSON array)")

    # Filter for RCS channel_type
    rcs_traces = []
    for trace in data:
        meta = trace.get("metadata") or {}
        if isinstance(meta, dict) and meta.get("channel_type") == "rcs":
            rcs_traces.append(trace)

    return rcs_traces

def analyze_rcs_traces(traces: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze RCS traces for accuracy and performance metrics."""

    if not traces:
        return {"error": "No RCS traces found", "count": 0}

    modules = Counter()
    modes = Counter()
    intents = Counter()
    statuses = Counter()
    answered = 0
    unanswered = 0
    video_attached = 0
    latencies: List[int] = []
    queries: List[Dict[str, Any]] = []
    scores: List[float] = []

    for t in traces:
        meta = t.get("metadata") or {}
        output = t.get("output") or {}
        input_data = t.get("input") or {}

        # Extract metrics
        modules[meta.get("module_label") or "General"] += 1
        modes[meta.get("selected_answer_mode") or "unknown"] += 1

        for lab in meta.get("intent_labels") or []:
            intents[str(lab)] += 1

        # Determine if answered
        answer = output.get("answer", "") if isinstance(output, dict) else ""
        is_answered = bool("i don't know" not in answer.lower() and answer.strip())

        if meta.get("answered") or is_answered:
            answered += 1
        else:
            unanswered += 1

        if meta.get("video_attached"):
            video_attached += 1

        # Latency
        try:
            lat = int(meta.get("latency_ms") or 0)
            if lat > 0:
                latencies.append(lat)
        except Exception:
            pass

        # Confidence score
        conf = meta.get("confidence")
        if conf:
            try:
                scores.append(float(conf))
            except Exception:
                pass

        # Query details
        query = meta.get("query", "") or input_data.get("query", "")
        if query:
            queries.append({
                "query": query[:100],
                "answered": is_answered,
                "module": meta.get("module_label") or "General",
                "confidence": conf,
                "mode": meta.get("selected_answer_mode"),
            })

        # Status
        status = "answered" if is_answered else "unanswered"
        statuses[status] += 1

    # Compute percentiles
    latencies.sort()
    p50 = latencies[len(latencies) // 2] if latencies else None
    p95 = latencies[int(len(latencies) * 0.95)] if len(latencies) >= 20 else (latencies[-1] if latencies else None)
    p99 = latencies[int(len(latencies) * 0.99)] if len(latencies) >= 100 else None

    avg_score = sum(scores) / len(scores) if scores else None

    total = answered + unanswered

    return {
        "summary": {
            "total_traces": len(traces),
            "answered": answered,
            "unanswered": unanswered,
            "answer_rate_pct": round(100.0 * answered / total, 1) if total else 0,
            "video_attach_rate_pct": round(100.0 * video_attached / answered, 1) if answered else 0,
            "avg_confidence": round(avg_score, 2) if avg_score else None,
        },
        "latency": {
            "p50_ms": p50,
            "p95_ms": p95,
            "p99_ms": p99,
            "avg_ms": round(sum(latencies) / len(latencies), 0) if latencies else None,
        },
        "by_module": dict(modules.most_common()),
        "by_mode": dict(modes.most_common()),
        "by_intent": dict(intents.most_common(15)),
        "by_status": dict(statuses),
        "top_queries": sorted(queries, key=lambda q: (q["answered"], float(q["confidence"] or 0)), reverse=True)[:20],
        "trace_count": len(traces),
    }

def build_html_dashboard(analysis: Dict[str, Any]) -> str:
    """Build HTML dashboard for RCS performance."""

    if "error" in analysis:
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>RCS Analytics - No Data</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .error {{ background: #fee; padding: 20px; border-radius: 8px; color: #c33; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>RCS Analytics Dashboard</h1>
        <div class="error">
            <p><strong>⏳ No RCS traces found yet</strong></p>
            <p>{analysis.get('error')}</p>
            <p>RCS was deployed on June 9, 2026. Check back after usage data flows in.</p>
        </div>
    </div>
</body>
</html>"""

    summary = analysis.get("summary", {})
    latency = analysis.get("latency", {})
    by_module = analysis.get("by_module", {})
    by_mode = analysis.get("by_mode", {})
    by_intent = analysis.get("by_intent", {})
    top_queries = analysis.get("top_queries", [])

    answer_rate = summary.get("answer_rate_pct", 0)
    video_rate = summary.get("video_attach_rate_pct", 0)
    avg_conf = summary.get("avg_confidence", "N/A")

    # Color coding
    answer_color = "#2ecc71" if answer_rate >= 80 else "#f39c12" if answer_rate >= 60 else "#e74c3c"
    video_color = "#2ecc71" if video_rate >= 50 else "#f39c12" if video_rate >= 25 else "#e74c3c"

    module_rows = "".join([
        f"<tr><td>{mod}</td><td align='right'>{count}</td></tr>"
        for mod, count in list(by_module.items())[:10]
    ])

    mode_rows = "".join([
        f"<tr><td>{mode}</td><td align='right'>{count}</td></tr>"
        for mode, count in list(by_mode.items())[:10]
    ])

    intent_rows = "".join([
        f"<tr><td>{intent}</td><td align='right'>{count}</td></tr>"
        for intent, count in list(by_intent.items())[:15]
    ])

    query_rows = "".join([
        f"""<tr>
            <td>{q['query']}</td>
            <td align='center'>{'✅' if q['answered'] else '❌'}</td>
            <td align='right'>{q['confidence'] or 'N/A'}</td>
            <td>{q['module']}</td>
        </tr>"""
        for q in top_queries[:25]
    ])

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>RCS Analytics Dashboard</title>
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

        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .card:hover {{ transform: translateY(-5px); box-shadow: 0 15px 40px rgba(0,0,0,0.15); }}

        .metric {{ margin-bottom: 20px; }}
        .metric-label {{ font-size: 0.85em; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
        .metric-value {{ font-size: 2.5em; font-weight: bold; color: #333; }}
        .metric-unit {{ font-size: 0.5em; color: #999; margin-left: 5px; }}

        .status-good {{ color: #2ecc71; }}
        .status-warning {{ color: #f39c12; }}
        .status-critical {{ color: #e74c3c; }}

        .table-section {{ background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
        .table-section h2 {{ font-size: 1.5em; margin-bottom: 20px; color: #333; }}

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

        .mini-chart {{
            display: inline-block;
            width: 30px;
            height: 30px;
            border-radius: 4px;
            background: #f0f0f0;
            margin-right: 8px;
            vertical-align: middle;
        }}

        .footer {{ text-align: center; color: white; margin-top: 40px; font-size: 0.9em; opacity: 0.8; }}

        .latency-badge {{
            display: inline-block;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .latency-badge.good {{ background: #d4edda; color: #155724; }}
        .latency-badge.warning {{ background: #fff3cd; color: #856404; }}
        .latency-badge.slow {{ background: #f8d7da; color: #721c24; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 RCS Analytics Dashboard</h1>
            <p>Real-time performance metrics for RCS channel questions</p>
        </div>

        <!-- Key Metrics -->
        <div class="grid">
            <div class="card">
                <div class="metric">
                    <div class="metric-label">Total Traces</div>
                    <div class="metric-value">{summary.get("total_traces", 0)}</div>
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">Answer Rate</div>
                    <div class="metric-value status-{('good' if answer_rate >= 80 else 'warning' if answer_rate >= 60 else 'critical')}">
                        {answer_rate}%
                    </div>
                </div>
                <div style="font-size: 0.9em; color: #666;">
                    {summary.get("answered", 0)} answered / {summary.get("unanswered", 0)} unanswered
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">Video Attachment Rate</div>
                    <div class="metric-value status-{('good' if video_rate >= 50 else 'warning' if video_rate >= 25 else 'critical')}">
                        {video_rate}%
                    </div>
                </div>
                <div style="font-size: 0.9em; color: #666;">
                    For answered queries only
                </div>
            </div>

            <div class="card">
                <div class="metric">
                    <div class="metric-label">Avg Confidence Score</div>
                    <div class="metric-value">{avg_conf}</div>
                </div>
                <div style="font-size: 0.9em; color: #666;">
                    Scale: 0-10
                </div>
            </div>
        </div>

        <!-- Latency Metrics -->
        <div class="table-section">
            <h2>⏱️ Latency Performance</h2>
            <div class="grid">
                <div class="card">
                    <div class="metric">
                        <div class="metric-label">P50 (Median)</div>
                        <div class="metric-value">{latency.get("p50_ms") or "N/A"}<span class="metric-unit">ms</span></div>
                    </div>
                </div>
                <div class="card">
                    <div class="metric">
                        <div class="metric-label">P95 (95th percentile)</div>
                        <div class="metric-value">{latency.get("p95_ms") or "N/A"}<span class="metric-unit">ms</span></div>
                    </div>
                </div>
                <div class="card">
                    <div class="metric">
                        <div class="metric-label">P99 (99th percentile)</div>
                        <div class="metric-value">{latency.get("p99_ms") or "N/A"}<span class="metric-unit">ms</span></div>
                    </div>
                </div>
                <div class="card">
                    <div class="metric">
                        <div class="metric-label">Average</div>
                        <div class="metric-value">{latency.get("avg_ms") or "N/A"}<span class="metric-unit">ms</span></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modules Table -->
        <div class="table-section">
            <h2>📦 Distribution by Module</h2>
            <table>
                <thead><tr><th>Module</th><th>Count</th></tr></thead>
                <tbody>
                {module_rows if module_rows else "<tr><td colspan='2'><em>No data</em></td></tr>"}
                </tbody>
            </table>
        </div>

        <!-- Modes Table -->
        <div class="table-section">
            <h2>🎭 Answer Modes</h2>
            <table>
                <thead><tr><th>Mode</th><th>Count</th></tr></thead>
                <tbody>
                {mode_rows if mode_rows else "<tr><td colspan='2'><em>No data</em></td></tr>"}
                </tbody>
            </table>
        </div>

        <!-- Intents Table -->
        <div class="table-section">
            <h2>🎯 Top Intents Detected</h2>
            <table>
                <thead><tr><th>Intent</th><th>Count</th></tr></thead>
                <tbody>
                {intent_rows if intent_rows else "<tr><td colspan='2'><em>No data</em></td></tr>"}
                </tbody>
            </table>
        </div>

        <!-- Top Queries -->
        <div class="table-section">
            <h2>💬 Top Queries</h2>
            <table>
                <thead>
                    <tr>
                        <th>Query Preview</th>
                        <th>Status</th>
                        <th>Confidence</th>
                        <th>Module</th>
                    </tr>
                </thead>
                <tbody>
                {query_rows if query_rows else "<tr><td colspan='4'><em>No data</em></td></tr>"}
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
            <p>Data source: Langfuse API | Channel: RCS | Filter: channel_type=rcs</p>
        </div>
    </div>
</body>
</html>"""

    return html

def main():
    """Main entry point."""
    print("🔄 Fetching RCS traces from Langfuse...", file=sys.stderr)

    try:
        traces = fetch_langfuse_rcs_traces(limit=500)
        print(f"✅ Found {len(traces)} RCS traces", file=sys.stderr)
    except Exception as e:
        print(f"❌ Error fetching traces: {e}", file=sys.stderr)
        # Create error dashboard
        analysis = {"error": str(e), "count": 0}
        html = build_html_dashboard(analysis)
        output_file = REPORTS_DIR / "rcs_dashboard.html"
        output_file.write_text(html, encoding="utf-8")
        print(f"Generated dashboard: {output_file}", file=sys.stderr)
        return

    print("📊 Analyzing traces...", file=sys.stderr)
    analysis = analyze_rcs_traces(traces)

    # Save JSON report
    json_file = REPORTS_DIR / "rcs_analytics.json"
    json_file.write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    print(f"✅ Saved JSON report: {json_file}", file=sys.stderr)

    # Build HTML
    print("🎨 Building HTML dashboard...", file=sys.stderr)
    html = build_html_dashboard(analysis)

    # Save HTML
    output_file = REPORTS_DIR / "rcs_dashboard.html"
    output_file.write_text(html, encoding="utf-8")
    print(f"✅ Generated dashboard: {output_file}", file=sys.stderr)

    # Print summary
    print("\n" + "="*60, file=sys.stderr)
    print("RCS ANALYTICS SUMMARY", file=sys.stderr)
    print("="*60, file=sys.stderr)
    print(f"Total Traces: {analysis.get('summary', {}).get('total_traces', 0)}", file=sys.stderr)
    print(f"Answer Rate: {analysis.get('summary', {}).get('answer_rate_pct', 0)}%", file=sys.stderr)
    print(f"Video Attach: {analysis.get('summary', {}).get('video_attach_rate_pct', 0)}%", file=sys.stderr)
    print(f"Avg Confidence: {analysis.get('summary', {}).get('avg_confidence', 'N/A')}", file=sys.stderr)
    print("="*60, file=sys.stderr)

if __name__ == "__main__":
    main()
