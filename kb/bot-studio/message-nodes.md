source_url: https://console-docs.gupshup.io/docs/message-nodes

<!-- kb-golden:v9 -->
# Message Nodes

**Module**: Bot Studio

## Definition
A node is a building block in the Bot Studio canvas representing a specific action, prompt, or message. Message nodes specifically are used for sending content to users, such as text, images, documents, or interactive UI elements..

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Message Nodes

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Message Nodes**.
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
- Go to **Message Nodes**.

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
# Message Nodes

**Module**: Bot Studio

## Overview
A node is a building block in the Bot Studio canvas representing a specific action, prompt, or message. Message nodes specifically are used for sending content to users, such as text, images, documents, or interactive UI elements..

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
## What is a Node?

A node is a building block in the Bot Studio canvas representing a specific action, prompt, or message. Message nodes specifically are used for sending content to users, such as text, images, documents, or interactive UI elements..

Message Nodes are the core components in Journey Builder used to send various types of content to users during a conversation. They form the foundational layer of any chatbot experience by handling the outbound messages sent by the bot.

These nodes enable the bot to communicate through a variety of media formats across supported channels (e.g., WhatsApp, Web, Instagram).

### Types of Message Nodes

- Text Node
- Image Node
- Audio Node
- Reply Node
- List Node
- Quick Reply
- Carousels
- Document
- Video Node
- Message Template
- Sticker Node
- Send Location Node

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
