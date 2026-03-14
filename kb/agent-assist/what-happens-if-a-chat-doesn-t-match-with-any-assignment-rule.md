source_url: https://console-docs.gupshup.io/docs/what-happens-if-a-chat-doesnt-match-with-any-assignment-rule







<!-- agent-assist-golden:v11 -->
# What happens if a chat doesn't match with any assignment rule?

**Module**: Agent Assist

## What this feature does
Usually all the brands are created with a default assignment rule that insures that the chats are assigned to the default team. But in a scenario where default assignment rule is deleted, there comes a possibility when the chats don't match with any rules. Such chats are termed as "No Rule Matched" chats.

## Exact UI path
Agent Assist

## Prerequisites
- Access to the relevant Agent Assist module/page.

## Setup path
- _Add the click-path in Console (breadcrumbs)._

## Fields to configure
- No explicit fields were identified in the source; use the controls shown on this page.

## Steps
1. Open Agent Assist.
2. _Add the click-path in Console (breadcrumbs)._

## Validation / where to check
- Run a quick test and confirm the expected behavior in Agent Assist.

## Save / publish / deploy behavior
- No save/publish step is required for this page unless explicitly stated in the UI.

## Troubleshooting
- If something does not work as expected, re-check the exact path, required fields, and save step.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

## Cross-module workflow docs
- Identify the upstream Agent Assist setting and the downstream chat/reporting behavior it affects.

## Module disambiguation docs
- Distinguish this page from adjacent Agent Assist settings before troubleshooting elsewhere.

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
