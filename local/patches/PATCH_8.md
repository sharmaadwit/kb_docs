# Patch 8 — `kb_answer.py` (production regression follow-up)

This file documents **Patch 8** only. Apply it **after** Patches **1–7** (see `PATCH_INSTRUCTIONS.md` and `LATEST_PATCHES.md` for Patch 7).

**Target file:** `kb_answer.py` only.

---

## What it fixes

| Symptom | Change |
|--------|--------|
| “Campaign in queue” still ranking **Campaign Analytics** | Penalize `campaign-analytics` when query has queue + campaign (not only Personalize). |
| Dynamic / tracked link queries still ranking **Campaign Analytics** too strongly | Raise `campaign-analytics` penalty in the dynamic-link phrase block from **-6** to **-8**. |
| “SMTP … Agent Assist” ranking **Assignment Rules** | Penalize `chat-management-assignment-rules` / `assignment-rules` paths when SMTP + Agent Assist. |
| “Give me an overview of Agent Assist …” returning a **narrow entity template** (e.g. Assignment Rules) | Overview intent no longer requires `len(entities) <= 1`; **`_compose_answer`** skips entity templates when `intent == "overview"`. |

**What it does not fix:** Loader/config issues (404 index path, `chunks` as `int`, missing chunk files). Those must be fixed in deployment.

---

## Step 8a — Extend `_query_source_penalty_adjustment`

**If you already have Patch 7’s function**, replace the body with the version below (or apply these edits):

1. **Inside** the `if ("queue" in q or "queued" in q) and "campaign" in q:` block, **after** the Personalize `if`, add:

```python
        if "campaign-analytics" in s:
            adj -= 8.0
```

2. **In** the dynamic-link `if any(ph in q for ph in (...)):` block, change the `campaign-analytics` line from `adj -= 6.0` to **`adj -= 8.0`** (if still at -6).

3. **Inside** `if any(ph in q for ph in ("smtp", "email server", "mail server")):` and `if "agent assist" in q:`, **after** the marketing-templates `if` block, add:

```python
            if "chat-management-assignment-rules" in s or "assignment-rules" in s:
                adj -= 10.0
```

**Full function after Patch 8** (drop-in replacement if unsure):

```python
def _query_source_penalty_adjustment(q: str, source: str) -> float:
    """Negative score deltas when query semantics conflict with frequent mis-ranked sources."""
    s = source.lower()
    adj = 0.0
    if ("queue" in q or "queued" in q) and "campaign" in q:
        if "personalize-enabled-campaign-manager" in s or "personalize/personalize-enabled" in s:
            adj -= 8.0
        if "campaign-analytics" in s:
            adj -= 8.0
    if any(
        ph in q
        for ph in (
            "dynamic link",
            "dynamic links",
            "link tracking",
            "tracked dynamic",
        )
    ):
        if "sending-an-automated-campaign" in s:
            adj -= 8.0
        if "personalize-enabled-campaign-manager" in s or "personalize/personalize-enabled" in s:
            adj -= 8.0
        if "campaign-analytics" in s:
            adj -= 8.0
    if any(ph in q for ph in ("smtp", "email server", "mail server")):
        if "agent assist" in q:
            if "sending-marketing-templates" in s or "marketing-templates-from-agent" in s:
                adj -= 10.0
            if "chat-management-assignment-rules" in s or "assignment-rules" in s:
                adj -= 10.0
    return adj
```

Ensure **`_score_chunk`** still ends with `score += _query_source_penalty_adjustment(q, source)` before `return score` (Patch 7).

---

## Step 8b — `_classify_intent`: overview without entity-count gate

In **`_classify_intent`**, find:

```python
    is_overview = any(x in q for x in _OVERVIEW_SIGNALS)
    if is_overview and len(entities) <= 1:
        return "overview"
```

**Replace** with:

```python
    is_overview = any(x in q for x in _OVERVIEW_SIGNALS)
    if is_overview:
        return "overview"
```

So explicit overview phrasing always wins over falling through to **`setup`** when multiple entities match (e.g. “overview of Agent Assist” with several weak entity hits).

---

## Step 8c — `_compose_answer`: skip templates for overview

In **`_compose_answer`**, **immediately after** the `if intent == "compare" and len(entities) >= 2:` block (after its `return answer`), **before** the comment `# --- Single-entity template lookup`, **insert**:

```python
    if intent == "overview":
        return _compose_from_evidence(query, intent, evidence, lines, entities)
```

Overview answers then use evidence composition (including Patch 7 overview diversity in `_select_evidence` when that branch is active), not a single entity’s setup template.

---

## Verify

```bash
python3 -m py_compile kb_answer.py
grep -n 'if intent == "overview":' kb_answer.py
grep -n campaign-analytics kb_answer.py | head
```

Expect **two** sensible hits for overview (`_classify_intent` / `_compose_answer` / `_select_evidence` / `_has_explicit_support` — at minimum `_compose_answer` must contain the new early return). Expect **`campaign-analytics`** in `_query_source_penalty_adjustment` **twice** (queue block + dynamic-link block).

---

## Summary

| Piece | Role |
|-------|------|
| Queue + `campaign-analytics` penalty | Stops analytics doc from winning pure “in queue” troubleshooting phrasing. |
| Stronger `campaign-analytics` under dynamic-link phrases | Aligns with eval misroutes to analytics. |
| SMTP + Agent Assist + assignment-rules penalty | Stops assignment doc from winning mail-server setup questions. |
| Overview intent + no entity templates | Stops one narrow template from replacing multi-page overview behavior. |

---

## `kb_search.py`

Not modified. Mirror penalty or ranking logic there only if product search must stay aligned with answer ranking.
