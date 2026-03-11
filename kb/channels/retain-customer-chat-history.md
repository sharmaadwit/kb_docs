source_url: https://console-docs.gupshup.io/docs/web-retain-customer-chat-history
# CHANNELS

## Retain Customer Chat History

# Retain Customer Chat History

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
