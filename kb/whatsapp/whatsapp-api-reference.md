# WhatsApp API Reference

Complete API reference for WhatsApp message delivery, webhooks, and authentication.

## Message Delivery

### Send Text Message
```
POST https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages

Headers:
  Authorization: Bearer {ACCESS_TOKEN}
  Content-Type: application/json

Body:
{
  "messaging_product": "whatsapp",
  "to": "1234567890",
  "type": "text",
  "text": {
    "preview_url": true,
    "body": "Hello, this is your message"
  }
}
```

**Returns:**
```json
{
  "messages": [
    {
      "id": "wamid.xxxxx",
      "message_status": "accepted"
    }
  ]
}
```

---

### Send Media Message
```
POST https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages

Body:
{
  "messaging_product": "whatsapp",
  "to": "1234567890",
  "type": "image",
  "image": {
    "link": "https://example.com/image.jpg"
  }
}
```

**Supported media types:**
- `image` — JPG, PNG
- `audio` — MP3, OGG
- `video` — MP4, 3GP
- `document` — PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT

---

### Send Template Message
```
POST https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages

Body:
{
  "messaging_product": "whatsapp",
  "to": "1234567890",
  "type": "template",
  "template": {
    "name": "order_confirmation",
    "language": {
      "code": "en_US"
    },
    "parameters": {
      "body": {
        "parameters": [
          {"type": "text", "text": "ORDER-123"},
          {"type": "text", "text": "$99.99"}
        ]
      }
    }
  }
}
```

---

### Send Location Message
```
Body:
{
  "messaging_product": "whatsapp",
  "to": "1234567890",
  "type": "location",
  "location": {
    "latitude": "37.4847",
    "longitude": "-122.1477",
    "name": "Gupshup HQ",
    "address": "1234 Main St"
  }
}
```

---

## Webhook Events

Register webhook endpoint to receive real-time events:

```
POST https://api.partner.com/webhooks/whatsapp
```

### Incoming Message
```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "id": "WABA_ID",
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "messages": [
              {
                "from": "1234567890",
                "id": "wamid.xxxxx",
                "timestamp": "1672531200",
                "type": "text",
                "text": {
                  "body": "Hi, I need help"
                }
              }
            ],
            "contacts": [
              {
                "profile": {
                  "name": "John Doe"
                },
                "wa_id": "1234567890"
              }
            ]
          }
        }
      ]
    }
  ]
}
```

---

### Message Status Update
```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "statuses": [
              {
                "id": "wamid.xxxxx",
                "status": "delivered",
                "timestamp": "1672531205",
                "recipient_id": "1234567890"
              }
            ]
          }
        }
      ]
    }
  ]
}
```

**Status values:**
- `accepted` — Message accepted by WhatsApp
- `sent` — Delivered to phone
- `delivered` — Read by recipient
- `read` — Seen by recipient
- `failed` — Delivery failed

---

### Delivery Error
```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "statuses": [
              {
                "id": "wamid.xxxxx",
                "status": "failed",
                "timestamp": "1672531205",
                "recipient_id": "1234567890",
                "errors": [
                  {
                    "code": 131026,
                    "title": "Message rejected",
                    "message": "Recipient number is not valid or does not exist",
                    "error_data": {
                      "details": "Invalid phone number format"
                    }
                  }
                ]
              }
            ]
          }
        }
      ]
    }
  ]
}
```

**Common error codes:**
- `131026` — Invalid phone number
- `131000` — Unsupported message type
- `131008` — Rate limit exceeded
- `100` — Invalid parameter

---

### Template Status Update
```json
{
  "object": "whatsapp_business_account",
  "entry": [
    {
      "changes": [
        {
          "value": {
            "messaging_product": "whatsapp",
            "message_template_status_update": {
              "id": "TEMPLATE_ID",
              "status": "APPROVED",
              "category": "ACCOUNT_UPDATE"
            }
          }
        }
      ]
    }
  ]
}
```

**Template statuses:**
- `APPROVED` — Template approved and ready to use
- `PENDING_REVIEW` — Under Meta review
- `REJECTED` — Template rejected (see reason)
- `DISABLED` — Template disabled (violation detected)

---

## Authentication

### OAuth 2.0 Flow

1. **Register Application** in Meta Developers Portal
2. **Request Access Token**
   ```
   GET https://api.instagram.com/oauth/authorize?
     client_id={APP_ID}
     &redirect_uri={REDIRECT_URI}
     &scope=whatsapp_business_messaging
   ```

3. **Exchange Code for Token**
   ```
   POST https://graph.instagram.com/v25.0/oauth/access_token
   
   Parameters:
     client_id={APP_ID}
     client_secret={APP_SECRET}
     grant_type=authorization_code
     code={CODE}
     redirect_uri={REDIRECT_URI}
   ```

4. **Use Access Token in Requests**
   ```
   Authorization: Bearer {ACCESS_TOKEN}
   ```

---

## Rate Limiting

Messages are rate-limited based on **quality rating**:

| Quality | Max Messages/Sec | Throttle |
|---------|------------------|----------|
| Green   | 80/sec           | None     |
| Yellow  | 40/sec           | 50% slow |
| Red     | 1/sec            | Major throttling |

---

## Error Handling

Always check response status:

**Success (200):**
```json
{
  "messages": [{"id": "wamid.xxxxx", "message_status": "accepted"}]
}
```

**Failure (400):**
```json
{
  "error": {
    "message": "Invalid parameter",
    "type": "OAuthException",
    "code": 100,
    "error_subcode": 2104001,
    "fbtrace_id": "xxxxx"
  }
}
```

---

See also:
- [[whatsapp-pricing]] — Cost structure
- [[meta-business-agent]] — Agent message handling
- [[bizai-api-endpoints]] — Gupshup BizAI endpoints
