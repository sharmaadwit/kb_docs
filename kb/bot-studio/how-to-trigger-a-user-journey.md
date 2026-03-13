source_url: https://console-docs.gupshup.io/docs/how-to-trigger-a-user-journey

<!-- kb-golden:v9 -->
# How to trigger a User Journey

**Module**: Bot Studio

## Definition
User journeys can be triggered by adding the trigger words in the start node of each user journey. Once the triggers are added and user journey is saved and deployed, the journey will get triggered by the user input mentioned in the start node.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → How to trigger a User Journey

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **How to trigger a User Journey**.
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
- Go to **How to trigger a User Journey**.

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
# How to trigger a User Journey

**Module**: Bot Studio

## Overview
User journeys can be triggered by adding the trigger words in the start node of each user journey. Once the triggers are added and user journey is saved and deployed, the journey will get triggered by the user input mentioned in the start node.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
User journeys can be triggered by adding the trigger words in the start node of each user journey. Once the triggers are added and user journey is saved and deployed, the journey will get triggered by the user input mentioned in the start node.

Read the document on how to make changes in the start node of each user joureny.

The configuration journey is a view-only journey. The keyword trigger node in configuration journey gets updated when user journeys with triggers are saved and deployed.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
