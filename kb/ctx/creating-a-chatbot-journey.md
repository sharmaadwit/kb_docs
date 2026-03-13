source_url: https://console-docs.gupshup.io/docs/creating-a-chatbot-journey

<!-- kb-golden:v7 -->
# Creating a chatbot journey

**Module**: Ctx

## Definition
Best Practices:

## Procedure
### Exact path
Gupshup Console → CTX → Creating a chatbot journey

### Where to configure it
Gupshup Console → CTX → Creating a chatbot journey

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **CTX**.
- Go to **Creating a chatbot journey**.

### Steps
1. Open Gupshup Console.
2. Go to **CTX**.
3. Go to **Creating a chatbot journey**.
4. Click on Bot Studio -> Journeys in the left hand menu.
5. Click on "+Create Journey" on the top-right corner of the screen.
6. Click on Bot Studio -> Journeys.
7. Click on "+Create Ad Journey" button on the top right corner and select "Start from scratch".
8. Click on the "Call and Return" node and this will get added in the journey. Click on the node and select the desired user journey that needs to be connected to CTWA ads.
9. Click **Save** (or **Save & Deploy**) to apply changes.

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
- CTX campaign → Bot Studio journey → Goal measurement

## Module disambiguation
- CTX covers ad-to-WhatsApp campaign flows; bot conversation logic still lives in **Bot Studio**.

## Reference (from source)
<!-- procedural:v2 -->
# Creating a chatbot journey

**Module**: Ctx

## Overview
Best Practices:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Best Practices:

- Create your base journey within Bot Studio -> User Journey
- Please make sure that the journey that needs to be run for CTWA is converted from a user journey to an ad journey. Only Ad journeys can be connected to CTWA ads
- As a best practice, run the FB preview link generated from Meta Ads Manager to check if the journey is working correctly and if the bot is portraying normal behaviour.
- (Get started by creating a user journey)
Creating the base user journey:

- Click on Bot Studio -> Journeys in the left hand menu
- Click on "+Create Journey" on the top-right corner of the screen
- In the pop-up that opens, either click on "Start from Scratch" or select a pre-existing template. Once done, the journey builder module will open.
Converting a User Journey to Ad Journey:

- Click on Bot Studio -> Journeys
- The main page lists all the User Journeys. On the user journey tab, click on the drop-down and select "Ad Journeys"
- Click on "+Create Ad Journey" button on the top right corner and select "Start from scratch"
- In the journey builder screen that opens, click on the blue dot on the right border of the starting node and select "Actions"
- Under the "Actions" tab, select "Call and Return" as the option:
- Click on the "Call and Return" node and this will get added in the journey. Click on the node and select the desired user journey that needs to be connected to CTWA ads.
- Once the journey is selected, close the node settings and click on "Save and Deploy". Your ad journey is now ready.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Once the journey is selected, close the node settings and click on "Save and Deploy". Your ad journey is now ready.

**Last updated (from source)**: Updated 6 months ago
