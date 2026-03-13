source_url: https://console-docs.gupshup.io/docs/connecting-ad-to-bot-in-gupshup-console

<!-- kb-golden:v9 -->
# Connecting ad to bot in Gupshup Console

**Module**: Ctx

## Definition
Best Practices:

## Procedure
### Exact UI path
Gupshup Console → CTX → Connecting ad to bot in Gupshup Console

### Steps
1. Open Gupshup Console.
2. Go to **CTX**.
3. Go to **Connecting ad to bot in Gupshup Console**.
4. Click on Bot Studio -> Journeys.
5. Click on "+Create Ad Journey" button on the top right corner and select "Start from scratch".
6. Click on the "Call and Return" node and this will get added in the journey. Click on the node and select the desired user journey that needs to be connected to CTWA ads.
7. Click on Click to Chat Ads -> Ad Management.
8. Click on "View Campaigns".
9. Select the Ad journey from the list of journeys that appear and click on "Connect Bot". Disclaimer: Only Ad Journeys are visible in this list, so as a best practice please ensure your user journey has been converted to an ad journey, following the steps shown in section 2.
10. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- On the ads page, click on "Connect Bot" and in the pop-up that opens for verification, click on "Confirm"

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
- Go to **Connecting ad to bot in Gupshup Console**.

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
# Connecting ad to bot in Gupshup Console

**Module**: Ctx

## Overview
Best Practices:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Best Practices:

- Please make sure that the journey that needs to be run for CTWA is converted from a user journey to an ad journey. Only Ad journeys can be connected to CTWA ads
- As a best practice, run the FB preview link generated from Meta Ads Manager to check if the journey is working correctly and if the bot is portraying normal behaviour.
- (Get started by creating a user journey)
Converting a User Journey to Ad Journey:

- Click on Bot Studio -> Journeys
- The main page lists all the User Journeys. On the user journey tab, click on the drop-down and select "Ad Journeys"
- Click on "+Create Ad Journey" button on the top right corner and select "Start from scratch"
- In the journey builder screen that opens, click on the blue dot on the right border of the starting node and select "Actions"
- Under the "Actions" tab, select "Call and Return" as the option:
- Click on the "Call and Return" node and this will get added in the journey. Click on the node and select the desired user journey that needs to be connected to CTWA ads.
- Once the journey is selected, close the node settings and click on "Save and Deploy". Your ad journey is now ready.
Step-by-step Process: Connecting Ad Journey to CTWA Ad

- Click on Click to Chat Ads -> Ad Management
- Click on "View Campaigns"
- For the campaign name that is configured for CTWA, click on "View Ads"
- On the ads page, click on "Connect Bot" and in the pop-up that opens for verification, click on "Confirm"
- Select the Ad journey from the list of journeys that appear and click on "Connect Bot". Disclaimer: Only Ad Journeys are visible in this list, so as a best practice please ensure your user journey has been converted to an ad journey, following the steps shown in section 2.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Once the journey is selected, close the node settings and click on "Save and Deploy". Your ad journey is now ready.

**Last updated (from source)**: Updated 6 months ago
