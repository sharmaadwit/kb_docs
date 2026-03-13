source_url: https://console-docs.gupshup.io/docs/ctx-goal-nodes-adding-to-the-journey

<!-- kb-golden:v7 -->
# CTX Goal Nodes and Conversions API: Adding to the journey

**Module**: Ctx

## Definition
CTX Goals are added to track the number of leads that have come in the bot journey and is a milestone-based approach to get drop-offs in the journey

## Procedure
### Exact path
Gupshup Console → CTX → CTX Goal Nodes and Conversions API: Adding to the journey

### Where to configure it
Gupshup Console → CTX → CTX Goal Nodes and Conversions API: Adding to the journey

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **CTX**.
- Go to **CTX Goal Nodes and Conversions API: Adding to the journey**.

### Steps
1. Open Gupshup Console.
2. Go to **CTX**.
3. Go to **CTX Goal Nodes and Conversions API: Adding to the journey**.
4. Add the following API: curl --location --request POST 'https://ctx-be.gupshup.io/external/facebook/capi/events' \ --header 'externalApiKey: EXTERNAL_API_KEY' \ //EXTERNAL_API_KEY is a variable and needs to be filled --header 'Content-Type: application/json' \ --data-raw '{ "user_channel_id" : {{var_system.user_channel_id}}, "ad_id" : "{{var_system.conversation_context_id}}", "event_name" : "LeadSubmitted" }'.
5. Add the following API:.
6. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- In the API screen, click on the toggle and select "Curl"

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- CTX campaign → Bot Studio journey → Goal measurement

## Module disambiguation
- CTX covers ad-to-WhatsApp campaign flows; bot conversation logic still lives in **Bot Studio**.

## Reference (from source)
<!-- procedural:v2 -->
# CTX Goal Nodes and Conversions API: Adding to the journey

**Module**: Ctx

## Overview
CTX Goals are added to track the number of leads that have come in the bot journey and is a milestone-based approach to get drop-offs in the journey

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
## Objectives of CTX Goals:

CTX Goals are added to track the number of leads that have come in the bot journey and is a milestone-based approach to get drop-offs in the journey

Goal 1: Lead Best practice: Add this goal node as soon as the journey commences ie after the “Starting Node”. CTX Lead goal is used to retrieve the phone number of the user.

Goal 2: Deep Conversation Best practice: At the midpoint of the journey. For eg: If journey includes 4 user inputs, Deep Conversation to be added after the 2nd user prompt

Goal 3: Qualified Lead Best practice: Add the goal node after the journey ends ie after the last user prompt. This helps in calculating the correct journey completion rate

## Adding CTX Goals in the journey

Best Practice and Disclaimer: CTX Goals are automatically created when the client onboards their Meta Ads Account to Ad Management. Please DO NOT create CTX goals manually.

Step 1: Click on the “Add” button on the connecting thread between the two nodes. This button pops-up as soon as you hover on the blue thread using the cursor

Step 2: In the list that opens, select Action > Goal

Step 3: Once the goal is added, click on the goal node to open the pop-up shown on the right hand side of the screenshot above

Step 4: In the pop-up, add the information as shown in the screenshot above:

Step 5: You can now repeat the mentioned steps in the previous slides to similarly add the following other CTX Goals:

- Deep Conversation
- Qualified Lead
## Adding Conversion API Node to the Ad Journey

- Open the ad journey that was created corresponding to the user journey under Bot Studio -> Journeys -> Ad Journey
Open the ad journey that was created corresponding to the user journey under Bot Studio -> Journeys -> Ad Journey

- After the starting node, under Actions, select API
After the starting node, under Actions, select API

- In the API node, click on "+Add new API"
In the API node, click on "+Add new API"

- In the API screen, click on the toggle and select "Curl"
In the API screen, click on the toggle and select "Curl"

- Add the following API: curl --location --request POST 'https://ctx-be.gupshup.io/external/facebook/capi/events' \ --header 'externalApiKey: EXTERNAL_API_KEY' \ //EXTERNAL_API_KEY is a variable and needs to be filled --header 'Content-Type: application/json' \ --data-raw '{ "user_channel_id" : {{var_system.user_channel_id}}, "ad_id" : "{{var_system.conversation_context_id}}", "event_name" : "LeadSubmitted" }'
Add the following API:

```
curl --location --request POST 'https://ctx-be.gupshup.io/external/facebook/capi/events' \
          --header 'externalApiKey: EXTERNAL_API_KEY' \ //EXTERNAL_API_KEY is a variable and needs to be filled
          --header 'Content-Type: application/json' \
          --data-raw '{
              "user_channel_id" : {{var_system.user_channel_id}},
              "ad_id" : "{{var_system.conversation_context_id}}",
              "event_name" : "LeadSubmitted"
          }'
```

- Once the above API is added, Curl will be populated like this:
Once the above API is added, Curl will be populated like this:

- In the above code in the API builder Curl, replace the text "EXTERNAL_API_KEY" with the key of the project. This can be retrieved, as shown in the screenshot below:
In the above code in the API builder Curl, replace the text "EXTERNAL_API_KEY" with the key of the project. This can be retrieved, as shown in the screenshot below:

- Once the External API key is replaced, the curl will look like this:
Once the External API key is replaced, the curl will look like this:

- Once done, close the API window with the X mark and choose the API from the dropdown in the API node that was just created. CAPI has now been successfully configured.
Once done, close the API window with the X mark and choose the API from the dropdown in the API node that was just created. CAPI has now been successfully configured.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 6 months ago
