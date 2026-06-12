# Bug Fix: NDJSON Video Events Not Loading

**Date:** 2026-06-12  
**Status:** FIXED

## The Bug

When loading video delivery events from NDJSON files, scripts were looking for `event.get("timestamp")` instead of `event.get("ts")`.

**Impact:** 3-day dashboard showed 0 video events when 88 were actually present.

### Root Cause

NDJSON video event format uses `"ts"` field:
```json
{"ts": "2026-06-11T06:07:22.694481+00:00", "event": "video.delivered", "payload": {...}}
```

But the dashboard script was checking for `"timestamp"`:
```python
ts_str = event.get("timestamp")  # ❌ Wrong - always returns None
```

## The Fix

1. **3-day dashboard script:** Changed `event.get("timestamp")` → `event.get("ts")`
2. **Added helper function:** `load_ndjson_since()` in `analytics_common.py` to provide a standard, correct way to load filtered NDJSON

## Prevention

Future scripts should use the standard helper:

```python
from analytics_common import load_ndjson_since
from datetime import datetime, timedelta, timezone

cutoff = datetime.now(timezone.utc) - timedelta(days=3)
events = load_ndjson_since(cutoff)  # Correctly handles 'ts' field
```

**NOT:**
```python
# ❌ Wrong - will miss all video events
for line in f:
    event = json.loads(line)
    ts = event.get("timestamp")  # This is always None for NDJSON
```

## Files Changed

- `local/scripts/analytics_common.py` — Added `load_ndjson_since()` helper (line ~202)
- `local/reports/3day_dashboard.html` — Regenerated with 88 video events
- `local/reports/3day_analytics.json` — Regenerated with video event count

## Test

Verify the fix:
```bash
python3 -c "
from local.scripts.analytics_common import load_ndjson_since
from datetime import datetime, timedelta, timezone
cutoff = datetime.now(timezone.utc) - timedelta(days=3)
events = load_ndjson_since(cutoff)
print(f'Video events in last 3 days: {len(events)}')  # Should be ~88
"
```

---

**Lesson:** Always verify field names when parsing external data formats. NDJSON fields are not always obvious.
