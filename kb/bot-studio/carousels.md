source_url: https://console-docs.gupshup.io/docs/carousels

<!-- kb-golden:v9 -->
# Carousels

**Module**: Bot Studio

## Definition
Carousels or cards are multi-product messages which consist of an image of the product, a short description, and clickable buttons. Carousels are widely used for showcasing multiple products in a message. Each card can have a description of a product. A maximum of 10 products can be shown using carousels.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Carousels

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Carousels**.
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
- Go to **Carousels**.

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
# Carousels

**Module**: Bot Studio

## Overview
Carousels or cards are multi-product messages which consist of an image of the product, a short description, and clickable buttons. Carousels are widely used for showcasing multiple products in a message. Each card can have a description of a product. A maximum of 10 products can be shown using carousels.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Carousels or cards are multi-product messages which consist of an image of the product, a short description, and clickable buttons. Carousels are widely used for showcasing multiple products in a message. Each card can have a description of a product. A maximum of 10 products can be shown using carousels.

A card has the following constituents:

Image: An image can be uploaded on the card using a URL, the image can be of 8 MB maximum, and JPEG, JPG, and PNG images can be uploaded.

Title: A text field where a title to the image can be added giving a brief description of the item in the image. It can be 80 characters maximum. Emojis and variables are supported in the title field.

Subtitle: A field to enter supporting text for the card. It can be a description of the product. 80 characters can be added to the description. Emojis and variables are supported. This field is optional and can be added as per the requirement.

Buttons: To set actions in the card for a customer, buttons are used. Each button can lead to a URL or a payload. 1 button is mandatory.

### When to use

To showcase multiple products in a message using cards, carousels can be used.

### Validations

- A maximum of 10 cards can be added.
- A maximum of 3 buttons can be added to a card.
- Image size can’t exceed more than 8 MB
### How to use

Carousel is a message type available in the action & prompts menu.

### Carousel Node

Updated 4 months ago

How to use Carousel with dynamic cards...

- Dynamic Carousel Node

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
