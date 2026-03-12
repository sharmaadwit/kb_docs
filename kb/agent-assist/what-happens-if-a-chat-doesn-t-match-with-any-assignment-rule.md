source_url: https://console-docs.gupshup.io/docs/what-happens-if-a-chat-doesnt-match-with-any-assignment-rule


<!-- agent-assist-golden:v2 -->
# What happens if a chat doesn't match with any assignment rule?

**Module**: Agent Assist

## What this feature does
Usually all the brands are created with a default assignment rule that insures that the chats are assigned to the default team. But in a scenario where default assignment rule is deleted, there comes a possibility when the chats don't match with any rules. Such chats are termed as "No Rule Matched" chats.

## Where to configure it
Agent Assist

## Setup path
- _Add the click-path in Console (breadcrumbs)._ 

## Steps
1. Open Agent Assist.
2. Configure the required fields.

## Save/publish behavior
- _No save/publish step is required for this page unless explicitly stated in the UI._

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Reference (from source)
### Overview
Usually all the brands are created with a default assignment rule that insures that the chats are assigned to the default team. But in a scenario where default assignment rule is deleted, there comes a possibility when the chats don't match with any rules. Such chats are termed as "No Rule Matched" chats.

### When to use
_Add the primary scenarios and personas._

### Details
Usually all the brands are created with a default assignment rule that insures that the chats are assigned to the default team. But in a scenario where default assignment rule is deleted, there comes a possibility when the chats don't match with any rules. Such chats are termed as "No Rule Matched" chats.

No Rule Matched chats can be easily identified on agent assist:

- Live Monitoring Dashboard: The dashboard as "No Rule Matched" metric that tells the number of chats that hasn't matched with any assignment rule.
- "Waiting for Assignment" View: Waiting on assignment chats view has all the chats that are in waiting for assignment. All the chats in this view are associated with a special tag that further describes a chat. Within this all the chats that have "No rules Matched" tags are the chats that have not matched with any assignment rule
- Filtering the chats based on the "No Rules Matched" tag: By clicking on "No Rules Matched" tag, the user will be redirected to the search filter where all the chats that havent matched with any assignment rules will be listed
By using the above features, the user will be able to know what kind of chats are not matching with assignment rules. This will help the user to rectify the assignment rules. Once assignment rules are rectified, the system will again try to reassign those chats based on the updated assignment rules automatically.

Note: All the chats that don't match with any assignment rules get closed automatically after 24 hours of inactivity
