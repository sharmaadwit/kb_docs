source_url: https://api.dotgo.com/rcs/reference

<!-- kb-golden:v10 -->
# RCS API Reference

**Module**: Channels

## API Base URLs

| Environment | URL |
|-------------|-----|
| Production | `https://api.dotgo.com/rcs` |
| Sandbox | `https://sandbox.dotgo.com/rcs` (when available) |

## Endpoint Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/bot/v1/{botId}/messages/async` | Send message |
| GET | `/bot/v1/{botId}/messages/{msgId}/status` | Query message status |
| PUT | `/bot/v1/{botId}/messages/{msgId}/status` | Revoke message |
| GET | `/bot/v1/{botId}/contactCapabilities` | Check RCS capability |
| POST | `/directory/secure/api/v1/bots/submit_bot` | Create agent |
| PUT | `/directory/secure/api/v1/bots/submit_bot` | Update agent |
| POST | `/directory/secure/api/v1/bots/{botId}/templates` | Submit template |
| PUT | `/directory/secure/api/v1/bots/{botId}/templates/{templateId}` | Update template |
| DELETE | `/directory/secure/api/v1/bots/{botId}/templates/{templateId}` | Delete template |
| GET | `/directory/secure/api/v1/bots/{botId}/templates/{templateId}` | Get template details |
| GET | `/directory/secure/api/v1/bots/{botId}/templates` | List templates |

## HTTP Response Codes

| Code | Status | Description |
|------|--------|-----------|
| 200 | OK | Request successful, response body included |
| 202 | Accepted | Request accepted for processing (async) |
| 204 | No Content | Request successful, no response body |
| 400 | Bad Request | Invalid input, malformed request |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side error |
| 502 | Bad Gateway | Service temporarily unavailable |
| 503 | Service Unavailable | Service down for maintenance |

## Authentication Header

**Required for all API calls**:

```
Authorization: Bearer <access_token>
```

Where `<access_token>` is obtained from Auth2 SSO endpoint (see rcs-authentication.md).

## Message Status Values

| Status | Description |
|--------|-----------|
| `pending` | Message queued for delivery |
| `sent` | Message sent to carrier |
| `delivered` | Message delivered to device |
| `displayed` | Message read by user |
| `failed` | Delivery failed |
| `cancelled` | Message was revoked |

## Delivery Error Codes

| Error Code | Error Type | Description | Action |
|-----------|-----------|-----------|--------|
| 402 | insufficient_balance | Account balance too low | Recharge account |
| 403 | curfew_hrs | Message blocked by quiet hours | Retry after quiet hours |
| 404 | rcs_disabled | RCS disabled for number/carrier | Use fallback channel |
| 409 | invalid_template | Template not approved or doesn't exist | Submit/approve template |
| 410 | opted_out | User opted out of messaging | Respect opt-out |
| 423 | dnd_enabled | Do Not Disturb enabled | Don't retry |
| 429 | rate_limit | Rate limit exceeded | Implement backoff/queue |
| 500 | internal_server_error | Server error | Retry with exponential backoff |
| 400 | invalid_client | Bad client ID/secret | Check credentials |
| 400 | maap_specific_error | Carrier/RCS specific error | Check carrier status |
| 400 | google_rate_limit | Google API rate exceeded | Increase quota/retry |
| 410 | ttl_expiration_revoke_failed | Message expired before revoke | Message already delivered |

## Message Request Fields

### Text Message

```json
{
  "RCSMessage": {
    "textMessage": "string (max 2500 chars)"
  },
  "messageContact": {
    "userContact": "string (E.164 format, e.g., +1234567890)"
  }
}
```

### Template Message

```json
{
  "RCSMessage": {
    "templateMessage": {
      "templateCode": "string (template ID)",
      "customParams": {
        "key1": "value1",
        "key2": "value2"
      }
    }
  },
  "messageContact": {
    "userContact": "string"
  }
}
```

### File Message

```json
{
  "RCSMessage": {
    "fileMessage": {
      "fileUrl": "string (publicly accessible URL)",
      "fileType": "image|video|application/pdf"
    }
  },
  "messageContact": {
    "userContact": "string"
  }
}
```

## Template Request Fields (Submission)

| Field | Validation | Required | Example |
|-------|-----------|----------|---------|
| name | Max 20 chars, alphanumeric + underscore | Yes | "welcome_template" |
| type | text_message, text_message_with_pdf, rich_card, rich_card_carousel | Yes | "text_message" |
| textMessageContent | Max 2500 chars | Yes (text types) | "Hello [name], welcome!" |
| fallbackText | Max 160 chars | Optional | "Hello, welcome!" |
| templateUseCase | Transactional, Promotional, OTP | Conditional | "Transactional" |
| suggestions | Array of suggestion objects | Optional | See suggestions structure |
| mediaUrl | Valid public URL | Conditional (rich cards) | "https://..." |
| multimedia_files | File upload (multipart) | Conditional | File stream |
| cardTitle | Max 200 chars | Conditional (rich cards) | "Card Title" |
| cardDescription | Max 2000 chars | Conditional (rich cards) | "Card description" |

## Suggestion Types

```json
{
  "suggestionType": "reply|url_action|dialer_action|calendar_action|map_action",
  "displayText": "string (max 25 chars)",
  "postback": "string (max 120 chars)",
  "phoneNumber": "string (for dialer_action)",
  "url": "string (for url_action)",
  "calendarAction": {
    "startTime": "ISO 8601 timestamp",
    "endTime": "ISO 8601 timestamp",
    "title": "string",
    "description": "string"
  },
  "mapAction": {
    "latitude": "number",
    "longitude": "number",
    "label": "string",
    "fallbackUrl": "string"
  }
}
```

## Agent Creation Fields

| Field | Validation | Example |
|-------|-----------|---------|
| bot_name | Max 40, alphanumeric + underscore | "support_bot_123" |
| bot_summary | Max 100 chars | "Customer support chatbot" |
| privacy_url | Valid URL, max 2048 | "https://example.com/privacy" |
| term_condition_url | Valid URL, max 2048 | "https://example.com/terms" |
| platform | "GSMA API" or "Google API" | "GSMA API" |
| email_list | Max 3 emails | [{"value":"support@example.com","label":"Support"}] |
| website_list | Max 3 URLs | [{"value":"https://example.com","label":"Website"}] |
| phone_list | Max 3 phones, E.164 format | [{"value":"+1234567890","label":"Phone"}] |
| logo_image | JPG/PNG, 224x224px, <90KB | multipart file |
| bg_image | JPG/PNG, 1440x448px, <360KB | multipart file |
| agent_color | Hex RGB (#XXXXXX), 4.5:1 contrast | "#000000" |
| lang_supported | Comma-separated codes | "English,Spanish,Hindi" |
| agent_msg_type | Transactional, Promotional, OTP, Multi-Use | "Transactional" |
| billing_category | Conversational, Non_Conversational | "Conversational" |
| carrier_details | MCCMNC array + global_reach flag | {"carrier_mccmnc":["62160","62402"],"global_reach":false} |
| region | "India" or "Rest of World" | "India" |
| is_carrier_edited | boolean | true |

## Carrier Codes (MCCMNCs)

**Common Carriers**:

| Country | Carrier | MCCMNC |
|---------|---------|--------|
| India | Jio | 62160 |
| India | Vodafone | 62402 |
| India | Airtel | 310160 |
| USA | AT&T | 310410 |
| USA | Verizon | 310012 |
| UK | Vodafone | 234715 |
| Germany | Deutsche Telekom | 26201 |

See Dotgo documentation for full list of 90+ supported carriers.

## Rate Limiting

**Token Endpoint**: 60 requests/minute per client

**Message APIs**: 60 TPM (Transactions Per Minute) per client by default

**Rate Limit Headers** (included in response):
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1640001600
```

**Handling Rate Limits**:
1. Check `X-RateLimit-Remaining` before each request
2. Implement exponential backoff: 1s, 2s, 4s, 8s, etc.
3. Queue excess requests; don't hammer the API
4. Contact rbm-support@dotgo.com to increase limits

## Media File Size & Format Limits

| Type | Formats | Max Size | Works with Rich Cards |
|------|---------|----------|----------------------|
| Image | JPG, JPEG, PNG, GIF | 100MB | Yes |
| Video | H263, MP4, MPEG-4, WebM | 100MB | Yes |
| GIF | GIF animated | 100MB | Yes |
| PDF | PDF only | 100MB | Text+PDF only |

**Recommendations**:
- Keep files <5MB for optimal delivery speed
- Compress images/videos before upload
- Use CDN for reliable file hosting
- Test with largest file size before production

## Webhook Payload Structure

All webhook events follow this structure:

```json
{
  "messageEvent": { ... } | "messageStatusEvent": { ... }
}
```

**Message Event Fields**:

```json
{
  "messageEvent": {
    "messageFrom": {
      "userContact": "+1234567890"
    },
    "timestamp": "2022-01-10T10:30:00Z",
    "messageId": "msg_12345",
    "text": { "body": "string" },
    "isTyping": "active|inactive",
    "suggestionResponse": {
      "postbackData": "string",
      "displayText": "string"
    }
  }
}
```

**Message Status Event Fields**:

```json
{
  "messageStatusEvent": {
    "status": "pending|sent|delivered|displayed|failed|cancelled",
    "timestamp": "2022-01-10T10:31:00Z",
    "messageId": "msg_12345",
    "deliveryReceiptEvent": {
      "timestamp": "2022-01-10T10:31:00Z",
      "status": "DELIVERED|FAILED"
    }
  }
}
```

## Required Headers

| Header | Value |
|--------|-------|
| Authorization | Bearer <access_token> |
| Content-Type | application/json (for JSON bodies) |
| Content-Type | multipart/form-data (for file uploads) |

## Common Error Response Format

```json
{
  "error": {
    "code": 400,
    "message": "Descriptive error message",
    "status": "Bad Request",
    "details": {
      "field": "error_detail"
    }
  }
}
```

## Retry Logic Recommendations

```python
import time
import random

def send_with_retry(api_call, max_retries=3, backoff_base=2):
    for attempt in range(max_retries):
        try:
            response = api_call()
            return response
        except RateLimitError:
            wait_time = backoff_base ** attempt + random.uniform(0, 1)
            print(f"Rate limited. Retrying in {wait_time}s...")
            time.sleep(wait_time)
        except ServerError:
            if attempt < max_retries - 1:
                wait_time = backoff_base ** attempt
                print(f"Server error. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
```

## Cross-module workflow docs

Use this reference alongside service-specific docs:
- rcs-authentication.md for credential management
- rcs-messaging-api.md for message sending
- rcs-templates.md for template submission
- rcs-webhooks-and-callbacks.md for webhook handling

## Reference (from source)

<!-- procedural:v2 -->
# RCS API Reference

Detailed technical reference for all RCS API endpoints, fields, error codes, and rate limits.
