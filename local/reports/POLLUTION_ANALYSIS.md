# User Email Pollution Analysis

## Timeline

- **2026-07-02 14:06:59**: Commit `667912ea` — Added TRACE_ENV detection for local-analysis environment
- **2026-07-03 16:23:16**: Commit `3141e118` — **BUG INTRODUCED**: Set `user_email` default to `adwit.sharma@gupshup.io` globally (no environment check)
  - This affected ALL production traces where user_email was not explicitly passed
  - Duration: ~2 hours before fix
- **2026-07-03 18:20:20**: Commit `56dc9179` — Other fixes (unrelated)
- **2026-07-03 18:32:43**: Commit `76050a16` — **BUG PARTIALLY FIXED**: Removed hardcoded default entirely
- **Latest**: Commit `d6ea6ec4` — **PROPERLY SCOPED**: Default now only applies to `trace_env=local-analysis`

## Polluted Data Window

**2026-07-03 16:23 to 2026-07-03 18:32 (~2 hours)**

All traces in this window with `user_email = adwit.sharma@gupshup.io` that were NOT your intentional tests are polluted.

## How to Identify Actual Users

Since Langfuse API is unreliable, the actual user identifiers are likely in these metadata fields:

```
- userId (Langfuse user ID)
- sessionId (conversation session)
- externalId (external reference)
- trace_id (unique trace identifier)
- input.query (the actual question — may hint at user type)
```

## Query to Langfuse

To extract the polluted traces manually:

```bash
# Via Langfuse API with timestamp range
GET /api/public/traces?fromTimestamp=2026-07-03T16:23:00Z&toTimestamp=2026-07-03T18:32:00Z
```

Filter the response for:
```json
{
  "metadata": {
    "user_email": "adwit.sharma@gupshup.io"
  }
}
```

Then examine each trace's:
- `userId` (internal Langfuse user ID)
- `sessionId` (could be session UUID from calling API)
- `externalId` (external system reference)
- `input.query` (content may reveal actual user intent/domain)

## Recommended Actions

1. **Export polluted traces** from Langfuse Traces UI (filter by timestamp 2026-07-03 16:23–18:32, user_email = adwit.sharma@gupshup.io)
2. **Inspect sessionId/userId/externalId** fields for actual user attribution
3. **Backfill user_email** in Langfuse or analytics if you have a mapping (external API calls should embed the real email)
4. **Filter from reports** until corrected (current dashboard filters `adwit.sharma@gupshup.io` from leads anyway)

## Current Status

✅ **Fixed**: All new traces from 2026-07-03 18:32 onwards have correct user_email attribution
⚠️ **Polluted window**: ~2-hour window on 2026-07-03 16:23–18:32 needs manual cleanup
✅ **Scoped correctly**: Future local testing via Claude will use `trace_env=local-analysis` to avoid pollution
