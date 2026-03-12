source_url: https://console-docs.gupshup.io/docs/functions-from-i-l

<!-- kb-golden:v4 -->
# Functions from I - L

**Module**: Bot Studio

## Definition
Check whether an expression is true or false. Based on the result, return a specified value.

## Procedure
### Exact path
Gupshup Console → Bot Studio → Functions from I - L

### Where to configure it
Gupshup Console → Bot Studio → Functions from I - L

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Functions from I - L**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- if
- indexOf
- indicesAndValues
- int
- intersection
- isArray
- isBoolean
- isDate
- isDateRange
- isDateTime

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
# Functions from I - L

**Module**: Bot Studio

## Overview
Check whether an expression is true or false. Based on the result, return a specified value.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### if

Check whether an expression is true or false. Based on the result, return a specified value.

```
if(<expression>, <valueIfTrue>, <valueIfFalse>)
```

Example

This example evaluates whether equals(1,1) is true:

```
if(equals(1, 1), 'yes', 'no')
```

And returns yes because the specified expression returns true. Otherwise, the example returns no.

### indexOf

Return the starting position or index value of a substring. This function is case-insensitive, and indexes start with the number 0.

```
indexOf('<text>', '<searchText>')
```

Example 1

This example finds the starting index value of the substring world in the string hello world:

```
indexOf('hello world', 'world')
```

And returns the result 6.

Example 2

This example finds the starting index value of the substring def in the array ['abc', 'def', 'ghi']:

```
indexOf(createArray('abc', 'def', 'ghi'), 'def')
```

And returns the result 1.

### indicesAndValues

Turn an array or object into an array of objects with index (current index) and value properties. For arrays, the index is the position in the array. For objects, it's the key for the value.

```
indicesAndValues('<collection or object>')
```

Example 1

Say you have a list { items:["zero", "one", "two"] }. The following function takes that list:

```
indicesAndValues(items)
```

And returns a new list:

```
[
  {
    index: 0,
    value: 'zero'
  },
  {
    index: 1,
    value: 'one'
  },
  {
    index: 2,
    value: 'two'
  }
]
```

Example 2

Say you have a list { items:["zero", "one", "two"] }. The following function takes that list:

```
where(indicesAndValues(items), elt, elt.index >= 1)
```

And returns a new list:

```
[
  {
    index: 1,
    value: 'one'
  },
  {
    index: 2,
    value: 'two'
  }
]
```

Example 3

Say you have a list { items:["zero", "one", "two"] }. The following function takes that list:

```
join(foreach(indicesAndValues(items), item, item.value), ',')
```

And returns the result zero,one,two. This expression has the same effect as join(items, ',').

Example 4

Say you have an object { user: {name: 'jack', age: 20} }. The following function takes that object:

```
indicesAndValues(user)
```

And returns a new object:

```
[
  {
    index: 'name',
    value: 'jack'
  },
  {
    index: 'age',
    value: 20
  }
]
```

### int

Return the integer version of a string. An exception will be thrown if the string can't be converted to an integer.

```
int('<value>')
```

Example

This example creates an integer version for the string 10:

```
int('10')
```

And returns the result as the integer 10.

### intersection

Return a collection that has only the common items across the specified collections. To appear in the result, an item must appear in all the collections passed to this function. If one or more items have the same name, the last item with that name appears in the result.

```
intersection([<collection1>], [<collection2>], ...)
intersection('<collection1>', '<collection2>', ...)
```

Example

This example finds the common items across the following arrays:

```
intersection(createArray(1, 2, 3), createArray(101, 2, 1, 10), createArray(6, 8, 1, 2))
```

And returns an array with only the items [1, 2].

### isArray

Return true if a given input is an array.

```
isArray('<input>')
```

Examples

The following examples check if the input is an array:

```
isArray('hello')
isArray(createArray('hello', 'world'))
```

And return the following results respectively:

- The input is a string, so the function returns false.
- The input is an array, so the function returns true.
### isBoolean

Return true if a given input is a Boolean.

```
isBoolean('<input>')
```

Examples

The following examples check if the input is a Boolean:

```
isBoolean('hello')
isBoolean(32 > 16)
```

And return the following results respectively:

- The input is a string, so the function returns false.
- The input is a Boolean, so the function returns true.
### isDate

Return true if a given TimexProperty or Timex expression refers to a valid date. Valid dates contain the month and dayOfMonth, or contain the dayOfWeek.

```
isDate('<input>')
```

Examples

These examples check if the following inputs are valid dates:

```
isDate('2020-12')
isDate('xxxx-12-21')
```

And return the following results:

- false
- true
### isDateRange

Return true if a given TimexProperty or Timex expression refers to a valid date range.

```
isDateRange('<input>')
```

Examples

These examples check if the following input is a valid date range:

```
isDateRange('PT30M')
isDateRange('2012-02')
```

And return the following results:

- false
- true
### isDateTime

Return true if a given input is a UTC ISO format (YYYY-MM-DDTHH:mm:ss.fffZ) timestamp string.

```
isDateTime('<input>')
```

Examples

The following examples check if the input is a UTC ISO format string:

```
isDateTime('hello world!')
isDateTime('2019-03-01T00:00:00.000Z')
```

And return the following results respectively:

- The input is a string, so the function returns false.
- The input is a UTC ISO format string, so the function returns true.
### isDefinite

Return true if a given TimexProperty or Timex expression refers to a valid date. Valid dates contain the year, month and dayOfMonth.

```
isDefinite('<input>')
```

Examples

Suppose there is a TimexProperty object validFullDate = new TimexProperty("2020-02-20") and the Now property is set to true. The following examples check if the object refers a valid full date:

```
isDefinite('xxxx-12-21')
isDefinite(validFullDate)
```

And return the following results respectively:

- false
- true
### isDuration

Return true if a given TimexProperty or Timex expression refers to a valid duration.

```
isDuration('<input>')
```

Examples

The examples below check if the following input refers to a valid duration:

```
isDuration('PT30M')
isDuration('2012-02')
```

And return the following results respectively:

- true
- false
### isFloat

Return true if a given input is a floating-point number. Due to the alignment between C#and JavaScript, a number with an non-zero residue of its modulo 1 will be treated as a floating-point number.

```
isFloat('<input>')
```

Examples

The following examples check if the input is a floating-point number:

```
isFloat('hello world!')
isFloat(1.0)
isFloat(12.01)
```

And return the following results respectively:

- The input is a string, so the function returns false.
- The input has a modulo that equals 0, so the function returns false.
- The input is a floating-point number, so the function returns true.
### isInteger

Return true if a given input is an integer number. Due to the alignment between C# and JavaScript, a number with an zero residue of its modulo 1 will be treated as an integer number.

```
isInteger('<input>')
```

Examples

The following examples check if the input is an integer:

```
isInteger('hello world!')
isInteger(1.0)
isInteger(12)
```

And return the following results respectively:

- The input is a string, so the function returns false.
- The input has a modulo that equals 0, so the function returns true.
- The input is an integer, so the function returns true.
### isObject

Return true if a given input is a complex object or return false if it's a primitive object. Primitive objects include strings, numbers, and Booleans; complex types, like classes, contain properties.

```
isObject('<input>')
```

Examples

The following examples check if the given input is an object:

isObject('hello world!') isObject({userName: "Sam"})

And return the following results respectively:

- The input is a string, so the function returns false.
- The input is an object, so the function returns true.
### isPresent

Return true if a given TimexProperty or Timex expression refers to the present.

```
isPresent('<input>')
```

Examples Suppose we have an TimexProperty object validNow = new TimexProperty() { Now = true } and set the Now property to true. The examples below check if the following input refers to the present:

isPresent('PT30M') isPresent(validNow)

And return the following results respectively:

- false
- true
### isString

Return true if a given input is a string.

```
isString('<input>')
```

Examples

The following examples check if the given input is a string:

isString('hello world!') isString(3.14)

And return the following results respectively:

- The input is a string, so the function returns true.
- The input is a float, so the function returns false.
### isTime

Return true if a given TimexProperty or Timex expression refers to a valid time. Valid time contains hours, minutes and seconds.

```
isTime('<input>')
```

Examples

These examples check if the following input refers to a valid time:

isTime('PT30M') isTime('2012-02-21T12:30:45')

And return the following results respectively:

- false
- true
### isTimeRange

Return true if a given TimexProperty or Timex expression refers to a valid time range Valid time ranges contain partOfDay.

```
isTime('<input>')
```

Examples

Suppose we have an TimexProperty object validTimeRange = new TimexProperty() { PartOfDay = "morning" } and set the Now property to true. These examples check if the following inputs are valid time ranges:

isTimeRange('PT30M') isTimeRange(validTimeRange)

And return the following results respectively:

- false
- true
### join

Return a string that has all the items from an array, with each character separated by a delimiter.

```
join([<collection>], '<delimiter>')
```

Example

This example creates a string from all the items in this array with the specified character . as the delimiter:

join(createArray('a', 'b', 'c'), '.')

And returns the result a.b.c.

### json

Return the JavaScript Object Notation (JSON) type value or object of a string or XML.

```
json('<value>')
```

Example 1

This example converts a string to JSON:

json('{"fullName": "Sophia Owen"}')

And returns the result:

{ "fullName": "Sophia Owen" }

Example 2

This example converts XML to JSON:

```
json(xml('<?xml version="1.0"?> <root> <person id='1'> <name>Sophia Owen</name> <occupation>Engineer</occupation> </person> </root>'))
```

And returns the result:

```
{  
   "?xml": { "@version": "1.0" },  
   "root": {  
      "person": [ {  
         "@id": "1",  
         "name": "Sophia Owen",  
         "occupation": "Engineer"  
      } ]  
   }  
}
```

### jsonStringify

Return the JSON string of a value.

Examples

These examples show objects converted to JSON strings:

jsonStringify(null) jsonStringify({a:'b'})

And return the following string results respectively:

- null
- {"a":"b"}
### last

Return the last item from a collection.

```
last('<collection>')  
last([<collection>])
```

Example

These examples find the last item in these collections:

last('abcd') last(createArray(0, 1, 2, 3))

And returns the following results respectively:

- d
- 3
### lastIndexOf

Return the starting position or index value of the last occurrence of a substring. This function is case-insensitive, and indexes start with the number 0.

```
lastIndexOf('<text>', '<searchText>')
```

Example 1

This example finds the starting index value of the last occurrence of the substring world in the hello world string:

lastIndexOf('hello world', 'world')

And returns the result 6.

Example 2

This example finds the starting index value of the last occurrence of substring def in the array ['abc', 'def', 'ghi', 'def'].

lastIndexOf(createArray('abc', 'def', 'ghi', 'def'), 'def')

And returns the result 3.

### length

Return the length of a string.

```
length('<str>')
```

Examples

These examples get the length of strings:

length('hello') length('hello world')

And returns the following results respectively:

- 5
- 11
### less

Check whether the first value is less than the second value. Return true if the first value is less, or return false if the first value is more.

```
less(<value>, <compareTo>)  
less('<value>', '<compareTo>')
```

Examples

These examples check whether the first value is less than the second value.

less(5, 10) less('banana', 'apple')

And return the following results respectively:

- true
- false
### lessOrEquals

Check whether the first value is less than or equal to the second value. Return true if the first value is less than or equal, or return false if the first value is more.

```
lessOrEquals(<value>, <compareTo>)  
lessOrEquals('<value>', '<compareTo>')
```

Example

These examples check whether the first value is less than or equal to the second value.

lessOrEquals(10, 10) lessOrEquals('apply', 'apple')

And return the following results respectively:

- true
- false

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
