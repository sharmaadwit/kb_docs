source_url: https://console-docs.gupshup.io/docs/implementing-goals

<!-- kb-golden:v9 -->
# Implementing Goals

**Module**: Goals

## Definition
Please refer to your journey and create Milestones and Trackers accordingly. You CANNOT implement Goal nodes without creating them.

## Procedure
### Exact UI path
Gupshup Console → Goals → Implementing Goals

### Steps
1. Open Gupshup Console.
2. Go to **Goals**.
3. Go to **Implementing Goals**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- _Run a quick smoke test and confirm expected behavior._

### Fields to configure
- _List the fields/inputs you must set in the UI (and expected format)._

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- Please refer to your journey and create Milestones and Trackers accordingly. You CANNOT implement Goal nodes without creating them.

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Goals**.
- Go to **Implementing Goals**.

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation docs
- _Add 1–2 bullets distinguishing this module from adjacent modules to reduce retrieval drift._

## Reference (from source)
<!-- procedural:v2 -->
# Implementing Goals

**Module**: Goals

## Overview
Please refer to your journey and create Milestones and Trackers accordingly. You CANNOT implement Goal nodes without creating them.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### You need to create Goals before you can implement them in your journeys.

Please refer to your journey and create Milestones and Trackers accordingly. You CANNOT implement Goal nodes without creating them.

You can implement Goals within your journeys by adding Goal Nodes.

## Adding Goal Nodes in Journeys

- You can add a Goal Node at the point in your Journey where the user has achieved a Milestone.
### Milestones are sequential in nature. Their sequence is set as per creation, NOT implementation in journeys.

For example, if a Goal has been created with three Milestones in the sequence M1 followed by M2 followed by M3, their sequence remains the same even if M2 and M3 is implemented in a Goal node before M1.

### If a Milestone is skipped and a Milestone after it in the sequence of creation is achieved, the Tracker Values for that milestone are automatically filled with the respective Default Values against the user’s customer ID.

For example, if a user achieves the third Milestone without achieving the first and second Milestones, the respective Default Values are set as Tracker Values entered by that user in the first and second Milestones.

- Then select the name of Goal and the name of the Milestone being achieved from the respective dropdowns.
- The Trackers associated with the selected Milestone will be populated in the Goal node.
- Finally, assign a Tracker Value for each Tracker. You can enter a fixed value or a variable.
Updated 10 months ago

- Goal Analytics

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
