source_url: https://console-docs.gupshup.io/docs/error-handling-timeout-recovery

<!-- kb-consulting:error-recovery-framework -->
# Error Handling: Timeout Error Recovery

**Module**: Bot Studio
**Category**: Error Recovery Framework
**Consultation Tier**: Tactical Recovery

## Definition

Recovery strategies for API timeout errors—when the API doesn't respond within the configured timeout window. Provides diagnosis of timeout causes and three escalating options from immediate adjustments to fallback patterns.

## Understanding Timeout Errors

### What Is a Timeout?

A timeout occurs when your API call doesn't receive a response within the configured timeout window (default: 10 seconds in Bot Studio).

```
Timeline:
0s    ← Request sent
5s    ← Waiting for response (no response yet)
10s   ← TIMEOUT (default limit reached)
       ← Error returned to Bot Studio
       ← Journey continues on error branch
```

### Why Timeouts Happen

Timeouts happen for one of three reasons:

| Reason | Cause | Recovery Strategy |
|--------|-------|-------------------|
| **Network Latency** | Distance/connection slowness | Increase timeout threshold (Option 1) |
| **API Under Load** | Server processing slowly | Retry with backoff (Option 2) |
| **Upstream Dependency Slow** | 3rd party API lag | Add fallback service (Option 3) |

---

## Diagnostic Process: "Why Is This Timing Out?"

### Step 1: Measure Response Time (2 minutes)

**Test the API directly** (not through Bot Studio):
```bash
# Time how long API actually takes to respond
curl -w "Total time: %{time_total}s\n" https://api.example.com/endpoint
```

**What to measure**:
- **<2 seconds**: API is fast, timeout threshold might be too low
- **2-5 seconds**: API is moderately slow, normal for some services
- **5-10 seconds**: API is slow, consider longer timeout
- **>10 seconds**: API is very slow, need either longer timeout or fallback

### Step 2: Check Response Time Consistency (2 minutes)

**Is timeout intermittent or consistent?**

```
Consistent timeout: API always slow
├─ Indicates systematic slowness
├─ Likely: API under load, far away, or slow by design
└─ Solution: Increase timeout or add fallback

Intermittent timeout: Sometimes succeeds, sometimes times out
├─ Indicates transient issues
├─ Likely: Traffic spikes, network hiccups
└─ Solution: Retry (server recovers between attempts)
```

### Step 3: Determine Root Cause (3 minutes)

Use this checklist to identify which cause applies:

**Is the API responding slowly even with direct test?**
- ✅ YES → API is slow (your timeout threshold too low, or API under load)
- ❌ NO → Problem is network or connection (on your side or in between)

**Is your location far from the API's server?**
- ✅ YES → Network latency (geographical distance)
- ❌ NO → Probably not a latency issue

**Does the API provider's status page show degradation or high load?**
- ✅ YES → API under load (upstream issue)
- ❌ NO → Probably isolated to your requests

**Based on root cause, select recovery option below:**

---

## Recovery Options

### Option 1: Increase Timeout Threshold

**Use this if**: API responds, but takes longer than current timeout.

**When this works best**:
- API is genuinely slow (5-10+ second responses)
- Timeout threshold is too aggressive for this API
- You don't mind waiting longer for responses

**How to implement**:

1. **In Bot Studio**:
   - Open API Node configuration
   - Find **Timeout** field (default: 10 seconds)
   - Increase value (max: 60 seconds)
   - Recommended: Set to (observed_response_time + 2 seconds)

2. **Example**:
   ```
   Observed response time: 8 seconds
   Current timeout: 10 seconds
   Increased timeout: 12 seconds
   ```

3. **Deploy and test**

**Pros**:
- ✅ Simple to implement (one setting change)
- ✅ No code changes needed
- ✅ Works if API is consistently slow

**Cons**:
- ❌ Delays user experience (longer wait for response)
- ❌ Doesn't help if API is unreliable
- ❌ Hitting max timeout of 60 seconds? Time to reconsider API

**Recommended limits**:
- 10-15 seconds: Most fast APIs (good)
- 15-30 seconds: Slower APIs (acceptable)
- 30-60 seconds: Very slow APIs (consider fallback)
- >60 seconds: Not supported, use fallback

---

### Option 2: Implement Retry with Backoff

**Use this if**: Timeouts are intermittent (sometimes succeeds, sometimes fails).

**When this works best**:
- API timeout is transient (traffic spike passes)
- Retry might succeed second time
- You want automatic recovery without manual intervention

**How this works**:

```
Timeline:
0s    ← Request 1 sent
10s   ← TIMEOUT (backoff delay starts)
11s   ← Wait 1 second
12s   ← Request 2 sent
22s   ← TIMEOUT (backoff delay starts)
24s   ← Wait 2 seconds
26s   ← Request 3 sent
36s   ← SUCCESS (API recovered)
```

**How to implement in Bot Studio**:

1. **Enable HTTP Status Code Branching**:
   - Open API Node
   - Toggle ON "HTTP Status Code" switch
   - Add connector for timeout (if available)

2. **Add Retry Logic**:
   - If timeout occurs, add delay node
   - Connect back to API node
   - Limit retries to 2-3 attempts

3. **Example flow**:
   ```
   API Node (timeout)
   └─ Timeout connector
      └─ Delay 1-2 seconds
         └─ Retry API Node
            ├─ Success → Continue
            └─ Timeout → Delay 2-4 seconds → Retry API Node
               ├─ Success → Continue
               └─ Timeout → Fallback response
   ```

**Pros**:
- ✅ Automatic recovery from transient failures
- ✅ Doesn't require changing timeout threshold
- ✅ Works for intermittent issues

**Cons**:
- ❌ More complex journey logic
- ❌ Increases overall response time (due to retries)
- ❌ Doesn't help if API is consistently slow

**Backoff strategy**:
```
Attempt 1: Fail immediately (0s)
Wait:      1 second
Attempt 2: If timeout → Wait 2 seconds
Attempt 3: If timeout → Wait 4 seconds
After 3 attempts: Give up, return error
```

**Max retries recommended**: 2-3 attempts (total time: 7-10 seconds)

---

### Option 3: Add Fallback Service

**Use this if**: Primary API is frequently timing out and you need high reliability.

**When this works best**:
- Primary API is unreliable or frequently slow
- You have a backup API or local cache
- Availability is critical (mission-critical flow)
- Acceptable to serve slightly outdated data

**How this works**:

```
Timeline:
0s    ← Request to Primary API
10s   ← TIMEOUT (primary fails)
       ← Fall back to Secondary API
11s   ← Request to Secondary API sent
13s   ← SUCCESS from Secondary
       ← Continue with secondary response
```

**Fallback patterns**:

**Pattern A: Simple Sequential Fallback (A → B)**
```
Try Primary API
├─ Success → Return response
└─ Timeout → Try Secondary API
   ├─ Success → Return response
   └─ Timeout → Return error
```

**Pattern B: Multiple Endpoints (A → B → C)**
```
Try Primary API
├─ Success → Return response
└─ Timeout → Try Secondary API
   ├─ Success → Return response
   └─ Timeout → Try Tertiary API
      ├─ Success → Return response
      └─ Timeout → Return error
```

**Pattern C: Circuit Breaker (Auto-switch on repeated failures)**
```
Closed (using Primary)
├─ Consecutive timeouts >5
└─ Open (switch to Secondary)
   └─ After 60 seconds
   └─ Half-Open (try Primary again)
      ├─ Success → Closed (back to Primary)
      └─ Timeout → Open (back to Secondary)
```

**How to implement in Bot Studio**:

1. **Configure Secondary API**:
   - Settings → API Management → Add new API
   - Set up secondary endpoint (same interface)

2. **Update Journey**:
   - Primary API Node
   - Add timeout connector
   - Secondary API Node on timeout path
   - Success = continue
   - Fallback timeout = error message

3. **Test failover**:
   - Test normal flow (Primary succeeds)
   - Test fallback (Primary times out, Secondary succeeds)
   - Verify responses are compatible

**Example implementation**:
```
API Node: Get User from Primary
├─ Success → Store in user_data
└─ Timeout → API Node: Get User from Cache
   ├─ Success → Store in user_data (note: cached)
   └─ Timeout → Send error message
```

**Pros**:
- ✅ High reliability (fallback reduces outages)
- ✅ Automatic failure recovery
- ✅ Works for consistently unreliable APIs

**Cons**:
- ❌ More complex setup (need secondary API)
- ❌ Data consistency risk (primary and fallback might differ)
- ❌ Higher cost (paying for two APIs)

**Fallback considerations**:
- Is secondary response format compatible?
- Is data freshness acceptable (cached vs live)?
- What's the cost of serving stale data?
- Can you monitor which API is being used?

---

## Decision Framework: "Which Option Should I Choose?"

### Quick Decision Tree

```
Is timeout intermittent or consistent?
├─ INTERMITTENT (sometimes succeeds)
│  └─ Use OPTION 2: Retry with backoff
│     └─ 60-70% chance this solves it
│
└─ CONSISTENT (always times out)
   └─ How often can you tolerate timeouts?
      ├─ Can wait longer for response
      │  └─ Use OPTION 1: Increase timeout
      │     └─ Simple, but slower for users
      │
      └─ Cannot tolerate timeouts (mission-critical)
         └─ Use OPTION 3: Fallback service
            └─ Complex, but high reliability
```

### Recommended Approach by Scenario

| Scenario | Recommended Option | Rationale |
|----------|-------------------|-----------|
| **API sometimes times out, sometimes succeeds** | Option 2 (Retry) | Intermittent issue, retry likely succeeds |
| **API always takes 15-30 seconds** | Option 1 (Increase timeout) | API is slow but reliable, just needs more time |
| **API frequently times out, can't afford to wait** | Option 3 (Fallback) | Need reliability, have backup available |
| **API is slow AND unreliable** | Option 2 + 1 (Retry + Increase) | First try retry, then increase timeout |
| **Critical flow, API is flaky** | Option 3 (Fallback) | High availability required |
| **Low-priority flow, API is slow** | Option 1 (Increase) | Simple solution, user can wait |

---

## Timeout Recovery Checklist

### For Intermittent Timeouts (Option 2):

```
✓ Step 1: Confirm timeout is intermittent (test 5+ times)
✓ Step 2: Add retry logic to API node
✓ Step 3: Implement 1-2 second delay between retries
✓ Step 4: Max retries: 2-3 attempts
✓ Step 5: Test: Verify retry succeeds on 2nd attempt
✓ Step 6: Deploy and monitor
✓ Step 7: If still failing, add Option 1 (increase timeout)
```

### For Consistently Slow API (Option 1):

```
✓ Step 1: Measure actual response time (10+ tests)
✓ Step 2: Calculate new timeout (response_time + 2-3 seconds)
✓ Step 3: Check max limit (60 seconds max in Bot Studio)
✓ Step 4: Update timeout value in API node
✓ Step 5: Test API connection
✓ Step 6: Deploy changes
✓ Step 7: Monitor if acceptable for user experience
✓ Step 8: If too slow, escalate to Option 3 (fallback)
```

### For Unreliable API (Option 3):

```
✓ Step 1: Identify fallback API (same response format)
✓ Step 2: Configure fallback in API Management
✓ Step 3: Test fallback API works independently
✓ Step 4: Update journey flow (primary → fallback)
✓ Step 5: Test primary + fallback paths
✓ Step 6: Verify response format compatibility
✓ Step 7: Deploy with monitoring
✓ Step 8: Track which API is being used (monitoring)
✓ Step 9: Plan to switch back to primary once stable
```

---

## Monitoring & Follow-Up

### Key Questions After Implementation

**After increasing timeout (Option 1):**
- ✓ Are users seeing acceptable response times?
- ✓ Are timeouts now rare?
- ✓ Is 60-second limit sufficient?

**After adding retry (Option 2):**
- ✓ Do retries succeed on 2nd/3rd attempt?
- ✓ What % of requests need retries?
- ✓ Are total response times acceptable?

**After adding fallback (Option 3):**
- ✓ What % of requests use primary vs fallback?
- ✓ Are fallback responses acceptable quality?
- ✓ Can you monitor which API is used?
- ✓ When can you migrate back to primary?

---

## Consulting Notes

**For Consulting Tone:**
- "Let's start by understanding if this timeout is consistent or intermittent."
- "Based on the response time you're seeing, I recommend [OPTION]."
- "This type of timeout typically indicates [CAUSE]. Here's what that means..."
- "The recovery strategy depends on how reliable this API needs to be."
- "If this API continues timing out, we may need to reconsider using it."

**When to Escalate:**
- Consistent timeouts >60 seconds (API fundamentally slow)
- Timeouts only at certain times of day (capacity planning needed)
- No fallback available and mission-critical flow (architecture decision)
- Rate limit hit during retry attempts (need higher tier)

**When to Consider Alternatives:**
- API timeouts >30 seconds consistently (quality of API questionable)
- Fallback needed but no secondary API available (design issue)
- Timeout delays affecting user experience (may need different API)

---

## See Also

- [Error Recovery: Diagnosing Error Patterns](./error-handling-diagnosing-error-patterns.md)
- [Error Recovery: HTTP Errors (4xx/5xx)](./error-handling-http-errors.md)
- [Error Recovery: Smart Retry Implementation](./error-handling-smart-retry.md)
- [Error Recovery: Fallback Services & Circuit Breaker](./error-handling-fallback-patterns.md)
- [Error Recovery: Production Checklist](./error-handling-production-checklist.md)
- [API Timeout Default to 10 Secs](./api-timeout-default-to-10-secs.md)
- [API Node: HTTP Status Code Branching](./api-node-http-status-code-branching.md)
