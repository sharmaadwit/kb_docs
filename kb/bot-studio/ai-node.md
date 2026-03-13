source_url: https://console-docs.gupshup.io/docs/ai-node

<!-- kb-golden:v7 -->
# AI Node

**Module**: Bot Studio

## Definition
The AI Node is used to link journeys with trained workspaces created in the AI Admin in Bot Studio. For instance, if businesses want to answer customer FAQs, bot designer can train the data workspace with relevant FAQ related data sources and use the AI Node to link the journey with the same data workspace. When a user interacts with the bot at run-time, user can ask the query and the AI enabled journey provides the best relevant answer to the user.

## Procedure
### Exact path
Gupshup Console → Bot Studio → AI Node

### Where to configure it
Gupshup Console → Bot Studio → AI Node

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **AI Node**.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **AI Node**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- How to use

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
# AI Node

**Module**: Bot Studio

## Overview
The AI Node is used to link journeys with trained workspaces created in the AI Admin in Bot Studio. For instance, if businesses want to answer customer FAQs, bot designer can train the data workspace with relevant FAQ related data sources and use the AI Node to link the journey with the same data workspace. When a user interacts with the bot at run-time, user can ask the query and the AI enabled journey provides the best relevant answer to the user.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### When to use

The AI Node is used to link journeys with trained workspaces created in the AI Admin in Bot Studio. For instance, if businesses want to answer customer FAQs, bot designer can train the data workspace with relevant FAQ related data sources and use the AI Node to link the journey with the same data workspace. When a user interacts with the bot at run-time, user can ask the query and the AI enabled journey provides the best relevant answer to the user.

Currently, bot designer can use AI Node in journeys to automate -

- Generic queries of customers such as FAQs for the business
- Commerce use cases such as queries on product catalogues of the business
### How to use

Drag and drop the AI Node from the Node Panel to the canvas.

- The enhanced "AI Node" allows selection of successfully trained workspaces.
- Selection of a Generic workspace results in pre-filled “FAQ” intent as a read-only option.
- Selection of a commerce workspace pre-filled “Product Search, Q&A” as a read-only option.
- Users can opt for individual content tags or select all associated tags by choosing the "All" option
- User can differentiate the subsequent experience based on the content tag detected by using a System variable; {{var_system.ai_inference_payload.faq_response[0].categories[0]}} in a text node. A sample is attached below. Bot designer can use other message nodes to provide the response to customers.
```
{{var_local.VariableUsed.output[0].faq_response[0].message}} //Can be used to send text to users
```

### Limitations

- This node is available only when AI is enabled in the recipe.
- Data workspace that are created and trained successfully in the AI Admin Module are visible in the dropdown to select data workspace.
- Response can be stored in JSON Variable only.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
