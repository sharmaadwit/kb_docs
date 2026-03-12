source_url: https://console-docs.gupshup.io/docs/sticker-node

<!-- kb-golden:v1 -->
# Sticker Node

**Module**: Bot Studio

## Definition
The Sticker Message Node in Journey Builder enables businesses to send engaging sticker messages to users via supported channels, currently only WhatsApp. Stickers add a fun and interactive visual element to conversations, enhancing user engagement and making communication more lively.

## Procedure
### Where to configure it
Gupshup Console → Bot Studio → Sticker Node

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Sticker Node**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- Festival Greetings
- Customer Service Interactions with Personalized Stickers
- Promotional Offers with Visual Flair

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Reference (from source)
<!-- procedural:v2 -->
# Sticker Node

**Module**: Bot Studio

## Overview
The Sticker Message Node in Journey Builder enables businesses to send engaging sticker messages to users via supported channels, currently only WhatsApp. Stickers add a fun and interactive visual element to conversations, enhancing user engagement and making communication more lively.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
# Introduction

The Sticker Message Node in Journey Builder enables businesses to send engaging sticker messages to users via supported channels, currently only WhatsApp. Stickers add a fun and interactive visual element to conversations, enhancing user engagement and making communication more lively.

# WhatsApp Specifics

- Format Requirements: Stickers need to be in .webp format ONLY. This ensures compatibility with WhatsApp's sticker feature.
- Size Limits: Animated Stickers: Max file size of 500 KB. Static Stickers: Max file size of 100 KB.
- Animated Stickers: Max file size of 500 KB.
- Static Stickers: Max file size of 100 KB.
# Functionality

File Upload: Bot designers can upload stickers directly into the node, as long as they meet the format and size requirements.

Link URL: Designers can also link a URL containing the sticker file. This is helpful when the sticker is hosted externally or stored as part of user data.

# Validation

File Validation: Uploaded stickers will be validated to ensure they are in the correct .webp format and meet the size constraints (500 KB max.).

URL/Variable: Stickers linked via URL won't be validated, so bot designers must ensure that the links contain valid sticker files.

# How to Use

- Add the Sticker Node: In Journey Builder, insert the Sticker Node into your flow. Choose whether to upload a file or link a URL for the sticker content.
- Sticker Upload: If uploading a file, ensure the sticker is in the correct .webp format and within the file size limits (500 KB for animated, 100 KB for static). The system will automatically validate the file.
- Linking URL: If using a URL, ensure the sticker file is hosted correctly and adheres to the format and size restrictions, as the system will not perform validation in this case.
# Use Cases

Few examples of how the Sticker Message Node can enhance user interaction:

### Festival Greetings

- Scenario: During festive seasons like Diwali or Christmas, a business wants to send warm wishes to its customers.
- Benefit: Stickers allow the brand to deliver visually appealing greetings, creating a more personal and festive interaction.
### Customer Service Interactions with Personalized Stickers

- Scenario: A customer service bot is handling inquiries and wants to make the interaction more human and friendly by adding stickers.
- Benefit: Stickers can be used to express emotion or appreciation during the conversation, helping the brand connect with users on a personal level.
### Promotional Offers with Visual Flair

- Scenario: A business wants to send a visually appealing promotional offer to users via WhatsApp.
- Benefit: Using stickers, the business can enhance the message with eye-catching visuals that grab attention, encouraging users to engage with the offer.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
