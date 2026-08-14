# Channels & Integration: Error Codes by Platform

## Diagnosis: Message Failed, What Went Wrong?

Your SMS didn't deliver. WhatsApp was silently dropped. RCS fell back to SMS. Now you need to know: Is this a temporary network hiccup you should retry? A permanent number issue (invalid, blocked)? A policy violation? A rate limit? Each platform (Twilio, AWS SNS, MessageBird, WhatsApp Cloud API, Google RCS) speaks a different error language. Without a classification strategy, you'll retry invalid numbers forever or give up on fixable problems.

This diagnosis helps you classify platform-specific errors and build smart retry/fallback logic.

## Context: Platform-Specific Errors and Classification

**Error Classification Taxonomy:**

**Transient (Retry)** — The error is temporary. Retry with exponential backoff.
- Network timeout, carrier congestion, API overload
- Action: Retry (backoff 2s → 5s → 15s → 60s)
- Example: "Service temporarily unavailable"

**Permanent (Don't Retry)** — The error is structural. Retrying won't help.
- Invalid number (wrong format, non-existent), account suspended, policy violation
- Action: Log, skip, fallback to different channel or ask user to update number
- Example: "Invalid phone number"

**Rate Limit (Queue)** — You're sending too fast. Slow down without fallback spam.
- Per-account, per-carrier, per-recipient limits hit
- Action: Queue message, wait, retry later or reduce send rate
- Example: "Rate limit exceeded"

**Compliance (Skip)** — Consent/compliance issue. Fallback to compliant channel.
- User didn't consent, country restriction, anti-spam trigger
- Action: Skip this channel, try fallback, or alert user
- Example: "Recipient not opted in"

**Platform-Specific Error Mapping:**

**SMS Carriers (Twilio, AWS SNS, MessageBird):**

| Error Code | Message | Type | Action |
|------------|---------|------|--------|
| 20001 | Invalid phone number | Permanent | Skip, ask user to verify |
| 21211 | Invalid 'To' parameter | Permanent | Log, investigate format |
| 21601 | Message exceeds max length | Permanent | Truncate or split message |
| 30001 | Queue full | Rate Limit | Backoff and retry |
| 30003 | Account not authorized for geo | Permanent | Check account settings |
| 30004 | Carrier blocked (spam flag) | Permanent | Manual review, reputational issue |
| 30005 | Daily limit exceeded | Rate Limit | Queue for next day |
| 30008 | Malformed request | Permanent | Debug API call |
| 30009 | Service temporarily unavailable | Transient | Retry with backoff |
| 50003 | Unreachable destination | Permanent | Number may be invalid or ported |

**WhatsApp Cloud API (Meta):**

| Error Code | Message | Type | Action |
|------------|---------|------|--------|
| 131000 | Message rate exceeded | Rate Limit | Queue, backoff, reduce rate |
| 131008 | Resource exhausted | Transient | Retry after 60s |
| 131009 | Messaging limit reached | Rate Limit | Account limit, contact Meta |
| 131021 | Account suspended | Permanent | Manual review, policy violation |
| 131022 | Template not approved | Permanent | Resubmit or use different template |
| 131026 | Phone number invalid | Permanent | Verify number with user |
| 131052 | Message to user blocked by user | Permanent | User blocked app, ask to unblock |
| 131057 | Too many requests | Rate Limit | Queue and backoff |
| 160001 | User not found | Permanent | Contact may have deleted WhatsApp |

**RCS (Google, carriers):**

| Error Code | Message | Type | Action |
|------------|---------|------|--------|
| 100 | Invalid parameter | Permanent | Debug request format |
| 400 | Invalid recipient | Permanent | Verify phone number |
| 401 | Authentication failed | Permanent | Check API credentials |
| 403 | Not authorized for geo | Permanent | RCS not available in region |
| 429 | Rate limited | Rate Limit | Backoff and queue |
| 500 | Server error | Transient | Retry with exponential backoff |
| 503 | Service unavailable | Transient | Retry with backoff |

## Options: Error Handling Approaches

### Option 1: Naive Retry (Anti-Pattern, Not Recommended)
Retry every error 3 times, then give up.

**Logic:**
```
send(message):
  for i in range(3):
    try:
      return api.send(message)
    except:
      sleep(2^i)  # exponential backoff
  log(failed)
```

**Cons:**
- Retries permanent errors forever (wastes API calls)
- Doesn't differentiate transient vs rate-limit vs compliance
- Can violate compliance (retrying non-opted contacts)
- No observability into error patterns

### Option 2: Classify, Route, Retry (Recommended)
Classify each error type, route accordingly, and retry only transient/rate-limit errors.

**Logic:**
```
send(message):
  try:
    return api.send(message)
  except ApiError as e:
    error_type = classify_error(e.code)
    
    if error_type == 'transient':
      retry_with_backoff(message, backoff=2s)
    elif error_type == 'rate_limit':
      queue_message(message, priority=high)
    elif error_type == 'permanent':
      log_permanent_failure(message, error=e)
      fallback_to_email(message)  # Try different channel
    elif error_type == 'compliance':
      skip_channel(message.user_id, message.channel)
      log_compliance_issue(message, error=e)
```

**Pros:**
- Retries only transient errors (saves API cost)
- Queues rate-limited messages (preserves throughput)
- Skips compliance violations (protects against fines)
- Enables smart fallback (only when truly needed)

**Cons:**
- Requires error code mapping per platform (setup cost)
- Needs monitoring to catch misclassifications

### Option 3: Partner with Vendor for Classification (Outsourced)
Use third-party service (Twilio Flex, MessageBird Insights) to classify errors automatically.

**Logic:**
- All errors flow through vendor classification API
- Vendor maintains error mappings as platforms change
- Your system receives normalized error type (transient/permanent/rate_limit)

**Pros:**
- Outsourced maintenance as platforms evolve
- Normalized across multiple platforms
- Vendor expertise in error handling

**Cons:**
- Additional API call latency (50-100ms per message)
- Vendor lock-in
- Cost (per-API-call fee)

## Recommended Approach

**Implement Option 2 (Classify & Route) with platform error mapping:**

1. **Month 1: Error Classification Schema**
   - Create `error_classification` table: `error_code, platform, error_type (transient/permanent/rate_limit/compliance), action, timestamp`
   - Build error classifier: Given platform + error_code → error_type
   - Start with SMS (Twilio) and WhatsApp error mappings above

2. **Week 2: Retry Logic**
   ```python
   def send_with_retry(user_id, channel, message):
       max_retries = {'transient': 3, 'rate_limit': 10}
       
       for attempt in range(max_retries.get(error_type, 1)):
           try:
               result = api.send(user_id, channel, message)
               log(success, channel)
               return result
           except ApiError as e:
               error_type = classify_error(e.code, channel)
               
               if error_type == 'transient':
                   wait_time = min(2 ** attempt, 120)  # cap at 2 min
                   time.sleep(wait_time)
               elif error_type == 'rate_limit':
                   queue.add(user_id, channel, message, delay=60)
                   return
               elif error_type in ['permanent', 'compliance']:
                   log_terminal_failure(user_id, channel, error_type)
                   return
   ```

3. **Month 2: Fallback Integration**
   - Permanent/compliance errors → try fallback channel (Email)
   - Rate-limit errors → queue, don't fallback (respects rate limit)
   - Transient errors → retry, don't fallback

4. **Month 3: Observability**
   - Dashboard: Error breakdown by type and platform
   - Alerts: When transient error rate > 5%, rate-limit errors > threshold
   - Weekly report: Top errors by platform, manual review candidates

**Error Handling by Message Type:**

| Message Type | Transient | Rate Limit | Permanent | Compliance |
|--------------|-----------|-----------|-----------|-----------|
| OTP/Security | Retry 3x | Queue | Fallback to email | Skip SMS, try email |
| Order Update | Retry 3x | Queue | Fallback to email | Skip WhatsApp, try SMS |
| Support | Retry 1x | Queue | Fallback | Skip channel |
| Marketing | Retry 1x | Queue | Mark as unreachable | Skip entirely |

## Follow-Up Questions

- What's your current error handling? (All retry equally, or differentiated?)
- Which platforms are you using? (Need platform-specific error codes)
- How many messages are failing with "rate limit" vs "permanent" errors?
- Do you have error tracking logs from the last month? (Can classify retrospectively)
- What's your SLA for message delivery? (Determines retry aggressiveness)
- Are you tracking which errors correlate with user complaints?

## See Also

- [Channels Routing Diagnosis](channels-routing-diagnosis.md) — Choosing primary channels
- [Channels Fallback Strategy](channels-fallback-strategy.md) — Building fallback chains using error classification
- [Channels Rate Limiting Strategy](channels-rate-limiting-strategy.md) — Handling rate-limit errors specifically
- [Channels Compliance Checklist](channels-compliance-checklist.md) — Compliance errors and solutions
