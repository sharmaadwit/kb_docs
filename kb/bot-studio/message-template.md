source_url: https://console-docs.gupshup.io/docs/message-template

<!-- kb-golden:v9 -->
# Message Template

**Module**: Bot Studio

## Definition
The Message template node allows the selection of a pre-approved template for creating interactive campaigns. A template can be added to the chatbot conversation using this node and will reflect on the channel if applicable. Values to the variables in templates can be defined as per the need.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Message Template

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Message Template**.
4. Select one of the listed templates.
5. Add the Fallback Value per variable present in the template.
6. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- _Run a quick smoke test and confirm expected behavior._

### Fields to configure
- Fallback connector path

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- _Add common failure modes and how to fix them._

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **Message Template**.

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
# Message Template

**Module**: Bot Studio

## Overview
The Message template node allows the selection of a pre-approved template for creating interactive campaigns. A template can be added to the chatbot conversation using this node and will reflect on the channel if applicable. Values to the variables in templates can be defined as per the need.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
The Message template node allows the selection of a pre-approved template for creating interactive campaigns. A template can be added to the chatbot conversation using this node and will reflect on the channel if applicable. Values to the variables in templates can be defined as per the need.

### When to use

To add a template message in the conversation journey or to create marketing use cases. Message Templates can be added only if the account has pre-configured message templates.

### Limitations

- The message template can’t be blank.
- A fallback value is mandatory to be defined per variable present in the template.
### How to use

VIDEO COMING SOON

The Message Template node can be added to the canvas or dragged from the Message Node section in the left-side panel.

When the account has pre-configured template messages, click the select template button to add template

Select one of the listed templates

Add the Fallback Value per variable present in the template

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
