source_url: https://console-docs.gupshup.io/docs/how-to-measure-click-through-rates

<!-- kb-golden:v4 -->
# How to measure Click through Rates?

**Module**: Campaign Manager

## Definition
You can now track click through rates for a campaign. Now track which links were clicked, how many times and by whom.

## Procedure
### Exact path
Gupshup Console → Campaign Manager → How to measure Click through Rates?

### Where to configure it
Gupshup Console → Campaign Manager → How to measure Click through Rates?

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Campaign Manager → How to measure Click through Rates?**.
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
- We need to note that links mentioned in the campaign message cannot be tracked. Only links which are replaced in place of variables in a template message or "Dynamic Link Tracking CTA Button link" can be tracked.

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation
- Campaign creation/config is in **Campaign Manager**; delivery status can also be observed via **Webhooks** (Integrations).

## Reference (from source)
<!-- procedural:v2 -->
# How to measure Click through Rates?

**Module**: Campaign Manager

## Overview
You can now track click through rates for a campaign. Now track which links were clicked, how many times and by whom.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
You can now track click through rates for a campaign. Now track which links were clicked, how many times and by whom.

- To enable link tracking, click the checkbox on the audience page while creating the campaign.
- After you enable the checkbox, upload a file which has a column with links. Name that column precisely to identify links.
- We need to note that links mentioned in the campaign message cannot be tracked. Only links which are replaced in place of variables in a template message or "Dynamic Link Tracking CTA Button link" can be tracked.
- Let's first understand how to track links which are replaced in place of variables. After enabling the link tracking on audience page, select a template in which you need to use the links mentioned in the file. On the template variable substitution page, select the column with the links against the variable which you wish to replace.
- Please note that links mentioned in the fallback cannot be tracked. Hence, mention all links which you need to track in the file uploaded. File uploaded may contain same links for all phone numbers or different links for different phone numbers.
- Now lets take the case of "Dynamic Link Tracking CTA Button". To track links on CTA button, you need to create a template of type "Dynamic Link Tracking". After enabling the link tracking on audience page, select a template which is of the type dynamic link tracking CTA button. On the template variable substitution page, select the column with the links against the "Button URL". All clicks on such CTA button will be tracked.
- Campaign analytics will show Click analysis real time covering the total clicks, unique clicks, CTR and Link Tracking Report. Total Clicks - Indicates the total number of times users have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Total clicks will be 4. Unique Clicks - Indicates the number of users that have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Unique clicks will be 1. Click Through Rate - Indicates the % of times users have Clicked a link of a WhatsApp campaign after viewing it. It is calculated as [(Total Clicks / Total Read) * 100][(Total Clicks / Total Read) * 100] Link tracking Report - It gives timewise summary of clicks which will have original URL, GupShup URL, time at which the link was clicked, IP address, device and OS of the end user.
- Total Clicks - Indicates the total number of times users have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Total clicks will be 4.
- Unique Clicks - Indicates the number of users that have clicked on a link included in the campaign. This means that if a user clicks 3 times on a link and 1 time on another link in the message, then Unique clicks will be 1.
- Click Through Rate - Indicates the % of times users have Clicked a link of a WhatsApp campaign after viewing it. It is calculated as [(Total Clicks / Total Read) * 100][(Total Clicks / Total Read) * 100]
- Link tracking Report - It gives timewise summary of clicks which will have original URL, GupShup URL, time at which the link was clicked, IP address, device and OS of the end user.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
