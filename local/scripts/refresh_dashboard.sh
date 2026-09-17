#!/bin/bash
# Refresh comprehensive dashboard with latest data from GitHub + Langfuse
# Always fetches and analyzes:
#   - Latest NDJSON files from GitHub
#   - Latest traces from Langfuse API
#   - Both Standalone and CC Express segments (email-based segmentation)

set -e

cd "$(dirname "$0")/../.."

echo "=================================================================================="
echo "DASHBOARD REFRESH: Pull Latest + Analyze Both Segments"
echo "=================================================================================="
echo "📊 This refresh will:"
echo "   ✓ Fetch latest NDJSON analytics from GitHub"
echo "   ✓ Fetch latest traces from Langfuse API"
echo "   ✓ Segment users: Standalone vs CC Express (@ccexpress.gupshup.io)"
echo "   ✓ Generate dual-segment comprehensive dashboard"
echo "=================================================================================="
echo

# Step 1: Fetch latest NDJSON from GitHub
echo "📥 Fetching latest NDJSON from GitHub..."
git fetch origin main > /dev/null 2>&1
DIVERGENT=$(git rev-list --left-right --count origin/main...HEAD 2>/dev/null | awk '{print $2}' || echo "0")
if [ "$DIVERGENT" -gt 0 ]; then
    echo "⚠️  Local commits ahead of origin. Rebasing..."
    # Preserve uncommitted work across the rebase: stash, rebase, then pop.
    STASHED=0
    if ! git diff --quiet || ! git diff --cached --quiet; then
        git stash push -u -m "refresh_dashboard auto-stash" > /dev/null 2>&1 && STASHED=1
    fi
    git pull --rebase origin main 2>&1 | grep -v "Rebasing\|Successfully" || true
    if [ "$STASHED" -eq 1 ]; then
        echo "↩️  Restoring uncommitted changes..."
        git stash pop > /dev/null 2>&1 || echo "⚠️  Could not auto-restore stash; recover with 'git stash pop'"
    fi
else
    git pull origin main 2>&1 | grep -v "Already up to date" || echo "✅ Already up to date"
fi

echo

# Step 2: Regenerate dashboard (which fetches live Langfuse traces)
echo "🔄 Regenerating dashboard with live Langfuse + merged NDJSON..."
python3 local/scripts/generate_analytics_dashboard.py 2>&1 | grep -vE "DeprecationWarning|utcnow\(\)|from_date|timestamp.*isoformat"

echo
echo "=================================================================================="
echo "✅ Dashboard refresh complete!"
echo "=================================================================================="
echo "📁 Files updated:"
echo "   • local/reports/comprehensive_dashboard.html"
echo "   • local/reports/dashboard_analysis.json"
echo
echo "📊 Dashboard contains:"
echo "   • Standalone tab (authenticated Gupshup users)"
echo "   • CC Express tab (users with @ccexpress.gupshup.io email domain)"
echo "   • Parity comparison metrics (answer rate, confidence, volume)"
echo
echo "Next: git status / git diff to review, then commit"
echo "=================================================================================="
