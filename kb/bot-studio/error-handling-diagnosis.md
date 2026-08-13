# Diagnosing Error Patterns — Error Classification Framework

## Diagnosis: What Type of Error Are You Seeing?

Four error categories:
1. **HTTP errors** (4xx client fault, 5xx server fault)
2. **Timeout errors** (API not responding within limit)
3. **Data validation errors** (response format mismatch)
4. **Authentication errors** (invalid token/credentials)

## Context: Where Errors Happen

**Request execution** (network, timeout) → **Response receipt** (HTTP status) → **Response parsing** (schema validation)

Errors can occur at any stage. Early detection matters for recovery strategy.

## Options: Classify & Route

### HTTP Errors (4xx/5xx)
- **4xx (400-499):** Client fault — Fix request before retry
- **5xx (500-599):** Server fault — Retry with backoff

### Timeout Errors
- Network latency
- API under load
- External service slow

### Validation Errors
- Response schema mismatch
- Unexpected data type
- Missing required fields

### Authentication Errors
- Token expired (401)
- Insufficient permissions (403)
- Invalid credentials

## Recommended Approach

**Classify error type first, then apply recovery strategy:**
- 4xx → Fix request, don't retry blindly
- 5xx → Retry with exponential backoff
- Timeout → Check upstream SLA, consider fallback
- Validation → Update schema parser or escalate

## Follow-Up Questions

- What HTTP status code are you getting?
- How often do timeouts occur?
- Does the error happen at request or response parsing?
