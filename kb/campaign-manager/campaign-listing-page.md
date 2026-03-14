source_url: https://console-docs.gupshup.io/docs/campaign-listing-page

<!-- kb-golden:v10 -->
# Campaign Listing Page

**Module**: Campaign Manager

## Definition
- The campaign listing page provides a list of all campaigns along with the channel for which it was scheduled, start date and time of the campaign, status and some high level analytics numbers (sent/delivered/read).
- On the top, you will find the WhatsApp tier limit displayed. This limit is defined by Meta and it can be upgraded to infinite number of messages. More details on how to upgrade the tier limit can be found here.
- You can apply filters to the listing table based on different statuses or search for a campaign based on the Title given for the campaign.
- You can clone or delete a campaign or create a new campaign from this page.
- You can stop a scheduled campaign from getting sent by deleting the scheduled campaign.
- Clicking on the name of the campaign with status ‘Sent’ will land you on the analytics page of that campaign.

## Procedure
### Exact UI path
Gupshup Console → Campaign Manager → Campaign Listing Page

### Prerequisites
- Access to Campaign Manager for the target brand/project.
- A campaign or campaign draft relevant to this configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Campaign Manager**.
3. Go to **Campaign Listing Page**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run a small test send and confirm the expected campaign status/metrics appear in Campaign Manager.

### Troubleshooting
- If data is missing or stale, confirm the campaign has actually run and refresh/reopen the analytics view.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Campaign Manager**.
- Go to **Campaign Listing Page**.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Identify the upstream module where this is configured and the downstream module where the outcome is verified.

## Module disambiguation docs
- Campaign creation/config is in **Campaign Manager**; delivery status can also be observed via **Webhooks** (Integrations).

## Reference (from source)
<!-- procedural:v2 -->
# Campaign Listing Page

**Module**: Campaign Manager

## Overview
- The campaign listing page provides a list of all campaigns along with the channel for which it was scheduled, start date and time of the campaign, status and some high level analytics numbers (sent/delivered/read).
- On the top, you will find the WhatsApp tier limit displayed. This limit is defined by Meta and it can be upgraded to infinite number of messages. More details on how to upgrade the tier limit can be found here.
- You can apply filters to the listing table based on different statuses or search for a campaign based on the Title given for the campaign.
- You can clone or delete a campaign or create a new campaign from this page.
- You can stop a scheduled campaign from getting sent by deleting the scheduled campaign.
- Clicking on the name of the campaign with status ‘Sent’ will land you on the analytics page of that campaign.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
- The campaign listing page provides a list of all campaigns along with the channel for which it was scheduled, start date and time of the campaign, status and some high level analytics numbers (sent/delivered/read).
- On the top, you will find the WhatsApp tier limit displayed. This limit is defined by Meta and it can be upgraded to infinite number of messages. More details on how to upgrade the tier limit can be found here.
- You can apply filters to the listing table based on different statuses or search for a campaign based on the Title given for the campaign.
- You can clone or delete a campaign or create a new campaign from this page.
- You can stop a scheduled campaign from getting sent by deleting the scheduled campaign.
- Clicking on the name of the campaign with status ‘Sent’ will land you on the analytics page of that campaign.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
