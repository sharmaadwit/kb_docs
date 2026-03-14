source_url: https://console-docs.gupshup.io/docs/wait-for-event

<!-- kb-golden:v10 -->
# Wait for Event

**Module**: Bot Studio

## Definition
The Wait for Event Node is used to pause the bot’s execution and wait for a specific user input or a time-based trigger before proceeding. It helps maintain conversational context by holding the flow temporarily until the event occurs or the timeout duration expires.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Wait for Event

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Wait for Event**.
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
- Go to **Wait for Event**.

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
# Wait for Event

**Module**: Bot Studio

## Overview
The Wait for Event Node is used to pause the bot’s execution and wait for a specific user input or a time-based trigger before proceeding. It helps maintain conversational context by holding the flow temporarily until the event occurs or the timeout duration expires.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
## Overview

The Wait for Event Node is used to pause the bot’s execution and wait for a specific user input or a time-based trigger before proceeding. It helps maintain conversational context by holding the flow temporarily until the event occurs or the timeout duration expires.

This node can be configured to wait for:

- A user expression-based event (e.g., a reply or message)
- A time-based event (e.g., a fixed delay or interval)
Maximum Duration: 24 hours

## When to Use

Use the Wait for Event Node when the bot needs to pause and:

- Wait for a user message before proceeding to the next step.
- Introduce a time delay (e.g., follow-ups, confirmations, or automated actions).
- Handle asynchronous workflows where responses or updates may not be immediate.
By default:

- The timeout for user message events is 30 minutes.
- The timeout for time-based events is 3 hours.
If no event is received within the configured duration, the bot automatically moves to the timeout path (if defined) or ends the flow.

Note: For scenarios where you want to re-engage users who don’t respond to a prompt, use the new Inactivity Nudge feature instead of configuring a Wait for Event Node manually. The Inactivity Nudge can be added after any Prompt Node and automatically sends a reminder or message when the user does not reply within a specified time. This approach ensures better analytics tracking, improved UX consistency, and avoids dependency on manual time-based event handling.

## Wait for Event Node Elements

The node supports two types of event configurations:

### 1. User Message Event

This configuration allows the bot to pause until a user sends a message or input. It is most commonly used after prompts or questions where the bot expects a user reply before continuing.

Key Configurations:

- Wait Duration (Optional): Maximum time the bot will wait for user input before timing out. Default: 30 minutes Maximum: 24 hours
- Timeout Path: Defines the fallback or next node if the user does not respond within the given time.
Example Use Case: After asking, “Would you like to talk to an agent?”, the bot waits for a reply. If no response is received within 30 minutes, it moves to a timeout node or sends a reminder (preferably via the Inactivity Nudge feature).

### 2. Time-Based Event

This configuration allows the bot to automatically proceed after a fixed time interval, without waiting for user input. It is ideal for delayed actions, scheduled notifications, or follow-up messages.

Key Configurations:

- Time Interval / Custom Timeout: Duration after which the node should proceed. Default: 3 hours Maximum: 24 hours
- Next Node: The subsequent node that executes once the wait duration ends.
Example Use Case: A transactional bot confirms an order and uses a 2-hour time-based event to send an order status update automatically.

## Node Behavior Summary

## Best Practices

- Use User Message Events immediately after a prompt when the user’s response determines the next flow.
- Use Time-Based Events for delayed automation, reminders, or time-driven actions.
- Keep durations under 24 hours to prevent session expiration on channels like WhatsApp.
- Always configure a timeout path to avoid hanging conversations.
- Do not use Wait for Event Node for inactivity reminders. Use the Inactivity Nudge feature for this purpose.
## Example Scenarios

### Scenario 1: User Response Wait

Bot: “Would you like to subscribe to our newsletter?” → Wait for Event Node (User Message) → If user replies ‘Yes’ → Proceed to subscription node → If no reply in 30 minutes → Timeout path triggers fallback

### Scenario 2: Time-Based Reminder

Bot: “Your payment is being processed.” → Wait for Event Node (Time-Based Event - 2 hours) → After 2 hours → “Your payment has been confirmed.”

### Scenario 3: Inactivity Nudge (Recommended Alternative)

Bot: “Please share your preferred appointment time.” → Prompt Node (with Inactivity Nudge enabled) → If no reply within 15 minutes → Send “Are you still there?” reminder automatically

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 4 months ago
