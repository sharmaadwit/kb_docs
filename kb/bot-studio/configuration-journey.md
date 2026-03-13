source_url: https://console-docs.gupshup.io/docs/configuration-journey

<!-- kb-golden:v9 -->
# Configuration Journey

**Module**: Bot Studio

## Definition
It is a system-generated journey that needs no alterations and is view-only to provide an overview of different journeys being handled by the Bot.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Configuration Journey

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Configuration Journey**.
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
- Go to **Configuration Journey**.

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
# Configuration Journey

**Module**: Bot Studio

## Overview
It is a system-generated journey that needs no alterations and is view-only to provide an overview of different journeys being handled by the Bot.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
It is a system-generated journey that needs no alterations and is view-only to provide an overview of different journeys being handled by the Bot.

The configuration journey carries information about the campaign and its associated journey.

It has the following nodes set in logic:

- Start Node
- Condition Node With Events
- Marketing Module Node - This contains all mappings between campaigns and associated journeys.
- Ad Campaign Module Node - This contains all mappings between ads and associated journeys.
- Keyword Trigger Node - This contains all mappings between user input and the associated user journey that can be triggered. For example, if Journey "Welcome" is linked to keyword "Hi", this journey will be triggered when a user says "Hi".
- Return Failure Node
In this journey, you can view keyword-based triggers, for eg, when a user says "Hi", journey Hi can be triggered.

The contains all mappings between campaigns and associated journeys.

### Configuration Journey

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
