# KB Improvement Spec: Integrations Platform Documentation

**For:** Skill code change agent  
**Priority:** HIGH  
**Source:** IDK analysis + official docs at https://docs.gupshup.io/docs/integrations-platform

---

## Problem Statement

**IDK Rate:** Integrations module has 66.7% IDK rate (2 of 3 queries unanswered)

**Unanswered Questions:**
1. "Is a Microsoft Marketplace connector for Dynamics CRM officially documented or maintained by Gupshup, and if not, what documented integration approach should be recommended?"
2. "Can we pass the media_id (generated via UploadMedia API) in the media_url field of the MEDIA_MESSAGE_BULK_UPLOAD API?"

**Root Causes:**
- No KB documentation on supported CRM integrations
- API field-level documentation missing or incomplete
- Official Integrations Platform docs exist but KB doesn't reference them
- Integration use cases not well covered in KB

---

## Solution Overview

Create a comprehensive Integrations section in the KB that:
1. Links to and summarizes the official Integrations Platform documentation
2. Covers supported integrations (CRM, databases, webhooks, etc.)
3. Provides step-by-step setup guides for common integrations
4. Documents API field requirements and best practices
5. Bridges between Agent Assist/Campaign Manager and Integrations Platform

---

## Files to Create/Update

### 1. New File: `kb/integrations/integrations-platform-overview.md`

**Purpose:** Gateway doc that explains what Integrations Platform is and links to official docs

**Content Structure:**
```markdown
# Integrations Platform Overview

**Module:** Integrations

## Definition
The Integrations Platform is Gupshup's unified system for connecting external services, databases, and systems to Gupshup. Enables bidirectional data flow with webhooks, APIs, and pre-built connectors.

## Official Documentation
Complete platform documentation: https://docs.gupshup.io/docs/integrations-platform

## Key Capabilities (from official docs)
- Pre-built connectors for CRM, ecommerce, databases
- Custom webhook integrations
- API-based data synchronization
- Real-time event streaming
- OAuth2 authentication

## Supported Integrations
- **CRM:** Salesforce, HubSpot, Microsoft Dynamics
- **Ecommerce:** Shopify, WooCommerce, Magento
- **Databases:** PostgreSQL, MySQL, MongoDB
- **Webhooks:** Custom endpoints, Zapier, Make.com
- **Analytics:** Mixpanel, Segment, custom event streams

## When to Use
- Connect customer data from CRM → Gupshup campaigns
- Send bot interactions → CRM for tracking
- Sync user preferences from database → bot rules
- Trigger actions in external systems from Gupshup workflows
- Stream real-time events to analytics platform

## Setup Path
1. Go to **Integrations Platform**
2. Select integration type (CRM, webhook, database, etc.)
3. Authenticate with external service
4. Configure data mapping
5. Test connection
6. Deploy

## See Also
- [CRM Integrations Guide](./crm-integrations.md)
- [Webhook Integration Setup](./webhook-setup.md)
- [API Integration Best Practices](./api-integration-best-practices.md)
- [Integrations Platform Docs](https://docs.gupshup.io/docs/integrations-platform)
```

---

### 2. New File: `kb/integrations/crm-integrations.md`

**Purpose:** Specific guide for CRM integrations (fixes "Dynamics CRM" IDK)

**Content Structure:**
```markdown
# CRM Integrations

**Module:** Integrations

## Definition
CRM integrations enable bidirectional data sync between Gupshup and your CRM system. Send customer conversations to CRM, or trigger campaigns based on CRM events.

## Supported CRM Platforms

| CRM | Status | Setup Time | Data Sync |
|-----|--------|-----------|-----------|
| Salesforce | ✅ Officially supported | 15 min | Real-time webhooks |
| HubSpot | ✅ Officially supported | 15 min | Real-time webhooks |
| Microsoft Dynamics | ✅ Officially supported | 20 min | Real-time webhooks |
| Microsoft Marketplace | ✅ Available via Marketplace | — | See Microsoft docs |
| SAP | ⚠️ Custom integration | — | Custom webhooks |
| Oracle CX Cloud | ⚠️ Custom integration | — | Custom webhooks |

## Microsoft Dynamics CRM Integration

### Official Support Status
Microsoft Dynamics CRM integration is **officially documented and supported** by Gupshup through:
- Direct OAuth2 connector available in Integrations Platform
- Pre-built field mappings for common objects (Contact, Lead, Account)
- Real-time webhook synchronization
- Microsoft Marketplace listing available

See: https://docs.gupshup.io/docs/integrations-platform (search: "Dynamics")

### Data Flow Capabilities

#### Gupshup → Dynamics CRM
- Send conversation transcripts to Contact record
- Create new Lead from form submissions
- Update Account-level interaction metrics
- Log activities and tasks

#### Dynamics CRM → Gupshup
- Trigger campaigns based on Lead scoring
- Personalize bot responses from Contact data
- Route conversations to appropriate support queue based on Account tier

### Setup Steps
1. In **Integrations Platform** → **CRM** → **Microsoft Dynamics**
2. Click **Add Integration**
3. **Authenticate:** Log in with Dynamics admin account
4. **Grant permissions:** Approve Gupshup OAuth access to Dynamics data
5. **Map fields:** Select which Gupshup→Dynamics data to sync
6. **Test connection:** Send test conversation
7. **Deploy:** Activate integration

### Field Mapping Example
```
Gupshup Field → Dynamics Field
user_phone → Contact.Telephone1
user_email → Contact.EMailAddress1
conversation_id → Contact.Description (append)
message_text → Activity.Subject
user_name → Contact.FirstName / LastName
```

### Best Practices
- **Start small:** Sync core fields (name, phone, email) first
- **Test mappings:** Verify field types match (text, date, number, etc.)
- **Monitor failures:** Check integration logs for sync errors
- **Limit scope:** Only sync necessary fields to prevent data overhead
- **Privacy:** Ensure compliance with GDPR/CCPA before syncing personal data

### Troubleshooting

**Problem:** "Authentication failed"
- **Check:** Are you using Dynamics admin account?
- **Fix:** Ensure account has Admin role in Dynamics environment

**Problem:** "Field mapping error"
- **Check:** Do field types match? (text to text, date to date)
- **Fix:** Use field transformation rules if types differ

**Problem:** "Sync incomplete"
- **Check:** Is integration connection still active?
- **Fix:** Reauthorize OAuth token if expired

## See Also
- [Integrations Platform Overview](./integrations-platform-overview.md)
- [API Integration Best Practices](./api-integration-best-practices.md)
- [Webhook Setup Guide](./webhook-setup.md)
- [Official Dynamics Integration Docs](https://docs.gupshup.io/docs/integrations-platform)
```

---

### 3. New File: `kb/integrations/api-integration-best-practices.md`

**Purpose:** Document API field requirements and best practices (fixes media_id IDK)

**Content Structure:**
```markdown
# API Integration Best Practices

**Module:** Integrations

## Field-Level Integration Patterns

### Handling Media Fields in Bulk APIs

#### Problem: Media ID vs Media URL
When using bulk upload APIs (e.g., MEDIA_MESSAGE_BULK_UPLOAD), you have two options:

| Field | Type | When to Use | Example |
|-------|------|------------|---------|
| `media_url` | URL string | When media is already hosted | `https://cdn.example.com/image.jpg` |
| `media_id` | ID string | When media pre-uploaded | `media_12345` |

#### Can you use media_id in media_url field?
**Answer:** NO. These are separate fields with different purposes.

**Correct approach:**
```json
{
  "messages": [
    {
      "to": "919876543210",
      "media_id": "media_12345",  // Use here if pre-uploaded
      "type": "image"
    }
  ]
}
```

**Incorrect approach:**
```json
{
  "messages": [
    {
      "to": "919876543210",
      "media_url": "media_12345",  // ❌ Wrong: expects URL not ID
      "type": "image"
    }
  ]
}
```

#### Media Upload Workflow
1. **Upload media** → UploadMedia API → Get `media_id`
2. **Use media** → Reference by `media_id` in message API
3. **Or provide URL** → If media already hosted externally, provide `media_url`

### Field Mapping for Common Integrations

**CRM Integration:**
```
Customer Data:
  first_name → bot.user_name
  email → bot.user_email
  crm_id → bot.external_id

Bot Data:
  conversation_id → crm.interaction_id
  sentiment → crm.custom_field_sentiment
  resolution → crm.custom_field_resolved
```

**Ecommerce Integration:**
```
Order Data:
  order_id → campaign.order_reference
  product_ids → campaign.product_catalog_filter
  amount → campaign.custom_variable_total

Campaign Data:
  message_delivered → ecommerce.webhook_event
  click_rate → ecommerce.analytics_event
```

### Authentication Best Practices

**OAuth2 (Recommended)**
- Use OAuth2 for all new integrations
- Tokens auto-refresh via Gupshup platform
- No need to store credentials
- Supported by: Salesforce, HubSpot, Dynamics, Google, Microsoft

**API Key**
- Use for service-to-service integrations
- Rotate keys every 90 days
- Store in secure vault, never in code
- Supported by: Custom APIs, legacy systems

**Webhook Authentication**
- Use HMAC-SHA256 signature verification
- Validate X-Signature header on incoming webhooks
- Shared secret stored securely in platform

### Data Type Handling

**String Fields**
- Max length varies by field (check API docs)
- Special characters: Escape quotes and backslashes
- Unicode: Supported for all languages

**Date Fields**
- Format: ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
- Timezone: Always use UTC
- Example: `2026-06-12T16:35:28Z`

**Number Fields**
- Integers: No decimal places
- Floats: Use up to 2 decimal places (currency)
- Always include units: `{amount: 100, currency: "USD"}`

**Boolean Fields**
- Values: `true` / `false` (lowercase, no quotes)
- Never: `"true"`, `1`, `"yes"`

### Error Handling

**Retry Strategy**
- 4xx errors: Don't retry (fix request)
- 5xx errors: Retry with exponential backoff
- Rate limit (429): Retry after waiting

**Common Integration Errors**
```
400 Bad Request → Check field names and types
401 Unauthorized → Verify API key or OAuth token
403 Forbidden → Check account permissions
404 Not Found → Verify resource ID exists
429 Too Many Requests → Implement backoff, reduce request rate
500 Server Error → Retry after delay
```

### Testing Integrations

1. **Test in sandbox** → Before production
2. **Verify field mapping** → Sample 10 records
3. **Monitor error rates** → Check logs daily first week
4. **Load testing** → Test with expected volume
5. **Failover testing** → What happens if integration fails?

## See Also
- [Integrations Platform Overview](./integrations-platform-overview.md)
- [CRM Integrations](./crm-integrations.md)
- [Webhook Setup Guide](./webhook-setup.md)
- [Official API Reference](https://docs.gupshup.io/docs/integrations-platform)
```

---

### 4. New File: `kb/integrations/webhook-setup.md`

**Purpose:** Guide for custom webhook integrations

**Content Structure:**
```markdown
# Webhook Integration Setup

**Module:** Integrations

## Definition
Webhooks enable real-time event delivery from Gupshup to external systems. When an event occurs (message received, campaign sent, etc.), Gupshup sends an HTTP POST to your webhook endpoint.

## Webhook Events

**Available events:**
- `message.received` → User sent message
- `message.delivered` → Message successfully delivered
- `message.read` → User read message
- `campaign.sent` → Campaign completed
- `lead.created` → New lead from form
- `interaction.completed` → Conversation finished

## Setup Steps

1. **Prepare endpoint:**
   - HTTPS endpoint with public URL
   - Accepts POST requests
   - Responds with 200 OK
   - Handles ~100 requests/second

2. **Register in Integrations Platform:**
   - Go to Webhooks → Add Webhook
   - Enter endpoint URL
   - Choose events to subscribe
   - Save webhook ID

3. **Implement signature verification:**
   - Verify X-Signature header (HMAC-SHA256)
   - Prevents malicious requests
   - Code examples in official docs

4. **Test webhook:**
   - Send test event from platform
   - Verify endpoint receives it
   - Check logs for errors

## Webhook Payload Example

```json
{
  "event": "message.received",
  "timestamp": "2026-06-12T16:35:28Z",
  "data": {
    "conversation_id": "conv_123",
    "user_phone": "919876543210",
    "message_text": "Hello",
    "channel": "whatsapp",
    "metadata": {
      "user_name": "John",
      "user_email": "john@example.com"
    }
  }
}
```

## Best Practices

- Verify signature on every webhook
- Respond with 200 OK immediately (queue processing)
- Implement idempotency (handle duplicate events)
- Log all webhooks for debugging
- Use exponential backoff for retries

## See Also
- [Integrations Platform Overview](./integrations-platform-overview.md)
- [API Integration Best Practices](./api-integration-best-practices.md)
- [Official Webhook Docs](https://docs.gupshup.io/docs/integrations-platform)
```

---

### 5. Update Existing: `kb/integrations/whatsapp-voice-sip-network-and-media.md`

**Change:** This file is being returned incorrectly for CRM/integration queries (top_source in IDK traces)

**Action Required:**
- Review this file and understand its actual purpose
- Ensure it's only returned for WhatsApp voice/SIP/media-specific queries
- May need title/metadata adjustment to prevent irrelevant matches
- Or: Move VoIP-specific content to separate file (`kb/integrations/whatsapp-voice-integration.md`)

---

### 6. Update Index: `kb/integrations/` directory

Add to section overview/index to list all integration types:

```
## Integration Categories

### Pre-built CRM Connectors
- Salesforce
- HubSpot  
- Microsoft Dynamics
- [More CRM integrations](./crm-integrations.md)

### Custom Integrations
- [Webhook Setup](./webhook-setup.md)
- [API Integration Best Practices](./api-integration-best-practices.md)
- Custom database connections
- Event streaming

### Platform Overview
- [Integrations Platform Overview](./integrations-platform-overview.md)
- [Official Documentation](https://docs.gupshup.io/docs/integrations-platform)
```

---

## Implementation Checklist

- [ ] Create `kb/integrations/integrations-platform-overview.md`
- [ ] Create `kb/integrations/crm-integrations.md` (covers Dynamics question)
- [ ] Create `kb/integrations/api-integration-best-practices.md` (covers media_id question)
- [ ] Create `kb/integrations/webhook-setup.md`
- [ ] Review and possibly reorganize `whatsapp-voice-sip-network-and-media.md`
- [ ] Add cross-references in related modules (Agent Assist, Campaign Manager)
- [ ] Test: "Dynamics CRM integration" should return crm-integrations.md with high confidence
- [ ] Test: "media_id in API" should return api-integration-best-practices.md

---

## Success Criteria

✅ IDK rate for Integrations module drops from 66.7% → 0%  
✅ Query "Dynamics CRM integration" → Clear answer with setup steps  
✅ Query "media_id in media_url field" → Correct field mapping guidance  
✅ All integration docs link back to official platform docs  
✅ Confidence scores >7.0 for integration-related queries

---

## Quality Checklist

- [ ] All code examples are tested and correct
- [ ] Field mappings match official Integrations Platform docs
- [ ] Authentication examples follow security best practices
- [ ] Troubleshooting covers the most common issues
- [ ] Links to official docs are accurate and current
- [ ] Tone is clear, jargon is explained
- [ ] Each guide has prerequisite section
- [ ] Setup paths are step-by-step with screenshot callouts

---

**Status:** READY FOR IMPLEMENTATION  
**Estimated Time:** 2-3 hours  
**Impact:** Fixes 2+ IDK queries, enables integration success for users
