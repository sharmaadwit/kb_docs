source_url: https://docs.gupshup.io/docs/integrations-platform

<!-- kb-golden:v10 -->
# Integrations Platform Overview

**Module**: Integrations

## Definition

The Integrations Platform is Gupshup's unified system for connecting external services, databases, and systems to Gupshup. It enables bidirectional data flow with webhooks, APIs, and pre-built connectors for seamless integration with your existing business systems.

## Official Documentation

Complete platform documentation: https://docs.gupshup.io/docs/integrations-platform

## Key Capabilities

- **Pre-built connectors** for CRM, ecommerce, databases
- **Custom webhook integrations** for real-time event delivery
- **API-based data synchronization** for programmatic control
- **Real-time event streaming** to analytics platforms
- **OAuth2 authentication** for secure, credential-less integration
- **Field mapping** for automatic data transformation

## Supported Integrations

### CRM Platforms
- Salesforce
- HubSpot
- Microsoft Dynamics
- SAP (custom integration)
- Oracle CX Cloud (custom integration)

### Ecommerce Platforms
- Shopify
- WooCommerce
- Magento

### Databases
- PostgreSQL
- MySQL
- MongoDB

### External Services
- Webhooks (custom endpoints)
- Zapier
- Make.com (formerly Integromat)
- Segment
- Mixpanel

## When to Use

Use Integrations Platform when you need to:

- **Connect customer data** from CRM → Gupshup campaigns
- **Send bot interactions** → CRM for tracking and analytics
- **Sync user preferences** from database → bot rules
- **Trigger actions** in external systems from Gupshup workflows
- **Stream real-time events** to analytics platforms
- **Receive webhooks** from third-party systems
- **Automate data sync** between systems

## Setup Path

### Quick Setup (Pre-built Connector)

1. Go to **Integrations Platform**
2. Select integration type (CRM, webhook, database, etc.)
3. Authenticate with external service
4. Configure data mapping
5. Test connection
6. Deploy and monitor

### Custom Webhook Setup

1. Prepare HTTPS endpoint
2. Register webhook URL in platform
3. Choose events to subscribe
4. Implement signature verification
5. Test and deploy

## Common Use Cases

### Lead Qualification
Connect Salesforce → Gupshup to auto-send bot qualification flows when new leads are created, then send responses back to Salesforce for lead scoring.

### Order Tracking
Connect Shopify → Gupshup to automatically send order updates via WhatsApp/RCS when status changes, with real-time tracking links.

### Support Escalation
Connect Zendesk → Gupshup to route escalated conversations to support queue, then update ticket status when conversation completes.

### Campaign Personalization
Connect HubSpot → Gupshup to pull contact data for campaign personalization, then sync click/conversion metrics back to HubSpot.

## Integration Architecture

```
External System
      ↓
  [OAuth2/API Key]
      ↓
Integrations Platform (Gupshup)
      ↓
  [Field Mapping]
      ↓
Bot Studio / Campaign Manager / Agent Assist
      ↓
  [Webhooks / APIs]
      ↓
External System (events/updates)
```

## Data Security

- **Encryption:** All data in transit uses HTTPS/TLS
- **Authentication:** OAuth2 or API keys (no passwords stored)
- **Permissions:** Granular scopes for each integration
- **Audit logs:** All data sync events logged
- **Compliance:** GDPR, CCPA, HIPAA ready

## Related Guides

- [CRM Integrations](./crm-integrations.md) - Setup guides for Salesforce, HubSpot, Dynamics
- [Webhook Setup](./webhook-setup.md) - Real-time event delivery to external systems
- [API Integration Best Practices](./api-integration-best-practices.md) - Field mapping, authentication, error handling

## Reference (from source)

<!-- procedural:v2 -->
# Integrations Platform Overview

Gupshup's unified integration system for connecting CRM, databases, webhooks, and external services with real-time data sync.
