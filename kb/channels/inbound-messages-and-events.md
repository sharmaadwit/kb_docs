source_url: https://console-docs.gupshup.io/docs/inbound-messages-and-events

<!-- kb-golden:v7 -->
# Inbound Messages and Events

**Module**: Channels

## Definition
As a console user, if you configure a secondary URL on your WhatsApp self-serve application, you will receive inbound events including message status events and inbound messages. Here are some details:

## Procedure
### Exact path
Gupshup Console → Channels → Inbound Messages and Events

### Where to configure it
Gupshup Console → Channels → Inbound Messages and Events

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Channels**.
- Go to **Inbound Messages and Events**.

### Steps
1. Open Gupshup Console.
2. Go to **Channels**.
3. Go to **Inbound Messages and Events**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- You set a callback URL for your app, or you have used the proxy command to invoke your app on Gupshup Proxy bot phone number (+917834811114) to test the app in sandbox mode.

## Available options
- _List the key variants/toggles visible in the UI._

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
# Inbound Messages and Events

**Module**: Channels

## Overview
As a console user, if you configure a secondary URL on your WhatsApp self-serve application, you will receive inbound events including message status events and inbound messages. Here are some details:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
As a console user, if you configure a secondary URL on your WhatsApp self-serve application, you will receive inbound events including message status events and inbound messages. Here are some details:

Inbound Messages

An inbound message is a mobile message triggered from our WhatsApp Self Serve platform and routed to your callback URL. For example, an inbound event is triggered when:

- You set a callback URL for your app, or you have used the proxy command to invoke your app on Gupshup Proxy bot phone number (+917834811114) to test the app in sandbox mode.
- An end-user gives their consent (opt-in) to receive notifications from your WhatsApp Business API number.
Inbound Events

An inbound event Is a type of event which is triggered by our WhatsApp Self-Serve Platform to your callback URL. These are the events related to your WhatsApp business API.

Inbound events are classified in majorly four parts: User events, system events, message events, and billing events.

## Classification of events

Figure 01: Classification of events. Click on the image to zoom in and zoom out.

This section explains the inbound event type message you receive on your callback URL. It states that a customer has sent a message to your WhatsApp Business API phone number. Here, we will understand the different types of payloads for inbound messages.

## Common payload for all inbound events of type message

```
{   
  "app": "DemoApp", 
  "timestamp": 1580227766370,   
  "version": 2, 
  "type": "message",    
  "payload": {  
    "id": "ABEGkYaYVSEEAhAL3SLAWwHKeKrt6s3FKB0c",   
    "source": "918x98xx21x4",   
    "type": "text"|"image"|"file"|"audio"|"video"|"contact"|"location"|"button_reply"|"list_reply", 
    "payload": {    
      // Varies according to the type of payload.    
    },  
    "sender": { 
      "phone": "918x98xx21x4",  
      "name": "Drew",   
      "country_code": "91", 
      "dial_code": "8x98xx21x4" 
    },  
    "context": {    
      "id": "gBEGkYaYVSEEAgnPFrOLcjkFjL8",  
      "gsId": "9b71295f-f7af-4c1f-b2b4-31b4a4867bad"    
    }   
  } 
}
```

## Common payload object description

Key

Description

Sample

app

The name of the Gupshup app to which the customer has sent a message on WhatsApp

DemoAPI

timestamp

The time in UNIX timestamp when the message sent by the customer was received by Gupshup

1584898839530

version

Callback payload version

2

type

The type of inbound event

message

payload

The payload object represents the following:

- WhatsApp message ID
- Sender's phone number along with their country code
- The type of message
- Content of the message
See the payload object description for more information.

sender

The sender object represents the following: Name of the sender Phone number of the sender

See the sender object description for more information.

context

The context object is optional, it will only be included when someone replies to one of your messages. It contains information about the content of the original message, such as the Gupshup ID and WhatsApp ID of the message.

See the context object description for more information.

## The payload object description

Key

Description

Sample

id

The unique WhatsApp message identifier for the inbound message

ABEGkYaYVSEEAhAt2MgAKjL1qGe88OKyMQfM

source

The phone number of the customer who has sent the message on WhatsApp, number is in E.164 format

918x98xx21x4

type

The type of message received from the end user. Depending on 'type', the relevant message object will be received as part of the payload.

Must be one of these: text, image, file, audio, video, contact, and location.

text

payload

The payload object contains the inbound message content sent by the customer

See types of incoming message received documentation below

## The sender object description

## The context object description

## Event subscriptions

An event subscription is a registration that specifies a particular event is about to be performed. When the triggering event happens, it indicates that the event is important to the system.

Events that require subscription

Events that do not require subscription

System Events

- Template events
- Account events: tier-events, pndn-events, review-events, status-events, capability-events.
User Events

- Sandbox-start
- Opted-in
- Opted-out
Message Events

- Read
- Sent
- Delivered
- Delete
- Others
Message Events

- Enqueued
- Failed
- Mismatch
Message (User messages) Billing Events

## Notifications

Whenever a trigger event occurs, the WhatsApp Self-Serve Platform sees the event and sends a notification to your configured Webhook URL. There are two types of notifications you will receive on your webhook/ callback URL.

## Payload object

The following payload is common to all inbound notifications.

```
{
  "app": "DemoApp",
  "timestamp": 1580227766370,
  "version": 2,
  "type": "account-event"|"user-event"|"template-event"|"message-event"|"billing-event"|"message",
  "payload": # This payload object varies according to the value of the property "type"
}
```

## Description: Payload object

Key

Description

Example

app

The name of the Gupshup Access API app to which the customer has sent a message on WhatsApp.

DemoApp

timestamp

UNIX timestamp of the message sent by the customer that was received by Gupshup

1584898839530

version

The payload's version that was received on the callback.

2

type

The type of inbound notification.

Possible values:

- user-event
- system-event
- message-event
- billing-event
- message
user-event

payload

The payload object contains information of the respective notification type.

Refer inbound payload description for different events and messages.

For type: user-event

```
{   "phone":"918x98xx21x4","type":"sandbox-start"
}
```

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
