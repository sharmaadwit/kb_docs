#!/usr/bin/env python3
"""Generate KB usage analytics reports + HTML dashboard (local only, no skill changes).

Usage:
  set -a && source .env && set +a
  python3 local/scripts/generate_reports.py

Reads: Langfuse (lf CLI), kb/analytics/*.ndjson, kb/kb_chunks.jsonl, kb/video_manifest.json
Writes: local/reports/state.json, local/reports/runs/<date>.json, local/reports/dashboard/index.html
"""
from __future__ import annotations

import json
import sys
from datetime import timedelta
from pathlib import Path

# Allow imports when run as script from repo root
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from analytics_common import (  # noqa: E402
    DASHBOARD_DIR,
    REPORTS_DIR,
    RUNS_DIR,
    STATE_PATH,
    build_corpus,
    count_ndjson_events,
    filter_events,
    load_kb_index,
    load_manifest_index,
    utc_now,
)
from analytics_html import render_dashboard  # noqa: E402
from analytics_reports import (  # noqa: E402
    build_all_reports,
    build_insights,
    daily_trend_series,
    update_state,
)


def _load_state() -> dict:
    if STATE_PATH.is_file():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {}


def _save_state(state: dict) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def main() -> int:
    now = utc_now()
    run_id = now.strftime("%Y-%m-%dT%H%M%SZ")
    since_30d = now - timedelta(days=30)
    since_3d = now - timedelta(days=3)
    since_prev_3d = now - timedelta(days=6)
    until_3d = since_3d

    all_events, all_videos, ingest_meta = build_corpus(since_30d)
    window_30d = filter_events(all_events, since_30d)
    window_3d = filter_events(all_events, since_3d)
    prev_3d = filter_events(all_events, since_prev_3d, until=until_3d)
    videos_30d = [v for v in all_videos if v.ts >= since_30d]

    kb_paths, chunks_per_module = load_kb_index()
    manifest_covered, manifest_entries, pitch_modules = load_manifest_index()

    video_clicks_30d = count_ndjson_events(since_30d, "video.clicked")

    reports = build_all_reports(
        all_events=all_events,
        all_videos=all_videos,
        window_3d=window_3d,
        window_30d=window_30d,
        videos_30d=videos_30d,
        video_clicks_30d=video_clicks_30d,
        prev_3d=prev_3d,
        kb_paths=kb_paths,
        chunks_per_module=chunks_per_module,
        manifest_covered=manifest_covered,
        manifest_entries=manifest_entries,
        pitch_modules=pitch_modules,
    )

    state = _load_state()
    state = update_state(state, all_events, run_id)
    daily_trend = daily_trend_series(state, days=30)

    insights = build_insights(reports, window_30d, window_3d, prev_3d, daily_trend)

    run_meta = {
        "run_id": run_id,
        "generated_at": now.isoformat(),
        "ingest_errors": ingest_meta.get("errors") or [],
        "langfuse_fetched": ingest_meta.get("langfuse_count"),
        "ndjson_rows": ingest_meta.get("ndjson_rows"),
    }

    payload = {
        "meta": run_meta,
        "insights": insights,
        "daily_trend": daily_trend,
        "reports": reports,
    }

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    run_path = RUNS_DIR / f"{now.strftime('%Y-%m-%d')}.json"
    run_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    _save_state(state)

    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    html_path = DASHBOARD_DIR / "index.html"
    html_path.write_text(
        render_dashboard(run_meta, reports, insights, daily_trend),
        encoding="utf-8",
    )

    md_path = RUNS_DIR / f"{now.strftime('%Y-%m-%d')}.md"
    md_lines = [
        f"# KB analytics run {run_id}",
        "",
        "## Executive summary",
        "",
    ]
    for ins in insights:
        md_lines.append(f"- **{ins.get('severity', 'info')}**: {ins.get('text', '')}")
    md_lines.append("")
    md_lines.append(f"Dashboard: `{html_path}`")
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"Wrote {html_path}")
    print(f"Wrote {run_path}")
    print(f"State: {STATE_PATH}")
    print(f"30d queries: {reports.get('summary_counts', {}).get('window_30d', 0)}")
    if ingest_meta.get("errors"):
        print("Warnings:", "; ".join(ingest_meta["errors"]), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
