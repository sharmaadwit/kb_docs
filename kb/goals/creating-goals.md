source_url: https://console-docs.gupshup.io/docs/creating-goals

<!-- kb-golden:v4 -->
# Creating Goals

**Module**: Goals

## Definition
Please refer to your journey and create Milestones and Trackers accordingly. You CANNOT implement Goal nodes without creating them.

## Procedure
### Exact path
Gupshup Console → Goals → Creating Goals

### Where to configure it
Gupshup Console → Goals → Creating Goals

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to the Goals section under Bot Studio in the navigation sidebar on the left.

### Steps
1. Open Gupshup Console.
2. Go to the Goals section under Bot Studio in the navigation sidebar on the left.
3. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- You need to create Goals before you can implement them in your journeys.
- Enter a name for the Goal in Goal Name.

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- Please refer to your journey and create Milestones and Trackers accordingly. You CANNOT implement Goal nodes without creating them.
- You CANNOT delete existing Milestones.

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation
- _Add 1–2 bullets distinguishing this module from adjacent modules to reduce retrieval drift._

## Reference (from source)
<!-- procedural:v2 -->
# Creating Goals

**Module**: Goals

## Overview
Please refer to your journey and create Milestones and Trackers accordingly. You CANNOT implement Goal nodes without creating them.

## When to use
_Add the primary scenarios and personas._

## Setup path
- Go to the Goals section under Bot Studio in the navigation sidebar on the left.

## Step-by-step configuration
### You need to create Goals before you can implement them in your journeys.

Please refer to your journey and create Milestones and Trackers accordingly. You CANNOT implement Goal nodes without creating them.

Goals dashboard (First-time users)

### Milestones are sequential in nature. Their sequence is set as per creation, NOT implementation in journeys.

For example, if a Goal has been created with three Milestones in the sequence M1 followed by M2 followed by M3, their sequence remains the same even if M2 is implemented in a Goal node before M1.

### If a Milestone is skipped, the Tracker Values for that milestone are automatically filled with the respective Default Values against the user’s customer ID.

For example, if a user achieves the third Milestone without achieving the first and second Milestones, the respective Default Values are set as Tracker Values entered by that user in the first and second Milestones.

- Go to the Goals section under Bot Studio in the navigation sidebar on the left.
- Click on the Create your first goal button to get started.
Creating a goal

- Enter a name for the Goal in Goal Name.
- Additionally, you can describe the aim/objective/desired result in Goal Description and add Tags if required.
- You can edit the name for the first Milestone from "Milestone 1".
- You can describe the Milestone in Description just below the Milestone name if required.
- You can edit the name for the first Tracker from "Tracker 1".
- You can describe the Tracker in Description just below the Tracker name if required.
- The Default Value field is mandatory for all added trackers. It is strongly recommended to keep the default value different from what user can enter so that it can
- It is strongly recommended to keep the default value different from what user can enter so that it can
### The Default Value is set as the Tracker Value for a user’s customer ID when they skip the Milestone in the same conversation.

As milestones are sequential in nature, if a user achieves the third milestone without achieving the first and second milestones, the respective Default Values are set as Tracker Values entered by that user in the first and second milestones.

- New trackers can be added using the + Add Tracker button at the bottom right of the trackers. The trash can icon can be clicked to delete a tracker.
- The trash can icon can be clicked to delete a tracker.
- New milestones can be added using the + Add Milestone button at the bottom left of the screen. The Delete Milestone option (in red) can be clicked to delete the milestone. A popup will appear for confirmation after you click the option.
- The Delete Milestone option (in red) can be clicked to delete the milestone. A popup will appear for confirmation after you click the option.
- Once you are done, click the Create button to save the goal.
Creating a goal

## Editing Goals

- You can edit a Goal by clicking on the Edit (pencil) icon that appears on the Goals listing page.
- You can rename the Goal, Milestones and Trackers.
- You can add new Milestones after the existing Milestones.
- You CANNOT delete existing Milestones.
- You can add or delete Trackers.
- You can update the Default Value for the Trackers.
Goals dashboard (Returning users)

Updated 10 months ago

- Implementing Goals

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Once you are done, click the Create button to save the goal.
