# Trace userId Fix Report — USER_EMAIL Env Override Bug

**Date:** 2026-07-10
**Scope:** kb_answer traces, 2026-07-01T00:00:00Z → 2026-07-10T08:00:00Z (before fix deployed)
**Script:** `local/scripts/fix_userid_env_override.py`
**Raw results:** `local/reports/userid_fix_results.json`

## Summary

| Category | Count |
|---|---|
| Total kb_answer traces in window | 350 |
| Already correct (userId == metadata.user_email) | 311 |
| **Mismatched (env override) — FIXED** | **1** |
| acct:N:unknown fallback (no metadata email) | 1 |
| Numeric userId, no metadata email | 3 |
| No userId at all (mostly local/automated tests) | 34 |
| Failed fixes | 0 |

## Fixed Traces (before → after)

| Trace ID | Old userId | New userId | Method | Verified |
|---|---|---|---|---|
| `kb-kb_answer-88ee9717cdde49f5` | adwit.sharma@gupshup.io | harishmanekscorpion@gmail.com | ingestion upsert | ✅ |

Only one env-override mismatch existed in the window — the previously known
2026-07-03 pollution incident had already been cleaned up by
`local/scripts/fix_polluted_traces.py`, which explains the low count.

## Method Notes

- `PATCH /api/public/traces/{id}` is **not supported** by Langfuse Cloud
  (the older fix script's PATCH calls would not have succeeded either).
- The working method is the **ingestion API upsert**: `POST /api/public/ingestion`
  with a `trace-create` event reusing the existing trace `id` and original
  `timestamp`, supplying only the corrected `userId`. Other fields (metadata,
  input/output, observations) are preserved by the merge.
- Ingestion is asynchronous — verification succeeded ~10s after the update.

## Unfixable Traces (no metadata.user_email to restore from)

| Trace ID | userId | Recommendation |
|---|---|---|
| `kb-kb_answer-9698b8b31035454b` | acct:2:unknown | user_id 2 = `visitor-8cbe2c97-...@ccexpress.gupshup.io` per `local/reports/uid_map_out.json` (anonymous CC Express visitor). Could be relabelled to that visitor email if desired — left as-is since it's not an env-override mismatch. |
| `kb-kb_answer-1e702707ba7f4975` | 2 | Same as above (numeric uid 2). |
| `kb-kb_answer-b39631122f524b34` | 2 | Same as above. |
| `kb-kb_answer-ce63f69d29c74702` | 2 | Same as above. |

34 traces have no userId at all — these are local/automated test runs
(trace_env=local) and intentionally carry no user identity; no action needed.

## Conclusion

- **1/1 mismatched traces fixed and verified.** 0 failures.
- New traces post-2026-07-10 08:00 UTC carry the correct userId from the code fix.
- Re-running the script is safe/idempotent (`--dry-run` to audit anytime).
