source_url: https://console-docs.gupshup.io/docs/manage-variables

<!-- kb-golden:v7 -->
# Manage Variables

**Module**: Bot Studio

## Definition
Variables in Journey Builder store and manage data dynamically within conversational journeys, enabling personalization, data manipulation, and efficient bot interactions.

## Procedure
### Exact path
Gupshup Console → Bot Studio → Manage Variables

### Where to configure it
Gupshup Console → Bot Studio → Manage Variables

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **Manage Variables**.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Manage Variables**.
4. Select the appropriate variable type.
5. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- Variable Types
- 1. Local Variables
- 2. Global Variables
- 3. System Variables
- 4. Constant Variables
- 5. CDP Variables
- How to Use
- Select the appropriate variable type.

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
Tables from the source:

| Variable Name | Description | Data Type |
| --- | --- | --- |
| event_type | Type of incoming event (user_input, ctx, ai_intent, etc.) | String |
| user_input | Keyword or button click payload sent by user (e.g., "Hi", Button "Yes") | String |
| channel | Channel from which the event/message was received (e.g., WhatsApp) | String |
| user_channel_id | Channel ID from which the event/message was received (e.g., WhatsApp) | String |
| payloadString | Complex JSON object containing metadata of the event | String |
| timeStampEpoch | Timestamp in epoch format | String |
| user_name | Name of the user | String |
| conversation_context_type | Context type of the conversation | String |
| conversation_context_id | Context ID of the conversation | String |
| ai_inference_payload | JSON payload from AI Backend | JSON |
| ai_intent | Identified intent from user message | String |
| payloadJson | JSON payload from the backend | JSON |
| event_id | Unique ID for the event | String |
| message_metadata | Additional message metadata | JSON |
| conversation_language | Language used in the conversation | String |

## Cross-module workflows
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Manage Variables

**Module**: Bot Studio

## Overview
Variables in Journey Builder store and manage data dynamically within conversational journeys, enabling personalization, data manipulation, and efficient bot interactions.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Overview

Variables in Journey Builder store and manage data dynamically within conversational journeys, enabling personalization, data manipulation, and efficient bot interactions.

Variables are categorized into five types:

- Local
- Global
- System
- Constant
- CDP
### Variable Types

#### 1. Local Variables

- Purpose: Store session-based information. Eg. : API Responses, User inputs etc.
- Lifecycle: Persist until the conversation ID resets at the backend (typically after 72 hours from the last user message).
- Data Types: String, Number, JSON
#### 2. Global Variables

- Purpose: Store persistent data associated with the user’s channel ID.
- Lifecycle: Persistent and does not clear automatically.
- Data Types: String, Number, JSON
#### 3. System Variables

- Purpose: Provide read-only system-generated information.

| Variable Name | Description | Data Type |
| --- | --- | --- |
| event_type | Type of incoming event (user_input, ctx, ai_intent, etc.) | String |
| user_input | Keyword or button click payload sent by user (e.g., "Hi", Button "Yes") | String |
| channel | Channel from which the event/message was received (e.g., WhatsApp) | String |
| user_channel_id | Channel ID from which the event/message was received (e.g., WhatsApp) | String |
| payloadString | Complex JSON object containing metadata of the event | String |
| timeStampEpoch | Timestamp in epoch format | String |
| user_name | Name of the user | String |
| conversation_context_type | Context type of the conversation | String |
| conversation_context_id | Context ID of the conversation | String |
| ai_inference_payload | JSON payload from AI Backend | JSON |
| ai_intent | Identified intent from user message | String |
| payloadJson | JSON payload from the backend | JSON |
| event_id | Unique ID for the event | String |
| message_metadata | Additional message metadata | JSON |
| conversation_language | Language used in the conversation | String |
#### 4. Constant Variables

- Purpose: Store values consistent across all users, typically used for static information like interest rates, discounts, or event dates.
- Lifecycle: Values are editable from the variable management interface and persist across all conversations until manually updated.
#### 5. CDP Variables

- Purpose: Fetch dynamic customer-specific attributes from the Personalize Module(also know as CDP) for real-time personalization.
- Lifecycle: Read-only and dynamically fetched from CDP, reflecting real-time updates.
### How to Use

- Open Manage Variables in the Journey Builder.
- Select the appropriate variable type.
- Create or select existing variables.
- Map variables directly into nodes for data handling or personalization.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 8 months ago
