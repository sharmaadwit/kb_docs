source_url: https://console-docs.gupshup.io/docs/campaign-journey

<!-- kb-golden:v4 -->
# Campaign Journey

**Module**: Bot Studio

## Definition
Use Campaign Journeys to interact with customers who respond to your Whatsapp Marketing Campaigns.

## Procedure
### Exact path
Gupshup Console → Bot Studio → Campaign Journey

### Where to configure it
Gupshup Console → Bot Studio → Campaign Journey

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Campaign Journey**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation
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
