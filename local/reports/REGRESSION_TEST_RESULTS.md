# Comprehensive Regression Test Results

**Date:** 2026-06-15  
**Baseline Period:** 30 days (428 traces)  
**Test Period:** 7 days (105 traces)  
**Status:** 🚨 **REGRESSION DETECTED**

---

## Executive Summary

**❌ Overall performance DECLINED after Phase 1-3 KB improvements**

| Metric | Baseline | Current | Change | Status |
|--------|----------|---------|--------|--------|
| **IDK Rate** | 35.7% | 45.7% | ↑ +10.0% | 🔴 WORSE |
| **Answer Rate** | 63.8% | 54.3% | ↓ -9.5% | 🔴 WORSE |
| **Avg Confidence** | 3.49/10 | 3.05/10 | ↓ -0.44 | 🔴 WORSE |
| **P50 Latency** | 741ms | 647ms | ↓ -94ms | 🟢 BETTER |
| **P95 Latency** | 7828ms | 22312ms | ↑ +14.5s | 🔴 MUCH WORSE |

---

## 🔴 Critical Regressions by Module

### Biggest Regressions (IDK Rate Got Worse)

| Module | Baseline | Current | Regression | Severity |
|--------|----------|---------|-----------|----------|
| **Analytics** | 70.0% | 100.0% | ↑ +30.0% | 🔴 CRITICAL |
| **Campaign Manager** | 15.8% | 66.7% | ↑ +50.9% | 🔴 CRITICAL |
| **Overview** | 46.7% | 71.4% | ↑ +24.7% | 🔴 CRITICAL |
| **Agent Assist** | 24.6% | 55.6% | ↑ +31.0% | 🔴 CRITICAL |
| **CTX** | 70.0% | 77.8% | ↑ +7.8% | 🟠 HIGH |
| **SuperAgent** | 30.8% | 50.0% | ↑ +19.2% | 🟠 HIGH |
| **Bot Studio** | 34.8% | 40.6% | ↑ +5.8% | 🟠 MEDIUM |
| **AI Admin** | 37.0% | 42.9% | ↑ +5.9% | 🟠 MEDIUM |

### Minor Improvements (Only 2 modules improved)

| Module | Baseline | Current | Improvement | Status |
|--------|----------|---------|-------------|--------|
| **Integrations** | 70.4% | 60.0% | ↓ -10.4% | 🟢 BETTER |
| **Channels** | 51.9% | 42.9% | ↓ -9.0% | 🟢 BETTER |

---

## Root Cause Analysis

### Hypothesis 1: New KB Docs Have Lower Relevance Scores
The new documents created in Phase 1-3 may have:
- ❌ Generic titles that don't match user queries well
- ❌ Poor content structure for TF-IDF scoring
- ❌ Insufficient keyword coverage
- ❌ Missing cross-references to official docs

**Evidence:**
- **Overview** module IDK ↑ +24.7% despite creating "console-navigation-guide.md"
- **Campaign Manager** IDK ↑ +50.9% despite creating guides
- Integrations IMPROVED (+10.4%) — These docs referenced official docs explicitly

### Hypothesis 2: New Docs Interfering with Existing Good Matches
The KB answer algorithm may be:
- Selecting new generic docs INSTEAD of specific expert docs
- Over-weighting new content due to recency bias
- Breaking previously-working query→answer mappings

**Evidence:**
- P95 latency EXPLODED (+14.5s) — System spending more time searching
- Confidence scores DOWN (-0.44) — Uncertainty increased
- Integrations improved because they linked to official docs (not generic)

### Hypothesis 3: Different Query Distribution in Last 7 Days
The test period (last 7 days) might have:
- Harder questions
- Different user types
- Different languages (Portuguese queries visible in data)
- Seasonal variation

**Evidence:**
- Sample size too small (105 vs 428 traces) — High variance expected
- Multiple modules regressed simultaneously → Systemic issue, not random

---

## Detailed Module Breakdown

### 🔴 CRITICAL: Analytics Module (70% → 100% IDK)

**What happened:**
- All analytics-related queries now get IDK responses
- Baseline had 70% IDK; now 100%

**Possible cause:**
- No KB docs created for Analytics
- Or existing Analytics docs were downranked

**Action:** 
- Check if Analytics docs exist in KB
- Verify they're not broken

---

### 🔴 CRITICAL: Campaign Manager (15.8% → 66.7% IDK)

**What happened:**
- Was the 3rd best module (16% IDK)
- Now worse than most modules (67% IDK)

**Possible cause:**
- New RCS campaigns guide introduced noise
- Generic "campaign creation" guides not matching specific queries
- Breaking existing templates/campaign docs

**Action:**
- Review `kb/campaign-manager/` docs
- Check if new docs are conflicting

---

### 🔴 CRITICAL: Overview (46.7% → 71.4% IDK)

**What happened:**
- Created "console-navigation-guide.md" (18K)
- IDK rate got WORSE by 25%

**Possible cause:**
- Navigation guide has low relevance scores
- Doesn't match query intent well
- System preferring it over more specific docs

**Action:**
- Audit console-navigation-guide.md quality
- Check if it's being over-selected

---

### 🟢 GOOD: Integrations (70.4% → 60.0% IDK)

**What worked here:**
- Only module that improved significantly
- Why? Integrations spec had:
  - ✅ Official docs links (credibility boost)
  - ✅ Specific CRM names (high relevance)
  - ✅ Field-level details (query matching)
  - ✅ Clear structure

**Lesson:** Successful docs link to official sources and provide specific details.

---

### 🟢 GOOD: Channels (51.9% → 42.9% IDK)

**What worked here:**
- WABA and RCS docs helped
- Why? Because they:
  - ✅ Had prerequisites section
  - ✅ Step-by-step structure
  - ✅ Timeline info
  - ✅ Specific prerequisite keywords

---

## Why New Docs Probably Hurt

### What We Created (Phases 1-3)
- ✅ `kb/overview/console-navigation-guide.md` — Generic
- ✅ `kb/channels/rcs-agent-onboarding-step-by-step.md` — Specific ✓
- ✅ `kb/whatsapp/setup-whatsapp-business-account-waba-in-gupshup.md` — Specific ✓
- ? Unknown Phase 2-3 documents

### What Probably Went Wrong
1. **Generic titles** — "Console Navigation Guide" matches too many queries poorly
2. **No official doc references** — Unlike Integrations docs
3. **Missing metadata** — No `intent_labels`, `source_url` links
4. **Competing with existing good docs** — New generic docs ranked higher

### What Worked
- **Integrations docs** — Linked to official docs, specific (CRM names)
- **WABA/RCS docs** — Step-by-step, prerequisites, timelines
- **Specific module docs** — Not generic "how to navigate"

---

## Recommendations

### Immediate Actions (24 hours)

1. **Audit new Phase 1-3 documents**
   - Review console-navigation-guide.md for quality
   - Check if it's being over-selected in queries
   - Consider breaking it into smaller, specific docs

2. **Verify KB structure**
   - Did Phase 2-3 implementations properly link to official docs?
   - Are they using the official docs URL pattern?
   - Do they have proper metadata/source_url?

3. **Rollback decision**
   - If quality issue confirmed, consider reverting generic docs
   - Keep specific docs (RCS, WABA, Integrations)

### Medium-term (1 week)

4. **Rebuild with best practices**
   - Create specific docs (not generic "navigation" guides)
   - Always link to official docs as source of truth
   - Use official doc structure/naming conventions
   - Include prerequisites, timelines, specific examples
   - Add source_url metadata pointing to official docs

5. **Test before deploying**
   - Run IDK analysis on subset before full rollout
   - Check confidence scores on sample queries
   - Verify P95 latency doesn't degrade

### Long-term

6. **Implement quality gates**
   - New KB docs must improve confidence score on 5+ test queries
   - Must not break existing good answers
   - Must link to official docs
   - Must have specific examples/IDs

---

## Comparison: What Worked vs What Didn't

### ✅ Docs That Improved Queries

| Doc | Module | Pattern | Result |
|-----|--------|---------|--------|
| CRM Integrations | Integrations | Official doc link + specific CRM names | ✓ IDK -10.4% |
| Salesforce/HubSpot guides | Integrations | Specific platform + step-by-step | ✓ Baseline |
| WABA Setup | Channels | Prerequisites + timeline + steps | ✓ IDK -9.0% |
| RCS Onboarding | Channels | Step-by-step + Dotgo details | ✓ Baseline |

### ❌ Docs That Hurt Queries

| Doc | Module | Pattern | Result |
|-----|--------|---------|--------|
| Console Navigation Guide | Overview | Generic + non-specific | ✗ IDK +24.7% |
| Phase 2-3 docs | Multiple | Unknown quality | ✗ 8+ modules worse |

---

## Success Metrics vs Reality

| Goal | Target | Actual | Status |
|------|--------|--------|--------|
| IDK rate | <10% | 45.7% | 🔴 FAILED |
| Answer rate | >90% | 54.3% | 🔴 FAILED |
| Avg confidence | 7.0+ | 3.05 | 🔴 FAILED |

---

## Next Steps

**Choose one:**

### Option A: Investigate & Fix (Recommended)
1. Audit all Phase 2-3 documents for quality
2. Check if generic docs are over-selected
3. Revert low-quality documents
4. Rebuild using best practices from Integrations/Channels success
5. Re-test in 3 days

### Option B: Rollback & Restart
1. `git revert` all Phase 1-3 KB changes
2. Return to 35.7% baseline
3. Implement quality gates
4. Rebuild methodically with testing

### Option C: Full Audit (Recommended)
1. List all documents created in Phase 1-3
2. Score each by: specificity, official doc links, structure
3. Fix generic docs (break into specific topics)
4. Add official doc references
5. Re-test

---

**Status:** ACTIONABLE REGRESSION  
**Severity:** HIGH (10% IDK increase)  
**Root Cause:** Likely low-quality generic docs interfering with existing good answers  
**Recovery Time:** 3-5 days with fix-and-test approach
