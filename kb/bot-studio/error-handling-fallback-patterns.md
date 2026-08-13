source_url: https://console-docs.gupshup.io/docs/error-handling-fallback-patterns

<!-- kb-consulting:error-recovery-framework -->
# Error Handling: Fallback Services & Circuit Breaker

**Module**: Bot Studio
**Category**: Error Recovery Framework
**Consultation Tier**: Advanced Patterns

## Definition

Advanced error recovery patterns for mission-critical flows. Covers fallback routing (primary → secondary → tertiary), circuit breaker patterns (auto-switch on repeated failures), and load balancing strategies to maximize availability.

## Understanding Fallback Patterns

### What Is a Fallback?

A fallback is an alternative action when the primary action fails. Instead of giving up on error, you try a backup option.

```
Normal case:
Request → Primary API → Success → Response

Error case (with fallback):
Request → Primary API → Failure → Secondary API → Success → Response
```

### Why Use Fallback?

**Use fallback when**:
- Primary API is unreliable or frequently fails
- You have a secondary source (backup API, cache, etc.)
- Availability is critical (mission-critical flow)
- Acceptable to serve slightly outdated data

**Don't use fallback when**:
- Primary API is reliable (>99% uptime)
- No secondary source available
- Data freshness is critical (can't serve stale data)
- Added complexity not worth benefit

---

## Fallback Pattern 1: Simple Sequential Fallback (A → B)

### How It Works

```
Timeline:
User requests data
  ↓
Try Primary API (e.g., production database)
  ├─ Success → Return fresh data
  └─ Failure (timeout/error) → Try Secondary API (e.g., cache)
     ├─ Success → Return cached data (may be stale)
     └─ Failure → Return error message
```

### When to Use

| Scenario | Recommended |
|----------|------------|
| Primary API sometimes times out, cache available | ✅ YES |
| Primary API 95% uptime, need 99% | ✅ YES |
| Primary API 99%+ uptime, no cache | ❌ NO (not needed) |
| Primary API always fast, needs data freshness | ❌ NO (cache stale) |

### Implementation in Bot Studio

**Configuration**:

```
[API Node: Primary - Get User Data]
├─ Success (200)
│  └─ [Store in: user_data]
│     └─ [Show user info]
│
├─ Timeout
│  └─ [API Node: Secondary - Get User from Cache]
│     ├─ Success (200)
│     │  └─ [Store in: user_data]
│     │     └─ [Show user info (cached)]
│     │
│     └─ Timeout/Error
│        └─ [Send: "Data unavailable, try again later"]
│
└─ Other errors (5xx)
   └─ [API Node: Secondary - Get User from Cache]
      (same as timeout branch)
```

**Steps to implement**:

1. **Add Primary API Node**
   - Endpoint: production.api.example.com/user/{user_id}
   - Timeout: 10 seconds

2. **Add HTTP Status Code Branching**
   - Success (200) → Continue path
   - Timeout/Error → Secondary

3. **Add Secondary API Node** (fallback)
   - Endpoint: cache.api.example.com/user/{user_id}
   - Timeout: 5 seconds (cache should be faster)

4. **Test both paths**:
   - Primary succeeds → Returns fresh data
   - Primary fails → Falls back to secondary (cached)

**Pros**:
- ✅ Simple to implement
- ✅ Clear success/fallback paths
- ✅ Easy to test and debug
- ✅ Minimal latency if primary succeeds

**Cons**:
- ❌ Static (always tries primary first)
- ❌ No automatic switching (even if primary fails repeatedly)
- ❌ Doesn't monitor primary API health

---

## Fallback Pattern 2: Multiple Fallbacks (A → B → C)

### How It Works

```
User requests data
  ↓
Try Primary (Production DB)
  ├─ Success → Return fresh data
  └─ Failure → Try Secondary (Replica DB)
     ├─ Success → Return replica data (slightly stale)
     └─ Failure → Try Tertiary (Cache)
        ├─ Success → Return cached data (very stale)
        └─ Failure → Return error message
```

### When to Use

| Scenario | Recommended |
|----------|------------|
| Need highest availability (4 nines) | ✅ YES |
| Multiple data sources available | ✅ YES |
| Can tolerate stale data | ✅ YES |
| Low-cost flow (doesn't matter if stale) | ✅ YES |
| Real-time data critical, no fallback | ❌ NO |

### Implementation in Bot Studio

**Configuration**:

```
[API Node: Primary - Live Database]
├─ Success → [Return live data]
└─ Failure → 
   [API Node: Secondary - Replica Database]
   ├─ Success → [Return replica data]
   └─ Failure →
      [API Node: Tertiary - Cache]
      ├─ Success → [Return cached data]
      └─ Failure → [Error: All sources failed]
```

**Escalation path**:
- Level 1: Fresh data (primary)
- Level 2: 5-min old data (replica)
- Level 3: 1-hour old data (cache)
- Level 4: Error

**Pros**:
- ✅ Maximum availability (multiple fallbacks)
- ✅ Graceful degradation (serves best available data)
- ✅ Handles cascading failures

**Cons**:
- ❌ Complex journey logic
- ❌ Multiple API configurations needed
- ❌ Data freshness vs availability trade-off
- ❌ Harder to debug (many paths)

---

## Fallback Pattern 3: Circuit Breaker (Smart Switching)

### How It Works

Circuit breaker automatically switches between primary and fallback based on health monitoring.

```
States:
CLOSED (healthy)
  ├─ Using Primary API
  ├─ Monitor error rate
  └─ If errors >threshold → Open
  
OPEN (unhealthy)
  ├─ Using Fallback API
  ├─ Stop trying Primary
  └─ After cooldown → Half-Open
  
HALF-OPEN (testing)
  ├─ Try Primary again
  ├─ If succeeds → Closed (back to primary)
  └─ If fails → Open (back to fallback)
```

### Timeline Example

```
Time    State      API Being Used    Comment
---     -----      ----------------  -------
0s      CLOSED     Primary           All requests to primary
10s     CLOSED     Primary           Primary succeeds
20s     CLOSED     Primary           Primary fails (1/100)
30s     CLOSED     Primary           Primary fails (2/100)
...     CLOSED     Primary           More failures accumulating
90s     CLOSED     Primary           Error rate >5%
100s    OPEN       Fallback          Switch to fallback
110s    OPEN       Fallback          Fallback handling all traffic
200s    HALF-OPEN  Primary           Try primary again
205s    HALF-OPEN  Primary           Primary succeeds
210s    CLOSED     Primary           Back to primary (healthy)
```

### Configuration Parameters

| Parameter | Recommended | Purpose |
|-----------|-------------|---------|
| **Failure Threshold** | 5 failures in 30s | When to open circuit |
| **Failure Rate** | >5% | Error rate trigger |
| **Cooldown Period** | 60 seconds | Wait before half-open |
| **Half-Open Window** | 3 test requests | How many to test |
| **Reset Timeout** | 300 seconds | If half-open healthy |

### Implementation in Bot Studio (Conceptual)

**Manual circuit breaker** (using variables):

```
Variable: circuit_state = "CLOSED"
Variable: failure_count = 0
Variable: last_failure_time = 0

[API Node: Get Data]
├─ Condition: circuit_state == "CLOSED"?
│  ├─ YES → [Try Primary API]
│  │  ├─ Success →
│  │  │  └─ [Set: failure_count = 0]
│  │  │     └─ [Return data]
│  │  │
│  │  └─ Failure →
│  │     ├─ [Set: failure_count += 1]
│  │     ├─ Condition: failure_count > 5?
│  │     │  ├─ YES → [Set: circuit_state = "OPEN"]
│  │     │  │        [Go to Secondary]
│  │     │  └─ NO → [Try again (retry)]
│  │
│  └─ NO (circuit_state == "OPEN")
│     └─ [Check if cooldown expired]
│        ├─ YES → [Set: circuit_state = "HALF-OPEN"]
│        │        [Try Primary test]
│        └─ NO → [Use Secondary/Fallback]
```

**Pros**:
- ✅ Automatic failure detection
- ✅ Stops hammering broken API
- ✅ Automatic recovery (half-open)
- ✅ Reduces latency (no timeouts)
- ✅ Production-grade reliability

**Cons**:
- ❌ Complex implementation (requires variable tracking)
- ❌ Hard to test all states
- ❌ Requires careful tuning
- ❌ May need external monitoring service

**Note**: Bot Studio doesn't natively support circuit breaker. Consider using:
- Custom middleware/proxy (implement circuit breaker logic)
- External service (Kong, Ambassador, Apigee)
- Bot Studio Variables + Conditions (manual implementation)

---

## Fallback Pattern 4: Load Balancing (Round-Robin)

### How It Works

Distribute requests across multiple endpoints instead of prioritizing one.

```
Request 1 → API Endpoint A → Returns data
Request 2 → API Endpoint B → Returns data
Request 3 → API Endpoint A → Returns data
Request 4 → API Endpoint B → Returns data
...
```

### When to Use

| Scenario | Recommended |
|----------|------------|
| Multiple APIs with same capacity | ✅ YES |
| Need load distribution | ✅ YES |
| Avoid overloading single API | ✅ YES |
| Endpoints have equal latency | ✅ YES |
| One endpoint faster than other | ❌ NO (use weighted) |

### Implementation in Bot Studio

**Round-robin using variable counter**:

```
Variable: endpoint_index = 0

[Condition: endpoint_index % 2 == 0?]
├─ YES (even) → [API Node: Endpoint A]
└─ NO (odd) → [API Node: Endpoint B]

[Set: endpoint_index = endpoint_index + 1]
[Return response]
```

**Pros**:
- ✅ Distributes load evenly
- ✅ Prevents single API overload
- ✅ Simple to implement

**Cons**:
- ❌ Doesn't handle API failures
- ❌ Assumes equal capacity
- ❌ No health checks

---

## Comparing Fallback Patterns

| Pattern | Availability | Complexity | Use Case |
|---------|--------------|-----------|----------|
| **Simple A→B** | ~95-97% | Low | Most cases |
| **Multiple A→B→C** | ~99%+ | Medium | Critical flows |
| **Circuit Breaker** | ~99%+ | High | Production, auto-recovery |
| **Load Balancing** | ~95%+ | Low | Distribute load |

---

## Decision Framework: "Which Fallback Pattern?"

### Quick Decision Tree

```
Is primary API unreliable?
├─ NO (>99% uptime) → Don't use fallback
│
└─ YES (sometimes fails)
   └─ Do you have a fallback source?
      ├─ NO → Add retry + increase timeout
      │      └─ (See: Smart Retry)
      │
      └─ YES (cache, replica, secondary API)
         └─ How critical is this flow?
            ├─ NOT CRITICAL → Use Pattern 1 (Simple A→B)
            │
            ├─ CRITICAL (95% uptime needed) → Use Pattern 1 or 2
            │
            └─ MISSION-CRITICAL (99%+ needed) → Use Pattern 2 or 3
               └─ Do you have dev resources? 
                  ├─ YES → Pattern 3 (Circuit Breaker)
                  └─ NO → Pattern 2 (A→B→C Fallback)
```

---

## Fallback Implementation Checklist

### For Simple Fallback (Pattern 1):

```
✓ Step 1: Configure Primary API Node
✓ Step 2: Enable HTTP Status Code Branching
✓ Step 3: Add failure connector (timeout/5xx)
✓ Step 4: Configure Secondary API Node
✓ Step 5: Test primary → success path
✓ Step 6: Test primary → fallback → success path
✓ Step 7: Verify response format compatibility
✓ Step 8: Document which fallback is used
✓ Step 9: Deploy and monitor
✓ Step 10: Track fallback usage rate
```

### For Multiple Fallbacks (Pattern 2):

```
✓ Step 1: Configure Primary API Node
✓ Step 2: Configure Secondary API Node (fallback)
✓ Step 3: Configure Tertiary API Node (fallback)
✓ Step 4: Chain failure paths (A→B→C)
✓ Step 5: Test all three paths independently
✓ Step 6: Test failure cascades (A fails, B succeeds)
✓ Step 7: Test all fail scenario (A, B, C all fail)
✓ Step 8: Verify data freshness is acceptable
✓ Step 9: Deploy with monitoring
✓ Step 10: Alert on fallback usage
```

### For Circuit Breaker (Pattern 3):

```
✓ Step 1: Define failure threshold (e.g., 5 failures)
✓ Step 2: Define error rate trigger (e.g., >5%)
✓ Step 3: Implement state tracking (CLOSED/OPEN/HALF-OPEN)
✓ Step 4: Implement failure counter (log_attempt_failure)
✓ Step 5: Implement health check (log_success_rate)
✓ Step 6: Test state transitions (CLOSED→OPEN→HALF-OPEN→CLOSED)
✓ Step 7: Monitor state changes
✓ Step 8: Alert on open circuit
✓ Step 9: Verify auto-recovery works
✓ Step 10: Deploy with heavy monitoring
```

---

## Monitoring Fallback Health

### Key Metrics

```
✓ Primary API Success Rate
  └─ Ideal: >99%
  └─ Warning: <95%
  └─ Critical: <90%

✓ Fallback Usage Rate
  └─ Normal: <1% of requests
  └─ Warning: 1-5%
  └─ Critical: >5%

✓ Fallback Success Rate
  └─ Ideal: >99%
  └─ Warning: <95%
  └─ (Fallback should be reliable)

✓ Data Freshness (if using cache fallback)
  └─ Normal: <5 minutes old
  └─ Warning: 5-60 minutes old
  └─ Critical: >1 hour old
```

### Alert Configuration

```
🔴 RED (Critical):
   Primary success rate <90%
   Fallback usage >10%
   All fallbacks failing
   
🟡 YELLOW (Warning):
   Primary success rate <95%
   Fallback usage >5%
   Circuit breaker OPEN for >1 hour
   
🟢 GREEN (Normal):
   Primary success rate >99%
   Fallback usage <1%
   All APIs healthy
```

---

## Recovery & Failover Procedures

### When Primary Fails

**Immediate**:
1. Fallback activated automatically
2. User continues (with fallback data)
3. Error logged for investigation

**Short-term** (within 5 minutes):
1. Check primary API status page
2. Verify if widespread outage
3. Wait for recovery

**Medium-term** (within 1 hour):
1. Contact primary API provider
2. Check logs for error pattern
3. Consider escalating to engineering

**Long-term** (recovery):
1. Primary API recovers
2. Circuit breaker enters half-open
3. Test primary with few requests
4. Gradually shift traffic back
5. Monitor for stability

---

## Best Practices

### ✅ DO

```
✓ Test fallback regularly (don't let it rot)
✓ Keep fallback data format compatible
✓ Monitor fallback usage (watch for issues)
✓ Document which fallback is active
✓ Set up alerts for fallback activation
✓ Plan for all fallbacks failing (error path)
✓ Log which API was used (for debugging)
✓ Measure fallback latency (cache slower?)
✓ Review fallback data freshness
✓ Have clear escalation procedures
```

---

### ❌ DON'T

```
❌ Use fallback if not needed (adds complexity)
❌ Forget to test fallback paths
❌ Let fallback data become stale
❌ Ignore when fallback is active
❌ Deploy fallback without monitoring
❌ Use incompatible response formats
❌ Forget error path (all fallbacks fail)
❌ Mix circuit breaker states (confusing)
❌ Assume fallback is always faster
❌ Deploy without load testing
```

---

## Real-World Examples

### Example 1: E-commerce Order Lookup

```
Primary: Production Database (live orders)
Fallback: Cache (orders from last hour)

Timeline:
- User asks for order status
- Primary DB times out (server restart)
- Fallback cache returns: "Order shipped"
- User sees result (1-hour stale but better than error)
- Primary recovers
- Next request uses primary (up-to-date)
```

### Example 2: User Profile with 3-Level Fallback

```
Level 1: User Service (primary, authoritative)
Level 2: Cache Service (5-min stale)
Level 3: Read Replica DB (30-min stale)

Scenario: User Service down for maintenance
- L1 Primary fails → Try L2 Cache
- L2 Cache succeeds → Return profile
- User continues without disruption
- Primary recovers
- Next request uses primary
```

### Example 3: Critical Report with Circuit Breaker

```
Primary: External Analytics API
Fallback: Local Cache

Monitoring:
- Track error rate of primary
- If >5% errors in 30 seconds → Open circuit
- Switch all traffic to cache
- After 60 seconds → Try primary (half-open)
- If primary healthy → Close circuit
- Resume primary traffic
```

---

## Consulting Notes

**For Consulting Tone:**
- "Given the reliability requirements, I recommend a fallback pattern."
- "For this critical flow, let's add a secondary source."
- "The circuit breaker pattern would automatically handle failures."
- "We should test the fallback regularly to ensure it works."
- "Let's monitor which API is being used to understand reliability."

**When to Escalate:**
- Primary consistently failing (>1 hour): Need to address root cause
- Fallback also failing: Need additional fallback or redesign
- Data freshness issues: Need to refresh cache more frequently
- Performance issues: Fallback adding too much latency

---

## See Also

- [Error Recovery: Diagnosing Error Patterns](./error-handling-diagnosing-error-patterns.md)
- [Error Recovery: HTTP Errors (4xx/5xx)](./error-handling-http-errors.md)
- [Error Recovery: Timeout Errors](./error-handling-timeout-recovery.md)
- [Error Recovery: Smart Retry Implementation](./error-handling-smart-retry.md)
- [Error Recovery: Production Checklist](./error-handling-production-checklist.md)
- [API Node: HTTP Status Code Branching](./api-node-http-status-code-branching.md)
