# RCS Prerequisites Checklist — Pre-Launch Validation

## Diagnosis: Are You Ready for Carrier Approval?

RCS approval has three gates:
1. **Business & Compliance** (1-2 weeks)
2. **Technical** (1-2 weeks)
3. **Template Review** (ongoing)

## Context: 31-Item Checklist

### Business Docs (8 items)
- Business license & registration
- MSISDN (phone number for RCS)
- Company logo (224x224px)
- Privacy policy URL
- Terms of service URL
- Data handling policy
- Opt-in/opt-out procedures documentation
- Customer support contact info

### Technical Setup (6 items)
- Webhook endpoint (24/7 uptime)
- OAuth 2.0 token refresh logic
- Message rate limits (requests/second)
- Retry logic for failed deliveries
- Logging and monitoring infrastructure
- Load testing for expected volume

### Agent Configuration (6 items)
- Agent name and branding
- Display picture
- Default message for unsupported formats
- Rich card templates (3-5 templates)
- Fallback SMS message if RCS unavailable
- Conversation history retention policy

### Carrier & Regional (3 items)
- Carrier matrix (T-Mobile, Verizon, AT&T, Jio, Airtel, VI, Orange)
- Regional compliance (TCPA, GDPR, TRAI)
- Customer consent verification system

### Template Management (4 items)
- Template registry (all templates documented)
- Template versioning
- Template approval workflow
- Template update procedures

### Compliance (4 items)
- DLT registration (if applicable for region)
- Consent token tracking
- Unsubscribe mechanism
- Audit trail logging

## Options: Accelerate Approval

Prepare all docs upfront, pre-design templates, set up webhook, respond to carrier questions <24h.

## Recommended Approach

**Validate carrier support in your market FIRST.** Plan 4-6 weeks for carrier approval. Most stalls due to 1-2 missing docs. Check all 31 items before submitting.

## Follow-Up Questions

- Which carriers are you targeting? That drives approval timeline.
- Have you documented regional compliance (TCPA/GDPR/TRAI)?
- Do you have a production-ready webhook with 24h uptime monitoring?
