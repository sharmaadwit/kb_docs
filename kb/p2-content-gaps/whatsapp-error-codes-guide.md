# WhatsApp Error Codes: Complete Troubleshooting & Prevention Guide

## Overview

WhatsApp Business API returns specific error codes for different failure scenarios. Understanding these codes helps you diagnose issues quickly, implement the right fix, and prevent recurrence. This guide covers the most common errors in production, their root causes, troubleshooting steps, and prevention strategies.

---

## Critical Errors (Immediate Action Required)

### Error 131000: Invalid Recipient Phone Number

**What it means:** The phone number format is invalid or doesn't exist in WhatsApp's system.

**Root causes:**
- Missing country code (e.g., `9876543210` instead of `+919876543210`)
- Invalid country code format (e.g., `+0919876543210` has leading zero)
- Number doesn't have WhatsApp account (dormant, never activated, or opted out)
- Number is landline or VoIP without WhatsApp support
- Number is temporarily suspended or blocked by WhatsApp

**Troubleshooting steps:**
1. Verify format: `+[country_code][area_code][local_number]` (no spaces, dashes, or leading zeros in country code)
2. Test with country code validator: `+919876543210` ✅ vs `919876543210` ❌
3. Check recipient has active WhatsApp account: ask them to send a test message to your business number
4. Confirm number isn't on business rejection list: review recent opt-outs in dashboard
5. If number is correct: recipient may need to reinstall WhatsApp or update app

**Prevention:**
- Normalize phone numbers before sending: `+[CC][number]` format
- Validate against known country codes (India: 91, US: 1, UK: 44)
- Implement double opt-in: confirm number before adding to send list
- Periodic verification: re-verify inactive numbers monthly

**Example:**
```
❌ Wrong: 9876543210, 09876543210, +0919876543210
✅ Right: +919876543210
```

---

### Error 131001: Message Send Failed

**What it means:** General message delivery failure. Usually temporary, but needs investigation.

**Root causes:**
- **Rate limiting:** Sending too many messages too fast to same recipient
- **Network timeout:** WhatsApp servers unreachable (usually resolves in <5 min)
- **Invalid message format:** Unsupported media type or corrupted payload
- **Account issue:** Your WhatsApp Business account has delivery limits active
- **Recipient network issue:** Poor connectivity on their end (temporary)

**Troubleshooting steps:**
1. Check timestamp: if error happened >5 minutes ago, likely resolved now; retry
2. Verify message format: text, image, document, video, or template (no custom formats)
3. Check sending rate: if sending >100 messages/minute, implement backoff strategy
4. Review account status: dashboard → Account Settings → Delivery Status
5. If image/video: confirm file size <16MB (images) or <100MB (videos)
6. Retry with exponential backoff: wait 5s, 10s, 20s before each retry

**Prevention:**
- Implement rate limiting: max 100 messages/minute per recipient
- Use exponential backoff for retries (not aggressive polling)
- Monitor account delivery status dashboard daily
- Test message format with small batch before scaling

---

### Error 131002: Message Rejected by WhatsApp

**What it means:** WhatsApp actively rejected your message (not a network error).

**Root causes:**
- **Spam detected:** Message content flagged as spam/phishing by WhatsApp filters
- **Template violation:** Using message template incorrectly (wrong variables, missing fields)
- **Recipient rejected:** User previously reported your messages as spam
- **Unsupported content:** Links to phishing sites, malware, or policy-violating content
- **Rate limiting:** Account has been throttled for previous spam

**Troubleshooting steps:**
1. Review message content: does it contain spam indicators? (too many links, urgency language, suspicious URLs)
2. For templates: verify all variables filled, correct placeholders used
3. Check recipient history: have they marked previous messages as spam?
4. Test with different recipient: if same error, likely content issue; if works, recipient-specific
5. Review dashboard: Account → Compliance → see if account has restrictions
6. Contact support: if error persists, escalate with message ID and recipient number

**Prevention:**
- Use pre-approved message templates for campaigns
- Avoid: "URGENT!!!", multiple links, URL shorteners (use full URLs)
- Monitor spam complaint rate: maintain <0.1% across all recipients
- Implement feedback loop: track which messages get "Report" clicks
- Test template content with small group before full broadcast

---

## Common Errors (Recoverable)

### Error 131003: Throttled

**What it means:** You're sending too many messages too fast. WhatsApp has rate-limited your account.

**Root causes:**
- Burst traffic: sending millions of messages in short period
- Repeated failures with aggressive retries
- Account behavior flagged as abnormal

**Fix:**
- Implement exponential backoff: 1s, 2s, 4s, 8s between retries
- Spread sends over time: 1000 messages/hour = ~17/minute
- Wait 60 seconds before retry if you get 131003

**Prevention:**
- Daily budget: don't exceed 10k messages/day without high-speed tier
- Monitor queue depth: if backing up, implement pause
- Contact Gupshup sales for high-speed tier if legitimately high volume

---

### Error 131004: Undeliverable

**What it means:** Message couldn't be delivered to recipient (not bounced, just unreachable).

**Root causes:**
- Recipient temporarily offline (airplane mode, poor network)
- Number doesn't have WhatsApp installed
- Device storage full (message can't be stored)
- WhatsApp server issue (rare)

**Fix:**
- Retry after 30 minutes for offline recipients
- For "doesn't have WhatsApp" errors: don't retry; user needs to activate first
- Check dashboard to see delivery status after 24 hours

---

### Error 131005: Invalid Media

**What it means:** Media file (image, video, document) is corrupted, wrong format, or too large.

**Root causes:**
- File size >16MB (images) or >100MB (videos)
- Unsupported format: video must be MP4/3GP, image must be JPG/PNG
- Corrupted file: upload failed partway through
- URL not accessible: media hosted on private server

**Fix:**
```python
# Validate before sending
if file_type == 'image':
    assert file_size < 16 * 1024 * 1024  # 16MB
    assert format in ['jpg', 'jpeg', 'png']

if file_type == 'video':
    assert file_size < 100 * 1024 * 1024  # 100MB
    assert format in ['mp4', '3gp']
```

---

## Error Code Reference Table

| Code | Error | Severity | Resolution Time |
|------|-------|----------|-----------------|
| 131000 | Invalid recipient | High | Immediate (validate number) |
| 131001 | Send failed (transient) | Medium | 5-10 min (retry) |
| 131002 | Message rejected | High | Immediate (fix content) |
| 131003 | Throttled | Medium | 60 sec (backoff) |
| 131004 | Undeliverable | Low | 30 min (retry) |
| 131005 | Invalid media | High | Immediate (validate file) |

---

## Debugging Workflow

**When you get an error:**

1. **Check the code:** Find it in the table above
2. **Read the cause:** Most errors are preventable
3. **Test immediately:** Try sending to yourself with that code
4. **Fix the root cause:** Not just the symptom
5. **Verify fix works:** Send test batch, monitor for error recurrence
6. **Update your process:** Add validation to prevent future occurrences

**Example: Error 131000**
```
Recipient says: "Message not received"
Check Gupshup logs: Error 131000 (Invalid recipient phone number)

Root cause: You stored "+919876543210" but actually sent "919876543210"
(missing the + prefix)

Fix: Normalize all numbers to +[CC][number] format before sending

Verification: Resend to that recipient, confirm success
```

---

## Advanced: Monitoring & Prevention

### Set Up Error Alerts

Monitor your dashboard for these error spikes:
- **131000 (Invalid numbers):** >1% error rate = data quality issue
- **131001 (Send failures):** >5% error rate = API or network issue
- **131002 (Rejected):** >0.5% error rate = spam content issue
- **131003 (Throttled):** Any occurrences = need rate limiting

### Monthly Audit

1. Export last 30 days of errors
2. Group by error code
3. For each error: identify root cause pattern
4. Update validation rules based on patterns found
5. Test updated validation with sample

---

## FAQ

**Q: I keep getting 131000 for a number I know is correct.**
A: WhatsApp may not have that number in its system. Ask recipient to: (1) reinstall WhatsApp, (2) verify their phone number in app settings, (3) send you a message first to activate.

**Q: How long should I retry 131004 (Undeliverable)?**
A: Retry for 24 hours. If still undeliverable after 24h, recipient likely doesn't have WhatsApp. Move to SMS or email.

**Q: Can I send to business numbers or landlines?**
A: No. WhatsApp only works with personal mobile numbers. Landlines and business numbers will always fail with 131000.

**Q: What's the difference between 131001 and 131004?**
A: 131001 = We tried to send, our system failed (temporary). 131004 = We sent, recipient unreachable (may be temporary or permanent).

---

## Best Practices Summary

✅ **DO:**
- Validate phone numbers before adding to list: `+[CC][number]`
- Use pre-approved templates for campaigns
- Implement exponential backoff for retries
- Monitor error rates daily
- Test with small batch before scaling

❌ **DON'T:**
- Send to numbers without WhatsApp accounts (ask them first)
- Use aggressive retries (1 second intervals)
- Send unsolicited messages (causes 131002)
- Send >100 messages/minute without high-speed tier
- Use URL shorteners (triggers spam filters)

---

**Last Updated:** 2026-08-11  
**Coverage:** WhatsApp Business API errors (Gupshup platform)
