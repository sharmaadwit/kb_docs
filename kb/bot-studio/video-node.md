source_url: https://console-docs.gupshup.io/docs/video-node

<!-- kb-golden:v10 -->
# Video Node

**Module**: Bot Studio

## Definition
As the name suggests, you can add a video to this node and add it to the chatbot conversation. The video can be uploaded in the conversation using a public URL of the video or from the local device.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Video Node

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Video Node**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

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
- Go to **Video Node**.

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
# Video Node

**Module**: Bot Studio

## Overview
As the name suggests, you can add a video to this node and add it to the chatbot conversation. The video can be uploaded in the conversation using a public URL of the video or from the local device.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
As the name suggests, you can add a video to this node and add it to the chatbot conversation. The video can be uploaded in the conversation using a public URL of the video or from the local device.

### When to use

Product videos can be shared using this node. It can help make the conversation more interactive and informative. Businesses can share videos of their products with their customers to increase leads or sales, to guide users regarding their issues.

### Limitations

- Video Upload size limit is 16 MB.
- The video can’t be blank.
- Only MP4 and 3GP format videos are supported.
### How to use Video Node

VIDEO COMING SOON

### Video Node

Uploading a Video from the device

Uploading Video through publicly accessible Video URL

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
