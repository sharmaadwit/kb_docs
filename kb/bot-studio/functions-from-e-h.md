source_url: https://console-docs.gupshup.io/docs/functions-from-e-h

<!-- kb-golden:v7 -->
# Functions from E - H

**Module**: Bot Studio

## Definition
Check whether an instance is empty. Return true if the input is empty. Empty means:

## Procedure
### Exact path
Gupshup Console → Bot Studio → Functions from E - H

### Where to configure it
Gupshup Console → Bot Studio → Functions from E - H

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **Functions from E - H**.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Functions from E - H**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- empty
- endsWith
- EOL
- equals
- exists
- exp
- first
- flatten
- float
- floor

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
# Functions from E - H

**Module**: Bot Studio

## Overview
Check whether an instance is empty. Return true if the input is empty. Empty means:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### empty

Check whether an instance is empty. Return true if the input is empty. Empty means:

- input is null or undefined
- input is a null or empty string
- input is zero size collection
- input is an object with no property.
```
empty('<instance>')
empty([<instance>])
```

Example

These examples check whether the specified instance is empty:

```
empty('')
empty('abc')
empty([1])
empty(null)
```

And return these results respectively:

- Passes an empty string, so the function returns true.
- Passes the string abc, so the function returns false.
- Passes the collection with one item, so the function returns false.
- Passes the null object, so the function returns true.
### endsWith

Check whether a string ends with a specific substring. Return true if the substring is found, or return false if not found. This function is case-insensitive.

```
endsWith('<text>', '<searchText>')
```

Example 1

This example checks whether the hello world string ends with the string world:

```
endsWith('hello world', 'world')
```

And it returns the result true.

Example 2

This example checks whether the hello world string ends with the string universe:

```
endsWith('hello world', 'universe')
```

And it returns the result false.

### EOL

Return the end of line (EOL) sequence text.

```
EOL()
```

Example

This example checks the end of the line sequence text:

```
EOL()
```

And returns the following strings:

- Windows: \r\n
- Mac or Linux: \n
### equals

Check whether both values, expressions, or objects are equivalent. Return true if both are equivalent, or return false if they're not equivalent.

```
equals('<object1>', '<object2>')
```

Example

These examples check whether the specified inputs are equivalent:

```
equals(true, 1)
equals('abc', 'abcd')
```

And returns these results respectively:

- Both values are equivalent, so the function returns true.
- Both values aren't equivalent, so the function returns false.
### exists

Evaluates an expression for truthiness.

```
exists(expression)
```

Example

These example evaluate the truthiness of foo = {"bar":"value"}:

```
exists(foo.bar)
exists(foo.bar2)
```

And return these results respectively:

- true
- false
### exp

Return exponentiation of one number to another.

```
exp(realNumber, exponentNumber)
```

Example

This example computes the exponent:

```
exp(2, 2)
```

And returns the result 4.

### first

Return the first item from a string or array.

```
first('<collection>')
first([<collection>])
```

Example

These examples find the first item in the following collections:

```
first('hello')
first(createArray(0, 1, 2))
```

And return these results respectively:

- h
- 0
### flatten

Flatten an array into non-array values. You can optionally set the maximum depth to flatten to.

```
flatten([<collection>], '<depth>')
```

Example 1

THis example flattens the following array:

```
flatten(createArray(1, createArray(2), createArray(createArray(3, 4), createArray(5, 6)))
```

And returns the result [1, 2, 3, 4, 5, 6].

Example 2

This example flattens the array to a depth of 1:

```
flatten(createArray(1, createArray(2), createArray(createArray(3, 4), createArray(5, 6)), 1)
```

And returns the result [1, 2,[3, 4], [5, 6]].

### float

Convert the string version of a floating-point number to a floating-point number. You can use this function only when passing custom parameters to an app, such as a logic app. An exception will be thrown if the string can't be converted to a float.

```
float('<value>')
```

Example

This example converts the float version of a string:

```
float('10.333')
```

And returns the float 10.333.

### floor

Return the largest integral value less than or equal to the specified number.

```
floor('<number>')
```

Example

This example calculates the floor value of the number 10.333:

```
floor(10.333)
```

And returns the integer 10.

### foreach

Operate on each element and return the new collection.

```
foreach([<collection/instance>], <iteratorName>, <function>)
```

Example 1

This example generates a new collection:

```
foreach(createArray(0, 1, 2, 3), x, x + 1)
```

And returns the result [1, 2, 3, 4].

Example 2

These examples generate a new collection:

```
foreach(json("{'name': 'jack', 'age': '15'}"), x, concat(x.key, ':', x.value))
foreach(json("{'name': 'jack', 'age': '15'}"), x=> concat(x.key, ':', x.value))
```

And return the result ['name:jack', 'age:15']. Note that the second expression is a lambda expression, which some find more readable.

### formatDateTime

Return a timestamp in an optional locale format.

```
formatDateTime('<timestamp>', '<format>'?, '<locale>'?)
```

Example 1

This example converts a timestamp to the specified format:

```
formatDateTime('03/15/2018 12:00:00', 'yyyy-MM-ddTHH:mm:ss')
```

And returns the result 2018-03-15T12:00:00.

Example 2

This example converts a timestamp in the de-DE locale:

```
formatDateTime('2018-03-15', '', 'de-DE')
```

And returns the result 15.03.18 00:00:00.

### formatEpoch

Return a timestamp in an optional locale format in the specified format from UNIX time (also know as Epoch time, POSIX time, UNIX Epoch time).

```
formatEpoch('<epoch>', '<format>'?, '<locale>'?)
```

Example

This example converts a Unix timestamp to the specified format:

```
formatEpoch(1521118800, 'yyyy-MM-ddTHH:mm:ss.fffZ)'
```

And returns the result 2018-03-15T12:00:00.000Z.

Example

This example converts a Unix timestamp in the de-DE locale:

```
formatEpoch(1521118800, '', 'de-DE')
```

And returns the result 15.03.18 13:00:00.

### formatNumber

Format a value to the specified number of fractional digits and an optional specified locale.

```
formatNumber('<number>', '<precision-digits>', '<locale>'?)
```

Example 1

This example formats the number 10.333 to 2 fractional digits:

```
formatNumber(10.333, 2)
```

And returns the string 10.33.

Example 2

These examples format numbers to a specified number of digits in the en-US locale:

```
formatNumber(12.123, 2, 'en-US')
formatNumber(1.551, 2, 'en-US')
formatNumber(12.123, 4, 'en-US')
```

And return the following results respectively:

- 12.12
- 1.55
- 12.1230
### formatTicks

Return a timestamp in an optional locale format in the specified format from ticks.

```
formatTicks('<ticks>', '<format>'?, '<locale>'?)
```

Example 1

This example converts ticks to the specified format:

```
formatTicks(637243624200000000, 'yyyy-MM-ddTHH:mm:ss.fffZ')
```

And returns the result 2020-05-06T11:47:00.000Z.

Example 2

This example converts ticks to the specified format in the de-DE locale:

```
formatTicks(637243624200000000, '', 'de-DE')
```

And returns the result 06.05.20 11:47:00.

### getFutureTime

Return the current timestamp in an optional locale format plus the specified time units.

```
getFutureTime(<interval>, <timeUnit>, '<format>'?, '<locale>'?)
```

Example 1

Suppose the current timestamp is 2019-03-01T00:00:00.000Z. The example below adds five days to that timestamp:

```
getFutureTime(2, 'Week')
```

And returns the result 2019-03-15T00:00:00.000Z.

Example 2

Suppose the current timestamp is 2018-03-01T00:00:00.000Z. The example below adds five days to the timestamp and converts the result to MM-DD-YY format:

```
getFutureTime(5, 'Day', 'MM-DD-YY')
```

And returns the result 03-06-18.

Example 3

Suppose the current timestamp is 2020-05-01T00:00:00.000Z and the locale is de-DE. The example below adds 1 day to the timestamp:

```
getFutureTime(1,'Day', '', 'de-DE')
```

And returns the result 02.05.20 00:00:00.

### getNextViableDate

Return the next viable date of a Timex expression based on the current date and an optionally specified timezone.

```
getNextViableDate(<timexString>, <timezone>?)
```

Examples

Say the date is 2020-06-12 and current time is 15:42:21.

These examples evaluate the Timex string for the next viable date based on the above date and time:

```
getPreviousViableDate("XXXX-12-20", "America/Los_Angeles")
getPreviousViableDate("XXXX-02-29")
```

And return the following strings respectively:

- 2020-12-20
- 2024-02-29
### getNextViableTime

Return the next viable time of a Timex expression based on the current time and an optionally specified timezone.

```
getNextViableTime(<timexString>, <timezone>?)
```

Examples

Say the date is 2020-06-12 and current time is 15:42:21.

These examples evaluate a Timex string for the next viable time based on the above date and time:

```
getNextViableTime("TXX:12:14", "Asia/Tokyo")
getNextViableTime("TXX:52:14")
```

And return the following strings respectively:

- T16:12:14
- T15:52:14
### getPastTime

Return the current timestamp minus the specified time units.

```
getPastTime(<interval>, <timeUnit>, '<format>'?)
```

Example 1

Suppose the current timestamp is 2018-02-01T00:00:00.000Z. This example subtracts five days from that timestamp:

```
getPastTime(5, 'Day')
```

And returns the result 2019-01-27T00:00:00.000Z.

Example 2

Suppose the current timestamp is 2018-03-01T00:00:00.000Z. This example subtracts five days to the timestamp in the MM-DD-YY format:

```
getPastTime(5, 'Day', 'MM-DD-YY')
```

And returns the result 02-26-18.

Example 3

Suppose the current timestamp is 2020-05-01T00:00:00.000Z and the locale is de-DE. The example below subtracts 1 day from the timestamp:

```
getPastTime(1,'Day', '', 'de-DE')
```

And returns the result 31.04.20 00:00:00.

### getPreviousViableDate

Return the previous viable date of a Timex expression based on the current date and an optionally specified timezone.

```
getPreviousViableDate(<timexString>, <timezone>?)
```

Examples

Say the date is 2020-06-12 and current time is 15:42:21.

These examples evaluate a Timex string for the previous viable date based on the above date and time:

```
getPreviousViableDate("XXXX-12-20", "Eastern Standard Time")
getPreviousViableDate("XXXX-02-29")
```

And return the following strings respectively:

- 2019-12-20
- 2020-02-29
### getPreviousViableTime

Return the previous viable time of a Timex expression based on the current date and an optionally specified timezone.

```
getPreviousViableTime(<timexString>, <timezone>?)
```

Examples

Say the date is 2020-06-12 and current time is 15:42:21.

These examples evaluate a Timex string for the previous viable time based on the above date and time:

```
getPreviousViableTime("TXX:52:14")
getPreviousViableTime("TXX:12:14", 'Europe/London')
```

And return the following strings respectively:

- T14:52:14
- T15:12:14
### getProperty

Return the value of a specified property or the root property from a JSON object.

#### Return the value of a specified property

```
getProperty(<JSONObject>, '<propertyName>')
```

Example

Say you have the following JSON object:

```
{
   "a:b" : "a:b value",
   "c":
   {
        "d": "d key"
    }
}
```

These example retrieve a specified property from the above JSON object:

```
getProperty({"a:b": "value"}, 'a:b')
getProperty(c, 'd')
```

And return the following strings respectively:

- a:b value
- d key
#### Return the root property

```
getProperty('<propertyName>')
```

Example

Say you have the following JSON object:

```
{
   "a:b" : "a:b value",
   "c":
   {
        "d": "d key"
    }
}
```

This example retrieves the root property from the above JSON object:

```
getProperty("a:b")
```

And returns the string a:b value.

### getTimeOfDay

Returns time of day for a given timestamp.

```
getTimeOfDay('<timestamp>')
```

Time returned is one of the following strings:

Listed below are the strings associated with the time of day:

Example

```
getTimeOfDay('2018-03-15T08:00:00.000Z')
```

Returns the result morning.

### greater

Check whether the first value is greater than the second value. Return true if the first value is more, or return false if less.

```
greater(<value>, <compareTo>)
greater('<value>', '<compareTo>')
```

Example

These examples check whether the first value is greater than the second value:

```
greater(10, 5)
greater('apple', 'banana')
```

And return the following results respectively:

- true
- false
### greaterOrEquals

Check whether the first value is greater than or equal to the second value. Return true when the first value is greater or equal, or return false if the first value is less.

```
greaterOrEquals(<value>, <compareTo>)
greaterOrEquals('<value>', '<compareTo>')
```

Example

These examples check whether the first value is greater or equal than the second value:

```
greaterOrEquals(5, 5)
greaterOrEquals('apple', 'banana')
```

And return the following results respectively:

- true
- false

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
