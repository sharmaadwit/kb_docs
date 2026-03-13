source_url: https://console-docs.gupshup.io/docs/extracting-and-manipulating-data-using-expression-library-functions-instead-of-code-node

<!-- kb-golden:v7 -->
# Extracting and Manipulating Data Using Expression Library Functions Instead of Code Node

**Module**: Bot Studio

## Definition
In legacy Journey Builder implementations, many common tasks such as string concatenation, conditional checks, or simple data transformations required a Code Node where bot designers or developers had to write custom JavaScript. This approach posed challenges such as increased complexity, need for coding skills, and higher chances of runtime errors.

## Procedure
### Exact path
Gupshup Console → Bot Studio → Extracting and Manipulating Data Using Expression Library Functions Instead of Code Node

### Where to configure it
Gupshup Console → Bot Studio → Extracting and Manipulating Data Using Expression Library Functions Instead of Code Node

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **Extracting and Manipulating Data Using Expression Library Functions Instead of Code Node**.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Extracting and Manipulating Data Using Expression Library Functions Instead of Code Node**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- Example Use Case

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Extracting and Manipulating Data Using Expression Library Functions Instead of Code Node

**Module**: Bot Studio

## Overview
In legacy Journey Builder implementations, many common tasks such as string concatenation, conditional checks, or simple data transformations required a Code Node where bot designers or developers had to write custom JavaScript. This approach posed challenges such as increased complexity, need for coding skills, and higher chances of runtime errors.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
In legacy Journey Builder implementations, many common tasks such as string concatenation, conditional checks, or simple data transformations required a Code Node where bot designers or developers had to write custom JavaScript. This approach posed challenges such as increased complexity, need for coding skills, and higher chances of runtime errors.

With the introduction of the Expression Library in Journey Builder V2, many of these routine operations can now be accomplished using built-in functions in a no-code, visual environment via the Modify Variable Node. This change empowers non-technical users to efficiently manipulate data, simplifies bot development, and improves maintainability.

### Example Use Case

Suppose an API returns the following JSON response containing user profile information and its saved in a JSON Variable user:

```
{
  "user": {
    "firstName": "John",
    "lastName": "Doe",
    "email": "john.doe@example.com",
    "age": 29,
    "subscription": {
      "status": "active",
      "startDate": "2023-01-15",
      "expiryDate": "2024-01-15"
    }
  }
}
```

## Legacy Approach: Using Code Node (JavaScript)

Previously, to concatenate the user's full name and check if their subscription is active, you'd write:

```
let data = JSON.parse(input);

let var_local.fullName = data.user.firstName + " " + data.user.lastName;

let var_local.isActive = data.user.subscription.status === "active";

output.fullName = fullName;
output.isActive = isActive;
```

## Modern Approach: Using Expression Library (No Code)

Now, in the Modify Variable Node, you can directly use these expressions without any code:

- Extract the First and Last Name using JSON Handler
- Concatenate First and Last Name
```
concat(var_local.firstName, " ", var_local.lastName)
```

Checkout all the other function available in the Expression Library to know more on the operation and logics available : Link

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 9 months ago
