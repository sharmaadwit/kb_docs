source_url: https://console-docs.gupshup.io/docs/document-node

<!-- kb-golden:v9 -->
# Document Node

**Module**: Bot Studio

## Definition
As the name suggests, you can add a document to this node and add it to the chatbot conversation. The document can be uploaded in the conversation using a public URL of the document or from the local device. It supports all formats of files.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Document Node

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Document Node**.
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
- Go to **Document Node**.

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
