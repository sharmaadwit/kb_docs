# Channels & Integration: Fallback Strategy

## Diagnosis: Channel Failing, What's the Fallback?

Your primary channel (SMS, WhatsApp, Email) just failed. Network timeout. Rate limit hit. Account suspended. Carrier block. Now what? Do you retry on the same channel? Switch to a backup? Alert the user? Without a fallback strategy, you silently lose messages. With a bad fallback strategy, you spam users or violate compliance.

This diagnosis helps you build a fallback chain that keeps messages flowing without breaking compliance or user trust.

## Context: Network Issues, Rate Limits, Carrier Blocks, and Fallback Triggers

**Common Failure Modes:**

**Network/Transient Failures**
- Carrier timeout (1-10 seconds)
- API gateway unavailable (rare, 30-60 seconds)
- DNS resolution failure (5-30 seconds)
- Recovery: Automatic retry (exponential backoff) on same channel

**Rate Limits**
- Per-account limit hit (e.g., 100 SMS/sec on Twilio)
- Per-carrier limit hit (e.g., Airtel blocks after 10k SMS/hour)
- Per-recipient limit hit (e.g., "too many messages to this number")
- Recovery: Queue and backoff, or switch channel

**Carrier Blocks (Hard Failure)**
- Number flagged as spam
- Repeated delivery failures (NXDOMAIN, invalid number)
- Carrier policy violation (high volume, short links, keywords)
- Recovery: Switch channel permanently or ask user to update number

**Account Suspension**
- WhatsApp: Policy violation (spam, harassment, keyword list)
- SMS: Account flagged by carrier
- Recovery: Manual review, account appeal, fallback to other channel

**User Has No Phone (SMS/WhatsApp Only)**
- International travel, new user, ported number
- Recovery: Email fallback, ask user to add contact method

**User Didn't Opt-In (Compliance Failure)**
- SMS consent not granted
- WhatsApp not in contact's profile
- Recovery: Skip send or use compliant channel (Email)

## Options: Fallback Approaches

### Option 1: SMS Fallback (Most Reliable)
Primary channel (WhatsApp, RCS, Email) fails → automatically resend via SMS.

**Routing:**
1. Try WhatsApp → fail after 5 seconds
2. → Retry SMS (opt-in check required)
3. → If SMS fails → Email

**Pros:**
- SMS is most reliable (95%+ delivery)
- Global reach (works everywhere)
- Compliance clear (explicit TCPA/GDPR requirements)

**Cons:**
- Cost increase (SMS is expensive)
- Only works if user has phone number
- Requires SMS opt-in (compliance)
- User gets duplicates if both channels used

### Option 2: Email Fallback (Cost-Optimized)
Primary channel (SMS, WhatsApp) fails → fallback to Email.

**Routing:**
1. Try SMS → fail
2. → Try WhatsApp
3. → Email fallback (no consent required for transactional)

**Pros:**
- Very low cost (negligible)
- No compliance barrier for transactional email
- Works for any user (email > phone)

**Cons:**
- Slower delivery (60+ seconds)
- No guarantee of inbox placement
- Not suitable for urgent alerts (OTP, fraud)

### Option 3: User Choice (Consent-Aware)
Ask user to select fallback preference or rank channel preference in profile.

**Routing:**
1. Try primary channel (user-selected)
2. → If fails, try user's secondary channel
3. → If no preference, use SMS (or Email for non-phone users)

**Pros:**
- User controls experience
- Respects consent (only tries channels user opted into)
- Highest user satisfaction

**Cons:**
- Requires UI/UX for preference management
- Not all users will set preference
- More complex logic

### Option 4: Manual Routing (Control-Heavy, Support-Intensive)
When primary channel fails, log to queue and have support team manually route.

**Routing:**
1. Try SMS → fail
2. → Log to "manual_routing_queue"
3. → Support team reviews and decides (contact user, try different channel, escalate)

**Pros:**
- Human judgment (can call customer, verify number)
- Catches fraud/invalid data
- Best UX for high-value customers

**Cons:**
- Doesn't scale
- Slow (hours vs seconds)
- Support overhead

## Recommended Approach

**Use a hybrid: Email + SMS Fallback with user preference override:**

1. **Define Primary Routing (Month 1):**
   - OTP/security: SMS only (no fallback needed)
   - Order updates: WhatsApp (if opted in) → SMS fallback (if opted in) → Email
   - Customer support: WhatsApp (replies) → SMS (if opted in) → Email
   - Notifications: Email only (no fallback needed)

2. **Implement Fallback Logic (Week 2):**
   ```
   send_message(user_id, message_type, content):
     for channel in user.channel_preference[message_type]:  # ['whatsapp', 'sms', 'email']
       try:
         result = send_via_channel(user_id, channel, content, attempt=1)
         if result.success:
           log(success, channel, timestamp)
           return
       except NetworkTimeout:
         retry_with_backoff(user_id, channel, message_type)  # Retry same channel
         return
       except RateLimit:
         queue_for_later(user_id, channel, message_type)  # Queue, don't fallback
         return
       except Consent:
         continue  # Skip this channel, try next
       except CarrierBlock:
         log(permanent_failure, channel, user_id)
         continue  # Try next channel
     
     log(all_channels_failed, user_id, message_type)
     alert_support(user_id, "No delivery channel available")
   ```

3. **User Preferences (Week 3):**
   - Add profile field: `channel_preference`: { "marketing": ["whatsapp", "email"], "transactional": ["sms", "email"] }
   - Provide UI to manage preferences
   - Default: SMS → WhatsApp → Email (respecting opt-ins)

4. **Monitor & Alert (Month 1+):**
   - Track fallback rate by message type (target: <5% fallback)
   - Alert when fallback exceeds threshold
   - Review carrier blocks weekly
   - Audit permanent failures (invalid numbers, suspended accounts)

**Key Principle:** Retry the same channel for transient failures. Fallback to a different channel for compliance/permanent failures.

## Follow-Up Questions

- Are you sending transactional (time-sensitive) or marketing (asynchronous) messages?
- What's your current delivery reliability by channel? (Needed to rank fallback priority)
- Do you have users without SMS consent? (Can you fallback to Email?)
- How many messages have you lost due to channel failures in the last month?
- Are you tracking which channels users actually check? (SMS vs Email open rate)
- Do you have data on user channel preferences by segment or geography?

## See Also

- [Channels Routing Diagnosis](channels-routing-diagnosis.md) — Choosing primary channels by use case
- [Channels Compliance Checklist](channels-compliance-checklist.md) — Consent rules for each channel
- [Channels Error Codes by Platform](channels-error-codes-by-platform.md) — Diagnosing why channels fail
- [Channels Rate Limiting Strategy](channels-rate-limiting-strategy.md) — Handling rate limits without fallback spam
