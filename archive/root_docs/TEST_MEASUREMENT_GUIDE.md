# KB Agent Test Measurement Guide
**Date:** 2026-06-16  
**Purpose:** How to measure improvement from 42.5% IDK to 20-25%

---

## 🎯 Quick Start: Measure Your Phase

### Phase 1 (5 min)
```bash
cd /Users/adwit.sharma/kb_docs
python3 local/test_10_queries.py
# Expected: 9/10 passed (90%)
```

### Phase 2 (5 min)
```bash
python3 local/run_comprehensive_test.py --phase 2
# Expected: 45+/51 passed (88%+)
```

### Phase 3 (5 min)
```bash
python3 local/run_comprehensive_test.py --phase 3
# Expected: 7+/8 passed (88%+)
```

### All Together (10 min)
```bash
python3 local/run_comprehensive_test.py --full
# Expected: 61+/69 passed (88%+)
```

---

## 📊 4 Measurement Methods

### Method 1: Query Test Runner (Fastest)
**Time:** <5 min  
**Scope:** 10 baseline queries (Q1-Q10)  
**Reliability:** High (uses local chunks)  

**Command:**
```bash
python3 local/test_10_queries.py
```

**Output:**
```
SUMMARY TABLE
Q1-Q5 (baseline):    4/5 answered (80%)
Q6-Q9 (focus area):  4/4 answered (100%)
Q10 (RCS):           1/1 answered (100%)
OVERALL: 9/10 answered (90%)
```

**What to measure:**
- Q1-Q5, Q10 still work (regression check)
- Q6-Q9 now answered (fix check)
- Confidence scores > 0.8

**Pass criteria:** 9/10 (90%)

---

### Method 2: Regression Test Suite (Comprehensive)
**Time:** 2-5 min  
**Scope:** 102 test cases across all categories  
**Reliability:** Very high (extensive coverage)  

**Command:**
```bash
python3 local/tests/test_regression.py
# Or with verbose output:
python3 local/tests/test_regression.py --verbose
```

**Output (compact):**
```
REGRESSION TEST SUMMARY
═══════════════════════════════════════════════════════════════
Category     Tests  Pass   Rate    Status
─────────────────────────────────────────────────────────────
A-misroute   6      6      100%    ✅
B-correct    8      8      100%    ✅
C-overview   5      4      80%     ⚠️
D-guardrails 6      6      100%    ✅
E-edge       10     9      90%     ✅
F-thresholds 12    11      92%     ✅
G-registry   15    15      100%    ✅
H-intent     20    18      90%     ✅
I-negatives  20    20      100%    ✅
─────────────────────────────────────────────────────────────
TOTAL        102   97      95%     ✅ PASS
```

**What to measure:**
- Overall pass rate (target: >95%)
- Category pass rates (no 0%)
- Specific failure reasons (printed below summary)

**Pass criteria:** >95% (98+/102)

---

### Method 3: IDK Analysis from Langfuse (Most Realistic)
**Time:** 5-10 min  
**Scope:** Real production traces (last 7-24 hours)  
**Reliability:** Very high (real behavior)  
**Requirements:** Langfuse API access

**Command:**
```bash
python3 local/scripts/fetch_recent_idk.py
python3 local/scripts/analyze_all_recent.py
```

**Output:**
```json
{
  "timestamp": "2026-06-16T14:30:00",
  "period": "last 7 days",
  "total": 200,
  "answered": 150,
  "idk": 50,
  "answer_rate": 75.0,
  "idk_rate": 25.0,
  "by_module": {
    "Bot Studio": {"answered": 45, "idk": 15, "rate": 75.0},
    "Channels": {"answered": 30, "idk": 2, "rate": 93.8},
    "Integrations": {"answered": 25, "idk": 5, "rate": 83.3},
    ...
  },
  "confidence_stats": {
    "mean": 3.8,
    "median": 3.2,
    "p95": 8.5
  }
}
```

**What to measure:**
- IDK rate (target: Phase 1: <38%, Phase 2: <30%, Phase 3: <25%)
- Answer rate (target: Phase 1: >62%, Phase 2: >70%, Phase 3: >75%)
- Module breakdown (any module >50% IDK needs investigation)
- Confidence distribution (mean >3.0)

**Pass criteria:**
- Phase 1: IDK 35-38%, Answer 62-65%
- Phase 2: IDK 25-30%, Answer 70-75%
- Phase 3: IDK 20-25%, Answer 75-80%

---

### Method 4: Visual Dashboard (Easy Trending)
**Time:** 2-3 min to generate  
**Scope:** Historical analysis over 24h/7d/30d  
**Reliability:** High (compiled from Langfuse)  

**Command:**
```bash
python3 local/scripts/comprehensive_analytics_dashboard.py
open local/reports/comprehensive_dashboard.html
```

**What you'll see:**
- Interactive charts:
  - IDK rate over time (24h, 7d, 30d)
  - Answer rate by module
  - Confidence score distribution
  - P95 latency trends
  - Video attachment rates

**What to measure:**
- Trend direction (should be down for IDK, up for answers)
- Module performance (which are improving fastest)
- Confidence increasing over time
- No spikes or regressions

**Pass criteria:** Clear downward trend in IDK rate

---

## 📈 Baseline Snapshot (For Comparison)

Before starting Phase 1, capture your baseline:

```bash
# Save baseline state
cp local/reports/comprehensive_analytics.json \
   local/reports/baseline_phase0.json

python3 local/test_10_queries.py > local/reports/baseline_phase0_queries.txt
python3 local/tests/test_regression.py > local/reports/baseline_phase0_regression.txt
```

After each phase, compare:

```bash
# Phase 1 results
python3 local/run_comprehensive_test.py --quick \
  --output local/reports/phase1_results.json

# Compare metrics
python3 << 'EOF'
import json

with open('local/reports/baseline_phase0.json') as f:
    baseline = json.load(f)

with open('local/reports/phase1_results.json') as f:
    phase1 = json.load(f)

print(f"IDK Rate: {baseline['idk_rate']:.1f}% → {phase1['idk_rate']:.1f}%")
print(f"Improvement: {baseline['idk_rate'] - phase1['idk_rate']:.1f} percentage points")
print(f"Relative improvement: {((baseline['idk_rate'] - phase1['idk_rate']) / baseline['idk_rate'] * 100):.1f}%")
EOF
```

---

## 🎯 Success Metrics by Phase

### Phase 1 Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Q1-Q10 pass rate | ≥90% | `python3 local/test_10_queries.py` → count passes |
| Regression pass rate | ≥95% | `python3 local/tests/test_regression.py` → read summary |
| Q6-Q9 answered | 4/4 | `python3 local/test_10_queries.py` → look for "ANSWERED" |
| Confidence >0.8 | ✅ | `python3 local/test_10_queries.py` → check Q6-Q9 confidence |
| No guardrail bypasses | ✅ | `python3 local/test_10_queries.py` → Q1 must be refusal |
| Latency stable | <2s P95 | Langfuse dashboard → check latency chart |

### Phase 2 Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| IDK rate | 35-38% | `python3 local/scripts/analyze_all_recent.py` → read `idk_rate` |
| Answer rate | 62-65% | Same as above → read `answer_rate` |
| IDK queries fixed | ≥45/51 | `python3 local/run_comprehensive_test.py --phase 2` → count passes |
| Module rates | >75% each | Langfuse dashboard → by_module breakdown |
| Avg confidence | >3.0 | Same → confidence_stats.mean |
| No regressions | ✅ | Compare to Phase 1 baseline → no new failures |

### Phase 3 Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| IDK rate | 20-25% | `python3 local/scripts/analyze_all_recent.py` |
| Answer rate | 75-80% | Same as above |
| High-score queries fixed | ≥7/8 | `python3 local/run_comprehensive_test.py --phase 3` |
| Avg confidence | >4.0 | Langfuse dashboard → confidence_stats |
| P95 latency | <2s | Langfuse dashboard → latency chart |
| False positive rate | <1% | Review Langfuse traces for guardrail bypasses |

---

## 📋 Test Report Template

Use this when documenting test results:

```markdown
# Test Results — Phase [1|2|3]
**Date:** 2026-06-XX HH:MM  
**Tester:** [name]  
**Environment:** Local/Staging/Prod  
**Changes Applied:** [brief description of fixes]

## Metrics Summary

### Quick Tests
- Q1-Q10 Test: **9/10 passed** (90%)
- Regression Suite: **97/102 passed** (95%)

### IDK Analysis
- IDK Rate: **38.0%** (target: 35-38% ✅)
- Answer Rate: **62.0%** (target: 62-65% ✅)
- Avg Confidence: **3.8** (target: >3.0 ✅)

### By Module (from Langfuse)
| Module | Answered | IDK | Rate |
|--------|----------|-----|------|
| Bot Studio | 45 | 15 | 75.0% |
| Channels | 30 | 2 | 93.8% |
| Integrations | 25 | 5 | 83.3% |

### Quality Checks
- ✅ Q1 guardrail still blocks API key queries
- ✅ No latency regression (P95: 1.2s)
- ✅ Confidence scores reasonable (0.8-6.0)
- ✅ No false positives detected

## Issues Found
[List any issues that came up during testing]

## Recommendation
- [Ready for next phase / Hold for investigation / Needs refinement]

**Approved by:** [Adwit/team lead]
```

---

## 🔍 Troubleshooting Measurements

### "My test results don't match expectations"

**Q: Local tests pass but Langfuse shows higher IDK rate?**  
A: Langfuse traces include off-topic queries that local tests don't. This is normal. Focus on the Langfuse number as the ground truth.

**Q: Regression test has failures?**  
A: Run with `--verbose` to see which specific tests failed. Then:
```bash
python3 local/tests/test_regression.py --verbose 2>&1 | grep "FAIL"
```

**Q: Q6-Q9 not answering after Phase 1 changes?**  
A: Verify changes applied correctly:
```bash
grep "MIN_EVIDENCE_SCORE = 0.8" skill/kb_answer.py
# Should return the line. If not, changes weren't saved.
```

**Q: Confidence scores too low?**  
A: Expected in Phase 1. They should improve with Phase 2 entity enhancements.

**Q: How do I know if I'm improving?**  
A: Compare metrics week-over-week:
```bash
python3 << 'EOF'
import json

baselines = [
    ("baseline", 42.5, 57.5),
    ("phase1", 38.0, 62.0),
    ("phase2", 28.0, 72.0),
    ("phase3", 22.0, 78.0),
]

for name, idk, answer in baselines:
    print(f"{name:15} IDK: {idk:5.1f}%  Answer: {answer:5.1f}%")
EOF
```

---

## 📊 Measurement Checklist

### Before Starting Phase 1
- [ ] Baseline snapshot saved (`baseline_phase0.json`)
- [ ] Q1-Q10 test passes (9/10)
- [ ] Regression suite passes (95%+)
- [ ] Langfuse IDK rate recorded (42.5%)
- [ ] Team notified of testing

### During Phase 1
- [ ] Changes applied to `skill/kb_answer.py`
- [ ] Q1-Q10 test runs
- [ ] Regression suite runs
- [ ] No new errors in test output
- [ ] Latency still <2s

### After Phase 1 (Day 1)
- [ ] IDK rate improved to 35-38%
- [ ] Q6-Q9 all answering
- [ ] No guardrail bypasses
- [ ] Confidence scores >0.8

### After Phase 1 (Day 7)
- [ ] IDK rate stable at 35-38%
- [ ] No regression in other areas
- [ ] Dashboard shows improvement trend
- [ ] Ready to proceed to Phase 2

### Repeat for Phase 2, Phase 3...

---

## 🎓 Common Measurement Patterns

### Pattern 1: Verify a specific query works
```bash
python3 << 'EOF'
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "skill"))
import kb_answer as kb

chunks = []
with open("kb/kb_chunks.jsonl") as f:
    for line in f:
        if line.strip():
            chunks.append(json.loads(line))

query = "How do I sync customer data from Salesforce to Gupshup through webhooks?"
module = kb._detect_module(query)
entities = kb._extract_entities(query)
intent = kb._classify_intent(query, entities)
scored = []
for c in chunks:
    s = kb._score_chunk(query, c, entities, module)
    if s > 0:
        scored.append({**c, "score": s})
scored.sort(key=lambda x: x.get("score", 0), reverse=True)
evidence = kb._select_evidence(query, scored, intent, module)
answer = kb._compose_answer(query, intent, entities, evidence, module)

print(f"Query: {query}")
print(f"Module: {module}")
print(f"Intent: {intent}")
print(f"Search score: {scored[0]['score']:.2f if scored else 0}")
print(f"Evidence score: {evidence[0]['score']:.2f if evidence else 0}")
print(f"Answered: {'✅' if 'don\'t know' not in answer.lower() else '❌'}")
EOF
```

### Pattern 2: Compare metrics across runs
```bash
# Save Phase 1 results
python3 local/run_comprehensive_test.py --full --output /tmp/phase1.json

# Apply Phase 2 changes

# Save Phase 2 results
python3 local/run_comprehensive_test.py --full --output /tmp/phase2.json

# Compare
python3 << 'EOF'
import json

with open('/tmp/phase1.json') as f:
    p1 = json.load(f)
with open('/tmp/phase2.json') as f:
    p2 = json.load(f)

print(f"Phase 1 → Phase 2")
print(f"Answer rate: {p1['answer_rate']:.1f}% → {p2['answer_rate']:.1f}%")
print(f"IDK rate:    {p1['idk_rate']:.1f}% → {p2['idk_rate']:.1f}%")
print(f"Pass rate:   {p1['pass_rate']:.1f}% → {p2['pass_rate']:.1f}%")
EOF
```

### Pattern 3: Find which queries are still failing
```bash
python3 local/run_comprehensive_test.py --full --verbose | grep "❌"
```

---

## 🚀 Measurement at Scale

For larger test sets, use batch processing:

```bash
# Test 100 queries in parallel
python3 << 'EOF'
import concurrent.futures
import json
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "skill"))
import kb_answer as kb

# Load chunks once
chunks = []
with open("kb/kb_chunks.jsonl") as f:
    for line in f:
        if line.strip():
            chunks.append(json.loads(line))

# Your queries here
queries = [...]

def test_query(query):
    module = kb._detect_module(query)
    entities = kb._extract_entities(query)
    intent = kb._classify_intent(query, entities)
    # ... run pipeline
    return result

# Run in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(test_query, queries))

# Aggregate
passed = sum(1 for r in results if r["passed"])
print(f"Passed: {passed}/{len(results)}")
EOF
```

---

## 📞 Support

**Questions about measurements?** Check:
- **Local tests:** `local/test_10_queries.py` and `local/tests/test_regression.py`
- **Langfuse analysis:** `local/scripts/analyze_all_recent.py`
- **Dashboard:** `local/scripts/comprehensive_analytics_dashboard.py`
- **Comprehensive runner:** `local/run_comprehensive_test.py`

**Expected times:**
- Q1-Q10: <1 min
- Regression suite: 2-5 min
- Full test (69 queries): 5-10 min
- Langfuse analysis: 5-10 min (depends on API)
- Dashboard: 2-3 min

---

**Created:** 2026-06-16  
**Last Updated:** 2026-06-16  
**Status:** Ready to use
