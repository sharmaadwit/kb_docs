source_url: https://console-docs.gupshup.io/docs/react-native-sdk

<!-- kb-golden:v9 -->
# React Native

**Module**: Channels

## Definition
- React Native CLI
- Node.js (v18 or above)
- Android Studio and Xcode installed
- A working React Native project

## Procedure
### Exact UI path
Gupshup Console → Channels → React Native

### Steps
1. Open Gupshup Console.
2. Go to **Channels**.
3. Go to **React Native**.
4. add(GipChatModule()).
5. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- const [userId, setUserId] = useState('Test-User-Id-1234');
- <Text style={styles.title}>GipSDK Demo Test</Text>

### Fields to configure
- _List the fields/inputs you must set in the UI (and expected format)._

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- message(exception.message ?: "Error occurred..")
- // Packages that cannot be autolinked yet can be added manually here, for example:
- GipIOSService.initialize((error: any, success: boolean) => {
- if (error) {
- console.error('Initialization failed:', error);
- GipIOSService.onError((error: any, message: string) => {

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Channels**.
- Go to **React Native**.

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- `{initialized ? 'Re-Initialize' : 'Initialize'}`

## Cross-module workflow docs
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation docs
- Channel setup governs connectivity and channel features; bot logic is configured separately in **Bot Studio**.

## Reference (from source)
<!-- procedural:v2 -->
# React Native

**Module**: Channels

## Overview
- React Native CLI
- Node.js (v18 or above)
- Android Studio and Xcode installed
- A working React Native project
## Installing the SDK

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### Prerequisites

- React Native CLI
- Node.js (v18 or above)
- Android Studio and Xcode installed
- A working React Native project
## Installing the SDK

### Android Setup

- Complete the steps required for Android Native Setup first before proceeding.
#### Platform-specific Configuration

- Create GipChatService.kt and GipChatModule.kt under app/src/main/java/com/<YourProjectName>
- import io.gupshup.gipchat.GipChat inside MainApplication.kt and use it like add(GipChatModule())
```
package com.awesomeproject
import android.view.View
import com.facebook.react.ReactPackage
import com.facebook.react.bridge.NativeModule
import com.facebook.react.bridge.ReactApplicationContext
import com.facebook.react.uimanager.ReactShadowNode
import com.facebook.react.uimanager.ViewManager

class GipChatModule: ReactPackage {
    override fun createNativeModules(reactContext: ReactApplicationContext): List<NativeModule> {
        val modules = ArrayList<NativeModule>()
        modules.add(GipChatService(reactContext))
        return modules
    }

    override fun createViewManagers(reactContext: ReactApplicationContext): List<ViewManager<View, ReactShadowNode<*>>> {
        return emptyList()
    }
}
```

```
package com.awesomeproject
import com.facebook.react.bridge.Callback
import com.facebook.react.bridge.ReactApplicationContext
import com.facebook.react.bridge.ReactContextBaseJavaModule
import com.facebook.react.bridge.ReactMethod
import io.gupshup.gipchat.GipChat
import io.gupshup.gipchat.listener.GipChatListener
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.jsonObject

class GipChatService(private val reactContext: ReactApplicationContext) : ReactContextBaseJavaModule(reactContext) {
    private val gipChat=GipChat
    private val listener = Listener()
    init {
        gipChat.setListener(listener)
    }
    override fun getName(): String {
        return "GipChatModule"
    }

    @ReactMethod
    fun setAppId(appId: String) {
        gipChat.setAppId(appId)
    }
  
    @ReactMethod
    fun setDevKey(devKey: String) {
        gipChat.setDevKey(devKey)
    }

    @ReactMethod
    fun setUserName(userName: String) {
        gipChat.setUserName(userName)
    }

    @ReactMethod
    fun setUserId(userId: String) {
        gipChat.setUserId(userId)
    }

    @ReactMethod
    fun initialize(callback: Callback?) {
        gipChat.initialize(reactContext) { initialized ->
            callback?.invoke(initialized)
        }
    }

    @ReactMethod
    fun onError(callback: Callback?) {
        listener.message = {message ->
            callback?.invoke(message)
        }
    }

    @ReactMethod
    fun show() {
        gipChat.show()
    }

    @ReactMethod
    fun close() {
        gipChat.close()
    }

    @ReactMethod
    fun setListener(listener: GipChatListener) {
        gipChat.setListener(listener)
    }

    inner class Listener: GipChatListener {
        var message: (String) -> Unit = {}
        override fun onError(exception: Exception) {
            exception.message?.let {
                try {
                    val json = Json.parseToJsonElement(it).jsonObject
                    if (json["message"] != null) {
                        message(json["message"].toString().replace("\"", ""))
                        return
                    }
                } catch (e: Exception) {
                    message(it)
                    return
                }
            }
            message(exception.message ?: "Error occurred..")
        }
        override fun onInitialized() {
            //println("Initialized")
        }

    }
}
```

```
package com.awesomeproject
import android.app.Application
import com.facebook.react.PackageList
import com.facebook.react.ReactApplication
import com.facebook.react.ReactHost
import com.facebook.react.ReactNativeHost
import com.facebook.react.ReactPackage
import com.facebook.react.defaults.DefaultNewArchitectureEntryPoint.load
import com.facebook.react.defaults.DefaultReactHost.getDefaultReactHost
import com.facebook.react.defaults.DefaultReactNativeHost
import com.facebook.soloader.SoLoader
import io.gupshup.gipchat.GipChat

class MainApplication : Application(), ReactApplication {

  override val reactNativeHost: ReactNativeHost =
      object : DefaultReactNativeHost(this) {
        override fun getPackages(): List<ReactPackage> =
            PackageList(this).packages.apply {
              // Packages that cannot be autolinked yet can be added manually here, for example:
              // add(MyReactNativePackage())
                add(GipChatModule())
            }

        override fun getJSMainModuleName(): String = "index"

        override fun getUseDeveloperSupport(): Boolean = BuildConfig.DEBUG

        override val isNewArchEnabled: Boolean = BuildConfig.IS_NEW_ARCHITECTURE_ENABLED
        override val isHermesEnabled: Boolean = BuildConfig.IS_HERMES_ENABLED
      }

  override val reactHost: ReactHost
    get() = getDefaultReactHost(applicationContext, reactNativeHost)

  override fun onCreate() {
    super.onCreate()
    SoLoader.init(this, false)
    if (BuildConfig.IS_NEW_ARCHITECTURE_ENABLED) {
      // If you opted-in for the New Architecture, we load the native entry point for this app.
      load()
    }
  }
}
```

### iOS Native Setup

- Complete the steps required for the iOS Native Setup first before proceeding.
- Create a swift file named "RNGipChat.swift" and paste the below code.
```
import Foundation
import React
import GipKit

@objc(RNGipChat)
class RNGipChat: NSObject {

   let gipChat = GipChat.shared
    let delegate = Delegate()
  override init() {
   gipChat.setDelegate(delegate)
 }
    @objc
   static func requiresMainQueueSetup() -> Bool {
       return true
   }

   @objc
   func setAppId(_ appId: String) {
     gipChat.setAppId(appId)
   }

   @objc
   func setDevKey(_ devKey: String) {
     gipChat.setDevKey(devKey)
   }
  
   @objc
   func setUserName(_ userName: String) {
     gipChat.setUserName(userName)
   }

   @objc
   func setUserId(_ userId: String) {
     gipChat.setUserId(userId)
   }

   @objc
     func initialize(_ callback: @escaping RCTResponseSenderBlock) {
       gipChat.initialize { success in
             callback([NSNull(), success])
         }
     }
    @objc
   func onError(_ callback: @escaping RCTResponseSenderBlock) {
     delegate.errorMessage = { message in
       callback([NSNull(), message])
     }
   }

   @objc
   func show() {
     gipChat.show()
   }

   @objc
   func close() {
     gipChat.close()
   }
  class Delegate: GipChatDelegate {
     var errorMessage: (String) -> Void = { message in }
    
     func onError(message: String) {
         errorMessage(message)
     }
 }
}
```

## Initializing the SDK

- Create a GipChat.tsx service file add all the methods to expose to the App.tsx
```
import {NativeModules, Platform} from 'react-native';

const GipService = NativeModules.GipChatModule;
const GipIOSService = NativeModules.RNGipChat;

const setAppId = (appId: string) => {
 if (Platform.OS === 'android') {
   GipService.setAppId(appId);
 } else {
   GipIOSService.setAppId(appId);
 }
};

const setDevKey = (devKey: string) => {
 if (Platform.OS === 'android') {
   GipService.setDevKey(devKey);
 } else {
   GipIOSService.setDevKey(devKey);
 }
};

// Set User Name only if available

const setUserName = (userName: string) => {
 if (Platform.OS === 'android') {
   GipService.setUserName(userName);
 } else {
   GipIOSService.setUserName(userName);
 }
};

// Set User ID only if available

const setUserId = (userId: string) => {
 if (Platform.OS === 'android') {
   GipService.setUserId(userId);
 } else {
   GipIOSService.setUserId(userId);
 }
};

const initialize = (callback: (success: boolean) => void) => {
 if (Platform.OS === 'android') {
   GipService.initialize((success: boolean) => {
     callback(success);
   });
 } else {
   GipIOSService.initialize((error: any, success: boolean) => {
     if (error) {
       console.error('Initialization failed:', error);
       callback(false);
     } else {
       callback(success);
     }
   });
 }
};

const onError = (callback: (message: string) => void) => {
 if (Platform.OS === 'android') {
   GipService.onError((message: string) => {
     callback(message)
   });
 } else {
   GipIOSService.onError((error: any, message: string) => {
     callback(message)
   });
 }
}

const show = () => {
 if (Platform.OS === 'android') {
   GipService.show();
 } else {
   GipIOSService.show();
}
};
export default {setAppId, setUserName, setUserId, initialize, show, onError};
```

## Using the SDK Features

- After successful initialization, you can use the SDK's features in your React Native components(App.tsx).
```
import React, {useState} from 'react';
import {
 SafeAreaView,
 StyleSheet,
 Text,
 TouchableOpacity,
 View,
} from 'react-native';
import {ActivityIndicator, TextInput} from '@react-native-material/core';
import GipChat from './GipChat';

function App(): React.JSX.Element {
 const [isLoading, setIsLoading] = useState(false);
 const [appId, setAppId] = useState('c5453fbf-95e6-4330-9e14-28a85d3ea6a5');
 const [devKey, setDevKey] = useState('02FD...');
 const [userName, setUserName] = useState('Gaurav');
 const [userId, setUserId] = useState('Test-User-Id-1234');
 const [initialized, setInitialized] = useState(false);

 const handleInitialize = () => {
   if (!appId && !userName && !userId) {
     console.log('Please fill the fields');
     return;
   }
   setIsLoading(true);
   GipChat.setAppId(appId);
   GipChat.setDevKey(devKey);
   GipChat.setUserName(userName);
   GipChat.setUserId(userId);
   GipChat.initialize((success: boolean) => {
     if (success) {
       console.log('Initialization success :: ', success);
       setInitialized(true);
     } else {
     //  console.log('Something went wrong!!');
     }
     setIsLoading(false);
   });
   GipChat.onError((message: string) => {
     console.log(message);
   });
 };

 const handleStartChat = () => {
   setIsLoading(true);
   GipChat.show();
   setIsLoading(false);
 };

 return (
   <SafeAreaView style={styles.container}>
     <View style={{height: 150, alignItems: 'center', paddingTop: 50}}>
       <Text style={styles.title}>GipSDK Demo Test</Text>
     </View>

     <View style={styles.form}>
       <TextInput
         style={styles.input}
         label="App Id"
         value={appId}
         onChangeText={setAppId}
       />
       <TextInput
         style={styles.input}
         label="Developer Key"
         value={devKey}
         onChangeText={setDevKey}
       />
       <TextInput
         style={styles.input}
         label="User Name"
         value={userName}
         onChangeText={setUserName}
         color="#904a3f"
       />
       <TextInput
         style={styles.input}
         label="User Id"
         value={userId}
         onChangeText={setUserId}
         color="#904a3f"
       />
       <View style={{alignItems: 'center', marginTop: 10}}>
         <TouchableOpacity
           style={styles.buttonContainer}
           onPress={handleInitialize}>
           <Text style={styles.text}>
             {initialized ? 'Re-Initialize' : 'Initialize'}
           </Text>
         </TouchableOpacity>
       </View>
     </View>

     <View style={{flex: 1, justifyContent: 'center'}}>
       <TouchableOpacity
         style={{...styles.buttonContainer, opacity: initialized ? 1 : 0.4}}
         onPress={handleStartChat}
         disabled={isLoading || !initialized}>
         {isLoading ? (
           <ActivityIndicator animating={isLoading} />
         ) : (
           <Text style={styles.text}>Start Chat</Text>
         )}
       </TouchableOpacity>
     </View>
   </SafeAreaView>
 );
}

const styles = StyleSheet.create({
 container: {
   flex: 1,
   alignItems: 'center',
   backgroundColor: '#fff',
 },
 form: {
   width: '80%',
 },
 label: {
   marginTop: 5,
   marginBottom: 2,
 },
 input: {
   borderBottomColor: '#999',
   marginBottom: 10,
 },
 buttonContainer: {
   height: 45,
   flexDirection: 'row',
   justifyContent: 'center',
   alignItems: 'center',
   marginBottom: 20,
   borderRadius: 30,
   backgroundColor: '#f8f2f4',
   width: 200,
   shadowColor: 'rgba(0,0,0, .99)', // IOS
   shadowOffset: {height: 1, width: 1}, // IOS
   shadowOpacity: 1, // IOS
   shadowRadius: 1, //IOS
   elevation: 1, // Android
 },
 title: {
   fontSize: 24,
   color: '#000',
   fontWeight: 'bold',
 },
 text: {
   color: '#8b4d43',
   fontSize: 16,
 },
});

export default App;
```

## Testing and Debugging

### Android Testing

Run the app on an Android emulator or device:

npx react-native run-android

### iOS Testing

Run the app on an iOS emulator or device:

npx react-native run-ios

### Debugging

- Use console.log for debugging.
- Use the React Native Debugger or Flipper for more advanced debugging features.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
