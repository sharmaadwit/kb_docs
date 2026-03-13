source_url: https://console-docs.gupshup.io/docs/reply-node

<!-- kb-golden:v9 -->
# Reply Node

**Module**: Bot Studio

## Definition
Node to add a Text or Image header in a message having a maximum number of 3 buttons for user selection.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Reply Node

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Reply Node**.
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
- Go to **Reply Node**.

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
# Reply Node

**Module**: Bot Studio

## Overview
Node to add a Text or Image header in a message having a maximum number of 3 buttons for user selection.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Node to add a Text or Image header in a message having a maximum number of 3 buttons for user selection.

## When to use

- Send promotional messages to customers on WhatsApp along with buttons.
- Showcase any single product in the conversation flow.
- Reply Node is an interactive message which will wait for the user's response as a selection on the given buttons followed by the subsequent journey.
- You can add an image of the item with a description to it along with the 3 most required buttons.
## Reply Node Elements

The reply node has below major fields:

- Header Image Header (Image can be added as header) Text Header (Text can be added as header)
- Header (Image can be added as header)
- Text Header (Text can be added as header)
- Description
- Footer Text (Short description)
- Buttons (Maximum 3 Buttons, Minimum 1 Buttons)
## Limitations

- Element and respective size:
- The description can’t be empty
- The button Title can not empty
- Emojis are not allowed in buttons
- Node is applicable for Whatsapp channel
## How to use

To add a reply node, you can select it from the menu on the canvas or in the prompts menu on the left-hand side panel. Select text, image, video or document headers.

## Reply Node

With Text Header:

With Image Header:

## Support for Synonyms in Reply Node

### Introduction

Bot designers can now add Synonyms for the List Row and Reply Button titles to ensure that the user inputs matching the title synonyms also gets captured as a valid input from the user.

### How to use Synonyms in Button Titles?

Bot designers can create nodes with the required button titles and then click on "More Options" to open the accordion containing the Synonym field. Synonyms can be typed, and then the user can press enter to save the synonym. Multiple synonyms can be entered for a single button to provide more flexibility to end-users in selecting input.

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
