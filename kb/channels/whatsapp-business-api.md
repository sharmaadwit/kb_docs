source_url: https://console-docs.gupshup.io/docs/whatsapp-business-api

<!-- kb-golden:v9 -->
# WhatsApp Business API

**Module**: Channels

## Definition
Gupshup's WhatsApp Business API provides you APIs to send free form messages or session messages and template messages (utility/marketing/authentication) to users on WhatsApp. Both of these types of messages are together referred as 'Outbound Messages'

## Procedure
### Exact UI path
Gupshup Console → Channels → WhatsApp Business API

### Steps
1. Open Gupshup Console.
2. Go to **Channels**.
3. Go to **WhatsApp Business API**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- _Run a quick smoke test and confirm expected behavior._

### Fields to configure
- _List the fields/inputs you must set in the UI (and expected format)._

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- Let's have a look at the error codes for the above outbound message APIs:
- Message sending failed because of insufficient balance.
- 1004 - Message sending failed as user is inactive for session message and template messaging is disabled.
- 1005 - Message sending failed as user is inactive for session message and template did not match
- 1006 - Message sending failed as user is inactive for session message and not opted in for template message
- 1007 - Message sending failed as user is inactive for session message, not opted in for template message and template did not match
- ### For any other error code, click here.

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Channels**.
- Go to **WhatsApp Business API**.

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- `{"id": "c6aecef6-bcb0-4fb1-8100-28c094e3bc6b","params": ["Agent","Local Address","Tracking code"]}`

## Cross-module workflow docs
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation docs
- Channel setup governs connectivity and channel features; bot logic is configured separately in **Bot Studio**.

## Reference (from source)
<!-- procedural:v2 -->
# WhatsApp Business API

**Module**: Channels

## Overview
Gupshup's WhatsApp Business API provides you APIs to send free form messages or session messages and template messages (utility/marketing/authentication) to users on WhatsApp. Both of these types of messages are together referred as 'Outbound Messages'

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Gupshup's WhatsApp Business API provides you APIs to send free form messages or session messages and template messages (utility/marketing/authentication) to users on WhatsApp. Both of these types of messages are together referred as 'Outbound Messages'

Here we will look at the different types of outbound messages you can send using Gupshup's API

## Session messaging

You can send Session messages to Active users only. When a user sends a message to your WhatsApp Business API, they become an active user. A session starts from the latest user message. Sessions remain Active for 24 hours.

You can use our send message API for sending session messages

## Send message API

The following guide will help you understand Gupshup's send message API. Using a single endpoint, you can send various messages to users on WhatsApp.

### API Endpoint

### Headers

### Request body

channel

string

The channel for sending messages.

whatsapp

source

string

For Live apps - Your registered WhatsApp Business API phone number.For Sandbox apps - Gupshup's sandbox/proxy number 917834811114

The number must be in E. 164 format.

917834811114

src.name

string

The Gupshup app name registered against the phone number provided in the API.

DemoAPI

destination

string

User's phone number.

919876543210

message

object

The message object will change depending on the type of message.

Refer message object description

disablePreview

Boolean

OptionalThis will enable/disable preview for media messages.

true

encode

Boolean

OptionalThis flag is used for sending an emoji in an Interactive List message. If the list message consists of emojis, set the encode flag to 'true'. This flag will not affect any other type of message.

true

### API Response

Send message API requests received by our platform are processed asynchronously, and hence you will always get an HTTP_SUCCESS(200 to 299) response range if the API request made is correct. The API response includes an object with a Gupshup unique message identifier and status as submitted. Your callback URL/webhook will receive a message event stating the submitted message to the WhatsApp API client(which eventually sends the message to the customer) is enqueued or has failed.

```
{
   "status":"submitted",
   "messageId":"ee4a68a0-1203-4c85-8dc3-49d0b3226a35"
}
```

The Gupshup unique message identifier that is the messageId in the API response will help you track messages through the inbound message events - enqueued, failed, sent, delivered, and read that you obtain on your webhook/callback URL.

## Template messaging

Template messages are Highly Structured(HSM)/ Notification messages. Once your WhatsApp Business API is Live, you can create template messages and submit them to WhatsApp for approval. You can send Template messages to users that you have opted-in. To know how you can opt-in users, read frequently asked questions.

### API Endpoint

### Headers

### Request body

source

string

Your registered WhatsApp Business API phone number.

The number must be in E. 164 format.

917834811114

destination

string

User's phone number.

919876543210

template

object

See template object description

{"id": "c6aecef6-bcb0-4fb1-8100-28c094e3bc6b","params": ["Agent","Local Address","Tracking code"]}

message

object

Required only if the template is of type Media - Image, Video, Document(.pdf) or location.

See message object description

Image: {"type":"image","image":{"link":""}}

Video:{"type":"video","video":{"link":""}}

Document: {"type":"document","document":{"link":""}}

Location: {"type":"location","location":{"longitude":"","latitude":""}}

#### Template object description

id

Unique identifier for a template

Use this API to get all template details for an app.

c6aecef6-bcb0-4fb1-8100-28c094e3bc6b

params

Array of placeholders/variables in the template in the order of occurrence.

["Agent","Local Address","Tracking code"]

#### Message object description

### API Response

Send message API requests received by our platform are processed asynchronously, and hence you will always get an HTTP_SUCCESS(200 to 299) response range if the API request made is correct. The API response includes an object with a Gupshup unique message identifier and status as submitted. Your callback URL/webhook will receive a message event stating the submitted message to the WhatsApp API client(which eventually sends the message to the customer) is enqueued or has failed.

```
{
   "status":"submitted",
   "messageId":"ee4a68a0-1203-4c85-8dc3-49d0b3226a35"
}
```

The Gupshup unique message identifier that is the messageId in the API response will help you track messages through the inbound message events - enqueued, failed, sent, delivered, and read that you obtain on your webhook/callback URL.

### Sample requests

Following are sample API requests for each message type. These examples are for your reference only. You can create templates from settings in the app dashboard and submit them to WhatsApp for review.

```
curl --location --request POST 'http://api.gupshup.io/sm/api/v1/template/msg' \
--header 'apikey: 2xxc4x4xx2c94xxxc2f9xx9d43xxxx8a' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'source=917834811114' \
--data-urlencode 'destination=918x98xx21x4' \
--data-urlencode 'template={"id": "c6aecef6-bcb0-4fb1-8100-28c094e3bc6b","params": ["Agent","Local Address","Tracking code"]}'
```

```
curl --location --request POST 'http://api.gupshup.io/sm/api/v1/template/msg' \
--header 'apikey: 2xxc4x4xx2c94xxxc2f9xx9d43xxxx8a' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'source=917834811114' \
--data-urlencode 'destination=918x98xx21x4' \
--data-urlencode 'template={"id": "c6aecef6-bcb0-4fb1-8100-28c094e3bc6b","params": ["Agent","Local Address","Tracking code"]}' \
--data-urlencode 'message={"type":"image","image":{"link":"https://www.buildquickbots.com/whatsapp/media/sample/jpg/sample01.jpg"}}'
```

```
curl --location --request POST 'http://api.gupshup.io/sm/api/v1/template/msg' \
--header 'apikey: 2xxc4x4xx2c94xxxc2f9xx9d43xxxx8a' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'source=917834811114' \
--data-urlencode 'destination=918x98xx21x4' \
--data-urlencode 'template={"id": "c6aecef6-bcb0-4fb1-8100-28c094e3bc6b","params": ["Agent","Local Address","Tracking code"]}' \
--data-urlencode 'message={"type":"document","document":{"link":"https://www.buildquickbots.com/whatsapp/media/sample/pdf/sample01.pdf","filename": "Sample funtional resume"}}'
```

```
curl --location --request POST 'http://api.gupshup.io/sm/api/v1/template/msg' \
--header 'apikey: 2xxc4x4xx2c94xxxc2f9xx9d43xxxx8a' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'source=917834811114' \
--data-urlencode 'destination=918x98xx21x4' \
--data-urlencode 'template={"id": "c6aecef6-bcb0-4fb1-8100-28c094e3bc6b","params": ["Agent","Local Address","Tracking code"]}' \
--data-urlencode 'message={"type":"video","video":{"link": "https://www.buildquickbots.com/whatsapp/media/sample/video/sample01.mp4"}}'
```

```
curl --location --request POST 'http://api.gupshup.io/sm/api/v1/template/msg' \
--header 'apikey: 2xxc4x4xx2c94xxxc2f9xx9d43xxxx8a' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'source=917834811114' \
--data-urlencode 'destination=918x98xx21x4' \
--data-urlencode 'template={"id": "c6aecef6-bcb0-4fb1-8100-28c094e3bc6b","params": ["Agent","Local Address","Tracking code"]}' \
--data-urlencode 'message={"type":"location","location":{"longitude":"","latitude":""}}'
```

```
curl --location --request POST 'http://api.gupshup.io/sm/api/v1/template/msg' \
--header 'apikey: 2xxc4x4xx2c94xxxc2f9xx9d43xxxx8a' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'source=917834811114' \
--data-urlencode 'destination=918x98xx21x4' \
--data-urlencode 'template={"id": "c49ee21d-4d39-452d-a6c1-25b7615e01e4","params": ["John","docs/bot-platform/guide/whatsapp-api-documentation"]}' \
--data-urlencode 'message={"type":"document","document":{"link":"https://www.buildquickbots.com/whatsapp/media/sample/pdf/sample01.pdf","filename": "Sample funtional resume"}}'
```

```
curl --location --request POST 'http://api.gupshup.io/sm/api/v1/template/msg' \
--header 'apikey: 2xxc4x4xx2c94xxxc2f9xx9d43xxxx8a' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'source=917834811114' \
--data-urlencode 'destination=918x98xx21x4' \
--data-urlencode 'template={"id": "c6aecef6-bcb0-4fb1-8100-28c094e3bc6b","params": ["12323XXXX"]}'
```

Let's have a look at the error codes for the above outbound message APIs:

1001 - Last mapped bot and sender details mismatched

It occurs if your Access API app is not Live yet and you are using the sandbox mode to send a template message.

To receive messages from your Access API app in sandbox mode, you must first send a WhatsApp message (proxy YourAppName) to the Gupshup proxy phone number (+917834811114).

1002 - Number does not exist on WhatsApp

The phone number you sent the message to is not registered on WhatsApp.

1003 - Unable to send message | Check your wallet balance

Message sending failed because of insufficient balance.

1004 - Message sending failed as user is inactive for session message and template messaging is disabled.

You have disabled template messaging for your app, and the user is not active for a session.

1005 - Message sending failed as user is inactive for session message and template did not match

The message is not a template message, and the user is not active for a session.

1006 - Message sending failed as user is inactive for session message and not opted in for template message

The user is not opted-in, and the user is not active for a session.

1007 - Message sending failed as user is inactive for session message, not opted in for template message and template did not match

The message is not a template message, the user is not opted-in and not active for a session.

1008 - User is not Opted in and Inactive

The user is not opted-in and not active for a session.

1010 - Invalid Media URL

It occurs if your Access API app is not Live yet and you are using the sandbox mode to send a message.

A sandbox Access API app is limited and only supports sending media messages given here.

1011 - Invalid Media Size

The size of the media file is not supported.

### For any other error code, click here.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- Following are sample API requests for each message type. These examples are for your reference only. You can create templates from settings in the app dashboard and submit them to WhatsApp for review.

**Last updated (from source)**: Updated 10 months ago
