#!/usr/bin/env bash
# Install a user crontab entry to regenerate the KB analytics dashboard every 3 days.
# Does not modify skill code or remote services.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PY="${PYTHON:-python3}"
MARKER="# kb_docs-analytics-dashboard"
LINE="0 6 */3 * * cd ${ROOT} && set -a && source .env && set +a && ${PY} local/scripts/generate_reports.py >> local/reports/cron.log 2>&1 ${MARKER}"

mkdir -p "${ROOT}/local/reports"

EXISTING="$(crontab -l 2>/dev/null || true)"
if echo "${EXISTING}" | grep -qF "${MARKER}"; then
  echo "Cron entry already installed (${MARKER})"
  exit 0
fi

{
  echo "${EXISTING}"
  echo "${LINE}"
} | crontab -

echo "Installed crontab (every 3 days at 06:00):"
echo "${LINE}"
