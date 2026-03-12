source_url: https://console-docs.gupshup.io/docs/campaign-and-ctx-ad-preview

<!-- procedural:v2 -->
# Campaign and CTX Ad Preview

**Module**: Agent Assist

## Overview
Learn how to enable Campaign Context and Ad Preview features to provide agents with valuable customer interaction context and Click to Chat ad insights.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Learn how to enable Campaign Context and Ad Preview features to provide agents with valuable customer interaction context and Click to Chat ad insights.

# Campaign and CTX Ad Preview

Enhance your agent experience with contextual customer insights through Campaign Context and Ad Preview features.

## Campaign Context

### Overview

The Campaign Context feature provides agents with visibility into the last five marketing campaigns sent to customers, offering valuable context for understanding customer conversations and interaction history.

### Benefits

- Enhanced Context: Agents can see recent marketing touchpoints
- Improved Customer Understanding: Better insight into customer journey
- Personalized Support: More informed customer interactions
### Enablement Process

To activate Campaign Context for your organization:

- Contact Support: Reach out to our support team at console-support@gupshup.io
Contact Support: Reach out to our support team at console-support@gupshup.io

- Provide Required Information: WABA number Project ID Agent Assist Brand ID
Provide Required Information:

- WABA number
- Project ID
- Agent Assist Brand ID
## Ad Preview

### Overview

The Ad Preview feature enables agents to view the specific Click to Chat (CTX) advertisement that initiated the customer's conversation, providing valuable context about the customer's entry point.

### Configuration Steps

To enable Ad Preview functionality:

- Configure CTX Ad Parameters: Set up the parameters in the Journey Builder Handover node
Configure CTX Ad Parameters: Set up the parameters in the Journey Builder Handover node

- Add Custom Attributes: In the handover node, include two custom attributes: Type: Set the value as "CTX" ID: Select "conversation_context_id" from the available variables
Add Custom Attributes: In the handover node, include two custom attributes:

- Type: Set the value as "CTX"
- ID: Select "conversation_context_id" from the available variables
- Journey Completion: Ad Preview becomes visible to agents only after the customer reaches the agent handover node in the bot journey
Journey Completion: Ad Preview becomes visible to agents only after the customer reaches the agent handover node in the bot journey

## Key Benefits

Agents gain comprehensive view of customer's marketing touchpoints and entry points

More personalized and informed customer interactions based on campaign and ad context

## Important Notes

Note: Both features require proper configuration and customer journey completion to function effectively. Ad Preview specifically requires customers to progress through the bot journey to the handover node.

These features work together to provide agents with comprehensive context, enabling them to deliver more personalized and effective customer support.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 4 months ago
