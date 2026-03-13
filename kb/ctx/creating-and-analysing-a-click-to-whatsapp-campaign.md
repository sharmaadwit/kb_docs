source_url: https://console-docs.gupshup.io/docs/creating-a-tiktok-specific-bot-journey

<!-- kb-golden:v9 -->
# Creating and Analysing a Click-to-WhatsApp Campaign

**Module**: Ctx

## Definition
Step 1: Click on "Click to Chat Ads" -> Ad Management, and click on "Ad Campaigns"

## Procedure
### Exact UI path
Gupshup Console → CTX → Creating and Analysing a Click-to-WhatsApp Campaign

### Steps
1. Open Gupshup Console.
2. Go to **CTX**.
3. Go to **Creating and Analysing a Click-to-WhatsApp Campaign**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Step 3: Click on "Connect Bot" and in the pop-up that opens, click on "Confirm"

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
- Go to **Creating and Analysing a Click-to-WhatsApp Campaign**.

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
# Creating and Analysing a Click-to-WhatsApp Campaign

**Module**: Ctx

## Overview
Step 1: Click on "Click to Chat Ads" -> Ad Management, and click on "Ad Campaigns"

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
# Linking an ad journey to a campaign

Step 1: Click on "Click to Chat Ads" -> Ad Management, and click on "Ad Campaigns"

Step 2: Search for the campaign that has been configured for TikTok to WhatsApp and click on "View Ads"

Step 3: Click on "Connect Bot" and in the pop-up that opens, click on "Confirm"

Step 4: In the bot setup page, select the Ad Journey created and click on "Publish". Your TTWA campaign is now active.

# Setting up retargeting

Step 1: When you click on the CTWA configured campaign under “Ads Management”, click on the “Retarget” button

Step 2: Select the WA approved messaging template and journey along with the number of hours after which you want the lead to receive the first retargeting message

Step 3: You have the option of sending 2nd and 3rd retargeting message by clicking on the toggle on the right. DND window signifies the hours in-between which leads will not receive any retargeting messages

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- Step 4: In the bot setup page, select the Ad Journey created and click on "Publish". Your TTWA campaign is now active.

**Last updated (from source)**: Updated 7 months ago
