source_url: https://console-docs.gupshup.io/docs/instagram-ice-breakers

<!-- kb-golden:v10 -->
# Ice Breakers

**Module**: Channels

## Definition
- Ice Breakers provide a way for users to start a conversation with a business with a list of frequently asked questions.
- Only first time users are able to view and interact with Ice Breakers.
- A maximum of 4 questions can be set as Ice Breakers.
How Ice Breakers appear on Instagram

## Procedure
### Exact UI path
Gupshup Console → Channels → Ice Breakers

### Prerequisites
- Access to the target channel configuration in Gupshup Console.
- A connected bot/app if the channel must route traffic to Bot Studio.

### Fields to configure
- as an Ice Breaker
- first question you wish
- payload for the first option
- another Ice Breaker. Click the delete icon

### Steps
1. Open Gupshup Console.
2. Go to the Instagram Settings tab.
3. Click Edit under Ice Breakers.
4. Enter the first question you wish to add as an Ice Breaker.
5. Enter payload for the first option.
6. Click Add Ice Breaker to enter another Ice Breaker. Click the delete icon to remove an Ice Breaker.
7. Click Save. Ice Breakers will now start appearing for first time users in your linked Instagram account's DM.
8. Enter Ice Breakers for that region. Click Save. The corresponding Ice Breakers will start appearing for first time users located in that region.

### Validation / where to check
- Send a live test on the target channel and confirm the bot/channel behavior matches the configuration.

### Troubleshooting
- If channel behavior is wrong, confirm the correct channel/app is connected and the latest bot configuration is live.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to the Instagram Settings tab.

## Options / variants
- Enter the first question you wish to add as an Ice Breaker.
- Enter payload for the first option.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Identify the upstream module where this is configured and the downstream module where the outcome is verified.

## Module disambiguation docs
- Channel setup governs connectivity and channel features; bot logic is configured separately in **Bot Studio**.

## Reference (from source)
<!-- procedural:v2 -->
# Ice Breakers

**Module**: Channels

## Overview
- Ice Breakers provide a way for users to start a conversation with a business with a list of frequently asked questions.
- Only first time users are able to view and interact with Ice Breakers.
- A maximum of 4 questions can be set as Ice Breakers.
How Ice Breakers appear on Instagram

## When to use
_Add the primary scenarios and personas._

## Setup path
- Go to the Instagram Settings tab.

## Step-by-step configuration
- Ice Breakers provide a way for users to start a conversation with a business with a list of frequently asked questions.
- Only first time users are able to view and interact with Ice Breakers.
- A maximum of 4 questions can be set as Ice Breakers.
How Ice Breakers appear on Instagram

## Setting Ice Breakers

- After linking your Instagram business account with Gupshup, App Settings will appear.
- Go to the Instagram Settings tab.
- Click Edit under Ice Breakers.
- Enter the first question you wish to add as an Ice Breaker.
- Enter payload for the first option.
The payload is additional data that you will receive with the selected option in the backend, mainly used for identification/differentiation purposes.

- Click Add Ice Breaker to enter another Ice Breaker. Click the delete icon to remove an Ice Breaker.
- Click Save. Ice Breakers will now start appearing for first time users in your linked Instagram account's DM.
## Adding Locales

- If you wish to have another set of Ice Breakers for a specific region, click Add Locale.
- From the Locale dropdown menu, select the region.
- Enter Ice Breakers for that region. Click Save. The corresponding Ice Breakers will start appearing for first time users located in that region.
For regions you don't specify, the default Ice Breakers set earlier will appear for first time users.

## Deleting Ice Breakers

- If you wish to delete any Ice Breaker, click the delete icon next to it and click Save.
- If you wish to delete all Ice Breakers, click Delete All at the bottom left corner of the dialog box.
Updated 10 months ago

- Autoresponders
- Persistent Menu

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Click Save. Ice Breakers will now start appearing for first time users in your linked Instagram account's DM.
- - Enter Ice Breakers for that region. Click Save. The corresponding Ice Breakers will start appearing for first time users located in that region.
- - If you wish to delete any Ice Breaker, click the delete icon next to it and click Save.
