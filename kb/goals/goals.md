source_url: https://console-docs.gupshup.io/docs/goals

<!-- kb-golden:v7 -->
# Concepts

**Module**: Goals

## Definition
The Goals feature enable businesses to define and track specific points in a bot journey where the Goal of the journey is being achieved.

## Procedure
### Exact path
Gupshup Console → Goals → Concepts

### Where to configure it
Gupshup Console → Goals → Concepts

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Goals**.
- Go to **Concepts**.

### Steps
1. Open Gupshup Console.
2. Go to **Goals**.
3. Go to **Concepts**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- Goal
- Milestone
- Tracker

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation
- _Add 1–2 bullets distinguishing this module from adjacent modules to reduce retrieval drift._

## Reference (from source)
<!-- procedural:v2 -->
# Concepts

**Module**: Goals

## Overview
The Goals feature enable businesses to define and track specific points in a bot journey where the Goal of the journey is being achieved.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
The Goals feature enable businesses to define and track specific points in a bot journey where the Goal of the journey is being achieved.

## Concepts

### Goal

- A Goal is the aim/objective/desired result that you wish to achieve within the bot journey.
- It comprises of one or more Milestones.
- A Goal is considered to be achieved only when all of its Milestones are achieved.
### Milestone

- A Milestone is a significant step/stage/event in the process of achieving a Goal.
- It comprises of one or more Trackers.
- When a Milestone is achieved, values are attributed to all its Trackers.
### Milestones are sequential in nature. Their sequence is set as per creation, NOT implementation in journeys.

For example, if a Goal has been created with three Milestones in the sequence M1 followed by M2 followed by M3, their sequence remains the same even if M2 and M3 is implemented in a Goal node before M1.

### If a Milestone is skipped, the Tracker Values for that milestone are automatically filled with the respective Default Values against the user’s customer ID.

For example, if a user achieves the third Milestone without achieving the first and second Milestones, the respective Default Values are set as Tracker Values entered by that user in the first and second Milestones.

### Tracker

- A Tracker refers to the additional information you wish to store when a Milestone is achieved.
- For example: "Email Address" would be the Tracker for a "Capturing Email Address" Milestone. "Country", "State" and "City" would the Trackers for a "User Location" Milestone.
- "Email Address" would be the Tracker for a "Capturing Email Address" Milestone.
- "Country", "State" and "City" would the Trackers for a "User Location" Milestone.
- You can also store pre-defined, static values in Trackers that may or may not be entered by a user.
Updated 10 months ago

- Creating Goals

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
