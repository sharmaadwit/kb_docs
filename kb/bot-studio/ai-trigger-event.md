source_url: https://console-docs.gupshup.io/docs/ai-trigger

<!-- kb-golden:v1 -->
# AI Trigger Event

**Module**: Bot Studio

## Definition
AI Trigger(available with AI Recipe only): This event is selected when there are intents trained in the AI Admin and the journey should be triggered when a specific intent is detected. AI Trigger is the most efficient and dynamic way of triggering journeys as it can retain the context of the intent and the entities mentioned on the user input sentence/keyword. AI Trigger has few additional configurations which are as follows:

## Procedure
### Where to configure it
Gupshup Console → Bot Studio → AI Trigger Event

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → AI Trigger Event**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Reference (from source)
<!-- procedural:v2 -->
# AI Trigger Event

**Module**: Bot Studio

## Overview
AI Trigger(available with AI Recipe only): This event is selected when there are intents trained in the AI Admin and the journey should be triggered when a specific intent is detected. AI Trigger is the most efficient and dynamic way of triggering journeys as it can retain the context of the intent and the entities mentioned on the user input sentence/keyword. AI Trigger has few additional configurations which are as follows:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
AI Trigger(available with AI Recipe only): This event is selected when there are intents trained in the AI Admin and the journey should be triggered when a specific intent is detected. AI Trigger is the most efficient and dynamic way of triggering journeys as it can retain the context of the intent and the entities mentioned on the user input sentence/keyword. AI Trigger has few additional configurations which are as follows:

- Intents: Intents are trained on the AI Admin Model and can be used for triggering journeys based on that. You can customize your intent based on the domain and the LLM model will create utterances based on the description in order to provide a preview of the type of utterance that the Intent can detect. Local/Global Entities: You can create Intent Based Entities or Global Level Entities to have more information captured from the user's message and use them in the journey. Example for a user input like "Book a flight from Mumbai to Brazil for 25th of Dec" have multiple entities like the source and destination along with the date for which the user wanted to book the ticket. These entities will be detected if there are Local Entities mapped with the intent and can be tightly coupled with a variable to update the variable value and use it later.\ Entity<>Variable mappings are tightly coupled and any update on the value of entity or variable will update the other as well.
- Intents: Intents are trained on the AI Admin Model and can be used for triggering journeys based on that. You can customize your intent based on the domain and the LLM model will create utterances based on the description in order to provide a preview of the type of utterance that the Intent can detect.
- Local/Global Entities: You can create Intent Based Entities or Global Level Entities to have more information captured from the user's message and use them in the journey. Example for a user input like "Book a flight from Mumbai to Brazil for 25th of Dec" have multiple entities like the source and destination along with the date for which the user wanted to book the ticket. These entities will be detected if there are Local Entities mapped with the intent and can be tightly coupled with a variable to update the variable value and use it later.\ Entity<>Variable mappings are tightly coupled and any update on the value of entity or variable will update the other as well.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
