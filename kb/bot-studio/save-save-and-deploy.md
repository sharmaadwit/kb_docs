source_url: https://console-docs.gupshup.io/docs/save-save-deploy

<!-- kb-golden:v9 -->
# Save, Save & Deploy

**Module**: Bot Studio

## Definition
Assuming a journey is to be made which is complex to design and has a lot of nodes involved. You are done with designing a small part of the flow for instance say 10% of the complete. It is advised to save the progress done so far. For this purpose, you get a ‘Save’ button on the Bot Studio itself.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Save, Save & Deploy

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Save, Save & Deploy**.
4. Save & Deploy is a mandatory step to see all the changes done, in the live environment.

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
- Go to **Bot Studio**.
- Go to **Save, Save & Deploy**.

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Save, Save & Deploy

**Module**: Bot Studio

## Overview
Assuming a journey is to be made which is complex to design and has a lot of nodes involved. You are done with designing a small part of the flow for instance say 10% of the complete. It is advised to save the progress done so far. For this purpose, you get a ‘Save’ button on the Bot Studio itself.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### Save Button

Assuming a journey is to be made which is complex to design and has a lot of nodes involved. You are done with designing a small part of the flow for instance say 10% of the complete. It is advised to save the progress done so far. For this purpose, you get a ‘Save’ button on the Bot Studio itself.

A click on the Save button performs an action in the backend and saves the entire progress. You can keep your progress saved at regular intervals to avoid any loss of effort.

### Save & Deploy

Alright, so once we are done with the journey building and ready with our chatbot to be seen in action, we need to host the chatbot on any channel.

The Save & Deploy button allows you to host the chatbot on any channel and see the chatbot in action. Deploy action pushes all the details saved on Bot Studio to live.

Save & Deploy is a mandatory step to see all the changes done, in the live environment.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- ### Save Button
- A click on the Save button performs an action in the backend and saves the entire progress. You can keep your progress saved at regular intervals to avoid any loss of effort.
- ### Save & Deploy
- The Save & Deploy button allows you to host the chatbot on any channel and see the chatbot in action. Deploy action pushes all the details saved on Bot Studio to live.
- Save & Deploy is a mandatory step to see all the changes done, in the live environment.

**Last updated (from source)**: Updated 10 months ago
