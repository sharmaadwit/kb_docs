# Confidence Score Bug Analysis

## Issue
Recent PROD_EXT traces show **inflated confidence values**:
- Expected: 0–1 normalized scores
- Actual: Raw unbounded scores (0.5–8+)
- Display: Langfuse shows as `X*100%` (e.g., 2.9 → 290%, 8.05 → 805%)

## Traces Affected
Analyzed 5 latest PROD_EXT traces:
- Trace 1: confidence=8.05 (displayed as 805.00%)
- Trace 2: confidence=2.9 (displayed as 290.00%)
- Trace 3: confidence=2.9 (displayed as 290.00%)
- Trace 4: confidence=2.85 (displayed as 285.00%)
- Trace 5: confidence=2.9 (displayed as 290.00%)

## Root Cause Analysis

### Location: `skill/kb_answer.py`

**Bug #1: Hardcoded confidence for case studies (line 4100)**
```python
return {
    "answered": True,
    "answer": answer,
    "sources": sources,
    "_chunks": scored_top_matches,
    "confidence": 8.0  # ← HARDCODED, should use actual case study score
}
```
- Scope: Only case study answers
- Impact: Case study confidence always 8.0 (displayed as 800%)

**Bug #2: Raw unbounded scores sent to telemetry (line 6873)**
```python
"confidence": results[0].get("score") if results else 0.0,  # ← Raw score, not normalized
```
- Scope: All regular KB answers
- Impact: Scores range 0.5–8+ instead of 0–1
- Why it happens: Scoring system uses unbounded BM25-like scores:
  - Base token matches: 0.05–0.25 per token
  - Module match: +0.35
  - Entity boosts: variable
  - SuperAgent boost/penalty: ±4.0 to ±5.0

## Comparison: Before & After Refactor

**Checked commits:**
- `667912ea` (before self-contained refactor)
- `3602daa5` (after self-contained refactor)
- Further back to `cfd0c76c` (telemetry integration)

**Finding:** Bug exists in all versions checked — not introduced by recent changes.

## What Changed in Self-Contained Refactor

The refactor (`72bdda85` → `3602daa5`) **did NOT change** the confidence logic:
- No changes to `_score_chunk()` function
- No changes to metadata["confidence"] assignment
- No normalization added or removed
- Confidence transmission mechanism unchanged

The raw score values have always been sent; this is **pre-existing behavior**.

## Impact on Analysis

**Langfuse Display Interpretation:**
- Langfuse UI multiplies by 100 to show `%`
- 2.9 raw → displayed as "290.00%"
- **This is misleading**: looks like 290% confidence, actually 2.9/8+ raw score

**Dashboard/Analytics:**
- Raw score values are correct (2.9, 8.05, etc.)
- BUT percentages in dashboards will be meaningless
- Comparisons between traces will work (relative ranking OK)

## Fix Recommendations

### Option A: Normalize to 0–1 (Recommended)
```python
# Line 6873
"confidence": min(1.0, max(0.0, results[0].get("score", 0.0) / 8.0)) if results else 0.0,
```
- Assumes max reasonable score ≈ 8
- Clamps outliers to 1.0
- Produces displayable percentages

### Option B: Cap at 1.0
```python
# Line 6873
"confidence": min(1.0, results[0].get("score", 0.0)) if results else 0.0,
```
- Simpler: just cap at max probability
- Loses granularity above 1.0
- Easier to explain

### Option C: Document as raw scores
```python
# Rename field to avoid percentage confusion
"relevance_score": results[0].get("score") if results else 0.0,
```
- Preserve raw data for ML/analysis
- Document in SKILL.md that scores are unbounded

### Fix Case Study Bug (Required)
```python
# Line 4100
return {
    "answered": True,
    "answer": answer,
    "sources": sources,
    "_chunks": scored_top_matches,
    "confidence": scored_top_matches[0].get("score", 0.0) if scored_top_matches else 0.0
}
```

## Recommendation

**Do Option A + Fix Case Study Bug:**

1. Normalize `confidence` to 0–1 by dividing by 8.0
2. Fix hardcoded 8.0 for case studies to use actual score
3. Keep `top_score` as raw for internal analysis
4. Update telemetry docs in SKILL.md

**Impact:**
- Langfuse will display 0–100% (meaningful)
- Old traces remain unchanged (raw 2.9, 8.05 scores unchanged)
- All future traces will have normalized confidence
