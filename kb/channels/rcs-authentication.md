source_url: https://api.dotgo.com/rcs/auth

<!-- kb-golden:v10 -->
# RCS Authentication & Credentials

**Module**: Channels

## Definition

RCS API authentication uses OAuth2 with Client Credentials flow via Dotgo's Auth2 SSO service. After registering as an RCS agent, you receive a Client ID and Client Secret, which you use to obtain Bearer tokens for all API calls.

## Authentication Flow

### Step 1: Register RCS Agent

Complete RCS Agent Setup (see rcs-agent-setup.md). You'll receive:
- **Client ID** (clientId)
- **Client Secret** (clientSecret)
- **Bot ID** (botId)

### Step 2: Obtain Access Token

Use your Client ID and Client Secret to request an access token:

**Endpoint**: `POST https://auth.dotgo.com/auth/oauth/token`

**Request Format**:

```
POST https://auth.dotgo.com/auth/oauth/token?grant_type=client_credentials HTTP/1.1
Host: auth.dotgo.com
Content-Type: application/x-www-form-urlencoded
Authorization: Basic <base64(clientId:clientSecret)>

grant_type=client_credentials
```

**Authorization Header**:
- Encode `clientId:clientSecret` as base64
- Prefix with "Basic "
- Example: `Authorization: Basic aWFtY2xpZW50OnlvdW93ZXpzYW1lbHk=`

### Step 3: Use Access Token

Include the Bearer token in all API requests:

```
Authorization: Bearer <access_token>
```

## Token Details

| Field | Value |
|-------|-------|
| **Endpoint** | `https://auth.dotgo.com/auth/oauth/token` |
| **Grant Type** | client_credentials |
| **Scope** | Chatbot-message (implicit) |
| **Token Expiry** | Typically 1 hour; check `expires_in` field |
| **Rate Limit** | 60 requests per minute per client |

## Token Response

**Success (200 OK)**:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "Chatbot-message"
}
```

**Failure (401 Unauthorized)**:

```json
{
  "error": "invalid_client",
  "error_description": "Bad client credentials"
}
```

## Sample cURL Request

```bash
curl -X POST https://auth.dotgo.com/auth/oauth/token \
  -H "Authorization: Basic aWFtY2xpZW50OnlvdXNlY3JldA==" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials"
```

## Sample Python Request

```python
import requests
import base64

client_id = "your_client_id"
client_secret = "your_client_secret"

# Create base64 encoded credentials
credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

headers = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(
    "https://auth.dotgo.com/auth/oauth/token",
    headers=headers,
    data={"grant_type": "client_credentials"}
)

token_data = response.json()
access_token = token_data["access_token"]
```

## Using the Access Token

**In API Requests**:

```bash
curl -X GET https://api.dotgo.com/bot/v1/{botId}/messages/{msgId}/status \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Credential Management

### Storing Credentials Securely

1. **Environment Variables**: Store Client ID/Secret in environment variables, never in code
   ```
   export RCS_CLIENT_ID="your_client_id"
   export RCS_CLIENT_SECRET="your_client_secret"
   ```

2. **Secrets Manager**: Use AWS Secrets Manager, Azure Key Vault, or similar
   ```python
   client_id = get_secret("rcs/client_id")
   client_secret = get_secret("rcs/client_secret")
   ```

3. **Configuration Files**: Store in secure, restricted files (not in git)
   ```yaml
   # config/rcs.yml (excluded from version control)
   client_id: ${RCS_CLIENT_ID}
   client_secret: ${RCS_CLIENT_SECRET}
   ```

### Rotating Credentials

1. Request new credentials from Dotgo support (rbm-support@dotgo.com)
2. Update application with new credentials
3. Test with new credentials before decommissioning old ones
4. Keep old credentials active during transition period (24-48 hours)
5. Decommission old credentials once all services are using new ones

## Error Responses

| HTTP Code | Error | Cause | Resolution |
|-----------|-------|-------|-----------|
| 400 | `invalid_request` | Missing or malformed parameters | Check request format |
| 401 | `invalid_client` | Bad client ID or secret | Verify credentials from agent setup |
| 401 | `invalid_grant` | Grant type not supported | Use `grant_type=client_credentials` |
| 500 | `server_error` | Server-side issue | Retry after a few seconds |
| 503 | `service_unavailable` | Auth service down | Wait and retry |

## Rate Limits

**Token Endpoint**:
- 60 requests per minute per client ID
- Returns 429 Too Many Requests if exceeded

**Message APIs**:
- Default: 60 TPM (Transactions Per Minute) per client
- Contact rbm-support@dotgo.com to increase

## Security Best Practices

1. **HTTPS Only**: Always use HTTPS for token requests and API calls
2. **Token Storage**: Store tokens in-memory; refresh before expiry
3. **Token Refresh**: Request new tokens before expiry; don't cache beyond expires_in
4. **Credential Isolation**: Use separate client ID/secret for different environments (dev/staging/prod)
5. **Audit Logging**: Log all token requests and credential usage
6. **IP Whitelisting**: If possible, whitelist IP addresses at Dotgo
7. **Monitor Usage**: Track token requests and API calls for anomalies
8. **Revoke Compromised**: If credentials are exposed, request revocation immediately

## Troubleshooting

### "Invalid Client" Error

**Cause**: Client ID or Client Secret is incorrect or has been revoked

**Fix**:
1. Verify credentials from agent creation email
2. Check for extra whitespace or encoding issues
3. Confirm credentials match the correct environment (dev vs prod)
4. Contact Dotgo support to verify credentials are active

### "Invalid Grant" Error

**Cause**: Grant type is incorrect

**Fix**:
- Use `grant_type=client_credentials` exactly as shown
- Don't use `grant_type=password` or other types

### Token Expiry During Request

**Cause**: Token expired before API call completed

**Fix**:
1. Implement token refresh logic before expiry
2. Always check `expires_in` in token response
3. Refresh tokens proactively (e.g., after 55 minutes for 1-hour tokens)

### Authorization Header Rejected

**Cause**: Malformed or missing Authorization header

**Fix**:
- Ensure format: `Authorization: Bearer <token>`
- No extra spaces or line breaks
- Token must be valid and not expired

## Cross-module workflow docs

- Use the same access token for all RCS API calls (messaging, templates, webhooks)
- Refresh tokens before expiry to avoid authentication failures
- Implement token caching with refresh logic for high-volume scenarios

## Reference (from source)

<!-- procedural:v2 -->
# RCS Authentication

Authenticate RCS API requests using OAuth2 Client Credentials flow with Dotgo Auth2 SSO.
