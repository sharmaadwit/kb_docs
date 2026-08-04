# SMS DLT Registration and Compliance

DLT (Distributed Ledger Technology) registration is required in India to send promotional and transactional SMS through approved Telecom Service Providers (TSPs). Gupshup provides guidance and co-registration support.

## What is DLT?

DLT is India's regulatory framework (TRAI) for tracking SMS content. Every SMS must be tagged as:

- **Transactional (OTP, confirmations, alerts)** — Faster approval (2–3 days)
- **Promotional** — Slower (5–7 days)
- **Service Explicit Consent (SEC)** — Requires customer opt-in consent

## Why DLT is Required

Telecom regulators (TRAI) require businesses to register their SMS sending entity and template category to prevent spam. Without DLT registration, SMS may be silently dropped or throttled by TSPs.

## Registration Steps

### Step 1: Register with TSP (Telecom Service Provider)

Common TSPs in India:

- Bharti Airtel
- Jio (BSNL)
- VI (Vodafone Idea)

Visit your TSP's DLT portal and register:

1. Business details (PAN, GST if applicable)
2. Contact person
3. Entity classification (Transactional/Promotional/both)

**Timeline**: 2–5 business days for approval

### Step 2: Create Templates in Gupshup Console

1. Navigate to **SMS** → **Templates**
2. Create template with DLT-compliant format:
   - Include an unsubscribe mechanism (e.g., "Reply STOP to unsubscribe")
   - Use clear sender ID (your business name, max 6 characters)
   - Tag as Transactional or Promotional

### Step 3: Provide DLT Approval to Gupshup

Once TSP approves your DLT registration, provide:

1. TSP name
2. DLT registration ID / Header ID
3. Registered entity name

Gupshup maps this to your account; SMS sending is automatically routed through your approved TSP.

## Common Issues & Resolution

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| "DLT not approved" | Wrong entity classification | Re-register with correct type (Transactional vs Promotional) |
| "SMS delivery failing" | DLT header mismatch | Verify sender ID matches TSP registration |
| "Templates rejected" | Missing unsubscribe clause | Add STOP keyword to template |
| "Slow approval" | Promotional tag on transactional SMS | Re-classify as Transactional (faster) |

## Gupshup's Role

- **We provide**: Compliance checklist, template audit, TSP mapping guidance
- **You own**: TSP relationship, DLT registration, entity credentials
- **Timeline**: 2–4 weeks total (TSP approval 2–3 weeks + Gupshup mapping 1 week)

## Best Practices

1. **Start with Transactional SMS** (OTP/confirmations) — Faster approval, simpler compliance
2. **Batch templates** — Don't submit 1 template at a time; group by category
3. **Use clear sender IDs** — Avoid ambiguity; TSPs reject unclear identities
4. **Monitor delivery rates** — Low delivery = DLT header mismatch or TSP throttling

For help, email support@gupshup.io with your TSP name and DLT ID.
