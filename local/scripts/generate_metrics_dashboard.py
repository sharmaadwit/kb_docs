#!/usr/bin/env python3
"""
Lightweight metrics-only dashboard (fast generation, no conversation analysis).
Focuses on: accuracy metrics, module/intent breakdown, weekly trends.
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

# Get env credentials
LANGFUSE_HOST = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")
LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY", "")

def fetch_traces_simple():
    """Fetch 1 day of traces from Langfuse for quick metrics."""
    if not LANGFUSE_PUBLIC_KEY or not LANGFUSE_SECRET_KEY:
        return []

    import base64
    import urllib.request
    import urllib.parse
    import ssl

    try:
        import certifi
        ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    except:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

    try:
        creds = base64.b64encode(f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}".encode()).decode()
        headers = {"Authorization": f"Basic {creds}"}

        from_date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
        params = urllib.parse.urlencode({"page": 1, "limit": 100, "fromTimestamp": from_date})
        url = f"{LANGFUSE_HOST}/api/public/traces?{params}"

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=ssl_ctx) as resp:
            body = json.loads(resp.read())
            return body.get("data", [])
    except Exception as e:
        print(f"⚠️  Trace fetch failed: {e}")
        return []

def load_cached_traces():
    """Fall back to cached traces."""
    cache_path = "archive/local_reports/langfuse_traces_7day_offline.json"
    if os.path.exists(cache_path):
        try:
            with open(cache_path) as f:
                data = json.load(f)
                return data if isinstance(data, list) else [data]
        except:
            pass
    return []

def compute_metrics(traces):
    """Compute accuracy metrics from traces."""
    if not traces:
        return None

    # Filter to kb_answer traces
    kb_traces = [t for t in traces if t.get("name") == "kb_answer"]
    if not kb_traces:
        return None

    total = len(kb_traces)
    answered = 0
    idk_count = 0
    confidence_sum = 0.0
    modules = defaultdict(int)
    intents = defaultdict(int)

    for t in kb_traces:
        output = t.get("output", {})
        if isinstance(output, str):
            try:
                output = json.loads(output)
            except:
                output = {}

        # Check if answered
        answer_text = str(output.get("answer", "")).lower()
        is_idk = "idk" in answer_text or "don't know" in answer_text

        if not is_idk:
            answered += 1
        else:
            idk_count += 1

        # Get confidence
        score = output.get("score", 0)
        if isinstance(score, (int, float)):
            confidence_sum += score

        # Get module and intent
        metadata = t.get("metadata", {})
        module = metadata.get("module", "General")
        intent = metadata.get("intent", "unknown")

        if module:
            modules[module] += 1
        if intent:
            intents[intent] += 1

    answer_rate = 100 * answered / total if total > 0 else 0
    idk_rate = 100 * idk_count / total if total > 0 else 0
    avg_conf = confidence_sum / total if total > 0 else 0

    return {
        "total_queries": total,
        "answered": answered,
        "idk_count": idk_count,
        "answer_rate": answer_rate,
        "idk_rate": idk_rate,
        "avg_confidence": avg_conf,
        "modules": dict(sorted(modules.items(), key=lambda x: -x[1])[:10]),
        "intents": dict(sorted(intents.items(), key=lambda x: -x[1])[:8]),
    }

def compute_weekly(traces):
    """Compute weekly accuracy metrics."""
    kb_traces = [t for t in traces if t.get("name") == "kb_answer"]

    weekly = defaultdict(lambda: {"total": 0, "answered": 0, "conf_sum": 0})

    for t in kb_traces:
        ts_str = t.get("timestamp", "")
        try:
            ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00")).replace(tzinfo=None)
            week = ts.isocalendar()
            week_key = f"{week[0]}-W{week[1]:02d}"
        except:
            continue

        output = t.get("output", {})
        if isinstance(output, str):
            try:
                output = json.loads(output)
            except:
                output = {}

        weekly[week_key]["total"] += 1

        answer_text = str(output.get("answer", "")).lower()
        if "idk" not in answer_text and "don't know" not in answer_text:
            weekly[week_key]["answered"] += 1

        score = output.get("score", 0)
        if isinstance(score, (int, float)):
            weekly[week_key]["conf_sum"] += score

    weeks = []
    for week_key in sorted(weekly.keys()):
        w = weekly[week_key]
        total = w["total"]
        weeks.append({
            "week": week_key,
            "queries": total,
            "answer_rate": 100 * w["answered"] / total if total > 0 else 0,
            "avg_conf": w["conf_sum"] / total if total > 0 else 0,
        })

    return weeks

def generate_html(metrics, weekly):
    """Generate HTML dashboard."""
    if not metrics:
        return "<p>No data available.</p>"

    # Top modules
    modules_html = ""
    for module, count in sorted(metrics["modules"].items(), key=lambda x: -x[1])[:10]:
        modules_html += f"<tr><td>{module}</td><td>{count}</td></tr>\n"

    # Top intents
    intents_html = ""
    for intent, count in sorted(metrics["intents"].items(), key=lambda x: -x[1])[:8]:
        intents_html += f"<tr><td>{intent}</td><td>{count}</td></tr>\n"

    # Weekly table
    weekly_html = ""
    for w in weekly[-12:]:  # Last 12 weeks
        weekly_html += f"""<tr>
            <td>{w['week']}</td>
            <td>{w['queries']}</td>
            <td><strong>{w['answer_rate']:.1f}%</strong></td>
            <td>{w['avg_conf']:.2f}</td>
        </tr>\n"""

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>KB Metrics Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            color: #333;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: white; margin-bottom: 20px; }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .metric-label {{ font-size: 0.8em; color: #666; text-transform: uppercase; margin-bottom: 8px; }}
        .metric-value {{ font-size: 2.2em; font-weight: bold; color: #667eea; }}
        .section {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        h2 {{ font-size: 1.6em; color: #333; border-bottom: 3px solid #667eea; padding-bottom: 10px; margin-bottom: 20px; }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #ddd;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{ background: #f8f9fa; }}
        .footer {{ text-align: center; color: white; margin-top: 40px; font-size: 0.9em; opacity: 0.8; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 KB Metrics Dashboard (Fast Mode)</h1>

        <div class="metrics">
            <div class="card">
                <div class="metric-label">Total Queries (Last 15d)</div>
                <div class="metric-value">{metrics['total_queries']}</div>
            </div>
            <div class="card">
                <div class="metric-label">Answer Rate</div>
                <div class="metric-value" style="color: #2ecc71;">{metrics['answer_rate']:.1f}%</div>
            </div>
            <div class="card">
                <div class="metric-label">IDK Rate</div>
                <div class="metric-value" style="color: #f39c12;">{metrics['idk_rate']:.1f}%</div>
            </div>
            <div class="card">
                <div class="metric-label">Avg Confidence</div>
                <div class="metric-value">{metrics['avg_confidence']:.2f}</div>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div class="section">
                <h2>🗂️ Top Modules</h2>
                <table>
                    <thead>
                        <tr><th>Module</th><th>Queries</th></tr>
                    </thead>
                    <tbody>
                        {modules_html}
                    </tbody>
                </table>
            </div>

            <div class="section">
                <h2>🎯 Top Intents</h2>
                <table>
                    <thead>
                        <tr><th>Intent</th><th>Count</th></tr>
                    </thead>
                    <tbody>
                        {intents_html}
                    </tbody>
                </table>
            </div>
        </div>

        <div class="section">
            <h2>📈 Weekly Trend (Last 12 Weeks)</h2>
            <table>
                <thead>
                    <tr>
                        <th>Week</th>
                        <th>Queries</th>
                        <th>Answer Rate</th>
                        <th>Avg Confidence</th>
                    </tr>
                </thead>
                <tbody>
                    {weekly_html}
                </tbody>
            </table>
        </div>

        <div class="footer">
            <strong>Data Source:</strong> Langfuse API (Real-time telemetry)
            <br>
            <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
            <br>
            <strong>Mode:</strong> Fast (optimized for speed, metrics-only)
        </div>
    </div>
</body>
</html>"""

    return html

if __name__ == "__main__":
    print("=" * 80)
    print("LIGHTWEIGHT METRICS DASHBOARD GENERATOR (Fast Mode)")
    print("=" * 80)
    print()

    print("🔄 Fetching live traces...")
    traces = fetch_traces_simple()

    if not traces:
        print("⚠️  Live fetch failed, using cached traces...")
        traces = load_cached_traces()

    if traces:
        print(f"✅ Loaded {len(traces)} traces")
    else:
        print("❌ No traces available")
        exit(1)

    print("📊 Computing metrics...")
    metrics = compute_metrics(traces)

    if not metrics:
        print("❌ No metrics computed")
        exit(1)

    print(f"   Total: {metrics['total_queries']} queries")
    print(f"   Answer Rate: {metrics['answer_rate']:.1f}%")
    print(f"   IDK Rate: {metrics['idk_rate']:.1f}%")
    print(f"   Avg Confidence: {metrics['avg_confidence']:.2f}")

    print("📈 Computing weekly trends...")
    weekly = compute_weekly(traces)
    print(f"   {len(weekly)} weeks of data")

    print("📝 Generating HTML...")
    html = generate_html(metrics, weekly)

    output_file = "local/reports/metrics_dashboard.html"
    with open(output_file, 'w') as f:
        f.write(html)

    print(f"✅ Dashboard saved to: {output_file}")
