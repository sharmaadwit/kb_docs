source_url: https://console-docs.gupshup.io/docs/android-native-sdk

<!-- kb-golden:v10 -->
# Android Native

**Module**: Channels

## Definition
- Android OS version 9.0 or above
- Android Studio version 2022.3.1 or above

## Procedure
### Exact UI path
Gupshup Console → Channels → Android Native

### Prerequisites
- Access to the target channel configuration in Gupshup Console.
- A connected bot/app if the channel must route traffic to Bot Studio.

### Fields to configure
- a custom repository to the dependency resolution block
- the following permissions in your project manifest file

### Steps
1. Open Gupshup Console.
2. Go to **Channels**.
3. Go to **Android Native**.
4. Add a custom repository to the dependency resolution block.
5. Add the following permissions in your project manifest file.
6. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Send a live test on the target channel and confirm the bot/channel behavior matches the configuration.

### Troubleshooting
- If channel behavior is wrong, confirm the correct channel/app is connected and the latest bot configuration is live.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Channels**.
- Go to **Android Native**.

## Options / variants
- Add a custom repository to the dependency resolution block.
- Add the following permissions in your project manifest file.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Identify the upstream module where this is configured and the downstream module where the outcome is verified.

## Module disambiguation docs
- Channel setup governs connectivity and channel features; bot logic is configured separately in **Bot Studio**.

## Reference (from source)
<!-- procedural:v2 -->
# Android Native

**Module**: Channels

## Overview
- Android OS version 9.0 or above
- Android Studio version 2022.3.1 or above
## Setup

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### Prerequisites

- Android OS version 9.0 or above
- Android Studio version 2022.3.1 or above
## Setup

- Add a custom repository to the dependency resolution block.
```
// You can access this block in the "build.gradle" file at project level.

dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
        maven {
            url = uri("https://nexus.gupshup.tech/repository/android")
            credentials {
                username = "dev.nexus"
                password = "devNexus"
            }
        }
    }
}
```

```
// You can access this block in "settings.gradle.kts" or "build.gradle.kts" file at project level depending on the project structure you are using.
// For more info, please visit: https://developer.android.com/build/remote-repositories#kts

dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
        maven {
            url = uri("https://nexus.gupshup.tech/repository/android")
            credentials {
                username = "dev.nexus"
                password = "devNexus"
            }
        }
    }
}
```

- Based on selected build configuration language during project creation, add the below dependency.
```
// Add the following lines to your project level build.gradle file and build/sync project.

implementation 'io.gupshup:gipchat:1.1.0'
```

```
// Add the following lines to your project level build.gradle file and build/sync project.

implementation("io.gupshup:gipchat:1.1.0")
```

## Granting Permissions to the SDK

- Add the following permissions in your project manifest file.
- The following code needs to be added in AndroidManifest.xml file for enabling upload file and images/media at the mobile application level.
```
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
```

## Setting the App ID, Developer Key, User Name and User ID

- The following code needs to added to set these details using GipChat class as shown below. App ID: Gupshup Web channel's app ID User Name (set only if available): The end customer's name User ID (set only if available): The external/custom ID assigned to the end customer
- App ID: Gupshup Web channel's app ID
- User Name (set only if available): The end customer's name
- User ID (set only if available): The external/custom ID assigned to the end customer
```
GipChat.setAppId(appId)
GipChat.setUserName(userName)
GipChat.setUserId(userId)
GipChat.setDevKey(devKey)
```

### Getting the App ID

- Log in to your Gupshup Console account and go to Web under Channels in the navigation bar on the left.
- The App ID can be located in the Embed URL as shown below.
## Initializing the SDK

### The App ID, User Name and User ID must be set before you initialize the SDK.

- To initialize the SDK, use the initialize method and pass context as shown below in code snippet. If SDK is successfully initialized, it will return the value as true in boolean format. You can store this value if you wish to update your mobile application UI or to show a re-initialization button after successful initialization.
- If SDK is successfully initialized, it will return the value as true in boolean format.
- You can store this value if you wish to update your mobile application UI or to show a re-initialization button after successful initialization.
```
// Add the following lines to your Activity/Application where you want to initialize the SDK.

GipChat.initialize(context) { value ->
   initialized = value
}
```

If you have already initialized the SDK, it can be re-initialized similarly by using the GipChat.initialize method.

## Showing the chat screen

- You can simply call GipChat.show() once the SDK is initialized successfully to take the user to the chat screen.
```
GipChat.show()
```

## Closing the chat session

- To close the chat session, call the GipChat.close() method of GipChat class.
```
GipChat.close()
```

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
