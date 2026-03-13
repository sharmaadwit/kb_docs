source_url: https://console-docs.gupshup.io/docs/lead-generation-goal

<!-- kb-golden:v9 -->
# Lead Generation

**Module**: Goals

## Definition
Let's take an example of a lead generation journey.

## Procedure
### Exact UI path
Gupshup Console → Goals → Lead Generation

### Steps
1. Open Gupshup Console.
2. Go to **Goals**.
3. Go to **Lead Generation**.
4. Select the "Lead Generation" Goal and "Capturing the name" Milestone from the respective dropdowns.
5. Click **Save** (or **Save & Deploy**) to apply changes.

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
- Go to **Goals**.
- Go to **Lead Generation**.

## Options / variants
- Select the "Lead Generation" Goal and "Capturing the name" Milestone from the respective dropdowns.

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
# Lead Generation

**Module**: Goals

## Overview
Let's take an example of a lead generation journey.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Let's take an example of a lead generation journey.

The user details being captured in the journey are name, phone number and email address in that exact order, without any chance of skipping.

### Milestones are sequential in nature. Their sequence is set as per creation, NOT implementation in journeys.

For example, if a Goal has been created with three Milestones in the sequence M1 followed by M2 followed by M3, their sequence remains the same even if M2 and M3 is implemented in a Goal node before M1.

### If a Milestone is skipped and a Milestone after it in the sequence of creation is achieved, the Tracker Values for that milestone are automatically filled with the respective Default Values against the user’s customer ID.

For example, if a user achieves the third Milestone without achieving the first and second Milestones, the respective Default Values are set as Tracker Values entered by that user in the first and second Milestones.

Your Goal for this journey can be named as "Lead Generation", meaning capturing all user details mentioned above.

Your milestones and trackers can be as follows:

- First, you will need to create the goal using the above mentioned details.
First, you will need to create the goal using the above mentioned details.

- Next, you need to insert a Goal Node in the journey right after the user's name has been captured.
Next, you need to insert a Goal Node in the journey right after the user's name has been captured.

- Store the user's name in a local variable (if not done already).
Store the user's name in a local variable (if not done already).

- Select the "Lead Generation" Goal and "Capturing the name" Milestone from the respective dropdowns.
Select the "Lead Generation" Goal and "Capturing the name" Milestone from the respective dropdowns.

- The "Name" tracker will automatically appear under Key Trackers along with a "Value" field. Enter the variable which stores the user's name in the "Value" field.
The "Name" tracker will automatically appear under Key Trackers along with a "Value" field. Enter the variable which stores the user's name in the "Value" field.

- Now, repeat steps 2 to 5 for the phone number and the email address as well.
Now, repeat steps 2 to 5 for the phone number and the email address as well.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
