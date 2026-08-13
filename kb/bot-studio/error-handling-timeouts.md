# Timeout Error Recovery — When APIs Don't Respond

## Diagnosis: API Isn't Responding

Causes:
- Network latency (geographical distance)
- API under load (slow server)
- External service dependency slow (3rd party lag)

## Context: Timeout vs Slow

**Timeout:** Request exceeds time limit (e.g., 30s)  
**Slow:** Request completes but takes 10-30s

Slow APIs need strategy adjustment. Timeouts need recovery.

## Options: Three Strategies

### Option 1: Increase Timeout Threshold
If API is actually slow (9+ seconds typical), increase timeout to 15-30s.

### Option 2: Implement Retry with Backoff
For transient timeouts (50% of requests succeed), retry 3-5 times.

### Option 3: Add Fallback Service
If timeouts are persistent, use redundant endpoint or cached response.

## Recommended Approach

**Start with Option 2 (retry).** If retry success <30%, escalate to Option 3 (fallback).

## Monitoring

Track timeout rate weekly. Alert if >5% of requests timeout.
