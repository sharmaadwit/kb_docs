source_url: https://console-docs.gupshup.io/docs/delay-node

<!-- kb-golden:v9 -->
# Delay Node

**Module**: Bot Studio

## Definition
Node to put a delay in between two messages during the conversation. Using this node, a maximum of 10 seconds delay can be introduced between 2 chatbot messages.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Delay Node

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Delay Node**.
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
- Delay can be used as per the requirement wherever there is a need to introduce a certain time gap between 2 chatbot messages and enhance the user experience.

### Setup path
- Go to **Bot Studio**.
- Go to **Delay Node**.

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
# Delay Node

**Module**: Bot Studio

## Overview
Node to put a delay in between two messages during the conversation. Using this node, a maximum of 10 seconds delay can be introduced between 2 chatbot messages.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### Delay

Node to put a delay in between two messages during the conversation. Using this node, a maximum of 10 seconds delay can be introduced between 2 chatbot messages.

### When to use

Delay can be used as per the requirement wherever there is a need to introduce a certain time gap between 2 chatbot messages and enhance the user experience.

### How to use

Delay Node can be dragged and dropped on the canvas from the left-hand actions & prompts menu by setting a particular delay between 0-10 seconds in two consequent messages.

### Delay Node

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
