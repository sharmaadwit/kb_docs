# Production Error Handling Checklist

Use this before deploying API nodes to production.

## Request Level
- [ ] Timeout set (default 30s, adjust per API)
- [ ] Retry logic implemented (exponential backoff)
- [ ] Request validation before sending
- [ ] Headers validated (auth, content-type)

## Response Level
- [ ] Status code check (route 200 vs 4xx vs 5xx)
- [ ] Response parsing validation (check schema)
- [ ] Error message logging (for debugging)
- [ ] Response size limits (prevent memory issues)

## Fallback Level
- [ ] Fallback endpoint configured (if critical)
- [ ] Circuit breaker monitoring (if multiple retries)
- [ ] Escalation path to human (if all retry/fallback fails)
- [ ] Graceful degradation (user message if API unavailable)

## Observability
- [ ] Log all errors to dashboard (Langfuse, monitoring)
- [ ] Alert on repeated failures (error rate >5%)
- [ ] Track which recovery path was used
- [ ] Monitor latency distribution (P50, P95, P99)

## Testing
- [ ] Tested with API failing 100% of requests
- [ ] Tested with API timeout on every request
- [ ] Tested with malformed response (invalid JSON)
- [ ] Tested with slow API (10+ second responses)

✅ All items checked? Ready for production.
