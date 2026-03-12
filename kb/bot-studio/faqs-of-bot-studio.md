source_url: https://console-docs.gupshup.io/docs/faqs-of-bot-studio

<!-- kb-golden:v4 -->
# FAQs of Bot Studio

**Module**: Bot Studio

## Definition
Question: How to access Bot Studio?

## Procedure
### Exact path
Gupshup Console → Bot Studio → FAQs of Bot Studio

### Where to configure it
Gupshup Console → Bot Studio → FAQs of Bot Studio

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → FAQs of Bot Studio**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# FAQs of Bot Studio

**Module**: Bot Studio

## Overview
Question: How to access Bot Studio?

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Question: How to access Bot Studio?

Response: Drop an Email to the Console / Bot Builder team.

Provide the following information in the Email:

- WhatsApp account details
- Instagram account details
- Agent Assist required (Yes/No)
The bot Builder team will create an account for the above-requested details and login credentials of the unified console will be shared within 2 working days.

Question: How to create a chatbot on Bot Studio?

Response: Open Bot Studio, and create a journey using nodes, prompts, and action present in the Action and Prompts menu. Nodes can be added by clicking on the Add button on the connector or on the node as well.

Question: How to trigger a chatbot journey?

Response: To trigger/start a chatbot journey, set a trigger on the condition node in the configuration journey. The chatbot gets started as per the set trigger. For Instance: "Hello" is a trigger set on the condition node, as the trigger is added, a connector on the condition node appears, a call and return node having a particular journey can be added or a new journey can be created on the configuration journey as well.

Questions: How to jump from one journey to another?

Response: Use a Call and Return node to Jump from one Journey to another. On using the Call and Return node, the transfer is shifted from the ongoing journey to the called journey. Once the called journey is completely executed, the control is shifted back to the main journey.

Question: How to save and deploy a chatbot journey?

Response: Once a journey is created, you can save the journey/progress by clicking on the save button on the top right corner of the Bot Studio screen. A success message pops up on the screen once the journey is saved.

Question: How to create and manage APIs?

Response: APIs can be created on the Manage API screen. APIs can be created or a postman collection can be imported. Both options are provided on the screen.

Manage API can be accessed from the following places:

- Action and prompts menu lower end.
- On the canvas when the Action and Prompt menu is closed.
- On the API node.
Question: How to create and manage variables?

Response: Variables can be created on the Manage Variable screen. To create a variable, a variable name, data type and default value (optional) are to be provided. Once the variable is created, it can be used as per the requirement.

Manage Variables screen can be accessed from the following places:

- Action and prompts menu lower end.
- On the canvas when the Action and Prompt menu is closed.
- On the edit screen (left panel) of nodes where the user response can be stored in a variable.
NOTE: A variable created can't be edited or deleted except the default value. A new variable is to be created if there is any change required in a variable.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- Question: How to save and deploy a chatbot journey?

**Last updated (from source)**: Updated 10 months ago
