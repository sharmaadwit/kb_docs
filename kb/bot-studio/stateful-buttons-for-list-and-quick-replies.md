source_url: https://console-docs.gupshup.io/docs/stateful-buttons-for-static-button-based-nodes

<!-- kb-golden:v10 -->
# Stateful Buttons for List and Quick Replies

**Module**: Bot Studio

## Definition
Journey Builder features a variety of button-based nodes designed to send Quick Reply or Multiple radio button-based list messages across WhatsApp and other channels. These nodes have been upgraded to maintain their state along with the configured action, even after traversal and progression in the conversation when users select alternative buttons or inputs.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Stateful Buttons for List and Quick Replies

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Stateful Buttons for List and Quick Replies**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run the flow in **Test your Bot** and confirm the expected node/path executes.
- If the change must affect live traffic, use **Save & Deploy** and verify on the target channel.

### Troubleshooting
- If behavior is unchanged, confirm you updated the correct node and used **Save & Deploy** for live channels.
- If the wrong branch/path runs, re-check conditions, connected nodes, and fallback connectors.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Bot Studio**.
- Go to **Stateful Buttons for List and Quick Replies**.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Stateful Buttons for List and Quick Replies

**Module**: Bot Studio

## Overview
Journey Builder features a variety of button-based nodes designed to send Quick Reply or Multiple radio button-based list messages across WhatsApp and other channels. These nodes have been upgraded to maintain their state along with the configured action, even after traversal and progression in the conversation when users select alternative buttons or inputs.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### Overview:

Journey Builder features a variety of button-based nodes designed to send Quick Reply or Multiple radio button-based list messages across WhatsApp and other channels. These nodes have been upgraded to maintain their state along with the configured action, even after traversal and progression in the conversation when users select alternative buttons or inputs.

### Key Features:

State Retention: The enhanced button nodes now preserve their state, ensuring continuity in the conversation flow. Users can seamlessly navigate the conversation history on WhatsApp and select different buttons or list items while still proceeding along the configured path within Journey Builder.

Improved User Experience: With stateful buttons, users can interact with various options within the conversation without losing context or disrupting the journey's intended progression. This feature enhances user engagement and facilitates smoother interactions across channels.

Note: Ensure proper configuration of stateful buttons to leverage this enhanced functionality

### What's New!

- Additional Configuration available on List, Reply Button and Quick Reply Nodes to make a Button stateful
- Stateful Buttons retains its context till its clickable from the channel side
- Stateful buttons allow users to change the current context and start a fresh journey while in uninterrupted model. For Global Model the previous journey context will be retained
- Designers can enable multiple stateful button for a single node
- Support of Additional Payload to pass user context/info to the stateful journey(requires variable from the stateful journey to be mapped to the parent journey)
### How to use Stateful Buttons ?

Let's take a use case where the user will be greeted with a welcome message and some Menu options to choose from whenever a message is sent to the bot. One of the options provided is to Talk to an Agent which the user should be able to initiate at any point during the bot conversation.

Journey creation steps:

- The bot designer is responsible for creating the journey in which the "Talk to Agent" button will be integrated.
- It is essential to link a stateful button to a journey. Therefore, the journey must be created prior to configuring the stateful button node.
- For Quick Reply and List nodes, ensure that the nodes are set to multi-connector mode to enable support for stateful features.
- In the Menu journey, designers can utilize Quick Reply, List or Reply buttons and designate one or more buttons as Stateful. This button should then be linked to the Agent Journey, as illustrated below.
- Designers can include user context or information in the Additional Payload and subsequently retrieve this data through a variable in the stateful journey
- Make sure that the variable is created on the Stateful journey in order to map it in the parent journey
- Once configured as described in the preceding steps, the bot can be deployed. Subsequently, the button will retain its stateful context, allowing seamless user interaction even if alternative selections are made during the journey initiation process.
In the image above, the user first selected the "Check order status" option and then chose the "Talk to Agent" option from the same Quick Reply. As the button was stateful, it initiated the journey associated with it.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
