source_url: https://console-docs.gupshup.io/docs/skip-node

<!-- kb-golden:v10 -->
# Skip Node

**Module**: Bot Studio

## Definition
Now you can use Skip Node as an Integrated feature into Prompt nodes, designed to streamline chatbot interactions by bypassing questions if certain conditions are met. It functions by skipping the Prompt node question if the assigned variable already contains a value.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Skip Node

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Skip Node**.
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
- Go to **Skip Node**.

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
# Skip Node

**Module**: Bot Studio

## Overview
Now you can use Skip Node as an Integrated feature into Prompt nodes, designed to streamline chatbot interactions by bypassing questions if certain conditions are met. It functions by skipping the Prompt node question if the assigned variable already contains a value.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### Introduction

Now you can use Skip Node as an Integrated feature into Prompt nodes, designed to streamline chatbot interactions by bypassing questions if certain conditions are met. It functions by skipping the Prompt node question if the assigned variable already contains a value.

This can be found at the bottom of the prompt node settings after the store in variables option. This capability enhances user experience by avoiding repetitive queries and expediting the conversation flow.

### When to Use

- Optimised dialogue flow as Skip Node jumps over prompts
- Avoidance of Redundant questions leading to quicker resolutions
- Streamlined conversation: Conditions trigger skip, enhancing flow.
- Multiple skip nodes can be deployed in a single journey
### Note

- When employing Skip Node, ensure variables assigned to store responses are appropriately managed. If a variable already contains data, the associated prompt will be skipped.
- For seamless integration, ensure Skip Node configurations align with the overall chatbot logic and user journey.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
