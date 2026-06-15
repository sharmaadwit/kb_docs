source_url: https://docs.gupshup.io/docs/rate-limits

<!-- kb-golden:v10 -->
# API Rate Limits & Quotas

**Module**: APIs

## Definition

Rate limits control request frequency (per second). Quotas control resource allocation (per month/org).

## Rate Limits by API

| API | Limit | What Happens |
|-----|-------|--------------|
| Send Message | 100/sec per WABA | Returns 429, retry with backoff |
| Webhooks | 100/sec per endpoint | Webhook delivery queued, retried |
| Template Creation | 10/min | Returns 429 error |
| Authentication | 60/min | Returns 429, wait before retry |
| Contact Lookup | 100/sec | Returns 429 error |

## Quotas by Resource

| Resource | Limit | How to Increase |
|----------|-------|-----------------|
| WABAs per org | Unlimited (approval-based) | Contact support with use case |
| Phone numbers per WABA | 5 included | +$5/month per additional |
| Business accounts | Based on tier | Upgrade plan |
| API keys | 10 | Contact support |
| Active integrations | 50 | Contact support |
| Webhook endpoints | 20 per WABA | Contact support |

## How Limits Are Enforced

**Rate limiting algorithm:** Sliding window (per-second)

**When you exceed limit:**
```
HTTP 429 Too Many Requests
Retry-After: 60 (seconds to wait before retry)
```

**Recommended backoff:**
```
Attempt 1: Fail immediately
Wait 1 second, retry
Attempt 2: Fail
Wait 2 seconds, retry
Attempt 3: Fail
Wait 4 seconds, retry
(exponential backoff)
```

## Request Higher Limits

1. **Go to:** Console → Settings → Support
2. **Submit:** Business justification + expected volume
3. **Wait:** 24-48 hours for response
4. **Example:** "We send 500K messages/day to seasonal promotions"

## Best Practices

### Batch Requests
❌ Don't: Send 1000 API calls sequentially
```python
for user in users:
    send_message(user)  # 1000 calls = slow, risk rate limit
```

✅ Do: Batch requests
```python
messages = [build_message(u) for u in users]
send_batch(messages)  # 1 call = fast, under limit
```

### Use Async Endpoints
❌ Synchronous: Wait for response
```
POST /messages (waits for delivery confirmation)
```

✅ Asynchronous: Queue message, don't wait
```
POST /messages/async (returns immediately)
```

### Implement Exponential Backoff
```python
import time
import random

def send_with_retry(message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return api.send(message)
        except RateLimitError as e:
            wait_time = 2 ** attempt + random.uniform(0, 1)
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
```

### Monitor Usage
- Check Console → Analytics → Usage
- Set alerts at 80% of limit
- Reduce batch size if approaching limits

## Error Codes

| Code | Meaning | Fix |
|------|---------|-----|
| 429 | Too Many Requests | Wait and retry with backoff |
| 503 | Service Unavailable | Retry with exponential backoff |
| 401 | Unauthorized | Check API key is valid |
| 403 | Forbidden | Check permissions for API key |

## Reference (from source)

<!-- procedural:v2 -->
# API Rate Limits & Quotas

Rate limits, quotas, enforcement, and best practices for staying under limits.
