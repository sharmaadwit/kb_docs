source_url: https://api.dotgo.com/rcs/webhooks

<!-- kb-golden:v10 -->
# RCS Webhooks & Event Callbacks

**Module**: Channels

## Definition

RCS Webhooks enable real-time event notifications from the Gupshup Dotgo RBM platform to your application. When users send messages, interact with suggestions, or events occur on the RCS channel, webhook callbacks are sent to your registered endpoint via HTTPS POST.

Webhook events include: incoming messages, typing indicators, message status updates, user interaction with suggestions, and more.

## Webhook Setup

### Register Webhook Endpoint

During agent creation (RCS Agent Setup), provide your webhook URL:

**Field**: `webhook_url`  
**Format**: HTTPS URL (max 2048 chars)  
**Example**: `https://yourdomain.com/rcs/webhook`

### Webhook Security

- All webhooks are sent via **HTTPS only**
- Requests include **Bearer token authorization header**
- Webhook payloads are **signed** (verify signature if needed)
- Use certificate pinning for added security

### Webhook Retry Policy

- Failed webhook deliveries are retried up to 3 times
- Exponential backoff: 5s, 25s, 125s delays between retries
- Respond with HTTP 200 to acknowledge receipt

## Webhook Event Types

### 1. Message from User

**Triggered when**: User sends a message to your bot.

**Payload Structure**:

```json
{
  "messageEvent": {
    "messageFrom": {
      "userContact": "+914253136789"
    },
    "timestamp": "2022-01-10T10:30:00Z",
    "text": {
      "body": "Hello, I need help"
    },
    "messageId": "msg_12345"
  }
}
```

### 2. isTyping Message from User

**Triggered when**: User starts/stops typing.

**Payload Structure**:

```json
{
  "messageEvent": {
    "messageFrom": {
      "userContact": "+914253136789"
    },
    "timestamp": "2022-01-10T10:30:00Z",
    "isTyping": "active"
  }
}
```

**isTyping Values**: `active` (typing), `inactive` (stopped typing)

### 3. Message Status Update

**Triggered when**: Message status changes (sent, delivered, displayed, failed, etc.)

**Payload Structure**:

```json
{
  "messageStatusEvent": {
    "status": "delivered",
    "timestamp": "2022-01-10T10:31:00Z",
    "messageId": "msg_12345",
    "deliveryReceiptEvent": {
      "timestamp": "2022-01-10T10:31:00Z",
      "status": "DELIVERED"
    }
  }
}
```

**Status Values**: `pending`, `sent`, `delivered`, `displayed`, `failed`, `cancelled`

### 4. Response to Suggested Reply/Action

**Triggered when**: User clicks a suggested reply or action.

**Payload Structure**:

```json
{
  "messageEvent": {
    "messageFrom": {
      "userContact": "+914253136789"
    },
    "timestamp": "2022-01-10T10:32:00Z",
    "suggestionResponse": {
      "postbackData": "set_by_chatbot_reply_1",
      "displayText": "Yes"
    },
    "messageId": "msg_reply_001"
  }
}
```

### 5. Response to Template Suggestion

**Triggered when**: User interacts with suggestions within template messages.

**Payload Structure**:

```json
{
  "messageEvent": {
    "messageFrom": {
      "userContact": "+914253136789"
    },
    "timestamp": "2022-01-10T10:33:00Z",
    "suggestionResponse": {
      "postbackData": "offer_code_abc123",
      "displayText": "Claim Offer"
    },
    "messageId": "template_resp_001"
  }
}
```

## Webhook Request Format

All webhooks are delivered as HTTPS POST requests:

```
POST https://yourdomain.com/rcs/webhook
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "messageEvent": { ... }
  or
  "messageStatusEvent": { ... }
}
```

## Webhook Response

Your endpoint should respond with HTTP 200 to acknowledge successful receipt:

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "received"
}
```

**Response Codes**:
- `200` — Successfully processed
- `4xx` — Client error (not retried)
- `5xx` — Server error (retried with backoff)

## Common Webhook Event Fields

| Field | Type | Description |
|-------|------|-----------|
| messageId | String | Unique message identifier |
| userContact | String | User phone number (MSISDN) |
| timestamp | ISO 8601 | Event timestamp in UTC |
| text.body | String | Message text content |
| status | String | Message delivery status |
| suggestionResponse.postbackData | String | Postback data from user action |
| suggestionResponse.displayText | String | Display text of clicked suggestion |

## Webhook Payload Examples

### Example 1: User Text Message

```json
{
  "messageEvent": {
    "messageFrom": {
      "userContact": "+914253136789"
    },
    "timestamp": "2022-01-10T10:30:00Z",
    "text": {
      "body": "I want to book a flight"
    },
    "messageId": "6cd095cd-62f6-4338-bba2-4b1db98b0537"
  }
}
```

### Example 2: Message Status (Delivered)

```json
{
  "messageStatusEvent": {
    "status": "delivered",
    "timestamp": "2022-01-10T10:31:00Z",
    "messageId": "ddc24c2-cff5-48ac-baaa-4f286bc28061",
    "deliveryReceiptEvent": {
      "timestamp": "2022-01-10T10:31:00Z",
      "status": "DELIVERED"
    }
  }
}
```

### Example 3: User Click on Suggestion

```json
{
  "messageEvent": {
    "messageFrom": {
      "userContact": "+914253136789"
    },
    "timestamp": "2022-01-10T10:32:00Z",
    "suggestionResponse": {
      "postbackData": "offer_claimed_01",
      "displayText": "Claim Offer"
    },
    "messageId": "suggestion_resp_abc123"
  }
}
```

### Example 4: User Typing

```json
{
  "messageEvent": {
    "messageFrom": {
      "userContact": "+914253136789"
    },
    "timestamp": "2022-01-10T10:33:00Z",
    "isTyping": "active",
    "messageId": "typing_001"
  }
}
```

## Webhook Best Practices

1. **Idempotency**: Process each `messageId` only once. Store processed IDs to handle duplicates.
2. **Timeout**: Respond within 5 seconds to avoid timeout and retry.
3. **Async Processing**: Queue webhook events for async processing; don't block on response.
4. **Logging**: Log all webhook events for debugging and audit trails.
5. **Error Handling**: Return HTTP 200 even if processing fails internally (log errors).
6. **Signature Verification**: Verify Bearer token in Authorization header.
7. **Retry Handling**: Implement exponential backoff on your end if you retry sends.

## Troubleshooting

### Webhooks Not Received

1. Verify webhook URL is publicly accessible (HTTPS, valid certificate)
2. Check firewall/security rules allow connections from Dotgo IPs
3. Verify Authorization header Bearer token matches your credentials
4. Check server logs for 5xx errors
5. Confirm webhook endpoint is returning HTTP 200

### Duplicate Events

1. Implement idempotency using `messageId`
2. Store processed message IDs in database
3. Deduplicate within sliding time window (e.g., 5 minutes)

### Message Status Never Updates

1. Verify webhook endpoint is registered and accessible
2. Check authorization token validity
3. Monitor RCS platform status (carrier issues may delay status)
4. Use message status query API as fallback: `GET /messages/{msgId}/status`

## Cross-module workflow docs

- Webhooks are automatically sent when registered during agent setup
- Use events to update bot conversation state in Bot Studio
- Track message delivery for analytics and reporting
- Implement user interaction handling for suggestion responses

## Options / variants

- **Async vs Sync**: Process webhooks asynchronously to avoid timeouts
- **Batching**: Implement webhook batching for high-volume scenarios
- **Fallback**: Have fallback mechanisms if webhook processing fails
- **Monitoring**: Set up alerts for missing webhooks or high failure rates

## Reference (from source)

<!-- procedural:v2 -->
# RCS Webhooks

Receive real-time event notifications for user messages, interactions, and message status updates via webhook callbacks.
