source_url: https://console-docs.gupshup.io/docs/web-sync-browser-login-with-chat-widget
# CHANNELS

## Sync Browser Login with your Chat Widget

# Sync Browser Login with your Chat Widget

This provision allows you to sync the information of users who have logged in on your website with the Web chat widget.

- You can provide your unique customer IDs to authenticate anonymous users on the chat widget.
- These customer IDs can be set as the user IDs for the bot using the Login Function.
### To start using Functions, you need to insert the Embed Script at the "footer" tag or the end of "/body" tag of your website.

You can find the Embed Script when you the visit the Web channel under Channels. For a detailed guide on how to use functions, click here.

## Login Function

This Function sets the user ID for authenticating the user on the chat widget, thereby syncing the chat widget with the browser login.

```
window.gipMessengerPlugin.setUserId('YourUserId')
```

### You cannot use the special character underscore i.e. "_" in your specified user ID.

### The Login Function must be called again every time the user refreshes, reloads or revisits the webpage after closing it.

Not doing so will lead to the removal of the user ID you had assigned to the user.

## Logout Function

This Function removes the user ID from local storage. If a logged in user (plus authenticated on the chat widget) logs out from your website, the Logout Function should be called.

- This will start a new session on the chat widget as a fresh anonymous user.
- This will hide their chat history (if enabled) from the chat widget until they log in on the website again and the Login Function is called.
```
window.gipMessengerPlugin.removeUserId()
```

## Guidelines & Limitations

- If an anonymous user chats with the bot and then logs in on your website, their messages exchanged anonymously will not appear as chat history after they are authenticated on the chat widget.
- If a user authenticated on the chat widget closes the website and returns to the website again: If they are still logged in as per the website, the website must call the Login Function again to keep the user authenticated on the chat widget and fetch their chat history. If their logged in session has expired or timed out as per the website, the Logout Function must be caled by the website.
- If they are still logged in as per the website, the website must call the Login Function again to keep the user authenticated on the chat widget and fetch their chat history.
- If their logged in session has expired or timed out as per the website, the Logout Function must be caled by the website.
- If a logged in user (plus authenticated on the chat widget) clears their browsing history and cookies, there will be no impact on the authentication and the chat history.
- If a logged in user (plus authenticated on the chat widget) clears their browser’s local storage, they will be reverted back to an anonymous user and their chat history will be deleted from the chat widget.
Updated 10 months ago

- Chat Widget Functions
