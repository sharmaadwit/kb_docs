source_url: https://console-docs.gupshup.io/docs/skip-node

<!-- kb-golden:v9 -->
# Skip Node

**Module**: Bot Studio

## Definition
Now you can use Skip Node as an Integrated feature into Prompt nodes, designed to streamline chatbot interactions by bypassing questions if certain conditions are met. It functions by skipping the Prompt node question if the assigned variable already contains a value.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Skip Node

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Skip Node**.
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
- Go to **Skip Node**.

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
