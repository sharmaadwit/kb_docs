#!/usr/bin/env python3
"""
Add language analytics section to the comprehensive dashboard.
Analyzes ALL queries from Langfuse (not just IDK samples) for language distribution.
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from base64 import b64encode

def detect_query_language(query: str) -> str:
    """Detect language from query text using heuristics."""
    if not query:
        return "English"

    query_lower = query.lower()

    # Character-based detection
    has_portuguese = any(c in query_lower for c in "ãõçé")
    has_spanish = any(c in query_lower for c in "áéíóú¿¡ñ")
    has_arabic = any(ord(c) >= 0x0600 and ord(c) <= 0x06FF for c in query)

    if has_arabic:
        return "Arabic"
    if has_portuguese:
        return "Portuguese"
    if has_spanish:
        return "Spanish"

    return "English"


def fetch_langfuse_traces(days: int = 7):
    """Fetch ALL traces from Langfuse for comprehensive language analysis."""
    # Load .env
    env_path = Path(__file__).parent.parent.parent / ".env"
    env_vars = {}
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                env_vars[key.strip()] = val.strip()

    try:
        import urllib.request, urllib.parse

        host = env_vars.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")
        pub = env_vars.get("LANGFUSE_PUBLIC_KEY", "")
        sec = env_vars.get("LANGFUSE_SECRET_KEY", "")

        if not (pub and sec):
            print("⚠️  Langfuse credentials missing")
            return None

        creds = b64encode(f"{pub}:{sec}".encode()).decode()
        headers = {"Authorization": f"Basic {creds}"}

        from_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")
        all_traces = []
        page = 1

        while True:
            params = urllib.parse.urlencode({"page": page, "limit": 100, "fromTimestamp": from_date})
            url = f"{host}/api/public/traces?{params}"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read())

            batch = body.get("data", [])
            all_traces.extend(batch)
            print(f"   📥 Page {page}: {len(batch)} traces")

            if not batch:
                break
            if len(all_traces) >= body.get("meta", {}).get("totalItems", len(all_traces)):
                break
            page += 1

        print(f"✅ Fetched {len(all_traces)} total traces")
        return all_traces

    except Exception as e:
        print(f"⚠️  Could not fetch traces: {e}")
        return None


def analyze_language_stats(traces: list) -> dict:
    """Analyze language statistics from ALL traces."""
    language_stats = defaultdict(lambda: {
        "count": 0, "answered": 0, "idk": 0,
        "total_confidence": 0.0, "idk_samples": []
    })

    for trace in traces:
        metadata = trace.get("metadata", {})
        query = metadata.get("query", trace.get("input", {}).get("query", ""))

        if not query:
            continue

        lang = detect_query_language(query)

        is_answered = metadata.get("answered", False)
        is_idk = metadata.get("unanswered", False)
        score = metadata.get("top_score") or 0.0

        language_stats[lang]["count"] += 1

        if is_answered:
            language_stats[lang]["answered"] += 1
        if is_idk:
            language_stats[lang]["idk"] += 1
            language_stats[lang]["idk_samples"].append({
                "query": query[:70],
                "module": metadata.get("module_label", "General"),
                "score": score
            })

        language_stats[lang]["total_confidence"] += score

    # Calculate percentages and averages
    for lang in language_stats:
        stats = language_stats[lang]
        if stats["count"] > 0:
            stats["answer_rate"] = round(stats["answered"] / stats["count"] * 100, 1)
            stats["idk_rate"] = round(stats["idk"] / stats["count"] * 100, 1)
            stats["avg_confidence"] = round(stats["total_confidence"] / stats["count"], 2)

        # Sort IDK samples by score descending, keep top 5
        stats["idk_samples"].sort(key=lambda x: x["score"], reverse=True)
        stats["idk_samples"] = stats["idk_samples"][:5]

    return dict(language_stats)


def generate_language_html(lang_stats: dict) -> str:
    """Generate HTML for language analytics section."""
    # Sort by count
    sorted_langs = sorted(lang_stats.items(), key=lambda x: x[1]["count"], reverse=True)

    html = """
        <!-- 🌍 Language Analytics Section -->
        <div class="section">
            <h2>🌍 Language Analytics (All 7-Day Queries)</h2>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                <!-- Report 1: Language Distribution (Pie Chart) -->
                <div style="background: #f8f9fa; padding: 16px; border-radius: 8px;">
                    <h3 style="font-size: 1em; margin-bottom: 12px;">📊 Query Distribution by Language</h3>
                    <canvas id="languageDistributionChart" style="max-height: 200px;"></canvas>
                </div>

                <!-- Report 2: Answer Rate by Language (Bar Chart) -->
                <div style="background: #f8f9fa; padding: 16px; border-radius: 8px;">
                    <h3 style="font-size: 1em; margin-bottom: 12px;">✅ Answer Rate by Language</h3>
                    <canvas id="answerRateByLanguageChart" style="max-height: 200px;"></canvas>
                </div>
            </div>

            <!-- Report 3: Language Performance Metrics -->
            <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="font-size: 1em; margin-bottom: 12px;">🔥 Language Performance Metrics</h3>
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background: #e9ecef;">
                            <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">Language</th>
                            <th style="padding: 10px; text-align: center; border-bottom: 2px solid #dee2e6;">Queries</th>
                            <th style="padding: 10px; text-align: center; border-bottom: 2px solid #dee2e6;">Answer Rate</th>
                            <th style="padding: 10px; text-align: center; border-bottom: 2px solid #dee2e6;">IDK Rate</th>
                            <th style="padding: 10px; text-align: center; border-bottom: 2px solid #dee2e6;">Avg Confidence</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    # Add rows
    for lang, stats in sorted_langs:
        if stats["count"] == 0:
            continue

        answer_rate = stats.get("answer_rate", 0)
        idk_rate = stats.get("idk_rate", 0)
        color = "#d4edda" if answer_rate >= 65 else "#fff3cd" if answer_rate >= 50 else "#f8d7da"

        html += f"""
                        <tr style="border-bottom: 1px solid #dee2e6;">
                            <td style="padding: 10px;"><strong>{lang}</strong></td>
                            <td style="padding: 10px; text-align: center;">{stats['count']}</td>
                            <td style="padding: 10px; text-align: center; background: {color}; border-radius: 4px;"><strong>{answer_rate:.1f}%</strong></td>
                            <td style="padding: 10px; text-align: center;">{idk_rate:.1f}%</td>
                            <td style="padding: 10px; text-align: center;">{stats.get('avg_confidence', 0):.2f}</td>
                        </tr>
"""

    html += """
                    </tbody>
                </table>
            </div>

            <!-- Report 4: Top IDK Queries by Language (Tabs) -->
            <div style="background: #f8f9fa; padding: 16px; border-radius: 8px;">
                <h3 style="font-size: 1em; margin-bottom: 12px;">❌ Top IDK Queries by Language</h3>
                <div style="margin-bottom: 12px;">
"""

    # Language tabs
    for i, (lang, stats) in enumerate(sorted_langs):
        if stats["count"] == 0:
            continue
        active = "background: white; border-bottom: 3px solid #667eea;" if i == 0 else "background: #e9ecef;"
        html += f"""
                    <button style="padding: 8px 16px; margin-right: 4px; border: none; border-radius: 4px 4px 0 0; cursor: pointer; {active}" onclick="showLanguageTab('{lang}')">
                        {lang} ({stats['count']})
                    </button>
"""

    html += """
                </div>
"""

    # Tab content
    for i, (lang, stats) in enumerate(sorted_langs):
        if stats["count"] == 0:
            continue

        display = "block" if i == 0 else "none"
        html += f"""
                <div id="tab_{lang}" style="display: {display};">
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="background: #e9ecef;">
                                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6;">Query</th>
                                <th style="padding: 10px; text-align: center; border-bottom: 2px solid #dee2e6;">Module</th>
                                <th style="padding: 10px; text-align: center; border-bottom: 2px solid #dee2e6;">Score</th>
                            </tr>
                        </thead>
                        <tbody>
"""

        for sample in stats.get("idk_samples", []):
            score = sample.get("score", 0)
            html += f"""
                            <tr style="border-bottom: 1px solid #dee2e6;">
                                <td style="padding: 10px;">{sample.get('query', 'N/A')}</td>
                                <td style="padding: 10px; text-align: center; font-size: 0.9em;">{sample.get('module', 'General')}</td>
                                <td style="padding: 10px; text-align: center;"><strong>{score:.2f}</strong></td>
                            </tr>
"""

        html += """
                        </tbody>
                    </table>
                </div>
"""

    html += """
            </div>
        </div>

        <script>
            // Wait for Chart.js to load
            function initLanguageCharts() {
                if (typeof Chart === 'undefined') {
                    setTimeout(initLanguageCharts, 100);
                    return;
                }

                // Language distribution pie chart
                try {
                    const languageCtx = document.getElementById('languageDistributionChart');
                    if (languageCtx) {
                        new Chart(languageCtx.getContext('2d'), {
                            type: 'doughnut',
                            data: {
                                labels: [""" + ", ".join(f"'{lang}'" for lang, _ in sorted_langs if _["count"] > 0) + """],
                                datasets: [{
                                    data: [""" + ", ".join(str(stats.get('count', 0)) for _, stats in sorted_langs if stats["count"] > 0) + """],
                                    backgroundColor: ['#667eea', '#2ecc71', '#f39c12', '#e74c3c']
                                }]
                            },
                            options: { responsive: true, maintainAspectRatio: true, plugins: { legend: { position: 'bottom' } } }
                        });
                    }
                } catch(e) { console.error('Chart 1 error:', e); }

                // Answer rate by language bar chart
                try {
                    const answerCtx = document.getElementById('answerRateByLanguageChart');
                    if (answerCtx) {
                        new Chart(answerCtx.getContext('2d'), {
                            type: 'bar',
                            data: {
                                labels: [""" + ", ".join(f"'{lang}'" for lang, _ in sorted_langs if _["count"] > 0) + """],
                                datasets: [{
                                    label: 'Answer Rate %',
                                    data: [""" + ", ".join(str(stats.get('answer_rate', 0)) for _, stats in sorted_langs if stats["count"] > 0) + """],
                                    backgroundColor: '#2ecc71'
                                }]
                            },
                            options: { responsive: true, maintainAspectRatio: true, scales: { y: { beginAtZero: true, max: 100 } } }
                        });
                    }
                } catch(e) { console.error('Chart 2 error:', e); }
            }

            // Tab switching
            function showLanguageTab(lang) {
                document.querySelectorAll('[id^="tab_"]').forEach(el => el.style.display = 'none');
                document.getElementById('tab_' + lang).style.display = 'block';
            }

            // Initialize when DOM is ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initLanguageCharts);
            } else {
                initLanguageCharts();
            }
        </script>
"""

    return html


def inject_language_section(dashboard_path: str):
    """Inject language analytics section into dashboard HTML."""
    # Read dashboard
    with open(dashboard_path) as f:
        html_content = f.read()

    # Add Chart.js library if not already present
    if 'chart.js' not in html_content.lower():
        chart_js = '<script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>'
        html_content = html_content.replace('</head>', f'    {chart_js}\n    </head>')
        print("✅ Added Chart.js library")

    # Fetch fresh traces for comprehensive analysis
    print("🔄 Fetching traces from Langfuse...")
    traces = fetch_langfuse_traces(days=7)

    if traces:
        lang_stats = analyze_language_stats(traces)
        print(f"✅ Analyzed language distribution across all {len(traces)} traces")
    else:
        print("❌ Could not fetch traces")
        return

    # Generate language section
    lang_section = generate_language_html(lang_stats)

    # Find Sample of Remaining IDK section and inject before it
    idk_pattern = r'(<!-- Sample of Remaining IDK Queries -->)'

    if not re.search(idk_pattern, html_content):
        print("⚠️  Could not find insertion point, appending before closing body")
        html_content = html_content.replace('</body>', f'{lang_section}\n    </body>')
    else:
        html_content = re.sub(idk_pattern, f'{lang_section}\n        \\1', html_content)

    # Write updated dashboard
    with open(dashboard_path, 'w') as f:
        f.write(html_content)

    print(f"✅ Language analytics injected into {dashboard_path}")


if __name__ == "__main__":
    dashboard_path = "/Users/adwit.sharma/kb_docs/local/reports/comprehensive_dashboard.html"

    if not Path(dashboard_path).exists():
        print(f"❌ Dashboard file not found: {dashboard_path}")
        exit(1)

    inject_language_section(dashboard_path)
    print("✅ Language analytics updated")
