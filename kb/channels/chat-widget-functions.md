source_url: https://console-docs.gupshup.io/docs/web-chat-widget-functions

<!-- kb-golden:v9 -->
# Chat Widget Functions

**Module**: Channels

## Definition
Functions are custom events that allow greater control over the visibility and interaction of the Web chat widget integrated on your website.

## Procedure
### Exact UI path
Gupshup Console → Channels → Chat Widget Functions

### Steps
1. Open Gupshup Console.
2. Go to **Channels**.
3. Go to **Chat Widget Functions**.
4. Enable Authenticated Users.
5. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- _Run a quick smoke test and confirm expected behavior._

### Fields to configure
- _List the fields/inputs you must set in the UI (and expected format)._

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- ### You can call only 1 Function at a time.

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Channels**.
- Go to **Chat Widget Functions**.

## Options / variants
- <button class="button" id="toggleChatButton">Toggle Chat Box</button>
- Enable Authenticated Users

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation docs
- Channel setup governs connectivity and channel features; bot logic is configured separately in **Bot Studio**.

## Reference (from source)
<!-- procedural:v2 -->
# Chat Widget Functions

**Module**: Channels

## Overview
Functions are custom events that allow greater control over the visibility and interaction of the Web chat widget integrated on your website.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Functions are custom events that allow greater control over the visibility and interaction of the Web chat widget integrated on your website.

### Before using Functions, you need to insert the Embed Script at the "footer" tag or the end of "/body" tag of your website.

You can find the Embed Script when you the visit the Web channel under Channels in your Gupshup Conversation Cloud account.

## List of Functions

## How to use Functions?

### Functions will work only after the chat widget is loaded on your website.

Please check the availability of the chat widget on your website before you call a Function.

### You can call only 1 Function at a time.

If you wish to call multiple Functions, please add a delay between the Function calls.

Here’s a simple HTML and CSS example of how you might use these Functions on your website:

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Widget Integration</title>
</head>
<body>
    <h1>Chat Widget Integration</h1>
    <button class="button" id="showChatButton">Show Chat Widget</button>
    <button class="button" id="hideChatButton">Hide Chat Widget</button>
    <button class="button" id="toggleChatButton">Toggle Chat Box</button>
    <button class="button" id="maximizeChatButton">Maximize Chat</button>
    <button class="button" id="minimizeChatButton">Minimize Chat</button>
    <button class="button" id="setUserIdButton">Set User ID</button>
    <button class="button" id="removeUserIdButton">Remove User ID</button>

    <script id="gs-sdk" src="https://web-widget.gupshup.io/v3/demo/static/js/sdk.js" appId="YOUR_APP_ID" ref="ar">
        
    </script>
    
    <script>
        
        window.onload = function() {
        
           // Listen for the custom event when gipMessengerPlugin is Ready
            window.addEventListener("gipMessengerPluginReady", function () {
                window.gipMessengerPlugin.hideChatWidget();
            });
            
            // Event listeners for custom buttons to control chat widget
            document.getElementById('showChatButton').addEventListener('click', function() {
                window.gipMessengerPlugin.showChatWidget();
            });

            document.getElementById('hideChatButton').addEventListener('click', function() {
                window.gipMessengerPlugin.hideChatWidget();
            });

            document.getElementById('toggleChatButton').addEventListener('click', function() {
                window.gipMessengerPlugin.toggleChatWidget();
            });

            document.getElementById('maximizeChatButton').addEventListener('click', function() {
                window.gipMessengerPlugin.maximizeChat();
            });

            document.getElementById('minimizeChatButton').addEventListener('click', function() {
                window.gipMessengerPlugin.minimizeChat();
            });

            document.getElementById('setUserIdButton').addEventListener('click', function() {
                window.gipMessengerPlugin.setUserId('USER_ID');
            });

            document.getElementById('removeUserIdButton').addEventListener('click', function() {
                window.gipMessengerPlugin.removeUserId();
            });
        };
    </script>
</body>
</html>
```

Web View rendered by the above code:

- You can click the buttons to trigger the respective functions. For example, if you click the Maximize Chat button, the chat widget will be opened (maximized) without the need to click on the web chat widget icon.
- For example, if you click the Maximize Chat button, the chat widget will be opened (maximized) without the need to click on the web chat widget icon.
Updated 10 months ago

- Enable Authenticated Users

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
