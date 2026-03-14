source_url: https://console-docs.gupshup.io/docs/multi-journey-user-journeys

<!-- kb-golden:v10 -->
# Multi-Journey - User Journeys

**Module**: Bot Studio

## Definition
Multi Journey is the concept of having a complex use case broken down into smaller journeys in a chatbot which can be called in any other journey.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Multi-Journey - User Journeys

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Multi-Journey - User Journeys**.
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
- Go to **Multi-Journey - User Journeys**.

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
