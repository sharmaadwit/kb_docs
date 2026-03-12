source_url: https://console-docs.gupshup.io/docs/journey-settings

<!-- procedural:v2 -->
# Journey Settings

**Module**: Bot Studio

## Overview
Every User Journey has a dedicated settings which determines how the journey will be used by the bot. Journey Settings can be found inside the Design Canvas along with the Manage Variable and API Management options.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Every User Journey has a dedicated settings which determines how the journey will be used by the bot. Journey Settings can be found inside the Design Canvas along with the Manage Variable and API Management options.

An upgraded Journey Settings is being introduced with new options to select the Primary Intent, Journey Workspace and Excluded Intent.

- AI Model: There are 2 types of AI models available for the Journey
- Global AI Model - Selecting this model will allow the end user to switch to another journey based on user’s input unless an excluded Intent has been detected in the user utterance
### For example:

Assume that the user is currently on a Product Search Journey and the user types in a different question which is not related to the Product Search journey viz. "Contact Support" or "Talk to customer care".

In these cases, if the bot has a trained intent with the users intent("Contact Support") and has a journey associated with it then that journey will get triggered leaving the Product Search Journey midway.

This behavior can also be modified as per requirement using the Sticky Journeys concept which is discussed later part of this doc.

- Uninterrupted Model - Selecting this model will not allow the end user to switch to another journey based on user’s input unless an excluded Intent has been detected in the user utterance
For Example:

Uninterrupted Model can be used for transactional like journeys where the user is expected to complete the journey in a structured manner to ensure that the payment authentication is done within the authentication expiry time. In case where the user wants to cancel the journey the Bot Designer can keep an Excluded Intent ( cancel as shown above) which can be triggered by the user's intent. The bot designer can let the end user know on the keyword to enter incase the user wishes to cancel the payment process throughout the flow.

- Primary Intent:
- The primary intent of an AI journey is the current intent of the respective journey for the end user. The primary intent would enable the end user to resume the current journey when no Intent is detected for the user utterance
- It is selected from a dropdown menu in the Journey Settings that includes only the values of the chosen intent in the Start Trigger Node of the journey.
- Only 1 intent can be chosen as the primary intent for each journey. The workspace associated with the chosen primary intent becomes the Journey Workspace.
- Journey Workspace:
- The Journey Workspace is the workspace associated with the primary intent selected in the Journey Settings of respective journey
- The Journey Workspace option is read-only and auto-populated based on the selected primary intent
- If the primary intent is being changed, the corresponding workspace of the intents becomes the Journey workspace
- Excluded Intent:
- The excluded intent allows the end user to switch to a different journey when triggered from the current Journey in an Uninterrupted Model
- Only 1 Intent can be chosen as “Excluded Intent” of the Journey
- Excluded Intents are the list of the Intents from the Journey Workspace and is an optional parameter to be selected when selected AI Model is Uninterrupted Model
- Excluded intents display the intent name in the dropdown. Switching the primary intent does not clear the excluded intent or its associated settings, provided both intents belong to the same workspace
## Sticky Journeys:

Sticky Journeys is an available optional configuration for all User Journeys which allows bot designers the flexibility to make the end users complete the existing journey incase the users wishes to ask contextual questions in between the flow or subconsciously diverts from the existing flow.

### This configuration needs to be used with a bit of caution to ensure that the end user experience is not affected.

How does it work?

Sticky journey converts all the existing and new Prompt nodes to Persistent nodes so that the user comes back to the last persistent prompt node available on the Journey which is marked as sticky.

The Bot designer have to ensure that they add the prompt nodes at points where the user is expected to provide an input and can enter something unrelated to the expected input which can divert the user to a different flow. If Sticky Journey is enabled and there are prompt nodes also added, then if the user gets diverted to a different journey halfway through the parent journey then once the new journey is complete then the user will come back to the previous journey at the point of last traversed prompt node.

The below representation helps you to understand it better:

Backend/Bot Level Changes associated with Sticky Journeys:

- All Prompt nodes are converted to persistent node. This means that the persistent nodes expects a related input and if the user switches the intent before answering the prompt node question then the node will wait for the user to comeback after completing the new intent related journey.
- Bot Designers can uncheck the checkbox on Prompt Node which should not be persistent. In such cases the user will land to the previous Persistent prompt node available on the parent journey
- Incase there are not Persistent Prompt Node available on the flow then the user will be sent to the very beginning of the Sticky Journey i.e. the node right after the Starting node.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
