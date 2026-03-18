# Local-only patches

Apply these only in your local repo (e.g. when running regression scripts). **Do not send to the agent/skill** — the skill does not contain these files.

---

## tmp_regression_500.py — refusal_terms (for negative-kind scoring)

**File:** `tmp_regression_500.py`  
**Location:** Inside `score_text()`, in the `refusal_terms` list when `kind == "negative"`.

**Find (exact):**
```python
            "i don t know based on the docs",
            "documented gupshup console question",
```

**Replace with:**
```python
            "i don t know based on the docs",
            "i don t know based on the documentation provided",
            "documented gupshup console question",
            "documented gupshup console capability",
```

So the guardrail reply “I don’t know based on the documentation provided…” scores as pass for negative/unsupported questions in local regression runs.
