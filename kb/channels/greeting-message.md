source_url: https://console-docs.gupshup.io/docs/web-greeting-message

<!-- kb-golden:v10 -->
# Greeting Message

**Module**: Channels

## Definition
The Greeting Message is the first message that appears to users when they open your Web chat widget for the very first time.

## Procedure
### Exact UI path
Gupshup Console → Channels → Greeting Message

### Prerequisites
- Access to the target channel configuration in Gupshup Console.
- A connected bot/app if the channel must route traffic to Bot Studio.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Channels**.
3. Go to **Greeting Message**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Send a live test on the target channel and confirm the bot/channel behavior matches the configuration.

### Troubleshooting
- If channel behavior is wrong, confirm the correct channel/app is connected and the latest bot configuration is live.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Channels**.
- Go to **Greeting Message**.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Identify the upstream module where this is configured and the downstream module where the outcome is verified.

## Module disambiguation docs
- Channel setup governs connectivity and channel features; bot logic is configured separately in **Bot Studio**.

## Reference (from source)
<!-- procedural:v2 -->
# Greeting Message

**Module**: Channels

## Overview
The Greeting Message is the first message that appears to users when they open your Web chat widget for the very first time.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
The Greeting Message is the first message that appears to users when they open your Web chat widget for the very first time.

If the "Retain Customer Chat History" toggle is enabled, the Greeting Message will be sent only for the first time the user visits from a specific browser and device.

- You can add the following in your greeting message: Image Text Quick Reply Buttons (max. 20)
- Image
- Text
- Quick Reply Buttons (max. 20)
- You can check how your greeting message will appear to users in the Preview displayed on the right.
Updated 10 months ago

- Persistent Menu

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
