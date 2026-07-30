# Comprehensive KB Agent Test Plan
**Status:** Ready for deployment  
**Date:** 2026-06-16  
**Target:** 3-phase IDK reduction from 42.5% → 20-25%

---

## 📋 Test Overview

This plan validates the KB agent improvements across three phases:
- **Phase 1:** Confidence threshold & concept boosts (42.5% → 35-38% IDK)
- **Phase 2:** Coverage & scoring refinements (35-38% → 25-30% IDK)
- **Phase 3:** Advanced optimizations (25-30% → 20-25% IDK)

### Query Distribution
- **10 baseline queries (Q1-Q10)** — Critical path validation
- **51 IDK queries** — Real production failures from Langfuse
- **8 high-score failures** — Scoring edge cases

**Total: 69 test queries**

---

## 🎯 Phase 1: Confidence Threshold & Concept Boosts
**Expected IDK: 42.5% → 35-38%**

### Test Queries (Q1-Q10: Baseline)

| Q | Query | Expected | Module | Intent | Reason |
|---|-------|----------|--------|--------|--------|
| **Q1** | Where do I find my API keys in the Gupshup Console? | Refusal | General | setup | Guardrail test (security) |
| **Q2** | How do I structure JSON for WhatsApp quick reply buttons? | ANSWERED | Channels | definition | Baseline: should work |
| **Q3** | What's the pattern for collecting user input, validating it, then sending a response in a journey? | ANSWERED | Bot Studio | definition | Baseline: pattern matching |
| **Q4** | How do I set up a WhatsApp Business Account WABA and connect it to Gupshup? | ANSWERED | Channels | setup | Baseline: setup doc |
| **Q5** | What are the steps to onboard an RCS agent through Dotgo RBM Hub? | ANSWERED | Channels | setup | Baseline: RCS setup |
| **Q6** | How do I sync customer data from Salesforce to Gupshup through webhooks? | ANSWERED | Integrations | setup | **FIX TARGET:** Low confidence (0.7 → needs boost) |
| **Q7** | How do I configure a WABA in the Gupshup Console and register webhook endpoints? | ANSWERED | Channels | setup | **FIX TARGET:** Threshold issue (1.4 confidence) |
| **Q8** | What are the API rate limits for sending messages, and how do I handle 429 responses? | ANSWERED | API | schema | **FIX TARGET:** Coverage threshold issue (0.95 → 4.45) |
| **Q9** | What are the steps to create and send my first campaign to 1000 contacts? | ANSWERED | Bot Studio | setup | **FIX TARGET:** Intent coverage (1.1 → 4.10) |
| **Q10** | What's the recommended message design best practice for RCS rich cards to maximize engagement? | ANSWERED | Channels | definition | Baseline: RCS rich cards |

**Success Criteria (Q1-Q10):**
- ✅ Q1 returns refusal (guardrail working)
- ✅ Q2-Q5, Q10 still answered (no regressions)
- ✅ Q6-Q9 all return answers (critical fixes)
- ✅ Overall: 9/10 answered (90%)

### Phase 1 Implementation
**Files to modify:** `skill/kb_answer.py`

1. **Lower confidence thresholds** (lines 204-209):
   ```python
   MIN_EVIDENCE_SCORE = 0.8          # Was 1.2
   MIN_EVIDENCE_SCORE_UNBOOSTED = 1.0    # Was 4.0
   MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI = 0.8  # Was 2.5
   ```

2. **Add concept registry boosts** (lines 2088-2132):
   - `waba_console` → +3.0 (fixes Q7)
   - `api_rate_limits` → +3.5 (fixes Q8)
   - `campaign_creation` → +3.0 (fixes Q9)

3. **Improve evidence selection** (lines 4295-4306):
   Prefer high-scoring chunks for webhook patterns.

4. **Lower coverage thresholds** (lines 4403-4408):
   - Module-matched: 0.2 → 0.15
   - Non-module-matched: 0.4 → 0.3

### Phase 1 Test Command
```bash
cd /Users/adwit.sharma/kb_docs
python3 local/test_10_queries.py
```

**Expected Output:**
```
SUMMARY TABLE
Q1-Q5 (baseline):    4/5 answered (80%)
Q6-Q9 (focus area):  4/4 answered (100%)  ← CRITICAL FIX
Q10 (RCS):           1/1 answered (100%)
OVERALL: 9/10 answered (90%)
```

---

## 📊 Phase 2: Coverage & Scoring Refinements
**Expected IDK: 35-38% → 25-30%**

### Test Queries (51 IDK from Langfuse)

These are real queries from the last 7 days that returned "I don't know" but had searchable documents:

| ID | Query | Module | Top Score | Issue | Fix Target |
|---|-------|--------|-----------|-------|-----------|
| **console_roles** | What are the different console roles and their permissions? | Overview | 1.40 | Coverage threshold too high | Lower threshold |
| **retail_demo** | How would Gupshup Console be used in a retail demo scenario? | CTX | 1.10 | Intent classification issue | Improve intent detection |
| **flow_id** | What is a Flow ID in WhatsApp Flows? | Bot Studio | 5.55 | Exists but not selected | Evidence selection bug |
| **inapp_support_nodes** | How do I create in-app API/JSON/Agent support nodes in Journey Builder? | Bot Studio | 10.05 | High score but IDK | Evidence filtering issue |
| **webhooks_fields** | What fields are available in webhook payloads? | Integrations | 6.25 | Schema query | Intent→schema mapping |
| **webhook_server_setup** | How do I set up a webhook server to receive events from Gupshup? | Integrations | 9.75 | Setup guide exists | Coverage refinement |
| **retained_history** | How is retained chat history handled in Gupshup? | Overview | 1.55 | Definition query | Entity detection |
| **wa_delivery_logs** | How do I access and view WhatsApp delivery logs and status? | Channels | 1.55 | Status/ops feature | Module detection |
| **mo_callback_gg** | How do I set up an MO callback with an external URL? | Bot Studio | 1.10 | Callback pattern | Concept registry |
| **external_event_pt** | How do I trigger an external event from an external system? | Bot Studio | 1.45 | Trigger mechanism | Intent classification |
| ... | 41 more IDK queries | ... | ... | ... | ... |

**Phase 2 Test Data:** Full list in `/Users/adwit.sharma/kb_docs/local/reports/idk_regression_baseline.json`

**Success Criteria (Phase 1 + 2):**
- ✅ 60/61 test queries answered (Q1-Q10 + 51 IDK)
- ✅ IDK rate: 35-38% (down from 42.5%)
- ✅ Confidence scores: avg > 2.5
- ✅ No false positives on sensitive queries

### Phase 2 Test Command
```bash
cd /Users/adwit.sharma/kb_docs
python3 local/test_regression_advanced.py \
  --phase 2 \
  --queries local/reports/idk_regression_baseline.json \
  --output local/reports/phase2_results.json
```

**Expected Output:**
```
Passed: 45-50/51 IDK queries (88-98%)
IDK rate: 35-38%
Top failure reasons:
  - Coverage threshold (3 queries)
  - Entity detection (2 queries)
  - Intent classification (1 query)
```

### Phase 2 Target Fixes

1. **Expand concept registry** (+15-20 concepts):
   - Add domain-specific aliases
   - Map common synonyms
   - Boost related multi-word terms

2. **Improve entity detection** (+5-10 accuracy):
   - Expand entity dictionary
   - Add product/feature names
   - Improve module inference

3. **Refine coverage thresholds** (per-intent basis):
   - Setup: 0.15 (current)
   - Definition: 0.20
   - Schema: 0.25
   - Troubleshooting: 0.10

4. **Add evidence fallback chains**:
   - If kb_search score > 3.0 but no answers: use fallback
   - If multiple modules match: prefer current module
   - If low confidence: add "Related docs" section

---

## 🎓 Phase 3: Advanced Optimizations
**Expected IDK: 25-30% → 20-25%**

### Test Queries (8 High-Score Failures)

These are queries with high search scores (>5.0) but currently returning IDK:

| ID | Query | Search Score | Confidence | Gap | Issue |
|---|-------|--------------|------------|-----|-------|
| **inapp_support_nodes** | In-app API/JSON support nodes | 10.05 | 0.0 | 10.05 | Answer composition |
| **webhook_server_setup** | Webhook server setup | 9.75 | 0.0 | 9.75 | Evidence selection |
| **webhooks_fields** | Webhook payload fields | 6.25 | 0.0 | 6.25 | Schema classification |
| **webhook_v3_modes** | Webhook V3 modes | 5.90 | 0.0 | 5.90 | Mode documentation |
| **journey_complete_email** | Journey completion event | 5.15 | 0.0 | 5.15 | Event handling |
| **template_then_ai** | Template to AI journey migration | 2.40 | 0.0 | 2.40 | Intent mismatch |
| **catalog_api** | Catalog message API usage | 0.85 | 0.0 | 0.85 | API discovery |
| **custom_integrations_example** | Custom REST webhook integration | N/A | N/A | N/A | Missing example doc |

**Phase 3 Test Data:** Generated from real Langfuse high-score failures

**Success Criteria (Phase 1 + 2 + 3):**
- ✅ 67/69 test queries answered (Q1-Q10 + 51 IDK + 8 high-score)
- ✅ IDK rate: 20-25% (down from 42.5%)
- ✅ High-score queries: 95%+ answer rate (gap < 0.5)
- ✅ Confidence distribution: median > 3.0
- ✅ Quality maintained: false positive < 2%

### Phase 3 Test Command
```bash
cd /Users/adwit.sharma/kb_docs
python3 local/test_regression_advanced.py \
  --phase 3 \
  --queries local/reports/high_score_failures.json \
  --output local/reports/phase3_results.json
```

**Expected Output:**
```
High-score queries fixed: 7-8/8 (88-100%)
Phase 3 IDK rate: 20-25%
Cumulative improvement: 42.5% → 20-25% (53% reduction)
```

### Phase 3 Target Fixes

1. **Answer composition improvements** (+3-5 accuracy):
   - Better section selection from multi-section docs
   - Improved summarization for schema questions
   - Event handling pattern detection

2. **Evidence filtering refinement** (+2-3 accuracy):
   - Distinguish between high-score false matches
   - Improve module-intent coordination
   - Add confidence calibration layer

3. **Fallback strategies** (+3-5 accuracy):
   - Progressive answer quality levels
   - "Related docs" for low-confidence
   - Graceful degradation patterns

4. **Documentation gaps** (+2-3 accuracy):
   - Create stub docs for common patterns
   - Add integration examples
   - Document webhook best practices

---

## 📈 Success Metrics

### Baseline → Target Progression

| Metric | Baseline | Phase 1 | Phase 2 | Phase 3 | Status |
|--------|----------|--------|---------|---------|--------|
| **IDK Rate** | 42.5% | 35-38% | 25-30% | 20-25% | 📊 Progressive |
| **Answer Rate** | 57.5% | 62-65% | 70-75% | 75-80% | 📊 Progressive |
| **Avg Confidence** | 2.5 | 3.2 | 3.8 | 4.2 | 📊 Improving |
| **P95 Latency** | <12s | <12s | <12s | <12s | ✅ Stable |
| **False Positives** | <1% | <1% | <1% | <1% | ✅ Controlled |

### Quality Gates (All Phases)

- ✅ Q1 guardrail always blocks API key queries
- ✅ Confidence > 0.5 for all answers
- ✅ Latency < 2s for 95% of queries
- ✅ No syntax errors in responses
- ✅ Evidence properly cited (source + confidence visible in Langfuse)

---

## 🛠️ How to Run Tests

### Full Test Suite (All Phases)

```bash
cd /Users/adwit.sharma/kb_docs

# Phase 1: Baseline + fixes
echo "=== PHASE 1 TEST ==="
python3 local/test_10_queries.py
python3 local/tests/test_regression.py --verbose

# Phase 2: IDK reduction
echo "=== PHASE 2 TEST ==="
python3 local/tests/test_regression_advanced.py --phase 2

# Phase 3: High-score fixes
echo "=== PHASE 3 TEST ==="
python3 local/tests/test_regression_advanced.py --phase 3

# All together
echo "=== COMPREHENSIVE TEST ==="
python3 local/run_comprehensive_test.py
```

### Individual Test Categories

```bash
# Just baseline validation
python3 local/test_10_queries.py

# Regression suite (102 tests)
python3 local/tests/test_regression.py

# Advanced regression (51 IDK + 8 high-score)
python3 local/tests/test_regression_advanced.py

# Live Langfuse trace analysis (last 24h/7d)
python3 local/scripts/fetch_recent_idk.py
python3 local/scripts/analyze_all_recent.py
```

### Monitoring Dashboard

```bash
# Generate interactive dashboard
python3 local/scripts/comprehensive_analytics_dashboard.py

# Output: local/reports/comprehensive_dashboard.html
# Open in browser to see:
#   - IDK rate trend (24h, 7d, 30d)
#   - Query success rate by module
#   - Confidence distribution
#   - Latency percentiles
#   - Error analysis
```

---

## 📊 Measurement Methods

### Method 1: Local Query Runner
**What it measures:** Answer quality on known-good queries  
**Time:** <5 min per phase  
**Reliability:** High (uses local chunks)  

```bash
python3 local/test_10_queries.py
# Output: Pass/fail for Q1-Q10
```

### Method 2: Regression Test Suite
**What it measures:** Coverage across all query types  
**Time:** ~2-5 min per suite  
**Reliability:** High (102 test cases)  

```bash
python3 local/tests/test_regression.py --verbose
# Output: Pass/fail for 102 test cases
```

### Method 3: Langfuse Analysis
**What it measures:** Real production behavior  
**Time:** ~5-10 min per analysis  
**Reliability:** Very high (real traces)  
**Requirements:** Langfuse API access

```bash
python3 local/scripts/analyze_all_recent.py
# Output: IDK rate, avg confidence, modules by channel
```

### Method 4: Dashboard Visualization
**What it measures:** Trends and patterns over time  
**Time:** ~2-3 min to generate  
**Reliability:** High (historical data)  

```bash
python3 local/scripts/comprehensive_analytics_dashboard.py
# Output: interactive HTML dashboard
```

### Comparison: Before vs After
**To measure improvement:**

```bash
# Get baseline (before Phase 1 changes)
echo "Recording baseline Langfuse snapshot..."
cp local/reports/comprehensive_analytics.json \
   local/reports/baseline_before_phase1.json

# Apply Phase 1 fixes
# (edit kb_answer.py as per instructions)

# Test Phase 1
python3 local/test_10_queries.py
python3 local/scripts/analyze_all_recent.py > local/reports/phase1_after.json

# Compare
python3 local/scripts/compare_metrics.py \
  --before local/reports/baseline_before_phase1.json \
  --after local/reports/phase1_after.json

# Example output:
# IDK rate: 42.5% → 35-38% (improvement: 7-7.5%)
# Avg confidence: 2.5 → 3.2 (improvement: +0.7)
```

---

## 🎯 Success Criteria Checklist

### Phase 1 Complete When:
- [ ] Q1-Q10 test passes (9/10)
- [ ] Regression test suite passes (>95%)
- [ ] No new guardrail bypasses
- [ ] Latency unchanged (<2s P95)
- [ ] Confidence avg > 3.0

### Phase 2 Complete When:
- [ ] 45+ of 51 IDK queries now answered
- [ ] IDK rate 35-38% (vs 42.5% baseline)
- [ ] Module-specific pass rates > 85%
- [ ] Avg confidence > 3.5
- [ ] No false positives on sensitive topics

### Phase 3 Complete When:
- [ ] High-score queries: 7+/8 answered
- [ ] IDK rate 20-25% (vs 42.5% baseline)
- [ ] Overall answer rate 75-80%
- [ ] Avg confidence > 4.0
- [ ] False positive rate < 1%

---

## 📝 Test Report Template

When running tests, capture:

```markdown
# Test Run Report — Phase [1|2|3]
**Date:** YYYY-MM-DD HH:MM  
**Tester:** [name]  
**Env:** Local/Staging/Production  

## Test Results

### Phase 1 (if applicable)
- Queries passed: 9/10 ✅
- Regression tests: [pass_count]/102
- New issues: [none/list]

### Phase 2 (if applicable)
- IDK queries fixed: [count]/51
- IDK rate: [%]
- By module: [table]

### Phase 3 (if applicable)
- High-score queries: [count]/8
- Final IDK rate: [%]
- Quality metrics: [table]

## Issues Found
- [issue 1]: [description] → FIX: [action]
- [issue 2]: [description] → FIX: [action]

## Recommendation
- [ ] Ready for next phase
- [ ] Needs refinement (Phase X)
- [ ] Hold for investigation

**Approved by:** [name]
```

---

## 🔄 Deployment Process

### Pre-deployment Checklist
1. ✅ All phase tests passing
2. ✅ Langfuse analysis shows improvement
3. ✅ No regression in guardrails
4. ✅ Confidence scores reasonable
5. ✅ Documentation updated
6. ✅ Team reviewed changes

### Deployment Steps

**Step 1: Phase 1 fixes**
```bash
# Backup current version
cp skill/kb_answer.py skill/kb_answer.py.backup.phase0

# Apply Phase 1 changes (thresholds + boosts)
# (Edit lines 204-209, 2088-2132, 4295-4306, 4403-4408)

# Run tests
python3 local/test_10_queries.py  # Must be 9/10
python3 local/tests/test_regression.py  # Must be >95%

# Deploy to staging
git add skill/kb_answer.py
git commit -m "Phase 1: Lower confidence thresholds and add concept boosts"
git push origin main

# Verify on staging (30 min)
# Monitor: /local/reports/comprehensive_dashboard.html
```

**Step 2: Phase 2 fixes** (After 24h monitoring)
```bash
# Backup
cp skill/kb_answer.py skill/kb_answer.py.backup.phase1

# Apply Phase 2 changes (registry + coverage)
# Test
python3 local/tests/test_regression_advanced.py --phase 2

# Deploy + monitor (30 min)
```

**Step 3: Phase 3 fixes** (After 7d monitoring)
```bash
# Backup
cp skill/kb_answer.py skill/kb_answer.py.backup.phase2

# Apply Phase 3 changes (composition + fallbacks)
# Test
python3 local/tests/test_regression_advanced.py --phase 3

# Deploy + monitor (7 days)
```

### Rollback Plan (if needed)
```bash
# Quick rollback to previous phase
cp skill/kb_answer.py.backup.phase[X] skill/kb_answer.py
git add skill/kb_answer.py
git commit -m "Rollback to Phase [X] — [reason]"
git push origin main
```

---

## 📞 Test Support

### Files Referenced
- **Baseline queries:** `local/test_10_queries.py` (Q1-Q10)
- **IDK list:** `local/reports/idk_regression_baseline.json` (51 queries)
- **Regression suite:** `local/tests/test_regression.py` (102 tests)
- **Advanced suite:** `local/tests/test_regression_advanced.py` (59 tests)
- **KB chunks:** `kb/kb_chunks.jsonl` (loaded by tests)
- **Skill source:** `skill/kb_answer.py` (target for changes)

### Key Dashboards
- **Comprehensive:** `local/reports/comprehensive_dashboard.html` (Langfuse analysis)
- **Phase 1:** `local/reports/REGRESSION_TEST_POST_FIX.md` (detailed results)
- **Phase 2:** `local/reports/phase2_results.json` (IDK reduction)
- **Phase 3:** `local/reports/phase3_results.json` (high-score fixes)

### Common Issues

**Q: Test passes locally but fails in production?**  
A: Check KB version mismatch. Run `python3 local/scripts/verify_kb_sync.py` to confirm `kb_chunks.jsonl` matches production.

**Q: Confidence scores too low after Phase 1?**  
A: Expected (0.8-1.0 is fine). They'll improve in Phase 2 with better entity detection.

**Q: Guardrail being bypassed?**  
A: Run `python3 local/test_10_queries.py` — Q1 should always be "Refusal". If not, check `_guardrail_answer()` function.

**Q: How to debug a specific query?**  
A: Edit `local/debug_query.py`, add the query, run it to see full search/answer pipeline with scores.

---

## 📚 Related Documentation

- **Phase 1 Details:** `local/docs/QUICK_WIN_CONCEPT_BOOSTS.md`
- **Concept Registry:** `skill/kb_answer.py` lines 2088-2132
- **Scoring Logic:** `skill/kb_answer.py` lines 3500-3600 (_score_chunk)
- **Evidence Selection:** `skill/kb_answer.py` lines 4290-4330 (_select_evidence)
- **Langfuse Integration:** `skill/kb_answer.py` lines 4650-4700

---

**Created:** 2026-06-16  
**Last Updated:** 2026-06-16  
**Status:** Ready for Phase 1 Deployment  
**Next Review:** After Phase 1 (7-day monitoring)
