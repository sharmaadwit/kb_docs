source_url: https://console-docs.gupshup.io/docs/creating-a-click-to-whatsapp-ad-on-ttam

<!-- kb-golden:v9 -->
# Creating a Click-to-WhatsApp Ad on TTAM

**Module**: Ctx

## Definition
Log on to TikTok Ads Manager, go to campaign and click on "Create"

## Procedure
### Exact UI path
Gupshup Console → CTX → Creating a Click-to-WhatsApp Ad on TTAM

### Steps
1. Open Gupshup Console.
2. Go to **CTX**.
3. Go to **Creating a Click-to-WhatsApp Ad on TTAM**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Step 3 (Optional): Split Test can be used for Targeting, Bidding & Optimization, Creative

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
- Go to **Creating a Click-to-WhatsApp Ad on TTAM**.

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
# Creating a Click-to-WhatsApp Ad on TTAM

**Module**: Ctx

## Overview
Log on to TikTok Ads Manager, go to campaign and click on "Create"

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
# Creating a CTWA campaign on TTAM

Log on to TikTok Ads Manager, go to campaign and click on "Create"

### Campaign Level:

Step 1: Log on to TikTok Ads Manager, go to campaign and click on "Create"

Step 2: Choose "Lead generation" as your campaign objective

Step 3 (Optional): Split Test can be used for Targeting, Bidding & Optimization, Creative

Step 4: Click "Continue"

### Ad-Group Level:

Step 1: Choose "Instant messaging apps" as your "Optimization location"

Step 2: Placement will be TikTok by default. Now set up the audience, location, dayparting and budge as needed

Step 3: Select your Instant messaging app as WhatsApp and choose your Optimization Goal as "Conversation"

- Note: 'Conversations' option will be greyed and unable to select if no event sets have been created before on Gupshup.
Step 4: Add your WhatsApp business API number, and your message event-set configured on Gupshup will be automatically matched and populated.

### Ad Level:

Step 1: You can choose to use a TikTok identity to deliver Spark Ads but it is not mandatory. Add the creative or video

Step 2: Add the Text under "Text" to enter the headline of the ad

Step 3: In the next option, add the CTA that users will click on to redirect to WhatsApp

Step 4: Destination: This field will be automatically filled. To edit, please return to Ad Group level. Click "Publish" to start your Instant Messaging Ads.

Here's a detailed guide on creating TikTok Messaging Ads: https://ads.tiktok.com/help/article/how-to-set-up-tiktok-instant-messaging-ads?lang=en

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- Step 4: Destination: This field will be automatically filled. To edit, please return to Ad Group level. Click "Publish" to start your Instant Messaging Ads.

**Last updated (from source)**: Updated 7 months ago
