source_url: https://console-docs.gupshup.io/docs/test-bot-widget-on-jb-canvas

<!-- procedural:v2 -->
# Test Bot Widget on JB Canvas

**Module**: Bot Studio

## Overview
Test bot widget is an existing feature on the Journey List page which lets Bot designers to test the bot or go through the Message logs to debug any issue on the bot. Now Bot designer will be able to Test, debug, fix, and deploy all at a single place.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### Introduction

Test bot widget is an existing feature on the Journey List page which lets Bot designers to test the bot or go through the Message logs to debug any issue on the bot. Now Bot designer will be able to Test, debug, fix, and deploy all at a single place.

### What's New?

- Dedicated Widget “ Test Bot” for the Deployed Bot where in, the user can view the message logs to test, debug and fix the Journey flow
- Bot Designer can view the basic node type information and payload on click of the message icon
- Bot Designer can also view the list of updated variables wherein the Journey information is stored
This feature has now been extended to the individual Journey Canvas as well making it more useful and easier for bot designers to Test the Bot without requiring to come back to the journey listing page.

Additionally, the Test Bot in Journey Builder canvas automatically retrieves the User Input text (if configured on the Starting Node) from the open journey and fills it in the Bot input text box for quicker journey execution.

### Note:

If there is no User input text added on the Starting Node of the Journey then no pre-fill action would be done and the designer has to trigger the journey with the required input. Eg. If the Starting Node is configured with an AI Trigger Intent then the designer has to type the utterance which can trigger the intent and invoke the journey.

### If Customer Chat History Retention is enabled, message logs will not be retained for messages from previous conversations.

Following actions result in new Test Bot conversations and message logs will not be available for all messages sent before the action:

- Closing and reopening the Journey Listing or Journey Canvas web page
- Refreshing or reloading the Journey Listing or Journey Canvas web page

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
