source_url: https://docs.gupshup.io/docs/webhooks-crm

<!-- kb-golden:v10 -->
# Webhook CRM Integration Patterns

**Module**: Integrations

## Definition

Real-time bidirectional sync between Gupshup and CRM systems via webhooks for lead capture, conversation tracking, and customer data sync.

## Pattern 1: CRM → Gupshup (Event-Triggered Bot)

**Use case:** When lead created in Salesforce, automatically send qualification bot in Gupshup

**Webhook payload from Salesforce:**
```json
{
  "event": "lead_created",
  "data": {
    "lead_id": "00Q1x00000IZ3FVEA",
    "email": "john@example.com",
    "phone": "14155552671",
    "first_name": "John",
    "company": "Acme Corp"
  }
}
```

**Gupshup receives webhook → Triggers journey:**
1. Parse phone number
2. Send first message: "Hi John! Let's qualify your needs"
3. Capture responses in journey variables
4. Send responses back to Salesforce (Pattern 2)

## Pattern 2: Gupshup → CRM (Conversation Data Sync)

**Use case:** When conversation ends, send transcript to CRM Contact record

**Gupshup sends webhook to Salesforce:**
```json
{
  "event": "conversation_complete",
  "data": {
    "contact_id": "003xx000003T7z",
    "messages": 5,
    "duration_seconds": 480,
    "sentiment": "positive",
    "key_intent": "interested",
    "transcript": "User showed interest in product..."
  }
}
```

**Salesforce receives → Updates Contact record:**
- Updates "Last Conversation" field
- Increments "Conversation Count"
- Sets "Last Intent" = "interested"
- Appends transcript to notes

## Field Mapping Examples

### Salesforce Contact ↔ Gupshup
```
Salesforce     → Gupshup Variable
FirstName      → {{first_name}}
Email          → {{user_email}}
Phone          → {{phone_number}}
Company        → {{company_name}}
LeadScore      → {{lead_score}}
custom_field   → {{custom_var}}
```

### HubSpot Contact ↔ Gupshup
```
HubSpot        → Gupshup Variable
firstname      → {{first_name}}
email          → {{user_email}}
phone          → {{phone_number}}
company        → {{company_name}}
lifecyclestage → {{lead_stage}}
```

### Microsoft Dynamics Contact ↔ Gupshup
```
Dynamics       → Gupshup Variable
firstname      → {{first_name}}
emailaddress1  → {{user_email}}
telephone1     → {{phone_number}}
companyname    → {{company_name}}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Webhook not received by CRM | Verify URL is HTTPS, check firewall allows Gupshup IPs |
| Data not syncing correctly | Verify field mapping, check field types match (text/date/number) |
| Authentication failed | Verify API key/OAuth token is current, check permissions |
| Payload too large | Reduce fields, compress data, send only essential fields |
| Webhook timing issues | Add delay before webhook call if data not ready |

## Testing

1. Set up webhook in Console
2. Send test payload via curl:
```bash
curl -X POST https://your-crm-webhook-url \
  -H "Content-Type: application/json" \
  -d '{"event":"test","data":{"id":"123"}}'
```
3. Check CRM received the data
4. Verify fields mapped correctly

## Reference (from source)

<!-- procedural:v2 -->
# Webhook CRM Integration Patterns

Real-time sync patterns for CRM → Gupshup triggers and Gupshup → CRM data push.
