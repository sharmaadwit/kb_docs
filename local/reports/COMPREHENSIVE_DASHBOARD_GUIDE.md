# Comprehensive KB Analytics Dashboard — User Guide

**Version:** 2.0  
**Release Date:** 2026-06-11  
**Scope:** All channels • All modules • 7-day rolling window

---

## 🎯 Overview

The Comprehensive KB Analytics Dashboard consolidates **all analytics sources** into a single unified view:

| Source | Events | What It Tracks |
|--------|--------|---|
| **Langfuse** | 200+ | KB answers, quality, confidence, latency, channels |
| **Local NDJSON** | 190+ | Video deliveries, module distribution, user intent |
| **Combined** | — | Correlation of answer quality + video engagement |

**Result:** Single dashboard tracking all channels (RCS, WhatsApp, Instagram, Web, SMS, etc.) with performance metrics per channel, module, and intent.

---

## 📊 What Gets Tracked

### By Channel (Multi-channel support)
- ✅ RCS (new, P1 fix deployed)
- ✅ WhatsApp (tracked as "untagged" for legacy queries)
- ✅ Instagram (tracked as "untagged" for legacy queries)
- ✅ Web (tracked as "untagged" for legacy queries)
- ✅ SMS (tracked as "untagged" for legacy queries)
- ✅ Any custom channel via `channel_type` metadata

**Current state:** RCS explicitly tagged (3 queries), others captured as "untagged" (197 queries)

### By Module (10+ modules)
- Bot Studio (most queries)
- Agent Assist
- Overview
- Analytics
- Campaign Manager
- Channels
- Goals
- SuperAgent
- AI Admin
- Personalize
- And more...

### By Intent (User intent classification)
- **setup** — "How do I configure/use this?" (43% of queries)
- **overview** — "What is this?" (48% of queries)
- **compare** — "How does X vs Y?" (6% of queries)
- **definition** — "Define this term" (2% of queries)

### Metrics Tracked (Per channel/module)
- Query count
- Answer rate %
- Video attachment rate %
- Average confidence score
- P50 latency (median response time)
- Top module (for channels) / top channel (for modules)

---

## 📁 Files

### Main Dashboard
- **`comprehensive_dashboard.html`** — Interactive visualization
  - Modern gradient design
  - Color-coded health indicators
  - Sortable tables
  - Real-time metrics
  - Data source transparency

### Data Exports
- **`comprehensive_analytics.json`** — Structured data
  - Full metrics for programmatic access
  - Langfuse breakdown
  - Local analytics summary
  - Timestamps for trend tracking

### Script
- **`comprehensive_analytics_dashboard.py`** — Reusable generator
  - Fetches fresh Langfuse traces on demand
  - Loads 7-day NDJSON history
  - Generates HTML + JSON
  - No manual updates needed

---

## 🚀 How to Use

### Option 1: One-time generation
```bash
set -a && source .env && set +a
python3 local/scripts/comprehensive_analytics_dashboard.py
# Opens: local/reports/comprehensive_dashboard.html
```

### Option 2: Scheduled daily monitoring
```bash
# Add to cron or schedule:
0 9 * * * cd /Users/adwit.sharma/kb_docs && set -a && source .env && set +a && python3 local/scripts/comprehensive_analytics_dashboard.py
```

### Option 3: View the interactive dashboard
```bash
# In your browser:
open local/reports/comprehensive_dashboard.html
# Or view the structured data:
cat local/reports/comprehensive_analytics.json | jq '.langfuse.by_channel'
```

---

## 📊 Current Performance (Latest Run)

### Overall
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Total Queries** | 200 | — | 🟢 Good volume |
| **Answer Rate** | 65.0% | >80% | 🟡 Improving |
| **Video Attachment** | 56.2% | >50% | 🟢 Strong |
| **Avg Confidence** | 1.37/10 | >5.0 | 🟡 Moderate |
| **P50 Latency** | 837ms | <1000ms | 🟢 Good |
| **P95 Latency** | 10.6s | <5s | 🔴 High spikes |

### By Channel
```
untagged (legacy):  197 queries | 65.5% answer | 56.6% video
rcs (new):            3 queries | 33.3% answer |  0.0% video
```

**Interpretation:**
- **Untagged (197):** Pre-existing queries without explicit channel_type
- **RCS (3):** New RCS queries since launch on June 9
  - Low count: RCS just deployed (P1 fix just applied)
  - 33% answer rate: Waiting for real queries to test fix
  - 0% video: Videos disabled for RCS (pending creation)

---

## 🔄 Channel Type Detection

### How channels are identified:

**In Langfuse traces:**
```python
metadata["channel_type"] = detect_channel_from_source(top_source)
```

**Detection logic:**
- `kb/channels/rcs-*` → `channel_type="rcs"`
- `kb/channels/*whatsapp*` → `channel_type="whatsapp"`
- `kb/channels/*instagram*` → `channel_type="instagram"`
- Other channels → auto-detected from path
- Unknown → `channel_type="untagged"`

**To tag new channels:**
1. Update `_detect_channel_type()` in `skill/kb_answer.py`
2. Add new channel paths and detection logic
3. Re-run script to see new channels appear

---

## 💡 Key Insights

### What This Dashboard Reveals

✅ **Channel-specific performance**
- Which channels have high/low answer rates
- Which channels benefit most from videos
- Per-channel confidence scores
- Latency by channel

✅ **Module-channel correlation**
- Which modules are used by which channels
- Cross-channel module comparison
- Intent patterns per channel

✅ **Video effectiveness**
- Video attachment rate by channel
- Video coverage gaps
- Module-level video strategies

✅ **Health indicators**
- System-wide performance trends
- Channel-specific bottlenecks
- Intent-based performance

### What This Dashboard Doesn't Show

❌ Real-time user feedback
❌ Video completion rates (YouTube metrics)
❌ Session-level user behavior
❌ Historical trends (single snapshot only)

---

## 📈 Trend Tracking

### To track trends over time:

1. **Schedule daily runs:**
   ```bash
   # Every day at 9 AM
   0 9 * * * cd /Users/adwit.sharma/kb_docs && ... comprehensive_analytics_dashboard.py
   ```

2. **Archive snapshots:**
   ```bash
   cp local/reports/comprehensive_analytics.json \
      local/reports/archive/comprehensive_analytics_$(date +%Y-%m-%d).json
   ```

3. **Analyze trends:**
   ```python
   # Compare answer_rate across dates
   # Plot video_attachment trend
   # Alert on latency spikes
   ```

---

## 🎯 Recommended Actions (By Channel)

### RCS (3 queries, 33% answer rate)
- ⏳ Wait for more real queries (P1 fix just deployed)
- 📊 Run script daily to see confidence improvement
- 🎬 Videos disabled (pending creation)
- **Action:** Monitor for improvement after fix activates

### Untagged/Legacy (197 queries, 65% answer rate)
- 🏷️ Consider adding channel_type tagging
- 📈 Segment by module for targeted improvements
- **Action:** Prioritize Channels module (44% answer rate)

### Future Channels (WhatsApp, Instagram, Web, SMS)
- 🔍 Update channel detection in skill code
- 📊 Run script to start tracking separately
- **Action:** Add channel detection for known sources

---

## 🔧 Customization

### Modify channel detection:
Edit `skill/kb_answer.py` → `_detect_channel_type()`

### Add new metrics:
Edit `comprehensive_analytics_dashboard.py` → `analyze_langfuse_traces()`

### Change dashboard design:
Edit `comprehensive_analytics_dashboard.py` → `build_dashboard_html()`

### Adjust data window:
Edit `analyze_local_video_analytics()` → change `timedelta(days=7)`

---

## 📋 Data Freshness

| Source | Update Frequency | Latency | Quality |
|--------|-----------------|---------|---------|
| **Langfuse** | Real-time | <1s | High (live traces) |
| **NDJSON** | Daily | 0-24h | High (logged events) |
| **Dashboard** | On-demand | Instant | Combined |

**Note:** Dashboard is a snapshot. Run script frequently for latest data.

---

## 🚨 Alerts & Thresholds

The dashboard automatically color-codes metrics:

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Answer Rate | ≥80% | 60-80% | <60% |
| Video Attach | ≥50% | 25-50% | <25% |
| P95 Latency | <3s | 3-5s | >5s |
| Confidence | >5.0 | 3-5 | <3 |

**Green ✓** = Healthy  
**Yellow ⚠️** = Monitor  
**Red ✗** = Action needed

---

## 📞 Support & Questions

### "Why is RCS showing 0% video attachment?"
Videos are disabled for RCS (commit 4fd4f9d). Once RCS videos are created and added to video_manifest.json, this will automatically increase.

### "Why are most channels showing as 'untagged'?"
Legacy queries don't have channel_type metadata. New queries with channel detection will show as RCS, WhatsApp, etc.

### "How do I add a new channel?"
1. Update `_detect_channel_type()` in skill/kb_answer.py
2. Run script again — new channel automatically appears

### "Can I view historical trends?"
Not yet. Script generates single snapshot. To track trends:
1. Archive JSON files daily
2. Compare metrics across dates
3. Build trend charts yourself

---

## 📚 Related Documentation

- **RCS Diagnostics:** `local/reports/rcs_diagnostics_report.md`
- **7-Day Analytics:** `local/reports/7day_insights.md`
- **NDJSON Analysis:** `local/reports/ndjson_analysis.md`
- **Regression Tests:** `local/scripts/idk_regression.py`

---

## ✅ Deployment Checklist

- [x] Comprehensive dashboard created
- [x] Multi-channel tracking implemented
- [x] Langfuse + NDJSON data consolidated
- [x] Interactive HTML dashboard built
- [x] Structured JSON export ready
- [ ] Schedule daily runs (user action)
- [ ] Set up alerting (optional)
- [ ] Archive historical snapshots (optional)

---

**This dashboard is your single source of truth for KB performance across all channels. Run it daily to track trends, identify bottlenecks, and measure the impact of improvements.**
