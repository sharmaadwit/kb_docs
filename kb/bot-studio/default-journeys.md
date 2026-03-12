source_url: https://console-docs.gupshup.io/docs/default-journeys

<!-- kb-golden:v1 -->
# Default Journeys

**Module**: Bot Studio

## Definition
Each bot has three journeys by default in the User Journeys section -

## Procedure
### Where to configure it
Gupshup Console → Bot Studio → Default Journeys

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Default Journeys**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- Limitations:

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Reference (from source)
<!-- procedural:v2 -->
# Default Journeys

**Module**: Bot Studio

## Overview
Each bot has three journeys by default in the User Journeys section -

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Each bot has three journeys by default in the User Journeys section -

- Configuration Journey - Click to find more about this journey
Configuration Journey - Click to find more about this journey

- Fallback Journey -This default journey is triggered when a node fails to proceed forward based on the user input or some technical failures such as API failed to respond etc. In such cases the fallback journey gets triggered to send an invalid input message or error message. By default, the fallback journey contains a text node which can be edited or customized - Incase there is a need to sent a customized fallback message on any user inputs then the fallback connecter of the node can be linked with a Text Node and then back to the same node in order to repeat the invalid message as shown below. Incase the fallback connector is left empty then the Fallback Journey will be triggered. The fallback journey can also be customized to provide quick replies and other suggestions in order to make the conversational experience better.
Fallback Journey -This default journey is triggered when a node fails to proceed forward based on the user input or some technical failures such as API failed to respond etc. In such cases the fallback journey gets triggered to send an invalid input message or error message. By default, the fallback journey contains a text node which can be edited or customized -

Incase there is a need to sent a customized fallback message on any user inputs then the fallback connecter of the node can be linked with a Text Node and then back to the same node in order to repeat the invalid message as shown below. Incase the fallback connector is left empty then the Fallback Journey will be triggered.

The fallback journey can also be customized to provide quick replies and other suggestions in order to make the conversational experience better.

- Welcome Journey - Welcome Journey is triggered when the user input doesn't matches with any of the configured events on the start nodes of all journeys. This enables bot builders to leverage the Welcome Journey as a greeting journey for new users if they type in gibberish keywords which doesn't triggers any configured journeys. Its suggested to keep the Welcome Journey interactive in order to let the users know what all things the bot can help them with. The way how Welcome Journey differentiates from Fallback is based on the user state. Incase the user is already traversing a journey and then enters an invalid input then the Fallback Journey or Node connecter will respond. But if the user is not inside any Journey or the session(72hours) has expired from the last traversed journey then in such cases the Welcome Journey will be triggered.
Welcome Journey - Welcome Journey is triggered when the user input doesn't matches with any of the configured events on the start nodes of all journeys. This enables bot builders to leverage the Welcome Journey as a greeting journey for new users if they type in gibberish keywords which doesn't triggers any configured journeys.

Its suggested to keep the Welcome Journey interactive in order to let the users know what all things the bot can help them with.

The way how Welcome Journey differentiates from Fallback is based on the user state. Incase the user is already traversing a journey and then enters an invalid input then the Fallback Journey or Node connecter will respond. But if the user is not inside any Journey or the session(72hours) has expired from the last traversed journey then in such cases the Welcome Journey will be triggered.

Note: If the bot responds with "Welcome" for user inputs and another user journey needs to be triggered instead , please check if the intended User Journey to be triggered has the keywords configured in the start node.

### Limitations:

- The names of default journeys can not be changed or duplicated.
- Configuration Journey is view only. Please contact console-support@gupshup.io for changes in configuration journey.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
