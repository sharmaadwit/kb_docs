source_url: https://console-docs.gupshup.io/docs/creating-a-tiktok-specific-bot-journey-copy

<!-- kb-golden:v9 -->
# Creating a TikTok-specific Bot Journey

**Module**: Ctx

## Definition
Please click on the link below to download the sample json journey template for TikTok: https://drive.google.com/drive/folders/1s_p6T89yDJWNf-hN1yUx9krqgHBcVPJ9?usp=sharing

## Procedure
### Exact UI path
Gupshup Console → CTX → Creating a TikTok-specific Bot Journey

### Steps
1. Open Gupshup Console.
2. Go to "Ad Management" in the left menu under "Click to chat ads", copy it from the right corner and paste it in the code.
3. Click **Save** (or **Save & Deploy**) to apply changes.

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
- Go to "Ad Management" in the left menu under "Click to chat ads", copy it from the right corner and paste it in the code.

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
# Creating a TikTok-specific Bot Journey

**Module**: Ctx

## Overview
Please click on the link below to download the sample json journey template for TikTok: https://drive.google.com/drive/folders/1s_p6T89yDJWNf-hN1yUx9krqgHBcVPJ9?usp=sharing

## When to use
_Add the primary scenarios and personas._

## Setup path
- Go to "Ad Management" in the left menu under "Click to chat ads", copy it from the right corner and paste it in the code.

## Step-by-step configuration
# Link to download journey template

Please click on the link below to download the sample json journey template for TikTok: https://drive.google.com/drive/folders/1s_p6T89yDJWNf-hN1yUx9krqgHBcVPJ9?usp=sharing

# Creating a "user journey"

Step 1: Login to the Gupshup console

Step 2: In the left menu, click on "Bot Studio" -> Journeys

Step 3: Once on the journeys page, on the top-right corner, click on the "Import" button and upload the file downloaded from the above link. You can also rename the files (optional) as per your requirement.

Step 4: Under "User Journeys", open the imported journey.

Step 5: Click on the first node and select "user input" and in the expression choose "contains" and add "TikTok"

Step 6: In the second node, which includes the code below:

```
var_local.external_api_key = '{{ctx_external_app_id}}'

var_local.user_modified_message = 'TikTok ' + var_system.user_input.substring(var_system.user_input.indexOf(' ') + 1)
```

- In the code above, replace the CTX External App ID ONLY. To procure your app ID: Go to "Ad Management" in the left menu under "Click to chat ads", copy it from the right corner and paste it in the code.
- Go to "Ad Management" in the left menu under "Click to chat ads", copy it from the right corner and paste it in the code.
Step 7: Complete the journey basis the chatbot flow and click on "Save and Deploy"

# Converting user journey to TikTok "ad journey"

Step 1: Under "Bot Studio" -> Journeys, on the top-left under "User Journeys", there will be a drop-down.

Step 2: Click on the drop-down and select "Ad Journeys"

Step 3: If the ad journey will be imported while doing the previous journey setup, click on the journey to open it. If no ad journey is visible, click on "+Create Journey" on the right corner and choose "Start from scratch"

Step 4: Once the journey is opened, on the starting node at the right border, click on the blue dot and select "+Add"

Step 5: Choose "Actions" -> "Call and Return" and select the user journey created for TikTok from the drop-down.

Step 6: Click on "Save and Deploy"

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- Step 7: Complete the journey basis the chatbot flow and click on "Save and Deploy"
- Step 6: Click on "Save and Deploy"

**Last updated (from source)**: Updated 10 months ago
