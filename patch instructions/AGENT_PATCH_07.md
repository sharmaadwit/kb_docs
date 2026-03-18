# Patch 7 of 9 — Dead code cleanup (kb_answer.py)

**File:** `kb_answer.py`
**Depends on:** Patch 6 passing Gate B with no regressions
**Risk:** Low — removes code that is no longer called. If Patch 6 passed regression, this is safe.
**What it does:** Deletes old functions and data structures that are fully replaced by the new pipeline. Renames `_score_chunk_v2` to `_score_chunk`.

> **IMPORTANT — DO NOT touch telemetry code.** All Langfuse integration, tracing, span logging, and telemetry-related functions/imports must remain exactly as they are. Only delete the specific functions listed below.

## Step 1 — Rename _score_chunk_v2 → _score_chunk

**Find (exact):**
```
def _score_chunk_v2(
```

**Replace with:**
```
def _score_chunk(
```

Also update the one caller in `kb_answer()`:

**Find (exact):**
```
        s = _score_chunk_v2(query, c, entities, explicit_module)
```

**Replace with:**
```
        s = _score_chunk(query, c, entities, explicit_module)
```

## Step 2 — Delete old _score_chunk

The old `_score_chunk` function (the one that does NOT take `entities` as a parameter) should now be deleted entirely. It was the version with only `query`, `chunk`, and `explicit_module` parameters. Find it and delete the entire function body.

If it no longer exists (because Step 1 already overwrote it), skip this step.

## Step 3 — Delete _handle_exact_cases

If the file contains a function called `def _handle_exact_cases(`, delete the **entire** function. This was the ~960-line block of hardcoded answers now replaced by `_compose_answer`.

## Step 4 — Delete FEATURE_RULES

If the file contains a dict called `FEATURE_RULES = {`, delete the entire dictionary. It is replaced by `source_boosts` and `source_penalties` inside `CONCEPT_REGISTRY`.

## Step 5 — Delete any other dead references

Search the file for any remaining calls to `_handle_exact_cases` or `FEATURE_RULES`. If found, delete those lines.

## Test — Sanity check

Results should be **identical** to Patch 6 output since this patch only removes unused code. Re-run these from the Patch 6 smoke tests:

| # | Query | Expected in answer |
|---|-------|-------------------|
| S1 | `"Where do I configure business hours?"` | Mentions **User Management: Business Hours** |
| S6 | `"How do I collect text user input in a journey?"` | Mentions **Prompt Node** |
| M1 | `"Should I check business hours or auto replies for away messages?"` | Mentions both **Business Hours** and **Auto Replies** |
| N1 | `"How do I make pizza?"` | Refuses: off-topic |
| N4 | `"How do I hack into the admin panel?"` | Refuses: sensitive |

If ANY of these differ from Patch 6 output, the cleanup deleted something that was still in use — revert and investigate.

---
**Next:** Patch 8 applies the concept registry and new scoring to `kb_search.py`.
