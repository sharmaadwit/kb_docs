source_url: https://docs.gupshup.io/docs/integrations

<!-- kb-golden:v10 -->
# Google Sheets Integration with Bot Studio

**Module**: Bot Studio / Integrations

## Definition

Google Sheets integration enables Bot Studio journeys to read from, write to, and manipulate Google Sheets data in real-time. This allows you to store form responses, manage customer data, track campaigns, and dynamically fetch information for personalized conversations.

## Current Status

**Fully Supported** — Google Sheets integration is available in Bot Studio via API nodes and webhooks. Gupshup Console includes pre-built connectors for SuperAgent, and Bot Studio can connect using custom API patterns.

## Integration Methods

### 1. Custom API Node (Webhook/REST)

The primary method for Bot Studio is using the **API Node** to make authenticated requests to Google Sheets API.

**Setup Requirements:**
- Google Cloud Project with Sheets API enabled
- OAuth 2.0 credentials (Client ID, Client Secret)
- Access token with `https://www.googleapis.com/auth/spreadsheets` scope
- Spreadsheet ID and Sheet name/ID

**How it works:**
1. Create an API Node in your journey
2. Configure HTTP POST/GET to Google Sheets API endpoint
3. Pass access token in Authorization header
4. Map response data to journey variables

**Example API Call (Add Row):**
```
POST https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}!A1:append
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "values": [
    ["John Doe", "john@example.com", "2026-06-16"]
  ]
}
```

**Example API Call (Read Data):**
```
GET https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}!A1:Z100
Authorization: Bearer {ACCESS_TOKEN}
```

### 2. Webhook Integration (Inbound Data)

Receive Google Sheets updates via webhooks or push data from Sheets to Gupshup.

**Setup:**
- Use Gupshup's Custom Integration to define webhook endpoint
- Configure Google Sheets App Script to POST to webhook on sheet changes
- Map incoming data to journey variables and triggers

**Example Google Sheets App Script:**
```javascript
function onEdit(e) {
  const range = e.range;
  const values = range.getValues();
  
  const payload = {
    sheet_name: e.source.getActiveSheet().getName(),
    row: range.getRow(),
    column: range.getColumn(),
    value: values[0][0],
    timestamp: new Date().toISOString()
  };
  
  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload),
    headers: {
      'Authorization': 'Bearer YOUR_GUPSHUP_TOKEN'
    }
  };
  
  UrlFetchApp.fetch('https://your-webhook-endpoint/sheets-update', options);
}
```

## Supported Operations

### Read Operations

- **Fetch row(s)** — Get specific cells, rows, or ranges
- **Query data** — Filter and search spreadsheet values
- **List sheets** — Get metadata about sheet structure
- **Get formatted values** — Retrieve with formatting (colors, number formats)

**Example Query (Search for customer):**
```
GET /spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}!A:Z
```
Parse response to find matching customer by email or phone.

### Write Operations

- **Append rows** — Add new data to the end of a range
- **Update cells** — Modify specific cell values
- **Clear range** — Delete cell contents
- **Batch updates** — Multiple changes in one request

**Example Write (Form Response):**
When a user submits a form in the journey:
1. Collect responses in journey variables
2. Call API Node to append to Sheets
3. Return success/failure to user

## Known Limitations

### Quota & Rate Limits

- **Read Requests:** 300 requests per minute per user, per project
- **Write Requests:** 120 requests per minute per user
- **Batch Size:** Max 10,000 cells per batch update
- **Cell Size:** Max 50,000 characters per cell

**Impact on Bot Studio:**
- High-volume journeys (thousands of concurrent users) may hit rate limits
- Implement backoff/retry logic in your journey
- Consider caching frequently-read data in journey variables

### Authentication

- **OAuth Token Expiry:** Access tokens expire every 1 hour
- **Service Account vs User Account:** Service accounts have separate quotas
- **Scope Limitations:** Limited to `spreadsheets` scope (can't access Drive)

**Impact on Bot Studio:**
- Store refresh tokens securely, don't embed in journeys
- Use Gupshup's credential management for OAuth tokens
- Test token expiration handling in long-running journeys

### Data Format Constraints

- **No Formulas in API Responses:** API returns values, not formula definitions
- **Limited Cell Formatting:** Read operations return plain values
- **No Real-time Notifications:** Must poll or use webhooks for updates
- **Tab Name Limits:** Sheet names with special characters need escaping

**Workaround:**
- Use Apps Script to handle complex formulas before API call
- Store formatted output separately if formatting is critical
- Implement polling at 5-10 second intervals for near-real-time updates

### Concurrent Access

- **Simultaneous Edits:** Multiple journeys updating same cells may cause conflicts
- **Cell Locking:** Sheets API doesn't support native row/cell locks
- **No Transactions:** Updates aren't atomic across multiple cells

**Best Practice:**
- Designate specific columns/rows for bot writes (separate from manual edits)
- Use unique identifiers (IDs) to avoid overwriting data
- Log all bot-initiated changes for audit trails

## Use Cases

### 1. Form Response Storage

**Scenario:** Collect customer details via Bot Studio forms, store in Sheets.

**Flow:**
1. Journey asks for name, email, phone in prompt nodes
2. API Node appends row: `[name, email, phone, timestamp]`
3. Confirm to user: "Response saved!"

**Sheets Structure:**
```
Name          | Email              | Phone          | Timestamp
John Doe      | john@example.com   | 919876543210   | 2026-06-16T10:30:00Z
Jane Smith    | jane@example.com   | 919876543211   | 2026-06-16T10:35:00Z
```

### 2. Dynamic Data Lookup

**Scenario:** Customer asks for their order status; bot fetches from Sheets.

**Flow:**
1. Ask user for order ID
2. API Node reads all rows from Sheets
3. Filter to find matching order ID
4. Return status to user

**Sheets Structure:**
```
Order ID  | Customer Name | Status    | Ship Date
ORD-001   | John Doe      | Shipped   | 2026-06-15
ORD-002   | Jane Smith    | Processing| Pending
```

### 3. Lead Tracking & Scoring

**Scenario:** Capture leads from multiple channels, score in Sheets, trigger follow-ups.

**Flow:**
1. Append new lead row
2. External system (Zapier, etc.) scores lead
3. Webhook triggers journey to send follow-up message
4. Update "contacted" status in Sheets

## Implementation Checklist

### Prerequisites
- [ ] Google Cloud Project with Sheets API enabled
- [ ] OAuth 2.0 credentials created (or Service Account JSON key)
- [ ] Spreadsheet created and shared with bot account
- [ ] Spreadsheet ID and Sheet name/ID identified

### In Bot Studio
- [ ] Create API node with authentication headers
- [ ] Test read/write operations before deployment
- [ ] Implement error handling (token expiry, rate limits)
- [ ] Map Sheets data to journey variables
- [ ] Add retry logic for failed API calls

### Validation
- [ ] [ ] Read test: Fetch specific row and confirm data matches
- [ ] Write test: Append dummy row and verify in Sheets UI
- [ ] End-to-end test: Full journey with form → Sheets → confirmation
- [ ] Rate limit test: Simulate high-volume scenario

## Troubleshooting

### API Returns 401 Unauthorized

**Cause:** Invalid or expired OAuth token

**Fix:**
1. Verify token hasn't expired (tokens last 1 hour)
2. Regenerate access token using refresh token
3. Check OAuth scopes include `spreadsheets`
4. Confirm token is in Authorization header: `Bearer {TOKEN}`

### API Returns 404 Not Found

**Cause:** Invalid Spreadsheet ID or Sheet name

**Fix:**
1. Copy Spreadsheet ID from sheet URL: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/...`
2. Confirm Sheet name matches exactly (case-sensitive): `Sheet1`, `Responses`, etc.
3. Verify sheet exists and isn't deleted
4. Check cell range format: `A1:Z100` (not `A:Z100` for specific range)

### API Returns 429 Too Many Requests

**Cause:** Exceeded quota limits (300 reads/min, 120 writes/min)

**Fix:**
1. Reduce query frequency; cache results in variables
2. Batch multiple updates into single request
3. Spread API calls across time intervals
4. Consider using Service Account for higher quota

### Data Not Appearing in Sheet

**Cause:** API succeeded (200 response) but data missing

**Fix:**
1. Verify API response includes actual row count: `"updatedRows": 1`
2. Confirm sheet isn't read-only or protected
3. Check cell range in API call matches expected location
4. View sheet history to confirm insert timestamp

## Best Practices

### 1. Secure Credentials

- Never embed OAuth tokens in journey code
- Use Gupshup's Manage API section to store credentials
- Rotate refresh tokens monthly
- Restrict API key scope to `spreadsheets` only

### 2. Implement Exponential Backoff

```
Attempt 1: Immediate
Attempt 2: Wait 1 second, retry
Attempt 3: Wait 2 seconds, retry
Attempt 4: Wait 4 seconds, retry
Then fail with user message
```

### 3. Log All Sheet Operations

Track every read/write for audit and debugging:
```
{
  "timestamp": "2026-06-16T10:30:00Z",
  "operation": "append_row",
  "sheet": "Responses",
  "data": ["John Doe", "john@example.com"],
  "status": "success"
}
```

### 4. Separate Read and Write Sheets

- Use one sheet for form responses (bot writes only)
- Use another sheet for lookup data (bot reads only, humans update)
- Prevents data corruption from concurrent edits

### 5. Handle Missing/Malformed Data

```
if response.status != 200:
    message = "Unable to save. Please try again."
elif response.data is empty:
    message = "No matching records found."
else:
    process_data(response.data)
```

## See Also

- [API Node in Bot Studio](./api-node.md)
- [Webhook Integration Patterns](../integrations/webhook-crm-integration-patterns.md)
- [Custom Integrations](../integrations/custom-integrations.md)
- [Google Sheets API Reference](https://developers.google.com/sheets/api/reference/rest)
- [Google Apps Script Documentation](https://developers.google.com/apps-script)

## Reference (from source)

<!-- procedural:v2 -->
# Google Sheets Integration with Bot Studio

Integrate Google Sheets with Bot Studio journeys to store and retrieve data in real-time using API nodes and webhooks. Supports reading, writing, and updating spreadsheet data.
