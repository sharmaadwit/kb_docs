#!/bin/bash
# Refresh comprehensive dashboard with latest data from GitHub + Langfuse
# Always fetches: latest NDJSON files from GitHub, latest traces from Langfuse API

set -e

cd "$(dirname "$0")/../.."

echo "=================================================================================="
echo "DASHBOARD REFRESH: Pull Latest + Regenerate"
echo "=================================================================================="
echo

# Step 1: Fetch latest NDJSON from GitHub
echo "📥 Fetching latest NDJSON from GitHub..."
git fetch origin main > /dev/null 2>&1
DIVERGENT=$(git rev-list --left-right --count origin/main...HEAD 2>/dev/null | awk '{print $2}' || echo "0")
if [ "$DIVERGENT" -gt 0 ]; then
    echo "⚠️  Local commits ahead of origin. Rebasing..."
    git stash > /dev/null 2>&1 || true
    git pull --rebase origin main 2>&1 | grep -v "Rebasing\|Successfully"
else
    git pull origin main 2>&1 | grep -v "Already up to date" || echo "✅ Already up to date"
fi

echo

# Step 2: Regenerate dashboard (which fetches live Langfuse traces)
echo "🔄 Regenerating dashboard with live Langfuse + merged NDJSON..."
python3 local/scripts/generate_analytics_dashboard.py 2>&1 | grep -vE "DeprecationWarning|utcnow\(\)|from_date|timestamp.*isoformat"

echo
echo "✅ Dashboard refresh complete!"
echo "   File: local/reports/comprehensive_dashboard.html"
echo
echo "Next: Review changes and commit locally, or 'git push' to update remote"
