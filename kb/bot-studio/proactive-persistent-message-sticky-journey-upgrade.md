source_url: https://console-docs.gupshup.io/docs/proactive-persistent-message-sticky-journey-upgrade

<!-- kb-golden:v10 -->
# Proactive Persistent Message (Sticky Journey Upgrade)

**Module**: Bot Studio

## Definition
For sticky journeys, the wait-for-event based nodes now features an improved and customizable experience. This ensures end users can return to an unfinished journey if the context changes before completion. Previously available only for Prompt Nodes, this feature now extends to Reply, Quick Reply, and List Nodes as well.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Proactive Persistent Message (Sticky Journey Upgrade)

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Proactive Persistent Message (Sticky Journey Upgrade)**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run the flow in **Test your Bot** and confirm the expected node/path executes.
- If the change must affect live traffic, use **Save & Deploy** and verify on the target channel.

### Troubleshooting
- If behavior is unchanged, confirm you updated the correct node and used **Save & Deploy** for live channels.
- If the wrong branch/path runs, re-check conditions, connected nodes, and fallback connectors.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Bot Studio**.
- Go to **Proactive Persistent Message (Sticky Journey Upgrade)**.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Proactive Persistent Message (Sticky Journey Upgrade)

**Module**: Bot Studio

## Overview
For sticky journeys, the wait-for-event based nodes now features an improved and customizable experience. This ensures end users can return to an unfinished journey if the context changes before completion. Previously available only for Prompt Nodes, this feature now extends to Reply, Quick Reply, and List Nodes as well.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
## Introduction

For sticky journeys, the wait-for-event based nodes now features an improved and customizable experience. This ensures end users can return to an unfinished journey if the context changes before completion. Previously available only for Prompt Nodes, this feature now extends to Reply, Quick Reply, and List Nodes as well.

Nodes marked as persistent will now have the option to add a Proactive Persistent Message. This message, sent by the bot Pro-actively when the unfinished journey is resumed, helps users understand the resumed context and continue the journey seamlessly.

## How to use the feature:

NOTE - The 'Persistent' message feature is available only when 'Sticky Journey' is enabled.

There are just 2 easy steps to use the persistent feature in your journey.

Steps:

- Check the 'Persistent' box ON in the node. This will add a 'Persistent Message' option. Click on it.
- This will add a 'Persistent Message' text box, where you can add the message which you want to show the user when the unfinished journey is resumed.
## Use Cases:

Here are some use cases that demonstrate the potential applications of Proactive Persistent Message:

1. Customer Support Follow-up

Scenario: A customer initiates a support request but doesn't complete the interaction. Proactive Persistent Message: The bot sends a reminder message to the customer to resume the support request with the current context. Benefit: Ensures issues are resolved efficiently by reminding customers to complete their support journey, reducing abandoned requests.

2. Abandoned Cart Recovery

Scenario: A user adds items to their shopping cart but leaves the site before completing the purchase. Proactive Persistent Message: The bot sends a message reminding the user to complete their purchase, with a summary of the items in the cart. Benefit: Increases conversion rates by prompting users to finalize their purchase, reducing cart abandonment.

3. Incomplete Registration or Onboarding

Scenario: A user starts the registration or onboarding process but doesn't finish it. Proactive Persistent Message: The bot sends a message encouraging the user to complete the process, providing context on the steps left. Benefit: Enhances user acquisition by ensuring more users complete the registration or onboarding process.

4. Service Booking Confirmation

Scenario: A user initiates a service booking but leaves before confirming the appointment. Proactive Persistent Message: The bot sends a message prompting the user to confirm or reschedule the booking. Benefit: Improves booking rates and reduces missed appointments by ensuring users complete the booking process.

5. Feedback and Survey Completion

Scenario: A user starts a feedback form or survey but doesn't finish it. Proactive Persistent Message: The bot sends a message reminding the user to complete the feedback or survey with context about the remaining questions. Benefit: Enhances the quality and quantity of feedback collected, providing valuable insights for the business.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
