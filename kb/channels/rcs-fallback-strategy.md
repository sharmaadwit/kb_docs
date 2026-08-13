# Handling RCS Fallback & Degradation — When RCS Fails

## Diagnosis: What Happens When RCS Fails?

Four failure modes:
1. **User device doesn't support RCS** (10-40% of users)
2. **Carrier network issue** (1-2%, temporary)
3. **User opted out** (2-5% of users)
4. **Template rejected** (rare, <1%)

**Without fallback, delivery fails during critical moments** (order confirmations, payments, shipping, security alerts).

## Context: RCS Fallback Landscape

**High-priority messages need guaranteed delivery:**
- Order confirmations
- Payment verifications
- Shipping updates
- Security alerts

**High-frequency campaigns need fallback:**
- Flash sales
- Time-bound offers
- Marketing promotions

**RCS-only → ~95% delivery**  
**RCS+SMS → ~99% delivery**

Trade-off: Higher cost vs guaranteed delivery.

## Options: Three Fallback Strategies

### Option A: Automatic SMS Fallback
Send RCS first, auto-retry as SMS within 2-5 seconds if fails.

- **Delivery:** 99%+
- **Transparency:** Automatic, user-unaware
- **Complexity:** Low
- **Effort:** 4-8 hours
- **Best for:** Critical messages

### Option B: Manual Routing
Your app decides RCS vs SMS before sending.

- **Control:** Fine-grained
- **Cost:** Optimizable
- **Complexity:** Medium
- **Effort:** 12-20 hours
- **Risk:** Device detection imperfect

### Option C: User Choice
Let customers choose RCS or SMS preference.

- **Autonomy:** Respects user choice
- **Engagement:** May degrade (users prefer SMS)
- **Complexity:** Medium
- **Effort:** 6-12 hours
- **Risk:** Users opt for SMS (lower engagement)

## Recommended Approach

**Use Option A (Automatic SMS Fallback) for production.**

Most robust for time-sensitive messages.

**Cost:** $0.025-0.04/message  
**Setup:** 2-8 hours one-time

## Follow-Up Questions

- What should our fallback rate be? (Good: 15-30%, Warning: >50%)
- How do we measure impact?
- SLA target? (Option A: 99%+ delivery)
