# userId Bug Fix — USER_EMAIL Override Issue

**Date:** 2026-07-10  
**Issue:** USER_EMAIL env var was overriding actual user context in production traces  
**Status:** ✅ FIXED

---

## The Bug

**Symptom:**
```json
Trace: kb-kb_answer-88ee9717cdde49f5 (July 8, 2026)
{
  "userId": "adwit.sharma@gupshup.io",           ❌ WRONG (env override)
  "metadata": {
    "user_email": "harishmanekscorpion@gmail.com"  ← Correct user
  }
}
```

**Root Cause:**
In `kb_answer()` main entry (lines 7099-7103), the code was:

```python
# OLD CODE (BUGGY)
if not params.get("user_email"):
    env_email = os.getenv("USER_EMAIL")
    if env_email:
        params["user_email"] = env_email
```

**Problem:**
- When kb_answer is called from production (SuperAgent, Azure Functions), the `context` object has `user_email`
- But this code only checks `params.get("user_email")`, not whether `context.user_email` exists
- Result: If params lack user_email, it gets filled from env, overriding the real user context

**Scenario that triggers the bug:**
1. Production call: `kb_answer(params={}, context=UserContext(user_email="harish@example.com"))`
2. Code path: `if not params.get("user_email"):` → TRUE (params empty)
3. Fallback: Sets `params["user_email"] = "adwit.sharma@gupshup.io"` (env default)
4. Result: Real user's email is ignored, trace gets your env email instead ❌

---

## The Fix

**File:** `skill/kb_answer.py` lines 7098-7110

**NEW CODE (FIXED):**
```python
# Default user_email from USER_EMAIL env var ONLY if no user context is available.
# This env var is a fallback for local testing when no real user context exists.
# Do NOT override if context has user_email (production/external calls preserve actual user).
if not params.get("user_email"):
    # Only use env fallback if context doesn't provide user_email
    has_context_email = (context is not None and
                        hasattr(context, "user_email") and
                        context.user_email)
    if not has_context_email:
        import os
        env_email = os.getenv("USER_EMAIL")
        if env_email:
            params["user_email"] = env_email
```

**Key Change:**
- Added check: `has_context_email = (context is not None and hasattr(context, "user_email") and context.user_email)`
- Only apply env fallback if context doesn't have user_email
- Preserves production user context while keeping local test fallback

---

## Test Scenarios

### Scenario 1: Local Test (No Context) — Should use env
```python
# Before fix and after fix: Should use USER_EMAIL
result = kb_answer(
    parameters={"query": "..."},
    context=None  # No context
)
# Expected: userId = "adwit.sharma@gupshup.io" (from env) ✅
```

### Scenario 2: Production Call (Has Context) — Should preserve context user
```python
# Before fix: BROKEN ❌
class UserContext:
    user_email = "harish@example.com"

result = kb_answer(
    parameters={"query": "..."},
    context=UserContext()
)
# Before: userId = "adwit.sharma@gupshup.io" (env override) ❌
# After:  userId = "harish@example.com" (context preserved) ✅
```

### Scenario 3: Explicit Params Override — Should use params
```python
# Before and after fix: params should take precedence
result = kb_answer(
    parameters={"query": "...", "user_email": "user1@example.com"},
    context=UserContext(user_email="user2@example.com")
)
# Expected: userId = "user1@example.com" (params win) ✅
```

---

## Impact

**What this fixes:**
- ✅ Production traces from SuperAgent now get correct userId (actual user, not env override)
- ✅ Local tests still get env fallback when no context exists
- ✅ Explicit params still take precedence over context
- ✅ No breaking changes to existing behavior

**Affected traces:**
- Fixes: Any production trace that came from a system with its own context (SuperAgent, etc.)
- Unaffected: Local test traces (they still get env email correctly)

**Priority of user_email resolution (after fix):**
1. `params["user_email"]` (explicit, highest priority)
2. `context.user_email` (caller's context, production)
3. `os.getenv("USER_EMAIL")` (fallback, local testing only)

---

## Verification

The trace `kb-kb_answer-88ee9717cdde49f5` from July 8 would be fixed:
- **Before fix:** `userId = "adwit.sharma@gupshup.io"` (env override, WRONG)
- **After fix:** `userId = "harishmanekscorpion@gmail.com"` (context preserved, CORRECT)

---

## Code Review

**Lines changed:** 12 (added comments + conditional check)  
**Functions affected:** `kb_answer()` main entry  
**Functions NOT affected:** `_langfuse_user_context()` (receives corrected params)  
**Backward compatibility:** ✅ Full (local tests still work, production now correct)  

**Edge cases handled:**
- context is None → uses env ✅
- context exists but has no user_email → uses env ✅
- context.user_email is empty string → uses env ✅
- params have user_email → ignores env ✅
- context has user_email → ignores env ✅

