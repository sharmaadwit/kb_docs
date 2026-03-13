source_url: https://console-docs.gupshup.io/docs/json-handler-instead-of-code-node

<!-- kb-golden:v9 -->
# JSON Handler instead of Code Node

**Module**: Bot Studio

## Definition
In older versions of Journey Builder (JB Pro), you'd use a Code Node and write custom JavaScript like this:

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → JSON Handler instead of Code Node

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **JSON Handler instead of Code Node**.
4. Add JSON Handler Node after your API Node.
5. Configure mappings visually by specifying JSON paths and the variable names to map values to.
6. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- _Run a quick smoke test and confirm expected behavior._

### Fields to configure
- JSON Handler Node after your API Node

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- _Add common failure modes and how to fix them._

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **JSON Handler instead of Code Node**.

## Options / variants
- Add JSON Handler Node after your API Node.

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# JSON Handler instead of Code Node

**Module**: Bot Studio

## Overview
In older versions of Journey Builder (JB Pro), you'd use a Code Node and write custom JavaScript like this:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
## Parsing Using Legacy Code Node (JavaScript) - Deprecated use case

In older versions of Journey Builder (JB Pro), you'd use a Code Node and write custom JavaScript like this:

### Sample API JSON Payload (Example)

```
{
  "user": {
    "id": 12345,
    "name": "Alice",
    "email": "alice@example.com",
    "orders": [
      {
        "orderId": "ORD001",
        "amount": 250,
        "status": "delivered"
      },
      {
        "orderId": "ORD002",
        "amount": 450,
        "status": "processing"
      }
    ]
  }
}
```

Sample Code used to parse the JSON earlier:

```
//Assume variable `input` contains the API response JSON string\

let response = JSON.parse(var_local.input);

//Extract user details\
let userId = response.user.id;
let userName = response.user.name;
let userEmail = response.user.email;

// Extract first order details\
let firstOrder = response.user.orders\[0];
let orderId = firstOrder.orderId;
let orderAmount = firstOrder.amount;
let orderStatus = firstOrder.status;

// Store extracted values in output variables to use later in the journey\
output.userId = userId;
output.userName = userName;
output.userEmail = userEmail;
output.orderId = orderId;
output.orderAmount = orderAmount;
output.orderStatus = orderStatus;
```

This requires:

- Parsing JSON manually
- Writing and debugging JavaScript code
- Mapping extracted values to output variables manually
## Parsing Using New JSON Handler Node (No-Code)

With the new JSON Handler Node introduced in JB V2 (Upgraded Journey Builder), you can achieve this without code, via an intuitive UI that lets you define JSON paths for mapping.

### How it works:

- Add JSON Handler Node after your API Node.
- Configure mappings visually by specifying JSON paths and the variable names to map values to.
- More on How to use JSON Handler : Link
- Example mappings you would configure:
The JSON Handler node automatically parses the JSON payload from the previous API call and assigns the values to the specified variables. No coding is required, and the UI guides you to enter correct JSON paths.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 9 months ago
