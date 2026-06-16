# KB Test Plan: Quick Reference Card

## 🎯 Target: 42.5% IDK → 20-25% (3 Phases)

### Phase 1: Confidence Thresholds (42.5% → 35-38%)
```bash
# Test it (< 1 min)
python3 local/test_10_queries.py
# Expected: 9/10 passed ✅

# Run the fix
# Edit skill/kb_answer.py lines 204-209, 2088-2132, 4295-4306, 4403-4408
# Changes:
#   MIN_EVIDENCE_SCORE: 1.2 → 0.8
#   MIN_EVIDENCE_SCORE_UNBOOSTED: 4.0 → 1.0
#   Add concept boosts: waba_console, api_rate_limits, campaign_creation
```

### Phase 2: Coverage & Scoring (35-38% → 25-30%)
```bash
# Test it (2-5 min)
python3 local/run_comprehensive_test.py --phase 2
# Expected: 45+/51 passed (88%+)

# Changes (TBD after Phase 1 success):
#   - Expand concept registry (+15-20 concepts)
#   - Improve entity detection
#   - Refine coverage thresholds per intent
#   - Add evidence fallback chains
```

### Phase 3: High-Score Fixes (25-30% → 20-25%)
```bash
# Test it (2-5 min)
python3 local/run_comprehensive_test.py --phase 3
# Expected: 7+/8 passed (88%+)

# Changes (TBD after Phase 2 success):
#   - Answer composition improvements
#   - Evidence filtering refinement
#   - Fallback strategies
#   - Documentation gaps filled
```

---

## 📊 Quick Measurement Commands

### Fastest (< 1 min)
```bash
python3 local/test_10_queries.py
# Shows: Q1-Q10 pass/fail, confidence scores
```

### Complete (2-5 min)
```bash
python3 local/run_comprehensive_test.py --full
# Shows: All 69 queries, phase-by-phase breakdown
```

### Production Reality (5-10 min)
```bash
python3 local/scripts/analyze_all_recent.py
# Shows: Real IDK rate from Langfuse (truth metric)
```

### Visual Dashboard (2-3 min)
```bash
python3 local/scripts/comprehensive_analytics_dashboard.py
open local/reports/comprehensive_dashboard.html
# Shows: Trends, module breakdown, confidence distribution
```

---

## ✅ Success Checklist

### Phase 1 Success
- [ ] Q1-Q10: 9/10 passed
- [ ] Q6-Q9 specifically answered
- [ ] Regression: >95% passed
- [ ] No guardrail bypasses (Q1 still refusal)
- [ ] Confidence scores: 0.8-6.0 range

### Phase 2 Success
- [ ] IDK rate: 35-38% (checked via Langfuse)
- [ ] Answer rate: 62-65%
- [ ] 45+/51 IDK queries now answered
- [ ] All modules >75% answer rate
- [ ] Avg confidence: >3.0

### Phase 3 Success
- [ ] IDK rate: 20-25%
- [ ] Answer rate: 75-80%
- [ ] 7+/8 high-score queries answered
- [ ] Avg confidence: >4.0
- [ ] False positives: <1%

---

## 🔧 Test Query Sets

### Set 1: Baseline (10 queries)
Located in: `local/test_10_queries.py`
- Q1: API keys (expect: refusal)
- Q2-Q5, Q10: Should work (baselines)
- Q6-Q9: Phase 1 focus (currently IDK → should become ANSWERED)

### Set 2: IDK Reduction (51 queries)
Located in: `local/reports/idk_regression_baseline.json`
Real Langfuse failures including:
- console_roles, retail_demo, flow_id
- webhooks_fields, webhook_server_setup
- retained_history, wa_delivery_logs
- ... 43 more real production failures

### Set 3: High-Score Failures (8 queries)
Search scores > 5.0 but currently IDK:
- inapp_support_nodes (10.05)
- webhook_server_setup (9.75)
- webhooks_fields (6.25)
- ... 5 more

---

## 📈 Measurement Targets

| Phase | IDK% | Answer% | Queries Passed | Success Rate |
|-------|------|---------|-----------------|--------------|
| Start | 42.5 | 57.5    | 25/69 (36%)    | Baseline     |
| Phase 1 | 35-38 | 62-65 | 55-58/69 (80%+) | ✅ Main focus |
| Phase 2 | 25-30 | 70-75 | 60-64/69 (87%+) | ✅ Major improvement |
| Phase 3 | 20-25 | 75-80 | 67-69/69 (97%+) | ✅ Near perfect |

---

## 🚨 Red Flags (Stop & Investigate)

- [ ] Q1 guardrail returning answers (security issue!)
- [ ] Regression test <90% (lost baseline functionality)
- [ ] Confidence scores going down (algorithm issue)
- [ ] Latency spike >5s (performance regression)
- [ ] False positives on sensitive queries (safety issue)

---

## 📂 Key Files

| File | Purpose | Phase |
|------|---------|-------|
| `skill/kb_answer.py` | Main KB algorithm | Edit here |
| `local/test_10_queries.py` | Baseline test | All |
| `local/tests/test_regression.py` | 102 test cases | All |
| `local/run_comprehensive_test.py` | All 69 queries | All |
| `local/reports/idk_regression_baseline.json` | 51 real IDK queries | Phase 2 |
| `local/scripts/analyze_all_recent.py` | Langfuse analysis | Validation |
| `COMPREHENSIVE_TEST_PLAN.md` | Detailed plan | Reference |
| `TEST_MEASUREMENT_GUIDE.md` | How to measure | Reference |

---

## 💡 Common Patterns

### Test a specific query
```python
import sys, os, json
sys.path.insert(0, "skill")
import kb_answer as kb

# Load chunks
chunks = [json.loads(l) for l in open("kb/kb_chunks.jsonl") if l.strip()]

# Test query
query = "Your query here"
module = kb._detect_module(query)
entities = kb._extract_entities(query)
intent = kb._classify_intent(query, entities)

# Score and answer
scored = [{"score": kb._score_chunk(query, c, entities, module), **c} 
          for c in chunks]
scored = sorted(scored, key=lambda x: x["score"], reverse=True)
evidence = kb._select_evidence(query, scored, intent, module)
answer = kb._compose_answer(query, intent, entities, evidence, module)

print(f"Answered: {('don\'t know' not in answer.lower())}")
print(f"Confidence: {evidence[0]['score']:.2f if evidence else 0}")
```

### Compare two runs
```bash
python3 local/run_comprehensive_test.py --full -o /tmp/before.json
# (make changes)
python3 local/run_comprehensive_test.py --full -o /tmp/after.json
# Then compare JSON files
```

### Filter failures
```bash
python3 local/run_comprehensive_test.py --full --verbose 2>&1 | grep "❌"
```

---

## 🎯 What Each Phase Fixes

**Phase 1 (Confidence):**
- Q6: Salesforce webhook (0.7 → 0.95 confidence)
- Q7: WABA setup (1.4 → 1.40 after boost)
- Q8: API rate limits (0.95 → 4.45 after boost)
- Q9: First campaign (1.1 → 4.10 after boost)

**Phase 2 (Coverage & Scoring):**
- Expand concept registry from 50 → 70+ concepts
- Improve entity extraction accuracy
- Per-intent coverage thresholds
- Fallback answer chains
- Expected: Fix 45+ of 51 remaining IDK

**Phase 3 (Advanced):**
- Better answer composition from multi-section docs
- High-score false match filtering
- Graceful degradation patterns
- Documentation stub creation
- Expected: Fix 7-8 high-score queries

---

## 📞 When in Doubt

1. **"Does this look right?"** → Run: `python3 local/test_10_queries.py`
2. **"Did I break something?"** → Run: `python3 local/tests/test_regression.py`
3. **"What's the real IDK rate?"** → Run: `python3 local/scripts/analyze_all_recent.py`
4. **"Show me trends"** → Run: `python3 local/scripts/comprehensive_analytics_dashboard.py`
5. **"All tests at once?"** → Run: `python3 local/run_comprehensive_test.py --full`

---

## ⏱️ Time Estimates

| Task | Time | Command |
|------|------|---------|
| Run baseline test | <1 min | `python3 local/test_10_queries.py` |
| Run regression suite | 2-5 min | `python3 local/tests/test_regression.py` |
| Test one phase | 2-5 min | `python3 local/run_comprehensive_test.py --phase 1` |
| Test all phases | 5-10 min | `python3 local/run_comprehensive_test.py --full` |
| Langfuse analysis | 5-10 min | `python3 local/scripts/analyze_all_recent.py` |
| Generate dashboard | 2-3 min | `python3 local/scripts/comprehensive_analytics_dashboard.py` |

---

**Card Version:** 1.0  
**Date:** 2026-06-16  
**Print & keep handy during testing!**
