# HTTP Error Recovery — Status Code Strategies

## Diagnosis: Which HTTP Error Are You Getting?

### 4xx Errors (Client Fault)
- **400 Bad Request:** Fix request payload, retry
- **401 Unauthorized:** Token expired, refresh and retry
- **403 Forbidden:** Check permissions/scopes
- **404 Not Found:** Verify URL/resource exists
- **429 Rate Limited:** Respect Retry-After header, backoff

### 5xx Errors (Server Fault)
- **500 Internal Error:** Retry with backoff
- **502 Bad Gateway:** Retry, likely temporary
- **503 Service Unavailable:** Wait, then retry
- **504 Gateway Timeout:** Retry with increased timeout

## Context: Different Recovery Strategy for Each

**4xx = Client's problem** → Fix first, don't blindly retry  
**5xx = Server's problem** → Retry with exponential backoff

## Options: Recovery Strategies

### Option 1: Immediate Fail (for 4xx)
Don't retry. Log error, escalate to developer.

### Option 2: Exponential Backoff (for 5xx)
Retry at: 1s, 2s, 4s, 8s, with jitter

### Option 3: Fallback Service (for critical APIs)
If primary fails, try secondary endpoint

### Option 4: User Escalation
If all retries exhausted, route to human support

## Recommended Approach

**Check status code → Apply appropriate recovery:**
- 4xx: Log & escalate (don't waste retries)
- 5xx: Retry with backoff (max 3-5 attempts)
- 429: Respect rate limit headers
- Critical API failures: Use fallback service

## Monitoring

Track HTTP error distribution weekly. Alert if 5xx errors >2%.
