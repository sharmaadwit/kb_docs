# Channels & Integration: Rate Limiting Strategy

## Diagnosis: Getting Rate Limited, What Now?

Your SMS API just returned "Rate limit exceeded." WhatsApp account is temporarily throttled. RCS carrier is blocking your IP. You've hit a limit—either per-account, per-carrier, per-hour, or per-recipient. Now your messages queue up. Some get dropped. Users get confused. Support tickets spike. Without a rate-limiting strategy, you're either flying blind or overspending on extra accounts.

This diagnosis helps you understand rate-limit triggers, build backoff + queue logic, and optimize send rates without hitting limits.

## Context: Per-Carrier, Per-Account, Peak vs Off-Peak Limits

**Rate Limit Types:**

**Per-Account Limits** (Enforced by your vendor: Twilio, MessageBird, AWS)
- Total SMS per second: 100-1,000 msgs/sec (varies by vendor, plan, account age)
- Daily SMS cap: Varies by tier (starter: 1k/day, enterprise: unlimited)
- Example: "You have 50 msgs/sec quota. Upgrade for 100 msgs/sec"
- Hit when: Bulk send campaigns, mass notifications

**Per-Carrier Limits** (Enforced by mobile carriers: Verizon, Airtel, Deutsche Telekom)
- Short-form SMS: 1 msg per second to same number (prevents spam)
- Keywords: "Verify", "Confirm", "Click" flagged, rate-limited
- High volume: Carrier may cap you after 10k msgs/hour (varies by carrier)
- Hit when: Campaign targets same carrier heavily, bulk send during peak

**Per-Recipient Limits** (Anti-spam, carrier-enforced)
- Can't send >1 message every 30 seconds to same number
- Repeated failures to same number (NXDOMAIN, invalid) flag number as "unreachable"
- Multiple short links or keywords trigger spam filters
- Hit when: Retrying failed messages too aggressively

**WhatsApp Limits** (Meta-enforced)
- Tier 1 (new accounts): 1k msgs/day
- Tier 2 (established): 100k msgs/day
- Tier 3 (enterprise): Unlimited (on request)
- Hit rate: 131000 (message rate exceeded), 131009 (messaging limit reached)

**RCS Limits** (Carrier-dependent, varies)
- Per IP: Carrier may cap to 1k-10k msgs/hour
- Per sending number: Similar caps
- No standardization across carriers

## Options: Rate-Limit Handling Approaches

### Option 1: Fail Fast (Simple, Loses Messages)
When rate limit hit, return error immediately. Caller decides whether to retry.

**Logic:**
```
send(message):
  if current_rate > limit:
    raise RateLimitError("Quota exceeded")
  return api.send(message)
```

**Pros:**
- Simple, no infrastructure
- Caller has control

**Cons:**
- Messages are lost (unless caller implements queue)
- No visibility into queued backlog
- User gets no confirmation of delivery
- Support bears cost of complaints

### Option 2: Exponential Backoff (Anti-Pattern for High Volume)
When rate limit hit, wait and retry exponentially. Works for low volume, fails at scale.

**Logic:**
```
send(message):
  for attempt in range(5):
    try:
      return api.send(message)
    except RateLimitError:
      wait_time = 2 ** attempt  # 1s, 2s, 4s, 8s, 16s
      time.sleep(wait_time)
  raise RateLimitError("Exceeded max retries")
```

**Cons:**
- Blocks caller thread (no async)
- Doesn't scale (1,000 messages would wait forever)
- Still loses messages after max retries

### Option 3: Queue + Backoff (Recommended Standard)
Implement a message queue. When rate limit hit, enqueue message with exponential backoff and retry asynchronously.

**Logic:**
```
send(message):
  try:
    return api.send(message)
  except RateLimitError:
    queue.add(message, retry_delay=60, backoff_factor=1.5)
    return queued_confirmation(message)

async def process_queue():
  while True:
    message = queue.get_next()
    if message.next_retry_time > now():
      continue  # Not ready yet
    try:
      api.send(message)
      queue.mark_success(message)
    except RateLimitError:
      message.retry_count += 1
      message.next_retry_time = now() + (60 * 1.5^retry_count)
      queue.update(message)
    except PermanentError:
      queue.mark_failed(message)
```

**Pros:**
- Non-blocking (async)
- Preserves all messages
- Exponential backoff respects vendor limits
- Observable (queue depth, retry stats)

**Cons:**
- Requires message queue infrastructure (Redis, SQS, database)
- Messages may be delayed (hours in extreme cases)

### Option 4: Burst Management with Token Bucket (Optimized)
Use token bucket algorithm to spread sends evenly and prevent burst overages.

**Logic:**
```
class TokenBucket:
  def __init__(self, capacity=100, refill_rate=10):  # 100 msgs/sec, refill 10/sec
    self.capacity = capacity
    self.tokens = capacity
    self.refill_rate = refill_rate
    self.last_refill = time.time()
  
  def acquire(self, count=1):
    self.refill()
    if self.tokens >= count:
      self.tokens -= count
      return True
    return False
  
  def refill(self):
    now = time.time()
    elapsed = now - self.last_refill
    tokens_earned = elapsed * self.refill_rate
    self.tokens = min(self.capacity, self.tokens + tokens_earned)
    self.last_refill = now

bucket = TokenBucket(capacity=100, refill_rate=50/sec)

def send(message):
  if not bucket.acquire(1):
    queue.add(message, delay=0.1)  # Try again in 100ms
  else:
    api.send(message)
```

**Pros:**
- Spreads load evenly (prevents bursts)
- Never exceeds limit
- Predictable latency
- Reduces queue depth

**Cons:**
- Adds latency (waiting for tokens)
- More complex logic

## Recommended Approach

**Start with Option 3 (Queue + Backoff) + Option 4 (Token Bucket optional):**

1. **Immediate (Week 1):**
   - Identify your per-account limits: SMS (msgs/sec), WhatsApp (msgs/day), RCS (msgs/hour)
   - Set alert at 70% of limit (e.g., if limit is 100 msgs/sec, alert at 70/sec)

2. **Week 2-3: Queue Implementation**
   - Add Redis or database queue: `failed_message_queue` table with columns: `user_id, channel, content, status (pending/retry/failed), retry_count, next_retry_time`
   - Implement async worker: Check queue every 10 seconds, retry messages where `next_retry_time <= now()`
   - Implement backoff: `next_retry_time = now() + (60 * 1.5 ^ retry_count)`, cap at 24 hours

3. **Month 1: Send Rate Monitoring**
   - Track sends per second by channel (SMS, WhatsApp, RCS)
   - Alert: If SMS send rate > 70/sec (assuming 100/sec limit)
   - Alert: If WhatsApp queue depth > 1,000 (messages piling up)

4. **Month 2: Optimization**
   - If frequently hitting limits, negotiate higher quota with vendor
   - If spread across multiple accounts, implement per-account round-robin
   - If carrier-specific blocks, consider multi-carrier routing

5. **Optional: Token Bucket (Month 3, if bursty traffic)**
   - If traffic is bursty (e.g., campaign at 9am → 500 msgs/sec burst), implement token bucket to smooth
   - Refill rate = 50 msgs/sec, capacity = 100 msgs (allows 2-second bursts without hitting 100/sec limit)

**Queuing & Retry Strategy by Message Type:**

| Message Type | Max Queue Wait | Max Retries | Retry Backoff |
|--------------|---|---|---|
| OTP/Security | 5 min | 3 | 30s → 1m → 2m |
| Urgent Alert | 2 min | 2 | 20s → 1m |
| Order Update | 1 hour | 5 | 1m → 3m → 10m → 30m → 1h |
| Marketing | 24 hours | 10 | 1h → exponential to 24h |

**Alert Thresholds:**

| Threshold | Alert Level | Action |
|-----------|------------|--------|
| Send rate > 70% of limit | Yellow | Monitor closely |
| Send rate > 85% of limit | Orange | Reduce non-critical sends, consider upgrade |
| Rate limit error | Red | Queue activated, investigate spike |
| Queue depth > 10k | Red | Critical, check for sustained overload |

## Follow-Up Questions

- What's your current send rate (msgs/sec) by channel?
- What's your vendor's rate limit? (SMS msgs/sec, WhatsApp msgs/day)
- Are you hitting rate limits today, or is this preventive?
- What percentage of sends are campaign-driven (bursty) vs transactional (steady)?
- Do you have a queue infrastructure (Redis, RabbitMQ, SQS)?
- How long can users tolerate a delay in message delivery? (SLA)
- Are you using multiple SMS accounts or carriers to scale?

## See Also

- [Channels Routing Diagnosis](channels-routing-diagnosis.md) — Multi-channel strategy to distribute load
- [Channels Fallback Strategy](channels-fallback-strategy.md) — Don't fallback on rate-limit errors (queue instead)
- [Channels Error Codes by Platform](channels-error-codes-by-platform.md) — Classify rate-limit errors specifically
- [Channels Compliance Checklist](channels-compliance-checklist.md) — Rate limiting vs compliance (retry limits)
