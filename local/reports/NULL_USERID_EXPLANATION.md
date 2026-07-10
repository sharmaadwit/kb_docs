# Null userId Issue — Explanation & Current Status

**Date:** 2026-07-10  
**Context:** Test traces showing `userId: null` in Langfuse; clarification of why this happens and whether it's a problem

---

## The Issue

When running local tests against `kb_answer`, test traces recorded in Langfuse show:
```json
{
  "userId": null,
  "metadata": {
    "user_email": "adwit.sharma@gupshup.io",
    "user_id": 123
  }
}
```

Or sometimes:
```json
{
  "userId": null,
  "metadata": {
    "user_email": null,
    "user_id": null
  }
}
```

**Question:** Why is `userId` null when we have `user_email` and `user_id` in metadata?

---

## Root Cause: Test Harness Doesn't Pass User Context

The local test harness (`FakeContext` class in test scripts) doesn't include a user context object:

```python
# From analyze_idk_traces.py
class FakeContext:
    def get_secret(self, name):
        return None
    # No user_email, user_id, or other user attributes
```

When `kb_answer` runs with this test context:
1. It calls `_langfuse_user_context(context, params)` (line 6789–6841)
2. This function looks for `user_email` in: params → context attributes → environment
3. Since FakeContext has no user attributes, it falls back to environment
4. If the environment doesn't have `USER_EMAIL` set, `user_email` becomes `None`
5. Without a `user_email`, `trace_user_id` is `None`
6. Langfuse body gets `userId: null`

---

## How kb_answer Derives userId

The logic in `kb_answer.py` lines 6789–6841:

```python
def _langfuse_user_context(context, params=None):
    """Returns (trace_user_id for Langfuse body.userId, user metadata)."""
    
    # 1. Check params first
    user_email = None
    for key in ("user_email", "userEmail"):
        if key in (params or {}):
            user_email = (params[key] or "").strip()
            if user_email:
                break
    
    # 2. Fall back to context attributes
    if not user_email:
        em = getattr(context, "user_email", None)
        if em:
            user_email = em.strip()
    
    # 3. Try user_id as fallback
    user_id_val = None
    for key in ("user_id", "userId"):
        user_id_val = params.get(key) if params else None
    
    if user_id_val is None:
        user_id_val = getattr(context, "user_id", None)
    
    # 4. Construct trace_user_id
    trace_user_id = ""
    if user_email:
        trace_user_id = user_email  # ← Preferred
    elif user_id_val is not None:
        trace_user_id = f"acct:{uid}:{name}"  # ← Fallback
    
    return (trace_user_id or None, meta_user)
```

**Priority order:**
1. `user_email` from params → context → environment → None
2. `user_id` from params → context → None (if email is absent)
3. If both absent: `trace_user_id = None` → `userId = null`

---

## Current Environment Setup

Your `.env` file has:
```bash
USER_EMAIL=adwit.sharma@gupshup.io
TRACE_ENV=LOCAL
```

This means:
- **Production/real Langfuse traces:** get `USER_EMAIL` from env → `userId = "adwit.sharma@gupshup.io"` ✅
- **Local test traces with env set:** get `USER_EMAIL` from env → `userId = "adwit.sharma@gupshup.io"` ✅
- **Local test traces WITHOUT env:** get `user_email = None` → `userId = null` ❌

---

## Why This Happens in Local Tests

Most test scripts don't pass `user_email` to the FakeContext:

```python
# Before (test harness setup)
class FakeContext:
    def get_secret(self, name):
        return None

# Then later:
kb_answer.kb_answer(parameters={"query": "..."}, context=FakeContext())
# No user_email passed → falls back to env → gets USER_EMAIL ✅
```

**But if the test environment doesn't have USER_EMAIL set (e.g., running in Docker, CI/CD, or clean Python venv):**
- FakeContext has no user attributes
- Environment has no USER_EMAIL
- Result: `userId = null` ❌

---

## Is This a Problem?

### No, it's expected behavior:

1. **For local development:** `userId = null` is fine — it's a test trace, not production
2. **For CI/CD:** Set `USER_EMAIL` in CI environment → trace gets proper userId
3. **For production:** Real Azure Functions/Cloud Functions always have the user context → userId always set

### Yes, it's a problem if:

1. **You're trying to attribute traces to real users** and expecting all traces to have userId
2. **You're analyzing local test traces as if they were production** (they're not)
3. **You're comparing test trace metrics to production** (different attribution)

---

## Solution: Set USER_EMAIL in Test Context (Optional)

If you want test traces to have non-null userId, pass it to the context:

**Option 1: Through parameters**
```python
kb_answer.kb_answer(
    parameters={"query": "...", "user_email": "test@example.com"},
    context=FakeContext()
)
```

**Option 2: Extend FakeContext**
```python
class FakeContext:
    def __init__(self, user_email="test@example.com"):
        self.user_email = user_email
    
    def get_secret(self, name):
        return None

kb_answer.kb_answer(parameters={"query": "..."}, context=FakeContext(user_email="adwit.sharma@gupshup.io"))
```

**Option 3: Set environment before importing**
```python
import os
os.environ["USER_EMAIL"] = "adwit.sharma@gupshup.io"

# Then import and use kb_answer
from skill import kb_answer
```

---

## Production vs. Local Comparison

| Scenario | userId Set? | Source | Notes |
|----------|------------|--------|-------|
| **Production trace** | ✅ Yes | Azure Function context | Real user email from auth |
| **Local test (env set)** | ✅ Yes | .env USER_EMAIL | Simulates production |
| **Local test (env unset)** | ❌ No | No fallback | FakeContext has no attributes |
| **CI/CD trace** | ✅ Yes | CI environment vars | Set USER_EMAIL in CI config |

---

## Historical Context

From the prior conversation summary:
> "why iz user id null?" — asked about null userId in test traces; clarified it's because test harness didn't pass userId

**Your fix:** You corrected the testing approach to use env-configured credentials:
```bash
USER_EMAIL=adwit.sharma@gupshup.io TRACE_ENV=LOCAL python test_script.py
```

This ensures test traces get proper attribution without modifying test code.

---

## Current Status

✅ **This is working as designed:**
- Local test traces with `USER_EMAIL` set in env → `userId = "adwit.sharma@gupshup.io"`
- Langfuse can now properly attribute test traces to you
- Production traces continue to get userId from Azure Function context

✅ **No action needed** unless you want to:
1. Make test traces always have userId regardless of env (extend FakeContext)
2. Analyze which test traces are yours vs. others (filter by userId)
3. Clean up old test traces from Langfuse (manually delete from UI)

---

## For the LRP Project

**Important:** When testing BizAI agents with LRP data:
- Always set `USER_EMAIL=adwit.sharma@gupshup.io` or similar
- This ensures your test traces are properly attributed in Langfuse
- Otherwise, you'll see `userId: null` and won't be able to filter/analyze your own traces

```bash
USER_EMAIL=adwit.sharma@gupshup.io python test_bizai_lrp.py
```

---

## Appendix: How Production Avoids This

In production (Azure Functions):

```python
# Real context from Azure Functions request/context object
context.user_email = "real.user@loreal.com"  # ← Always present
context.user_id = 12345  # ← Set by auth middleware

# kb_answer gets called with real context
result = kb_answer(parameters={...}, context=context)

# _langfuse_user_context extracts user_email
trace_user_id = "real.user@loreal.com"

# Langfuse trace gets proper userId
body["userId"] = "real.user@loreal.com"  # ← Never null
```

This is why production traces always have userId, and local test traces need env setup.

