source_url: https://console-docs.gupshup.io/docs/test-your-bot

<!-- kb-golden:v4 -->
# Test your Bot

**Module**: Bot Studio

## Definition
Now you can Test your Bot on-the-go without the need to connect to Proxy or Webapp on different tabs.

## Procedure
### Exact path
Gupshup Console → Bot Studio → Test your Bot

### Where to configure it
Gupshup Console → Bot Studio → Test your Bot

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Test your Bot**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- # Test your Bot
- Now you can Test your Bot on-the-go without the need to connect to Proxy or Webapp on different tabs.

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
# Test your Bot

**Module**: Bot Studio

## Overview
Now you can Test your Bot on-the-go without the need to connect to Proxy or Webapp on different tabs.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Now you can Test your Bot on-the-go without the need to connect to Proxy or Webapp on different tabs.

Overview

Journey Builder is equipped with a Test Bot functionality to help you Test and Debug your Bot while you build it on console. Test Bot feature is available for all console projects and can be found on the right top of the journey listing page in Bot Studio > Journeys.

You can use the widget to send messages and initiate a conversation using the configured trigger inputs on the Starting Node of the created journeys.

Test Bot feature is also equipped with a message log button across each user message on the Bot widget which will help to identify any errors or bugs in the bot design. This will incrementally reduce the efforts to debug a bot or fix issues without requiring a need to reach out to support. The message log is available for every user message only where it renders the payload generated after the user message is sent.

Message Log

Message Log consists of two sections viz. Basic Info and Payload. These two sections helps a Bot Designer or a Bot Dev to view detailed info of the Journeys and Nodes executed after the user message is sent.

- Basic Info : This section contains the information in a structured manner showing the execution of each node inside a journey once a user message is sent. The tabs inside the Basic Info can be expanded to view more about about the execution of the node and the variables that were updated during the process.
Basic Info : This section contains the information in a structured manner showing the execution of each node inside a journey once a user message is sent. The tabs inside the Basic Info can be expanded to view more about about the execution of the node and the variables that were updated during the process.

- Payload : Payload Section will contain the backend JSON Payload that got generated post a user message is sent. The payload can also be copied to view separately.
Payload : Payload Section will contain the backend JSON Payload that got generated post a user message is sent. The payload can also be copied to view separately.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
