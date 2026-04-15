source_url: https://console-docs.gupshup.io/docs/whatsapp-voice-call-logs-insights

<!-- kb-golden:v10 -->
# WhatsApp Voice — call logs (CDR), insights, and agent analytics

**Module**: Channels

## Definition
**CDR (Call Detail Records)** capture call metadata (duration, talk time, recordings where enabled). **Call Insights** and **Agent** analytics summarize performance, including **agent connectivity** for human agents. Source: **WA Voice Self Help** document (Demo Document for WA Voice, v1.1, revision 20-02-2026).

## Procedure
### Exact UI path
- **Call logs / CDR:** Open the **SR** or Console area where **inbound** (and related) **call logs** are listed (exact menu path depends on deployment and release).
- **Insights:** **Call Insights** (filters available).
- **Agent analytics:** **Agent Call Insights** table (when human agents are configured to receive calls).

### Prerequisites
- WhatsApp Voice traffic and appropriate roles to view **CDR** / recordings.
- **Human agents** configured to receive calls if you need **Agent Call Insights** productivity views.

### Fields to configure
- No explicit fields were identified in the self-help source; use the filters and columns available in the current UI.

### Steps
1. Open **inbound** (or applicable) **call logs** / **CDR** for WhatsApp Voice.
2. Review **call duration**, **talk time**, and other columns shown for your release.
3. Where **recording** is enabled, **listen** or **download** recordings (for example caller vs **AI agent** or human agent, depending on handling).
4. Open **Call Insights**; use **filters** as supported.
5. For human-agent scenarios, open **Agent Call Insights** (or equivalent) to review **productivity** and performance tables.

### Validation / where to check
- After a test call, confirm a **CDR** row appears and metrics look correct.
- Confirm **recordings** play or download when your account has recording enabled.

### Troubleshooting
- If logs are missing, confirm the call completed on the correct WABA / environment and that your user has access to the reporting area.
- If channel behavior is wrong, confirm the correct channel/app is connected and the latest configuration is live.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) in **Gupshup Console** when you change settings that affect logging or retention; viewing **CDR** / insights does not require **Save**.

### Setup path
- **Call logs (CDR)** → **Call Insights** → **Agent Call Insights** (as available in your build).

## Options / variants
- **Agent connectivity** in **Call Insights** refers to **human agent** connectivity when agents are in the loop (vs bot-only calls).

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Inbound flow: `kb/channels/whatsapp-voice-overview-and-inbound-calls.md`
- Outbound session and permissions: `kb/channels/whatsapp-voice-outbound-calls-session-and-permissions.md`
- SIP operations (recording, DTMF, FAQ): `kb/integrations/whatsapp-voice-sip-operations-faq.md`

## Module disambiguation docs
- **SR** reporting for WhatsApp Voice is separate from **Bot Studio** analytics unless your deployment links them; use the reporting module your project uses for voice CDR.

## Reference (from source)
<!-- procedural:v2 -->
# WhatsApp Voice — call logs (CDR), insights, and agent analytics

**Module**: Channels

## Overview
**Inbound logs** show **CDR** with duration, recordings, talk time, etc. **Call Insights** includes filtering; **agent connectivity** means human agent connectivity when agents participate. **Agent analytics** includes productivity under **Agent Call Insights** when human agents receive calls.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
**CDR:** View inbound (and related) logs; access **recordings** to listen and download.

**Insights:** Use **Call Insights** and filters.

**Agent analytics:** Review productivity and performance in **Agent Call Insights** when human agents are configured for calls.

## Demo and training videos (titles from self-help)
- **WhatsApp Calls over SR**
- **Customer View of WhatsApp Voice — Business Calls**
