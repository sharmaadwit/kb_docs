# Critical Credential Mismatch Fix

**Issue Date:** 2026-06-23  
**Severity:** 🔴 **CRITICAL** — Telemetry disabled due to environment variable mismatch

---

## Problem Summary

The skill code and `.env` file are using **different environment variable names** for Langfuse host:

**In `.env` (line 10):**
```
LANGFUSE_BASE_URL="https://cloud.langfuse.com"
```

**In `skill/kb_answer.py` (line 5571):**
```python
host = context.get_secret("LANGFUSE_HOST")
```

**Result:** Host is never found → telemetry is never sent → traces remain empty in Langfuse

---

## Why This Breaks Telemetry

```python
# skill/kb_answer.py line 5578
if host and public_key and secret_key:  # ← host is None, so this fails
    # ... telemetry code never runs ...
else:
    error = "missing_credentials: LANGFUSE_HOST"  # ← This is what happens
    print(f"[LANGFUSE] Cannot ingest: {error}", flush=True)
```

This is why we saw:
- ❌ Empty traces in Langfuse (metadata never sent)
- ❌ No error logs (code path never reached)
- ❌ 3 failing trace IDs with no data

---

## Solution

### Option A: Fix `.env` (Recommended)

Change line 10 in `.env`:
```diff
- LANGFUSE_BASE_URL="https://cloud.langfuse.com"
+ LANGFUSE_HOST="https://cloud.langfuse.com"
```

### Option B: Fix `skill/kb_answer.py`

Change line 5571 in `skill/kb_answer.py`:
```diff
- host = context.get_secret("LANGFUSE_HOST")
+ host = context.get_secret("LANGFUSE_BASE_URL")
```

**Recommendation:** Use Option A (fix `.env`) because:
- `.env` is already in place
- Only need to change one file
- Matches standard Langfuse config naming

---

## Additional Security Issue

Your `.env` file also contains a **real GitHub PAT token** (line 17):
```
GITHUB_TOKEN=***REMOVED-GITHUB-PAT***
```

### ⚠️ Security Actions Required

1. **Immediately rotate** this PAT token on GitHub
2. **Never commit `.env`** to git (it's in `.gitignore` but this token may be in git history)
3. **Revoke** the exposed token here: https://github.com/settings/tokens

To rotate:
1. Go to https://github.com/settings/tokens
2. Find the token starting with `github_pat_11AEBWENY0GPh1...`
3. Click "Delete"
4. Generate a new token
5. Update your `.env` file

---

## Implementation Steps

### Step 1: Fix Langfuse Host Variable
```bash
# Edit .env and change LANGFUSE_BASE_URL to LANGFUSE_HOST
sed -i 's/LANGFUSE_BASE_URL=/LANGFUSE_HOST=/' .env
```

Or manually edit line 10:
```
LANGFUSE_HOST="https://cloud.langfuse.com"
```

### Step 2: Rotate GitHub PAT
1. Go to https://github.com/settings/tokens
2. Delete the old token
3. Create a new personal access token
4. Update `.env` with new token

### Step 3: Test Telemetry
```bash
# Run a test query in your skill
# Check logs for [LANGFUSE] markers
# Verify traces appear with metadata in Langfuse
```

### Step 4: Verify Fix
```bash
python3 local/scripts/diagnose_telemetry.py
# Should now show:
# ✅ Credentials present
# ✅ Recent traces found
# ✅ Traces have metadata
```

---

## Why This Wasn't Caught Earlier

1. The mismatch was silent (no error message without the patch)
2. Traces were still created (but empty)
3. The patch now logs `[LANGFUSE] Cannot ingest: missing_credentials: LANGFUSE_HOST`

---

## Impact

**Before fix:**
- ❌ All telemetry silently dropped
- ❌ Traces empty in Langfuse
- ❌ Dashboard only shows old/cached data
- ❌ No way to debug without logs

**After fix:**
- ✅ All telemetry successfully ingested
- ✅ Traces populated with complete metadata
- ✅ Dashboard shows live data
- ✅ Error logs guide debugging if issues occur

---

## Files Affected

| File | Change | Impact |
|------|--------|--------|
| `.env` | `LANGFUSE_BASE_URL` → `LANGFUSE_HOST` | **Critical** — unblocks telemetry |
| `GitHub PAT` | Rotate immediately | **Security** — prevent unauthorized access |

---

## Rollout Checklist

- [ ] Fix `.env`: Change `LANGFUSE_BASE_URL` to `LANGFUSE_HOST`
- [ ] Rotate GitHub PAT token (high priority)
- [ ] Update skill environment with new PAT
- [ ] Run test query
- [ ] Check skill logs for `[LANGFUSE]` (should be none if successful)
- [ ] Verify traces in Langfuse have metadata
- [ ] Re-run diagnostic: `python3 local/scripts/diagnose_telemetry.py`

---

**Status:** Ready to fix — This is the root cause of empty traces  
**Priority:** 🔴 CRITICAL — Deploy immediately after rotating GitHub PAT
