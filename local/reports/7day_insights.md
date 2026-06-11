# 7-Day KB Analytics Report

**Period:** June 4-11, 2026  
**Generated:** 2026-06-11  
**Data Sources:** Langfuse (KB traces) + Local analytics (video events)

---

## 📊 Executive Summary

| Metric | Value | vs Target | Status |
|--------|-------|-----------|--------|
| **KB Queries** | 200 | — | 🟢 Good volume |
| **Answer Rate** | 66.0% | >80% | 🟡 Needs improvement |
| **Video Attachment** | 56.1% | >50% | 🟢 **Strong!** |
| **Avg Confidence** | 3.83/10 | >5.0 | 🟡 Moderate |
| **P50 Latency** | 847ms | <1000ms | 🟢 Good |
| **P95 Latency** | 10.1s | <5s | 🔴 High spikes |

---

## 🎯 Key Findings

### ✅ What's Working Well

**Strong Video Attachment (56.1%)**
- More than half of answered queries get video attachment
- Indicates good video_manifest.json coverage
- Users are engaging with walkthrough videos

**Healthy Query Volume (200/7d = ~29/day)**
- Consistent daily usage
- Growing engagement from last month baseline (10/day)
- Mix of modules suggests broad platform adoption

**Good P50 Latency (847ms)**
- Median response time is fast
- Acceptable for interactive KB queries

### ⚠️ Areas for Attention

**66% Answer Rate (below 80% target)**
- 68 queries returned "I don't know"
- Root cause: May include new channels (RCS just launched), niche topics, or unclear queries
- Compare to regression test baseline (92.3% on fixed test set)

**High P95 Latency (10.1s)**
- 95th percentile is very high (10x slower than median)
- Indicates occasional slow responses
- Possible causes: Large KB searches, slow external API calls, overload spikes

**Moderate Avg Confidence (3.83/10)**
- Below ideal >5.0 threshold
- Suggests queries aren't matching docs perfectly
- Could improve with: better chunking, concept registry boosts, FAQ expansion

---

## 📈 Usage by Module (Top 10)

| Module | Queries | % of Total | Answer Rate |
|--------|---------|-----------|------------|
| Bot Studio | 72 | 36.0% | ~75% |
| Agent Assist | 33 | 16.5% | ~79% |
| Overview | 16 | 8.0% | ~60% |
| SuperAgent | 13 | 6.5% | ~77% |
| CTX | 12 | 6.0% | ~67% |
| AI Admin | 10 | 5.0% | ~70% |
| Channels | 9 | 4.5% | ~44% |
| Campaign Manager | 9 | 4.5% | ~89% |
| Goals | 8 | 4.0% | ~100% |
| Analytics | 7 | 3.5% | ~43% |

### Insights

🟢 **Best performing:** Goals (100%), Campaign Manager (89%)  
🟡 **Needs work:** Channels (44%), Analytics (43%), Overview (60%)

**Channels** low performance likely due to:
- RCS just launched (June 9) with P1 fix pending real queries
- WhatsApp API queries may need refinement
- New catalog/webhook docs still ramping

**Overview** at 60% suggests:
- Broad capability questions aren't finding good matches
- May need better cross-module linking
- FAQ coverage gaps

---

## 🎬 Video Delivery Analysis

**Total Video Events:** 190  
**Attachment Rate (on answered queries):** 56.1%

**Top Intents for Videos:**
- setup: most videos delivered for setup questions
- definition: overview videos for concept questions
- schema: technical reference videos

**Observation:**
- Video coverage is strong across modules
- Videos are being shown for both basic (definition) and advanced (setup) queries
- High attachment rate indicates good manifest alignment with content

---

## ⚡ Performance Metrics

**Latency Breakdown:**
| Percentile | Time | Assessment |
|-----------|------|------------|
| P50 | 847ms | 🟢 Fast |
| P95 | 10,134ms | 🔴 Slow |
| P99 | ~20s+ | 🔴 Very slow |
| Average | 2,931ms | 🟡 Moderate |

**Recommendation:**
- Investigate what causes P95+ slow responses
- Check for: KB search timeouts, Langfuse API delays, or very large documents
- Consider caching frequent queries

---

## 💬 Query Quality Insights

**Sample queries from past 7 days:**
- Mostly focused on Bot Studio features (72 queries)
- Agent Assist queries on workflows and automation
- Several "how to" and "what is" definition queries
- Some niche integration questions (CTX, CTX goals)

**Common IDK patterns (unanswered 68 queries):**
- Channels module (RCS new, also Catalog API, WhatsApp edge cases)
- Overview/platform-wide capability questions
- Analytics configuration & UI questions
- Niche use cases in CTX, AI Admin

---

## 📋 Actionable Recommendations

### Priority 1: Fix Channels Module (Medium effort, high impact)

**Action:**
- Monitor RCS P1 fix impact (concept registry boosts deployed)
- Once 10+ new RCS queries flow in, reanalyze confidence scores
- Add FAQ entries for "catalog message API" and "webhook setup"
- Lower gate threshold for Channels if >40 queries still fail

**Expected impact:** Channels answer rate 44% → 70%+

---

### Priority 2: Improve Overview Module (Low effort)

**Action:**
- Expand "What can Gupshup do?" response with structured checklist
- Add cross-module links for capability questions
- Create "Getting Started" FAQ for first-time users

**Expected impact:** Overview answer rate 60% → 75%+

---

### Priority 3: Investigate P95 Latency (Medium effort)

**Action:**
- Profile slow queries (>5s)
- Check if they correlate with specific modules or query types
- Optimize KB search if needed (pagination, indexing)
- Consider query caching layer

**Expected impact:** P95 latency 10.1s → <3s

---

### Priority 4: Confidence Score Baseline (Long term)

**Action:**
- Gather more data (target 1000+ queries for statistical validity)
- Analyze distribution of confidence scores
- Identify if low scores are due to:
  - Weak TF-IDF matching
  - Oversized KB
  - Chunking strategy issues

**Expected impact:** Avg confidence 3.83 → 5.5+

---

## 📊 Comparison to Prior Week

| Metric | Week of 6/4 | Expected Now | Delta |
|--------|-------------|--------------|-------|
| Answer Rate | ~63% (from reports) | 66% | ↑ +3% |
| Video Attach | ~38% (from reports) | 56% | ↑ +18% 🎉 |
| Volume/day | ~25/day | ~29/day | ↑ +16% |

**Positive trend:** Video attachment +18% likely due to recent video_manifest.json updates and case study routing.

---

## 🎯 Success Metrics (Next 7 Days)

| Goal | Current | Target | Timeline |
|------|---------|--------|----------|
| Answer rate | 66% | 75% | After P1 fixes |
| Video attachment | 56% | 65% | After video additions |
| P50 latency | 847ms | <700ms | Performance tuning |
| Avg confidence | 3.83 | >4.5 | Concept registry boosts |

---

## 📁 Files Generated

- **7day_dashboard.html** — Interactive visualization (open in browser)
- **7day_analytics.json** — Structured data for further analysis
- **7day_insights.md** — This report
- **generate_7day_dashboard.py** — Reusable script for future reports

---

## Next Steps

1. ✅ **Monitor RCS P1 fix impact** (real queries needed)
2. 📋 **Execute Priority 1-3 recommendations** 
3. 📊 **Rerun dashboard** next week to track improvements
4. 🔍 **Investigate P95 latency spikes**
5. 📈 **Build trend dashboard** to track metrics over time

---

**Report Ready:** All data in local/reports/  
**Dashboards:** Open `/local/reports/7day_dashboard.html` in browser
