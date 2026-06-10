# RCS Analytics: Recommended Next Steps — Execution Summary

**Date:** 2026-06-10  
**Time:** After performing Steps 1-4  
**Status:** ✅ All steps completed, diagnostics ready

---

## What Was Done

### ✅ Step 1: Run Regression Test
```bash
python3 local/scripts/idk_regression.py --label rcs-followup
```

**Result:** 24/26 (92.3%) — **STABLE**

- No regression from case study routing or marketing docs
- RCS-specific issues are isolated
- System remains healthy

---

### ✅ Step 2: Check RCS Chunk Quality

**Inventory:**
- 9 RCS markdown files
- 187 total chunks indexed
- Coverage: Agent setup, authentication, messaging API, templates, webhooks, FAQ, quickstart, overview

**Distribution:**
- **Well-chunked:** rcs-templates.md (31), rcs-webhooks.md (27), rcs-messaging-api.md (24), rcs-authentication.md (23)
- **Moderately chunked:** rcs-agent-setup.md (20), rcs-api-reference.md (19)
- **Minimal chunking:** rcs-overview.md (12)

**Quality Assessment:**
- ✅ Content is comprehensive and detailed
- ✅ Procedural steps are clear
- ❌ Confidence scores are low (avg 1.37/10)
- ❌ Some queries don't match despite having relevant docs

**Root Cause:** TF-IDF scoring/matching issue, not missing documentation.

---

### ✅ Step 3: Video Manifest Status

**Current:** 🔴 Videos disabled for RCS

**Reason:** Commit 4fd4f9d disabled RCS videos pending RCS-specific video creation

**Action Required:**
1. Create/obtain RCS videos for:
   - Agent setup walkthrough
   - Authentication flow tutorial
   - Sending first message
   - Template compliance

2. Once available, update `kb/video_manifest.json`:
```json
{
  "source": "kb/channels/rcs-agent-setup.md",
  "video_id": "<YOUTUBE_ID>",
  "title": "RCS Agent Setup",
  "default_lang": "en"
}
```

3. Rerun `kb_ingest` to rebuild chunks with video metadata

---

### ✅ Step 4: RCS Query Analysis

| Query | Status | Confidence | Issue |
|-------|--------|-----------|-------|
| RCS Agent Setup & Onboarding | ✅ Answered | 2.05 | None — working as intended |
| RCS Authentication & Credentials | ❌ Unanswered | 1.45 | TF-IDF mismatch despite relevant docs |
| How to enable RCS | ❌ Unanswered | 0.60 | Query too generic, no good chunk match |

**Key Finding:** Documentation exists and is indexed, but query-to-chunk matching is weak.

---

## What The Data Shows

### 📊 Current RCS Performance

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Answer Rate | 33.3% | >80% | 🔴 Critical |
| Total Traces | 3 | 50+ for statistical validity | ⏳ Early data |
| Avg Confidence | 1.37 | >5.0 | 🔴 Very low |
| Video Attachment | 0% | 50%+ | 🔴 Disabled (expected) |
| Avg Latency | 433ms | <1000ms | 🟢 Good |
| Regression Impact | None | Zero regression | 🟢 Good |

### 🎯 What's Working

✅ Agent setup query answered correctly (2.05 confidence)  
✅ System latency acceptable (433ms)  
✅ No regression on other modules  
✅ All 187 RCS chunks successfully indexed  

### ⚠️ What Needs Fixing

❌ 2/3 queries fail despite having relevant docs (1.45 and 0.60 confidence)  
❌ Average confidence is 1.37/10 (gating threshold likely >2-3)  
❌ No query routing to RCS-specific FAQ sections  
❌ Videos disabled (intentional, pending creation)  

---

## Recommended Actions (In Priority Order)

### 🔴 Priority 1: Debug Query Matching for RCS Authentication

**Problem:** Query "RCS Authentication & Credentials authentication flow..." should match rcs-authentication.md but scores only 1.45.

**Investigation:**
- Check if rcs-authentication.md chunks are being retrieved at all
- Verify TF-IDF scoring on authentication keywords
- Check if concept registry has RCS keywords

**Action:**
```python
# Add to skill/kb_answer.py:
# - RCS concept registry booster
# - Query expansion for "credentials" → "client_id", "client_secret", "oauth"
# - Lower gate threshold for RCS queries
```

**Owner:** Skill agent  
**Timeline:** 2-3 hours  
**Effort:** Medium  
**Expected Impact:** Could recover 1-2 answers (raise to 50-67% success rate)

---

### 🟡 Priority 2: Enhance RCS FAQ & Entry Points

**Problem:** Query "How to enable RCS" has no good match (0.60 confidence).

**Solution:**
1. Add FAQ entry to rcs-quickstart.md: "How to enable RCS on my project?"
2. Add cross-link in rcs-overview.md: "To get started, see the 5-step quickstart"
3. Update concept registry: boost "enable", "activate", "deploy" for Channels module

**Owner:** Product/KB team  
**Timeline:** 1 hour  
**Effort:** Low  
**Expected Impact:** Recover 1 answer

---

### 🟠 Priority 3: Video Integration Plan

**Timeline:** 1-2 weeks (pending video creation)

**Videos Needed:**
1. RCS Agent Setup (5-10 min) — walkthrough of console registration
2. Authentication & Tokens (3-5 min) — OAuth2 flow explanation
3. Send Your First Message (3-5 min) — end-to-end demo
4. Template Submission (5-7 min) — compliance & best practices

**Implementation:**
```json
// Add to kb/video_manifest.json
[
  {
    "source": "kb/channels/rcs-agent-setup.md",
    "video_id": "xxxxxx",
    "title": "RCS Agent Setup"
  },
  ...
]
```

**Expected Impact:** 
- Video attachment: 0% → 50-70% (once enabled)
- User engagement on RCS docs: +30-50%
- Perceived quality: significantly improved

---

### 💡 Priority 4: Continuous Monitoring

**Automated daily check:**
```bash
# local/scripts/rcs_analytics.py (already created)
python3 local/scripts/rcs_analytics.py
# Opens: local/reports/rcs_dashboard.html
```

**Alert thresholds:**
- Answer rate < 25% → escalate
- Avg confidence < 1.0 → investigate query quality
- RCS volume spike (>20 queries/day) → increase sample size

---

## Files Generated

| File | Purpose | Location |
|------|---------|----------|
| rcs_dashboard.html | Interactive performance dashboard | local/reports/ |
| rcs_analytics.json | Structured analytics data | local/reports/ |
| rcs_diagnostics_report.md | Detailed investigation findings | local/reports/ |
| rcs_next_steps_summary.md | This document | local/reports/ |
| rcs_analytics.py | Reusable script to refresh data | local/scripts/ |
| idk_regression_rcs-followup.json | Regression test results | local/reports/ |

---

## Next Steps by Role

### Analytics Team
- ✅ Fetch fresh Langfuse data daily (automated via rcs_analytics.py)
- ✅ Monitor answer rate trend (should improve after Priority 1 fix)
- 📋 Weekly report: trace volume, confidence distribution, top queries
- 📋 Alert if answer rate stays <50% after Priority 1 fix applied

### Skill Agent (Code changes)
- 📋 Investigate concept registry for RCS keywords
- 📋 Add RCS-specific query boosts (Priority 1)
- 📋 Test matching on authentication queries
- 📋 Lower gate threshold for new channels if needed

### Product/Marketing
- 📋 Create/source RCS walkthrough videos (4 videos, 20-25 min total)
- 📋 Add FAQ entries to rcs-quickstart.md (Priority 2)
- 📋 Update rcs-overview.md with "Getting Started" section

### Deployment
- 📋 Once Priority 1 fix ready: deploy to Gupshup Console
- 📋 Once videos ready: update video_manifest.json + kb_ingest
- 📋 Monitor post-deployment metrics

---

## Success Criteria

| Milestone | Target | Timeline |
|-----------|--------|----------|
| P1 Investigation complete | Find root cause | 2-3 hours |
| P1 Fix deployed | Answer rate >60% | 1 day after fix |
| FAQ entries added | 3-5 new entries | 1 day |
| Videos sourced | 4 RCS videos identified | 1 week |
| Videos deployed | Videos in manifest | 2 weeks |
| Overall answer rate | >75% (Channels module) | 3 weeks |

---

## Session Recap

**What we learned:**
1. RCS has solid documentation (9 files, 187 chunks)
2. System performance is stable (no regression)
3. Issue is in query-to-chunk matching, not missing docs
4. Only 3 traces so far — early-stage data (need 50+ for confidence)
5. Videos are intentionally disabled, waiting for RCS-specific content

**What we built:**
1. ✅ RCS analytics dashboard (HTML + JSON)
2. ✅ Reusable Langfuse query script
3. ✅ Comprehensive diagnostics report
4. ✅ Prioritized action plan

**Next conversation focus:**
- Execute Priority 1 (concept registry fix) in skill-code chat
- Return here to rerun `rcs_analytics.py` after fix deployed
- Track answer rate improvement

---

**Generated:** 2026-06-10 | **Data Period:** June 8-10 (early, 3 traces) | **Status:** Ready for next phase
