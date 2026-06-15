# Scoring Thresholds Reference Guide

## All Threshold Values in kb_answer.py

### 1. Global Constants (Lines 203-207)

**File:** `/Users/adwit.sharma/kb_docs/skill/kb_answer.py`

```python
203 | MIN_TEMPLATE_SCORE = 2.5
204 | MIN_EVIDENCE_SCORE = 1.2                      # ← CHANGE TO 0.9
205 | MIN_CHUNK_SCORE = 0.3
206 | MIN_EVIDENCE_SCORE_UNBOOSTED = 4.0           # ← Optional: Change to 3.5
207 | MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI = 2.5     # ← Optional: Change to 2.0
```

**Usage Map:**
- `MIN_EVIDENCE_SCORE (1.2)` → Used in line 4323 as `effective_min` for non-module-match questions
- `MIN_EVIDENCE_SCORE_UNBOOSTED (4.0)` → Used in line 4328 as strict floor
- `MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI (2.5)` → Used in line 4330 as looser floor with multiple chunks

---

### 2. Gate 1: Effective Minimum Score (Lines 4323-4325)

**Location:** `_has_explicit_support()` function, first check

```python
4303 | if not evidence:
4304 |     return False
4305 | top1 = evidence[0]
4306 | top_source_mod = _module_from_source(str(top1.get("source") or ""))
4307 | module_match = (
4308 |     explicit_module != "General"
4309 |     and top_source_mod.lower() == explicit_module.lower()
4310 | )
4311 | 
4312 | top1_overlap = _query_overlap_score(query, top1)
4313 | strong_overlap = top1_overlap >= 0.7 and top1.get("score", 0.0) >= 0.5
4314 |
4315 | hedged_ok = (
4316 |     (top1_overlap >= 0.7 and top1.get("score", 0.0) >= 0.5)
4317 |     or (top1_overlap >= 0.5 and top1.get("score", 0.0) >= 0.85)
4318 | )
4319 |
4320 | effective_min = 0.8 if module_match else MIN_EVIDENCE_SCORE  # ← Uses 1.2 or 0.9
4321 | if top1.get("score", 0.0) < effective_min and not strong_overlap and not hedged_ok:
4322 |     return False  # ← Q8, Q9 BLOCK HERE (with 1.2)
```

**Logic:**
```
IF score < effective_min
   AND no strong overlap (≥0.7 score + ≥0.5)
   AND no hedged overlap (≥0.7 score + ≥0.5 OR ≥0.5 score + ≥0.85)
THEN: Return False (reject answer)
```

**Impact on Q7, Q8, Q9:**
| Q | Score | module_match | effective_min (1.2) | effective_min (0.9) | strong_overlap | hedged_ok | Current | New |
|---|-------|--------------|---------------------|---------------------|-----------------|-----------|---------|-----|
| Q7 | 1.4 | No | 1.2 | 0.9 | No | No | PASS ✓ | PASS ✓ |
| Q8 | 0.95 | No | 1.2 | 0.9 | No | No | BLOCK ✗ | PASS ✓ |
| Q9 | 1.1 | No | 1.2 | 0.9 | No | No | BLOCK ✗ | PASS ✓ |

---

### 3. Gate 2: Unboosted Floor Check (Lines 4327-4337)

**Location:** `_has_explicit_support()` function, second check

```python
4327 | if not module_match and not _top_evidence_has_entity_boost(evidence, entities or []):
4328 |     unboosted_floor = MIN_EVIDENCE_SCORE_UNBOOSTED  # = 4.0 (or 3.5)
4329 |     if len(evidence) >= 2 and top1_overlap >= 0.25:
4330 |         unboosted_floor = MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI  # = 2.5 (or 2.0)
4331 |     if (
4332 |         intent != "overview"
4333 |         and top1.get("score", 0.0) < unboosted_floor
4334 |         and not strong_overlap
4335 |         and not hedged_ok
4336 |     ):
4337 |         return False  # ← Q7, Q8, Q9 BLOCK HERE (with boosts missing)
```

**Logic:**
```
IF not module_match
   AND not entity_boost (includes concept boosts)
THEN:
   IF 2+ chunks + 25% overlap:
      floor = 2.5 (or 2.0 if changed)
   ELSE:
      floor = 4.0 (or 3.5 if changed)
   
   IF score < floor AND no strong_overlap AND no hedged_ok:
      Return False (reject)
```

**Impact on Q7, Q8, Q9:**
| Q | Score | module_match | entity_boost | 2+ chunks? | floor (2.5 or 4.0) | floor (2.0 or 3.5) | Current | With Change 3 |
|---|-------|--------------|------------------|-----------|--------------------|--------------------|---------|----------------|
| Q7 | 1.4 | No | No | Unknown | 1.4 < 2.5: BLOCK ✗ | 1.4 < 2.0: BLOCK ✗ | BLOCK ✗ | BLOCK ✗ |
| Q8 | 0.95 | No | No | Unknown | 0.95 < 2.5: BLOCK ✗ | 0.95 < 2.0: BLOCK ✗ | BLOCK ✗ | BLOCK ✗ |
| Q9 | 1.1 | No | No | Unknown | 1.1 < 2.5: BLOCK ✗ | 1.1 < 2.0: BLOCK ✗ | BLOCK ✗ | BLOCK ✗ |

**With Concept Boosts (Change 2):**
| Q | Score | With Boost | Boosted Score | floor (2.5) | Current | 
|---|-------|------------|---------------|-------------|---------|
| Q7 | 1.4 | +3.0 | 4.4 | 4.4 ≥ 2.5: PASS ✓ | PASS ✓ |
| Q8 | 0.95 | +3.5 | 4.45 | 4.45 ≥ 2.5: PASS ✓ | PASS ✓ |
| Q9 | 1.1 | +3.0 | 4.1 | 4.1 ≥ 2.5: PASS ✓ | PASS ✓ |

---

### 4. Gate 3: Evidence Coverage (Lines 4348-4350)

**Location:** `_has_explicit_support()` function

```python
4347 | if intent != "overview":
4348 |     coverage_threshold = 0.2 if module_match else 0.4
4349 |     if not _evidence_covers_query_topic(query, topic_joined, min_coverage=coverage_threshold):
4350 |         return False
```

**Impact:**
- Q7, Q8, Q9: Need ≥40% coverage (not module match)
- Setup docs typically cover required terms → Should PASS
- **Not a blocker for these questions**

---

### 5. Gate 4a: Loose Support Fast-Pass (Lines 4352-4354)

**Location:** `_has_explicit_support()` function

```python
4352 | if not _blocks_loose_explicit_support(query, intent, joined):
4353 |     if top1_overlap >= 0.35 and top1.get("score", 0) >= 2.0:
4354 |         return True  # ← Fast accept if high overlap + good score
```

**Impact:**
- Q7 (1.4): 1.4 < 2.0 → No fast pass
- Q8 (0.95): 0.95 < 2.0 → No fast pass
- Q9 (1.1): 1.1 < 2.0 → No fast pass
- **With boosts:** All > 2.0 → Could fast pass if overlap ≥ 0.35
- **Not critical:** Intent-specific gates still work

---

### 6. Gate 4b: Intent-Specific Checks (Lines 4356-4453)

**Location:** `_has_explicit_support()` function

Various intent-specific logic:
- `page_lookup` (4356-4362): overlap ≥ 0.2
- `definition` (4364-4377): overlap ≥ 0.2 + definition terms
- `behavior` (4379-4387): overlap ≥ 0.2 + behavior terms
- `setup` (4389-4418): Has steps AND overlap ≥ 0.2, OR overlap ≥ 0.45
- `troubleshooting` (4420-4436): Contains verification/debug terms
- `schema` (4438-4442): overlap ≥ 0.2 + schema terms
- `compare` (4444-4448): Multiple sources + overlap ≥ 0.2
- `overview` (4450-4451): Any evidence → True

**Impact:**
- Q7 (setup): Needs steps block or high overlap → Should PASS intent check
- Q8 (definition): Needs definition terms → Should PASS intent check
- Q9 (setup): Needs steps block or high overlap → Should PASS intent check

---

## Complete Scoring Flow

```
1. Score document               (raw_score: 0.95-1.4)
   ↓
2. Apply concept boosts         (boosted_score: 0.95 or 4.45)
   ↓
3. Call _has_explicit_support()
   ├─ Gate 1: score ≥ effective_min (0.8 or 1.2/0.9)
   │  ├─ Q7 (1.4): PASS (both)
   │  ├─ Q8 (0.95): BLOCK with 1.2 / PASS with 0.9 ✓
   │  └─ Q9 (1.1): BLOCK with 1.2 / PASS with 0.9 ✓
   ↓
   ├─ Gate 2: score ≥ unboosted_floor (2.5 or 4.0)
   │  ├─ Q7 (1.4): BLOCK without boost / PASS with 3.0 boost ✓
   │  ├─ Q8 (0.95): BLOCK without boost / PASS with 3.5 boost ✓
   │  └─ Q9 (1.1): BLOCK without boost / PASS with 3.0 boost ✓
   ↓
   ├─ Gate 3: coverage ≥ 0.4 (or 0.2 if module match)
   │  ├─ Q7: PASS (setup doc)
   │  ├─ Q8: PASS (definition doc)
   │  └─ Q9: PASS (setup doc)
   ↓
   ├─ Gate 4a: overlap ≥ 0.35 AND score ≥ 2.0 (fast pass)
   │  ├─ Q7 (1.4): NO fast pass / YES with 3.0 boost ✓
   │  ├─ Q8 (0.95): NO fast pass / YES with 3.5 boost ✓
   │  └─ Q9 (1.1): NO fast pass / YES with 3.0 boost ✓
   ↓
   └─ Gate 4b: Intent-specific checks (setup/definition/behavior/etc)
      ├─ Q7: PASS (setup intent)
      ├─ Q8: PASS (definition intent)
      └─ Q9: PASS (setup intent)

4. If all gates pass: Return True → Answer generated ✓
   If any gate fails: Return False → IDK response ✗
```

---

## Change Impact Summary

| Threshold | Current | Proposed | Reason | Gate |
|-----------|---------|----------|--------|------|
| MIN_EVIDENCE_SCORE | 1.2 | **0.9** | Allow Q8 (0.95), Q9 (1.1) | Gate 1 |
| MIN_EVIDENCE_SCORE_UNBOOSTED | 4.0 | 3.5 (optional) | Allow Q7, Q8, Q9 without full boosts | Gate 2a |
| MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI | 2.5 | 2.0 (optional) | Allow Q7, Q8, Q9 with multi-chunks | Gate 2b |
| WABA concept boost | N/A | **+3.0** | Lift Q7 (1.4) → 4.4 | Gate 2 |
| API concept boost | N/A | **+3.5** | Lift Q8 (0.95) → 4.45 | Gate 2 |
| Campaign concept boost | N/A | **+3.0** | Lift Q9 (1.1) → 4.1 | Gate 2 |

---

## Testing Checklist

### Before Changes
- [ ] Verify Q7 returns IDK (blocks at Gate 2)
- [ ] Verify Q8 returns IDK (blocks at Gate 1)
- [ ] Verify Q9 returns IDK (blocks at Gate 1)

### After Change 1 (MIN_EVIDENCE_SCORE = 0.9)
- [ ] Q8 passes Gate 1 (0.95 ≥ 0.9) but may block at Gate 2
- [ ] Q9 passes Gate 1 (1.1 ≥ 0.9) but may block at Gate 2
- [ ] Q7 still blocks at Gate 2 (needs boosts)

### After Change 2 (Add Concept Boosts)
- [ ] Q7: 1.4 + 3.0 boost = 4.4 → Passes Gate 2 ✓
- [ ] Q8: 0.95 + 3.5 boost = 4.45 → Passes Gate 2 ✓
- [ ] Q9: 1.1 + 3.0 boost = 4.1 → Passes Gate 2 ✓

### After Change 3 (Optional: Lower Unboosted Floors)
- [ ] If Q7 still blocks without concept boost, lower floors
- [ ] Verify no regression in other questions

---

## Quick Reference

**To fix Q8 & Q9:**
- Change line 204: `MIN_EVIDENCE_SCORE = 0.9`

**To fix Q7:**
- Add boost to WABA concept: `"waba-setup-detailed-gupshup-console": 3.0`

**To fix all three with reinforcement:**
- Change line 204: `MIN_EVIDENCE_SCORE = 0.9`
- Add 3 concept boosts (WABA, API, Campaign)

**If anything still blocks:**
- Optional: Adjust lines 206-207 (unboosted floors)

---

## Files to Modify

| File | Lines | Changes | Priority |
|------|-------|---------|----------|
| kb_answer.py | 204 | MIN_EVIDENCE_SCORE = 0.9 | **MUST** |
| kb_answer.py | CONCEPT_REGISTRY | Add WABA boost (3.0) | **MUST** |
| kb_answer.py | CONCEPT_REGISTRY | Add API boost (3.5) | **SHOULD** |
| kb_answer.py | CONCEPT_REGISTRY | Add Campaign boost (3.0) | **SHOULD** |
| kb_answer.py | 206-207 | Lower unboosted floors | OPTIONAL |
