source_url: https://console-docs.gupshup.io/docs/web-retain-customer-chat-history

<!-- kb-golden:v11 -->
# Retain Customer Chat History

**Module**: Channels

## Definition
- Use this setting when you want repeat visitors to see previous web-widget conversations.
- The feature stores up to **255** of the latest customer and bot messages in the web widget.
- If you are asking **“Customers say old widget chats disappear after refresh. What settings control chat retention?”** -> check **Channels -> Retain Customer Chat History** first.

## Procedure
### Exact UI path
Gupshup Console -> Channels -> Retain Customer Chat History

### Where to configure it
- Open the web channel settings.
- Go to the chat-history retention setting in the widget preferences area.

### Prerequisites
- Access to the **Web channel** configuration.
- A web widget already installed so you can test the behavior after saving.

### Fields to configure
- **Retain Customer Chat History** toggle
- **Enable Authenticated Users** if your widget distinguishes logged-in users

### Steps
1. Open Gupshup Console.
2. Go to **Channels**.
3. Open **Retain Customer Chat History**.
4. Enable the chat-history retention toggle.
5. Enable **Authenticated Users** if required for your use case.
6. Save the widget settings.

### Validation / where to check
- Open the widget, exchange a few messages, then refresh or reopen the same widget.
- Confirm the old conversation still appears.
- Test both anonymous and authenticated-user behavior if your setup supports both.

### Troubleshooting
- If old chats disappear, confirm the **Retain Customer Chat History** toggle is enabled.
- If the issue affects anonymous users only, check whether browser local storage was cleared.
- If the toggle is disabled, new messages will not be retained for future sessions.
- Disabling the setting does not automatically remove messages that were already stored earlier.

### Save / publish / deploy behavior
- Save the widget configuration after changing retention settings.
- Re-test in the same browser after saving.

## Options / variants
- Up to **255** latest messages are shown on a FIFO basis.
- Anonymous-user history is stored in browser local storage.
- Authenticated-user behavior can be configured separately.

## Module disambiguation docs
- **Retain Customer Chat History** controls whether old widget conversations remain visible.
- **Pre-Chat Form** controls what the user must submit before starting a chat.
- **Security** controls allowed domains; it does not store conversation history.
