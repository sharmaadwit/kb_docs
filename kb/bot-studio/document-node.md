source_url: https://console-docs.gupshup.io/docs/document-node

<!-- kb-golden:v10 -->
# Document Node

**Module**: Bot Studio

## Definition
As the name suggests, you can add a document to this node and add it to the chatbot conversation. The document can be uploaded in the conversation using a public URL of the document or from the local device. It supports all formats of files.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Document Node

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Document Node**.
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
- Go to **Document Node**.

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
# Document Node

**Module**: Bot Studio

## Overview
As the name suggests, you can add a document to this node and add it to the chatbot conversation. The document can be uploaded in the conversation using a public URL of the document or from the local device. It supports all formats of files.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
As the name suggests, you can add a document to this node and add it to the chatbot conversation. The document can be uploaded in the conversation using a public URL of the document or from the local device. It supports all formats of files.

### When to use

Say for instance a brochure or user manual is to be sent to a customer which will be helping them to better understand the product, in such cases, the document node plays a vital role. There are two ways to add documents. A publicly accessible document URL can be added to this node and the document gets visible at the communication channel. Documents can also be be uploaded from the device.

### Limitations

- Document upload size limit is 16 MB
- The document node can’t be blank.
- Type of Documents: Any valid MIME-type.
### How to use Document Node

To add a document node, you can select it from the menu on the canvas or in the message menu on the left-hand side panel.

VIDEO COMING SOON

### Document Node

Uploading a Document from the device

Uploading Document through publicly accessible Document URL

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
