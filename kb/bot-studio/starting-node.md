source_url: https://console-docs.gupshup.io/docs/starting-node

<!-- kb-golden:v9 -->
# Starting Node

**Module**: Bot Studio

## Definition
Starting Node is the default available node in all new journeys. The configuration of Starting Node triggers a journey based on the event received.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Starting Node

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Starting Node**.
4. Click on the Starting Node to open the Node configuration on the right side.
5. Select from the the available list of Event based on which you would like to trigger the journey.
6. Click **Save** (or **Save & Deploy**) to apply changes.

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
- Go to **Starting Node**.

## Options / variants
- Select from the the available list of Event based on which you would like to trigger the journey

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
# Starting Node

**Module**: Bot Studio

## Overview
Starting Node is the default available node in all new journeys. The configuration of Starting Node triggers a journey based on the event received.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Starting Node is the default available node in all new journeys. The configuration of Starting Node triggers a journey based on the event received.

### How to configure

- Click on the Starting Node to open the Node configuration on the right side
- Select from the the available list of Event based on which you would like to trigger the journey
- There are three available selection viz. No Event, User Input and AI Trigger(available with AI Recipe)
- You can also add custom Conditions if required to personalize the event triggers
### Event Types:

- No Event: This option is selected when you don't want this journey to be trigger with any user action. Ideally journeys used with Call & Return nodes are used with No Event to ensure its triggered only through the Call & Return Node.
- User Input: This event is selected to trigger the journey based on a match with user input. You can select from list of available operations(contains, equals to etc.) to validate the user input and trigger the journey.
### Additional Condition:

Bot designers will also have provision to personalize or put conditional check for the events triggered before responding with a journey. These conditions can be added in the Start Node based on the available variables.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
