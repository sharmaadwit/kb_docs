# KB Agent Test Plan: README

**Status:** Ready for deployment  
**Target:** Reduce IDK rate from 42.5% to 20-25% (3 phases)  
**Created:** 2026-06-16

---

## 📚 Documentation Structure

This test plan consists of 4 comprehensive guides:

### 1. **COMPREHENSIVE_TEST_PLAN.md** (Main Document)
The complete test plan with all details:
- 3-phase progression with success metrics
- Test query distribution (10 baseline + 51 IDK + 8 high-score)
- Expected improvements per phase
- Commands to run tests
- Deployment process with rollback strategy

**Read this first** to understand the full scope.

### 2. **TEST_QUICK_REFERENCE.md** (Cheat Sheet)
One-page quick reference with:
- Phase-by-phase test commands (< 1 min each)
- Success checklists for each phase
- Red flags to watch
- Key files and common patterns

**Print this** and keep it handy while testing.

### 3. **TEST_MEASUREMENT_GUIDE.md** (How to Measure)
Detailed guide on measuring improvements:
- 4 measurement methods (local tests, regression suite, Langfuse, dashboard)
- Baseline snapshot procedures
- Success metrics by phase
- Troubleshooting guide for common issues

**Use this** when you need to verify progress.

### 4. **TEST_QUERY_SETS.md** (Test Data)
Complete test query catalog:
- Q1-Q10 baseline queries with explanations
- IDK1-IDK51 real production failures from Langfuse
- HS1-HS8 high-score failures
- CSV format for bulk testing

**Reference this** when adding or modifying test queries.

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Understand the Goal
- **Current state:** 42.5% IDK rate (baseline)
- **Target:** 20-25% IDK rate
- **Method:** 3 phases of targeted improvements
- **Timeline:** Phase 1 (day 1), Phase 2 (day 2-7), Phase 3 (week 2)

### Step 2: Run Baseline Test
```bash
cd /Users/adwit.sharma/kb_docs
python3 local/test_10_queries.py
# Expected: 6/10 answered (Q6-Q9 should be IDK before Phase 1)
```

### Step 3: Apply Phase 1 Fixes
Edit `skill/kb_answer.py`:
- Lines 204-209: Lower confidence thresholds
- Lines 2088-2132: Add concept boosts
- Lines 4295-4306: Improve evidence selection
- Lines 4403-4408: Lower coverage thresholds

### Step 4: Verify Phase 1
```bash
python3 local/test_10_queries.py
# Expected: 9/10 answered ✅
python3 local/tests/test_regression.py
# Expected: >95% passed ✅
```

### Step 5: Monitor & Iterate
```bash
python3 local/scripts/analyze_all_recent.py
# Check: IDK rate 35-38%, answer rate 62-65%
```

---

## 📊 Test Plan at a Glance

### Phase 1: Confidence Thresholds
**Target:** 42.5% → 35-38% IDK  
**Effort:** Low (4 code changes)  
**Time:** Day 1 (30 min implementation, 6+ hours monitoring)  
**Success:** 9/10 baseline test + >95% regression suite  

**What it fixes:**
- Q6: Salesforce webhook sync
- Q7: WABA + webhook configuration
- Q8: API rate limits
- Q9: First campaign creation

### Phase 2: Coverage & Scoring
**Target:** 35-38% → 25-30% IDK  
**Effort:** Medium (registry expansion + entity improvements)  
**Time:** Day 2-7 (implementation varies, 24h monitoring per change)  
**Success:** 45+/51 IDK queries answered  

**What it fixes:**
- High-value IDK queries from real production (Langfuse)
- Entity detection for better concept matching
- Coverage thresholds per intent
- Fallback chains for uncertain matches

### Phase 3: Advanced Optimizations
**Target:** 25-30% → 20-25% IDK  
**Effort:** High (composition + edge cases)  
**Time:** Week 2+ (implementation varies)  
**Success:** 7+/8 high-score queries fixed  

**What it fixes:**
- High-score false positives (search found but answer IDK)
- Multi-section answer composition
- Graceful degradation patterns
- Documentation gaps

---

## ✅ Success Metrics

### Baseline (Before Testing)
```
IDK Rate:           42.5%
Answer Rate:        57.5%
Q1-Q10 Pass Rate:   60% (Q6-Q9 IDK)
Regression Suite:   95%+ (baseline)
```

### Phase 1 Complete
```
IDK Rate:           35-38%  ← 42.5% → 38% = 4.5% improvement
Answer Rate:        62-65%
Q1-Q10 Pass Rate:   90% (9/10)
Regression Suite:   95%+ (maintained)
Q6-Q9 Status:       ALL ANSWERED ✅
```

### Phase 2 Complete
```
IDK Rate:           25-30%  ← 38% → 27% = 11% improvement
Answer Rate:        70-75%
IDK Queries Fixed:  45+/51 (88%+)
Module Rates:       All >75% answer rate
```

### Phase 3 Complete
```
IDK Rate:           20-25%  ← 27% → 22% = 5% improvement (53% total)
Answer Rate:        75-80%
High-Score Queries: 7-8/8 (88-100%)
False Positive Rate: <1%
```

---

## 🎯 How to Use This Plan

### For Phase 1 (Confidence Fixes)
1. Read: `COMPREHENSIVE_TEST_PLAN.md` Section "Phase 1"
2. Implement: Edit `skill/kb_answer.py` per instructions
3. Test: `python3 local/test_10_queries.py`
4. Verify: `python3 local/tests/test_regression.py`
5. Monitor: `python3 local/scripts/analyze_all_recent.py`
6. Check: `TEST_QUICK_REFERENCE.md` Success Checklist

### For Phase 2 (Coverage Fixes)
1. Analyze: `local/reports/idk_regression_baseline.json`
2. Design: Review top 20 IDK queries in `TEST_QUERY_SETS.md`
3. Implement: Concept registry + entity detection improvements
4. Test: `python3 local/run_comprehensive_test.py --phase 2`
5. Measure: `TEST_MEASUREMENT_GUIDE.md` Method 3 (Langfuse)
6. Monitor: `local/scripts/comprehensive_analytics_dashboard.py`

### For Phase 3 (High-Score Fixes)
1. Identify: Query high-score failures from Langfuse
2. Analyze: High scores but IDK responses
3. Implement: Answer composition + evidence filtering
4. Test: `python3 local/run_comprehensive_test.py --phase 3`
5. Measure: Dashboard trends + Langfuse analysis
6. Validate: False positive check via guardrail tests

---

## 📁 File References

### Main Test Files
- `local/test_10_queries.py` — Baseline test (Q1-Q10)
- `local/tests/test_regression.py` — Regression suite (102 tests)
- `local/tests/test_regression_advanced.py` — Phase 2-3 tests
- `local/run_comprehensive_test.py` — All-in-one test runner

### Data Files
- `local/reports/idk_regression_baseline.json` — 51 IDK queries from Langfuse
- `kb/kb_chunks.jsonl` — KB documents (loaded by tests)
- `skill/kb_answer.py` — Main algorithm (edit here for fixes)

### Analysis Scripts
- `local/scripts/fetch_recent_idk.py` — Get latest IDK traces
- `local/scripts/analyze_all_recent.py` — Langfuse analytics
- `local/scripts/comprehensive_analytics_dashboard.py` — HTML dashboard

### Documentation
- `COMPREHENSIVE_TEST_PLAN.md` — Full plan with all details
- `TEST_QUICK_REFERENCE.md` — One-page cheat sheet
- `TEST_MEASUREMENT_GUIDE.md` — How to measure progress
- `TEST_QUERY_SETS.md` — Complete query catalog

---

## 🔍 Troubleshooting Quick Links

| Issue | Solution |
|-------|----------|
| Tests failing after Phase 1 | Check `TEST_QUICK_REFERENCE.md` Red Flags section |
| Not sure if improving | Run `python3 local/scripts/analyze_all_recent.py` |
| Q1 guardrail broken | Look for guardrail bypass in Q1 output - revert changes |
| Confidence too low | Expected in Phase 1; improves in Phase 2 |
| Need to debug specific query | Use pattern in `TEST_MEASUREMENT_GUIDE.md` Pattern 1 |
| Want to compare two runs | Use pattern in `TEST_MEASUREMENT_GUIDE.md` Pattern 2 |
| High-score queries still failing | Wait for Phase 3, check evidence selection logic |

---

## 📞 Support Resources

### For Understanding
- `COMPREHENSIVE_TEST_PLAN.md` — Complete explanation of what, why, how
- `TEST_QUERY_SETS.md` — Detailed breakdown of each test query
- `TEST_MEASUREMENT_GUIDE.md` — In-depth measurement methods

### For Quick Answers
- `TEST_QUICK_REFERENCE.md` — One-page guide with common patterns
- This README — File overview and quick links

### For Implementation
- `COMPREHENSIVE_TEST_PLAN.md` Phase sections — Step-by-step instructions
- `skill/kb_answer.py` — Source code with line numbers referenced

### For Validation
- `TEST_MEASUREMENT_GUIDE.md` — Multiple validation approaches
- Success checklists in `TEST_QUICK_REFERENCE.md`

---

## 📅 Recommended Timeline

**Day 1 (30 min + 6h monitoring):**
- Apply Phase 1 fixes
- Run baseline test → 9/10
- Run regression suite → >95%
- Begin Langfuse monitoring

**Day 2-7 (varies + 24h monitoring per change):**
- Analyze Phase 1 results
- Design Phase 2 improvements
- Implement entity + registry enhancements
- Validate against 51 IDK queries

**Week 2+ (varies + 7d monitoring):**
- Analyze Phase 2 results
- Design Phase 3 optimizations
- Implement answer composition fixes
- Validate against 8 high-score queries
- Reach 20-25% IDK target

---

## 🎓 Learning Path

**New to this project?**
1. Start: This README
2. Then: `TEST_QUICK_REFERENCE.md` (overview)
3. Then: `COMPREHENSIVE_TEST_PLAN.md` (details)
4. Then: `TEST_MEASUREMENT_GUIDE.md` (how to validate)
5. Reference: `TEST_QUERY_SETS.md` (as needed)

**Already familiar?**
1. Skip to: `TEST_QUICK_REFERENCE.md`
2. Jump to: Phase-specific sections in `COMPREHENSIVE_TEST_PLAN.md`
3. Use: `TEST_MEASUREMENT_GUIDE.md` for validation

**Just want to run tests?**
```bash
python3 local/test_10_queries.py                    # Quick (< 1 min)
python3 local/run_comprehensive_test.py --full      # Complete (5-10 min)
python3 local/scripts/analyze_all_recent.py         # Real data (5-10 min)
```

---

## 💡 Key Insights

### Phase 1: Why These Fixes Work
- **Confidence thresholds were too strict** — kb_search found good docs (5.3-14.7 score) but kb_answer rejected them (0.7-1.4 confidence < 1.2 threshold)
- **Solution:** Lower thresholds (1.2→0.8, 4.0→1.0) + concept boosts
- **Result:** Q6-Q9 now use proper documents instead of returning IDK

### Phase 2: Why Coverage Matters
- **51 real IDK queries** show systematic gaps in entity detection, intent classification, and concept registry
- **Solution:** Expand registry, improve entities, refine per-intent thresholds
- **Expected:** Fix 45+ of 51 (88%+)

### Phase 3: Why High-Score Fixes Are Important
- **Evidence quality paradox** — Some queries have very high search scores (10.05 for API nodes) but still return IDK
- **Solution:** Fix evidence selection, answer composition, fallback chains
- **Expected:** 7-8/8 high-score queries answered

---

## ⏱️ Time Investment

| Activity | Time | Frequency |
|----------|------|-----------|
| Run baseline test | <1 min | After each Phase |
| Run regression suite | 2-5 min | After each Phase |
| Test full set (all 69) | 5-10 min | Per Phase completion |
| Langfuse analysis | 5-10 min | Daily during Phase |
| Generate dashboard | 2-3 min | Daily during Phase |
| Code review/implement | 30 min - 2h | Per Phase |
| Monitor & iterate | 6-24h | Per Phase |

**Total for all 3 phases:** ~15 hours (spread over 2 weeks)

---

## ✨ Success Indicators

**Phase 1 Success 🎯**
- Q1-Q10 test: 9/10 ✅
- Regression: >95% ✅
- Q6-Q9 all answered ✅

**Phase 2 Success 🎯**
- IDK rate: 35-38% ✅
- 45+/51 IDK fixed ✅
- Module rates: >75% ✅

**Phase 3 Success 🎯**
- IDK rate: 20-25% ✅
- 7-8/8 high-score fixed ✅
- Overall answer rate: 75-80% ✅

---

## 📞 Questions?

- **"Where's the full plan?"** → `COMPREHENSIVE_TEST_PLAN.md`
- **"How do I test?"** → `TEST_QUICK_REFERENCE.md` + `TEST_MEASUREMENT_GUIDE.md`
- **"What queries should I use?"** → `TEST_QUERY_SETS.md`
- **"Is it working?"** → Run `python3 local/test_10_queries.py`
- **"What's the real IDK rate?"** → Run `python3 local/scripts/analyze_all_recent.py`

---

**Version:** 1.0  
**Date:** 2026-06-16  
**Status:** Ready for Phase 1 Deployment  
**Next Step:** Read `TEST_QUICK_REFERENCE.md` or `COMPREHENSIVE_TEST_PLAN.md`
