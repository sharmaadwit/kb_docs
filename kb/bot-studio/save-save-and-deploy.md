source_url: https://console-docs.gupshup.io/docs/save-save-deploy

<!-- kb-golden:v10 -->
# Save, Save & Deploy

**Module**: Bot Studio

## Definition
Use **Save** when you want to keep draft progress inside Bot Studio. Use **Save & Deploy** when you want the latest saved journey changes to go live on the connected channel.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Journey Builder → Save / Save & Deploy

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Open the target journey in **Journey Builder**.
4. While building or editing the journey, click **Save** to store draft progress in Bot Studio.
5. When you want the latest saved journey to affect the live channel, click **Save & Deploy**.
6. Run a channel test to confirm the live bot reflects the deployed change.

### Validation / where to check
- After **Save**, reopen or refresh the builder and confirm your draft changes are still present.
- After **Save & Deploy**, test on the target live channel and confirm the customer sees the updated behavior.
- If you want a draft-only check first, use **Test your Bot** before deploying.

### Troubleshooting
- If behavior is unchanged, confirm you updated the correct node and used **Save & Deploy** for live channels.
- If the wrong branch/path runs, re-check conditions, connected nodes, and fallback connectors.
- If the builder shows the latest change but the live channel does not, the most common cause is that the journey was **saved but not deployed**.

### Save / publish / deploy behavior
- **Save** stores progress in Bot Studio.
- **Save & Deploy** pushes the saved journey to the live environment/channel.
- **Save & Deploy** is required to see the latest changes in the live environment.

### Setup path
- Go to **Bot Studio**.
- Open **Journey Builder**.
- Use **Save** or **Save & Deploy** from the builder.

## Options / variants
- **Save**
- **Save & Deploy**

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Bot Studio journey → Test your Bot → Save & Deploy → live channel verification
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes in the builder; **Save & Deploy** publishes those changes to live channels.
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
