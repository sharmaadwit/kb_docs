source_url: https://console-docs.gupshup.io/docs/whatsapp-carousel-message-using-the-send-message-node

<!-- kb-golden:v4 -->
# WhatsApp Carousel Message Using the Send Message Node

**Module**: Bot Studio

## Definition
This guide explains how to send a WhatsApp Media Carousel Message using the Send Message Node in Journey Builder by selecting WhatsApp Raw and pasting the exact supported payload.

## Procedure
### Exact path
Gupshup Console → Bot Studio → WhatsApp Carousel Message Using the Send Message Node

### Where to configure it
Gupshup Console → Bot Studio → WhatsApp Carousel Message Using the Send Message Node

### Prerequisites
- WhatsApp's Media Carousel Message allows businesses to send up to 10 media cards in a horizontally scrollable carousel. Each card must meet the following requirements:

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → WhatsApp Carousel Message Using the Send Message Node**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- Journey Builder – JB Pro Guide
- Add a Send Message Node to your journey.

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
