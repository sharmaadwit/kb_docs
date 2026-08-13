# Fallback Services & Circuit Breaker Patterns

## Diagnosis: When Do You Need a Fallback?

Fallback needed if:
- Primary API fails >5% of requests
- Primary API timeout rate >2%
- Business impact of failure is high (payments, support, orders)

## Context: Fallback Patterns

### Pattern 1: A→B Sequential
Try primary, if fails try secondary.

### Pattern 2: A→B→C Multiple
Chain fallbacks (e.g., 3 redundant endpoints).

### Pattern 3: Circuit Breaker
Auto-switch to fallback when error rate exceeds threshold.

### Pattern 4: Load Balancing
Distribute across multiple endpoints.

## Options: Implementation Patterns

### Option 1: Simple Sequential Fallback
Pros: Simple implementation  
Cons: Doubles latency if primary fails

### Option 2: Multiple Fallbacks
Pros: High availability  
Cons: Complex management

### Option 3: Circuit Breaker
Pros: Auto-switches, monitors health  
Cons: Requires state management

### Option 4: Load Balancing
Pros: Distribute load, fail gracefully  
Cons: Requires health checks

## Recommended Approach

**Start Option 1 (simple). Upgrade to Option 3 (circuit breaker) if >5% failure rate.**

Circuit breaker prevents cascading failures and reduces wasted retries.

## Monitoring

Track which fallback is active. Emit alerts when primary unreliable.
