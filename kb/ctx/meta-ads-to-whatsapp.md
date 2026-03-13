source_url: https://console-docs.gupshup.io/docs/overview

<!-- kb-golden:v9 -->
# Meta Ads to WhatsApp

**Module**: Ctx

## Definition
(Each essential step has been explained in detail in their respective subsections)

## Procedure
### Exact UI path
Gupshup Console → CTX → Meta Ads to WhatsApp

### Steps
1. Open Gupshup Console.
2. Go to **CTX**.
3. Go to **Meta Ads to WhatsApp**.
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
- Go to **Meta Ads to WhatsApp**.

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
# Meta Ads to WhatsApp

**Module**: Ctx

## Overview
(Each essential step has been explained in detail in their respective subsections)

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
(Each essential step has been explained in detail in their respective subsections)

# Essential steps to follow for successful CTWA setup

## Connect Meta Ads Manager to Gupshup Console

Access needed:

- Admin access to Facebook Business Manager (FBM)
- Access to any page owned by FBM
- Access to the ad account to run CTWA ads, owned by the FBM
## Add CTX Goals to User Journey

Best practices:

- Goal 1: Lead Best practice: Add this goal node as soon as the journey commences ie after the “Start Node”. CTX Lead goal is used to retrieve the phone number of the user.
- Goal 2: Deep Conversation Best practice: At the midpoint of the journey. For eg: If journey includes 4 user inputs, Deep Conversation to be added after the 2nd user prompt
- Goal 3: Qualified Lead Best practice: Add the goal node after the journey ends ie after the last user prompt. This helps in calculating the correct journey completion rate
## Convert User Journey to Ad Journey

## Connect CTWA Ads to Ad Journey under Click-to-chat ads module

Best Practices:

- Before clicking on “Manage Ads”, make sure the correct ad ID is being converted to a click-to-chat ad. Please compare the ad IDs before managing ads.
- As a best practice, run the FB preview link generated from Meta Ads Manager to check if the journey is working correctly and if the bot is portraying normal behaviour.
## Set-up retargeting

Best Practices:

- Please make sure that the WhatsApp template being used for retargeting does not contain any variables
- Please ensure that the option “Retarget after default free window” is left unchecked, otherwise it may incur a cost if retargeting messages are sent to users outside the 72-hour window

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 6 months ago
