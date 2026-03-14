source_url: https://console-docs.gupshup.io/docs/configuration-journey

<!-- kb-golden:v10 -->
# Configuration Journey

**Module**: Bot Studio

## Definition
It is a system-generated journey that needs no alterations and is view-only to provide an overview of different journeys being handled by the Bot.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Configuration Journey

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Configuration Journey**.
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
- Go to **Configuration Journey**.

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
