source_url: https://docs.gupshup.io/docs/integrations-platform

<!-- kb-golden:v10 -->
# API Integration Best Practices

**Module**: Integrations

## Field-Level Integration Patterns

### Handling Media Fields in Bulk APIs

#### Problem: Media ID vs Media URL

When using bulk upload APIs (e.g., MEDIA_MESSAGE_BULK_UPLOAD), you have two options for specifying media:

| Field | Type | When to Use | Example |
|-------|------|------------|---------|
| `media_url` | URL string | When media is already hosted | `https://cdn.example.com/image.jpg` |
| `media_id` | ID string | When media pre-uploaded | `media_12345` |

#### Can You Use media_id in the media_url Field?

**Answer: NO** ❌

`media_id` and `media_url` are **separate fields** with **different purposes**:
- `media_url` expects a full HTTP/HTTPS URL pointing to the media file
- `media_id` expects the ID returned from a previous UploadMedia API call

Using a media_id value in the media_url field will result in a 400 Bad Request error.

#### Correct Media Upload Workflow

1. **Step 1: Upload media** 
   ```
   POST /api/v1/media/upload
   Response: { "media_id": "media_12345", ... }
   ```

2. **Step 2: Reference by ID in bulk message**
   ```json
   {
     "messages": [
       {
         "to": "919876543210",
         "media_id": "media_12345",  // ✅ Use the ID here
         "type": "image"
       }
     ]
   }
   ```

Or if media is already hosted externally:

```json
{
  "messages": [
    {
      "to": "919876543210",
      "media_url": "https://cdn.example.com/image.jpg",  // ✅ Use full URL
      "type": "image"
    }
  ]
}
```

**Incorrect (will fail):**
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

#### When to Use Each Approach

**Use `media_id` when:**
- You're uploading media via UploadMedia API first
- You want to reuse the same media across multiple messages
- You're building messages programmatically
- You need guaranteed media availability

**Use `media_url` when:**
- Media is already hosted on a CDN or external server
- You're building messages dynamically with external URLs
- You don't want to manage media uploads
- URL is temporary or request-specific

## Field Mapping for Common Integrations

### CRM Integration Field Mapping

**Customer Data (CRM → Gupshup Bot):**
```
CRM Field → Bot Variable
Contact.FirstName → {user_first_name}
Contact.Email → {user_email}
Contact.Phone → {user_phone}
Account.Name → {company_name}
Opportunity.Amount → {deal_value}
Lead.LeadSource → {source}
```

**Bot Data (Gupshup → CRM):**
```
Bot Field → CRM Field
conversation_id → Contact.Description (append)
sentiment_score → Contact.custom_field_sentiment
resolution_status → Contact.custom_field_resolved
chat_duration → Contact.custom_field_duration_sec
user_intent → Lead.custom_field_intent
```

### Ecommerce Integration Field Mapping

**Order Data (Ecommerce → Gupshup Campaign):**
```
Order Field → Campaign Variable
order_id → {order_reference}
product_ids → {product_catalog_filter}
order_total → {custom_variable_total}
customer_email → {recipient_email}
order_status → {campaign_trigger}
```

**Campaign Data (Gupshup → Ecommerce):**
```
Campaign Event → Ecommerce Event
message_delivered → order.webhook_event_delivered
link_clicked → order.webhook_event_clicked
conversion_completed → order.webhook_event_conversion
user_replied → order.webhook_event_replied
```

## Authentication Best Practices

### OAuth2 (Recommended for New Integrations)

**Advantages:**
- Auto token refresh via Gupshup platform
- No need to store credentials
- User-initiated authorization (more secure)
- Supported by most modern APIs

**How it works:**
```
1. User clicks "Connect to Salesforce"
2. Redirected to Salesforce login
3. User approves permission scopes
4. Salesforce returns authorization code
5. Gupshup exchanges code for access token
6. Token auto-refreshes when expired
```

**Supported platforms:**
- Salesforce
- HubSpot
- Microsoft Dynamics
- Google Workspace
- Microsoft 365

### API Key Authentication

**When to use:**
- Service-to-service integrations
- Legacy systems without OAuth2
- Internal company APIs

**Best practices:**
- Rotate keys every 90 days
- Store in secure vault (never in code)
- Use separate keys for staging/production
- Revoke immediately if compromised
- Monitor key usage in logs

**Example:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.example.com/v1/data
```

### Webhook Authentication (HMAC-SHA256)

**How it works:**
1. Gupshup sends webhook with `X-Signature` header
2. Signature = HMAC-SHA256(payload, secret)
3. Your endpoint verifies signature
4. Prevents unauthorized webhook calls

**Verification pseudocode:**
```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected_sig = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected_sig)
```

## Data Type Handling

### String Fields

**Rules:**
- Max length varies by field (check API docs)
- Special characters: Escape quotes and backslashes
- Unicode: Supported for all languages (UTF-8)
- Whitespace: Trimmed automatically in most fields

**Examples:**
```
Valid:   "John O'Brien"
Valid:   "東京, Japan"
Invalid: "John \"Johnny\" Doe"  (needs escaping: "John \\"Johnny\\" Doe")
```

### Date Fields

**Format:** ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)

**Rules:**
- Always use UTC timezone (append Z)
- Timezone offset: Not recommended (use UTC)
- Timezone abbreviations: Never (BST, EST, etc. are ambiguous)

**Valid examples:**
```
2026-06-12T16:35:28Z       ✅ Correct
2026-06-12T16:35:28+00:00  ✅ Also correct (UTC offset)
2026-06-12T16:35:28        ❌ Missing timezone
2026-06-12T16:35:28-05:00  ⚠️ Not UTC (avoid)
```

### Number Fields

**Integers:**
```json
{
  "count": 42,        // ✅ No decimal places
  "count": 42.0,      // ❌ Should be integer
  "count": "42"       // ❌ Should be number not string
}
```

**Floats (Currency):**
```json
{
  "amount": 99.99,      // ✅ Up to 2 decimal places
  "amount": 99.999,     // ⚠️ Rounds to 99.99
  "currency": "USD"     // ✅ Always include currency
}
```

### Boolean Fields

**Valid values:**
```json
{
  "is_active": true,    // ✅ Correct
  "is_active": false,   // ✅ Correct
  "is_active": "true",  // ❌ String not boolean
  "is_active": 1,       // ❌ Number not boolean
  "is_active": "yes"    // ❌ String not boolean
}
```

## Error Handling

### Retry Strategy

**4xx Client Errors:** Don't retry
- 400 Bad Request → Fix request format
- 401 Unauthorized → Check credentials
- 403 Forbidden → Check permissions
- 404 Not Found → Verify resource exists

**5xx Server Errors:** Retry with exponential backoff
- 500 Internal Server Error → Retry after 1-2 seconds
- 502 Bad Gateway → Retry after 2-4 seconds
- 503 Service Unavailable → Retry after 4-8 seconds

**429 Rate Limit:** Respect backoff header
```
Retry-After: 60  (wait 60 seconds before retry)
```

### Common Integration Error Reference

```
Error Code | Cause | Solution
-----------|-------|----------
400        | Invalid field format | Check field names, types, required fields
401        | Invalid credentials | Verify API key, OAuth token, or basic auth
403        | Insufficient permissions | Check API key scopes, user role
404        | Resource not found | Verify ID, endpoint, URL spelling
409        | Conflict (duplicate) | Check for existing record, use idempotency key
429        | Rate limit exceeded | Implement backoff, reduce request frequency
500        | Server error | Retry after delay, contact support if persistent
502        | Gateway error | Retry after delay, check service status
503        | Service unavailable | Retry after delay, check maintenance status
```

## Testing Integrations

### Pre-Deployment Testing Checklist

1. **Test in Sandbox Environment**
   - Create test account in external system
   - Configure integration with sandbox credentials
   - Verify all features work in isolated environment

2. **Verify Field Mapping**
   - Sample 10 records from source system
   - Check that all fields map correctly
   - Verify data types (text, date, number) match
   - Test special characters and Unicode

3. **Monitor Error Rates**
   - Check logs daily for first week
   - Alert on error rate >5%
   - Review failed records and fix issues
   - Document any patterns

4. **Load Testing**
   - Test with expected message volume
   - Monitor latency and error rates
   - Check rate limit headers
   - Implement backoff if needed

5. **Failover Testing**
   - What happens if integration fails?
   - Does sync pause or continue?
   - Are errors logged?
   - Can you resume manually?

## See Also

- [Integrations Platform Overview](./integrations-platform-overview.md)
- [CRM Integrations](./crm-integrations.md)
- [Webhook Setup Guide](./webhook-setup.md)
- [Official API Reference](https://docs.gupshup.io/docs/integrations-platform)

## Reference (from source)

<!-- procedural:v2 -->
# API Integration Best Practices

Field mapping, authentication, data types, error handling, and testing for API integrations.
