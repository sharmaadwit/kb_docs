source_url: https://api.dotgo.com/rcs/messaging

<!-- kb-golden:v10 -->
# RCS Messaging API

**Module**: Channels

## Definition

The RCS Messaging API allows you to send messages to users on RCS-capable devices. Gupshup supports both GSMA Chatbot MaaP and Google Business Messages API standards, allowing flexibility in your integration approach. Both styles support text messages, template messages, file messages, rich cards, and suggested actions.

## Message Types Supported

- **Text Messages**: Plain text with optional suggestions
- **Template Messages**: Pre-approved templates with custom variables
- **File Messages**: Images, videos, GIFs, PDFs
- **Rich Cards**: Standalone or carousel with media and suggested actions
- **Suggested Replies & Actions**: URL actions, dialer actions, calendar events, map locations

## API Styles

### GSMA Chatbot MaaP API

**Server Root**: `https://api.dotgo.com/rcs`

**Endpoint**: `POST /bot/v1/{botId}/messages/async`

Follows GSMA Chatbot MaaP specifications for request/response formats.

### Google Business Messages (RBM) API

**Server Root**: `https://api.dotgo.com/rcs`

**Endpoint**: `POST /bot/v1/{botId}/messages/async`

Follows Google Business Messages API specifications.

## GSMA Messaging Endpoints

### Send a Message (GSMA Style)

**Endpoint**: `POST https://api.dotgo.com/bot/v1/{botId}/messages/async`

**Authorization**: Bearer token (from Auth2 SSO)

**Request Format**:

```json
{
  "RCSMessage": {
    "textMessage": "hello world"
  },
  "messageContact": {
    "userContact": "+914253136789"
  }
}
```

**Request Parameters** (select one message type):

| Name | Type | Description | Remarks |
|------|------|-------------|---------|
| botId | Path variable | Bot registered with RCS APIs platform | E.g., OsOsQ0GwNvUdLTV9Bd |
| userContact | A field in Request Body | User MSISDN in canonical form | Ex: +914253136789 |
| textMessage | String | Plain text message | "hello world" |
| templateMessage | Object | Template with code and custom params | {"templateCode":"template_123","customParams":{"name":"user"}} |
| fileMessage | Object | File URL (image/video/PDF) | {"fileUrl":"https://example.com/file.mp4"} |
| richcardMessage | Object | Rich card with media and suggestions | See rich card structure below |
| suggestedChipList | Object | Suggested reply chips/actions | See suggestions structure below |
| enableFallback | Query parameter | Enable GIP fallback (optional) | Values: true/false |
| sendGipLink | Query parameter | Send SMS with GIP link (optional) | Values: true/false |

**Response Format** (202 Accepted):

```json
{
  "RCSMessage": {
    "msgId": "6cd095cd-62f6-4338-bba2-4b1db98b0537",
    "status": "pending"
  }
}
```

**Message Status States**:
- `pending` — Message queued for delivery
- `sent` — Delivered to user device
- `delivered` — Displayed on device
- `displayed` — User has read it
- `failed` — Delivery failed
- `cancelled` — Sent message revoked

### Send Message Example (Text)

**Request**:

```json
{
  "RCSMessage": {
    "textMessage": "hello world"
  },
  "messageContact": {
    "userContact": "+914253136789"
  }
}
```

### Send Message Example (Template)

**Request**:

```json
{
  "RCSMessage": {
    "templateMessage": {
      "templateCode": "template_123",
      "customParams": {
        "name": "user"
      }
    }
  },
  "messageContact": {
    "userContact": "+914253136789"
  }
}
```

### Send Message Example (File Message)

**Request**:

```json
{
  "RCSMessage": {
    "fileMessage": {
      "fileUrl": "https://konnect.kirusa.com/uploads/rcsTemplates/InstaVoice.png"
    }
  },
  "messageContact": {
    "userContact": "+14251234567"
  }
}
```

### Send isTyping Indication

**Endpoint**: `POST https://api.dotgo.com/bot/v1/{botId}/messages/async`

**Request**:

```json
{
  "RCSMessage": {
    "isTyping": "active"
  },
  "messageContact": {
    "userContact": "+914253136789"
  }
}
```

## Message Status Query

**Endpoint**: `GET https://api.dotgo.com/bot/v1/{botId}/messages/{msgId}/status`

**Authorization**: Bearer token

**Response** (200 OK):

```json
{
  "RCSMessage": {
    "msgId": "ddc24c2-cff5-48ac-baaa-4f286bc28061",
    "status": "sent",
    "timestamp": "2020-11-10T11:06:26"
  }
}
```

## Revoke Sent Message

**Endpoint**: `PUT https://api.dotgo.com/bot/v1/{botId}/messages/{msgId}/status`

**Request**:

```json
{
  "RCSMessage": {
    "status": "cancelled"
  }
}
```

**Response** (204 No Content)

Message revocation only succeeds if message hasn't been delivered. Once delivered, revocation is best-effort.

## Check RCS Capability

**Endpoint**: `GET https://api.dotgo.com/bot/v1/{botId}/contactCapabilities?userContact=+914253136789`

**Authorization**: Bearer token

**Response** (200 OK):

```json
{
  "capabilities": [
    "chatBotCommunication",
    "chat",
    "fileTransfer"
  ]
}
```

**Possible Capabilities**:
- `chatBotCommunication` — Bot communication supported
- `chat` — RCS chat available
- `fileTransfer` — File transfer available
- `videoCall` — Video call supported
- `geolocationPush` — Location push supported
- `callComposer` — Call composer feature
- `chatBotCommunication` — Generic bot messaging

## Suggested Actions Structure

**Suggestion Types**:

```json
"suggestions": [
  {
    "reply": {
      "displayText": "suggestion#1",
      "postback": {
        "data": "set_by_chatbot_reply_1"
      }
    }
  },
  {
    "action": {
      "displayText": "Call",
      "postback": {
        "data": "postback_data_1234"
      },
      "dialerAction": {
        "dialPhoneNumber": {
          "phoneNumber": "+15556667777"
        }
      }
    }
  },
  {
    "action": {
      "displayText": "Open website or deep link",
      "postback": {
        "data": "set_by_chatbot_open_url"
      },
      "urlAction": {
        "openUrl": {
          "url": "https://www.google.com"
        }
      }
    }
  },
  {
    "action": {
      "displayText": "Schedule Meeting",
      "postback": {
        "data": "set_by_chatbot_create_calendar_event"
      },
      "calendarAction": {
        "createCalendarEvent": {
          "startTime": "2017-03-14T10:00:00Z",
          "endTime": "2017-03-14T23:59:59Z",
          "title": "Meeting",
          "description": "GSG review meeting"
        }
      }
    }
  },
  {
    "action": {
      "displayText": "Show location on a map",
      "postback": {
        "data": "set_by_chatbot_open_map"
      },
      "mapAction": {
        "showLocation": {
          "location": {
            "latitude": 37.4220041,
            "longitude": -122.0862515,
            "label": "Googleplex"
          },
          "fallbackUrl": "https://www.google.com/maps/@37.4219162,-122.078063,15z"
        }
      }
    }
  }
]
```

## Media Support

**File Size Limits**:
- **Images** (JPG, PNG, GIF): 100MB
- **Videos** (MP4, WebM, H263, MPEG-4): 100MB
- **PDFs**: 100MB
- **Recommended**: Keep files <5MB for optimal delivery

**Supported Formats**:
| Media Type | Formats | Works with Rich Cards |
|-----------|---------|----------------------|
| image | JPG, JPEG, PNG, GIF | Yes |
| video | H263, MP4, MPEG-4, WebM | Yes |
| application/pdf | PDF | No (text+PDF only) |

## Rich Card Structure

```json
{
  "RCSMessage": {
    "trafficType": "advertisement",
    "richcardMessage": {
      "message": {
        "generalPurposeCard": {
          "layout": {
            "cardOrientation": "HORIZONTAL",
            "imageAlignment": "LEFT"
          },
          "content": {
            "media": {
              "mediaUrl": "https://cdn.server/path/media.mp4",
              "mediaContentType": "video/mp4",
              "mediaFileSize": 2718288,
              "thumbnailUrl": "https://cdn.server/path/media.png",
              "thumbnailContentType": "image/png",
              "thumbnailFileSize": 314159,
              "height": "MEDIUM_HEIGHT",
              "contentDescription": "Textual description of media content"
            },
            "title": "This is a single rich card.",
            "description": "This is the description of the rich card. It's the first field that will be truncated if it exceeds the maximum width or height of a card."
          }
        }
      },
      "suggestedChipList": {
        "suggestions": [
          {
            "reply": {
              "displayText": "Yes",
              "postback": {
                "data": "set_by_chatbot_reply_yes"
              }
            }
          }
        ]
      }
    }
  },
  "messageContact": {
    "userContact": "+14251234567"
  }
}
```

## Error Responses

**400 Bad Request**:

```json
{
  "error": {
    "code": 400,
    "message": "Please provide valid JSON data",
    "status": "Bad Request"
  }
}
```

**401 Unauthorized**:

```json
{
  "error": {
    "code": 401,
    "message": "This request is unauthorized.",
    "status": "Unauthorized"
  }
}
```

**403 Forbidden**:

```json
{
  "error": {
    "code": 403,
    "message": "Invalid clientId or Invalid IP address",
    "status": "Forbidden"
  }
}
```

## Error Code Details

| Error Code | Error Message | Resolution |
|-----------|---------------|-----------|
| 402 | insufficient_balance | Recharge account to send messages |
| 403 | curfew_hrs | Message blocked due to quiet hours |
| 404 | rcs_disabled | RCS disabled for number/carrier |
| 409 | invalid_template | Template not approved or doesn't exist |
| 410 | opted_out | User has opted out of messaging |
| 423 | dnd_enabled | Do Not Disturb enabled for user |
| 429 | rate_limit | Rate limit exceeded (60 TPM default) |
| 500 | internal_server_error | Server error, retry later |

## Rate Limiting

**Default**: 60 Transactions Per Minute (TPM) per client

**Rate Limit Header**:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 59
X-RateLimit-Reset: 1640001600
```

To increase limits, contact rbm-support@dotgo.com

## Cross-module workflow docs

- Send messages via Bot Studio flows or Campaign Manager
- Track delivery status via webhooks or status query API
- Use capability check to validate RCS support before sending
- Implement fallback (SMS/email) for non-RCS devices

## Options / variants

- **Message styles**: Choose GSMA or Google API based on preference
- **Fallback messages**: Provide SMS fallback for non-RCS devices
- **Suggestions**: Offer multiple action types (reply, URL, phone, calendar, map)
- **Rich media**: Leverage images, videos, carousels for engagement

## Reference (from source)

<!-- procedural:v2 -->
# RCS Messaging

Send rich messages, templates, and interactive content to RCS-enabled users with delivery tracking.
