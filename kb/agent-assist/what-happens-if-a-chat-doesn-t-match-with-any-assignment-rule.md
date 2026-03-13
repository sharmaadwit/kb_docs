source_url: https://console-docs.gupshup.io/docs/what-happens-if-a-chat-doesnt-match-with-any-assignment-rule




<!-- agent-assist-golden:v8 -->
# What happens if a chat doesn't match with any assignment rule?

**Module**: Agent Assist

## What this feature does
Usually all the brands are created with a default assignment rule that insures that the chats are assigned to the default team. But in a scenario where default assignment rule is deleted, there comes a possibility when the chats don't match with any rules. Such chats are termed as "No Rule Matched" chats.

## Where to configure it
Agent Assist

## Exact path
Agent Assist

## Prerequisites
- _List required roles/access, teams, and any upstream configuration._

## Setup path
- _Add the click-path in Console (breadcrumbs)._

## Steps
1. Open Agent Assist.
2. _Add the click-path in Console (breadcrumbs)._

## Save/publish behavior
- _No save/publish step is required for this page unless explicitly stated in the UI._

## Validation
- _Run a quick test (new chat / assignment / workflow) and confirm expected behavior._

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- _Link this feature to adjacent modules (e.g., Business Hours ↔ Auto Replies; Assignment Rules ↔ Teams ↔ Views)._

## Module disambiguation
- _Add 1–2 bullets distinguishing this feature from adjacent settings to reduce retrieval drift._

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
