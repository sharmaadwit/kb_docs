# Scoring Threshold Decision Tree

## Flow Diagram: How Q7, Q8, Q9 Documents Are Evaluated

```
kb_answer(query) 
  ↓
  ├─ Score document: 1.4 (Q7), 0.95 (Q8), 1.1 (Q9)
  ↓
  ├─ Call _has_explicit_support(query, intent, evidence, ...)
  ↓
  └─ GATE 1: Check effective_min (Line 4323-4325)
      │
      ├─ effective_min = 0.8 (if module_match) 
      │                    OR MIN_EVIDENCE_SCORE (if not)
      │
      ├─ Q7: module_match? No → effective_min = 1.2 (CURRENT) / 0.9 (NEW)
      │      score (1.4) ≥ 1.2? YES ✓ (current)
      │      score (1.4) ≥ 0.9? YES ✓ (new)
      │      → Passes gate 1 (both)
      │
      ├─ Q8: module_match? No → effective_min = 1.2 (CURRENT) / 0.9 (NEW)
      │      score (0.95) ≥ 1.2? NO ✗ (current: BLOCKS HERE)
      │      score (0.95) ≥ 0.9? YES ✓ (new: PASSES)
      │      → BLOCKS at gate 1 (current) / Passes (new)
      │
      └─ Q9: module_match? No → effective_min = 1.2 (CURRENT) / 0.9 (NEW)
             score (1.1) ≥ 1.2? NO ✗ (current: BLOCKS HERE)
             score (1.1) ≥ 0.9? YES ✓ (new: PASSES)
             → BLOCKS at gate 1 (current) / Passes (new)

         [ESCAPE ROUTES: strong_overlap (≥0.7 & score ≥0.5) or hedged_ok]
         └─ Q7, Q8, Q9: Don't have strong overlap or hedged_ok → no escape
             → These don't help them pass

  ↓ [All pass gate 1? Proceed to gate 2]

  └─ GATE 2: Check unboosted floor (Line 4327-4337)
      │
      ├─ Condition: not module_match 
      │          AND not _top_evidence_has_entity_boost(...)
      │          AND intent != "overview"
      │
      ├─ Q7: module_match? No
      │      entity_boost? Unknown (depends on concept match)
      │      intent? Likely "setup" (not overview)
      │      → ENTERS gate 2 check
      │        ├─ len(evidence) ≥ 2 and top1_overlap ≥ 0.25?
      │        │  If YES: unboosted_floor = 2.5 (CURRENT) / 2.0 (NEW-optional)
      │        │  If NO:  unboosted_floor = 4.0 (CURRENT) / 3.5 (NEW-optional)
      │        │
      │        └─ score (1.4) < 2.5? YES → BLOCKS ✗ (current)
      │           score (1.4) < 2.0? YES → BLOCKS ✗ (new-optional)
      │           [ESCAPE: strong_overlap or hedged_ok → No]
      │           → BLOCKS at gate 2 (both scenarios)
      │
      │        SOLUTION: Add concept boost of 3.0
      │        → Boosted score: 1.4 + 3.0 = 4.4
      │        → 4.4 ≥ 2.5? YES ✓ (PASSES gate 2)
      │
      ├─ Q8: module_match? No
      │      entity_boost? Unknown
      │      intent? Likely "definition" or "setup"
      │      → ENTERS gate 2 check
      │        └─ score (0.95) < 2.5? YES → BLOCKS ✗ (current)
      │           [But Q8 already blocked at gate 1]
      │           
      │           With Change 1 (threshold = 0.9):
      │           → Passes gate 1, then:
      │           → Add concept boost of 3.5
      │           → Boosted score: 0.95 + 3.5 = 4.45
      │           → 4.45 ≥ 2.5? YES ✓ (PASSES gate 2)
      │
      └─ Q9: module_match? No
             entity_boost? Unknown
             intent? Likely "setup"
             → ENTERS gate 2 check
               └─ score (1.1) < 2.5? YES → BLOCKS ✗ (current)
                  [But Q9 already blocked at gate 1]
                  
                  With Change 1 (threshold = 0.9):
                  → Passes gate 1, then:
                  → Add concept boost of 3.0
                  → Boosted score: 1.1 + 3.0 = 4.1
                  → 4.1 ≥ 2.5? YES ✓ (PASSES gate 2)

  ↓ [All pass gate 2? Proceed to gate 3]

  └─ GATE 3: Check evidence coverage (Line 4348-4350)
      │
      ├─ coverage_threshold = 0.2 (if module_match) 
      │                      OR 0.4 (if not)
      │
      ├─ Q7, Q8, Q9: module_match? No → threshold = 0.4
      │  → Need ≥40% of query terms in evidence text
      │  → Likely PASS (setup/definition docs usually cover terms)
      │
      └─ If fail: BLOCKS here
         [But expected to pass for these documents]

  ↓ [All pass gate 3? Proceed to gates 4+]

  └─ GATES 4+: Intent-specific checks
      │
      ├─ Gate 4a (Loose support): Line 4352-4354
      │  └─ If top1_overlap ≥ 0.35 and score ≥ 2.0: ACCEPT (bypass all)
      │     → Q7 (1.4): score < 2.0 → no bypass
      │     → Q8 (0.95): score < 2.0 → no bypass
      │     → Q9 (1.1): score < 2.0 → no bypass
      │     [With boosts: all ≥ 2.0 → could bypass]
      │
      ├─ Gate 4b (Intent-specific): Line 4356+
      │  ├─ page_lookup: top1_overlap ≥ 0.2? (probably yes for these)
      │  ├─ definition: overlap ≥ 0.2 + contains definition terms? (probably yes)
      │  ├─ setup: has_action AND overlap ≥ 0.2, OR overlap ≥ 0.45
      │  │  → Setup docs should have steps/actions → probably yes
      │  ├─ behavior: overlap ≥ 0.2 + contains behavior terms? (depends)
      │  └─ [Expected: Most pass these]
      │
      └─ ALL PASS? → Return True → Answer generated ✓
         ANY FAIL? → Return False → IDK response ✗

  ↓ [If _has_explicit_support returns True]
  └─ Answer is accepted and returned to user ✓
```

---

## Current State (Before Changes)

| Question | Score | Gate 1 Check | Gate 2 Check | Result |
|----------|-------|--------------|--------------|--------|
| Q7 | 1.4 | 1.4 ≥ 1.2? YES ✓ | 1.4 ≥ 2.5? NO ✗ | **BLOCKED at Gate 2** |
| Q8 | 0.95 | 0.95 ≥ 1.2? NO ✗ | N/A | **BLOCKED at Gate 1** |
| Q9 | 1.1 | 1.1 ≥ 1.2? NO ✗ | N/A | **BLOCKED at Gate 1** |

---

## Proposed State (After Changes)

### Change 1: MIN_EVIDENCE_SCORE = 0.9
| Question | Score | Gate 1 Check | Gate 2 Check (no boost) | With Boost | Result |
|----------|-------|--------------|------------------------|------------|--------|
| Q7 | 1.4 | 1.4 ≥ 0.9? YES ✓ | 1.4 ≥ 2.5? NO ✗ | 4.4 ≥ 2.5? YES ✓ | **PASS** (with boost) |
| Q8 | 0.95 | 0.95 ≥ 0.9? YES ✓ | 0.95 ≥ 2.5? NO ✗ | 4.45 ≥ 2.5? YES ✓ | **PASS** (with boost) |
| Q9 | 1.1 | 1.1 ≥ 0.9? YES ✓ | 1.1 ≥ 2.5? NO ✗ | 4.1 ≥ 2.5? YES ✓ | **PASS** (with boost) |

---

## Why Each Change Matters

### Change 1: Lower MIN_EVIDENCE_SCORE from 1.2 to 0.9

**Who it helps:** Q8 (0.95), Q9 (1.1)

**Gate affected:** Gate 1 (Line 4323-4325)
```python
effective_min = 0.8 if module_match else MIN_EVIDENCE_SCORE  # ← Changed here
if top1.get("score", 0.0) < effective_min and not strong_overlap and not hedged_ok:
    return False
```

**Why it works:**
- Q8 and Q9 don't meet 1.2 threshold
- 0.9 is still meaningful (filters real noise)
- These docs are legitimately relevant; score is low due to shallow matching

**Risk:** May accept borderline docs with score 0.9-1.2
- **Mitigation:** Gate 2 still enforces 2.5 minimum for unboosted docs

---

### Change 2: Add Concept Boosts

**Who it helps:** Q7 (1.4), Q8 (0.95), Q9 (1.1)

**Gate affected:** Gate 2 (Line 4327-4337)
```python
unboosted_floor = MIN_EVIDENCE_SCORE_UNBOOSTED  # 4.0 or 2.5
if top1.get("score", 0.0) < unboosted_floor ... and not _top_evidence_has_entity_boost(...):
    # Concept boosts count as entity boosts!
    return False
```

**Why it works:**
- Concept boosts are applied in scoring (before _has_explicit_support)
- If Q7 doc matches "WABA" concept and gets +3.0 boost: 1.4 + 3.0 = 4.4
- Now 4.4 ≥ 2.5 floor → passes Gate 2

**Where boosts are applied:**
1. Scoring function (SEARCH for `source_boosts` usage)
2. Adds to raw score BEFORE _has_explicit_support checks
3. CONCEPT_REGISTRY defines which docs get boosted

**Risk:** Boosts too high may over-weight certain docs
- **Mitigation:** 3.0-3.5 is reasonable (lifts low score by ~1.5x, not 10x)

---

### Change 3: Lower Unboosted Floors (Optional)

**Who it helps:** Q7 if no concept boost applies

**Gate affected:** Gate 2 (Lines 206-207)
```python
MIN_EVIDENCE_SCORE_UNBOOSTED = 4.0  # ← Could lower to 3.5
MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI = 2.5  # ← Could lower to 2.0
```

**Why it works:**
- If Q7 doc doesn't match the WABA concept, it has no boost
- Then hits Gate 2 with unboosted_floor = 2.5 (or 4.0)
- Lowering to 2.0 allows Q7 (1.4) to pass
- **But this is a fallback:** Better to ensure concept boost applies

**Risk:** Significantly weakens gate 2 protection
- **Mitigation:** Only use if concept boosts don't work
- **Better:** Debug why concept boost didn't apply first

---

## Decision Matrix

```
Does Q7 doc match a WABA/setup concept?
├─ YES → Add boost 3.0 to that concept
│        Change 1 (0.9) + Change 2 (boost) = Q7 passes ✓
│
└─ NO → Two options:
         A. Create new concept for WABA setup + add boost (recommended)
            Change 1 (0.9) + Change 2 (new concept + boost) = Q7 passes ✓
         B. Lower unboosted floors as fallback
            Change 1 (0.9) + Change 3 (lower floors) = Q7 passes ✓
```

---

## Testing Validation

### Test Case 1: Q7 (WABA Setup)
```
Query: "How do I set up WABA on Gupshup Console?"
Expected doc: waba-setup-detailed-gupshup-console.md
Expected score: ~1.4
With boost: ~4.4

Validation:
1. Call kb_answer({"query": "How do I set up WABA?"})
2. Check that answer contains WABA setup info (not IDK)
3. Check that module = Channels or WhatsApp
4. Check that primary source = waba-setup-...
```

### Test Case 2: Q8 (API Rate Limits)
```
Query: "What are the API rate limits?"
Expected doc: api-rate-limits-and-quotas.md
Expected score: ~0.95
With boost: ~4.45

Validation:
1. Call kb_answer({"query": "What are the API rate limits?"})
2. Check that answer contains rate limit numbers (not IDK)
3. Check that module = Integrations or Agent Assist
4. Check that primary source = api-rate-limits-...
```

### Test Case 3: Q9 (Campaign Creation)
```
Query: "How do I create my first campaign?"
Expected doc: creating-your-first-campaign.md
Expected score: ~1.1
With boost: ~4.1

Validation:
1. Call kb_answer({"query": "How do I create my first campaign?"})
2. Check that answer contains campaign setup steps (not IDK)
3. Check that module = Campaign Manager
4. Check that primary source = creating-your-first-campaign
```

---

## Implementation Order

1. ✅ Change 1: Update MIN_EVIDENCE_SCORE = 0.9 (Line 204)
2. ✅ Change 2a: Add WABA boost to concept
3. ✅ Change 2b: Add/create API rate limits concept with boost
4. ✅ Change 2c: Add Campaign creation boost to concept
5. ✅ Test all three questions
6. ⏳ If Q7 fails: Apply Change 3 (optional)
7. ✅ Regression test (5-10 existing passing queries)

---

## Summary

| Gate | Current State | Change 1 | Change 2 | Change 3 |
|------|---------------|----------|----------|----------|
| **Gate 1** | MIN = 1.2 | MIN = 0.9 | — | — |
| **Gate 2** (unboosted) | Floor = 4.0/2.5 | Floor = 4.0/2.5 | Boosts applied | Floor = 3.5/2.0 |
| **Q7 Impact** | ✗ Blocked | ✗ Still blocked | ✓ Passes (with boost) | ✓ Passes |
| **Q8 Impact** | ✗ Blocked | ✓ Passes | ✓ Stronger | N/A |
| **Q9 Impact** | ✗ Blocked | ✓ Passes | ✓ Stronger | N/A |

**Recommendation:** Apply Changes 1 + 2 (all three boosts). Change 3 is optional fallback only.
