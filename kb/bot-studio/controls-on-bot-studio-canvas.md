source_url: https://console-docs.gupshup.io/docs/controls-on-bot-studio-canvas

<!-- kb-golden:v10 -->
# Controls on Bot Studio Canvas

**Module**: Bot Studio

## Definition
The following controls on the canvas make it easy to navigate through long journeys.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Controls on Bot Studio Canvas

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Controls on Bot Studio Canvas**.
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
- Go to **Controls on Bot Studio Canvas**.

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
# Controls on Bot Studio Canvas

**Module**: Bot Studio

## Overview
The following controls on the canvas make it easy to navigate through long journeys.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
The following controls on the canvas make it easy to navigate through long journeys.

## Mini Map View

The Mini Map provides an overview of the journey flow in a grayscale dynamic image in the bottom right hand corner. It helps the user to understand the extent of the flow and it’s current location.

## Controls

Zoom In - It is a button used to zoom in to the console body to work on the specific location in a detailed manner. Zoom out- It is a button used to zoom out from the console body to work on the other locations. Full Screen - It is a button used to get maximum overview of the console body. Lock- It is a button used to lock the console body to avoid changes in the directions/paths of the existing flow while adding new nodes to the flow. Align Horizontally - It is a button to automatically arrange the existing nodes/flow pattern into a horizontal set of manner. Align Vertically -It is a button to automatically arrange the existing nodes/flow pattern into a vertical set of manner.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
