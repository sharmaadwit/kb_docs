# Channel Type: Historical Data Policy

**Decision:** Accept historical data as-is. Do not backfill.

**Date:** 2026-06-11

---

## The Situation

**Historical traces (196 queries):**
- Generated before channel_type instrumentation was complete
- Have `channel_type = null` in Langfuse
- Display as "untagged" in analytics dashboard

**New traces (from June 11 onwards):**
- Generated with proper channel_type detection
- Will have `channel_type = "whatsapp"` (default) or `"rcs"` (for RCS queries)
- Will display correctly in analytics dashboard

---

## Why Accept As-Is

1. **Data Integrity** - Historical traces accurately reflect what was recorded at the time
2. **Simplicity** - No complex backfill scripts or Langfuse API calls needed
3. **Honest Timeline** - Dashboard shows the evolution: "untagged" era → proper tagging era
4. **Low Risk** - No modifications to Langfuse data or skill code needed
5. **Clear Causality** - Users can see exactly when proper channel detection was deployed

---

## What This Means for Analytics

### Current Dashboard View

```
untagged: 196 queries  ← Pre-fix historical data (June 5-11)
rcs:        4 queries  ← Post-fix new queries (June 11+)
```

### Future Dashboard View (after more queries come in)

```
whatsapp: 196 + N queries  ← Historical "untagged" + new WhatsApp queries
rcs:      4 + M queries    ← RCS queries post-fix
```

The "untagged" label will disappear as new queries dominate the 200-trace rolling window.

---

## Implementation

**No code changes needed.**

The dashboard script already handles this correctly:
```python
channel = meta.get("channel_type") or "untagged"
```

This line will:
- Show "untagged" for historical traces with `channel_type = null`
- Show proper channel names for new traces with channel_type set
- Naturally transition as old data ages out of the 200-trace window

---

## Precedent

This is a standard practice in analytics:

- **Database migrations**: Accept old schema data as-is, fix going forward
- **Analytics tools**: Historical data shows what was recorded, future data shows what's now recorded
- **API versioning**: Old API versions produce old data shapes, new versions produce new shapes

The timeline is honest and useful information in itself.

---

## Related Decisions

- **Skill code**: All NEW traces must have proper channel_type (no null values)
- **Dashboard script**: Displays historical data truthfully (null → "untagged")
- **Analytics scope**: Accept boundaries; don't backfill historical Langfuse data

---

**Status:** ACCEPTED  
**Impact:** Low (purely a data interpretation decision)  
**Maintenance:** None (no code changes, no backfill needed)
