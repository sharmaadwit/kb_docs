source_url: https://console-docs.gupshup.io/docs/setting-up-retargeting-post-go-live

<!-- kb-golden:v9 -->
# Setting up Retargeting post go-live

**Module**: Ctx

## Definition
- To maximize returns from ad spends we recommend to use the 72-hour free window to send out QBM messages to customers
- Seamless experience (Just select the segment in the audience section and send the campaign, no file download or upload is required)
- Ability to send interactive campaigns for higher conversion
- Realtime and campaign-wise analytics
# Best Practices:

## Procedure
### Exact UI path
Gupshup Console → CTX → Setting up Retargeting post go-live

### Steps
1. Open Gupshup Console.
2. Go to **CTX**.
3. Go to **Setting up Retargeting post go-live**.
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
- Go to **CTX**.
- Go to **Setting up Retargeting post go-live**.

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- CTX campaign → Bot Studio journey → Goal measurement

## Module disambiguation docs
- CTX covers ad-to-WhatsApp campaign flows; bot conversation logic still lives in **Bot Studio**.

## Reference (from source)
<!-- procedural:v2 -->
# Setting up Retargeting post go-live

**Module**: Ctx

## Overview
- To maximize returns from ad spends we recommend to use the 72-hour free window to send out QBM messages to customers
- Seamless experience (Just select the segment in the audience section and send the campaign, no file download or upload is required)
- Ability to send interactive campaigns for higher conversion
- Realtime and campaign-wise analytics
# Best Practices:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
# Advantages of Retargeting

- To maximize returns from ad spends we recommend to use the 72-hour free window to send out QBM messages to customers
- Seamless experience (Just select the segment in the audience section and send the campaign, no file download or upload is required)
- Ability to send interactive campaigns for higher conversion
- Realtime and campaign-wise analytics
# Best Practices:

- Please make sure that the WhatsApp template being used for retargeting does not contain any variables
- Please ensure that the option “Retarget after default free window” is left unchecked, otherwise it may incur a cost if retargeting messages are sent to users outside the 72-hour window
- Free retargeting messages are only sent to users who are either a “CTX Lead” or a “CTX Deep Conversation” in the funnel. Users who have completed the journey ie “CTX Qualified Lead” do not receive retargeting QBM messages.
# Setting up retargeting in Ads Management

Step 1: On the left menu of the console, click on Click-to-chat ads->Ad Management

Step 2: Click on "Ad Campaigns" under the Ads Account

Step 3: Click on "View Ads" button for the campaign

Step 4: For the ads connected to bot, click on "Retarget"

Step 5: Select the "Retarget Mode" and the WA approved messaging template, and journey along with the number of hours after which you want the lead to receive the first retargeting message

Step 6: You have the option of sending 2nd and 3rd retargeting message by clicking on the toggle on the right. DND window signifies the hours in-between which leads will not receive any retargeting messages. Click on the toggle to setup DND.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 6 months ago
