source_url: https://console-docs.gupshup.io/docs/functions-from-a-d

<!-- kb-golden:v10 -->
# Functions from A - D

**Module**: Bot Studio

## Definition
Return the absolute value of the specified number.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Functions from A - D

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- a number of days to a timestamp in an optional locale format
- a number of seconds to a timestamp

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Functions from A - D**.
4. add(<item1>, <item2>, ...).
5. add(1, 1.5).
6. add('hello',null).
7. add('hello','world').
8. Add a number of days to a timestamp in an optional locale format.
9. Add a number of hours to a timestamp in an optional locale format.
10. Add a number of minutes to a timestamp in an optional locale format.
11. Add a property and its value, or name-value pair, to a JSON object, and return the updated object. If the object already exists at runtime the function throws an error.
12. Add a number of seconds to a timestamp.
13. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run the flow in **Test your Bot** and confirm the expected node/path executes.
- If the change must affect live traffic, use **Save & Deploy** and verify on the target channel.

### Troubleshooting
- Add a property and its value, or name-value pair, to a JSON object, and return the updated object. If the object already exists at runtime the function throws an error.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Bot Studio**.
- Go to **Functions from A - D**.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Functions from A - D

**Module**: Bot Studio

## Overview
Return the absolute value of the specified number.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### abs

Return the absolute value of the specified number.

```
abs(<number>)
```

Examples

These examples compute the absolute value:

```
abs(3.12134)
abs(-3.12134)
```

And both return the result 3.12134.

### add

Return the result from adding two or more numbers (pure number case) or concatenating two or more strings (other case).

```
add(<item1>, <item2>, ...)
```

Example

This example adds the specified numbers:

```
add(1, 1.5)
```

And returns the result 2.5.

This example concatenates the specified items:

```
add('hello',null)
add('hello','world')
```

And returns the results

- hello
- helloworld
### addDays

Add a number of days to a timestamp in an optional locale format.

```
addDays('<timestamp>', <days>, '<format>'?, '<locale>'?)
```

Example 1

This example adds 10 days to the specified timestamp:

```
addDays('2018-03-15T13:00:00.000Z', 10)
```

And returns the result 2018-03-25T00:00:00.000Z.

Example 2

This example subtracts five days from the specified timestamp:

```
addDays('2018-03-15T00:00:00.000Z', -5)
```

And returns the result 2018-03-10T00:00:00.000Z.

Example 3

This example adds 1 day to the specified timestamp in the de-DE locale:

```
addDays('2018-03-15T13:00:00.000Z', 1, '', 'de-dE')
```

And returns the result 16.03.18 13:00:00.

### addHours

Add a number of hours to a timestamp in an optional locale format.

```
addHours('<timestamp>', <hours>, '<format>'?, '<locale>'?)
```

Example 1

This example adds 10 hours to the specified timestamp:

```
addHours('2018-03-15T00:00:00.000Z', 10)
```

And returns the result 2018-03-15T10:00:00.000Z.

Example 2

This example subtracts five hours from the specified timestamp:

```
addHours('2018-03-15T15:00:00.000Z', -5)
```

And returns the result 2018-03-15T10:00:00.000Z.

Example 3

This example adds 2 hours to the specified timestamp in the de-DE locale:

```
addHours('2018-03-15T13:00:00.000Z', 2, '', 'de-DE')
```

And returns the result 15.03.18 15:00:00.

### addMinutes

Add a number of minutes to a timestamp in an optional locale format.

```
addMinutes('<timestamp>', <minutes>, '<format>'?, '<locale>'?)
```

Example 1

This example adds 10 minutes to the specified timestamp:

```
addMinutes('2018-03-15T00:10:00.000Z', 10)
```

And returns the result 2018-03-15T00:20:00.000Z.

Example 2

This example subtracts five minutes from the specified timestamp:

```
addMinutes('2018-03-15T00:20:00.000Z', -5)
```

And returns the result 2018-03-15T00:15:00.000Z.

Example 3

This example adds 30 minutes to the specified timestamp in the de-DE locale:

```
addMinutes('2018-03-15T00:00:00.000Z', 30, '', 'de-DE')
```

And returns the result 15.03.18 13:30:00.

### addOrdinal

Return the ordinal number of the input number.

```
addOrdinal(<number>)
```

Example

```
addOrdinal(11)
addOrdinal(12)
addOrdinal(13)
addOrdinal(21)
addOrdinal(22)
addOrdinal(23)
```

And respectively returns these results:

- 11th
- 12th
- 13th
- 21st
- 22nd
- 23rd
### addProperty

Add a property and its value, or name-value pair, to a JSON object, and return the updated object. If the object already exists at runtime the function throws an error.

```
addProperty('<object>', '<property>', value)
```

Example

This example adds the accountNumber property to the customerProfile object, which is converted to JSON with the json() function. The function assigns a value that is generated by the newGuid() function, and returns the updated object:

```
addProperty(json('customerProfile'), 'accountNumber', newGuid())
```

### addSeconds

Add a number of seconds to a timestamp.

```
addSeconds('<timestamp>', <seconds>, '<format>'?)
```

Example 1

This example adds 10 seconds to the specified timestamp:

```
addSeconds('2018-03-15T00:00:00.000Z', 10)
```

And returns the result 2018-03-15T00:00:10.000Z.

Example 2

This example subtracts five seconds to the specified timestamp:

```
addSeconds('2018-03-15T00:00:30.000Z', -5)
```

And returns the result 2018-03-15T00:00:25.000Z.

### addToTime

Add a number of time units to a timestamp in an optional locale format. See also getFutureTime().

```
addToTime('<timestamp>', '<interval>', <timeUnit>, '<format>'?, '<locale>'?)
```

Example 1

This example adds one day to specified timestamp.

```
addToTime('2018-01-01T00:00:00.000Z', 1, 'Day')
```

And returns the result 2018-01-02T00:00:00.000Z.

Example 2

This example adds two weeks to the specified timestamp.

```
addToTime('2018-01-01T00:00:00.000Z', 2, 'Week', 'MM-DD-YY')
```

And returns the result in the 'MM-DD-YY' format as 01-15-18.

### all

Determine whether all elements of a sequence satisfy a condition.

```
all(<sequence>, <item>, <condition>)
```

Examples

These examples determine if all elements of a sequence satisfy a condition:

```
all(createArray(1, 'cool'), item, isInteger(item))
all(createArray(1, 2), item => isInteger(item))
```

And return the following results respectively:

- false, because both items in the sequence aren't integers.
- true, because both items in the sequence are integers.
### and

Check whether all expressions are true. Return true if all expressions are true, or return false if at least one expression is false.

```
and(<expression1>, <expression2>, ...)
```

Example 1

These examples check whether the specified Boolean values are all true:

```
and(true, true)
and(false, true)
and(false, false)
```

And respectively returns these results:

- Both expressions are true, so the functions returns true.
- One expression is false, so the functions returns false.
- Both expressions are false, so the function returns false.
Example 2

These examples check whether the specified expressions are all true:

```
and(equals(1, 1), equals(2, 2))
and(equals(1, 1), equals(1, 2))
and(equals(1, 2), equals(1, 3))
```

And respectively returns these results:

- Both expressions are true, so the functions returns true.
- One expression is false, so the functions returns false.
- Both expressions are false, so the functions returns false.
### any

Determine whether any elements of a sequence satisfy a condition.

```
all(<sequence>, <item>, <condition>)
```

Examples

These examples determine if all elements of a sequence satisfy a condition:

```
any(createArray(1, 'cool'), item, isInteger(item))
any(createArray('first', 'cool'), item => isInteger(item))
```

And return the following results respectively:

- true, because at least one item in the sequence is an integer
- false, because neither item in the sequence is an integer.
### average

Return the number average of a numeric array.

```
average(<numericArray>)
```

Example

This example calculates the average of the array in createArray():

```
average(createArray(1,2,3))
```

And returns the result 2.

### base64

Return the base64-encoded version of a string or byte array.

```
base64('<value>')
```

Example 1

This example converts the string hello to a base64-encoded string:

```
base64('hello')
```

And returns the result "aGVsbG8=".

Example 2

This example takes byteArr, which equals new byte[] { 3, 5, 1, 12 }:

```
base64('byteArr')
```

And returns the result "AwUBDA==".

### base64ToBinary

Return the binary array of a base64-encoded string.

```
base64ToBinary('<value>')
```

Example

This example converts the base64-encoded string AwUBDA== to a binary string:

```
base64ToBinary('AwUBDA==')
```

And returns the result new byte[] { 3, 5, 1, 12 }.

### base64ToString

Return the string version of a base64-encoded string, effectively decoding the base64 string.

```
base64ToString('<value>')
```

Example

This example converts the base64-encoded string aGVsbG8= to a decoded string:

```
base64ToString('aGVsbG8=')
```

And returns the result hello.

### binary

Return the binary version of a string.

```
binary('<value>')
```

Example

This example converts the string hello to a binary string:

```
binary('hello')
```

And returns the result new byte[] { 104, 101, 108, 108, 111 }.

### bool

Return the Boolean version of a value.

```
bool(<value>)
```

Example

These examples convert the specified values to Boolean values:

```
bool(1)
bool(0)
```

And respectively returns these results:

- true
- false
### ceiling

Return the largest integral value less than or equal to the specified number.

```
ceiling('<number>')
```

Example

This example returns the largest integral value less than or equal to the number 10.333:

```
ceiling(10.333)
```

And returns the integer 11.

### coalesce

Return the first non-null value from one or more parameters. Empty strings, empty arrays, and empty objects are not null.

```
coalesce(<object**1>, <object**2>, ...)
```

Example

These examples return the first non-null value from the specified values, or null when all the values are null:

```
coalesce(null, true, false)
coalesce(null, 'hello', 'world')
coalesce(null, null, null)
```

And respectively return:

- true
- hello
- null
### concat

Combine two or more objects, and return the combined objects in a list or string.

```
concat('<text1>', '<text2>', ...)
```

Expected return values:

- If all items are lists, a list will be returned.
- If there exists an item that isn't a list, a string will be returned.
- If a value is null, it's skipped and not concatenated.
Example

This example combines the strings Hello and World:

```
concat('Hello', 'World')
```

And returns the result HelloWorld.

Example 2

This example combines the lists [1,2] and [3,4]:

```
concat([1,2],[3,4])
```

And returns the result [1,2,3,4].

Example 3

These examples combine objects of different types:

```
concat('a', 'b', 1, 2)
concat('a', [1,2])
```

And return the following results respectively:

- The string ab12.
- The object aSystem.Collections.Generic.List 1[System.Object]. This is unreadable and best to avoid.
Example 4

These examples combine objects will null:

```
concat([1,2], null)
concat('a', 1, null)
```

And return the following results respectively:

- The list [1,2].
- The string a1.
### contains

Check whether a collection has a specific item. Return true if the item is found, or return false if not found. This function is case-sensitive.

```
contains('<collection>', '<value>')
contains([<collection>], '<value>')
```

This function works on the following collection types:

- A string to find a substring
- An array to find a value
- A dictionary to find a key
Example 1

This example checks the string hello world for the substring world:

```
contains('hello world', 'world')
```

And returns the result true.

Example 2

This example checks the string hello world for the substring universe:

```
contains('hello world', 'universe')
```

And returns the result false.

### count

Return the number of items in a collection.

```
count('<collection>')
count([<collection>])
```

Examples:

These examples count the number of items in these collections:

```
count('abcd')
count(createArray(0, 1, 2, 3))
```

And both return the result 4.

### countWord

Return the number of words in a string

```
countWord('<text>')
```

Example

This example counts the number of words in the string hello world:

```
countWord("hello word")
```

And it returns the result 2.

### convertFromUTC

Convert a timestamp in an optional locale format from Universal Time Coordinated (UTC) to a target time zone.

```
convertFromUTC('<timestamp>', '<destinationTimeZone>', '<format>'?, '<locale>'?)
```

Examples:

These examples convert from UTC to Pacific Standard Time:

```
convertFromUTC('2018-02-02T02:00:00.000Z', 'Pacific Standard Time', 'MM-DD-YY')
convertFromUTC('2018-02-02T02:00:00.000Z', 'Pacific Standard Time')
```

And respectively return these results:

- 02-01-18
- 2018-01-01T18:00:00.0000000
Example 2

This example converts a timestamp in the en-US locale from UTC to Pacific Standard Time:

```
convertFromUTC('2018-01-02T02:00:00.000Z', 'Pacific Standard Time', 'D', 'en-US')
```

And returns the result Monday, January 1, 2018.

### convertToUTC

Convert a timestamp in an optional locale format to Universal Time Coordinated (UTC) from the source time zone.

```
convertToUTC('<timestamp>', '<sourceTimeZone>', '<format>'?, '<locale>'?)
```

Example

This example converts a timestamp to UTC from Pacific Standard Time

```
convertToUTC('01/01/2018 00:00:00', 'Pacific Standard Time')
```

And returns the result 2018-01-01T08:00:00.000Z.

Example 2

This example converts a timestamp in the de-DE locale to UTC from Pacific Standard Time:

```
convertToUTC('01/01/2018 00:00:00', 'Pacific Standard Time', '', 'de-DE')
```

And returns the result 01.01.18 08:00:00.

### createArray

Return an array from multiple inputs.

```
createArray('<object1>', '<object2>', ...)
```

Example

This example creates an array from the following inputs:

```
createArray('h', 'e', 'l', 'l', 'o')
```

And returns the result [h ,e, l, l, o].

### dataUri

Return a data uniform resource identifier (URI) of a string.

```
dataUri('<value>')
```

Example

```
dataUri('hello')
```

Returns the result data:text/plain;charset=utf-8;base64,aGVsbG8=.

### dataUriToBinary

Return the binary version of a data uniform resource identifier (URI).

```
dataUriToBinary('<value>')
```

Example

This example creates a binary version for the following data URI:

```
dataUriToBinary('aGVsbG8=')
```

And returns the result new byte[] { 97, 71, 86, 115, 98, 71, 56, 61 }.

### dataUriToString

Return the string version of a data uniform resource identifier (URI).

```
dataUriToString('<value>')
```

Example

This example creates a string from the following data URI:

```
dataUriToString('data:text/plain;charset=utf-8;base64,aGVsbG8=')
```

And returns the result hello.

### date

Return the date of a specified timestamp in m/dd/yyyy format.

```
date('<timestramp>')
```

```
date('2018-03-15T13:00:00.000Z')
```

Returns the result 3-15-2018.

### dateReadBack

Uses the date-time library to provide a date readback.

```
dateReadBack('<currentDate>', '<targetDate>')
```

Example 1

```
dateReadBack('2018-03-15T13:00:00.000Z', '2018-03-16T13:00:00.000Z')
```

Returns the result tomorrow.

### dateTimeDiff

Return the difference in ticks between two timestamps.

```
dateTimeDiff('<timestamp1>', '<timestamp2>')
```

Example 1

This example returns the difference in ticks between two timestamps:

```
dateTimeDiff('2019-01-01T08:00:00.000Z','2018-01-01T08:00:00.000Z')
```

And returns the number 315360000000000.

Example 2

This example returns the difference in ticks between two timestamps:

```
dateTimeDiff('2018-01-01T08:00:00.000Z', '2019-01-01T08:00:00.000Z')
```

Returns the result -315360000000000. The value is a negative number.

### dayOfMonth

Return the day of the month from a timestamp.

```
dayOfMonth('<timestamp>')
```

Example

This example returns the number for the day of the month from the following timestamp:

```
dayOfMonth('2018-03-15T13:27:36Z')
```

And returns the result 15.

### dayOfWeek

Return the day of the week from a timestamp.

```
dayOfWeek('<timestamp>')
```

Example

This example returns the number for the day of the week from the following timestamp:

```
dayOfWeek('2018-03-15T13:27:36Z')
```

And returns the result 3.

### dayOfYear

Return the day of the year from a timestamp.

```
dayOfYear('<timestamp>')
```

Example

This example returns the number of the day of the year from the following timestamp:

```
dayOfYear('2018-03-15T13:27:36Z')
```

And returns the result 74.

### div

Return the integer result from dividing two numbers. To return the remainder see mod().

```
div(<dividend>, <divisor>)
```

Example

Both examples divide the first number by the second number:

```
div(10, 5)
div(11, 5)
```

And return the result 2.

There exists some gap between Javascript and .NET SDK. For example, the following expression will return different results in Javascript and .NET SDK:

If one of the parameters is a float, the result will also be a FLOAT with .NET SDK.

Example

```
div(11.2, 2)
```

Returns the result 5.6.

If one of the parameters is a float, the result will be an INT with Javascript SDK.

Example

```
div(11.2, 2)
```

Returns the result 5.

The workaround for Javascript to keep a certain number of decimal places in results is to use such expression. For example, to keep 3 decimal places:

```
float(concat(string(div(a, b)),'.',string(mod(div(a*1000, b), 1000))))
```

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
