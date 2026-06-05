"""Static HTML dashboard for KB usage analytics."""
from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from typing import Any, Dict, List


def _esc(s: Any) -> str:
    return html.escape(str(s) if s is not None else "")


def _table(headers: List[str], rows: List[List[Any]]) -> str:
    if not rows:
        return "<p class='muted'>(no data)</p>"
    th = "".join(f"<th>{_esc(h)}</th>" for h in headers)
    body = []
    for row in rows:
        tds = "".join(f"<td>{_esc(c)}</td>" for c in row)
        body.append(f"<tr>{tds}</tr>")
    return f"<table><thead><tr>{th}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def _counter_table(items: List[Dict[str, Any]], label_key: str = "label") -> str:
    rows = [[it.get(label_key), it.get("count"), it.get("pct", "")] for it in (items or [])]
    return _table(["Label", "Count", "Share"], rows)


def _trend_bars(series: List[Dict[str, Any]]) -> str:
    if not series:
        return "<p class='muted'>(no daily data yet)</p>"
    mx = max((d.get("queries") or 0) for d in series) or 1
    parts = []
    for d in series:
        q = d.get("queries") or 0
        h = max(4, int(80 * q / mx))
        parts.append(
            f"<div class='bar-col' title='{_esc(d.get('date'))}: {q} queries'>"
            f"<div class='bar' style='height:{h}px'></div>"
            f"<span class='bar-lbl'>{_esc(str(d.get('date', ''))[5:])}</span></div>"
        )
    return f"<div class='bar-chart'>{''.join(parts)}</div>"


def render_dashboard(
    run_meta: Dict[str, Any],
    reports: Dict[str, Any],
    insights: List[Dict[str, str]],
    daily_trend: List[Dict[str, Any]],
) -> str:
    generated = run_meta.get("generated_at", datetime.now(timezone.utc).isoformat())
    sc = reports.get("summary_counts") or {}

    insight_html = "".join(
        f"<li class='insight {_esc(i.get('severity', 'info'))}'>{_esc(i.get('text', ''))}</li>"
        for i in insights
    )

    lb_rows = [
        [
            r.get("user_email"),
            r.get("queries_30d"),
            r.get("queries_3d"),
            "internal" if r.get("internal") else "external",
            r.get("idk_rate"),
            ", ".join(f"{x.get('label')}({x.get('count')})" for x in (r.get("top_modules") or [])[:3]),
        ]
        for r in (reports.get("C1_user_leaderboard") or [])[:30]
    ]

    backlog_rows = [
        [b.get("module"), b.get("queries"), b.get("idk_rate"), b.get("priority_score"), b.get("avg_top_score")]
        for b in (reports.get("D7_editorial_backlog") or [])
    ]

    matrix_rows = [
        [m.get("module"), m.get("queries"), m.get("answer_rate"), m.get("idk_rate"), m.get("doc_chunks"), m.get("queries_per_100_chunks")]
        for m in (reports.get("G1_investment_matrix") or [])
    ]

    hot_vid_rows = [
        [h.get("source"), h.get("queries"), h.get("module")]
        for h in (reports.get("A2_hot_pages_without_video") or [])
    ]

    idk_mod_rows = [
        [r.get("module"), r.get("queries"), r.get("idk"), r.get("idk_rate")]
        for r in (reports.get("D1_idk_by_module") or [])[:15]
    ]

    unmapped = reports.get("A1_video_manifest_gaps_by_module") or {}
    a1_rows = [[x.get("label"), x.get("count"), x.get("pct")] for x in (unmapped.get("by_module") or [])]

    e1 = reports.get("E1_video_attach_rate") or {}
    meta_errors = run_meta.get("ingest_errors") or []

    sections = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>KB Usage Analytics Dashboard</title>
  <style>
    :root {{
      --bg: #0f1419;
      --card: #1a2332;
      --text: #e7ecf3;
      --muted: #8b9cb3;
      --accent: #3d8bfd;
      --high: #ff6b6b;
      --medium: #ffb347;
      --info: #6bcbff;
    }}
    * {{ box-sizing: border-box; }}
    body {{ font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 1.5rem; line-height: 1.5; }}
    h1 {{ font-size: 1.6rem; margin: 0 0 0.25rem; }}
    h2 {{ font-size: 1.15rem; margin: 2rem 0 0.75rem; border-bottom: 1px solid #2a3548; padding-bottom: 0.35rem; }}
    .meta {{ color: var(--muted); font-size: 0.9rem; margin-bottom: 1.5rem; }}
    nav {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0; }}
    nav a {{ color: var(--accent); text-decoration: none; font-size: 0.85rem; padding: 0.25rem 0.5rem; background: var(--card); border-radius: 4px; }}
    .card {{ background: var(--card); border-radius: 8px; padding: 1rem 1.25rem; margin: 1rem 0; }}
    .kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.75rem; }}
    .kpi {{ background: #243044; padding: 0.75rem; border-radius: 6px; }}
    .kpi strong {{ display: block; font-size: 1.4rem; }}
    .kpi span {{ color: var(--muted); font-size: 0.8rem; }}
    ul.insights {{ list-style: none; padding: 0; margin: 0; }}
    ul.insights li {{ padding: 0.6rem 0.75rem; margin: 0.4rem 0; border-radius: 6px; background: #243044; }}
    li.insight.high {{ border-left: 4px solid var(--high); }}
    li.insight.medium {{ border-left: 4px solid var(--medium); }}
    li.insight.info {{ border-left: 4px solid var(--info); }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.88rem; }}
    th, td {{ text-align: left; padding: 0.45rem 0.6rem; border-bottom: 1px solid #2a3548; }}
    th {{ color: var(--muted); font-weight: 600; }}
    .muted {{ color: var(--muted); }}
    .bar-chart {{ display: flex; align-items: flex-end; gap: 3px; height: 100px; overflow-x: auto; padding-top: 0.5rem; }}
    .bar-col {{ display: flex; flex-direction: column; align-items: center; min-width: 22px; }}
    .bar {{ width: 14px; background: var(--accent); border-radius: 2px 2px 0 0; }}
    .bar-lbl {{ font-size: 0.65rem; color: var(--muted); margin-top: 4px; transform: rotate(-45deg); }}
    pre {{ background: #243044; padding: 0.75rem; overflow: auto; font-size: 0.75rem; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>KB Usage Analytics</h1>
  <p class="meta">Generated {_esc(generated)} · Run {_esc(run_meta.get('run_id', ''))} · Sources: Langfuse + kb/analytics NDJSON + kb index/manifest (read-only)</p>
  {"<p class='muted'>Ingest notes: " + _esc("; ".join(meta_errors)) + "</p>" if meta_errors else ""}

  <nav>
    <a href="#executive">Executive</a>
    <a href="#trend">30-day trend</a>
    <a href="#popularity">Popularity</a>
    <a href="#users">Users</a>
    <a href="#quality">Quality</a>
    <a href="#video">Video</a>
    <a href="#investment">Investment</a>
    <a href="#coverage">Coverage</a>
    <a href="#ops">Ops</a>
  </nav>

  <section id="executive" class="card">
    <h2>Executive summary (rules-based)</h2>
    <ul class="insights">{insight_html}</ul>
    <div class="kpis">
      <div class="kpi"><strong>{sc.get('window_30d', 0)}</strong><span>Queries (30d)</span></div>
      <div class="kpi"><strong>{sc.get('window_3d', 0)}</strong><span>Queries (3d)</span></div>
      <div class="kpi"><strong>{sc.get('all_events_deduped', 0)}</strong><span>All-time deduped</span></div>
      <div class="kpi"><strong>{_esc(e1.get('pct', '—'))}</strong><span>Video attach (LF answers)</span></div>
    </div>
  </section>

  <section id="trend" class="card">
    <h2>30-day query trend</h2>
    {_trend_bars(daily_trend)}
  </section>

  <section id="popularity" class="card">
    <h2>Module popularity (30d)</h2>
    {_counter_table(reports.get('B1_module_popularity_30d'))}
    <h2>Topic popularity — top sources (30d)</h2>
    {_counter_table(reports.get('B2_topic_popularity_30d'))}
    <h2>Intent &amp; mode mix (30d)</h2>
    <h3 class="muted">Intents</h3>
    {_counter_table((reports.get('B3_intent_mode_mix_30d') or {{}}).get('intents'))}
    <h3 class="muted">Modes</h3>
    {_counter_table((reports.get('B3_intent_mode_mix_30d') or {{}}).get('modes'))}
    <h2>Query themes (30d)</h2>
    {_counter_table(reports.get('D3_query_themes_30d'))}
  </section>

  <section id="users" class="card">
    <h2>User leaderboard (full email, 30d)</h2>
    {_table(["Email", "30d", "3d", "Audience", "IDK rate", "Top modules"], lb_rows)}
    <h2>Audience split (30d)</h2>
    <pre>{_esc(json.dumps(reports.get('B5_audience_split_30d'), indent=2))}</pre>
    <h2>Cross-module explorers</h2>
    {_table(["Email", "# modules", "Modules"], [
      [r.get('user_email'), r.get('module_count'), ", ".join(r.get('modules') or [])]
      for r in (reports.get('B4_cross_module_users') or [])
    ])}
  </section>

  <section id="quality" class="card">
    <h2>IDK by module (30d)</h2>
    {_table(["Module", "Queries", "IDK", "IDK rate"], idk_mod_rows)}
    <h2>IDK by top source</h2>
    {_counter_table(reports.get('D1_idk_by_source'))}
    <h2>Editorial backlog (priority)</h2>
    {_table(["Module", "Queries", "IDK rate", "Priority", "Avg score"], backlog_rows)}
    <h2>Sample IDK queries (for editors)</h2>
    <pre>{_esc(json.dumps(reports.get('D8_sample_idk_queries'), indent=2)[:8000])}</pre>
    <h2>Low-confidence answered (samples)</h2>
    <pre>{_esc(json.dumps(reports.get('D2_samples'), indent=2)[:4000])}</pre>
  </section>

  <section id="video" class="card">
    <h2>Video attach rate</h2>
    <pre>{_esc(json.dumps(e1, indent=2))}</pre>
    <h2>High-traffic pages without video</h2>
    {_table(["Source", "Queries", "Module"], hot_vid_rows)}
    <h2>Top videos delivered (30d NDJSON)</h2>
    {_counter_table(reports.get('E4_top_videos_delivered'))}
    <h2>Video backlog (union)</h2>
    <pre>{_esc(json.dumps(reports.get('E7_video_backlog_union'), indent=2))}</pre>
    <h2>Manifest never hit (30d)</h2>
    <pre>{_esc(json.dumps(reports.get('A3_manifest_never_hit'), indent=2)[:5000])}</pre>
  </section>

  <section id="investment" class="card">
    <h2>Investment matrix (volume vs quality)</h2>
    {_table(["Module", "Queries", "Answer %", "IDK %", "Doc chunks", "Q per 100 chunks"], matrix_rows)}
    <h2>Rising demand (3d window)</h2>
    <pre>{_esc(json.dumps(reports.get('G3_rising_demand_3d'), indent=2))}</pre>
    <h2>Voice / WhatsApp / integration interest</h2>
    <pre>{_esc(json.dumps(reports.get('G6_voice_whatsapp_interest'), indent=2))}</pre>
  </section>

  <section id="coverage" class="card">
    <h2>Video manifest gaps by module (static)</h2>
    <p class="muted">Unmapped doc paths: {unmapped.get('unmapped_doc_count', 0)}</p>
    {_table(["Module", "Unmapped docs", "Share"], a1_rows)}
    <h2>KB chunk inventory by module</h2>
    {_counter_table(reports.get('A5_kb_inventory_by_module'))}
    <h2>Sample unmapped paths</h2>
    <pre>{_esc(chr(10).join((unmapped.get('sample_unmapped_paths') or [])[:25]))}</pre>
  </section>

  <section id="ops" class="card">
    <h2>Latency (30d)</h2>
    <pre>{_esc(json.dumps(reports.get('F1_latency'), indent=2))}</pre>
    <h2>Data source mix (30d)</h2>
    <pre>{_esc(json.dumps(reports.get('F2_data_sources_30d'), indent=2))}</pre>
    <h2>Environments</h2>
    {_counter_table(reports.get('F3_environments'))}
    <h2>Search vs answer</h2>
    <pre>{_esc(json.dumps(reports.get('F5_search_vs_answer'), indent=2))}</pre>
    <h2>Clarification / refusal</h2>
    <pre>{_esc(json.dumps(reports.get('D5_clarification_refusal'), indent=2))}</pre>
  </section>

  <p class="muted" style="margin-top:2rem">Re-run: <code>python3 local/scripts/generate_reports.py</code> · Cron: every 3 days via local/scripts/install_analytics_cron.sh</p>
</body>
</html>"""
    return sections
