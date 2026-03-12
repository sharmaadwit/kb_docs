source_url: https://console-docs.gupshup.io/docs/inline-analytics

<!-- kb-golden:v1 -->
# Inline Analytics

**Module**: Bot Studio Analytics

## Definition
- Inline Analytics refers to node-specific analytics that can be referred to while designing your journey on the Bot Studio Canvas.
- You can view the Inline Analytics for a journey by navigating to the Canvas of that journey and switching on the Analytics toggle present near the Journey Name.
### Inline Analytics displays the counts only for the last 30 days.

## Procedure
### Where to configure it
Gupshup Console → Bot Studio Analytics → Inline Analytics

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio Analytics → Inline Analytics**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- Inline Analytics displays the counts only for the last 30 days.

## Notes
- _Add prerequisites, constraints, and rollout behavior._

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
