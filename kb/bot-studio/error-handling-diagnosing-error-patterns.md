source_url: https://console-docs.gupshup.io/docs/error-handling-diagnosis

<!-- kb-consulting:error-recovery-framework -->
# Error Handling: Diagnosing Error Patterns

**Module**: Bot Studio
**Category**: Error Recovery Framework
**Consultation Tier**: Diagnostic

## Definition

Identifies what type of API error you're encountering and routes you to the appropriate recovery guide. The framework classifies errors by root cause (network, authentication, validation, server) rather than just HTTP status codes.

## Diagnostic Framework

### DECISION TREE: "What type of error are you seeing?"

#### Step 1: Identify the Error Source

**Question**: When does the error occur?

| Scenario | Error Type | Next Step |
|----------|-----------|-----------|
| "API never responds, times out after X seconds" | **Timeout Error** | → Go to [Timeout Error Recovery](./error-handling-timeout-recovery.md) |
| "I get a response with status code like 400, 401, 404" | **4xx Client Error** | → Go to [HTTP Error Recovery (4xx/5xx)](./error-handling-http-errors.md) |
| "I get a response with status code like 500, 502, 503" | **5xx Server Error** | → Go to [HTTP Error Recovery (4xx/5xx)](./error-handling-http-errors.md) |
| "Response received but doesn't match expected format (JSON parsing fails)" | **Data Validation Error** | → See Validation section below |
| "401, 403 errors - 'Unauthorized' or 'Forbidden'" | **Authentication Error** | → See Authentication section below |
| "429 error - 'Too Many Requests'" | **Rate Limit Error** | → Go to [Smart Retry Implementation](./error-handling-smart-retry.md) |

---

## Error Classification System

### 1. Timeout Errors

**What it is**: API doesn't respond within the configured timeout window (default 10 seconds).

**Root causes**:
- Network latency (geographical distance, slow connection)
- API server under load (slow response processing)
- External service dependency slow (3rd party API lag)
- Large response payload taking time to transmit

**How to diagnose**:
- Check Bot Studio logs for "Connection timeout" or "Request timeout"
- Measure response time: Is API consistently slow? Or intermittent?
- Check API provider status page (is service degraded?)

**Recovery path**: [Timeout Error Recovery](./error-handling-timeout-recovery.md)

---

### 2. HTTP 4xx Client Errors (400, 401, 403, 404)

**What it is**: Your request has an issue. The API is rejecting it because of something you sent.

**Common subtypes**:
- **400 Bad Request**: Request format invalid (malformed JSON, missing required field)
- **401 Unauthorized**: Authentication failed (expired token, invalid API key)
- **403 Forbidden**: Authenticated but not permitted to access resource
- **404 Not Found**: Endpoint or resource doesn't exist (URL wrong, ID invalid)

**Root causes**:
- Incorrect request format (wrong JSON structure)
- Missing or expired authentication credentials
- Request contains invalid data type (e.g., string where number expected)
- API endpoint or resource has changed
- Permissions insufficient for API key being used

**How to diagnose**:
- Check Bot Studio logs for exact error message and status code
- Verify request format matches API documentation
- Confirm API credentials are valid and not expired
- Validate request payload (all required fields present?)

**Recovery path**: [HTTP Error Recovery (4xx/5xx)](./error-handling-http-errors.md)

---

### 3. HTTP 5xx Server Errors (500, 502, 503, 504)

**What it is**: Your request was valid, but the API server failed to process it.

**Common subtypes**:
- **500 Internal Server Error**: Generic server error
- **502 Bad Gateway**: API gateway failed or upstream server unavailable
- **503 Service Unavailable**: API temporarily overloaded or in maintenance
- **504 Gateway Timeout**: Upstream server took too long to respond

**Root causes**:
- API server crashes or bugs
- Temporary service degradation or maintenance
- Database connectivity issues on API side
- Load spike (too many concurrent requests to API)
- Upstream dependency failure

**How to diagnose**:
- Check API provider's status page (is service down/degraded?)
- Check if error is intermittent (retry succeeds?) or persistent
- Monitor error rate over time (spike indicates load issue)

**Recovery path**: [HTTP Error Recovery (4xx/5xx)](./error-handling-http-errors.md) → Retry with backoff

---

### 4. Rate Limit Errors (429)

**What it is**: You've exceeded the API's request rate limit. The API is throttling your requests.

**Root causes**:
- Too many requests in a short time window
- Not respecting rate limit headers (Retry-After)
- Concurrent requests exceeding per-second limit
- No exponential backoff between retries

**How to diagnose**:
- Check HTTP response code: **429 Too Many Requests**
- Look for `Retry-After` header (tells you how long to wait)
- Review request frequency (are you sending many requests in parallel?)

**Recovery path**: [Smart Retry Implementation](./error-handling-smart-retry.md) → Implement exponential backoff

---

### 5. Authentication Errors (401, 403)

**What it is**: Your API credentials are missing, expired, or don't have permission.

**Subtypes**:
- **401**: Credentials missing or expired (token invalid, API key wrong)
- **403**: Credentials valid but insufficient permissions (API key has wrong scopes)

**Root causes**:
- API token expired (OAuth tokens have expiry)
- API key revoked or rotated
- Wrong credentials in Bot Studio configuration
- API key doesn't have permission for this endpoint

**How to diagnose**:
- Verify API credentials in Bot Studio (Settings → API Management)
- Check if token/key is expired (compare against provider's expiry date)
- Confirm API key has correct scopes/permissions for endpoint

**Recovery path**: Refresh credentials → Retry request

---

### 6. Data Validation Errors

**What it is**: API responded, but response format doesn't match what you expected.

**Root causes**:
- API changed response structure (breaking API change)
- Variable mapping in Bot Studio incorrect (expecting wrong field names)
- Response is error message HTML (API returned 200 but with error content)
- JSON parsing fails (response not valid JSON)

**How to diagnose**:
- Check actual API response vs. expected schema
- Enable debug logging (Bot Studio → Debug Mode)
- Verify JSON Handler node is configured correctly
- Check if API changed response format (check their changelog)

**Recovery path**: Update JSON Handler mapping → Re-test API

---

## When to Choose Which Recovery Path

### Quick Reference Decision Table

| Error Type | Status Code | Root Cause Category | Recovery Guide |
|-----------|------------|-------------------|-----------------|
| Timeout | (none - timeout occurred) | Network/Slow API | [Timeout Recovery](./error-handling-timeout-recovery.md) |
| Bad Request | 400 | Your request format | [HTTP Error Recovery](./error-handling-http-errors.md) |
| Unauthorized | 401 | Auth expired/missing | Refresh token/key, then retry |
| Forbidden | 403 | Insufficient permissions | Check API key scopes |
| Not Found | 404 | URL/resource wrong | Verify endpoint & resource ID |
| Server Error | 500 | API bug/crash | [HTTP Error Recovery](./error-handling-http-errors.md) → Retry |
| Bad Gateway | 502 | Upstream failure | [HTTP Error Recovery](./error-handling-http-errors.md) → Retry |
| Unavailable | 503 | Overload/maintenance | [HTTP Error Recovery](./error-handling-http-errors.md) → Retry with backoff |
| Rate Limited | 429 | Too many requests | [Smart Retry](./error-handling-smart-retry.md) → Exponential backoff |
| Data Format | (varies) | Response schema mismatch | Update JSON Handler mapping |

---

## Recommended Diagnostic Process

### Step 1: Check Error Details (2 minutes)
1. Look at Bot Studio logs or test results
2. Note the exact error: status code, message, timestamp
3. Check if error is **consistent** (happens every time) or **intermittent** (happens sometimes)

### Step 2: Classify Error Type (1 minute)
Use the Decision Tree above to identify which category your error falls into.

### Step 3: Go to Recovery Guide (5-10 minutes)
- **Timeout errors** → [Timeout Error Recovery](./error-handling-timeout-recovery.md)
- **4xx/5xx HTTP errors** → [HTTP Error Recovery](./error-handling-http-errors.md)
- **429 rate limit** → [Smart Retry Implementation](./error-handling-smart-retry.md)
- **401/403 auth** → Check credentials, refresh token, retry
- **Data validation** → Update JSON Handler, re-test

### Step 4: Apply Recovery Strategy
Follow the specific recovery guide for your error type.

### Step 5: Monitor & Escalate
- Does retry succeed? ✅ Problem solved
- Does it still fail? → Log error for further investigation
- Persistent failures? → Escalate to API provider support

---

## Key Principles

1. **Error Type Matters**: Same HTTP status code can have different causes and different recovery strategies
2. **Retryable vs Non-Retryable**: Some errors (5xx) should be retried; others (4xx, except 429) should not
3. **Root Cause Focus**: Understanding *why* the error happened guides the recovery action
4. **Validation First**: Always check your request before retrying—don't retry a bad request

---

## Consulting Notes

**For Consulting Tone:**
- "Let's start by identifying what type of error you're seeing."
- "Based on the error code and behavior, I believe this is [ERROR_TYPE]. Here's what that means..."
- "The recovery strategy differs depending on the root cause. Let's figure out which applies to you."
- "This type of error is usually [ROOT_CAUSE]. Let's confirm by checking [DIAGNOSTIC_STEP]."

**When to Escalate:**
- Persistent 5xx errors for >1 hour (API provider issue)
- Consistent 404 errors after verifying URL is correct (endpoint deprecated)
- Authentication failures after refreshing credentials (API key revoked)
- Rate limit errors even with backoff (need to request higher limit)

---

## See Also

- [Error Recovery: HTTP Errors (4xx/5xx)](./error-handling-http-errors.md)
- [Error Recovery: Timeout Errors](./error-handling-timeout-recovery.md)
- [Error Recovery: Smart Retry Implementation](./error-handling-smart-retry.md)
- [Error Recovery: Fallback Services & Circuit Breaker](./error-handling-fallback-patterns.md)
- [Error Recovery: Production Checklist](./error-handling-production-checklist.md)
- [API Node: HTTP Status Code Branching](./api-node-http-status-code-branching.md)
- [API Timeout Default to 10 Secs](./api-timeout-default-to-10-secs.md)
- [API Integration Best Practices](../integrations/api-integration-best-practices.md)
