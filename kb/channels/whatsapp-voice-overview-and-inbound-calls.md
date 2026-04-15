source_url: https://console-docs.gupshup.io/docs/whatsapp-voice-inbound-calls

<!-- kb-golden:v10 -->
# WhatsApp Voice — overview and inbound calls

**Module**: Channels

## Definition
WhatsApp calling lets customers and businesses use a **unified WhatsApp Business number** for **WhatsApp Chat** (messaging) and **WhatsApp Call** (voice) on the same WABA number. Training material for this topic is based on the **WA Voice Self Help** document (Demo Document for WA Voice, v1.1, revision 20-02-2026).

## Procedure
### Exact UI path
- **Customer:** WhatsApp client → **Call** → business **WABA** phone number (same number as chat).
- **Agent:** **SR** (agent console) → sign in → **Available** (typically **top right**).

### Prerequisites
- **SR** login credentials for your deployment (issued separately; not in the self-help PDF).
- A **WABA** number enabled for WhatsApp Voice, with routing configured for your use case (for example **AI bot** vs **contact center (CC)** lines where separate numbers are used).

### Fields to configure
- No explicit Console form fields were identified in the self-help source; routing (AI vs CC) follows your project configuration.

### Steps
1. **Customer — inbound:** The customer places a **WhatsApp voice call** to the business **WhatsApp Business** number.
2. **Routing:** The call is offered on the business side according to how **AI bot** vs **CC** routing is set up for that number (demo material illustrated separate numbers per line type).
3. **Agent:** Open **SR** and sign in with credentials provided for your project.
4. Set agent status to **Available** (commonly from the **top right** of the agent UI).
5. When **Available**, the agent can **receive inbound** WhatsApp voice calls routed to the correct queue or skill group.
6. Answer the call from the agent **calling / queue** UI (labels depend on product version).

### Validation / where to check
- Place a test inbound call to the WABA number and confirm the agent receives it while **Available**.
- Confirm routing matches the intended line (AI vs human/CC) for that number.

### Troubleshooting
- If the agent does not receive calls, confirm **SR** sign-in, **Available** status, and that the dialed number matches the configured WABA / queue.
- If channel behavior is wrong, confirm the correct channel/app is connected and the latest configuration is live.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) in **Gupshup Console** when you change channel or app settings that affect WhatsApp or routing; **SR** sign-in and **Available** do not use Console **Save**.

### Setup path
- **SR** → sign in → **Available** → wait for inbound WhatsApp Voice.

## Options / variants
- **AI bot** line vs **CC** line: demo documentation used different WABA numbers to illustrate separate entry points; production follows your routing design.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Outbound flow, session, and call permission: `kb/channels/whatsapp-voice-outbound-calls-session-and-permissions.md`
- Call logs (CDR), insights, analytics: `kb/channels/whatsapp-voice-cdr-insights-and-agent-analytics.md`
- SIP integration (UIC/BIC, gateway): `kb/integrations/whatsapp-voice-sip-overview.md`, `kb/integrations/whatsapp-voice-sip-inbound-calls.md`

## Module disambiguation docs
- Channel setup and WhatsApp numbering govern how users reach the business; agent handling in **SR** is separate from **Bot Studio** journey canvas configuration unless integrated by your deployment.

## Reference (from source)
<!-- procedural:v2 -->
# WhatsApp Voice — overview and inbound calls

**Module**: Channels

## Overview
WhatsApp calling supports a unified business number for **WhatsApp Chat** and **WhatsApp Call**. **SR** login credentials are shared separately for training and production environments.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
**Inbound — customer:** Customer calls the WABA number on WhatsApp (demo material referenced distinct numbers for an AI bot vs CC).

**Inbound — agent:** Agent logs in to **SR**, marks **Available** from the **top right**, then receives inbound calls in the agent UI.

## Demo and training references
- **WhatsApp Calls over SR** (training video title from self-help).
- **Customer View of WhatsApp Voice — Business Calls** (training video title from self-help).
