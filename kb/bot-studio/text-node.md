source_url: https://console-docs.gupshup.io/docs/text-node

<!-- kb-golden:v10 -->
# Text Node

**Module**: Bot Studio

## Definition
It is a node in which you can enter the text that you want to send to your customer. It can be just information or any sort of acknowledgment that you want to have in the conversation.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Text Node

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Text Node**.
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
- Go to **Text Node**.

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
# Text Node

**Module**: Bot Studio

## Overview
It is a node in which you can enter the text that you want to send to your customer. It can be just information or any sort of acknowledgment that you want to have in the conversation.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
It is a node in which you can enter the text that you want to send to your customer. It can be just information or any sort of acknowledgment that you want to have in the conversation.

### When to use

This node can be used when you want to send some information to the user without expecting any response to it.

### Elements of Text Node

- Textbox: The textbox is free size and can be pulled from the side to increase the size.
- Emoji: The icon when clicked will open the emoji dropdown to select any number of emojis
### Limitations

- Number of Characters - 640 Characters limit should not exceed
- Bot Says field should not be empty.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
