source_url: https://console-docs.gupshup.io/docs/dynamic-carousel-node

<!-- kb-golden:v9 -->
# Dynamic Carousel Node

**Module**: Bot Studio

## Definition
Send Personalized cards in the carousel for each user based on the user preference or business suggestion.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Dynamic Carousel Node

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Dynamic Carousel Node**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- "title": "Book Test Drive",

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
- Go to **Dynamic Carousel Node**.

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
# Dynamic Carousel Node

**Module**: Bot Studio

## Overview
Send Personalized cards in the carousel for each user based on the user preference or business suggestion.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Send Personalized cards in the carousel for each user based on the user preference or business suggestion.

### Introduction

Carousel Node is now enhanced with dynamic payload support to render the cards with dynamic content during bot conversation. Bot designers can fetch the card content from client APIs or internal sources and create the dynamic json payload to be converted to Carousel.

### What's New!

- Send Dynamic Cards with Personalized Images
- Send dynamic contents and buttons for every card individually
- Supported on Web Widget and Instagram Channel
- Ability to send Static and Dynamic cards using one node
- Send upto 10 cards with one Dynamic Node
- Support of CTA Buttons and URLs as well
### How to use a Dynamic Carousel?

To use the Dynamic Carousel Bot designer will have to toggle the Dynamic Node Toggle button as shown below which will provide the options to pass on the JSON Elements for the dynamic cards.

Bot designers will need to form the required JSON payload during design time or runtime of the bot to have the required information to send the Dynamic carousel on the required channel.

Once the Dynamic functionality is toggled on, the Carousel Node will have these additional fields to pass the JSON Element reference for each field of the Card viz. Image, Title , Buttons etc.

Bot designers have to store the formatted JSON on a Variable to refer to the same while configuring the Dynamic Carousel node.

A sample JSON for Dynamic Carousel is shown below which is stored on the jsonVar variable :

```
\{\
"carousel": \[
\{
"image": "[https://picsum.photos/200"](https://picsum.photos/200"),
"bodyTitle": "Title of the Card1",
"bodysubTitle": "Subtitle of the Card1",
"buttons": \[
\{
"title": "Buy",
"type": "postback",
"payload": "card1\_yes"
},
\{
"title": "Book Test Drive",
"type": "postback",
"payload": "card1\_no"
},
\{
"title": "Know More",
"type": "url",
"URL": "[https://gupshup.io](https://gupshup.io)"
}
]\[
\{
"title": "Buy",
"type": "postback",
"payload": "card1\_yes"
},
\{
"title": "Book Test Drive",
"type": "postback",
"payload": "card1\_no"
},
\{
"title": "Know More",
"type": "url",
"URL": "[https://gupshup.io](https://gupshup.io)"
}
]
},
\{
"image": "[https://picsum.photos/200"](https://picsum.photos/200"),
"bodyTitle": "Title of the Card1",
"bodysubTitle": "Subtitle of the Card1",
"buttons": \[
\{
"title": "Buy",
"type": "postback",
"payload": "card1\_yes"
},
\{
"title": "Book Test Drive",
"type": "postback",
"payload": "card1\_no"
},
\{
"title": "Know More",
"type": "url",
"URL": "[https://gupshup.io](https://gupshup.io)"
}
]\[
\{
"title": "Buy",
"type": "postback",
"payload": "card1\_yes"
},
\{
"title": "Book Test Drive",
"type": "postback",
"payload": "card1\_no"
},
\{
"title": "Know More",
"type": "url",
"URL": "[https://gupshup.io](https://gupshup.io)"
}
]
}
]
}
```

Now let's check on how each of the fields needs to be configured in the Dynamic Carousel.

Card Element: Card element represents the JSON Key where the Cards array is stored. During Journey execution the Card element will be iterated to fetch the information of the cards that needs to be shown to the user. Each array element inside the carousel key will form a card with its information provided inside it.

Eg.: In the above JSON the Card Element will be var_local.jsonVar as it contains the array of the cards information. Since there are 2 items inside the array then 2 cards will be processed during runtime of the journey.

Image Element: Similar to card element, the bot designer have to mention the key from which the Images for the respective cards can be fetched.

Eg.: In the above JSON the Images of each card is stored in the card elements image key. Bot will iterate through each json object inside the card element to fetch the image URLs for the same.

Title and Subtitle Elements: Bot designers have to similarly refer to the respective Title and Subtitle keys for each card inside the Card element.

Button Element: Button element can be mapped with the same or different JSONs to make it more flexible for Bot designer to fetch the Button titles from a different JSON object if required.

Eg. In the above case the Button element is referred from the same Card element JSON.

Note: Currently Dynamic Carousel doesn't support combination of Payload Based buttons and URL CTA Buttons.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 8 months ago
