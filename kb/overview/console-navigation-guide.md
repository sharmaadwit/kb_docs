source_url: https://docs.gupshup.io/docs/console-overview

<!-- kb-golden:v10 -->
# Console Navigation Guide

**Module**: Overview

## Definition

Quick reference for finding features, settings, and information in Gupshup Console.

## Finding Credentials

### API Keys
- **Path:** Console → Settings → API Keys
- **What you'll see:** List of API keys for authentication
- **Use for:** REST API calls, authentication

### Client ID & Client Secret
- **Path:** Console → Settings → OAuth Applications
- **What you'll see:** OAuth2 credentials for integration
- **Use for:** Third-party service integrations

### Webhooks Credentials
- **Path:** Console → Integrations → Webhooks → [Webhook Name]
- **What you'll see:** Webhook secret for signature verification
- **Use for:** HMAC-SHA256 signature verification

## Finding Metrics & Performance

### Delivery Rates
- **Path:** Console → Analytics → Messages
- **What you'll see:** Sent, delivered, failed message counts
- **Metrics:** Delivery %, time to delivery

### Performance (p95)
- **Path:** Console → Analytics → Performance
- **What you'll see:** p95, p99 response times
- **Use for:** Track API latency

### Message Status Dashboard
- **Path:** Console → Messages → Status
- **What you'll see:** Real-time message delivery status
- **Filter by:** Phone, date range, status

## Settings & Configuration

### Project Settings
- **Path:** Console → Settings → Project
- **Configure:** Project name, timezone, default language

### Channel Configuration
- **Path:** Console → Channels → [Channel Name]
- **Configure:** API keys, webhooks, rate limits

### Template Approval
- **Path:** Console → Templates
- **View:** Approval status, rejection reasons

## Quotas & Limits

### View Usage
- **Path:** Console → Settings → Usage & Quotas
- **See:** Current usage vs limits
- **Monitor:** WABA count, phone numbers, API calls

### Rate Limits
- **Path:** Console → Settings → Rate Limits
- **Configure:** Messages per second, API calls per minute

## Teams & Users

### User Management
- **Path:** Console → Settings → Users
- **Manage:** Add/remove team members
- **Set:** Roles and permissions

### Team Assignment
- **Path:** Console → Settings → Teams
- **Create:** Team groups
- **Assign:** Users to teams

## Navigation Tips

- **Quick search:** Press Cmd+K (Mac) or Ctrl+K (Windows) to search
- **Breadcrumbs:** Top of page shows current location
- **Sidebar collapse:** Click hamburger icon to expand/collapse menu
- **Back button:** Browser back button works throughout Console

## Reference (from source)

<!-- procedural:v2 -->
# Console Navigation Guide

Where to find credentials, metrics, settings, quotas, and configuration in Gupshup Console.
