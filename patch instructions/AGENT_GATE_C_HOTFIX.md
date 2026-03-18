# Gate C Hotfix — Fix 7 kb_search.py failures

**File:** `kb_search.py`
**Risk:** Medium — fixes guardrails, slug alignment, and result diversity.

> **IMPORTANT — DO NOT touch telemetry code.** All Langfuse integration, tracing, span logging, and telemetry-related functions/imports must remain exactly as they are.

---

## Fix 1 — Verify guardrail call exists in kb_search()

Open `def kb_search(` and verify these lines exist near the top of the function, BEFORE the `chunks = _load_chunks(context)` line:

```python
    guardrail = _guardrail_category(query)
    if guardrail:
```

If this block is missing, the guardrail is never checked and off-topic queries return results. Add it if missing — see Patch 9 for the full `kb_search()` function.

## Fix 2 — Harden OFFTOPIC_TERMS

Find `OFFTOPIC_TERMS` in `kb_search.py`. It currently looks like:

```python
OFFTOPIC_TERMS = [
    "cricket", "ipl", "football", "weather", "biryani", "pizza", "burger",
    "dinner", "gym", "workout", "diet", "movie", "japan", "iphone",
    "birthday", "bored", "motivational",
]
```

Replace with:

```python
OFFTOPIC_TERMS = [
    "cricket", "ipl", "football", "weather", "biryani", "pizza", "burger",
    "dinner", "gym", "workout", "diet", "movie", "japan", "iphone",
    "birthday", "bored", "motivational", "joke", "tell me a joke",
    "salesforce", "hubspot", "zoho",
]
```

## Fix 3 — Add real KB slug aliases to source_boosts

The concept registry's `source_boosts` slugs must match the real KB source paths. Several don't. Apply these changes:

### 3a — save_deploy: add real slug

Find the `save_deploy` entry in `CONCEPT_REGISTRY`. Change its `source_boosts`:

```python
        "source_boosts": {"save-vs-save-deploy": 5.0},
```

Replace with:

```python
        "source_boosts": {"save-vs-save-deploy": 5.0, "save-save-and-deploy": 5.0},
```

### 3b — webhooks: add penalty for wrong page

Find the `webhooks` entry. Change its `source_penalties`:

```python
        "source_penalties": {"others-webhooks": -3.0},
```

Replace with:

```python
        "source_penalties": {"others-webhooks": -3.0, "callback-url-event-on-starting-node": -4.0},
```

### 3c — assignment_rules: add real slug for console 7.0

Find the `assignment_rules` entry. Change its `source_boosts`:

```python
        "source_boosts": {"chat-management-assignment-rules": 5.0},
```

Replace with:

```python
        "source_boosts": {"chat-management-assignment-rules": 5.0, "assignment-enhancements-in-console-7-0": 4.0},
```

## Fix 4 — Add result diversity for multi-concept queries

The current `_apply_feature_lock` keeps all chunks matching ANY entity's boost slugs. For multi-concept queries like "business hours vs auto replies", this lets one concept's chunks dominate. Replace the entire `_apply_feature_lock` function with:

```python
def _apply_feature_lock(scored: List[Dict], entities: List[Dict]) -> List[Dict]:
    if not entities:
        return scored

    per_entity = []
    for entity in entities:
        tokens = list(entity.get("source_boosts", {}).keys())
        if not tokens:
            continue
        matching = [
            row for row in scored
            if any(tok in str(row.get("source") or "").lower() for tok in tokens)
        ]
        if matching:
            per_entity.append(matching)

    if not per_entity:
        return scored

    if len(per_entity) == 1:
        return per_entity[0] if per_entity[0] else scored

    merged = []
    seen_ids = set()
    max_len = max(len(bucket) for bucket in per_entity)
    for i in range(max_len):
        for bucket in per_entity:
            if i < len(bucket):
                cid = bucket[i].get("chunk_id", id(bucket[i]))
                if cid not in seen_ids:
                    seen_ids.add(cid)
                    merged.append(bucket[i])
    return merged if merged else scored
```

This interleaves results from each entity's matching chunks in round-robin order, ensuring both concepts get representation in the top-k.

## Smoke test — verify fixes

Run these queries using `kb_search` and report results:

| # | Query | Expected |
|---|-------|----------|
| N1 | `"Tell me a joke"` | Empty results (guardrail) |
| N2 | `"How do I make pizza?"` | Empty results (guardrail) |
| S4 | `"save vs save & deploy"` | Top source contains `save-save-and-deploy` or `save-vs-save-deploy` |
| S5 | `"Where do I add a webhook callback URL?"` | Top source does NOT contain `callback-url-event-on-starting-node` |
| M1 | `"business hours vs auto replies"` | Top 5 includes BOTH `user-management-business-hours` and `response-management-auto-replies` sources |

---
**After this hotfix, re-run the full Gate C validation.**
