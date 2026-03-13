source_url: https://console-docs.gupshup.io/docs/modify-variable-node

<!-- kb-golden:v7 -->
# Modify Variable Node

**Module**: Bot Studio

## Definition
The Modify variable is a new node available in the Journey Builder Action node list for performing various operations on the values stored in any variable. This will enable bot designers to perform simple to complex operations on different data types (string, number, and JSON) without needing to use the code node

## Procedure
### Exact path
Gupshup Console → Bot Studio → Modify Variable Node

### Where to configure it
Gupshup Console → Bot Studio → Modify Variable Node

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **Modify Variable Node**.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Modify Variable Node**.
4. Add at Beginning: The “Add at Beginning” modifier is used for appending a specified string value to the beginning of the string variable.(For e.g - Add Mr. to “JOHN DOE” → “Mr.JOHN DOE”).
5. Add at Last: The “Add at Last” modifier is used for appending a specified string value to the end of the string variable.(For e.g - Add “ Department” to “Artificial Intelligence” → “Artificial Intelligence Department”).
6. Add at Both Side: The “Add at Both Side” adds a specified string value to both the beginning and end of the string variable.(For e.g - Add quotes(“) to John → “John”).
7. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- Note:
- Supported Operations:
- STRING:
- JSON
- Number

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
# Modify Variable Node

**Module**: Bot Studio

## Overview
The Modify variable is a new node available in the Journey Builder Action node list for performing various operations on the values stored in any variable. This will enable bot designers to perform simple to complex operations on different data types (string, number, and JSON) without needing to use the code node

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### Introduction

The Modify variable is a new node available in the Journey Builder Action node list for performing various operations on the values stored in any variable. This will enable bot designers to perform simple to complex operations on different data types (string, number, and JSON) without needing to use the code node

### Note:

The list of supported operations will be available based on the variable where the operated value will be stored. Eg.: If the variable on which the value will be stored is of the Number data type, then the operations available in the dropdown will be limited to those applicable to numbers only.

The modified variable will have multiple input/variable selection placeholders available based on the selected operation. The bot designer must ensure that the selected variable is of the required data type for the operation to be performed.

### Supported Operations:

#### STRING:

- Capitalize First Letter: The “Capitalize” First Letter modifier can be used to convert the first letter of a string variable to uppercase, leaving the rest unchanged.(For e.g - “john doe” → “John doe”)
Capitalize First Letter: The “Capitalize” First Letter modifier can be used to convert the first letter of a string variable to uppercase, leaving the rest unchanged.(For e.g - “john doe” → “John doe”)

- Capitalize First Letter of each word: Capitalizes the first letter of each word in a specific string variable while maintaining the original letter casing.( A combination of both upper and lower case string. (For e.g - “john doe” → “John Doe”)
Capitalize First Letter of each word: Capitalizes the first letter of each word in a specific string variable while maintaining the original letter casing.( A combination of both upper and lower case string. (For e.g - “john doe” → “John Doe”)

- All Upper Case: The modifier “All Upper Case” converts all letters in the specified string variable to uppercase. (For e.g - “john doe” → “JOHN DOE”)
All Upper Case: The modifier “All Upper Case” converts all letters in the specified string variable to uppercase. (For e.g - “john doe” → “JOHN DOE”)

- All Lower Case: The “All Lower Case” modifier converts all the letters in the specified string variable to lowercase. (For e.g - “JOHN DOE” → “john doe”)
All Lower Case: The “All Lower Case” modifier converts all the letters in the specified string variable to lowercase. (For e.g - “JOHN DOE” → “john doe”)

- Add at Beginning: The “Add at Beginning” modifier is used for appending a specified string value to the beginning of the string variable.(For e.g - Add Mr. to “JOHN DOE” → “Mr.JOHN DOE”)
Add at Beginning: The “Add at Beginning” modifier is used for appending a specified string value to the beginning of the string variable.(For e.g - Add Mr. to “JOHN DOE” → “Mr.JOHN DOE”)

- Add at Last: The “Add at Last” modifier is used for appending a specified string value to the end of the string variable.(For e.g - Add “ Department” to “Artificial Intelligence” → “Artificial Intelligence Department”)
Add at Last: The “Add at Last” modifier is used for appending a specified string value to the end of the string variable.(For e.g - Add “ Department” to “Artificial Intelligence” → “Artificial Intelligence Department”)

- Add at Both Side: The “Add at Both Side” adds a specified string value to both the beginning and end of the string variable.(For e.g - Add quotes(“) to John → “John”)
Add at Both Side: The “Add at Both Side” adds a specified string value to both the beginning and end of the string variable.(For e.g - Add quotes(“) to John → “John”)

- Trim from beginning: The “Trim from Beginning” modifier removes a specified number of characters from the start of the string variable. (For e.g - Specified number of characters = 2 from String - “919090909090” → “9090909090”)
Trim from beginning: The “Trim from Beginning” modifier removes a specified number of characters from the start of the string variable. (For e.g - Specified number of characters = 2 from String - “919090909090” → “9090909090”)

- Trim from last: The “Trim from last” modifier removes a specified number of characters from the end of the string variable. (For e.g - Specified number of characters = 1 from String - “T-Shirts” → “T-Shirt”)
Trim from last: The “Trim from last” modifier removes a specified number of characters from the end of the string variable. (For e.g - Specified number of characters = 1 from String - “T-Shirts” → “T-Shirt”)

- Trim spaces from both sides: The “Trim spaces from both sides” modifier removes any leading or trailing spaces from the string variable. (For e.g - “ JOHN DOE ” → “.JOHN DOE”)
Trim spaces from both sides: The “Trim spaces from both sides” modifier removes any leading or trailing spaces from the string variable. (For e.g - “ JOHN DOE ” → “.JOHN DOE”)

- Assign Value: You can use the "Assign Value" modifier to update a variable with the desired value. This value can either be directly entered or cloned from another variable.
Assign Value: You can use the "Assign Value" modifier to update a variable with the desired value. This value can either be directly entered or cloned from another variable.

- Remove from beginning: Removes the specified characters from the beginning of the selected string. (For e.g - Remove “Rs. ” from “ Rs. 99” → “99”)
Remove from beginning: Removes the specified characters from the beginning of the selected string. (For e.g - Remove “Rs. ” from “ Rs. 99” → “99”)

- Remove from last: Removes the specified characters from the end of the selected string. (For e.g - Remove “cm” from “ 5.7cm” → “5.7”)
Remove from last: Removes the specified characters from the end of the selected string. (For e.g - Remove “cm” from “ 5.7cm” → “5.7”)

### JSON

- Stringify: The “Stringify” modifier converts an object variable into its string representation.
(For e.g. : userPreferences: { "theme": "dark", "notifications": true, "language": "English" }

→ Stringified userPreferences: "{"theme":"dark","notifications":true,"language":"English"}"

- String to object: The “String to object” modifier parses a string variable into an object. Reverse of the above given example.
### Number

- Addition: The “Addition” modifier Increases the numeric value by a specific numerical value.
Addition: The “Addition” modifier Increases the numeric value by a specific numerical value.

- Subtraction: The “Subtraction” modifier decreases the numeric variable by a specific numerical value.
Subtraction: The “Subtraction” modifier decreases the numeric variable by a specific numerical value.

- Multiply: The “Multiply” modifier multiplies the numeric value by a specific numerical value.
Multiply: The “Multiply” modifier multiplies the numeric value by a specific numerical value.

- Round-up: The “Round-up” modifier rounds the numeric variable up to the nearest whole number. (For e.g 3.2 → 4 AND 7.8 → 8)
Round-up: The “Round-up” modifier rounds the numeric variable up to the nearest whole number. (For e.g 3.2 → 4 AND 7.8 → 8)

- Round-down: The “Round-down” modifier rounds the numeric variable down to the nearest whole number. (For e.g 3.2 → 3 AND 7.8 → 7)
Round-down: The “Round-down” modifier rounds the numeric variable down to the nearest whole number. (For e.g 3.2 → 3 AND 7.8 → 7)

- Round-Off to nearest: The “Round-Off to nearest” modifier rounds the numeric variable to the nearest whole number or the nearest multiple of ten. (For e.g: Whole Number: 3.2 → 3 , 7.8 → 8 ; Multiple of 10: 13 → 10 , 15 → 20)
Round-Off to nearest: The “Round-Off to nearest” modifier rounds the numeric variable to the nearest whole number or the nearest multiple of ten. (For e.g: Whole Number: 3.2 → 3 , 7.8 → 8 ; Multiple of 10: 13 → 10 , 15 → 20)

- Remove from beginning: Removes the specified characters from the beginning of the selected string. (For e.g - Remove “91 ” from “919090909090” → “9090909090”)
Remove from beginning: Removes the specified characters from the beginning of the selected string. (For e.g - Remove “91 ” from “919090909090” → “9090909090”)

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
