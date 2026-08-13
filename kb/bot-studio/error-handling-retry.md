# Smart Retry Implementation — Backoff Algorithms

## Diagnosis: Should You Retry This Error?

**Retryable:** 5xx, timeouts, 429 rate limits  
**Non-retryable:** 4xx errors (fix first)

## Context: Retry Strategies

### Linear Retry
Fixed delay (e.g., 1s between attempts)

### Exponential Backoff
Delay grows: 1s → 2s → 4s → 8s

### Jittered Backoff
Random delays to avoid thundering herd

**Exponential with jitter is production standard.**

## Options: Implementation Approaches

### Option 1: Simple Retry
3 attempts, fixed 1s delay. Simplest, least optimal.

### Option 2: Exponential Backoff
3-5 attempts, exponential delay. Balances retry and latency.

### Option 3: Exponential + Jitter
3-5 attempts, exponential delay + randomization. Best for distributed systems.

### Option 4: Adaptive Retry
Monitor success rate, adjust max_attempts dynamically.

## Recommended Approach

**Use Option 2 (Exponential Backoff):**
- Max 3-5 attempts
- Initial delay: 1s
- Multiplier: 2x per retry
- Max delay: 30s

## Code Pattern

```
attempt = 0
delay = 1
while attempt < 5:
  try:
    response = api_call()
    return response
  except RetryableError:
    attempt += 1
    if attempt >= 5: raise
    sleep(delay)
    delay = min(delay * 2, 30)
```
