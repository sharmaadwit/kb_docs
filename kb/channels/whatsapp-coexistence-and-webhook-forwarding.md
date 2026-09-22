# WhatsApp Coexistence and Webhook Forwarding

**Module**: Channels

## Definition

WhatsApp Coexistence allows businesses to maintain their existing Meta app connection to a WhatsApp Business Account (WABA) while also connecting the same WABA to Gupshup. This enables organizations to continue receiving webhooks in their existing CRM systems while leveraging Gupshup's platform for advanced messaging features.

Webhook Forwarding in Gupshup refers to the capability to forward incoming WhatsApp messages and events to customer-defined webhook URLs, preserving the original Meta Cloud API payload format.

## Procedure

### Prerequisites for Coexistence
- Eligible WhatsApp Business Account with proper ownership verification
- Existing Meta app with valid credentials and webhook configuration
- Technical contact with access to both Meta developer console and Gupshup Console

### Enabling Coexistence
1. Contact Gupshup Support or your account representative before onboarding
2. Provide your existing WABA ID and Meta app details for verification
3. Gupshup team will coordinate with Meta to enable multi-app access to your WABA
4. Complete standard Gupshup WhatsApp Business API onboarding process

### Configuring Webhook Forwarding
1. Navigate to **Channels** → **WhatsApp Business API** → **Webhook Settings**
2. Enable "Webhook Forwarding" toggle
3. Enter your webhook URL where you want to receive forwarded messages
4. Optionally configure authentication headers if your webhook requires them
5. Save configuration

### Validation
- Test webhook forwarding by sending a message to your WhatsApp number
- Verify receipt of the forwarded webhook at your endpoint
- Confirm payload format matches Meta Cloud API specifications

## Field Mapping / Schemas

### Webhook Forwarding Payload Format
Forwarded webhooks maintain the original Meta Cloud API format:
```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
    "changes": [{
      "value": {
        "messaging_product": "whatsapp",
        "metadata": {
          "display_phone_number": "PHONE_NUMBER",
          "phone_number_id": "PHONE_NUMBER_ID"
        },
        "contacts": [{
          "profile": {
            "name": "NAME"
          },
          "wa_id": "PHONE_NUMBER"
        }],
        "messages": [{
          "from": "PHONE_NUMBER",
          "id": "MESSAGE_ID",
          "timestamp": "TIMESTAMP",
          "text": {
            "body": "MESSAGE_CONTENT"
          },
          "type": "text"
        }]
      },
      "field": "messages"
    }]
  }]
}
```

## Options / Variants

### Coexistence Models
1. **Read-only Coexistence**: Gupshup connects to WABA in read-only mode, preventing conflicting operations
2. **Shared Ownership**: Gupshup and existing Meta app share control with conflict prevention mechanisms

### Webhook Forwarding Filters
- Forward all events (messages, statuses, etc.)
- Filter by event type (messages only, statuses only)
- Filter by message direction (inbound only, outbound delivery receipts)

## Troubleshooting

### Common Coexistence Issues

#### Error: "Could not verify your information" during onboarding
**Cause**: WABA ownership validation failed
**Solution**: 
1. Verify your business has admin access to the WABA in Meta Business Manager
2. Confirm the WABA ID is correct
3. Contact Gupshup Support with WABA ID and business verification details

#### Error: "Could not share WhatsApp Business Account with partners"
**Cause**: Multi-app access not enabled for the WABA
**Solution**: Contact Gupshup Support to request coexistence setup - this requires manual Meta approval

### Webhook Forwarding Issues

#### No webhooks received at custom endpoint
**Cause**: Incorrect URL or connectivity issues
**Solution**:
1. Verify webhook URL is accessible from public internet
2. Check URL format (must be HTTPS)
3. Review authentication settings if using headers
4. Check Gupshup Console webhook logs for delivery errors

#### Mismatched payload format
**Cause**: Misconfiguration expecting Gupshup format instead of Meta Cloud API
**Solution**: Ensure webhook consumers are expecting standard Meta Cloud API format

## Cross-module Workflow

### With Bot Studio
When using coexistence with Bot Studio journeys:
- Incoming messages are processed by both your existing system and Gupshup bots
- Careful design is needed to avoid duplicate responses

### With Campaign Manager
Campaign messages sent through Gupshup do not interfere with existing Meta app operations
Delivery receipts are forwarded to both systems if webhook forwarding is enabled

## Related Documentation

- [WhatsApp Business API Setup](./whatsapp-business-api.md)
- [Webhook and Event Callbacks](../integrations/webhooks.md)
- [Partner Program Overview](../reseller-and-partner-programs/partner-program-overview.md)