source_url: https://console-docs.gupshup.io/docs/implementing-goals

<!-- kb-golden:v4 -->
# Implementing Goals

**Module**: Goals

## Definition
Please refer to your journey and create Milestones and Trackers accordingly. You CANNOT implement Goal nodes without creating them.

## Procedure
### Exact path
Gupshup Console → Goals → Implementing Goals

### Where to configure it
Gupshup Console → Goals → Implementing Goals

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Goals → Implementing Goals**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- You need to create Goals before you can implement them in your journeys.

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- Please refer to your journey and create Milestones and Trackers accordingly. You CANNOT implement Goal nodes without creating them.

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation
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
