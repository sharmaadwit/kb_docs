source_url: https://console-docs.gupshup.io/docs/trigger-event-node

<!-- kb-golden:v4 -->
# Trigger Event Node

**Module**: Bot Studio

## Definition
The Trigger Event Node is a newly introduced action node in the Journey Builder Canvas that empowers businesses to send custom internal events during live journey execution. These events are sent to the Event Manager(New Module on Console), Gupshup's centralized event tracking system, and can be seamlessly integrated with Personalize (Customer360) to update profile attributes for users.

## Procedure
### Exact path
Gupshup Console → Bot Studio → Trigger Event Node

### Where to configure it
Gupshup Console → Bot Studio → Trigger Event Node

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to Console Sidebar → Event Manager

### Steps
1. Open Gupshup Console.
2. Go to Console Sidebar → Event Manager
3. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- 📌 What is it?
- 🧭 How to Use
- Cart Abandonment Tracking
- Product Viewed Event
- Form Submission Completion
- User Opts-In for a Notification
- Optionally, toggle the Save in Personalize to update CDP Profile attributes using Event data
- Choose the Event Category (Custom only)
- Select your Event Name from the dropdown

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Trigger Event Node

**Module**: Bot Studio

## Overview
The Trigger Event Node is a newly introduced action node in the Journey Builder Canvas that empowers businesses to send custom internal events during live journey execution. These events are sent to the Event Manager(New Module on Console), Gupshup's centralized event tracking system, and can be seamlessly integrated with Personalize (Customer360) to update profile attributes for users.

## When to use
_Add the primary scenarios and personas._

## Setup path
- Go to Console Sidebar → Event Manager

## Step-by-step configuration
### 📌 What is it?

The Trigger Event Node is a newly introduced action node in the Journey Builder Canvas that empowers businesses to send custom internal events during live journey execution. These events are sent to the Event Manager(New Module on Console), Gupshup's centralized event tracking system, and can be seamlessly integrated with Personalize (Customer360) to update profile attributes for users.

### 🧭 How to Use

#### Step 1: Create a Custom Event in Event Manager

- Go to Console Sidebar → Event Manager
- Click "Add Event"
- Define Event Name and select source as Bot Studio
- Optionally, toggle the Save in Personalize to update CDP Profile attributes using Event data
- Map the Custom Property with the Profile Property
- Click "Save"
#### Step 2: Configure Trigger Event Node in Journey Builder

- Open or create a journey in Journey Builder
- Drag the Trigger Event Node from "Action Nodes" to the canvas
- Choose the Event Category (Custom only)
- Select your Event Name from the dropdown
- Map Local/Global Variables to event attributes
- Click "Save & Deploy"
#### Step 3: Runtime Behavior

- Event is fired on node execution
- Logged in Personalize if Profile attribute is updated
- No journey delay — continues asynchronously
- Profile attribute update can take up to 20 mins before they can be used with the updated value.
### ✅Use Cases

- Cart Abandonment Tracking Scenario: User drops off after adding items to cart. Event: cart_abandoned Outcome: Triggers a Customer360 update and enables an automated campaign to re-engage the user.(in roadmap)
#### Cart Abandonment Tracking

- Product Viewed Event Scenario: User browses a product in the journey. Event: product_viewed Outcome: Event logs the product details and can be used for retargeting ads or dynamic personalization.
#### Product Viewed Event

- Form Submission Completion Scenario: User completes a lead gen or feedback form. Event: form_submitted Outcome: Event updates Personalize profile and triggers internal CRM workflows or scoring.
#### Form Submission Completion

- User Opts-In for a Notification Scenario: User agrees to receive promotional updates. Event: opt_in_notification Outcome: Event gets stored in Customer360 and used for future segmentation.
#### User Opts-In for a Notification

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Optionally, toggle the Save in Personalize to update CDP Profile attributes using Event data
- - Click "Save"
- - Click "Save & Deploy"

**Last updated (from source)**: Updated 10 months ago
