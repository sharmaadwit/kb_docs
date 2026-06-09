source_url: https://api.dotgo.com/rcs/quickstart

<!-- kb-golden:v10 -->
# RCS Quickstart — From Registration to First Message

**Module**: Channels

## Definition

Get your brand on RCS in 5 steps. This guide walks you through agent registration, template creation, and sending your first message using the Gupshup Dotgo RBM Hub.

## When to Use

Start here if you're:
- New to RCS and want to understand the basics
- Setting up your first RCS agent
- Ready to send your first rich message to customers

## Step-by-Step Setup

### Step 1: Register Your RCS Agent (5 minutes)

RCS agents represent your brand on the RBM Hub. You'll provide your business details and verification information.

**What you need:**
- Company name and website
- Logo (224x224px JPG/PNG, <90KB)
- Privacy policy URL
- Terms & conditions URL
- Support contact email

**How:**
1. Submit registration via the RCS Agent Setup flow (see rcs-agent-setup.md for full details)
2. You'll receive:
   - **Bot ID** (used in all API calls)
   - **Client ID & Client Secret** (for authentication)
3. Store credentials securely (use environment variables, never commit to code)

**Status:** After submission, Dotgo reviews and approves within 24-48 hours.

---

### Step 2: Authenticate Your API Client (2 minutes)

Once approved, you can obtain access tokens to make API calls.

**Quick OAuth2 flow:**

```bash
# Get access token
curl -X POST https://auth.dotgo.com/auth/oauth/token \
  -H "Authorization: Basic $(echo -n 'CLIENT_ID:CLIENT_SECRET' | base64)" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials"

# Response includes: access_token, expires_in (3600s)
```

**Keep the token safe:**
- Valid for 1 hour
- Use in all RCS API calls as: `Authorization: Bearer <access_token>`
- Refresh before expiry (get a new token at 55 minutes)

See rcs-authentication.md for full credential management.

---

### Step 3: Create Your First Template (5 minutes)

Templates are pre-approved message formats. Rich messages are sent via templates.

**Simple text template:**

```json
POST https://api.dotgo.com/directory/secure/api/v1/bots/{botId}/templates

{
  "name": "order_confirmation",
  "type": "text_message",
  "textMessageContent": "Order {{order_id}} confirmed! Track your shipment: {{tracking_url}}",
  "fallbackText": "Order confirmed"
}
```

**With rich media (image + text):**

```json
{
  "name": "product_promotion",
  "type": "rich_card",
  "mediaUrl": "https://cdn.example.com/product.jpg",
  "cardTitle": "New Product Launch",
  "cardDescription": "Limited time offer — 30% off",
  "suggestions": [
    {
      "reply": {
        "displayText": "Shop Now",
        "postback": {"data": "shop_now"}
      }
    }
  ]
}
```

**Status:** Templates are approved within 2-4 hours. Once approved, you can use them to send messages.

See rcs-templates.md for all template types (carousel, PDF, actions).

---

### Step 4: Send Your First Message (2 minutes)

Once your template is approved, send a rich message to a test phone number.

```json
POST https://api.dotgo.com/bot/v1/{botId}/messages/async

{
  "RCSMessage": {
    "templateMessage": {
      "templateCode": "order_confirmation",
      "customParams": {
        "order_id": "ORD-12345",
        "tracking_url": "https://track.example.com/ORD-12345"
      }
    }
  },
  "messageContact": {
    "userContact": "+914251234567"
  }
}
```

**Response:** You'll get a message ID and status ("pending"):

```json
{
  "RCSMessage": {
    "msgId": "msg_abc123",
    "status": "pending"
  }
}
```

See rcs-messaging-api.md for text, file, and rich card examples.

---

### Step 5: Track Message Status (ongoing)

Messages move through these states:
- **pending** → **sent** → **delivered** → **displayed** (if read)
- Or: **failed** / **cancelled** if there's an issue

**Check status anytime:**

```bash
GET https://api.dotgo.com/bot/v1/{botId}/messages/{msgId}/status
```

**Set up webhooks for real-time updates:**

Register a webhook URL in your agent config. You'll receive instant notifications when:
- User sends a message
- Message is delivered/read
- User clicks a suggested action

See rcs-webhooks-and-callbacks.md for webhook setup.

---

## Next Steps

✅ Agent registered and authenticated  
✅ First template created and approved  
✅ First message sent  

**What's next:**

1. **Scale templates** — Create rich card carousels, PDF attachments, actions
2. **Implement webhooks** — Receive user messages and interactions in real-time
3. **Integrate with Bot Studio** — Route RCS messages through journeys
4. **Track analytics** — Monitor delivery, engagement, and ROI
5. **Launch campaigns** — Use Campaign Manager to send multi-channel promotions

---

## Troubleshooting

**Template submission fails:**
- Check media URLs are publicly accessible
- Verify image sizes and formats (JPG/PNG, <90KB for logo)
- Ensure text is under 2500 chars

**Message sending returns 400 error:**
- Verify phone number is in E.164 format: `+1234567890`
- Check template exists and is approved
- Confirm custom parameters match template variables

**Message stuck in "pending" state:**
- May take 30-60 seconds on first try
- Check carrier supports RCS for that phone number
- Verify user's device supports RCS (Android Messages, iPhone iMessage)

See rcs-api-reference.md for all error codes and solutions.

---

## Cross-module workflow docs

- Link agents to **Bot Studio** journeys for conversational workflows
- Use **Campaign Manager** to send RCS messages at scale
- Track metrics in **Analytics** dashboard
- Manage **Webhooks** for real-time event handling

## Reference (from source)

<!-- procedural:v2 -->
# RCS Quickstart

Get your brand live on RCS in 5 minutes with step-by-step agent registration, template creation, and first message send.
