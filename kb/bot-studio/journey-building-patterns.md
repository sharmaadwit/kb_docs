source_url: https://docs.gupshup.io/docs/journey-patterns

<!-- kb-golden:v10 -->
# Journey Building Patterns

**Module**: Bot Studio

## Definition

Common journey sequences that solve specific use cases. Each pattern includes JSON, node configuration, and troubleshooting.

## Pattern 1: Collect Input → Validate → Send Response

**Use case:** Form collection, user preferences, user input

**Node sequence:**
```
Text Input Node → Condition Node → Message Node
```

**Steps:**
1. Add **Text Input Node** with prompt "Enter your email:"
2. Add **Condition Node** with rule: `input matches regex ^[^@]+@[^@]+$`
3. Add **Message Node** for valid email: "Thanks! We'll send confirmation"
4. Add **Message Node** for invalid: "Invalid email, try again"

**Store input in variables:**
```
Variable name: user_email
Source: Text Node output
Use in message: Hi {{user_email}}, thanks for signing up!
```

## Pattern 2: Text → Buttons → List

**Use case:** Multi-step selection, progressive disclosure

**Node sequence:**
```
Message (text) → Quick Reply (buttons) → List Message
```

**Example flow:**
```
1. Send: "What category interests you?"
   Buttons: [Electronics, Clothing, Other]
   
2. If "Electronics" clicked:
   Send list with:
   - Phones (Description: Smartphones and accessories)
   - Laptops (Description: Computers and tablets)
   - Accessories (Description: Cables, chargers, cases)

3. User selects item → Store in variable
```

**Common issue: List doesn't render**
- Check: Not more than 10 rows total
- Check: Not more than 3 sections
- Check: Descriptions under 72 characters
- Check: List message JSON is valid

**Fix:** Use Message Node JSON Reference for correct structure

## Pattern 3: Script Node → Dynamic Data → Message

**Use case:** Fetch data from API, personalize message

**Node sequence:**
```
Script Node → API Call Node → Message Node
```

**Example:**
```
1. Script Node:
   var order_id = {{captured_order_id}}
   var api_url = "https://api.example.com/orders/" + order_id

2. API Call Node:
   URL: {{api_url}}
   Method: GET
   Store response in: order_data

3. Message Node:
   "Your order #{{order_data.order_id}} costs ${{order_data.amount}}"
```

**Error handling:**
- If API returns 404: "Order not found"
- If API timeout: "System busy, try later"
- If API error: "Unable to fetch details"

## Pattern 4: Multi-Step Intent Detection

**Use case:** Progressive intent understanding, refinement

**Node sequence:**
```
Initial Intent Detection → Condition Node → Follow-up Question → Clarified Message
```

**Example:**
```
1. User says: "I need help"
   Intent detected: support (confidence: 0.6)

2. Condition: If confidence < 0.7
   Send: "Are you having an issue with an order or product?"
   Buttons: [Order Issue, Product Issue, Other]

3. Based on selection, send specific help message
```

## Pattern 5: Async Journey with Webhooks

**Use case:** Send message, wait for external event, resume

**Node sequence:**
```
Message Node → Wait for Event → Message Node
```

**Example:**
```
1. Send: "We've sent a code to your email"
2. Wait for webhook event: email_confirmed
3. When webhook arrives with email_confirmed:
   Resume with: "Your account is now verified!"
```

**Webhook payload expected:**
```json
{
  "event": "email_confirmed",
  "user_id": "user_12345",
  "timestamp": "2026-06-15T10:00:00Z"
}
```

## Testing Patterns

Before deployment:
1. Use Test Widget to run journey
2. Test each branch (valid input, invalid input, etc.)
3. Verify variables are captured
4. Check message formatting on actual device
5. Verify API calls work (if using APIs)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Variables not substituting | Ensure variable set before message node |
| List doesn't render | Check JSON structure in Message Node JSON Reference |
| Buttons unclickable | Verify button count ≤ 3, check IDs are unique |
| Journey stuck waiting | Check timeout settings, verify webhook is firing |
| API call failing | Verify URL is correct, check API keys, review API response |

## Reference (from source)

<!-- procedural:v2 -->
# Journey Building Patterns

Common journey sequences for form collection, multi-step selection, API integration, and async workflows.
