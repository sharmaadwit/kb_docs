source_url: https://console-docs.gupshup.io/docs/json-handler-instead-of-code-node
# BOT STUDIO

## JSON Handler instead of Code Node

# JSON Handler instead of Code Node

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

Updated 9 months ago
