source_url: https://docs.gupshup.io/docs/integrations-platform

<!-- kb-golden:v10 -->
# CRM Integrations

**Module**: Integrations

## Definition

CRM integrations enable bidirectional data sync between Gupshup and your CRM system. Send customer conversations to CRM, trigger campaigns based on CRM events, and personalize bot responses using CRM data.

## Supported CRM Platforms

| CRM | Status | Setup Time | Data Sync | Support |
|-----|--------|-----------|-----------|---------|
| Salesforce | ✅ Officially supported | 15 min | Real-time webhooks | OAuth2 |
| HubSpot | ✅ Officially supported | 15 min | Real-time webhooks | OAuth2 |
| Microsoft Dynamics | ✅ Officially supported | 20 min | Real-time webhooks | OAuth2 |
| Microsoft Marketplace | ✅ Available via Marketplace | — | Real-time webhooks | Certified connector |
| SAP | ⚠️ Custom integration | — | Custom webhooks | API-based |
| Oracle CX Cloud | ⚠️ Custom integration | — | Custom webhooks | API-based |

## Microsoft Dynamics CRM Integration

### Official Support Status

Microsoft Dynamics CRM integration is **officially documented and supported** by Gupshup through:
- Direct OAuth2 connector available in Integrations Platform
- Pre-built field mappings for common objects (Contact, Lead, Account)
- Real-time webhook synchronization
- Microsoft Marketplace certified connector available

See official docs: https://docs.gupshup.io/docs/integrations-platform

### Data Flow Capabilities

#### Gupshup → Dynamics CRM
- Send conversation transcripts to Contact record
- Create new Lead from form submissions
- Update Account-level interaction metrics
- Log activities and tasks
- Update custom fields with bot responses

#### Dynamics CRM → Gupshup
- Trigger campaigns based on Lead scoring
- Personalize bot responses from Contact data
- Route conversations to appropriate support queue based on Account tier
- Filter audience based on CRM field values

### Setup Steps

1. **Go to Integrations Platform**
   - Console → Integrations → CRM → Microsoft Dynamics
   - Click "Add Integration"

2. **Authenticate with Dynamics**
   - Click "Authenticate"
   - Log in with Dynamics admin account
   - Approve Gupshup OAuth access to Dynamics data

3. **Configure Integration**
   - Select Dynamics environment (Production/Sandbox)
   - Choose objects to sync (Contact, Lead, Account)
   - Define field mappings

4. **Map Fields**
   - Gupshup field → Dynamics field (see examples below)
   - Select sync direction (one-way or bidirectional)
   - Test with sample data

5. **Test Connection**
   - Send test conversation
   - Verify data appears in Dynamics
   - Check error logs if issues occur

6. **Deploy**
   - Enable integration
   - Set up webhook endpoints
   - Monitor sync health

### Field Mapping Examples

**Contact Object:**
```
Gupshup Field → Dynamics Field
user_phone → Telephone1
user_email → EMailAddress1
user_name → FirstName / LastName
user_company → CompanyName
conversation_id → Description (append)
```

**Lead Object:**
```
Gupshup Field → Dynamics Field
form_name → LeadSource
form_submitted_at → CreatedOn
form_data → Description
lead_rating → Rating
```

**Activity Object (for logging conversations):**
```
Gupshup Field → Dynamics Field
message_text → Subject
conversation_date → ActualStart
user_name → Owner
message_type → ActivityTypeCode
```

### Best Practices

1. **Start small:** Sync core fields (name, phone, email) first, then expand
2. **Test mappings:** Verify field types match (text→text, date→date, number→number)
3. **Monitor failures:** Check integration logs daily for sync errors
4. **Limit scope:** Only sync necessary fields to reduce data overhead and complexity
5. **Privacy:** Ensure compliance with GDPR/CCPA before syncing personal data
6. **Backup:** Export critical data before enabling sync
7. **Use bidirectional selectively:** Avoid circular updates; clearly define sync direction

### Troubleshooting

**Problem: "Authentication failed"**
- **Check:** Are you using a Dynamics admin account?
- **Solution:** Ensure account has Admin role in target Dynamics environment
- **Verify:** Check that OAuth app registration has correct permissions

**Problem: "Field mapping error"**
- **Check:** Do field types match? (Text field can't map to DateTime)
- **Solution:** Use field transformation rules if types differ
- **Verify:** Test mapping with sample record first

**Problem: "Sync incomplete or stopped"**
- **Check:** Is integration connection still active?
- **Solution:** Reauthorize OAuth token if expired (usually 90 days)
- **Verify:** Check that webhook endpoint is accessible (HTTPS, public URL)

**Problem: "Data not appearing in Dynamics"**
- **Check:** Is the field writable in Dynamics? (Some system fields are read-only)
- **Solution:** Test manually creating record in Dynamics with mapped field
- **Verify:** Check audit logs in both systems for errors

## Salesforce Integration

### Quick Setup
1. Integrations Platform → CRM → Salesforce
2. Authenticate with Salesforce admin account
3. Map Account/Contact/Lead fields
4. Test with sample data
5. Deploy

### Supported Objects
- Account
- Contact  
- Lead
- Opportunity
- Task/Activity

## HubSpot Integration

### Quick Setup
1. Integrations Platform → CRM → HubSpot
2. Authenticate with HubSpot admin account
3. Map Contact/Deal fields
4. Test with sample data
5. Deploy

### Supported Objects
- Contact
- Deal
- Company
- Activity/Note

## See Also

- [Integrations Platform Overview](./integrations-platform-overview.md)
- [API Integration Best Practices](./api-integration-best-practices.md)
- [Webhook Setup Guide](./webhook-setup.md)
- [Official Integrations Platform Docs](https://docs.gupshup.io/docs/integrations-platform)

## Reference (from source)

<!-- procedural:v2 -->
# CRM Integrations

Bidirectional sync between Gupshup and Salesforce, HubSpot, Microsoft Dynamics, and other CRM platforms.
