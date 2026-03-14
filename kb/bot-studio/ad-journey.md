source_url: https://console-docs.gupshup.io/docs/ad-journey

<!-- kb-golden:v10 -->
# Ad Journey

**Module**: Bot Studio

## Definition
Ad Journeys help businesses support interaction with customers when they interact with click-to-chat ads on Facebook or Instagram. To know more about click-to-chat Ads on Gupshup Console, contact us at console-support@gupshup.io.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Ad Journey

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Ad Journey**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run the flow in **Test your Bot** and confirm the expected node/path executes.
- If the change must affect live traffic, use **Save & Deploy** and verify on the target channel.

### Troubleshooting
- If behavior is unchanged, confirm you updated the correct node and used **Save & Deploy** for live channels.
- If the wrong branch/path runs, re-check conditions, connected nodes, and fallback connectors.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Bot Studio**.
- Go to **Ad Journey**.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Ad Journey

**Module**: Bot Studio

## Overview
Ad Journeys help businesses support interaction with customers when they interact with click-to-chat ads on Facebook or Instagram. To know more about click-to-chat Ads on Gupshup Console, contact us at console-support@gupshup.io.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Ad Journeys help businesses support interaction with customers when they interact with click-to-chat ads on Facebook or Instagram. To know more about click-to-chat Ads on Gupshup Console, contact us at console-support@gupshup.io.

If the console account supports click-to-chat ads, a new type of journeys called "Ad Journeys" will be available in Bot Studio.

In this module, businesses can design ad journeys that can be triggered when a customer responds to an Ad on Instagram or Facebook. Once an Ad Journey is designed, it can be mapped with an Ad on the "Click-to-Chat Ads" module in the console account.

To learn more about mapping Ad Journeys with Ad Journeys in the "Click-to-Chat Ads", contact us at console-support@gupshup.io. Once ads are mapped with Ad journeys in Bot Studio, the mapping will be updated in the Ad Campaign Node in the view-only Configuration Journey.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
