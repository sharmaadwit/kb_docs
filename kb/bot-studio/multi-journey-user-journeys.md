source_url: https://console-docs.gupshup.io/docs/multi-journey-user-journeys

<!-- kb-golden:v9 -->
# Multi-Journey - User Journeys

**Module**: Bot Studio

## Definition
Multi Journey is the concept of having a complex use case broken down into smaller journeys in a chatbot which can be called in any other journey.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Multi-Journey - User Journeys

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Multi-Journey - User Journeys**.
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
- Go to **Multi-Journey - User Journeys**.

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
# Multi-Journey - User Journeys

**Module**: Bot Studio

## Overview
Multi Journey is the concept of having a complex use case broken down into smaller journeys in a chatbot which can be called in any other journey.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### Multi Journey

Multi Journey is the concept of having a complex use case broken down into smaller journeys in a chatbot which can be called in any other journey.

Users can make multiple journeys to support a complex use case and call the sub-journeys in the main journey.

### When to use

In order to break a larger use case into smaller journeys, the multi-journey concept can be used. You can make the journey reusable by making a part of the complete flow broken into smaller parts and calling it in other journeys as and when required.

For instance: Lead Generation flow along with post-sales support is to be made. There can be a need for a part of the complete journey which is intermittent.

Additionally, multi-journey is to support campaigns for which users might need to create a different journey for each campaign. All these different journeys can also be utilized to create a bigger conversation journey.

### How to use

Multi Journey can be used from the My Journeys of the Bot Studio.

### Multi Journey Screen

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
