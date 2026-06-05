# KB usage analytics dashboard (local agent)

Analytics-only tooling: **does not change** `skill/` code. Reads telemetry and KB inventory, writes HTML under `local/reports/`.

## Prerequisites

- `.env` with `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`
- `lf` CLI installed and authenticated
- Optional: `kb/analytics/*.ndjson` and `kb/kb_chunks.jsonl` in the repo

## Run once

```bash
cd /path/to/kb_docs
set -a && source .env && set +a
python3 local/scripts/generate_reports.py
open local/reports/dashboard/index.html
```

## Cron (every 3 days)

```bash
chmod +x local/scripts/install_analytics_cron.sh
./local/scripts/install_analytics_cron.sh
```

Logs append to `local/reports/cron.log`.

## Outputs (gitignored)

| Path | Purpose |
|------|---------|
| `local/reports/state.json` | Cumulative + daily buckets for 30-day trend |
| `local/reports/runs/YYYY-MM-DD.json` | Full report JSON snapshot |
| `local/reports/runs/YYYY-MM-DD.md` | Executive summary markdown |
| `local/reports/dashboard/index.html` | Dashboard |

## Data sources

1. **Langfuse** — `kb_answer` traces (last 30 days, up to 5000 via `lf`)
2. **NDJSON** — `kb/analytics/*.ndjson` (`video.delivered`, `kb_answer_telemetry`, legacy `kb_usage` rows)
3. **Static** — `kb/video_manifest.json`, `kb/kb_chunks.jsonl`

Deduping prefers Langfuse when the same `trace_id` appears in NDJSON.

## Reports included

Coverage (A1–A5), popularity (B1–B7), users (C1–C2), quality (D1–D8), video (E1/E4/E5/E7), ops (F1–F5), investment (G1–G6), rules-based executive insights, 30-day trend chart.

## Legacy CLI

`local/scripts/usage_analytics.py` remains a quick terminal summary; the dashboard supersedes it for qualitative review.
