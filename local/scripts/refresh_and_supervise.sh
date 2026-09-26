#!/bin/bash
# Rebuild dashboard (fetches latest Langfuse traces), then run supervisor on same fresh data.
# Always run these in sequence — never in parallel — so both operate on the same trace snapshot.

set -e
cd "$(dirname "$0")/../.."

echo "Step 1/2: Dashboard refresh (pulls latest Langfuse traces)..."
bash local/scripts/refresh_dashboard.sh

echo
echo "Step 2/2: Supervisor analysis on fresh data..."
python3 -m local.supervisor.supervisor_agent --report --max-gaps 8 --days 14

echo
echo "Done. Dashboard + supervisor report both on latest data."
