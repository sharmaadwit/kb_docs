source_url: https://console-docs.gupshup.io/docs/carousels

<!-- kb-golden:v1 -->
# Carousels

**Module**: Bot Studio

## Definition
Carousels or cards are multi-product messages which consist of an image of the product, a short description, and clickable buttons. Carousels are widely used for showcasing multiple products in a message. Each card can have a description of a product. A maximum of 10 products can be shown using carousels.

## Procedure
### Where to configure it
Gupshup Console → Bot Studio → Carousels

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Carousels**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- When to use
- Validations
- How to use
- Carousel Node

## Notes
- _Add prerequisites, constraints, and rollout behavior._

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
