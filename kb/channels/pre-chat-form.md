source_url: https://console-docs.gupshup.io/docs/web-pre-chat-form

<!-- kb-golden:v10 -->
# Pre-Chat Form

**Module**: Channels

## Definition
- The Pre-Chat Form appears as the first thing users see on the chat widget after clicking the widget icon.
- Users must submit the Pre-Chat Form before they can start messaging on the chat widget.
- The form will help you get consent from new users on your terms and conditions or privacy policy before starting a chat.
- If the Retain Customer Chat History setting is enabled, the Pre-Chat Form will be shown to new anonymous users only once. Logged in users will be shown the form every time regardless of the setting.

## Procedure
### Exact UI path
Gupshup Console → Channels → Pre-Chat Form

### Prerequisites
- Access to the target channel configuration in Gupshup Console.
- A connected bot/app if the channel must route traffic to Bot Studio.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to the Pre-Chat Form tab in Settings of the Web channel.
3. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Send a live test on the target channel and confirm the bot/channel behavior matches the configuration.

### Troubleshooting
- Users cannot start messaging on the chat widget without clicking the Global Button.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to the Pre-Chat Form tab in Settings of the Web channel.

## Options / variants
- Turn on the Enable Pre-Chat Form toggle. You can now add the content to the form.

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
# Pre-Chat Form

**Module**: Channels

## Overview
- The Pre-Chat Form appears as the first thing users see on the chat widget after clicking the widget icon.
- Users must submit the Pre-Chat Form before they can start messaging on the chat widget.
- The form will help you get consent from new users on your terms and conditions or privacy policy before starting a chat.
- If the Retain Customer Chat History setting is enabled, the Pre-Chat Form will be shown to new anonymous users only once. Logged in users will be shown the form every time regardless of the setting.
## Setting the Pre-Chat Form

## When to use
_Add the primary scenarios and personas._

## Setup path
- Go to the Pre-Chat Form tab in Settings of the Web channel.

## Step-by-step configuration
- The Pre-Chat Form appears as the first thing users see on the chat widget after clicking the widget icon.
- Users must submit the Pre-Chat Form before they can start messaging on the chat widget.
- The form will help you get consent from new users on your terms and conditions or privacy policy before starting a chat.
- If the Retain Customer Chat History setting is enabled, the Pre-Chat Form will be shown to new anonymous users only once. Logged in users will be shown the form every time regardless of the setting.
## Setting the Pre-Chat Form

- Go to the Pre-Chat Form tab in Settings of the Web channel.
- Turn on the Enable Pre-Chat Form toggle. You can now add the content to the form.
### Header Image

- The Header Image appears at the top of the Pre-Chat Form. Uploading an image is optional.
- Uploading an image is optional.
- The uploaded image should jpeg, jpg or png and its maximum size can be 8 MB.
### Header

- The Header text appears just below the image (if added) or at the top of the form. Entering the Header text is mandatory.
- Entering the Header text is mandatory.
- It is always formatted as bold and is aligned horizontally to the center of the form.
- The maximum number of characters in the Header text is 100.
### Sub-Header

- The Sub-Header text appears just below the Header. Entering the Sub-Header text is optional.
- Entering the Sub-Header text is optional.
- The maximum number of characters in the Sub-Header text is 1000.
### Checkbox Text

- The Checkbox Text appears to the right of the checkbox located above the Global Button at the bottom of the form.
- It has 3 components: Preliminary Text appears as the normal text at the beginning of the Checkbox Text. The maximum number of characters in the Preliminary Text is 100. Hyperlinked Text appears as the hyperlinked text formatted in blue at the end of the Checkbox Text. The maximum number of characters in the Hyperlinked Text is 100. URL for Hyperlinked Text is the link to which the users are redirected when they click on the Hyperlinked Text. Entering the URL is optional.
- Preliminary Text appears as the normal text at the beginning of the Checkbox Text. The maximum number of characters in the Preliminary Text is 100.
- The maximum number of characters in the Preliminary Text is 100.
- Hyperlinked Text appears as the hyperlinked text formatted in blue at the end of the Checkbox Text. The maximum number of characters in the Hyperlinked Text is 100.
- The maximum number of characters in the Hyperlinked Text is 100.
- URL for Hyperlinked Text is the link to which the users are redirected when they click on the Hyperlinked Text. Entering the URL is optional.
- Entering the URL is optional.
### Global Button Text

- The Global Button appears at the bottom of the Pre-Chat Form.
- Users cannot start messaging on the chat widget without clicking the Global Button.
- If the checkbox is not ticked, the Global Button remains in a disabled state.
- The maximum number of characters in the Global Button text is 100.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Users must submit the Pre-Chat Form before they can start messaging on the chat widget.

**Last updated (from source)**: Updated 10 months ago
