source_url: https://console-docs.gupshup.io/docs/call-return-node

<!-- kb-golden:v4 -->
# Call & Return Node

**Module**: Bot Studio

## Definition
This is one of the action nodes to call another journey from the ongoing journey and return back to the same journey when the called journey is executed completely.

## Procedure
### Exact path
Gupshup Console → Bot Studio → Call & Return Node

### Where to configure it
Gupshup Console → Bot Studio → Call & Return Node

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Call & Return Node**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- How to use
- Call & Return Node

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation
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
