#!/bin/bash
# Cleanup script: remove supervisor run artifacts older than 3 days.
# Safe to run any time — never touches dashboards, skill reports, or KB content.
#
# Cleans:
#   local/reports/supervisor/     — old supervisor markdown reports
#   local/supervisor/logs/        — old run logs
#   local/supervisor/judge_outputs/ — old 4-bucket judge JSON outputs

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DAYS=3

echo "Cleaning data older than ${DAYS} days from ${REPO_ROOT}..."

# Supervisor reports
REPORTS_DIR="${REPO_ROOT}/local/reports/supervisor"
if [ -d "$REPORTS_DIR" ]; then
    count=$(find "$REPORTS_DIR" -name "supervisor_*.md" -mtime +${DAYS} | wc -l | tr -d ' ')
    find "$REPORTS_DIR" -name "supervisor_*.md" -mtime +${DAYS} -delete
    echo "  supervisor reports:   removed ${count} file(s)"
fi

# Supervisor logs
LOGS_DIR="${REPO_ROOT}/local/supervisor/logs"
if [ -d "$LOGS_DIR" ]; then
    count=$(find "$LOGS_DIR" -name "*.log" -mtime +${DAYS} | wc -l | tr -d ' ')
    find "$LOGS_DIR" -name "*.log" -mtime +${DAYS} -delete
    echo "  supervisor logs:      removed ${count} file(s)"
fi

# Judge outputs (subdirectories named PID_timestamp)
JUDGE_DIR="${REPO_ROOT}/local/supervisor/judge_outputs"
if [ -d "$JUDGE_DIR" ]; then
    count=$(find "$JUDGE_DIR" -mindepth 1 -maxdepth 1 -mtime +${DAYS} | wc -l | tr -d ' ')
    find "$JUDGE_DIR" -mindepth 1 -maxdepth 1 -mtime +${DAYS} -exec rm -rf {} + 2>/dev/null || true
    echo "  judge outputs:        removed ${count} dir(s)"
fi

echo "Done."
