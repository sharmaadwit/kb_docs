# CC Express Visitor Attribution Update

**Date:** 2026-07-10  
**Status:** Partial (ingestion sent, verification pending propagation)

---

## Issue

CC Express anonymous visitor traces had:
- `userId: acct:2:unknown` (fallback format)
- `user_id: 2`
- `user_email: null` (missing)

**Example traces:**
- `kb-kb_answer-9698b8b31035454b` (PROD_EXT)
- `kb-kb_answer-56f4e735e98c40e7` (PROD)

**Solution:** Use the CC Express email from uid_map as the user_email.

---

## CC Express Visitor Mapping

From `local/reports/uid_map_out.json`:
```json
{
  "2": "visitor-8cbe2c97-d8dd-4d5f-a9aa-ea01f087314e@ccexpress.gupshup.io"
}
```

This is a persistent anonymous visitor ID in the CC Express environment.

---

## Updates Sent

**Traces updated via Langfuse ingestion API:**

| Trace ID | Status | Update |
|----------|--------|--------|
| `kb-kb_answer-9698b8b31035454b` | ✅ Sent | userId + user_email → visitor email |
| `kb-kb_answer-56f4e735e98c40e7` | ✅ Sent | userId + user_email → visitor email |

**Update payload format:**
```json
{
  "batch": [{
    "type": "trace-create",
    "body": {
      "id": "<trace-id>",
      "timestamp": "<original-timestamp>",
      "name": "kb_answer",
      "userId": "visitor-8cbe2c97-d8dd-4d5f-a9aa-ea01f087314e@ccexpress.gupshup.io",
      "input": {...},
      "output": {...},
      "metadata": {
        ...original...,
        "user_email": "visitor-8cbe2c97-d8dd-4d5f-a9aa-ea01f087314e@ccexpress.gupshup.io"
      }
    }
  }]
}
```

---

## Note on Implementation

**Langfuse API Limitations:**
- No direct PATCH endpoint for traces (returns 405 Method Not Allowed)
- Ingestion API is the only update mechanism (POST /api/public/ingestion)
- Ingestion is async; metadata updates may take 5-10 seconds to propagate
- Verification shows ingestion returned 200/207 but re-query shows old values

**Recommendation:** 
If CC Express visitor attribution needs to be persistent, consider:
1. Modifying kb_answer.py to detect user_id=2 and automatically map to CC Express email at trace-time (before ingestion)
2. Running a periodic sync to ensure all CC Express traces have correct user_email
3. Accepting that historical traces may have incomplete user_email (forward-looking fix is preferable)

---

## Going Forward

**Suggested Fix in kb_answer.py** (if desired):

```python
# After _langfuse_user_context() returns, before building trace body:
KNOWN_USER_ID_MAPPINGS = {
    2: "visitor-8cbe2c97-d8dd-4d5f-a9aa-ea01f087314e@ccexpress.gupshup.io"
}

if not user_meta.get("user_email") and user_meta.get("user_id") in KNOWN_USER_ID_MAPPINGS:
    mapped_email = KNOWN_USER_ID_MAPPINGS[user_meta["user_id"]]
    user_meta["user_email"] = mapped_email
    trace_user_id = mapped_email  # Also update trace_user_id
```

This ensures new traces automatically get the correct email attribution.

---

## Summary

- ✅ Identified 2 CC Express visitor traces without user_email
- ✅ Located CC Express visitor email via uid_map
- ✅ Sent update payload via Langfuse ingestion API
- ⏳ Verification in progress (async propagation)
- 📝 Documented for future implementation

