# Healthcare: Multi-Clinic WhatsApp and SMS Strategy

Healthcare clinics and multi-location practices use WhatsApp and SMS for appointment reminders, patient follow-ups, and billing notifications. Gupshup handles compliance (patient data, DLT) and multi-clinic billing.

## Use Cases

### 1. Appointment Reminders (WhatsApp)

**What:** Confirm appointments 24 hours before scheduled time

**Template:** "Reminder: Your appointment with Dr. {{doctor_name}} on {{date}} at {{time}}. Location: {{clinic_name}}, {{address}}. Reply to confirm or reschedule."

**Category:** Utility (2–3 days approval)

**Volume:** 50–200 per clinic per day

### 2. Multi-Clinic Billing & Fee Notifications

**What:** Invoice reminders, payment links, subscription updates

**Template:** "Invoice {{invoice_id}}: ₹{{amount}} due by {{due_date}}. Pay here: {{payment_link}}"

**Category:** Transactional (1–2 days approval)

**Volume:** 30–100 per clinic per month

## Multi-Clinic Billing

Gupshup supports **per-clinic cost tracking** so you can allocate spend to individual locations:

**Setup:**
1. Create "cost centers" for each clinic location
2. Map WhatsApp phone numbers and SMS sender IDs to each clinic
3. Gupshup bills separately per clinic; you bill your patients or sub-practices

**Cost allocation:**
- Access fee: ₹13.80 per clinic per month
- WhatsApp messages: ₹0.80 per message (actual)
- SMS: ₹1.50–2 per message (actual)

## HIPAA and Patient Data Compliance

**What Gupshup does:**
- Ensure messages don't include full patient medical history (only necessary data: appointment time, medication name, test result name)
- Audit templates for PII exposure (SSN, full medical records)
- Support transactional messages for appointments, billing, follow-ups (no consent needed)

**What you own:**
- Patient consent records (for marketing campaigns)
- Data retention policies

## Gupshup Healthcare Starter

**Included:**
- 15 pre-built, compliance-audited templates
- Multi-clinic billing setup
- HIPAA compliance audit
- Dedicated healthcare-focused support

**Cost:** ₹2.5K/month + per-clinic add-ons (₹13.80/clinic) + message actuals

**ROI:** Typical multi-clinic practice reports 25% reduction in no-show rate, 10+ hours saved per month on billing
