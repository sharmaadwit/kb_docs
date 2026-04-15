source_url: https://console-docs.gupshup.io/docs/whatsapp-voice-outbound-calls

<!-- kb-golden:v10 -->
# WhatsApp Voice — outbound calls, session, and permissions

**Module**: Channels

## Definition
**Outbound** WhatsApp Voice is when the **business** initiates a call to the customer on WhatsApp. The self-help flow assumes an **active messaging session** with the user before placing the outbound call, and **call permission** where the platform requires it. Source: **WA Voice Self Help** document (Demo Document for WA Voice, v1.1, revision 20-02-2026).

## Procedure
### Exact UI path
- **Customer:** WhatsApp client → send an **inbound message** to the business number to open or continue a session.
- **Agent:** **SR** → **Available** → **WhatsApp call widget** → **calling window** → dial / connect.

### Prerequisites
- **SR** credentials and agent **Available** status.
- Customer has a **valid active session** when your configuration requires it (for example after a recent inbound message).
- **Call permission** granted by the customer when Meta / your program enforces permission for outbound calls.

### Fields to configure
- No explicit Console form fields were identified in the self-help source; use the controls shown in **SR** for outbound calling.

### Steps
1. **Customer:** Send a message (for example **Hi** or any text) to the business **WhatsApp number** to create or maintain an **active session** for receiving an outbound call request.
2. **Agent:** In **SR**, while **Available**, open the **WhatsApp call widget** and request an **outbound** call to the customer.
3. Use the **calling window** to complete dial / connect actions per the current **SR** UI.
4. If the customer has not granted permission, ensure they complete the **Call permissions** prompt so the business can **reach out** with calls.
5. After permission and session requirements are met, complete the call; **CDR** / recordings may appear per `kb/channels/whatsapp-voice-cdr-insights-and-agent-analytics.md`.

### Validation / where to check
- Confirm an inbound message exists when your deployment requires an active session before outbound.
- Confirm the customer accepted **call permission** when outbound is permission-gated.

### Troubleshooting
- **No call permission** or **no valid active session:** resolve session (user message) and permission before retrying outbound.
- For **SIP / API** integrations, **403** permission failures and retry policy: `kb/integrations/whatsapp-voice-sip-call-permissions-and-errors.md`.
- If channel behavior is wrong, confirm the correct channel/app is connected and the latest configuration is live.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) in **Gupshup Console** when you change settings that affect WhatsApp or routing.

### Setup path
- **SR** → **WhatsApp call widget** → **calling window** → outbound call.

## Options / variants
- Demo training used a **deep link with prefilled text** to illustrate session start; production uses any valid inbound message that satisfies your session rules.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Inbound overview: `kb/channels/whatsapp-voice-overview-and-inbound-calls.md`
- CDR and analytics: `kb/channels/whatsapp-voice-cdr-insights-and-agent-analytics.md`
- SIP outbound (BIC) and headers: `kb/integrations/whatsapp-voice-sip-outbound-calls.md`

## Module disambiguation docs
- **SR** outbound calling is distinct from dialer **SIP INVITE** flows; use Integrations SIP articles when implementing trunk-side BIC.

## Reference (from source)
<!-- procedural:v2 -->
# WhatsApp Voice — outbound calls, session, and permissions

**Module**: Channels

## Overview
Outbound flow: customer sends a message to create an **active session**; agent uses the **WhatsApp call widget** and **calling window**; users may see **Call permissions** to allow business outreach.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
**Outbound — customer:** Send **Hi** or any text to the business WhatsApp number so a session exists for an outbound call request.

**Outbound — agent:** Click the **WhatsApp call widget** to request outbound call; use the **calling window** and dialing steps in **SR**.

**Errors (from self-help):** No call permission / no valid active session until session and permission are satisfied.

**Permission UX:** Customer receives **Call permissions** request and must allow the business to reach out.
