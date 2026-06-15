# Langfuse Channel Instrumentation Fix — Completed

**Date:** 2026-06-11  
**Component:** skill/kb_answer.py  
**Change:** 1-line fix to ensure all traces include channel_type metadata

---

## What Was Fixed

### Problem
- 197 KB queries appeared as **"untagged"** in Langfuse analytics dashboard
- Could not distinguish WhatsApp (primary) from RCS (emerging) performance
- Early-exit code paths (guardrail, undocumented, rate_gap, etc.) had `channel_type = null`

### Root Cause
Line 5119 in `_send_langfuse()`:
```python
# OLD: Conditionally returns None
"channel_type": _detect_channel_type(top_source) if top_source else None,
```

When `top_source` was None (early exits with empty results), `channel_type` became `None` instead of the proper default.

### Solution
Changed to always call `_detect_channel_type()`:
```python
# NEW: Always calls detection, falls back to "whatsapp" for empty results
"channel_type": _detect_channel_type(top_source or ""),
```

---

## How It Works

### Detection Logic
The `_detect_channel_type()` function (line 2714) evaluates KB source paths:

| Source Path | Returns | Example |
|---|---|---|
| `kb/channels/rcs-*.md` | `"rcs"` | `kb/channels/rcs-authentication.md` |
| `kb/channels/*whatsapp*` | `"whatsapp"` | `kb/channels/whatsapp-flows.md` |
| `kb/channels/*instagram*` | `"instagram"` | `kb/channels/instagram-catalog.md` |
| `kb/channels/*web*` | `"web"` | `kb/channels/web-widget.md` |
| Other `kb/channels/*` | `"channels_other"` | `kb/channels/channel-types.md` |
| All other sources | `"whatsapp"` | `kb/bot-studio/journeys.md`, `""` (early exits) |

### Call Flow
```
Query arrives
  ↓
Early exit check (guardrail, undocumented, etc.)
  └→ _send_langfuse(..., results=[])
       └→ top_source = None
            └→ _detect_channel_type(None or "") 
                 └→ Returns "whatsapp" ✓
  ↓
Main KB flow
  └→ _send_langfuse(..., results=[{source, score}, ...])
       └→ top_source = results[0].source
            └→ _detect_channel_type("kb/channels/rcs-*.md")
                 └→ Returns "rcs" ✓
```

---

## Verification

### Test Cases (All Passing ✓)
```
✓ kb/channels/rcs-authentication.md    → "rcs"
✓ kb/channels/whatsapp-flows.md        → "whatsapp"
✓ kb/bot-studio/journeys.md            → "whatsapp"
✓ "" (empty, early-exit paths)         → "whatsapp"
✓ kb/channels/instagram-catalog.md     → "instagram"
✓ kb/channels/web-widget.md            → "web"
```

### Expected Langfuse Impact
Every trace now includes metadata like:
```json
{
  "metadata": {
    "channel_type": "rcs",  // or "whatsapp", "instagram", etc.
    "top_source": "kb/channels/rcs-authentication.md",
    "module_label": "Channels",
    "confidence": 5.2,
    "answered": true,
    // ... other fields ...
  }
}
```

---

## Dashboard Changes (After Regeneration)

### Before
```
untagged: 197 queries  ← Confusing (what does "untagged" mean?)
rcs:        3 queries
```

### After
```
whatsapp:  197 queries  ← Clear: primary channel for untagged Bot Studio/Agent Assist queries
rcs:         3 queries  ← Clear: emerging channel coverage
instagram:   0 queries  ← Clear: not yet used
web:         0 queries  ← Clear: not yet used
```

---

## Files Changed

| File | Lines | Change |
|---|---|---|
| `skill/kb_answer.py` | 5119 | 1-line fix to channel_type metadata |

**Commit:** `0c4d6bc`

---

## Next Steps for Analytics Team

1. **Verify in production** (after deployment):
   ```bash
   # Check that NO traces have channel_type = null
   lf traces list --name kb_answer --limit 100 | \
     jq '.[] | select(.metadata.channel_type == null) | length'
   
   # Expected result: 0
   ```

2. **Regenerate dashboard** with proper channel breakdown:
   - Filter by `channel_type` to show WhatsApp vs RCS metrics
   - Compare performance across channels
   - Monitor RCS adoption

3. **Set up channel-specific alerts** (optional):
   - RCS answer rate dropping below threshold
   - WhatsApp video engagement trends
   - New channel adoption (Instagram, Web, SMS)

---

## Impact Summary

✅ **No user-facing changes** — Purely analytics instrumentation  
✅ **Backward compatible** — Existing queries work exactly as before  
✅ **Low risk** — Only affects Langfuse metadata, not answer logic  
✅ **High value** — Unlocks multi-channel analytics and reporting  

**Key metric:** 0 null channel_type values in all future traces
