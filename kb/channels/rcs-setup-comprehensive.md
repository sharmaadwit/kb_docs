# How to Set Up RCS — Comprehensive Setup Guide

## Step 0: Diagnosis — Choose Your Path

**Answer 4 questions:**
1. **Expected daily volume?** (<10K vs 10K-100K)
2. **Engineering time available?** (1 person vs team)
3. **Launch timeline?** (urgent vs flexible)
4. **Existing SMS/WhatsApp scale?** (starting fresh vs migrating)

**Output:** Path 1 (Manual, <10K/day) or Path 2 (API-Driven, 10K-100K+/day)

## Prerequisites Before Launch (9 items)

1. **Business license & registration** — Carrier verification
2. **MSISDN phone number** — Dedicated for RCS
3. **Company logo** (224x224px) — Agent branding
4. **Privacy policy URL** — Legal requirement
5. **Compliance docs** — DLT registration (India), TCPA (US), GDPR (EU)
6. **Webhook endpoint** — 24/7 uptime for callbacks
7. **Customer consent system** — Opt-in tracking
8. **Template designs** — 3-5 templates ready
9. **Support contact info** — Escalation path

## Path 1: Manual UI-Based Setup

### Step 1: Access Gupshup Console
- Login to Gupshup Console
- Navigate to Channels > RCS

### Step 2: Submit Metadata
- Agent name & description
- Upload logo (224x224px)
- Provide business URL

### Step 3: Upload Compliance Docs
- Business license
- Privacy policy (URL or PDF)
- DLT/TCPA/GDPR compliance documentation

### Step 4: Submit for Approval
- Review checklist (9 prerequisites)
- Submit to carrier for verification
- **Timeline:** 4-6 weeks

### Step 5: Receive Credentials
- Carrier approval received
- API credentials generated
- Webhook endpoint registered

### Step 6: Configure Webhook
- Set webhook URL
- Enable delivery notifications
- Test with sample message

### Step 7: Create Templates
- Design templates (images, buttons, rich cards)
- Submit for approval (ongoing)
- Test with real users

### Step 8: Test & Validate
- Send sample messages
- Verify delivery & formatting
- Monitor user responses

### Step 9: Launch to Production
- Enable for all users
- Monitor metrics (delivery, open rate, engagement)
- Scale gradually if needed

## Path 2: API-Driven Setup

### Steps 1-7: Same as Path 1

### Step 8: API Integration
- Initialize RCS client (Node.js, Python, Go)
- Set up message sending SDK
- Implement retry logic (exponential backoff)
- Configure webhook handler for callbacks

### Step 9: Implement Resilience
- Retry logic for failed sends
- Fallback to SMS if RCS unavailable
- Circuit breaker for cascading failures
- Monitoring & alerting

### Step 10: Test & Validate
- Load testing (expected volume)
- Failover testing
- User acceptance testing

### Step 11: Launch & Monitor
- Staged rollout (10% → 25% → 50% → 100%)
- Monitor delivery metrics
- Scale infrastructure as needed

## Success Checklist (Pre-Launch)

- [ ] All 9 prerequisites complete
- [ ] Carrier approval received
- [ ] Webhook endpoint tested (24h uptime)
- [ ] Templates approved
- [ ] SMS fallback configured
- [ ] Monitoring & alerting set up
- [ ] Load testing passed
- [ ] Team trained on troubleshooting
- [ ] Escalation path documented
- [ ] Customer support briefed

## Recommended First 30 Days

- **Week 1:** Send 1000 RCS messages, monitor delivery
- **Week 2:** Scale to 10K messages/day, optimize based on metrics
- **Week 3:** Evaluate engagement (open rate, conversion), compare vs SMS
- **Week 4:** Decide on expansion (Path 1 → Path 2?) or consolidation

## Common Mistakes (With Fixes)

1. **Mistake:** Launching without SMS fallback  
   **Fix:** Implement automatic fallback for 5% of messages that fail RCS

2. **Mistake:** Too many templates  
   **Fix:** Start with 3-5 core templates, expand after validation

3. **Mistake:** No monitoring  
   **Fix:** Set up delivery alerts, open rate dashboard, escalation triggers

4. **Mistake:** Approval stalls (missing docs)  
   **Fix:** Use 31-item checklist before submitting (see prerequisites-checklist.md)

5. **Mistake:** No user consent tracking  
   **Fix:** Log consent tokens with each delivery for compliance audit
