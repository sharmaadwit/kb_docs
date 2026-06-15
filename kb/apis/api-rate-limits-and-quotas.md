<!-- kb-golden:v10 -->
# API Rate Limits and Quotas

**Module**: APIs

## Definition

**Rate Limits** are the maximum number of requests your application can make per unit of time (typically per second or per minute). They control request throughput and prevent API abuse.

**Quotas** are hard limits on resource consumption per billing period or per organization, such as the number of phone numbers or API keys you can create. Unlike rate limits, quotas represent absolute maximum allocations, not temporary throttling.

- **Rate Limit exceeded** → 429 Too Many Requests (temporary, can retry)
- **Quota exceeded** → 400 Bad Request or 403 Forbidden (permanent until quota increases)

## Rate Limits by API

### Message Sending

| Endpoint | Limit | Unit | Notes |
|----------|-------|------|-------|
| `POST /v1/msg/send` | 100 | messages/second per WABA | Includes all message types (text, media, template) |
| `POST /v1/msg/batch/send` | 100 | messages/second per WABA | Applies to bulk send operations |
| `POST /v1/media/upload` | 50 | uploads/second per org | Per-file upload requests |

**What happens when exceeded:**
- Response: `HTTP 429 Too Many Requests`
- Header: `Retry-After: 60` (wait time in seconds)
- Request queued internally; will not be discarded if under quota

### Webhooks

| Endpoint | Limit | Unit | Notes |
|----------|-------|------|-------|
| Incoming webhook delivery | 100 | requests/second per endpoint | Per unique webhook URL |
| Webhook event queue | 10,000 | events | Per webhook endpoint (backlog buffer) |

**What happens when exceeded:**
- Webhooks are queued and retry exponentially
- Max queue size: 10,000 events (older events discarded if exceeded)
- Retry window: 24 hours with exponential backoff

### Template Operations

| Endpoint | Limit | Unit | Notes |
|----------|-------|------|-------|
| `POST /v1/template/create` | 10 | templates/minute per org | WhatsApp template submissions |
| `GET /v1/template/list` | 60 | requests/minute | No per-template limit |
| `POST /v1/template/update` | 10 | updates/minute | For existing templates |

### Authentication & Session Management

| Endpoint | Limit | Unit | Notes |
|----------|-------|------|-------|
| `POST /v1/auth/login` | 60 | requests/minute per user | Prevents brute-force attacks |
| `POST /v1/auth/token/refresh` | 60 | requests/minute per org | API token refresh |
| `POST /v1/api-key/rotate` | 10 | requests/minute per org | API key rotation |

### Analytics & Reporting

| Endpoint | Limit | Unit | Notes |
|----------|-------|------|-------|
| `GET /v1/analytics/messages` | 30 | requests/minute | Historical message data |
| `GET /v1/analytics/campaigns` | 30 | requests/minute | Campaign performance data |
| `GET /v1/reports/export` | 5 | exports/minute | Large data exports |

### General API Endpoints

| Category | Limit | Unit | Notes |
|----------|-------|------|-------|
| Create operations | 60 | requests/minute | Contacts, segments, rules |
| Read operations | 300 | requests/minute | List, get, search endpoints |
| Update operations | 60 | requests/minute | PUT, PATCH endpoints |
| Delete operations | 30 | requests/minute | Destructive operations |

## Quotas by Resource

### Account & Project Quotas

| Resource | Limit | Hard Limit? | Tier-Based? | Notes |
|----------|-------|------------|------------|-------|
| WABAs per organization | Unlimited | No | No | Requires Meta approval for each WABA |
| Phone numbers per WABA | 5 included | No | Yes | Additional numbers require upgrade |
| Business accounts per org | Based on tier | Yes | Yes | Starter: 1, Professional: 5, Enterprise: Unlimited |
| Projects per organization | Unlimited | No | No | Organizational structure only |

### API & Integration Quotas

| Resource | Limit | Hard Limit? | Notes |
|----------|-------|------------|-------|
| API keys per project | 10 | Yes | Request increase for service accounts |
| Active API integrations | 50 | Yes | CRM, ecommerce, analytics platforms |
| Webhook endpoints per org | 20 | Yes | Per webhook configuration setup |
| OAuth applications | 5 | Yes | For partner integrations |

### Data Storage Quotas

| Resource | Limit | Hard Limit? | Notes |
|----------|-------|------------|-------|
| Stored conversations per project | 30 days | Yes | Automatic archival after 30 days |
| Media storage per org | Varies | Yes | Contact support for increase |
| User contacts per segment | 100,000 | No | Can create multiple segments |
| Template library per org | Unlimited | No | Subject to WABA template limits |

### Concurrent Operations Quotas

| Resource | Limit | Hard Limit? | Notes |
|----------|-------|------------|-------|
| Concurrent uploads | 5 | No | Per project; sequential queuing after |
| Concurrent exports | 2 | No | Per organization |
| Active bot conversations | Varies | Yes | Based on plan; scales with volume |

## How Limits Are Enforced

### Rate Limiting Algorithm: Sliding Window

Gupshup uses a **sliding window counter** algorithm to track request counts:

```
Current window: Last 60 seconds
Request arrives → Check total requests in window
If count >= limit → Return 429
Else → Accept request, increment counter
```

**Example: 100 msg/sec limit**
```
00:00 - Add requests 1-100       → All accepted
00:01 - Request 101              → 429 Too Many Requests
00:01 - Request 1 expires        → Window shifts
00:01 - Request 101 (retry)      → Accepted
```

**Advantages:**
- No "thundering herd" at second boundaries
- Fair distribution across time
- Prevents request bursts

### HTTP Response Codes

| Code | Meaning | Retry? | Action |
|------|---------|--------|--------|
| 200 OK | Success | No | Process response normally |
| 429 Too Many Requests | Rate limit exceeded | Yes | Wait and retry with backoff |
| 503 Service Unavailable | Temporary outage | Yes | Retry with exponential backoff |
| 401 Unauthorized | Invalid credentials | No | Check API key/token; regenerate if needed |
| 403 Forbidden | Quota exceeded or insufficient permissions | No | Request quota increase or check permissions |
| 400 Bad Request | Invalid request format | No | Fix request and resubmit |

### Retry-After Header

When you exceed a rate limit, the response includes:
```
HTTP/1.1 429 Too Many Requests
Retry-After: 60
Content-Type: application/json

{
  "error_code": "RATE_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded. Please retry after 60 seconds.",
  "rate_limit": {
    "limit": 100,
    "window_seconds": 60,
    "requests_in_window": 105
  }
}
```

**Interpretation:**
- `Retry-After: 60` means wait 60 seconds before next request
- Can be in seconds (integer) or HTTP-date format

### Backoff Strategy

**Recommended: Exponential Backoff with Jitter**

```python
import time
import random

def api_request_with_backoff(url, max_retries=5):
    for attempt in range(max_retries):
        try:
            response = requests.post(url)
            if response.status_code == 429:
                # Exponential backoff: 2^attempt seconds + random jitter
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"Rate limited. Waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
                continue
            return response
        except Exception as e:
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            print(f"Error: {e}. Retrying in {wait_time:.1f}s...")
            time.sleep(wait_time)
    
    raise Exception("Max retries exceeded")
```

**Formula:**
```
wait_time = (2 ^ attempt) + random_jitter(0, 1)

Attempt 1: 1-2 seconds
Attempt 2: 2-3 seconds
Attempt 3: 4-5 seconds
Attempt 4: 8-9 seconds
Attempt 5: 16-17 seconds
```

**Why jitter?**
- Prevents thundering herd (all clients retrying at same time)
- Distributes load more evenly
- Increases likelihood of success on retry

## How to Request Higher Limits

### Process

1. **Gather Information**
   - Current limit and current usage
   - Expected peak usage volume
   - Time window needed (months/years)
   - Business justification (use case)

2. **Submit Request**
   - Email: `support@gupshup.io` or in-app support ticket
   - Subject: "Rate Limit / Quota Increase Request"
   - Include all information from step 1

3. **Example Request Email**
   ```
   Subject: Rate Limit Increase Request

   Hello,

   We would like to request an increase to our message sending rate limit.

   Current Status:
   - Project: Company Marketing Platform
   - Current limit: 100 messages/second per WABA
   - Current usage: 85 messages/second (peak)
   - Requested limit: 500 messages/second per WABA

   Business Justification:
   We are expanding to 5 new countries and expect to send 200M messages/month.

   Timeline:
   - Implementation date: 2026-08-01
   - Duration: Permanent

   Contact: john.doe@company.com | +1-555-0123

   Best regards,
   John Doe
   ```

4. **Expected Approval Timeline**
   - Standard request: 24-48 hours
   - High-volume requests: 2-5 business days
   - Enterprise requests: Custom SLA

5. **Approval Response**
   - Email confirmation with new limits
   - Effective immediately upon confirmation
   - New limits visible in Console API settings

### Special Considerations

| Scenario | Process | Timeline |
|----------|---------|----------|
| Temporary spike (< 7 days) | Request temporary limit increase | 2-4 hours |
| Permanent increase | Standard request process | 24-48 hours |
| Enterprise custom limits | Account manager coordination | 3-7 days |
| Emergency (outage prevention) | Call support hotline | 15-30 minutes |

## Best Practices for Staying Under Limits

### 1. Batch Requests

**Instead of individual messages:**
```python
# ❌ Bad: 100 API calls for 100 messages
for recipient in recipients:
    send_message(recipient, message)  # 100 calls, hits rate limit

# ✅ Good: 1 API call for 100 messages
send_batch_messages(recipients, message)  # 1 call, 100x more efficient
```

**Batch endpoint:**
```
POST /v1/msg/batch/send
{
  "messages": [
    {"to": "919876543210", "text": "Hello"},
    {"to": "919876543211", "text": "Hello"},
    ...
  ]
}

Max batch size: 1000 messages per request
```

### 2. Use Async Endpoints (Queue Instead of Wait)

**Synchronous (blocking):**
```
POST /v1/msg/send (wait for response)
→ Can only send 100/sec if each response takes >10ms
```

**Asynchronous (non-blocking):**
```
POST /v1/msg/queue
→ Queues message immediately
→ Returns 202 Accepted
→ No waiting; can queue 10,000+ messages/sec
→ Webhook notifies on delivery status
```

### 3. Implement Exponential Backoff

See backoff strategy section above. Key points:
- Always implement client-side backoff
- Don't retry immediately
- Don't retry more than 5 times
- Use Retry-After header if provided

### 4. Monitor Usage Dashboard

**Location in Console:**
```
Project → Settings → API → Usage Statistics
```

**What to monitor:**
- Current requests per second (real-time)
- Daily/weekly trends
- Peak usage times
- Quota utilization

**Example dashboard metrics:**
```
Messages sent: 45M / 50M (90% of monthly quota)
API calls: 2.1B / 3B (70% of request quota)
Active webhooks: 18 / 20 (90% of endpoint quota)
```

### 5. Set Up Alerts

**Alert thresholds:**
- 70% of rate limit → Warning
- 80% of rate limit → Alert
- 90% of quota → Critical

**Example alert setup:**
```
GET /v1/project/alerts
{
  "alerts": [
    {
      "type": "rate_limit",
      "threshold_percent": 80,
      "email": "ops@company.com",
      "enabled": true
    }
  ]
}
```

## Error Handling

### Common Rate Limit Scenarios

#### Scenario 1: Normal Rate Limit (429)

```
Request: 101st message in 1 second
Response:
  HTTP 429 Too Many Requests
  Retry-After: 60
  {"error": "RATE_LIMIT_EXCEEDED"}

Action:
  1. Log the error
  2. Wait 60 seconds
  3. Retry with exponential backoff
  4. Monitor if approaching limit
```

#### Scenario 2: Quota Exceeded (403)

```
Request: Create 11th API key (quota is 10)
Response:
  HTTP 403 Forbidden
  {"error": "QUOTA_EXCEEDED", "current": 10, "limit": 10}

Action:
  1. Cannot retry immediately
  2. Must request quota increase
  3. Or delete unused keys first
  4. Cannot proceed without increase
```

#### Scenario 3: Authentication Error (401)

```
Request: API call with expired token
Response:
  HTTP 401 Unauthorized
  {"error": "INVALID_TOKEN"}

Action:
  1. Do NOT retry
  2. Refresh API key or OAuth token
  3. Resubmit request with new credentials
```

#### Scenario 4: Service Unavailable (503)

```
Request: During planned maintenance
Response:
  HTTP 503 Service Unavailable
  Retry-After: 300
  {"error": "SERVICE_UNAVAILABLE"}

Action:
  1. Implement exponential backoff
  2. Check status page: status.gupshup.io
  3. Retry after Retry-After delay
  4. Max 5 retries before alerting
```

### Error Response Reference Table

| Error Code | HTTP Status | Cause | Retry? | Action |
|-----------|-------------|-------|--------|--------|
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests per second | Yes | Wait and implement backoff |
| `QUOTA_EXCEEDED` | 403 | Reached hard limit on resource | No | Request increase or delete resources |
| `INVALID_TOKEN` | 401 | API key or OAuth token invalid/expired | No | Regenerate credentials |
| `INSUFFICIENT_PERMISSIONS` | 403 | Token missing required scopes | No | Check API key permissions |
| `INVALID_REQUEST` | 400 | Malformed request body or params | No | Fix and resubmit |
| `RESOURCE_NOT_FOUND` | 404 | ID or endpoint does not exist | No | Verify ID and endpoint |
| `CONFLICT` | 409 | Resource already exists or in-use | No | Use existing resource or delete first |
| `SERVICE_UNAVAILABLE` | 503 | Temporary outage | Yes | Implement exponential backoff |
| `INTERNAL_SERVER_ERROR` | 500 | Server error | Yes | Retry with backoff |

## Usage Dashboard

### Accessing Usage Statistics

**Path in Console:**
```
Gupshup Console
  → Your Project
    → Settings
      → API Settings
        → Usage & Quotas
```

### Dashboard Components

1. **Rate Limit Panel**
   ```
   Messages (per second)
   Current: 47/100
   Peak today: 78/100
   Status: Healthy
   ```

2. **Quota Usage Panel**
   ```
   API Keys: 8/10 (80%)
   Webhooks: 18/20 (90%)
   Integrations: 42/50 (84%)
   Action: Consider requesting increase
   ```

3. **Usage Trends**
   - Last 7 days chart
   - Last 30 days chart
   - Breakdown by endpoint
   - Peak time analysis

### How to Read the Charts

**Rate Limit Chart:**
- X-axis: Time (hourly buckets)
- Y-axis: Requests per second
- Red line: 100 msg/sec limit
- Green area: Current usage
- Yellow zone: 70-90% (approaching limit)
- Red zone: 90%+ (critical)

**Quota Usage Chart:**
- Donut/pie chart per quota type
- Color coding: Green (<70%), Yellow (70-89%), Red (90%+)
- Hover for exact numbers
- Click to drill into resource list

### Setting Up Quota Alerts

**In Console:**
```
Settings → Alerts & Notifications
  → API Quota Alerts
    → Add Alert
      - Resource: Messages per second
      - Threshold: 80%
      - Frequency: Daily summary
      - Recipients: ops@company.com
```

**Via API:**
```
POST /v1/project/alerts
{
  "alert_type": "quota",
  "resource": "messages_per_second",
  "threshold_percent": 80,
  "recipients": ["ops@company.com"],
  "enabled": true
}
```

## Summary Table

Quick reference for all limits and quotas:

| Resource | Limit | Unit | Hard Limit? | Enforcement | How to Increase |
|----------|-------|------|------------|-------------|-----------------|
| **Rate Limits** |
| Message sending | 100 | msgs/sec/WABA | Yes | 429 + backoff | Support request |
| Message batch | 100 | msgs/sec/WABA | Yes | 429 + backoff | Support request |
| Media upload | 50 | uploads/sec/org | Yes | 429 + backoff | Support request |
| Webhook delivery | 100 | events/sec/endpoint | Yes | Queue + retry | Support request |
| Template create | 10 | templates/min/org | Yes | 429 + backoff | N/A (Meta limit) |
| Template update | 10 | updates/min/org | Yes | 429 + backoff | N/A (Meta limit) |
| Auth/login | 60 | requests/min/user | Yes | 429 + backoff | Contact support |
| Analytics | 30 | requests/min/org | Yes | 429 + backoff | Support request |
| General create | 60 | requests/min/org | Yes | 429 + backoff | Support request |
| General read | 300 | requests/min/org | Yes | 429 + backoff | Support request |
| **Quotas** |
| API keys | 10 | per project | Yes | 403 Forbidden | Support request |
| Webhooks | 20 | per organization | Yes | 403 Forbidden | Support request |
| Active integrations | 50 | per organization | Yes | 403 Forbidden | Support request |
| Phone numbers | 5 included | per WABA | No | Purchase additional | Plan upgrade |
| Business accounts | Tier-based | per organization | Yes | 403 Forbidden | Plan upgrade |
| Conversation history | 30 | days | Yes | Auto-archive | Contact support |

## See Also

- [API Integration Best Practices](../integrations/api-integration-best-practices.md)
- [Webhook Setup Guide](../integrations/webhook-setup.md)
- [Official API Documentation](https://docs.gupshup.io/docs/api-reference)
- [Console Status Page](https://status.gupshup.io)
- [Support Portal](https://support.gupshup.io)

## Reference (from source)

<!-- procedural:v2 -->
# API Rate Limits and Quotas

Complete reference for rate limiting, quotas, enforcement, and best practices for Gupshup APIs.
