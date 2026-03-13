source_url: https://console-docs.gupshup.io/docs/web-retain-customer-chat-history

<!-- kb-golden:v7 -->
# Retain Customer Chat History

**Module**: Channels

## Definition
This feature allows you to show the messages from a user's previous conversations in the Web chat widget for repeat visits from the same browser and device. A toggle is provided in the Preferences tab in Settings to enable this feature.

## Procedure
### Exact path
Gupshup Console → Channels → Retain Customer Chat History

### Where to configure it
Gupshup Console → Channels → Retain Customer Chat History

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Channels**.
- Go to **Retain Customer Chat History**.

### Steps
1. Open Gupshup Console.
2. Go to **Channels**.
3. Go to **Retain Customer Chat History**.
4. Enable Authenticated Users.
5. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- By default, the toggle is disabled and the customer chat history is NOT retained.
- Enable Authenticated Users

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation
- Channel setup governs connectivity and channel features; bot logic is configured separately in **Bot Studio**.

## Reference (from source)
<!-- procedural:v2 -->
# Retain Customer Chat History

**Module**: Channels

## Overview
This feature allows you to show the messages from a user's previous conversations in the Web chat widget for repeat visits from the same browser and device. A toggle is provided in the Preferences tab in Settings to enable this feature.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
This feature allows you to show the messages from a user's previous conversations in the Web chat widget for repeat visits from the same browser and device. A toggle is provided in the Preferences tab in Settings to enable this feature.

### The maximum number of customer + bot messages stored for a single user will be 255.

Users will be able to see up to 255 latest messages they have exchanged in the chat widget as the messages are stored on a First In, First Out (FIFO) basis.

- By default, the toggle is disabled and the customer chat history is NOT retained.
- Once enabled, the messages are stored indefinitely and encrypted using the AES-GCM encryption.
- For retaining customer chat history of anonymous users, details are stored in the browser’s local storage and not cookies. If an anonymous user clears their browsing history and cookies, there will be no impact on their chat history. If an anonymous user clears their browser’s local storage, their chat history will be deleted from the chat widget.
- If an anonymous user clears their browsing history and cookies, there will be no impact on their chat history.
- If an anonymous user clears their browser’s local storage, their chat history will be deleted from the chat widget.
- If the “Retain Customer Chat History” toggle is disabled, new messages will not be saved for any type of user (anonymous or authenticated).
- Disabling the toggle also does not delete the previous chat history i.e. messages already saved for a user will always appear for them in future conversations.
Updated 10 months ago

- Security
- Enable Authenticated Users

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
