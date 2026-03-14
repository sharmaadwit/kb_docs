source_url: https://console-docs.gupshup.io/docs/campaign-journey

<!-- kb-golden:v10 -->
# Campaign Journey

**Module**: Bot Studio

## Definition
Use Campaign Journeys to interact with customers who respond to your Whatsapp Marketing Campaigns.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Campaign Journey

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Campaign Journey**.
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
- Go to **Campaign Journey**.

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
# Campaign Journey

**Module**: Bot Studio

## Overview
Use Campaign Journeys to interact with customers who respond to your Whatsapp Marketing Campaigns.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Use Campaign Journeys to interact with customers who respond to your Whatsapp Marketing Campaigns.

Scheduling Marketing Campaigns in the Campaign Module of the console, automatically creates a 1-way Campaign Journey in the Bot Studio Section.

By default, this 1-way Campaign Journey is non editable and consists of the start node and template node.

If you wish to build an interactive campaign i.e. interact with customers when they respond to your marketing campaign, convert this 1-way campaign journey to interactive journey.

Once the campaign is converted to an interactive journey, the default journey contains the start node, template node and wait for event node. Do not modify the default nodes of this journey and build your journey further.

Now, you can edit your interactive campaign journey as required and save and deploy. When the marketing campaign gets triggered as per the schedule, the bot will trigger the interactive journey when customers respond to the marketing campaign. No changes are required in the start node as the journey gets triggered along with the scheduled campaign.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
