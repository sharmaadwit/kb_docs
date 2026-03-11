source_url: https://console-docs.gupshup.io/docs/extracting-and-manipulating-data-using-expression-library-functions-instead-of-code-node
# BOT STUDIO

## Extracting and Manipulating Data Using Expression Library Functions Instead of Code Node

# Extracting and Manipulating Data Using Expression Library Functions Instead of Code Node

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

Updated 9 months ago
