source_url: https://console-docs.gupshup.io/docs/goal-node-beta

<!-- kb-golden:v10 -->
# Goal Node

**Module**: Bot Studio

## Definition
To track the milestones attained by users who are interacting with a Bot, bot designer can add the Goal Node in journeys. For instance, if a business wants to track how many customers have purchased a certain product, a goal node can be introduced in the journey.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Goal Node

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Goal Node**.
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
- Go to **Goal Node**.

## Options / variants
- You can use the analytics toggle to see node traversal and drop outs for this goal.

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
# Goal Node

**Module**: Bot Studio

## Overview
To track the milestones attained by users who are interacting with a Bot, bot designer can add the Goal Node in journeys. For instance, if a business wants to track how many customers have purchased a certain product, a goal node can be introduced in the journey.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### When to use

To track the milestones attained by users who are interacting with a Bot, bot designer can add the Goal Node in journeys. For instance, if a business wants to track how many customers have purchased a certain product, a goal node can be introduced in the journey.

### How to use

Drag and drop the Goal Node from the Action nodes on the Node Panel.

For instance, in the example given below, Goal Node can be used to mark a lead as generated when customers provide their name, phone number and email.

Goals can be created from the bot analytics module. Please contact console-support@gupshup.io to add goals name, milestone name and tracker names from the analytics module.

In the Goal Node, select the goal name, milestone name and tracker name and enter the tracker value or select a variable.

You can use the analytics toggle to see node traversal and drop outs for this goal.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
