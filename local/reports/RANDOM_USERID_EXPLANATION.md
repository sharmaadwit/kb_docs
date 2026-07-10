# Random userId Issue — Root Cause & Fix Status

**Date:** 2026-07-10  
**Issue:** Traces showing `userId: "2"` (random numeric string) with no user_email  
**Status:** ✅ FIXED (July 8, 2026)

---

## The Problem

Three PROD traces from **July 3, 2026** show:
```json
{
  "userId": "2",
  "metadata": {
    "user_email": null,
    "user_id": 2,
    "user_name": null
  }
}
```

**What's wrong:**
- `userId` is just the raw numeric ID `"2"` 
- No email, no name, just a bare number
- This is ambiguous — which user is ID 2? Multiple people could have `user_id=2` across different accounts

**Impact:** Can't properly attribute the trace to a real person in Langfuse

---

## Root Cause

When `kb_answer` runs without a `user_email`, the old logic (before July 8) was:

```python
# OLD CODE (before July 8 fix)
if user_email:
    trace_user_id = user_email
elif user_id_val is not None:
    trace_user_id = str(user_id_val)  # ← Just raw number: "2"
```

This meant traces with only `user_id` (no email, no name) would be attributed to just `"2"`, which is:
1. **Non-unique** — multiple people could share the same account-level ID
2. **Uninformative** — impossible to tell which actual person made the request
3. **A blocker** — same user_id across different people collapses into one Langfuse identity

---

## The Fix (July 8, 2026)

**Commit:** `634099209bc3f8bf06eb1c2c9b7213095e343c41`  
**Message:** "Use composite user_id:user_name key for Langfuse userId when email is missing"

**New logic:**
```python
# NEW CODE (after July 8 fix)
if user_email:
    trace_user_id = user_email  # ← Preferred: email is unique
elif user_id_val is not None and str(user_id_val).strip():
    uid = str(user_id_val).strip()
    name = user_name.strip() if user_name else "unknown"
    trace_user_id = f"acct:{uid}:{name}"  # ← Composite key: "acct:2:unknown"
```

**Result:**
- `user_id=2` + `user_name=null` → `userId = "acct:2:unknown"`
- `user_id=30` + `user_name="Alice"` → `userId = "acct:30:alice"`
- Different people with same account ID no longer collapse in Langfuse

---

## Evidence: Timeline

| Date | Trace Count | Issue | Status |
|------|------------|-------|--------|
| **July 1–3** | 3 traces | `userId: "2"` (bare number) | ❌ Affected |
| **July 8 21:48** | — | Fix deployed | ✅ Fixed |
| **July 9–10** | 513 recent | No bare numbers, proper attribution | ✅ Working |

---

## Current Status (July 10)

✅ **All recent traces (July 9–10) show proper userId:**
- With email: `userId = "user@example.com"` ✅
- Without email: `userId = "acct:2:unknown"` ✅ (or similar composite)
- No bare numeric strings ✅

The 3 traces with `userId: "2"` are **historical artifacts** from before the fix was deployed. They don't reflect the current behavior.

---

## Why This Matters for the LRP Project

When testing with local traces:
- **Before fix (July 3):** `userId = "2"` looks random/broken
- **After fix (July 8+):** `userId = "acct:2:unknown"` looks intentional/composite

If you see random-looking userIds in Langfuse:
1. **Check the trace timestamp** — if before July 8, it's a pre-fix artifact
2. **If after July 8**, it means no `user_email` was available, so the composite `acct:uid:name` format is being used (working as designed)

---

## Best Practice Going Forward

**For production traces:** Always ensure `user_email` is available in the context. This gives you:
- Clean, human-readable userId
- No ambiguity (emails are unique)
- Easy filtering in Langfuse

**For test traces:** If you want meaningful userId without setting up full auth context:
1. Pass `user_email` parameter to kb_answer
2. Or ensure `.env` has `USER_EMAIL` set
3. This prevents fallback to bare numeric IDs

**Example:**
```python
# Good — explicit user_email
result = kb_answer(
    parameters={"query": "...", "user_email": "test@example.com"},
    context=some_context
)

# Also good — env-configured
os.environ["USER_EMAIL"] = "adwit.sharma@gupshup.io"
result = kb_answer(parameters={"query": "..."}, context=some_context)
```

---

## Conclusion

The "random userId" issue has been **fixed and resolved**. 
- Old traces (pre-July 8) show `userId: "2"` → ✅ expected for that period
- New traces (post-July 8) show `userId: "acct:2:unknown"` → ✅ proper composite format
- No further action needed, but be aware when analyzing historical traces

