# Patch 9 of 9 — Swap kb_search() to new pipeline + cleanup (BEHAVIOR CHANGE)

**File:** `kb_search.py`
**Depends on:** Patch 8
**Risk:** Medium — changes search ranking behavior. Run regression after applying.
**What it does:** Replaces `kb_search()` to use `_score_chunk_v2`, `_extract_entities`, `_classify_intent`, and `_apply_feature_lock_v2`. Then cleans up old functions.

> **IMPORTANT — DO NOT touch telemetry code.** All Langfuse integration, tracing, span logging, and telemetry-related functions/imports must remain exactly as they are. The new `kb_search()` function retains all existing Langfuse trace/span calls. Preserve them exactly.

## Step 1 — Replace kb_search()

Find the entire `def kb_search(` function. Replace it with:

```python
def kb_search(parameters: object = None, context=None, **kwargs) -> dict:
    params = _parse_parameters(parameters, **kwargs)
    query = _extract_query(params)
    top_k = int(params.get("top_k") or 5)
    if not query:
        raise ValueError("query is required")

    started = datetime.now(timezone.utc)
    guardrail = _guardrail_category(query)
    if guardrail:
        latency_ms = int((datetime.now(timezone.utc) - started).total_seconds() * 1000)
        langfuse = _compact_langfuse(
            "kb_search", query, [], "General", [guardrail], "refusal", latency_ms, context,
        )
        return {
            "ok": True,
            "query": query,
            "top_k": top_k,
            "results": [],
            "langfuse": {
                "ok": langfuse["ok"],
                "trace_id": langfuse["trace_id"],
                "module_label": langfuse["metadata"]["module_label"],
                "module_source": langfuse["metadata"]["module_source"],
            },
        }

    chunks = _load_chunks(context)
    explicit_module = _detect_module(query)
    entities = _extract_entities(query)
    intents = _detect_intents(query)
    preferred_mode = _classify_intent(query, entities)

    scored = []
    for c in chunks:
        s = _score_chunk_v2(query, c, entities, explicit_module)
        if s > 0:
            row = dict(c)
            row["score"] = s
            scored.append(row)
    scored.sort(key=lambda x: x.get("score", 0.0), reverse=True)
    scored = _apply_feature_lock_v2(scored, entities)

    results = scored[:top_k]
    latency_ms = int((datetime.now(timezone.utc) - started).total_seconds() * 1000)
    langfuse = _compact_langfuse(
        "kb_search", query, results, explicit_module, intents, preferred_mode, latency_ms, context,
    )
    return {
        "ok": True,
        "query": query,
        "top_k": top_k,
        "results": results,
        "langfuse": {
            "ok": langfuse["ok"],
            "trace_id": langfuse["trace_id"],
            "module_label": langfuse["metadata"]["module_label"],
            "module_source": langfuse["metadata"]["module_source"],
        },
    }
```

## Step 2 — Rename _v2 functions and delete old versions

**Rename _score_chunk_v2 → _score_chunk:**

Find `def _score_chunk_v2(` and replace with `def _score_chunk(`.
Find `s = _score_chunk_v2(` in `kb_search()` and replace with `s = _score_chunk(`.

**Rename _apply_feature_lock_v2 → _apply_feature_lock:**

Find `def _apply_feature_lock_v2(` and replace with `def _apply_feature_lock(`.
Find `_apply_feature_lock_v2(scored` in `kb_search()` and replace with `_apply_feature_lock(scored`.

**Delete old _score_chunk** (the version without `entities` parameter).

**Delete old _apply_feature_lock** (the version without `entities` parameter).

**Delete old FEATURE_RULES** dict if it exists.

## Test — Gate C (BEHAVIOR CHANGE — search ranking)

### Smoke tests — search ranking (top result should match expected source)

| # | Query | Expected top source contains |
|---|-------|------------------------------|
| S1 | `"condition node"` | `condition-node` |
| S2 | `"api node in journey builder"` | `api-node` |
| S3 | `"business hours"` | `user-management-business-hours` |
| S4 | `"save vs save & deploy"` | `save-vs-save-deploy` |
| S5 | `"Where do I add a webhook callback URL?"` | `integrations/webhooks` |
| S6 | `"sticky assignment"` | `chat-management-assignment-rules` |

### Smoke tests — negative (should return empty results)

| # | Query | Expected |
|---|-------|----------|
| N1 | `"Tell me a joke"` | Empty results (guardrail) |
| N2 | `"How do I make pizza?"` | Empty results (guardrail) |

### Smoke tests — multi-concept (top results should cover both concepts)

| # | Query | Expected in top 5 results |
|---|-------|--------------------------|
| M1 | `"business hours vs auto replies"` | Both `user-management-business-hours` and `response-management-auto-replies` |
| M2 | `"campaign click metrics vs goal conversions"` | Both `campaign-analytics` and `goal-analytics` |

### If regressions appear

- Revert only Steps 1-2 (restore old `kb_search()`, old `_score_chunk`, old `_apply_feature_lock`)
- The concept registry and new functions from Patch 8 stay harmlessly in the file
- Fix the scoring issue and re-apply

---
**All 9 patches complete.**

## Full sequence and gate map

```
Patch 1  ─ Concept Registry A          ─ additive ─ Gate A (no change)
Patch 2  ─ Concept Registry B          ─ additive ─ Gate A
Patch 3  ─ Concept Registry C + Overrides ─ additive ─ Gate A
Patch 4  ─ Entity + Intent functions   ─ additive ─ Gate A
Patch 5  ─ Scoring v2 + Evidence + Composition ─ additive ─ Gate A
                                                     ▼
Patch 6  ─ Swap kb_answer() pipeline   ─ BEHAVIOR CHANGE ─ Gate B (regression_250, 18, 150)
                                                     ▼
Patch 7  ─ Delete dead code in kb_answer.py ─ cleanup ─ sanity check
Patch 8  ─ kb_search.py registry + v2 functions ─ additive ─ Gate A
                                                     ▼
Patch 9  ─ Swap kb_search() + cleanup  ─ BEHAVIOR CHANGE ─ Gate C (regression_500, 1000)
```

Patches 1-5 and 8 are zero-risk (additive only).
Patches 6 and 9 are the only behavior changes — each has a dedicated regression gate.
Patches 7 is cleanup after 6 is proven.
