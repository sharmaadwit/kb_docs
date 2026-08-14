# Channels & Integration: Routing Diagnosis

## Diagnosis: When to use SMS vs WhatsApp vs RCS vs Email

Your messaging platform supports multiple channels, each with distinct delivery speeds, costs, compliance profiles, and user adoption rates. The question isn't which channel is "best"—it's which channel is best for each use case, each user segment, and each geographic region. Sending everything via SMS is expensive. Relying solely on WhatsApp leaves you vulnerable to network blocks in regulated markets. Email works for confirmations but fails for urgent alerts. RCS promises rich messaging but carrier adoption is fragmented.

This diagnosis helps you build a routing strategy that maximizes delivery, minimizes costs, and maintains compliance across your customer base.

## Context: Channel Capabilities, Costs, Delivery Speed, and Compliance

Each channel has distinct operational characteristics:

**SMS (Short Message Service)**
- Delivery speed: 1-5 seconds (most reliable)
- Cost: $0.003-$0.10 per message (varies by carrier, volume)
- Adoption: ~95% globally (universal across devices)
- Character limit: 160 (GSM 7-bit) or 70 (Unicode)
- Compliance: TCPA (US), GDPR (EU), POPIA (South Africa), multiple country-specific regulations
- Use case: OTP, fraud alerts, urgent notifications

**WhatsApp**
- Delivery speed: 1-30 seconds (depends on network, app state)
- Cost: $0.004-$0.05 per message (template-based pricing)
- Adoption: ~70% in emerging markets, 40-50% in developed markets
- Character limit: None (up to 4,096 characters)
- Compliance: GDPR, but less regulated than SMS in most markets
- Use case: Customer support, order updates, onboarding, rich content
- Risk: Account suspension if flagged for spam or policy violation

**RCS (Rich Communication Services)**
- Delivery speed: 1-10 seconds (carrier-dependent)
- Cost: $0.01-$0.08 per message (emerging, variable pricing)
- Adoption: ~20-30% in developed markets, <5% in emerging markets
- Character limit: None (up to 2,000 characters)
- Compliance: GDPR, TCPA (rules evolving)
- Use case: Rich messaging, branded content, customer engagement
- Risk: Carrier fragmentation, fallback to SMS if unsupported

**Email**
- Delivery speed: 1-60 seconds (depends on inbox load)
- Cost: $0.0001-$0.001 per message (negligible)
- Adoption: ~99% (but inbox placement varies)
- Character limit: None
- Compliance: CAN-SPAM (US), GDPR (EU), multiple regulations
- Use case: Confirmations, receipts, newsletters, non-urgent updates
- Risk: Spam filtering, inbox fatigue

**Key Tradeoff Matrix:**
| Channel | Speed | Cost | Adoption | Compliance | Best For |
|---------|-------|------|----------|-----------|----------|
| SMS | Highest | Highest | Highest | Strictest | Alerts, OTP |
| WhatsApp | High | Medium | High (EM) | Medium | Support, updates |
| RCS | High | Medium | Low | Evolving | Rich content |
| Email | Medium | Lowest | Highest | Medium | Confirmation |

## Options: 3 Adoption Paths

### Option 1: SMS-First (Cost-Optimized, Compliance-Heavy)
Start with SMS for all use cases, add channels only when SMS fails or is inadequate. Best for regulated industries (finance, healthcare) or cost-constrained startups.

**Routing logic:**
1. Send via SMS
2. If SMS delivery fails → Email fallback
3. Add WhatsApp only for proactive customer support (not alerts)

**Pros:** Maximum compliance control, predictable costs, highest reliability
**Cons:** High cost at scale, poor UX for long-form messages, no rich content

### Option 2: Multi-Channel (Balanced, Adoption-Optimized)
Route based on message type and user preference. Send OTP via SMS, customer updates via WhatsApp (if opted in), confirmations via Email.

**Routing logic:**
1. OTP/security → SMS only
2. Order updates → WhatsApp (if opted in) + Email
3. Customer support → WhatsApp first, SMS fallback
4. Newsletters → Email

**Pros:** Lower cost, better UX, higher engagement on WhatsApp, compliance per channel
**Cons:** Operational complexity, multiple vendor integrations, compliance per channel

### Option 3: RCS-First (Future-Optimized)
Invest in RCS for rich experiences, with SMS fallback for unsupported devices. Best for consumer brands with long-term timelines (2-3 years).

**Routing logic:**
1. Send via RCS (rich messages)
2. If RCS not supported → fallback to SMS
3. Add WhatsApp for markets where RCS is blocked

**Pros:** Future-proof, rich content, lower cost than SMS long-term
**Cons:** Carrier adoption still evolving, immature fallback stack, compliance unclear

## Recommended Approach

**Start with Option 2 (Multi-Channel) targeting SMS + WhatsApp:**

1. **Immediate (Month 1):**
   - Route OTP, fraud alerts → SMS only (non-negotiable compliance)
   - Route order updates, shipping → WhatsApp (opt-in) + Email
   - Configure SMS fallback for WhatsApp

2. **Month 2-3:**
   - Add WhatsApp for customer support (replies enabled)
   - Measure WhatsApp adoption by segment and geography
   - Establish consent tracking per channel

3. **Month 4+:**
   - Evaluate RCS adoption in your key markets
   - Consider RCS for rich experiences (promotions, catalogs)
   - Deepen SMS-only strategy for regulated geographies

**Why this approach:**
- Balances cost, compliance, and user engagement
- SMS + WhatsApp covers ~85-90% of your users
- Preserves SMS for high-compliance use cases
- Allows you to defer RCS until adoption justifies investment
- Enables per-channel compliance and consent tracking

## Follow-Up Questions

- Which geographic regions are you operating in? (SMS/WhatsApp adoption varies significantly)
- What's your current message volume per channel?
- Do you have existing compliance obligations (TCPA, GDPR, sector-specific)?
- What percentage of your users have opted into WhatsApp?
- Are you sending proactive (company-initiated) or reactive (user-initiated) messages?
- What's your tolerance for message cost increase if adoption improves delivery rates?

## See Also

- [Channels Compliance Checklist](channels-compliance-checklist.md) — Regulatory requirements by country and channel
- [Channels Fallback Strategy](channels-fallback-strategy.md) — What to do when your primary channel fails
- [Channels Error Codes by Platform](channels-error-codes-by-platform.md) — Debugging delivery failures
- [Channels Rate Limiting Strategy](channels-rate-limiting-strategy.md) — Managing burst traffic and rate limits
