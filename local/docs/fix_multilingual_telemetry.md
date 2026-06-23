# Fix Multilingual Telemetry in kb_answer.py

**Last Updated:** 2026-06-19  
**Status:** Ready for Implementation  
**Priority:** High

---

## Why We're Making This Change

### The Problem

Non-English (Spanish/Portuguese/Arabic) queries are being **translated to English before Langfuse logging**, causing a critical telemetry mismatch:

- User asks in Spanish: `"¿Qué demostraciones son adecuadas para farmacéutica?"`
- System translates internally: `"what demonstrations are suitable for pharmaceutical?"`
- **Langfuse records only the translated version**
- User sees Spanish response, but trace shows English query
- **Impact:** Telemetry analysis cannot distinguish multilingual behavior

### Business Impact

| Issue | Impact | Severity |
|-------|--------|----------|
| **Lost language context** | Can't measure multilingual success rates | 🔴 High |
| **Trace-response mismatch** | Confusing when debugging non-English queries | 🔴 High |
| **Analytics blind spot** | Can't optimize for non-English users separately | 🟡 Medium |
| **Support debugging** | Harder to troubleshoot multilingual conversations | 🟡 Medium |

### Why This Matters for the KB Project

1. **Batch 1/2/Multilingual fixes** require accurate telemetry to measure impact
2. **Portuguese/Spanish users** are growing segment (evidenced by live traces)
3. **Can't measure what we don't log** — without original queries, we can't analyze multilingual performance
4. **Dashboard analytics** depend on accurate metadata for trending and optimization

### What This Fixes

✅ Preserves **original language** in Langfuse traces  
✅ Tracks **which language was asked** (for multilingual conversation analysis)  
✅ Allows **language-specific performance measurement** (IDK rate by language)  
✅ Enables **better debugging** of multilingual edge cases  
✅ Supports **future analytics** on non-English query patterns  

---

## Implementation Details

### File: `skill/kb_answer.py`

#### Step 1: Store Original Query Before Translation

**Location:** Lines 5616-5619

**Current Code:**
```python
query = _sanitize_kb_query(_extract_query(params))
if not query:
    raise ValueError("query is required")
query = _translate_key_terms(query)
```

**Change To:**
```python
query = _sanitize_kb_query(_extract_query(params))
if not query:
    raise ValueError("query is required")
original_query = query  # ← ADD THIS LINE
query = _translate_key_terms(query)
```

**Why:** Capture the original query before `_translate_key_terms()` overwrites the variable.

---

#### Step 2: Update `_send_langfuse` Function Signature

**Location:** Line 5482

**Current:**
```python
def _send_langfuse(
    trace_name: str,
    query: str,
    answer: str,
    results: List[Dict],
    explicit_module: str,
    intents: List[str],
    selected_answer_mode: str,
    clarification_asked: bool,
    latency_ms: int,
    context,
    params: Optional[Dict[str, Any]] = None,
    video_meta: Optional[Dict[str, Any]] = None,
    channel_type: Optional[str] = None,
) -> Dict:
```

**Change To:**
```python
def _send_langfuse(
    trace_name: str,
    query: str,
    answer: str,
    results: List[Dict],
    explicit_module: str,
    intents: List[str],
    selected_answer_mode: str,
    clarification_asked: bool,
    latency_ms: int,
    context,
    params: Optional[Dict[str, Any]] = None,
    video_meta: Optional[Dict[str, Any]] = None,
    channel_type: Optional[str] = None,
    original_query: Optional[str] = None,  # ← ADD THIS LINE
) -> Dict:
```

**Why:** Accept the original query as an optional parameter so we can pass it from kb_answer().

---

#### Step 3: Update Metadata Dictionary

**Location:** Lines 5518-5553 (metadata dict construction)

**Current (line 5522):**
```python
"query": q_prev,
```

**Change To:**
```python
"query": original_query or q_prev,  # Use original if provided, else translated
"query_translated": q_prev,  # Translated to English for processing
```

**Why:** Log both the original query (what user asked) and translated query (what system processes).

---

#### Step 4: Pass `original_query` to All `_send_langfuse` Calls

Add `original_query=original_query` parameter to every `_send_langfuse()` call in the `kb_answer()` function.

**Locations to Update:**

| Line | Context | Reason |
|------|---------|--------|
| ~5630 | Guardrail answer | Preserve original query for refusal intents |
| ~5646 | Undocumented topic | Preserve original query for unsupported topics |
| ~5662 | External gap | Preserve original query for integration gaps |
| ~5678 | Rate limit gap | Preserve original query for rate limit cases |
| ~5694 | Case study answer | Preserve original query for case study paths |
| ~5712 | Overview answer | Preserve original query for overview intents |
| ~5747 | Main answer | Preserve original query for standard answers |
| ~5861 | Final langfuse call | Preserve original query for final logging |

**Example:**
```python
langfuse = _send_langfuse(
    "kb_answer", query, answer, [], "General",
    ["refusal"], "refusal", False, latency_ms, context, params,
    channel_type=detected_channel,
    original_query=original_query,  # ← ADD THIS
)
```

**Why:** Ensure all telemetry paths capture and log the original (non-translated) query.

---

## File: `skill/kb_search.py`

Apply the same fix if it has similar code structure:

1. Store `original_query` before calling `_translate_key_terms()`
2. Pass `original_query` to any telemetry/logging functions
3. Log both original and translated queries in metadata

---

## Verification Checklist

- [ ] Original query is stored before translation (line ~5619)
- [ ] `original_query` parameter added to `_send_langfuse` signature (line ~5482)
- [ ] Metadata dict includes both `query` (original) and `query_translated` (English) (line ~5522)
- [ ] All 8 `_send_langfuse()` calls pass `original_query` parameter
- [ ] Same changes applied to `skill/kb_search.py` (if applicable)
- [ ] **Test Case 1:** Portuguese query `"¿Qué demostraciones son adecuadas para farmacéutica?"`
  - [ ] Verify Langfuse `metadata.query` shows original Portuguese text
  - [ ] Verify `metadata.query_translated` shows English version
- [ ] **Test Case 2:** Spanish query `"Muéstrame videos de creación de jornadas"`
  - [ ] Verify Langfuse shows Spanish original
  - [ ] Verify translated version is present
- [ ] **Test Case 3:** English query (regression test)
  - [ ] Verify trace is unchanged from before
  - [ ] Both `query` and `query_translated` should be identical for English queries
- [ ] No functional changes to query routing or response generation

---

## Expected Result

### Before Fix

**Langfuse Trace:**
```json
{
  "input": {
    "query": "what demonstrations are suitable for pharmaceutical?"
  },
  "metadata": {
    "query": "what demonstrations are suitable for pharmaceutical?",
    "answered": true
  }
}
```

**User Experience:**
- Asked in Spanish: `"¿Qué demostraciones...?"`
- Got Spanish response ✅
- But trace shows English query ❌

---

### After Fix

**Langfuse Trace:**
```json
{
  "input": {
    "query": "¿Qué demostraciones son adecuadas para farmacéutica?"
  },
  "metadata": {
    "query": "¿Qué demostraciones son adecuadas para farmacéutica?",
    "query_translated": "what demonstrations are suitable for pharmaceutical?",
    "answered": true
  }
}
```

**User Experience:**
- Asked in Spanish: `"¿Qué demostraciones...?"`
- Got Spanish response ✅
- Trace shows original Spanish query ✅

---

## Benefits

After implementing this change:

### For Analytics
- ✅ Track multilingual query patterns separately
- ✅ Measure IDK rate **by language** (which languages need help?)
- ✅ Identify language-specific edge cases

### For Debugging
- ✅ Easier to debug multilingual conversations
- ✅ Can match user's actual query to trace
- ✅ Better understanding of translation impact

### For Product Decisions
- ✅ Optimize KB content for specific languages
- ✅ Measure if multilingual fixes actually work
- ✅ Plan language-specific feature development

---

## Related Issues

- **Root Cause:** Multilingual translation layer (`_translate_key_terms()`) translates query BEFORE telemetry is logged
- **Affected Traces:** All Portuguese, Spanish, and Arabic queries since multilingual fix was deployed
- **Regression Risk:** None — only adding metadata fields, no logic changes

---

## Timeline

| Date | Event |
|------|-------|
| 2026-06-19 | Issue identified in telemetry analysis |
| 2026-06-19 | Fix instructions prepared |
| [TBD] | Implementation and testing |
| [TBD] | Deploy to production |

---

## Questions?

If you need clarification on any step, reference this document's:
- **Why section** (lines 8-50) for business context
- **Implementation Details** (lines 54+) for technical guidance
- **Verification Checklist** for testing approach
