source_url: https://console-docs.gupshup.io/docs/error-handling-http-errors

<!-- kb-consulting:error-recovery-framework -->
# Error Handling: HTTP Error Recovery (4xx/5xx)

**Module**: Bot Studio
**Category**: Error Recovery Framework
**Consultation Tier**: Tactical Recovery

## Definition

Recovery strategies for HTTP status code errors (4xx client errors, 5xx server errors). Provides specific troubleshooting steps for common status codes and routing to appropriate recovery action.

## HTTP Error Classification & Recovery

### Understanding HTTP Error Categories

**4xx errors = Client's fault**
- You sent a bad request
- API is correctly rejecting it
- Don't retry (retry will also fail)
- Fix the request, then retry

**5xx errors = Server's fault**
- API server has a problem
- Your request may have been valid
- Retry (server might recover)
- Use exponential backoff to avoid overwhelming server

**429 errors = Rate limit exceeded**
- Your request rate too high
- Respect Retry-After header
- Implement exponential backoff
- Consider reducing request frequency

---

## Common HTTP Status Codes & Recovery

### 4xx Client Errors (Fix Your Request)

#### 400 Bad Request
**What it means**: Request format is invalid.

**Common causes**:
- Malformed JSON (missing comma, extra bracket)
- Missing required field in request body
- Wrong data type (string instead of number)
- Invalid header format

**How to fix**:
1. Check Bot Studio API node configuration
2. Verify all required fields are present
3. Confirm data types match API spec (numbers as `123`, not `"123"`)
4. Validate JSON is syntactically correct
5. Check for special characters that need escaping

**Example fix**:
```
❌ Wrong:  {"user_id": "12345", "amount": "$99.99"}
✅ Correct: {"user_id": 12345, "amount": 99.99}
```

**Recommended action**: Fix request → **Don't retry** (retrying won't help)

---

#### 401 Unauthorized
**What it means**: API authentication failed (credentials missing, expired, or invalid).

**Common causes**:
- API token expired (OAuth tokens have expiry dates)
- API key is wrong or revoked
- Authorization header missing or malformed
- API key doesn't have required scopes

**How to diagnose**:
1. Check Bot Studio API Management (Settings → API → Manage APIs)
2. Verify API key/token is correct
3. Check token expiry (if OAuth, is token expired?)
4. Confirm header format is correct (`Authorization: Bearer TOKEN`)

**How to fix**:
1. **For API Key**: Refresh key from API provider (may need to regenerate)
2. **For OAuth Token**: Refresh token (most providers support automatic refresh)
3. Update Bot Studio API configuration with new credentials
4. Test API connection
5. Deploy changes

**Recommended action**: Refresh credentials → Retry request

---

#### 403 Forbidden
**What it means**: You're authenticated, but don't have permission to access this resource.

**Common causes**:
- API key doesn't have required permission scopes
- User account doesn't have access to resource
- API endpoint restricted to higher tier accounts

**How to diagnose**:
1. Verify API key scopes in provider dashboard (Settings → API Keys → Scopes)
2. Check if API endpoint requires special permissions
3. Confirm user account has access level for this resource

**How to fix**:
1. **To add permissions**: Ask API provider to grant scopes to your API key
2. Or: Generate new API key with required scopes
3. Or: Upgrade account tier (if endpoint requires higher tier)
4. Update Bot Studio configuration with new key
5. Retry

**Recommended action**: Request higher permissions → Update credentials → Retry

---

#### 404 Not Found
**What it means**: Endpoint or resource doesn't exist at that URL.

**Common causes**:
- URL is spelled wrong (typo in endpoint)
- API endpoint was deprecated/removed
- Resource ID doesn't exist (user ID invalid)
- Path structure changed (API versioning)

**How to diagnose**:
1. Double-check URL spelling (look for typos)
2. Verify resource ID exists (is the user_id or item_id valid?)
3. Check API documentation for correct endpoint path
4. Compare with API provider's changelog (did endpoint move?)

**How to fix**:
1. **If URL wrong**: Fix the endpoint URL in Bot Studio API node
2. **If resource not found**: Verify resource ID is correct
3. **If endpoint deprecated**: Update to new endpoint from documentation
4. Test the new URL
5. Deploy changes

**Recommended action**: Verify endpoint & resource ID → Update URL → Retry

---

#### 409 Conflict
**What it means**: Request conflicts with existing data (usually duplicate).

**Common causes**:
- Creating resource that already exists
- Updating with conflicting state
- Missing idempotency key on retry

**How to fix**:
1. Check if resource already exists in target system
2. Add idempotency key to prevent duplicates on retry
3. Or: Use update/merge instead of create
4. Retry with correction

**Recommended action**: Check for duplicates → Fix conflict → Retry (possibly with idempotency key)

---

#### 422 Unprocessable Entity
**What it means**: Request format is valid, but content violates business rules.

**Common causes**:
- Invalid business logic (e.g., order amount negative)
- Constraint violation (e.g., email already exists)
- Business rule not met (e.g., user under 18)

**How to diagnose**:
1. Read error message carefully (should explain the violation)
2. Check API documentation for business rules
3. Verify data meets all constraints

**How to fix**:
1. Review validation error message
2. Update request to comply with business rules
3. Retry

**Recommended action**: Fix business logic → Retry

---

### 5xx Server Errors (Retry with Backoff)

#### 500 Internal Server Error
**What it means**: API server crashed or encountered unexpected error.

**Common causes**:
- API server bug (crash)
- Unhandled exception in API code
- Database connection lost
- Temporary glitch

**How to diagnose**:
- Check API provider's status page (is service affected?)
- Is error intermittent (retry succeeds) or persistent?
- Check API logs for details

**How to fix**:
1. **Immediate**: Implement retry with exponential backoff
2. **First retry**: Wait 1-2 seconds, then retry
3. **If still fails**: Wait longer (5-10 seconds), retry again
4. **If persists >1 hour**: Escalate to API provider support

**Recommended action**: Retry with exponential backoff (see [Smart Retry](./error-handling-smart-retry.md))

---

#### 502 Bad Gateway
**What it means**: API gateway failed or upstream server unavailable.

**Common causes**:
- Upstream service down (the API is calling another service that's down)
- API gateway crashed
- Network connectivity issue between gateway and backend
- Temporary service disruption

**How to diagnose**:
- Check API provider's status page
- Is error intermittent (might be temporary) or consistent (might be widespread)?
- Try again in 30 seconds

**How to fix**:
1. Wait 2-5 seconds
2. Retry request
3. If still fails, wait longer (10-30 seconds) and retry
4. Use exponential backoff for multiple retries

**Recommended action**: Retry with exponential backoff (see [Smart Retry](./error-handling-smart-retry.md))

---

#### 503 Service Unavailable
**What it means**: API is temporarily unavailable (overloaded, in maintenance, or degraded).

**Common causes**:
- Scheduled maintenance window
- Traffic spike (API overloaded)
- Service degradation (partial outage)
- Database maintenance

**How to diagnose**:
- Check API provider's status page (is maintenance scheduled?)
- Are other users reporting issues?
- Is error intermittent (traffic spike) or persistent (maintenance)?

**How to fix**:
1. **Check status page**: Confirm when service will be back
2. **If temporary**: Wait 30-60 seconds, then retry
3. **If maintenance**: Wait until maintenance window ends
4. **For traffic spikes**: Implement aggressive backoff to reduce load

**Recommended action**: Wait → Retry with exponential backoff (see [Smart Retry](./error-handling-smart-retry.md))

---

#### 504 Gateway Timeout
**What it means**: API gateway didn't get response from upstream service in time.

**Similar to**: Regular timeout, but at gateway level

**Common causes**:
- Upstream service slow or unresponsive
- Network latency
- Load spike causing slow processing

**How to fix**:
1. Retry with exponential backoff
2. Consider increasing timeout setting
3. Check if upstream API has known issues

**Recommended action**: Retry with exponential backoff (see [Smart Retry](./error-handling-smart-retry.md))

---

### 429 Too Many Requests (Rate Limit)

**What it means**: You've exceeded the API's request rate limit.

**Common causes**:
- Sending too many requests per second
- Concurrent requests exceeding limit
- Not respecting previous rate limit responses
- No backoff between retries

**Key headers**:
- `Retry-After`: Seconds to wait before retrying (ALWAYS respect this)
- `X-RateLimit-Limit`: Max requests per time window
- `X-RateLimit-Remaining`: Requests left before hitting limit
- `X-RateLimit-Reset`: Unix timestamp when limit resets

**How to diagnose**:
1. Check `Retry-After` header (wait this many seconds)
2. Review request frequency (are you sending many in parallel?)
3. Check if you have other bots/integrations using the same API key

**How to fix**:
1. Immediately respect `Retry-After` header
2. Implement exponential backoff for retries
3. Reduce request frequency (batch requests, add delays)
4. If rate limit persists:
   - Monitor usage in API provider dashboard
   - Request higher rate limit (contact support)
   - Consider upgrading tier

**Recommended action**: Implement exponential backoff + respect Retry-After (see [Smart Retry](./error-handling-smart-retry.md))

---

## Decision Tree: "Should I Retry This?"

```
Is the HTTP status code 4xx (except 429)?
├─ YES (400, 401, 403, 404, etc.)
│  └─ DON'T RETRY
│     └─ Fix your request first
│        └─ Then retry
│
├─ NO, it's 5xx (500, 502, 503, 504)
│  └─ YES, RETRY
│     └─ Use exponential backoff
│        └─ Max 3-5 attempts
│
└─ NO, it's 429
   └─ YES, RETRY
      └─ Respect Retry-After header
         └─ Use exponential backoff
```

---

## HTTP Error Recovery Checklist

### For 4xx Errors (Client Fault):

```
✓ Step 1: Read error message carefully
✓ Step 2: Identify what's wrong with your request
✓ Step 3: Fix the issue (format, auth, URL, permissions)
✓ Step 4: Test API connection with fixed request
✓ Step 5: If success, deploy changes
✓ Step 6: If still fails, check API documentation for requirements
```

### For 5xx Errors (Server Fault):

```
✓ Step 1: Check API provider status page
✓ Step 2: Implement retry with exponential backoff
✓ Step 3: First attempt: Wait 1-2 seconds, retry
✓ Step 4: Second attempt: Wait 4-8 seconds, retry
✓ Step 5: Third attempt: Wait 16-32 seconds, retry
✓ Step 6: If still failing after 3 retries: Log error, escalate
```

### For 429 Rate Limit:

```
✓ Step 1: Check Retry-After header
✓ Step 2: Wait at least that many seconds
✓ Step 3: Implement exponential backoff for future requests
✓ Step 4: Reduce request frequency (batch, add delays)
✓ Step 5: Monitor usage dashboard
✓ Step 6: If persistent: Request higher rate limit
```

---

## Production Error Handling Best Practices

### 1. Don't Retry 4xx Errors
**Wrong**:
```
API returns 400 Bad Request
→ Wait and retry
→ Still fails (because request is still bad)
→ Wastes time and resources
```

**Right**:
```
API returns 400 Bad Request
→ Fix the request
→ Retry
→ Succeeds
```

### 2. Always Retry 5xx Errors (with backoff)
**Wrong**:
```
API returns 500 error
→ Give up immediately
→ User journey breaks
→ API recovers, but never retried
```

**Right**:
```
API returns 500 error
→ Wait 1-2 seconds
→ Retry
→ Succeeds (API recovered)
```

### 3. Respect Rate Limit Headers
**Wrong**:
```
API returns 429
Retry-After: 60
→ Retry immediately (2 seconds later)
→ Still rate limited
→ Keep hammering API
```

**Right**:
```
API returns 429
Retry-After: 60
→ Wait 60 seconds
→ Retry
→ Succeeds
```

### 4. Use Exponential Backoff
**Wrong** (Linear backoff):
```
Attempt 1: Fail (0s)
Attempt 2: Wait 5s, Fail
Attempt 3: Wait 5s, Fail
Total time: 10 seconds
```

**Right** (Exponential backoff):
```
Attempt 1: Fail (0s)
Attempt 2: Wait 1s, Fail
Attempt 3: Wait 2s, Fail
Attempt 4: Wait 4s, Succeed
Total time: 7 seconds (faster recovery)
```

---

## Consulting Notes

**For Consulting Tone:**
- "I see you're getting a [STATUS_CODE]. This typically means [CAUSE]."
- "The recovery strategy for [STATUS_CODE] is [STRATEGY]."
- "This is a [4xx/5xx] error, so [retry/don't retry]."
- "Let's start by checking [DIAGNOSTIC_STEP]."
- "If you continue seeing this, we should escalate to the API provider."

**When to Escalate:**
- Persistent 5xx errors for >1 hour (API provider issue)
- Rate limit errors even with backoff implemented (need higher tier)
- 401/403 after confirming credentials are correct (API key revoked/issue)
- Recurring 400 errors after fixing request format (API behavior changed)

---

## See Also

- [Error Recovery: Diagnosing Error Patterns](./error-handling-diagnosing-error-patterns.md)
- [Error Recovery: Timeout Errors](./error-handling-timeout-recovery.md)
- [Error Recovery: Smart Retry Implementation](./error-handling-smart-retry.md)
- [Error Recovery: Fallback Services & Circuit Breaker](./error-handling-fallback-patterns.md)
- [Error Recovery: Production Checklist](./error-handling-production-checklist.md)
- [API Rate Limits & Quotas](../apis/api-rate-limits-and-quotas.md)
- [API Integration Best Practices](../integrations/api-integration-best-practices.md)
