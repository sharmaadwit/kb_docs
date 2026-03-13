source_url: https://console-docs.gupshup.io/docs/block-templates

<!-- kb-golden:v7 -->
# Block Templates

**Module**: Bot Studio

## Definition
Block Templates are reusable building blocks created from nodes within a journey. These blocks can be saved, previewed, and dragged into other journeys within the same project—making bot creation significantly faster, more consistent, and modular.

## Procedure
### Exact path
Gupshup Console → Bot Studio → Block Templates

### Where to configure it
Gupshup Console → Bot Studio → Block Templates

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Navigate to the Blocks tab on the left panel of the canvas

### Steps
1. Open Gupshup Console.
2. Navigate to the Blocks tab on the left panel of the canvas
3. Select one or more connected nodes on the canvas.
4. Click on the preview icon to see the structure and nodes.
5. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- Select one or more connected nodes on the canvas

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- Starting Node cannot be part of a Block Template

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
# Block Templates

**Module**: Bot Studio

## Overview
Block Templates are reusable building blocks created from nodes within a journey. These blocks can be saved, previewed, and dragged into other journeys within the same project—making bot creation significantly faster, more consistent, and modular.

## When to use
_Add the primary scenarios and personas._

## Setup path
- Navigate to the Blocks tab on the left panel of the canvas

## Step-by-step configuration
## What Are Block Templates?

Block Templates are reusable building blocks created from nodes within a journey. These blocks can be saved, previewed, and dragged into other journeys within the same project—making bot creation significantly faster, more consistent, and modular.

You’ll now find a “Blocks” section on the left panel of the Journey Canvas, alongside Message and Action nodes. This makes it easy to preview, drag, and reuse frequently used blocks across multiple journeys.

## ✨ What’s New?

✅ Save Blocks from any journey to reuse them later

✅ Preview Blocks before importing them

✅ Drag and Drop onto any journey canvas

✅ Customize the block post-import without affecting the original

✅ Easily delete unused Block Templates

✅ Even a single Code Node can be saved as a template for reuse

✅ Original journey blocks can be deleted without impacting saved templates

## 📋 How to Use Block Templates

➕ Saving a Block:

- Select one or more connected nodes on the canvas
- Right-click and choose “Save as Block Template”
- Give your template a name and optional description
- Saved Blocks will now appear under the Blocks section on the left panel
📥 Using a Saved Block:

- Navigate to the Blocks tab on the left panel of the canvas
- Click on the preview icon to see the structure and nodes
- Drag and drop the block onto your current journey
- Update and connect it as needed
## ⚠️ Notes & Limitations

- A maximum of 100 Block Templates can be saved per project
- Starting Node cannot be part of a Block Template
- When you import a Block:
- Local variables in text fields are replaced by {{BLOCKVARIABLE}}
- Dropdown fields are cleared for reconfiguration
- Call & Return Node mappings are cleared
- Template Node variables are also reset
- Changes made to a saved block do not reflect in other journeys where it has already been used
## 💡 Pro Tips

- Use Block Templates to modularize large use cases (e.g., Lead capture, FAQs, Confirmations)
- Group reusable logic into dedicated templates like “Check Eligibility”, “Send Invoice”, etc.
- Maintain a naming convention like Lead_Capture_v1, FAQ_Product, etc., for easier management

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- ✅ Save Blocks from any journey to reuse them later
- - Right-click and choose “Save as Block Template”

**Last updated (from source)**: Updated 10 months ago
