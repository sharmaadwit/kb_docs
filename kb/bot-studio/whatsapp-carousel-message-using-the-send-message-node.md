source_url: https://console-docs.gupshup.io/docs/whatsapp-carousel-message-using-the-send-message-node
# BOT STUDIO

## WhatsApp Carousel Message Using the Send Message Node

# WhatsApp Carousel Message Using the Send Message Node

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

Updated 4 months ago
