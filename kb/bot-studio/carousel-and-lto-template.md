source_url: https://console-docs.gupshup.io/docs/carousel-and-lto-template-support-via-send-message-node

<!-- kb-golden:v7 -->
# Carousel & LTO Template

**Module**: Bot Studio

## Definition
Carousel & LTO Template via Send Message Node. Available for JB Pro only.

## Procedure
### Exact path
Gupshup Console → Bot Studio → Carousel & LTO Template

### Where to configure it
Gupshup Console → Bot Studio → Carousel & LTO Template

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **Carousel & LTO Template**.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Carousel & LTO Template**.
4. Select the Text/Template option on the send message node and use the below sample payload format for reference. Designers can dynamically create the Payload in the same format mentioned below to send customized Templates during bot runtime.
5. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- _List the key variants/toggles visible in the UI._

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
