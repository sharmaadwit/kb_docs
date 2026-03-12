source_url: https://console-docs.gupshup.io/docs/quick-reply

<!-- procedural:v2 -->
# Quick Reply

**Module**: Bot Studio

## Overview
It is a special type of message using which a chatbot can provide multiple options for a customer to select. It is a message type with a text message and clickable buttons. The clickable buttons are treated as a response from the user to process the journey further.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
It is a special type of message using which a chatbot can provide multiple options for a customer to select. It is a message type with a text message and clickable buttons. The clickable buttons are treated as a response from the user to process the journey further.

Quick Reply has the following constituents:

- A text message (max 640 characters)
- Buttons with a title (max 20-character limit)
Buttons support emojis and variables can be added to the buttons.

Synonyms can be added to the buttons' names.

## When to use

If there is a need to show multiple options with a message where the user can select one of the provided options, a quick reply can be used.

## Limitations

- Applicable for Instagram channel only
## Quick Reply Node

## Skip Node Feature

### Introduction

The Skip Node feature exists on Journey Builder Prompt Nodes, allowing businesses to skip a question where the bot is designed to ask for information from the user. If the Skip Node checkbox is enabled, the bot checks the variable mapped to the node, and if the variable already contains a value, it skips the node and proceeds to the next one.

This feature helps businesses reduce the number of repeated questions asked by the bot, making it smarter by reusing information already gathered at earlier stages or through API integrations.

### Use Cases

Here are a few use cases that demonstrate the benefits of the Skip Node feature:

#### Customer Profile Completion:

Scenario - A customer has already provided their email address during the initial registration process.

Benefit - When the bot asks for the email address again in a subsequent conversation, it can skip this question if the email address is already stored, thereby avoiding redundancy and improving user experience.

#### Support Ticket Management:

Scenario - A user previously reported an issue and provided their device information.

Benefit - When the bot assists the same user in a new conversation, it can skip asking for the device information again if it is already stored, streamlining the support process.

#### E-commerce Checkout:

Scenario - A returning customer is making another purchase and had previously entered their shipping address.

Benefit - The bot can skip the address prompt if the shipping address is already on file, making the checkout process faster and more efficient.

These use cases illustrate how the Skip Node feature can make interactions more efficient and user-friendly by reusing previously gathered information.

More on Skip Node functionality here: Existing Console Doc Link

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
