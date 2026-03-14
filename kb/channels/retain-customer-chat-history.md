source_url: https://console-docs.gupshup.io/docs/web-retain-customer-chat-history

<!-- kb-golden:v12 -->
# Retain Customer Chat History

**Module**: Channels

## Definition
This feature shows messages from a user's previous conversations in the Web chat widget for repeat visits from the same browser and device.

## Where It Is Configured
- A toggle is provided in the `Preferences` tab in `Settings`.

## Behavior
- Up to `255` latest messages are shown.
- Messages are stored on a `First In, First Out (FIFO)` basis.
- Once enabled, messages are stored indefinitely and encrypted using `AES-GCM`.
- By default, the toggle is disabled and customer chat history is not retained.

## What Happens When Disabled
- Disabling the toggle does not delete previous chat history that was already saved.
- If the toggle is disabled, new messages are not saved.

## Anonymous User Behavior
- For anonymous users, retained chat history is stored in the browser's local storage and not cookies.
- If an anonymous user clears browser local storage, chat history is deleted from the widget.
- If an anonymous user clears browsing history and cookies, there is no impact on chat history.

## Related Pre-Chat Form Behavior
From the `Pre-Chat Form` page:

- If Retain Customer Chat History is enabled, the Pre-Chat Form is shown to new anonymous users only once.
- Logged in users are shown the form every time regardless of this setting.

## Source Notes
- Primary source: `https://console-docs.gupshup.io/docs/web-retain-customer-chat-history`
- Additional source: `https://console-docs.gupshup.io/docs/web-pre-chat-form`
