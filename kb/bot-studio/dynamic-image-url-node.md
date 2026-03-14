source_url: https://console-docs.gupshup.io/docs/dynamic-image-url-node

<!-- kb-golden:v10 -->
# Dynamic Image URL Node

**Module**: Bot Studio

## Definition
The Dynamic Image URL Node can be used to create dynamic images during run-time. The dynamic card image can be stored in a variable and sent to the user using an Image Node. For instance, the business wants to send QR Code to customers with dynamic information of the customer, the dynamic image card can be created and sent to the user. This can be used to send movie tickets or banking statements to users.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Dynamic Image URL Node

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Dynamic Image URL Node**.
4. Select one of the three templates and fill the content. TemplateTemplate ContentTemplate 1Card titleSubtitleDescriptionImage(16MB)Image(16MB)Template 2Card TitleSubtitleImage(16MB)DescriptionTemplate 3Card TitleSubtitleDescriptionImage(16MB).
5. Select one of the three templates and fill the content.
6. Save the image in a string variable and bot designer can use a reply node or image node to send the dynamic card image URL to the channel.

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
- Go to **Dynamic Image URL Node**.

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
# Dynamic Image URL Node

**Module**: Bot Studio

## Overview
The Dynamic Image URL Node can be used to create dynamic images during run-time. The dynamic card image can be stored in a variable and sent to the user using an Image Node. For instance, the business wants to send QR Code to customers with dynamic information of the customer, the dynamic image card can be created and sent to the user. This can be used to send movie tickets or banking statements to users.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### When to Use

The Dynamic Image URL Node can be used to create dynamic images during run-time. The dynamic card image can be stored in a variable and sent to the user using an Image Node. For instance, the business wants to send QR Code to customers with dynamic information of the customer, the dynamic image card can be created and sent to the user. This can be used to send movie tickets or banking statements to users.

### How to Use

Drag and drop the Dynamic Image URL Node on the canvas.

- Select one of the three templates and fill the content. TemplateTemplate ContentTemplate 1Card titleSubtitleDescriptionImage(16MB)Image(16MB)Template 2Card TitleSubtitleImage(16MB)DescriptionTemplate 3Card TitleSubtitleDescriptionImage(16MB)
Select one of the three templates and fill the content.

All headers within a template are mandatory.

- Preview the template as it would be sent on the channel from the node on the canvas.
- Save the image in a string variable and bot designer can use a reply node or image node to send the dynamic card image URL to the channel.
### Limitations:

- Three pre-defined templates are available in the dynamic card image URL node
- A message node can send the image URL to the channel.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Save the image in a string variable and bot designer can use a reply node or image node to send the dynamic card image URL to the channel.

**Last updated (from source)**: Updated 10 months ago
