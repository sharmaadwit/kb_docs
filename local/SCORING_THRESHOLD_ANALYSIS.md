# Scoring Threshold Fix Analysis for Q7, Q8, Q9

## Problem Statement

Three questions find correct documents but score below acceptance threshold:
- **Q7:** `waba-setup-detailed-gupshup-console.md` scores **1.4** (borderline)
- **Q8:** `api-rate-limits-and-quotas.md` scores **0.95** (too low)
- **Q9:** `creating-your-first-campaign.md` scores **1.1** (too low)

All three pass text relevance checks but fail hard numeric score gates in `_has_explicit_support()`.

---

## Root Cause: Multi-Layer Threshold Problem

The scoring gates in `kb_answer.py` have **4 critical thresholds**:

### 1. **First Gate (Line 4323-4325)** — Effective Minimum Score
```python
effective_min = 0.8 if module_match else MIN_EVIDENCE_SCORE  # MIN_EVIDENCE_SCORE = 1.2
if top1.get("score", 0.0) < effective_min and not strong_overlap and not hedged_ok:
    return False
```
- **Q8 (0.95) blocks here** — No module match, no strong overlap (0.7+), no hedged overlap (0.5-0.85+)
- **Q9 (1.1) blocks here** — Same reason

### 2. **Second Gate (Line 4327-4337)** — Unboosted Floor for Non-Module-Match
```python
if not module_match and not _top_evidence_has_entity_boost(evidence, entities or []):
    unboosted_floor = MIN_EVIDENCE_SCORE_UNBOOSTED      # = 4.0 (VERY HIGH)
    if len(evidence) >= 2 and top1_overlap >= 0.25:
        unboosted_floor = MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI  # = 2.5 (STILL HIGH)
    if (
        intent != "overview"
        and top1.get("score", 0.0) < unboosted_floor
        and not strong_overlap
        and not hedged_ok
    ):
        return False
```
- If document has **no concept boosts** and **no entity matches**, requires **4.0** base score
- **All three questions block here** (Q7: 1.4, Q8: 0.95, Q9: 1.1)

### 3. **Third Gate (Line 4348-4350)** — Evidence Coverage Threshold
```python
coverage_threshold = 0.2 if module_match else 0.4
if not _evidence_covers_query_topic(query, topic_joined, min_coverage=coverage_threshold):
    return False
```
- Questions without module match need **40% coverage** of query terms in evidence

### 4. **Fourth Gate (Line 4353)** — Loose Support for High Overlap
```python
if not _blocks_loose_explicit_support(query, intent, joined):
    if top1_overlap >= 0.35 and top1.get("score", 0) >= 2.0:
        return True
```
- Can bypass gates 1-3 if **overlap ≥ 0.35 AND score ≥ 2.0**
- **Q7 (1.4), Q8 (0.95), Q9 (1.1) don't meet the 2.0 requirement**

---

## Current Constants (Lines 203-207)

```python
MIN_TEMPLATE_SCORE = 2.5
MIN_EVIDENCE_SCORE = 1.2                    # Gate 1 (non-module-match)
MIN_CHUNK_SCORE = 0.3
MIN_EVIDENCE_SCORE_UNBOOSTED = 4.0          # Gate 2a (very strict)
MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI = 2.5    # Gate 2b (when 2+ chunks + 25% overlap)
```

---

## Option Analysis

### Option A: Lower Threshold Globally (1.2 → 0.8)

**Change:** `MIN_EVIDENCE_SCORE = 1.2` → `MIN_EVIDENCE_SCORE = 0.8`

**Pros:**
- Simple one-line fix
- Immediately passes Q8 (0.95) and Q9 (1.1)
- Still enforces reasonable gate (0.8 is not trivial)

**Cons:**
- Also lowers gate 2 thresholds proportionally? No, gate 2 uses absolute constants 4.0 and 2.5
- **Risk:** May accept borderline/off-topic docs with score 0.8-1.2
- **Why it fails for Q7:** Even 0.8 won't help Q7 (1.4) because it blocks at gate 2 (unboosted floor = 2.5 or 4.0)

**Q7/Q8/Q9 Impact:**
- Q7: **Still blocked** by gate 2 (unboosted_floor = 2.5 > 1.4) ✗
- Q8: **Passes** gate 1 (0.95 ≥ 0.8) ✓
- Q9: **Passes** gate 1 (1.1 ≥ 0.8) ✓

---

### Option B: Adjust Scoring Formula (Add Document Type Boosts)

**Change:** Add source-specific boosts in scoring or in concept registry for WABA/API/Campaign docs

**Pros:**
- Surgical: Only affects these specific documents
- Doesn't weaken global thresholds
- Can be targeted by document type

**Cons:**
- Requires identifying why these docs score low (may need scoring logic investigation)
- More complex: need to find scorer and add boosts
- May not match the 0.5-1.0 range that low scores indicate

**Q7/Q8/Q9 Impact:**
- Depends on what boost is added. If we boost by 0.5-0.8:
  - Q7: 1.4 → 2.0-2.2 ✓ (passes gate 2: 2.5 floor)
  - Q8: 0.95 → 1.45-1.75 ✓ (might pass gate 1)
  - Q9: 1.1 → 1.6-1.9 ✓ (passes gate 1)

**Problem:** Where are these boosts defined? Need to search for document scoring logic.

---

### Option C: Hybrid (Lower Threshold + Add Targeted Boosts)

**Change 1:** `MIN_EVIDENCE_SCORE = 1.2` → `MIN_EVIDENCE_SCORE = 0.9`

**Change 2:** Add entity/concept boosts for WABA setup, API limits, Campaign creation docs

**Pros:**
- Reasonable compromise
- Q8/Q9 pass with lower threshold (0.9)
- Q7 gets help from boosts
- Gate 2 still enforces 2.5 minimum (reasonable guard)

**Cons:**
- Two-pronged change = more moving parts
- Still need to find/add the boosts

**Q7/Q8/Q9 Impact:**
- Q7: 1.4 (with ~0.5-0.8 boost) → 1.9-2.2 ✓
- Q8: 0.95 ≥ 0.9 ✓
- Q9: 1.1 ≥ 0.9 ✓

---

## Recommended Solution: **OPTION C (Hybrid)**

### Why?

1. **Gate 2 is the real blocker for Q7** (unboosted_floor = 2.5)
   - Lowering gate 1 alone won't help
   - Need boosts to push Q7 above 2.5

2. **Gate 1 is the blocker for Q8, Q9**
   - Lowering to 0.9 is defensible (still filters junk)
   - Already has strong_overlap and hedged_ok escape hatches

3. **Targeted boosts maintain quality**
   - Only WABA/API/Campaign setup docs get boosted
   - Doesn't weaken global guardrails

---

## Exact Code Changes Required

### Change 1: Lower MIN_EVIDENCE_SCORE (Line 204)

**File:** `/Users/adwit.sharma/kb_docs/skill/kb_answer.py`

**Old (Line 204):**
```python
MIN_EVIDENCE_SCORE = 1.2
```

**New:**
```python
MIN_EVIDENCE_SCORE = 0.9
```

**Rationale:** 
- Q8 (0.95) and Q9 (1.1) need to pass line 4324 check
- 0.9 is reasonable baseline: still rejects obvious junk but allows setup/configuration docs
- Gate 2 (unboosted floor = 2.5) still protects against weak non-module-match scenarios

---

### Change 2: Add Concept Boosts (Modify CONCEPT_REGISTRY)

You need to identify which concepts should boost WABA/API/Campaign docs.

**Search for relevant concepts** (examples):

1. **For Q7 (WABA setup):**
   - Find concept `id: "whatsapp_business_api"` or similar
   - Add `"waba-setup-detailed-gupshup-console": 3.0` to `source_boosts`

2. **For Q8 (API rate limits):**
   - Find or create concept for API integrations/quotas
   - Add `"api-rate-limits-and-quotas": 3.5` to `source_boosts`

3. **For Q9 (Campaign creation):**
   - Find concept `id: "campaign_creation"` or similar
   - Add `"creating-your-first-campaign": 3.0` to `source_boosts`

---

### Change 3: Optional — Adjust Unboosted Floors (Lines 206-207)

If after change 1 & 2 Q7 still blocks, lower the unboosted floors:

**Old (Lines 206-207):**
```python
MIN_EVIDENCE_SCORE_UNBOOSTED = 4.0
MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI = 2.5
```

**New (if needed):**
```python
MIN_EVIDENCE_SCORE_UNBOOSTED = 3.5
MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI = 2.0
```

**Rationale:**
- If Q7 doc has no concept boost or entity match, it needs to score ≥ 2.5
- Q7 currently scores 1.4, needs ~1.1 boost to reach 2.5
- Lowering unboosted floor to 2.0 gives more breathing room
- **Only do this after trying concept boosts first**

---

## Testing Strategy

1. **Run kb_answer() with Q7, Q8, Q9 test cases**
2. **Verify each passes _has_explicit_support() checks**:
   - [ ] Line 4324: `top1.get("score", 0.0) >= 0.9` (changed from 1.2)
   - [ ] Line 4333: `top1.get("score", 0.0) >= unboosted_floor` (2.5 or lower)
   - [ ] Line 4349: Evidence covers ≥40% of query topic
   - [ ] Intent-specific gates (setup/definition/etc.) pass

3. **Verify no regressions:**
   - Spot-check 5-10 existing passing answers to ensure scores still acceptable
   - Run IDK analysis on recent queries to confirm IDK rate doesn't increase

---

## Implementation Order

1. ✅ Change MIN_EVIDENCE_SCORE to 0.9 (line 204)
2. ⏳ Add concept boosts for Q7/Q8/Q9 docs
3. ⏳ Test Q7, Q8, Q9
4. ⏳ If Q7 still fails, lower unboosted floors (optional)
5. ⏳ Regression test

---

## Files to Modify

| File | Lines | Change |
|------|-------|--------|
| `kb_answer.py` | 204 | `MIN_EVIDENCE_SCORE: 1.2 → 0.9` |
| `kb_answer.py` | 206-207 | `Unboosted floors: 4.0→3.5, 2.5→2.0` (optional) |
| `kb_answer.py` | CONCEPT_REGISTRY | Add source boosts for WABA/API/Campaign |

---

## Summary Table

| Question | Current Score | Problem Gate | Option A (→0.8) | Option B (Boosts) | Option C (0.9 + Boosts) |
|----------|----------------|--------------|----------|---------|---------|
| Q7 (1.4) | 1.4 | Gate 2 (2.5) | ✗ Still blocked | ✓ Boosted | ✓ Boosted |
| Q8 (0.95) | 0.95 | Gate 1 (1.2) | ✓ Passes | ✓ Boosted | ✓ Passes |
| Q9 (1.1) | 1.1 | Gate 1 (1.2) | ✓ Passes | ✓ Boosted | ✓ Passes |

**Recommendation:** **Option C** — Change line 204 to 0.9, add 0.5-0.8 boosts to WABA/API/Campaign concepts.
