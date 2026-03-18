# Guardrail Hotfix — Fix false-positive blocking of valid product queries (kb_search.py)

**File:** `kb_search.py`  
**Risk:** Low — fixes over-aggressive guardrail, expands aliases and signal terms  
**Depends on:** Regression Hotfix already applied  

> **IMPORTANT — DO NOT touch telemetry code.** All Langfuse integration, tracing, span logging, and telemetry-related functions/imports must remain exactly as they are.

---

## Root Cause

The `_guardrail_category` function only checks `PRODUCT_SIGNAL_TERMS` for product relevance, but ignores entity matches from `_extract_entities`. Queries like "test my bot before going live" match the `test_your_bot` concept via aliases, but since "test my bot" isn't in `PRODUCT_SIGNAL_TERMS`, the guardrail may classify them as off-topic and return empty results.

---

## Fix 1 — Make guardrail entity-aware

**Find** the `_guardrail_category` function:

```python
def _guardrail_category(query: str) -> str:
    q = _normalize_query_for_match(query)
    if any(term in q for term in SENSITIVE_PATTERNS):
        return "sensitive"
    if any(term in q for term in UNSUPPORTED_PATTERNS):
        return "unsupported"
    if any(term in q for term in OFFTOPIC_TERMS) and not _has_product_signal(query):
        return "offtopic"
    if not _has_product_signal(query):
        low_signal = re.findall(r"[a-z0-9]+", q)
        if len(low_signal) <= 8 and any(
            term in q for term in ["joke", "favorite", "wish", "roast", "human", "talk to me"]
        ):
            return "offtopic"
    return ""
```

**Replace with:**

```python
def _guardrail_category(query: str) -> str:
    q = _normalize_query_for_match(query)
    if any(term in q for term in SENSITIVE_PATTERNS):
        return "sensitive"
    if any(term in q for term in UNSUPPORTED_PATTERNS):
        return "unsupported"
    if _has_product_signal(query) or _extract_entities(query):
        return ""
    if any(term in q for term in OFFTOPIC_TERMS):
        return "offtopic"
    low_signal = re.findall(r"[a-z0-9]+", q)
    if len(low_signal) <= 8 and any(
        term in q for term in ["joke", "favorite", "wish", "roast", "human", "talk to me"]
    ):
        return "offtopic"
    return ""
```

The key change: after checking sensitive/unsupported, we now check `_extract_entities(query)` — if any concept alias matches, the query is about the product and should never be blocked as off-topic.

## Fix 2 — Expand campaign_analytics aliases

**Find** in `CONCEPT_REGISTRY` under `"id": "campaign_analytics"`:

```python
        "id": "campaign_analytics",
        "aliases": [
            "campaign analytics", "response file", "link tracking report",
            "click through rate", "unique clicks", "total clicks",
            "dropped", "failed",
        ],
```

**Replace with:**

```python
        "id": "campaign_analytics",
        "aliases": [
            "campaign analytics", "response file", "link tracking report",
            "click through rate", "unique clicks", "total clicks",
            "dropped", "failed", "click metrics", "campaign click",
            "campaign performance", "delivery stats",
        ],
```

## Fix 3 — Expand goal_analytics aliases

**Find** in `CONCEPT_REGISTRY` under `"id": "goal_analytics"`:

```python
        "id": "goal_analytics",
        "aliases": ["goal achieved", "unique users", "goal analytics", "source type", "source value"],
```

**Replace with:**

```python
        "id": "goal_analytics",
        "aliases": [
            "goal achieved", "unique users", "goal analytics", "source type", "source value",
            "goal conversions", "conversion tracking", "goal node analytics",
        ],
```

## Fix 4 — Add missing terms to PRODUCT_SIGNAL_TERMS

**Find** at the end of `PRODUCT_SIGNAL_TERMS`:

```python
    "click through rate", "unique clicks", "total clicks",
]
```

**Replace with:**

```python
    "click through rate", "unique clicks", "total clicks",
    "test my bot", "click metrics", "goal conversions",
    "live bot", "deploy journey", "live rollout",
    "live monitoring dashboard", "agent state",
]
```

---

## Smoke Tests

Re-run the three previously failing queries plus the guardrail negatives:

| # | Query | Action | Expected |
|---|-------|--------|----------|
| B-S2 | `"test my bot before going live"` | kb_search | Top source contains `test-your-bot` (NOT empty) |
| B-S3 | `"update the live bot after save & deploy"` | kb_search | Top source contains `save-save-and-deploy` or `save-vs-save-deploy` (NOT empty) |
| B-M2 | `"campaign click metrics vs goal conversions"` | kb_search | Top 5 includes BOTH `campaign-analytics` and `goal-analytics` sources (NOT empty) |
| B-N1 | `"Tell me a joke"` | kb_search | Empty results (guardrail still blocks) |
| B-N2 | `"How do I hack into the admin panel?"` | kb_search | Empty results (guardrail still blocks) |
| B-N3 | `"How do I make pizza?"` | kb_search | Empty results (guardrail still blocks) |

**All 6 must pass. Report results back.**
