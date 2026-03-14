source_url: https://console-docs.gupshup.io/docs/chat-management-assignment-rules-chat-rules-slas-re-open-time






<!-- agent-assist-golden:v12 -->
# Chat Management: Assignment Rules

**Module**: Agent Assist

## Definition
`Assignment Rules` are part of chat management in Agent Assist and are used to assign chats to the appropriate agents or teams.

- The `Default Assignment Rule` assigns chats to agents or teams without specific assignment preferences.
- `Sticky Assignment` assigns reopened chats to the same agent who previously handled them.
- `External Assignment Rule` allows CRM-based assignment through an external API.

## Procedure
### Exact UI path
Agent Assist → Settings → Chat Management → Assignment Rules

### Steps
1. Open Agent Assist.
2. Navigate to the `Settings` tab on the bottom left side of the dashboard.
3. Select `Assignment Rules`.
4. Click `Add New Rule`.
5. Specify the name of the rule.
6. Add conditions, such as `Channel is equal to WhatsApp`.
7. Choose either `Sticky Assignment` or a `Team/Agent Name`.
8. Click `Save`.

### Validation / where to check
- Check whether the rule has been created and saved.
- For automatic assignment, make sure an `Agent Handover Node` has been added on the bot journey.

### Fields to configure
- `Rule name`
- Rule conditions
- `Sticky Assignment` or `Team/Agent Name`

### Save / publish / deploy behavior
- Click `Save` to save the rule.

## Prerequisites
- An `Agent Handover Node` on the bot journey is required for automatic assignment.

## Options / variants
- `Default Assignment Rule`
- `Sticky Assignment`
- `External Assignment Rule`
- Tag-based assignment

## Notes
- If agents are not available when a chat comes for assignment, the system retries assignment for the next 30 minutes.
- If agents become available during that time, the chat is assigned.
- Otherwise the chat moves to unassigned chats and the supervisor must assign it manually.

## Field mapping / schemas
- No payload schema is described on this page.

## Cross-module workflow docs
- Agent Assist tags can be used in assignment rules.
- Tags can also be mapped in the `Agent Handover` node in `Bot Studio`.

## Module disambiguation docs
- `Assignment Rules` handle team or agent assignment.
- `Chat Rules` are a separate concept on the same source page.
- `Sticky Assignment` controls reassignment behavior for reopened chats.

## Reference (from source)
- Tags can be created in `Settings > Tags` and then used in assignment-rule conditions.
