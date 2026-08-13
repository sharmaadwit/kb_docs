source_url: https://console-docs.gupshup.io/docs/error-handling-smart-retry

<!-- kb-consulting:error-recovery-framework -->
# Error Handling: Smart Retry Implementation

**Module**: Bot Studio
**Category**: Error Recovery Framework
**Consultation Tier**: Tactical Implementation

## Definition

Smart retry strategies for transient API failures. Covers retry classification (which errors to retry), backoff algorithms (exponential vs jittered), and production-ready retry patterns to minimize user-facing impact.

## Understanding Retries

### When to Retry

**DEFINITELY RETRY** (Retryable Errors):
- **5xx server errors** (500, 502, 503, 504) — Server problem, might recover
- **Timeouts** — Connection issue, might be transient
- **429 rate limit** — Respect Retry-After header, retry when ready

**DON'T RETRY** (Non-Retryable Errors):
- **4xx client errors** (except 429) — Your request is wrong, retrying won't help
  - 400 Bad Request → Fix request first
  - 401 Unauthorized → Refresh credentials first
  - 403 Forbidden → Fix permissions first
  - 404 Not Found → Fix URL/resource ID first

**MAYBE RETRY** (Context-Dependent):
- **409 Conflict** — Check if duplicate exists, then decide
- **422 Unprocessable Entity** — Check business rules, then decide

### Retry Classification Table

| Error | Retryable? | Reason | What to Do First |
|-------|-----------|--------|------------------|
| 5xx (500, 502, 503, 504) | ✅ YES | Server might recover | Wait + retry |
| Timeout | ✅ YES | Transient network/load | Wait + retry |
| 429 Rate Limit | ✅ YES | Respect Retry-After | Wait + retry |
| 4xx (400, 401, 403, 404) | ❌ NO | Your fault, not transient | Fix request, then retry |
| 409 Conflict | ⚠️ MAYBE | Depends on use case | Check for duplicate first |
| 422 Unprocessable | ⚠️ MAYBE | Depends on error | Check business rules first |

---

## Backoff Strategies

### What Is Backoff?

Backoff is the delay between retry attempts. Proper backoff is critical because:
1. **Gives server time to recover** (if it's overloaded)
2. **Avoids hammering the API** (multiple retries make overload worse)
3. **Reduces cascade failures** (if many clients retry at once)

### Backoff Algorithm Comparison

#### No Backoff (❌ Don't Do This)

```
Attempt 1: Fail (0s)
Attempt 2: Retry immediately (0.1s later)
Attempt 3: Retry immediately (0.2s later)
Problem: Hammers API, makes overload worse
Result: All retries fail
```

---

#### Linear Backoff (⚠️ Basic)

```
Attempt 1: Fail (0s)
Wait:      5 seconds (fixed)
Attempt 2: Fail (5s)
Wait:      5 seconds (fixed)
Attempt 3: Retry (10s)
Total time: 10 seconds

Pros: Simple to implement
Cons: Doesn't adapt to load, predictable (all clients retry together)
```

---

#### Exponential Backoff (✅ Recommended)

```
Attempt 1: Fail (0s)
Wait:      1 second (2^0)
Attempt 2: Fail (1s)
Wait:      2 seconds (2^1)
Attempt 3: Fail (3s)
Wait:      4 seconds (2^2)
Attempt 4: Succeed (7s)
Total time: 7 seconds

Formula: wait_time = min(max_delay, 2^attempt)

Pros: 
- Adapts to server load
- Recovers faster if server recovers quickly
- Standard across all major APIs

Cons: Predictable (all clients retry together)
```

---

#### Exponential Backoff with Jitter (✅✅ Best Practice)

```
Attempt 1: Fail (0s)
Wait:      1 second + random(0-1s) = 1.3s
Attempt 2: Fail (1.3s)
Wait:      2 seconds + random(0-2s) = 3.2s
Attempt 3: Fail (4.5s)
Wait:      4 seconds + random(0-4s) = 5.1s
Attempt 4: Succeed (9.6s)
Total time: 9.6 seconds

Formula: wait_time = min(max_delay, 2^attempt + random(0, 2^attempt))

Pros:
- Adapts to server load
- Randomization prevents "thundering herd"
  (all clients retrying at same second)
- Best recovery for overloaded APIs

Cons: Slightly longer wait time (but better overall)
```

---

### Choosing Your Backoff Strategy

| Strategy | Use Case | When |
|----------|----------|------|
| **Linear Backoff** | Simple, non-critical | Low-traffic bots, development |
| **Exponential Backoff** | Most cases | Production bots, moderate traffic |
| **Exponential + Jitter** | High-traffic, mission-critical | Enterprise bots, high concurrency |

**Recommendation for Bot Studio**: **Exponential backoff with jitter** (handles everything)

---

## Implementing Smart Retry in Bot Studio

### Simple Retry (Manual Flow)

**Scenario**: API sometimes times out, but retrying works.

**Implementation**:

```
[API Node: Get Order]
    ├─ Success (200)
    │  └─ [Continue Process]
    │
    └─ Timeout
       └─ [Delay 2 sec]
          └─ [API Node: Get Order - Retry 1]
             ├─ Success (200)
             │  └─ [Continue Process]
             │
             └─ Timeout
                └─ [Delay 4 sec]
                   └─ [API Node: Get Order - Retry 2]
                      ├─ Success (200)
                      │  └─ [Continue Process]
                      │
                      └─ Timeout
                         └─ [Error: API Failed]
```

**Steps to implement**:

1. **Add first API Node** (primary attempt)
2. **Add timeout connector** (enable HTTP Status Code branching)
3. **Add Delay Node** (2 seconds)
4. **Add second API Node** (retry 1, same API configuration)
5. **Add timeout connector** (from retry 1)
6. **Add Delay Node** (4 seconds)
7. **Add third API Node** (retry 2, same API configuration)
8. **Add error path** (if retry 2 also times out)

**Test**: Manually trigger API timeout, verify retries succeed

---

### Advanced Retry (Using Condition Nodes)

**Scenario**: Need to retry based on error type (5xx retry, 4xx don't retry).

**Implementation**:

```
[API Node: Call External API]
    ├─ Status 200 (success)
    │  └─ [Process Response]
    │
    ├─ Status 4xx (client error)
    │  └─ [Condition: Is Status 429?]
    │     ├─ YES → [Delay 30s] → [Retry]
    │     └─ NO → [Error: Fix Request]
    │
    └─ Status 5xx (server error)
       └─ [Condition: Retry Count < 3?]
          ├─ YES → [Delay 2^retryCount] → [Retry]
          └─ NO → [Error: API Unavailable]
```

**Key elements**:
- Status code branching (200 vs 4xx vs 5xx)
- Condition node to check retry count
- Exponential backoff (store `retryCount` variable)
- Max retries limit (usually 3)

---

### Using Variables for Retry Tracking

**Track retry attempts**:

```
Variable: retry_count (starts at 0)

[API Node: Call API]
├─ Success → return response
└─ Failure → 
   ├─ Set variable: retry_count = retry_count + 1
   ├─ Condition: retry_count < 3?
   │  ├─ YES → Delay (exponential) → Retry
   │  └─ NO → Error path
```

**Exponential backoff calculation**:
```
If retry_count = 1: delay = 1 second
If retry_count = 2: delay = 2 seconds
If retry_count = 3: delay = 4 seconds
```

**Example variable mapping**:
```
retry_delay = 2^(retry_count-1)
```

---

## Smart Retry Patterns

### Pattern 1: Simple 3-Attempt Retry (Most Common)

```
Attempt 1: Fail
Wait 1s
Attempt 2: Fail
Wait 2s
Attempt 3: Fail
Give up (total time: 3 seconds)

Success rate: ~90% for transient errors
Max wait time: 3 seconds
Complexity: Low
```

**When to use**: Most production cases

---

### Pattern 2: Aggressive Retry (For Critical Flows)

```
Attempt 1: Fail
Wait 1s
Attempt 2: Fail
Wait 2s
Attempt 3: Fail
Wait 4s
Attempt 4: Fail
Wait 8s
Give up (total time: 15 seconds)

Success rate: ~98% for transient errors
Max wait time: 15 seconds
Complexity: Medium
```

**When to use**: Mission-critical, must succeed

---

### Pattern 3: Rate Limit Retry (For 429 Errors)

```
API returns: 429 Too Many Requests
Check: Retry-After header (e.g., 60 seconds)
Wait: Exactly 60 seconds (MUST respect header)
Retry: Once
Result: Should succeed

Success rate: ~99% for rate limits
Max wait time: 60+ seconds
Complexity: Medium
```

**Implementation**:
```
[API Node: Send Message]
├─ Status 200 → Success
└─ Status 429 → 
   ├─ Extract Retry-After header
   ├─ Delay (Retry-After value) seconds
   └─ [Retry API Node]
      ├─ Status 200 → Success
      └─ Status 429 → Error (give up)
```

---

## Retry Best Practices

### ✅ DO

```
✓ Retry 5xx errors (server fault)
✓ Retry timeouts (transient network)
✓ Respect Retry-After header (honor API's backoff)
✓ Use exponential backoff (don't hammer server)
✓ Add jitter (prevent thundering herd)
✓ Max 3-5 retries (don't retry forever)
✓ Log all retries (for debugging)
✓ Track retry success rate (monitoring)
```

---

### ❌ DON'T

```
❌ Retry 4xx errors (your request is wrong)
❌ Retry immediately (wait between attempts)
❌ Use linear backoff (inefficient)
❌ Retry indefinitely (might lock up)
❌ Retry without condition (retry everything)
❌ Ignore Retry-After header (disrespect API)
❌ Retry silently (log for debugging)
❌ Assume retry succeeded (verify response)
```

---

## Retry Configuration Checklist

### For Timeout Retries:

```
✓ Timeout threshold set (10-30 seconds)
✓ Retry count: 2-3 attempts
✓ Backoff: Exponential (1s, 2s, 4s)
✓ Max total time: <15 seconds
✓ Test: Simulate timeout, verify retry succeeds
✓ Monitor: Track retry success rate
```

### For 5xx Server Error Retries:

```
✓ Status code routing: 5xx → retry path
✓ Backoff: Exponential (1s, 2s, 4s)
✓ Max retries: 3-5 attempts
✓ Check API status page before giving up
✓ Log error for human investigation
✓ Monitor: Track error rate over time
```

### For 429 Rate Limit Retries:

```
✓ Status code routing: 429 → retry path
✓ Extract Retry-After header
✓ Wait EXACTLY the header value
✓ Retry once (don't retry if still 429)
✓ Consider reducing request frequency
✓ Monitor: Track rate limit hits
✓ If frequent: Request higher rate limit
```

---

## Common Retry Mistakes

### Mistake 1: Retrying 4xx Errors

```
❌ Wrong:
[API returns 400 Bad Request]
→ Wait and retry
→ Still 400 (request still bad)
→ Wasted time

✅ Right:
[API returns 400 Bad Request]
→ Fix request
→ Retry
→ Succeeds (request now correct)
```

---

### Mistake 2: No Backoff (Hammering API)

```
❌ Wrong:
Attempt 1: Fail (API overloaded)
Attempt 2: Fail immediately (0.1s later, makes overload worse)
Attempt 3: Fail immediately (0.2s later, even worse)

✅ Right:
Attempt 1: Fail (API overloaded)
Attempt 2: Wait 1s (API recovers)
Attempt 3: Succeed
```

---

### Mistake 3: Ignoring Retry-After Header

```
❌ Wrong:
API returns: 429
Retry-After: 60
→ Retry after 5 seconds (ignoring header)
→ Still rate limited
→ Keep failing

✅ Right:
API returns: 429
Retry-After: 60
→ Wait exactly 60 seconds
→ Retry
→ Succeeds
```

---

### Mistake 4: Infinite Retries

```
❌ Wrong:
while API fails:
    wait
    retry
→ Might loop forever
→ Locks up journey

✅ Right:
for attempt in 1..3:
    if API succeeds: break
    wait exponential
if still fails: error
→ Guaranteed to finish
→ Clean error handling
```

---

## Production Retry Configuration

### Low-Traffic Bot (1-10 requests/sec)

```
Retry strategy: Simple exponential backoff
Retries: 2-3 attempts
Backoff: 1s, 2s, 4s
Jitter: Optional (traffic low)
Total time: ~7 seconds
```

### Medium-Traffic Bot (10-100 requests/sec)

```
Retry strategy: Exponential backoff + jitter
Retries: 3 attempts
Backoff: 1s, 2s, 4s (+ random)
Jitter: Required (prevent thundering herd)
Total time: ~7 seconds (varies with jitter)
```

### High-Traffic Bot (100+ requests/sec)

```
Retry strategy: Exponential backoff + jitter
Retries: 3-4 attempts
Backoff: 1s, 2s, 4s, 8s (+ random)
Jitter: Required (prevent thundering herd)
Total time: ~15 seconds
Consider: Circuit breaker (if failures persistent)
```

---

## Monitoring Retries

### Metrics to Track

```
✓ Retry rate: % of requests requiring retry
✓ Retry success: % of retries that succeed
✓ Attempt distribution: 1st, 2nd, 3rd attempt success %
✓ Total latency: Average time from request to final response
✓ Max latency: Longest request time (P95, P99)
✓ Backoff effectiveness: Is exponential backoff helping?
```

### Alert Thresholds

```
🔴 RED (Critical):
   Retry success <50% (retry strategy not working)
   
🟡 YELLOW (Warning):
   Retry rate >20% (API quality issue)
   Total latency >10s (user experience impact)
   
🟢 GREEN (Normal):
   Retry rate <5% (transient issues only)
   Retry success >90% (strategy working)
```

---

## Consulting Notes

**For Consulting Tone:**
- "Should we retry this error? Let's check if it's retryable..."
- "This is a transient error (5xx), so retry with backoff should help."
- "The retry strategy should use exponential backoff to give the server time to recover."
- "I recommend 2-3 retries with 1-2-4 second delays."
- "If retries still fail frequently, we may need to escalate or find alternative API."

**When to Escalate:**
- Retry success rate <50% (strategy isn't working)
- Retry rate >20% consistently (API quality issue)
- Max timeout reached (API too slow, need fallback)
- Rate limit errors even with Retry-After respected (need higher tier)

---

## See Also

- [Error Recovery: Diagnosing Error Patterns](./error-handling-diagnosing-error-patterns.md)
- [Error Recovery: HTTP Errors (4xx/5xx)](./error-handling-http-errors.md)
- [Error Recovery: Timeout Errors](./error-handling-timeout-recovery.md)
- [Error Recovery: Fallback Services & Circuit Breaker](./error-handling-fallback-patterns.md)
- [Error Recovery: Production Checklist](./error-handling-production-checklist.md)
- [API Rate Limits & Quotas](../apis/api-rate-limits-and-quotas.md)
- [API Integration Best Practices](../integrations/api-integration-best-practices.md)
