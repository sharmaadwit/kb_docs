source_url: https://console-docs.gupshup.io/docs/functions-from-m-q

<!-- kb-golden:v4 -->
# Functions from M - Q

**Module**: Bot Studio

## Definition
Return the highest value from a list or array. The list or array is inclusive at both ends.

## Procedure
### Exact path
Gupshup Console → Bot Studio → Functions from M - Q

### Where to configure it
Gupshup Console → Bot Studio → Functions from M - Q

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Functions from M - Q**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- max
- merge
- min
- mod
- month
- mul
- newGuid
- not
- or

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
# Functions from M - Q

**Module**: Bot Studio

## Overview
Return the highest value from a list or array. The list or array is inclusive at both ends.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### max

Return the highest value from a list or array. The list or array is inclusive at both ends.

```
max(<number1>, <number2>, ...)  
max([<number1>, <number2>, ...])
```

Examples

These examples get the highest value from the set of numbers and the array:

```
max(1, 2, 3)  
max(createArray(1, 2, 3))
```

And return the result 3.

### merge

Merges multiple JSON objects or an array of objects together.

```
merge(<json1>, <json2>, ...)
```

Examples

Say you have the following JSON objects:

```
json1 = @"{  
            'FirstName': 'John',  
            'LastName': 'Smith',  
            'Enabled': false,  
            'Roles': [ 'User' ]  
          }"  
json2 =@"{  
            'Enabled': true,  
            'Roles': [ 'User', 'Admin' ]  
          }"
```

This example merges the JSON objects:

```
string(merge(json(json1), json(json2)))
```

And returns the resulting object {"FirstName":"John","LastName":"Smith","Enabled":true,"Roles":["User","Admin"]}.

Say you want to combine objects and a list of objects together. The following example combines JSON object and an array of objects:

```
merge({k1:'v1'}, [{k2:'v2'}, {k3: 'v3'}], {k4:'v4'})
```

And returns the object { "k1": "v1", "k2": "v2", "k3": "v3", "k4": "v4" }.

### min

Return the lowest value from a set of numbers or an array.

```
min(<number1>, <number2>, ...)  
min([<number1>, <number2>, ...])
```

Examples

These examples get the lowest value in the set of numbers and the array:

```
min(1, 2, 3)  
min(createArray(1, 2, 3))
```

And return the result 1.

### mod

Return the remainder from dividing two numbers. To get the integer result, see div().

```
mod(<dividend>, <divisor>)
```

Example

This example divides the first number by the second number:

```
mod(3, 2)
```

And returns the result 1.

### month

Return the month of the specified timestamp.

```
month('<timestamp>')
```

Example

```
month('2018-03-15T13:01:00.000Z')
```

And it returns the result 3.

### mul

Return the product from multiplying two numbers.

```
mul(<multiplicand1>, <multiplicand2>)
```

Examples

These examples multiple the first number by the second number:

```
mul(1, 2)  
mul(1.5, 2)
```

And return the following results respectively:

- 2
- 3
### newGuid

Return a new Guid string.

```
newGuid()
```

Example

```
newGuid()
```

And it returns a result which follows the format xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx.

### not

Check whether an expression is false. Return true if the expression is false, or return false if true.

```
not(<expression>)
```

Example 1

These examples check whether the specified expressions are false:

```
not(false)  
not(true)
```

And return the following results respectively:

- The expression is false, so the function returns true.
- The expression is true, so the function returns false.
Example 2

These examples check whether the specified expressions are false:

```
not(equals(1, 2))  
not(equals(1, 1))
```

And return the following results respectively:

- The expression is false, so the function returns true.
- The expression is true, so the function returns false.
### or

Check whether at least one expression is true. Return true if at least one expression is true, or return false if all are false.

```
or(<expression1>, <expression2>, ...)
```

Example 1

These examples check whether at least one expression is true:

```
or(true, false)  
or(false, false)
```

And return the following results respectively:

- At least one expression is true, so the function returns true.
- Both expressions are false, so the function returns false.
Example 2

These examples check whether at least one expression is true:

```
or(equals(1, 1), equals(1, 2))  
or(equals(1, 2), equals(1, 3))
```

And return the following results respectively:

- At least one expression is true, so the function returns true.
- Both expressions are false, so the function returns false.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
