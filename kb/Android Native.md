# Android Native

### Prerequisites
1. Android OS version 9.0 or above
2. Android Studio version 2022.3.1 or above

## Setup
- Add a custom repository to the dependency resolution block.

```groovy
// You can access this block in the "build.gradle" file at project level. 
dependencyResolutionManagement { 
    repositories { 
        google() 
        central() 
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

- Add the dependency:
```groovy
implementation 'io.gupshup:gipchat:1.1.0'
```

## Granting Permissions to the SDK
- Add the following permissions in your AndroidManifest.xml:
```xml
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" /> 
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" /> 
<uses-permission android:name="android.permission.RECORD_AUDIO" /> 
<uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
```

## Setting the App ID, Developer Key, User Name and User ID
```java
GipChat.setAppId(appId) 
GipChat.setUserName(userName) 
GipChat.setUserId(userId) 
GipChat.setDevKey(devKey)
```
- App ID: Gupshup Web channel's app ID
- User Name: The end customer's name
- User ID: The external/custom ID assigned to the end customer
