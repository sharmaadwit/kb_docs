source_url: https://console-docs.gupshup.io/docs/how-to-trigger-a-user-journey

<!-- kb-golden:v10 -->
# How to trigger a User Journey

**Module**: Bot Studio

## Definition
User journeys can be triggered by adding the trigger words in the start node of each user journey. Once the triggers are added and user journey is saved and deployed, the journey will get triggered by the user input mentioned in the start node.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → How to trigger a User Journey

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **How to trigger a User Journey**.
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
- Go to **How to trigger a User Journey**.

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
