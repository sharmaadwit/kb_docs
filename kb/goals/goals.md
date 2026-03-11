source_url: https://console-docs.gupshup.io/docs/goals
# Goals

## Goals

# Goals

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
