source_url: https://console-docs.gupshup.io/docs/whatsapp-carousel-message-using-the-send-message-node

<!-- kb-golden:v10 -->
# WhatsApp Carousel Message Using the Send Message Node

**Module**: Bot Studio

## Definition
This guide explains how to send a WhatsApp Media Carousel Message using the Send Message Node in Journey Builder by selecting WhatsApp Raw and pasting the exact supported payload.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → WhatsApp Carousel Message Using the Send Message Node

### Prerequisites
- WhatsApp's Media Carousel Message allows businesses to send up to 10 media cards in a horizontally scrollable carousel. Each card must meet the following requirements:

### Fields to configure
- Message content

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **WhatsApp Carousel Message Using the Send Message Node**.
4. Add a Send Message Node to your journey.
5. Save & Deploy your journey.

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
- Go to **WhatsApp Carousel Message Using the Send Message Node**.

## Options / variants
- Add a Send Message Node to your journey.

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
# WhatsApp Carousel Message Using the Send Message Node

**Module**: Bot Studio

## Overview
This guide explains how to send a WhatsApp Media Carousel Message using the Send Message Node in Journey Builder by selecting WhatsApp Raw and pasting the exact supported payload.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
# WhatsApp Carousel Message via Send Message Node (WhatsApp Raw)

### Journey Builder – JB Pro Guide

This guide explains how to send a WhatsApp Media Carousel Message using the Send Message Node in Journey Builder by selecting WhatsApp Raw and pasting the exact supported payload.

## 1. Configure the Send Message Node

To send a WhatsApp Carousel message:

- Add a Send Message Node to your journey.
- In the node configuration panel: Channel: WhatsApp Message Type: WhatsApp Raw
- Channel: WhatsApp
- Message Type: WhatsApp Raw
- Paste the Carousel JSON payload into the Raw Payload editor.
- Save & Deploy your journey.
## 2. WhatsApp Carousel Overview

WhatsApp's Media Carousel Message allows businesses to send up to 10 media cards in a horizontally scrollable carousel. Each card must meet the following requirements:

- Unique card_index between 0–9
- Same header.type across all cards (image or video)
- One CTA button (cta_url) per card
- Optional short descriptive body text
- Minimum 2 cards required to render a carousel
## 3. Sample Carousel Payload (Use As-Is)

⚠ PASTE THIS EXACT PAYLOAD STRUCTURE WITHOUT ANY MODIFICATION

```
{
    "raw": {
        "type": "interactive",
        "interactive": {
            "type": "carousel",
            "body": {
                "text": "Check out our latest offers!"
            },
            "action": {
                "cards": [
                    {
                        "card_index": 0,
                        "type": "cta_url",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": "https://picsum.photos/200/300"
                            }
                        },
                        "body": {
                            "text": "Exclusive deal #1"
                        },
                        "action": {
                            "name": "cta_url",
                            "parameters": {
                                "display_text": "Shop now",
                                "url": "https://picsum.photos/200/300"
                            }
                        }
                    },
                    {
                        "card_index": 1,
                        "type": "cta_url",
                        "header": {
                            "type": "image",
                            "image": {
                                "link": "https://picsum.photos/200/300"
                            }
                        },
                        "body": {
                            "text": "Exclusive deal #2"
                        },
                        "action": {
                            "name": "cta_url",
                            "parameters": {
                                "display_text": "Shop now",
                                "url": "https://picsum.photos/200/300"
                            }
                        }
                    }
                ]
            }
        }
    }
}
```

Note: You can upto 10 cards by adding more objects inside the cards array.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Save & Deploy your journey.

**Last updated (from source)**: Updated 4 months ago
