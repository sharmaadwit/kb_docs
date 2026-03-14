source_url: https://console-docs.gupshup.io/docs/inline-analytics

<!-- kb-golden:v10 -->
# Inline Analytics

**Module**: Bot Studio Analytics

## Definition
- Inline Analytics refers to node-specific analytics that can be referred to while designing your journey on the Bot Studio Canvas.
- You can view the Inline Analytics for a journey by navigating to the Canvas of that journey and switching on the Analytics toggle present near the Journey Name.
### Inline Analytics displays the counts only for the last 30 days.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio Analytics → Inline Analytics

### Prerequisites
- Access to **Gupshup Console → Bot Studio Analytics → Inline Analytics** in Gupshup Console.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio Analytics**.
3. Go to **Inline Analytics**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run a test event/journey and confirm the expected analytics or goal data appears in the UI.

### Troubleshooting
- If something does not work as expected, re-check the exact UI path, required fields, and any save/deploy step.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Bot Studio Analytics**.
- Go to **Inline Analytics**.

## Options / variants
- You can click the refresh icon besides the Analytics toggle to reload the latest counts.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Identify the upstream module where this is configured and the downstream module where the outcome is verified.

## Module disambiguation docs
- Distinguish this page from adjacent modules/settings before troubleshooting elsewhere.

## Reference (from source)
<!-- procedural:v2 -->
# Inline Analytics

**Module**: Bot Studio Analytics

## Overview
- Inline Analytics refers to node-specific analytics that can be referred to while designing your journey on the Bot Studio Canvas.
- You can view the Inline Analytics for a journey by navigating to the Canvas of that journey and switching on the Analytics toggle present near the Journey Name.
### Inline Analytics displays the counts only for the last 30 days.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
- Inline Analytics refers to node-specific analytics that can be referred to while designing your journey on the Bot Studio Canvas.
- You can view the Inline Analytics for a journey by navigating to the Canvas of that journey and switching on the Analytics toggle present near the Journey Name.
### Inline Analytics displays the counts only for the last 30 days.

- After the toggle is switched on, an Analytics section appears in each node of the journey and numbers appear on the connectors between the nodes. The number appearing on a connector between nodes represents the number of times users traversed (moved) from the previous node to the next node.
- The number appearing on a connector between nodes represents the number of times users traversed (moved) from the previous node to the next node.
- There are two metrics visible in the Analytics section:
### The counts of Traversed and Exits always represent number of times, and not conversations or users.

- You can click the refresh icon besides the Analytics toggle to reload the latest counts.
## FAQs

Why is there a lesser number on a particular node than the node before it and after it?

There can be two possibilities here:

- Users can traverse (move) to multiple nodes from a single node. Hence the counts are divided between multiple nodes.
- The node has been newly added between two pre-existing nodes within the last 30 days. The new node shows the counts only after its addition, while the older nodes show total counts for the last 30 days from before and after the addition of the new node.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
