#!/usr/bin/env python3
"""
Standalone weekly accuracy increment report generator.
Uses cached or live Langfuse traces to generate all-time weekly trend HTML.
"""

import json
import os
import base64
import ssl
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Any, List, Optional

def load_traces_from_langfuse(days: int = 365) -> Optional[List[Dict[str, Any]]]:
    """Fetch traces from Langfuse API (all-time)."""
    import urllib.request
    import urllib.parse
    import base64
    import ssl

    host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")
    pub = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
    sec = os.environ.get("LANGFUSE_SECRET_KEY", "")

    if not pub or not sec:
        return None

    try:
        import certifi
        ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    except:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

    try:
        creds = base64.b64encode(f"{pub}:{sec}".encode()).decode()
        headers = {"Authorization": f"Basic {creds}"}

        from_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")
        all_traces = []
        page = 1

        while True:
            params = urllib.parse.urlencode({"page": page, "limit": 100, "fromTimestamp": from_date})
            url = f"{host}/api/public/traces?{params}"
            req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
                body = json.loads(resp.read())
                batch = body.get("data", [])
                all_traces.extend(batch)
                meta = body.get("meta", {})
                total = meta.get("totalItems", meta.get("total", len(all_traces)))

                if not batch or len(all_traces) >= total:
                    break
                page += 1

        if all_traces:
            print(f"✅ Fetched {len(all_traces)} traces from Langfuse API")
            return all_traces
    except Exception as e:
        print(f"⚠️  Langfuse fetch failed: {e}")

    return None

def load_traces() -> List[Dict[str, Any]]:
    """Load traces from Langfuse first, fall back to cache."""
    # Try live Langfuse API first
    traces = load_traces_from_langfuse(days=365*3)
    if traces:
        return traces

    # Fall back to cache
    cache_path = "archive/local_reports/langfuse_traces_7day_offline.json"
    if os.path.exists(cache_path):
        print(f"📦 Loading traces from cache: {cache_path}")
        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
                traces = data if isinstance(data, list) else [data]
            print(f"✅ Loaded {len(traces)} cached traces")
            return traces
        except Exception as e:
            print(f"⚠️  Cache load failed: {e}")

    return []

def compute_weekly_metrics(traces: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute weekly accuracy metrics from traces."""
    # Filter to kb_answer traces (query traces only)
    kb_traces = [t for t in traces if t.get('name') == 'kb_answer']

    # Group by ISO week
    weekly = defaultdict(lambda: {
        "week": "",
        "query_count": 0,
        "answer_count": 0,
        "idk_count": 0,
        "confidence_sum": 0.0,
        "answer_rate": 0.0,
        "idk_rate": 0.0,
        "avg_confidence": 0.0,
    })

    for t in kb_traces:
        ts_str = t.get('timestamp', '')
        try:
            ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00')).replace(tzinfo=None)
            week = ts.isocalendar()
            week_key = f"{week[0]}-W{week[1]:02d}"
        except:
            continue

        output = t.get('output', {})
        if isinstance(output, str):
            try:
                output = json.loads(output)
            except:
                output = {}

        weekly[week_key]["query_count"] += 1

        # Determine if answer or IDK
        answer_text = output.get('answer', '') if isinstance(output, dict) else ''
        is_idk = 'idk' in str(answer_text).lower()

        if not is_idk:
            weekly[week_key]["answer_count"] += 1
        else:
            weekly[week_key]["idk_count"] += 1

        # Get confidence score
        score = output.get('score', 0) if isinstance(output, dict) else 0
        if isinstance(score, (int, float)):
            weekly[week_key]["confidence_sum"] += score

    # Calculate percentages
    weeks_list = []
    for week_key in sorted(weekly.keys()):
        w = weekly[week_key]
        total = w["query_count"]
        w["week"] = week_key
        w["answer_rate"] = 100 * w["answer_count"] / total if total > 0 else 0
        w["idk_rate"] = 100 * w["idk_count"] / total if total > 0 else 0
        w["avg_confidence"] = w["confidence_sum"] / total if total > 0 else 0
        weeks_list.append(w)

    if not weeks_list:
        return {"weeks": []}

    # Current week is the last one
    current_week = weeks_list[-1]

    # Week-over-week delta
    wow_delta = 0.0
    trend = "→"
    if len(weeks_list) >= 2:
        prev_rate = weeks_list[-2].get("answer_rate", 0)
        curr_rate = current_week.get("answer_rate", 0)
        wow_delta = curr_rate - prev_rate
        if wow_delta > 0.5:
            trend = "📈"
        elif wow_delta < -0.5:
            trend = "📉"
        else:
            trend = "→"

    return {
        "weeks": weeks_list,
        "current_week": current_week,
        "week_over_week_delta": wow_delta,
        "trend": trend,
        "total_weeks": len(weeks_list),
    }

def generate_html(metrics: Dict[str, Any]) -> str:
    """Generate HTML for weekly accuracy report."""
    weeks = metrics.get("weeks", [])
    current = metrics.get("current_week", {})
    wow = metrics.get("week_over_week_delta", 0)
    trend = metrics.get("trend", "→")
    total_weeks = metrics.get("total_weeks", 0)

    if not weeks:
        return "<p>No weekly data available.</p>"

    # Build table rows (show ALL weeks)
    rows = ""
    for w in weeks:
        rows += f"""
            <tr>
                <td><strong>{w["week"]}</strong></td>
                <td>{w["query_count"]}</td>
                <td><strong>{w["answer_rate"]:.1f}%</strong></td>
                <td>{w["idk_rate"]:.1f}%</td>
                <td>{w["avg_confidence"]:.2f}</td>
            </tr>
        """

    html = f"""
            <div style="background: white; border-radius: 12px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 20px;">
                <h2>📊 Weekly Accuracy Increment (All-Time)</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px;">
                    <div style="background: #f0f4ff; padding: 16px; border-radius: 8px;">
                        <div style="font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Current Week Answer Rate</div>
                        <div style="font-size: 2.2em; font-weight: bold; color: #667eea;">{current.get("answer_rate", 0):.1f}%</div>
                    </div>
                    <div style="background: #f0fff4; padding: 16px; border-radius: 8px;">
                        <div style="font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Week-over-Week Change</div>
                        <div style="font-size: 2.2em; font-weight: bold; color: {'#10b981' if wow >= 0 else '#ef4444'};">{wow:+.1f} pp</div>
                    </div>
                    <div style="background: #fef3f2; padding: 16px; border-radius: 8px;">
                        <div style="font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Trend</div>
                        <div style="font-size: 1.5em; font-weight: bold; color: #667eea;">{trend}</div>
                    </div>
                    <div style="background: #f5f3ff; padding: 16px; border-radius: 8px;">
                        <div style="font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Current Week Volume</div>
                        <div style="font-size: 2.2em; font-weight: bold; color: #667eea;">{current.get("query_count", 0)}</div>
                    </div>
                </div>

                <h3 style="margin-top: 20px; margin-bottom: 12px;">📈 Complete Weekly Trend ({total_weeks} weeks)</h3>
                <table style="width: 100%; border-collapse: collapse; font-size: 0.9em;">
                    <thead>
                        <tr style="background: #f9fafb; border-bottom: 2px solid #e5e7eb;">
                            <th style="text-align: left; padding: 12px; font-weight: 600;">Week</th>
                            <th style="text-align: center; padding: 12px; font-weight: 600;">Queries</th>
                            <th style="text-align: center; padding: 12px; font-weight: 600;">Answer Rate</th>
                            <th style="text-align: center; padding: 12px; font-weight: 600;">IDK Rate</th>
                            <th style="text-align: center; padding: 12px; font-weight: 600;">Avg Conf</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
    """
    return html

if __name__ == "__main__":
    print("=" * 80)
    print("WEEKLY ACCURACY INCREMENT REPORT GENERATOR (All-Time)")
    print("=" * 80)
    print()

    traces = load_traces()
    if not traces:
        print("❌ No traces available")
        exit(1)

    print("📊 Computing weekly metrics...")
    metrics = compute_weekly_metrics(traces)

    if not metrics.get("weeks"):
        print("❌ No weekly data found")
        exit(1)

    print(f"✅ Found {metrics['total_weeks']} weeks of data")
    print(f"   Current week: {metrics['current_week'].get('week')}")
    print(f"   Answer rate: {metrics['current_week'].get('answer_rate', 0):.1f}%")
    print(f"   WoW delta: {metrics['week_over_week_delta']:+.1f} pp")

    print("\n📝 Generating HTML report...")
    html = generate_html(metrics)

    output_file = "local/reports/weekly_accuracy_report.html"
    with open(output_file, 'w') as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weekly Accuracy Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f3f4f6;
            padding: 20px;
            margin: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            color: #111827;
            margin-bottom: 10px;
        }}
        .timestamp {{
            color: #6b7280;
            font-size: 0.9em;
            margin-bottom: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Weekly Accuracy Increment Report</h1>
        <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</div>
        {html}
    </div>
</body>
</html>""")

    print(f"✅ Report saved to: {output_file}")
    print("\n📊 Weekly Breakdown:")
    for w in metrics["weeks"]:
        print(f"  {w['week']:10} | {w['query_count']:5} queries | {w['answer_rate']:6.1f}% answer | {w['avg_confidence']:5.2f} conf")
