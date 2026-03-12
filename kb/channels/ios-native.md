source_url: https://console-docs.gupshup.io/docs/ios-native-sdk

<!-- kb-golden:v1 -->
# iOS Native

**Module**: Channels

## Definition
- iOS version 13 or above
- Xcode 14 or above

## Procedure
### Where to configure it
Gupshup Console → Channels → iOS Native

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Channels → iOS Native**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- Prerequisites
- Download the framework
- Add the framework
- Link the framework
- Grant Permissions
- Import GipKit into ViewModel class
- Get reference to GipKit in ViewModel class
- Getting the App ID

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Reference (from source)
<!-- procedural:v2 -->
# iOS Native

**Module**: Channels

## Overview
- iOS version 13 or above
- Xcode 14 or above
## Setup

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### Prerequisites

- iOS version 13 or above
- Xcode 14 or above
## Setup

### Download the framework

- Open terminal and enter the following command.
```
curl --user dev.nexus:devNexus -o GipKit-1.1.0.zip https://nexus.gupshup.tech/repository/iOS/GipKit/GipKit-1.1.0.zip
```

- Find the downloaded file and unzip it to get "GipKit.xcframework".
### Add the framework

- Drag the framework file into the project folder in Xcode.
- When prompted, select the options as shown below and click Finish.
### Link the framework

- Add the framework to the target of the application if not already done.
- Remember to select Embed & Sign under the Embed column.
### Grant Permissions

- GipKit requires camera permission to click and upload pictures. It uses Audio permission to convert Speech to Text and record video to upload to the chatbot.
- Add the following keys to Info tab on the project target.
- Privacy - Microphone Usage Description
- Privacy - Camera Usage Description
### Import GipKit into ViewModel class

```
import GipKit
```

### Get reference to GipKit in ViewModel class

```
let gipChat: GipChat = GipChat.shared
```

## Setting the App ID for gipChat

```
let appId: String = "de0fa..."

gipChat.setAppId(appId)
```

### Getting the App ID

- Log in to your Gupshup Console account and go to Web under Channels in the navigation bar on the left.
- The App ID can be located in the Embed URL as shown below.
## Setting the Developer Key

```
let devKey: String = "02FD..."

gipChat.setDevKey(devKey)
```

## Setting the User Name and User ID

- For logged in users, set the end customer's name and unique ID.
- For anonymous users, set the User Name and User ID to nil.
```
let userId: String = "some-user-id"
let userName: String = "some-user-name"

gipChat.setUserId(userId)
gipChat.setUserName(userName)
```

```
gipChat.setUserId(nil)
gipChat.setUserName(nil)
```

## Initializing the SDK

- The .initialize method takes a closure which returns true if the SDK was initialized successfully.
- If the initialization fails, the method returns false.
- Based on this value, appropriate actions can be taken.
```
gipChat.initialize { initialized in
       // if initialized is true, show/enable chat button
	// or make appropriate UI state decisions.
}
```

## Showing the chat screen

```
gipChat.show()
```

## Listening for error messages

- App can register a delegate and listen for error messages that the SDK can generate.
```
gipChat.setDelegate(self)
```

- Extend the ViewModel class with GipChatDelegate as shown below.
```
extension ViewModel: GipChatDelegate {
    func onError(message: String) {
        print(message)
    }
}
```

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
