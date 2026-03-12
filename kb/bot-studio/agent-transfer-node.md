source_url: https://console-docs.gupshup.io/docs/agent-transfer-node

<!-- kb-golden:v4 -->
# Agent Transfer Node

**Module**: Bot Studio

## Definition
This node is to enable or allow customers to connect with a human agent in the below cases:

## Procedure
### Exact path
Gupshup Console → Bot Studio → Agent Transfer Node

### Where to configure it
Gupshup Console → Bot Studio → Agent Transfer Node

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Agent Transfer Node**.
3. Configure the required fields.
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
# Agent Transfer Node

**Module**: Bot Studio

## Overview
This node is to enable or allow customers to connect with a human agent in the below cases:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
This node is to enable or allow customers to connect with a human agent in the below cases:

- Bot failure.
- The user opted to connect with the agent.
Agent handover node is to support the chatbot in case there is any complex query that is not covered in either structured journey or not trained on the chatbot or there is a need for a customer to connect with an agent.

### When to use

Businesses can provide an option to connect with the agent if they have a need for customers to connect with an agent. For instance: For post-sales support, the customer wants to connect with an agent to file grievances regarding a product that they purchased and needs to connect with an agent to file it.

### How to use

The agent handover node is available on the Action & Prompts menu and can be dragged and dropped on the canvas for use.

Customise the default message that the customer will receive on the channel while the chat is being transferred to agent.

In some cases, there are specialised agent teams that handle a specific type of query from the users. For example, within the agent services, one team might handle "support services" while the other handles "sales assistance queries".

To handle this case, the agent dashboard settings allow the business to route chats based on chat rules. One way to configure chat rules is by using tags. Check the "Agent Assist" Dashboard to learn more about designing chat rules.

After tags are added in the agent dashboard settings, they can be used in the bot studio's agent transfer node to transfer chat to specialised agents.

Tags in Agent Dashboard Settings

Using Tags in Agent Transfer Node

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
