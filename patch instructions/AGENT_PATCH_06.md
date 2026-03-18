# Patch 6 of 9 — Swap kb_answer() to new pipeline (BEHAVIOR CHANGE)

**File:** `kb_answer.py`
**Depends on:** Patch 5
**Risk:** Medium — this is the first patch that changes live answer behavior. Run full regression after applying.
**What it does:** Replaces the `kb_answer()` main function to use the new pipeline: entity extraction → intent classification → `_score_chunk_v2` → evidence selection → answer composition. The old `_score_chunk`, `_handle_exact_cases`, and `FEATURE_RULES` still exist in the file but are no longer called.

> **IMPORTANT — DO NOT touch telemetry code.** All Langfuse integration, tracing, span logging, and telemetry-related functions/imports must remain exactly as they are. The new `kb_answer()` function retains all existing Langfuse trace/span calls. Preserve them exactly.

## Step 1 — Add _utc_now_iso if missing

Check if `def _utc_now_iso` exists. If not, add before `def _normalize_query_for_match`:

```python
def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


```

## Step 2 — Replace kb_answer()

Find the entire `def kb_answer(` function (from `def kb_answer` through its final `return`). Replace it with:

```python
def kb_answer(parameters: object = None, context=None, **kwargs) -> dict:
    params = _parse_parameters(parameters, **kwargs)
    query = _extract_query(params)
    if not query:
        raise ValueError("query is required")

    started = datetime.now(timezone.utc)

    guardrail = _guardrail_answer(query)
    if guardrail:
        latency_ms = int((datetime.now(timezone.utc) - started).total_seconds() * 1000)
        langfuse = _send_langfuse(
            "kb_answer", query, guardrail, [], "General",
            ["refusal"], "refusal", False, latency_ms, context,
        )
        return {"ok": True, "query": query, "answer": guardrail, "citations": [], "langfuse": langfuse}

    chunks = _load_chunks(context)
    explicit_module = _detect_module(query)
    entities = _extract_entities(query)
    intent = _classify_intent(query, entities)
    intents_list = _detect_intents(query)

    scored = []
    for c in chunks:
        s = _score_chunk_v2(query, c, entities, explicit_module)
        if s > 0:
            row = dict(c)
            row["score"] = s
            scored.append(row)
    scored.sort(key=lambda x: x.get("score", 0.0), reverse=True)

    evidence = _select_evidence(query, scored, intent, explicit_module)
    answer = _compose_answer(query, intent, entities, evidence)

    latency_ms = int((datetime.now(timezone.utc) - started).total_seconds() * 1000)
    langfuse = _send_langfuse(
        "kb_answer", query, answer, evidence, explicit_module,
        intents_list, intent, False, latency_ms, context,
    )
    return {"ok": True, "query": query, "answer": answer, "citations": [], "langfuse": langfuse}
```

Note: this calls `_score_chunk_v2` (the new function from Patch 5), NOT the old `_score_chunk`.

## Test — Gate B (BEHAVIOR CHANGE — run full regression)

This is the critical gate. Run **all** regression sets and compare against the baseline you saved before Patch 1.

### Smoke tests — single intent (answer should mention the expected page/concept)

| # | Query | Expected in answer |
|---|-------|-------------------|
| S1 | `"Where do I configure business hours?"` | Mentions **User Management: Business Hours** |
| S2 | `"What is sticky assignment?"` | Mentions **Sticky Assignment** |
| S3 | `"How do I test my bot before going live?"` | Mentions **Test your Bot** |
| S4 | `"What does Goal Achieved mean in goal analytics?"` | Mentions **Goal Analytics** |
| S5 | `"Where do I add a webhook callback URL?"` | Mentions **Webhooks** |
| S6 | `"How do I collect text user input in a journey?"` | Mentions **Prompt Node** |
| S7 | `"What happens when a prompt node times out?"` | Mentions **Timeout in Prompt Nodes** |
| S8 | `"Which dashboard shows ongoing chats and wait time metrics?"` | Mentions **Live Monitoring Dashboard** |

### Smoke tests — multi-intent / compare (answer should cover both sides)

| # | Query | Expected in answer |
|---|-------|-------------------|
| M1 | `"Should I check business hours or auto replies for away messages?"` | Mentions both **Business Hours** and **Auto Replies** |
| M2 | `"What is the difference between save and save & deploy?"` | Compare-style answer about **Save vs Save & Deploy** |
| M3 | `"Which page shows campaign click metrics vs goal conversions?"` | Mentions both **Campaign Analytics** and **Goal Analytics** |
| M5 | `"Where do I configure sticky assignment vs assignment rules?"` | Mentions both in a compare answer |
| M6 | `"CTWA traffic or campaign analytics — where do I check conversions?"` | Mentions both **CTWA** and **Campaign Analytics** |

### Smoke tests — negative / off-topic (should refuse)

| # | Query | Expected behavior |
|---|-------|-------------------|
| N1 | `"How do I make pizza?"` | Refuses: "I can help only with documented Gupshup Console and KB topics" |
| N2 | `"What is the weather today?"` | Refuses: "I can help only with documented Gupshup Console and KB topics" |
| N3 | `"Tell me about Salesforce CRM integrations"` | Refuses: off-topic (OFFTOPIC_TERMS) |
| N4 | `"How do I hack into the admin panel?"` | Refuses: sensitive query (SENSITIVE_PATTERNS) |

### If regressions appear

- Note which queries regressed and which intent/entity was involved
- You can revert ONLY this patch (restore the old `kb_answer()` function) and the system returns to pre-Patch-6 behavior — all data and new functions from Patches 1-5 remain harmlessly in the file
- Fix the regression in the composition/scoring logic and re-apply

**If green:** proceed to Patch 7 (dead code cleanup).

---
**Next:** Patch 7 removes old dead code that is no longer called.
