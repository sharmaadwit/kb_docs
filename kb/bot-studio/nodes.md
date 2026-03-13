source_url: https://console-docs.gupshup.io/docs/nodes-1

<!-- kb-golden:v9 -->
# Nodes

**Module**: Bot Studio

## Definition
Bot Studio has the capability of allowing users to design customised customer journeys and automate the conversation by using nodes.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Nodes

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Nodes**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

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
- Go to **Nodes**.

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
# Nodes

**Module**: Bot Studio

## Overview
Bot Studio has the capability of allowing users to design customised customer journeys and automate the conversation by using nodes.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Bot Studio has the capability of allowing users to design customised customer journeys and automate the conversation by using nodes.

There are the following types of Nodes on Bot Studio:

- Message Node
- Prompts Node
- Action Nodes
### Node Features across all Journeys

### Starting Node :

A Common Node that marks the start of each User Journey.

In User Journeys, define the keywords that trigger this journey in the start node. When the journey is saved and deployed, the triggers will be updated in Keyword Trigger Node of the view-only configuration journey.

On Save and Deploy of each journey, the changes will reflect in Keyword Trigger Node of default Configuration Journey.

Read moreon how to trigger User Journeys.

Channel based Filter: Journey Builder Canvas provides Nodes that can be used across all channels. Filter the Nodes based on channels on the left-side Node Panel to view nodes that are applicable to that channel.

Whatsapp, Instagram and Web Channel Nodes

Node Names: Each node in all journeys can be given unique Node Names.

Node Name Limitations:

- Each Node name should be alphanumerical.
- Specials characters allowed - Space, Underscore, Hyphen
- They should be unique within a journey
- 50 Characters are allowed
Inline Analytics - Beta: Check out the inline analytics for each node and connector available in a journey. Once a journey is deployed, inline analytics toggle can be switched on or refreshed to view the following-

- Node analytics - Traversed - View the number of times the node has been traversed in run-time Exits - View the number of times customers dropped off when they reached the node
- Traversed - View the number of times the node has been traversed in run-time
- Exits - View the number of times customers dropped off when they reached the node
- Connector analytics - Traversals - View the number of times a connector was traversed at runtime
- Traversals - View the number of times a connector was traversed at runtime

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- On Save and Deploy of each journey, the changes will reflect in Keyword Trigger Node of default Configuration Journey.

**Last updated (from source)**: Updated 10 months ago
