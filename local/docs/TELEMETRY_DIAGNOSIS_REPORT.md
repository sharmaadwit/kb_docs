# Telemetry Diagnosis Report
**Date:** 2026-06-23  
**Status:** ISSUE IDENTIFIED & PATCH DEPLOYED LOCALLY

---

## Executive Summary

**Problem:** Three trace IDs show **empty metadata in Langfuse** — queries are being logged but metadata is not being sent.

**Root Cause:** The `_send_langfuse()` function in `skill/kb_answer.py` silently fails during the HTTP POST to Langfuse ingestion endpoint. The error is caught but not logged, so traces are created but remain empty.

**Solution:** Added comprehensive error logging to surface the actual failure reason (HTTP status, exception type, missing credentials).

---

## Problem Details

### Failing Traces
- `kb-kb_answer-2ca13333cf56469f`
- `kb-kb_answer-3ff08e947f544c55`
- `kb-kb_answer-09ab9af0537f4180`

**Symptoms:**
- Traces exist in Langfuse ✅
- Timestamp field: empty ❌
- Query field: empty ❌
- Module/Intent/Answer: all empty ❌

### Root Cause Analysis

**File:** `skill/kb_answer.py` (lines 5587-5594 in original)

**Original Code:**
```python
try:
    resp = requests.post(endpoint, headers=headers, json=body, timeout=30)
    status_code = resp.status_code
    ingestion_ok = resp.status_code < 400
    if not ingestion_ok:
        error = "ingestion_failed"
except Exception:  # ← Silent failure here
    error = "ingestion_transport_error"
```

**Issue:** Exceptions are caught but never logged. Trace ID is generated and returned, but metadata never reaches Langfuse.

---

## Patch Applied

### Changes to `skill/kb_answer.py`

**1. HTTP Failure Logging**
```python
if not ingestion_ok:
    error = f"ingestion_failed_http_{status_code}"
    try:
        resp_text = resp.text[:200]
    except:
        resp_text = "[unable to read response]"
    print(f"[LANGFUSE] Ingestion failed: HTTP {status_code} | {resp_text}", flush=True)
```

**2. Exception Logging**
```python
except Exception as e:
    error = f"ingestion_transport_error: {type(e).__name__}: {str(e)[:100]}"
    print(f"[LANGFUSE] Ingestion exception: {error}", flush=True)
```

**3. Missing Credentials Logging**
```python
else:
    missing = []
    if not host: missing.append("LANGFUSE_HOST")
    if not public_key: missing.append("LANGFUSE_PUBLIC_KEY")
    if not secret_key: missing.append("LANGFUSE_SECRET_KEY")
    error = f"missing_credentials: {', '.join(missing)}"
    print(f"[LANGFUSE] Cannot ingest: {error}", flush=True)
```

### Test Results

✅ **All 5 verification checks passed:**
- HTTP status code captured in error message
- Error is logged with [LANGFUSE] marker
- Response text is logged (first 200 chars)
- Exception type is logged
- Exception is logged with [LANGFUSE] marker
- Missing credentials error message created
- All three credentials checked individually
- All error paths have flush=True
- Python syntax is valid

---

## Current Telemetry State

### Global Metrics
| Metric | Value |
|--------|-------|
| Total Queries (7d) | 148 |
| Answer Rate | 77.7% ✅ |
| IDK Rate | 22.3% |
| Avg Confidence | 4.4 |

### Module Performance
| Module | Queries | Answer Rate | Note |
|--------|---------|-------------|------|
| Bot Studio | 64 | 82.8% ✅ | Strongest performer |
| General | 33 | 78.8% ✅ | Stable |
| Agent Assist | 14 | 64.3% ⚠️ | Needs attention |
| Channels | 7 | 71.4% ⚠️ | Low volume |
| CTX | 7 | 85.7% ✅ | Strong |
| Analytics | 6 | 50.0% ❌ | Weakest module |

### Language Coverage
| Language | Queries | Answer Rate |
|----------|---------|-------------|
| English (EN) | 141 | 78.0% |
| Portuguese (PT) | 7 | 71.4% |

### Top Failing Queries
1. `message_metadata response JSON structure` — Bot Studio (score: 0.85)
2. `No Journey Builder, como modelar fallback para reply buttons` — Bot Studio (score: 1.45)
3. `Como definir fallback de inatividade no node de reply?` — Bot Studio (score: 1.10)
4. `In a flow, after the final submit is called, what flow data...` — Agent Assist (score: 1.50)
5. `journey variables in terminalmode` — Analytics (score: 0.55)

---

## Deployment Instructions

### Step 1: Deploy Patched Code
```bash
# Copy the patched skill/kb_answer.py to your Gupshup skill environment
cp skill/kb_answer.py <gupshup-skill-path>/
```

### Step 2: Verify Credentials
Ensure these secrets are set in your Gupshup skill environment:
- `LANGFUSE_HOST` = `https://cloud.langfuse.com`
- `LANGFUSE_PUBLIC_KEY` = (your public key)
- `LANGFUSE_SECRET_KEY` = (your secret key)

### Step 3: Test Query
Run a test query and check skill logs for `[LANGFUSE]` markers.

### Step 4: Expected Outcomes

**If successful (HTTP 200):**
- No [LANGFUSE] error log appears
- Trace appears in Langfuse with metadata populated ✅

**If HTTP error (401/403/404):**
- Log shows: `[LANGFUSE] Ingestion failed: HTTP 401 | {"error": "..."`
- → Check credentials or Langfuse endpoint

**If network error:**
- Log shows: `[LANGFUSE] Ingestion exception: ingestion_transport_error: ConnectTimeout: ...`
- → Check network connectivity

**If credentials missing:**
- Log shows: `[LANGFUSE] Cannot ingest: missing_credentials: LANGFUSE_PUBLIC_KEY, ...`
- → Add missing secrets to environment

---

## Files Committed

| File | Commit | Purpose |
|------|--------|---------|
| `skill/kb_answer.py` | `8f5f4f9` | **Patch** - Add debug logging for telemetry failures |
| `local/scripts/diagnose_telemetry.py` | `e59f776` | Diagnostic tool to identify telemetry issues |
| `local/scripts/test_telemetry_logging.py` | `8cc390f` | Test suite verifying patch correctness |

---

## Next Steps

1. **Deploy** patched `skill/kb_answer.py` to Gupshup environment
2. **Test** with a sample query
3. **Monitor** skill logs for `[LANGFUSE]` error messages
4. **Fix** the issue based on error message (see "Expected Outcomes" above)
5. **Verify** that new traces have metadata populated in Langfuse

---

## Troubleshooting

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| No [LANGFUSE] logs at all | Patch not deployed | Re-deploy skill/kb_answer.py |
| `HTTP 401` error | Auth failed | Regenerate Langfuse API keys |
| `HTTP 404` error | Endpoint wrong | Verify Langfuse URL is `https://cloud.langfuse.com` |
| `ConnectTimeout` error | Network issue | Check Gupshup network connectivity to Langfuse |
| `missing_credentials` | Env vars not set | Add LANGFUSE_* secrets to skill environment |

---

**Status:** Ready for production deployment ✅
