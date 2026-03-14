source_url: https://console-docs.gupshup.io/docs/call-return-node

<!-- kb-golden:v10 -->
# Call & Return Node

**Module**: Bot Studio

## Definition
This is one of the action nodes to call another journey from the ongoing journey and return back to the same journey when the called journey is executed completely.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Call & Return Node

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Call & Return Node**.
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
- Go to **Call & Return Node**.

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
# Call & Return Node

**Module**: Bot Studio

## Overview
This is one of the action nodes to call another journey from the ongoing journey and return back to the same journey when the called journey is executed completely.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
This is one of the action nodes to call another journey from the ongoing journey and return back to the same journey when the called journey is executed completely.

This helps in breaking a larger chatbot journey is smaller journeys and calling them on a journey as and when required.

### When to use

Call & Return node is helpful in calling a subpart of a chatbot journey in a journey. For instance: A lead generation bot along with post-sales support is to be made, in this situation, a sub journey for Lead generation can be made along with post-sales support use cases like order tracking, return or refund separately in the chatbot.

The lead generation sub-journey can be called in the main journey using the call & return node.

### How to use

The call & return node is present on the left panel in the action & prompt menu.

NOTE: Only deployed Journey can be seen in the dropdown of Call & Return Node.

### Call & Return Node

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
