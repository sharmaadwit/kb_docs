# Hotfix — AI Admin Intents/Entities Alias Gap

**Risk:** Low  
**Files:** `kb_answer.py`, `kb_search.py`  
**Telemetry modified:** No

## Problem

The query *"What is the difference between intents and entities in AI Admin?"* fails to trigger the compare path because the `ai_admin_intents` registry entry has no alias that appears as a substring of the normalized query. The word `"intents"` sits between `"between"` and `"and"`, so multi-word aliases like `"ai intents"` and `"ai admin intents"` never match.

Only `ai_admin_entities` is extracted (via `"entities in ai admin"`), so the compare path requires 2+ entities and falls back to a single-entity page answer.

## Fix

Add the bare alias `"intents"` and the phrase `"intents in ai admin"` to `ai_admin_intents`, and add the bare alias `"entities"` to `ai_admin_entities` — in **both** files.

---

## Step 1 — `kb_answer.py`

### 1a. Update `ai_admin_intents` aliases

Find this block:

```python
        "id": "ai_admin_intents",
        "aliases": [
            "ai intents", "intent creation", "create intent",
            "intent naming", "intent description", "ai admin intents",
            "intent guidelines", "user intent",
        ],
```

Replace with:

```python
        "id": "ai_admin_intents",
        "aliases": [
            "intents", "ai intents", "intent creation", "create intent",
            "intent naming", "intent description", "ai admin intents",
            "intent guidelines", "user intent", "intents in ai admin",
        ],
```

### 1b. Update `ai_admin_entities` aliases

Find this block:

```python
        "id": "ai_admin_entities",
        "aliases": [
            "ai entities", "entity creation", "create entity",
            "entity description", "ai admin entities",
            "entities in ai admin",
        ],
```

Replace with:

```python
        "id": "ai_admin_entities",
        "aliases": [
            "entities", "ai entities", "entity creation", "create entity",
            "entity description", "ai admin entities",
            "entities in ai admin",
        ],
```

---

## Step 2 — `kb_search.py`

### 2a. Update `ai_admin_intents` aliases

Find this block:

```python
        "id": "ai_admin_intents",
        "aliases": [
            "ai intents", "intent creation", "create intent",
            "intent naming", "intent description", "ai admin intents",
            "intent guidelines", "user intent",
        ],
```

Replace with:

```python
        "id": "ai_admin_intents",
        "aliases": [
            "intents", "ai intents", "intent creation", "create intent",
            "intent naming", "intent description", "ai admin intents",
            "intent guidelines", "user intent", "intents in ai admin",
        ],
```

### 2b. Update `ai_admin_entities` aliases

Find this block:

```python
        "id": "ai_admin_entities",
        "aliases": [
            "ai entities", "entity creation", "create entity",
            "entity description", "ai admin entities",
            "entities in ai admin",
        ],
```

Replace with:

```python
        "id": "ai_admin_entities",
        "aliases": [
            "entities", "ai entities", "entity creation", "create entity",
            "entity description", "ai admin entities",
            "entities in ai admin",
        ],
```

---

## Smoke Tests

| ID | Action | Query | Expected |
|----|--------|-------|----------|
| H-S1 | `kb_answer` | What is the difference between intents and entities in AI Admin? | Answer compares intents vs entities (mentions "Use Intents when" and "Use Entities when"), NOT a single-entity page answer |
| H-S2 | `kb_answer` | What are intents in AI Admin? | Answer mentions intents / Intent Creation (not broken) |
| H-S3 | `kb_answer` | What is sticky assignment? | Answer mentions Sticky Assignment (no regression) |
| H-S4 | `kb_answer` | How do I make pizza? | Refused (off-topic, no regression) |
