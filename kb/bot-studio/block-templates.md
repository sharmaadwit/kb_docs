source_url: https://console-docs.gupshup.io/docs/block-templates

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
