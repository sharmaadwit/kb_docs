source_url: https://console-docs.gupshup.io/docs/creating-and-analysing-a-click-to-whatsapp-campaign

<!-- kb-golden:v10 -->
# Ctwa To Bot To Goals

**Module**: Workflows

## Definition
Use this workflow when you want to:
- launch a **Click-to-WhatsApp (CTWA / CTX)** campaign
- send the click into the correct **Bot Studio** journey
- measure conversion using **Goals**

## Procedure
### Exact UI path
Gupshup Console → CTX / Campaign setup
Gupshup Console → Bot Studio → Journey Builder
Gupshup Console → Goals

### Where to configure it
- Configure the ad/campaign in **CTX**.
- Configure the bot entry flow in **Bot Studio**.
- Configure measurement in **Goals** / **Goal Analytics**.

### Prerequisites
- Access to **CTX**, **Bot Studio**, and **Goals**.
- A WhatsApp destination/campaign setup that can launch the bot flow.
- A Bot Studio journey that is ready to receive the CTWA user entry.
- A goal definition for the conversion event you want to measure.

### Fields to configure
- **Campaign / ad destination**
- **Bot journey / starting flow**
- **Goal / milestone / conversion point**

### Steps
1. Open Gupshup Console.
2. In **CTX**, create or open the Click-to-WhatsApp campaign/ad.
3. Configure the campaign so users land in the intended WhatsApp/bot entry point.
4. In **Bot Studio**, open the target journey and confirm the entry/start flow is ready for CTWA users.
5. Use **Save & Deploy** in Bot Studio so the live bot is ready before traffic is sent.
6. In **Goals**, create or update the goal that should represent conversion.
7. Implement the goal in the relevant Bot Studio journey path.
8. Launch a test click from the CTWA campaign and complete the intended conversion path.
9. Verify the goal/conversion appears in Goal Analytics.

### Validation / where to check
- Confirm the CTWA click opens the expected WhatsApp/bot experience.
- Confirm the user enters the correct **Bot Studio** journey path.
- Confirm the configured **Goal** is hit for the successful conversion path.
- Verify the result in **Goal Analytics**.

### Troubleshooting
- If the CTWA click opens WhatsApp but not the right bot flow, re-check the CTWA destination and the deployed Bot Studio entry flow.
- If the bot behaves correctly but conversions are not counted, re-check where the **Goal** is implemented in the journey.
- If the live experience is outdated, confirm Bot Studio changes were **Save & Deploy**'d, not just saved.

### Save / publish / deploy behavior
- Save/publish the CTWA campaign in **CTX**.
- Use **Save & Deploy** in **Bot Studio** so the live bot receives traffic correctly.
- Save the **Goal** configuration before validating analytics.

## Options / variants
- CTWA / CTX campaign setup
- Bot entry flow / journey selection
- Goal definition / milestone-based conversion measurement

## Field mapping / schemas
- No single schema is defined on this workflow page; see the linked CTX, Bot Studio, and Goals pages for module-specific fields.

## Cross-module workflow docs
- CTX campaign → WhatsApp click → Bot Studio journey → Goal hit → Goal Analytics
- Campaign launch → live bot behavior → conversion measurement

## Module disambiguation docs
- **CTX / CTWA** controls the ad/campaign entry.
- **Bot Studio** controls the conversation logic after the click.
- **Goals** controls conversion measurement; it does not control campaign routing or bot deployment.

## Reference (from source)
- CTX: `kb/ctx/creating-and-analysing-a-click-to-whatsapp-campaign.md`
- Bot Studio: `kb/bot-studio/getting-started-with-bot-studio.md`
- Goals: `kb/goals/creating-goals.md`, `kb/goals/goal-analytics.md`
