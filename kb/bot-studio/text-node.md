source_url: https://console-docs.gupshup.io/docs/text-node

<!-- kb-golden:v9 -->
# Text Node

**Module**: Bot Studio

## Definition
It is a node in which you can enter the text that you want to send to your customer. It can be just information or any sort of acknowledgment that you want to have in the conversation.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Text Node

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Text Node**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- _Run a quick smoke test and confirm expected behavior._

### Fields to configure
- _List the fields/inputs you must set in the UI (and expected format)._

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- _Add common failure modes and how to fix them._

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **Text Node**.

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

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
