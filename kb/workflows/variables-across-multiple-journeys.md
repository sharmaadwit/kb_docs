source_url: https://console-docs.gupshup.io/docs/manage-variables

<!-- kb-golden:v12 -->
# Workflow: Use variables across multiple journeys (Journey Builder)

**Module**: Workflows

## Definition
This page explains how to choose a variable type in Journey Builder when you need data to remain available beyond a single step.

## Open Manage Variables
1. Open `Manage Variables` in Journey Builder.
2. Create a new variable or select an existing variable.
3. Select the appropriate variable type.

## Variable Types
### Local Variables
- Data types: `String`, `Number`, `JSON`
- Persist until the conversation ID resets at the backend.
- Typical reset window: about `72 hours` from the last user message.
- Used for session-based information such as API responses and user inputs.

### Global Variables
- Data types: `String`, `Number`, `JSON`
- Persistent and does not clear automatically.
- Used to store persistent data associated with the user's channel ID.

### System Variables
- Read-only system-generated information.

Examples from the source:
- `event_type`
- `user_input`
- `channel`
- `user_channel_id`
- `payloadString`
- `timeStampEpoch`
- `user_name`
- `conversation_context_type`
- `conversation_context_id`
- `ai_inference_payload`
- `ai_intent`
- `payloadJson`
- `event_id`
- `message_metadata`
- `conversation_language`

### Constant Variables
- Editable from the variable-management interface.
- Persist across all conversations until manually updated.
- Used for static information such as interest rates, discounts, or event dates.

### CDP Variables
- Read-only and dynamically fetched from CDP.
- Reflect real-time updates.

## Choosing the Type
- Use `Local` for session-based information.
- Use `Global` for data that should persist for the user's channel ID.
- Use `Constant` for values that should stay the same across conversations until manually changed.
- Use `CDP` for dynamic customer-specific attributes from the Personalize module.

## Source Notes
- The source page documents variable types, lifecycle, and the `Manage Variables` entry point.
- It does not provide a separate multi-journey procedure beyond variable selection and usage.
