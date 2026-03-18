# Version Stamp — Set logic_version in telemetry metadata (kb_answer.py + kb_search.py)

**Files:** `kb_answer.py` and `kb_search.py`  
**Risk:** Zero — only changes a metadata string value. No logic, no telemetry structure, no behavior change.  
**Purpose:** Stamp the redesigned runtime version so Langfuse traces can be filtered by `logic_version` to compare pre-redesign vs post-redesign accuracy.

> **IMPORTANT — DO NOT touch any other telemetry code.** Only change the `logic_version` value as described below. All Langfuse integration, tracing, span logging, and telemetry-related functions/imports must remain exactly as they are.

---

## Step 1 — kb_answer.py

**Find** in the `metadata` dict inside the `kb_answer()` function (near the bottom of the function):

```python
        "logic_version": None,
```

**Replace with:**

```python
        "logic_version": "kb-answer-v2.0-concept-registry",
```

## Step 2 — kb_search.py

**Find** in the `metadata` dict inside the `kb_search()` function:

```python
            "logic_version": context.get_secret("KB_LOGIC_VERSION") if context else "search-telemetry-v1",
```

**Replace with:**

```python
            "logic_version": "kb-search-v2.0-concept-registry",
```

---

## Verification

After applying both changes, run one query through each action and check the Langfuse trace metadata:

| Action | Query | Expected `logic_version` in trace |
|--------|-------|-----------------------------------|
| kb_answer | `"What is sticky assignment?"` | `kb-answer-v2.0-concept-registry` |
| kb_search | `"condition node"` | `kb-search-v2.0-concept-registry` |

If both traces show the new version string, the stamp is live. You can now filter Langfuse by `logic_version` to isolate all post-redesign traffic.
