source_url: https://console-docs.gupshup.io/docs/carousel-and-lto-template-support-via-send-message-node

<!-- kb-golden:v10 -->
# Carousel & LTO Template

**Module**: Bot Studio

## Definition
Carousel & LTO Template via Send Message Node. Available for JB Pro only.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Carousel & LTO Template

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- Message content

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Carousel & LTO Template**.
4. Select the Text/Template option on the send message node and use the below sample payload format for reference. Designers can dynamically create the Payload in the same format mentioned below to send customized Templates during bot runtime.
5. Click **Save** (or **Save & Deploy**) to apply changes.

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
- Go to **Carousel & LTO Template**.

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
# Carousel & LTO Template

**Module**: Bot Studio

## Overview
Carousel & LTO Template via Send Message Node. Available for JB Pro only.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Carousel & LTO Template via Send Message Node. Available for JB Pro only.

# Introduction:

Journey Builder Pro now allows businesses to send Limited Time Offer and Carousel Templates during two-way conversations. This is made possible using the Send Message Node on the Journey Builder canvas. Bot designers can request dev access to use the Send Message Node for their project.

# How to use the feature:

Select the Text/Template option on the send message node and use the below sample payload format for reference. Designers can dynamically create the Payload in the same format mentioned below to send customized Templates during bot runtime.

# Sample Payloads:

## Limited Time Offer -

```
 {
    "type": "text",
    "template": "{\"id\":\"<<GUPSHUP_TEMPLATE_ID>>\",\"params\":[\"<<COUPON_CODE>>\"]}"
  }
```

## Carousel -

```
{
  "type": "text",
  "template": "{\"id\":\"<<GUPSHUP_TEMPLATE_ID>>\",\"params\":[]}",
  "message": "{\"type\":\"carousel\",\"cardHeaderType\":\"IMAGE\",\"cards\":[{\"link\":\"https://env1-common-marketing-bucket.s3.amazonaws.com/31252338/31563891/20/e4189ec7-36df-43fb-a79c-c8101dcd76cf/Media_Image_3.jpg\"},{\"link\":\"https://env1-common-marketing-bucket.s3.amazonaws.com/31252338/31563891/20/e4189ec7-36df-43fb-a79c-c8101dcd76cf/Media_Image_3.jpg\"}]}"
}
```

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 8 months ago
