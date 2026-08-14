# Channels & Integration: Compliance Checklist

## Diagnosis: What Compliance Applies to My Channels?

Messaging compliance is not one-size-fits-all. SMS falls under TCPA (US), GDPR (EU), POPIA (South Africa), and dozens of country-specific regulations. WhatsApp is lighter-touch but increasingly regulated. Email has CAN-SPAM (US) and similar rules. RCS compliance is still evolving. Add in sector-specific rules (finance, healthcare, gambling) and geographic variation, and compliance becomes your fastest path to legal risk.

This checklist helps you map which regulations apply to your channels, build compliant routing, and audit your consent trail.

## Context: GDPR, TCPA, Regulatory Landscape by Country and Channel

**Global Frameworks:**

**GDPR (EU, UK, EEA)**
- Applies to: SMS, WhatsApp, Email, RCS (all channels)
- Key requirement: Explicit opt-in consent before sending marketing
- Exception: Transactional messages (OTP, order confirmation) may have lighter consent
- Retention: Delete contact data after opt-out or consent expiry
- Enforcement: €20M or 4% global revenue (whichever is higher)
- Audit: Maintain consent records with timestamp, channel, user ID

**TCPA (Telemarketing Consumer Protection Act, US)**
- Applies to: SMS, WhatsApp (via phone), RCS
- Key requirement: Prior express written consent for SMS marketing
- Do-Not-Call: Must honor National Do-Not-Call registry
- Autodialer restrictions: Can't use automated systems to SMS without consent
- Enforcement: $500-$1,500 per message (private right of action)
- Audit: Consent log with timestamp, channel, user opt-in method

**PIPEDA (Canada)**
- Applies to: SMS, WhatsApp, Email, RCS
- Key requirement: Express or implied consent (lower bar than GDPR)
- Implied consent: Existing customer relationship allows 2-year window
- Enforcement: CAD $10M or 3% revenue (similar to GDPR)

**POPIA (South Africa)**
- Applies to: SMS, WhatsApp, Email, RCS
- Key requirement: Opt-in for marketing, lighter for transactional
- Enforcement: ZAR 1M+ fines, reputational damage

**CAN-SPAM (US Email)**
- Applies to: Email only
- Key requirement: Opt-out (not opt-in) for commercial email
- Exception: Transactional email (receipts, OTP) can be sent without consent
- Enforcement: FTC enforcement, not private right of action

**Regional Variations:**
- **India (TRAI)**: SMS opt-in per category (promotional, transactional, services), strict DND registry
- **Brazil (Lei Geral de Proteção de Dados)**: SMS/WhatsApp opt-in, higher fines than GDPR
- **Australia (Spam Act)**: SMS opt-in, harsh penalties for unsolicited

## Options: Compliance Tracking Approaches

### Option 1: Manual Audit (Documentation-Heavy, Risk)
Maintain compliance spreadsheets, periodic legal reviews, manual consent log inspection. Best for low-volume, single-channel businesses.

**Implementation:**
1. Keep Google Sheet of all SMS opt-ins with timestamp
2. Document consent source (API, web form, SMS reply)
3. Quarterly legal review of compliance log
4. Manual opt-out processing

**Pros:** Zero integration cost, visible consent trail
**Cons:** Manual effort, error-prone, doesn't scale, hard to prove compliance if audited

### Option 2: Automated Consent Tracking (Recommended)
Build consent tracking into your messaging platform. Log every opt-in, opt-out, channel preference, and timestamp.

**Implementation:**
1. Every SMS opt-in recorded with user_id, timestamp, source (form/SMS/API)
2. Consent payload includes: channel, message_type (marketing/transactional), country, opt-in_method
3. Automatic opt-out processing (SMS STOP, email unsubscribe, API)
4. Audit table queryable by user, channel, country, date
5. Monthly compliance report: consent breakdown, opt-outs processed, channel volume

**Pros:** Audit-proof, scalable, automatic opt-out handling, compliance by geography
**Cons:** Engineering effort upfront, requires consent schema design

### Option 3: Third-Party Compliance (Vendor-Managed, Cost)
Use compliance-as-a-service (e.g., Twilio Compliance, MessageBird Compliance) to handle consent, opt-out, audit trails.

**Implementation:**
1. Map all SMS/WhatsApp to third-party consent DB
2. Vendor handles opt-in validation, do-not-call checks, audit reports
3. Your system queries vendor API before sending
4. Vendor maintains compliance records

**Pros:** Outsourced risk, audit-ready reports, vendor expertise
**Cons:** Monthly fees ($500-$5k), vendor lock-in, less visibility into consent logic

## Recommended Approach

**Start with Option 2 (Automated Consent Tracking) with guardrails:**

1. **Immediate (Week 1):**
   - Add consent schema to your contact table: `consent_sms`, `consent_whatsapp`, `consent_email`, `consent_timestamp`, `consent_source`, `user_country`
   - Log every opt-in/opt-out to audit table: `user_id`, `action` (opt_in/opt_out), `channel`, `timestamp`, `source`

2. **Week 2-3:**
   - Route all SMS through consent check: `if contact.consent_sms != 'yes' → don't send`
   - Process SMS STOP replies automatically: `→ set consent_sms = 'no'`, log in audit table
   - Add country field to all contacts (enables GDPR/TCPA/POPIA routing)

3. **Month 1+:**
   - Build monthly compliance report: consent breakdown by country, opt-outs processed
   - Establish legal review cadence (quarterly) for audit readiness
   - Document consent source for each opt-in (form field: "How did you hear about us?")

**Compliance routing by geography:**
```
if country in ['US']:
    require TCPA consent (SMS opt-in) before sending
    check against DNC registry
else if country in ['EU', 'UK', 'EEA']:
    require GDPR consent (explicit opt-in)
    honor GDPR right to deletion
else if country in ['CA']:
    allow implied consent (2-year window)
else:
    require consent (default to strictest)
```

## Follow-Up Questions

- Which countries do you operate in? (Determines which regulations apply)
- What's your current consent tracking process? (Manual log, database, third-party?)
- Do you have a TCPA compliance process for US SMS? (DNC check, consent audit)
- How are you handling SMS STOP replies? (Automatic opt-out, manual review?)
- What's your data retention policy? (Affects GDPR compliance)
- Do you have a Data Processing Agreement (DPA) with your messaging vendor?
- Are you sending any sector-specific messages (financial, healthcare, gambling)?

## See Also

- [Channels Routing Diagnosis](channels-routing-diagnosis.md) — Choosing channels by use case and geography
- [Channels Fallback Strategy](channels-fallback-strategy.md) — Compliance considerations for fallback chains
- [Channels Error Codes by Platform](channels-error-codes-by-platform.md) — Diagnosing compliance-related delivery failures
