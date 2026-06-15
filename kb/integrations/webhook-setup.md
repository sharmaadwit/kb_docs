source_url: https://docs.gupshup.io/docs/integrations-platform

<!-- kb-golden:v10 -->
# Webhook Integration Setup

**Module**: Integrations

## Definition

Webhooks enable real-time event delivery from Gupshup to external systems. When an event occurs (message received, campaign sent, form submitted, etc.), Gupshup sends an HTTP POST to your webhook endpoint with event details.

## Webhook Events

**Available events from Gupshup:**

| Event | Trigger | Payload | Use Case |
|-------|---------|---------|----------|
| `message.received` | User sent message | Phone, text, channel | Receive customer messages |
| `message.delivered` | Message successfully delivered | Message ID, timestamp | Track message delivery |
| `message.read` | User read message | Message ID, timestamp | Track message engagement |
| `message.clicked` | User clicked button/link | Message ID, link, postback | Track link clicks |
| `campaign.sent` | Campaign completed | Campaign ID, recipient count | Track campaign status |
| `campaign.bounce` | Campaign bounced | Campaign ID, phone | Handle bounces |
| `lead.created` | New lead from form | Form data, phone, name | Create leads in CRM |
| `interaction.completed` | Conversation finished | Conversation ID, messages | Archive conversation |
| `form.submitted` | User submitted form | Form data, responses | Process form data |

## Webhook Setup Steps

### 1. Prepare HTTPS Endpoint

**Requirements:**
- HTTPS endpoint (HTTP not allowed)
- Publicly accessible URL
- Accepts POST requests with JSON body
- Responds with 200 OK within 5 seconds
- Can handle ~100 requests/second during peak

**Example endpoint:**
```
https://example.com/webhooks/gupshup
```

**Your code should:**
```python
@app.route('/webhooks/gupshup', methods=['POST'])
def webhook():
    payload = request.get_json()
    
    # Verify signature
    if not verify_signature(payload, request.headers):
        return 'Unauthorized', 401
    
    # Queue processing (don't process in request handler)
    queue.enqueue(process_webhook, payload)
    
    # Respond immediately
    return 'OK', 200
```

### 2. Register Webhook in Integrations Platform

1. Go to **Integrations Platform → Webhooks**
2. Click **Add Webhook**
3. Enter webhook URL: `https://example.com/webhooks/gupshup`
4. Choose events to subscribe:
   - `message.received`
   - `message.delivered`
   - `campaign.sent`
   - (etc.)
5. Click **Save**
6. Copy webhook ID and secret (for signature verification)

### 3. Implement Signature Verification

**Why:** Ensures webhooks are from Gupshup, prevents malicious requests

**How it works:**
1. Gupshup sends webhook with `X-Signature` header
2. Signature = HMAC-SHA256(payload, secret)
3. Your endpoint verifies signature
4. Reject if signature doesn't match

**Implementation:**

```python
import hmac
import hashlib
import json

WEBHOOK_SECRET = "your_webhook_secret_here"

def verify_signature(payload, headers):
    """Verify webhook signature"""
    signature = headers.get('X-Signature')
    if not signature:
        return False
    
    # If payload is dict, convert to JSON string
    if isinstance(payload, dict):
        payload_str = json.dumps(payload, separators=(',', ':'), sort_keys=True)
    else:
        payload_str = payload
    
    # Calculate expected signature
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload_str.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Compare (use constant-time comparison to prevent timing attacks)
    return hmac.compare_digest(signature, expected)

@app.route('/webhooks/gupshup', methods=['POST'])
def webhook():
    payload = request.get_json()
    
    # Verify signature FIRST
    if not verify_signature(payload, request.headers):
        return 'Unauthorized', 401
    
    # Process webhook
    event = payload.get('event')
    data = payload.get('data')
    
    if event == 'message.received':
        handle_message_received(data)
    elif event == 'campaign.sent':
        handle_campaign_sent(data)
    
    # Respond immediately (queue async processing)
    return 'OK', 200
```

### 4. Test Webhook

1. **Send test event from platform:**
   - Integrations Platform → Webhooks → [Your webhook] → **Send Test**
   - Gupshup sends test event to your endpoint

2. **Verify receipt:**
   - Check your server logs
   - Verify signature was valid
   - Confirm webhook was processed

3. **Check integration logs:**
   - Go back to Integrations Platform
   - View webhook delivery logs
   - Should show "Delivered" status for test event

## Webhook Payload Examples

### Message Received Event

```json
{
  "event": "message.received",
  "timestamp": "2026-06-12T16:35:28Z",
  "webhook_id": "wh_abc123",
  "data": {
    "conversation_id": "conv_12345",
    "user_phone": "919876543210",
    "message_id": "msg_xyz789",
    "message_text": "Hello, I need help with my order",
    "channel": "whatsapp",
    "media": null,
    "metadata": {
      "user_name": "John Doe",
      "user_email": "john@example.com",
      "bot_id": "bot_456"
    }
  }
}
```

### Campaign Sent Event

```json
{
  "event": "campaign.sent",
  "timestamp": "2026-06-12T16:35:28Z",
  "webhook_id": "wh_abc123",
  "data": {
    "campaign_id": "camp_789",
    "campaign_name": "Order Confirmation June",
    "channel": "whatsapp",
    "total_recipients": 5000,
    "total_sent": 4950,
    "total_failed": 50,
    "status": "completed"
  }
}
```

### Lead Created Event

```json
{
  "event": "lead.created",
  "timestamp": "2026-06-12T16:35:28Z",
  "webhook_id": "wh_abc123",
  "data": {
    "lead_id": "lead_999",
    "user_phone": "919876543210",
    "user_name": "Jane Smith",
    "user_email": "jane@example.com",
    "form_id": "form_123",
    "form_data": {
      "product_interest": "Enterprise Plan",
      "company_size": "100-500"
    }
  }
}
```

## Best Practices

### 1. Verify Signature on Every Webhook
```python
# ALWAYS verify signature first
if not verify_signature(payload, headers):
    return 'Unauthorized', 401
```

### 2. Respond Quickly (200 OK)
```python
# Queue async processing, respond immediately
queue.enqueue(process_webhook, payload)
return 'OK', 200
```

### 3. Implement Idempotency
```python
# Handle duplicate events (Gupshup retries on failure)
webhook_id = payload.get('webhook_id')
if already_processed(webhook_id):
    return 'OK', 200  # Already processed, skip

process_webhook(payload)
mark_as_processed(webhook_id)
return 'OK', 200
```

### 4. Log All Webhooks
```python
import logging

logger = logging.getLogger(__name__)

def webhook():
    logger.info(f"Received webhook: {payload.get('event')}")
    try:
        process_webhook(payload)
    except Exception as e:
        logger.error(f"Failed to process webhook: {e}")
        # Still respond 200 to stop retries
        return 'OK', 200
```

### 5. Use Exponential Backoff for Retries
```python
# If your processing fails, Gupshup will retry
# First retry: 5 seconds
# Second retry: 25 seconds
# Third retry: 125 seconds
# Then give up
```

### 6. Monitor Webhook Health
```python
# Track metrics
webhooks_received = 0
webhooks_processed = 0
webhooks_failed = 0

# Alert if failure rate > 5%
if webhooks_failed / webhooks_received > 0.05:
    send_alert("High webhook failure rate")
```

## Webhook Limitations

- **Timeout:** 5 seconds to respond (queue for async processing)
- **Payload size:** Max 1MB per webhook
- **Frequency:** Up to 100 requests/second during peak
- **Retry policy:** 3 retries with exponential backoff (5s, 25s, 125s)
- **Storage:** Delivery logs retained for 30 days

## Troubleshooting

### Webhook Not Being Called

**Check:**
1. Is webhook URL publicly accessible? (Test with curl)
2. Is endpoint accepting POST requests?
3. Is endpoint returning 200 OK?
4. Check Integrations Platform logs for errors

**Test:**
```bash
curl -X POST https://example.com/webhooks/gupshup \
  -H "Content-Type: application/json" \
  -d '{"event":"test"}'
```

### Signature Verification Failing

**Check:**
1. Using correct webhook secret?
2. Comparing raw payload (not parsed JSON)?
3. Using constant-time comparison?
4. Webhook secret hasn't rotated?

### Duplicate Events

**Expected behavior:** Gupshup may send duplicate webhooks during retries

**Solution:** Implement idempotency by checking webhook_id

## See Also

- [Integrations Platform Overview](./integrations-platform-overview.md)
- [API Integration Best Practices](./api-integration-best-practices.md)
- [CRM Integrations](./crm-integrations.md)
- [Official Webhook Docs](https://docs.gupshup.io/docs/integrations-platform)

## Reference (from source)

<!-- procedural:v2 -->
# Webhook Integration Setup

Real-time event delivery from Gupshup to external systems via HTTPS webhooks with signature verification.
