source_url: https://console-docs.gupshup.io/docs/functions-from-r-u

<!-- kb-golden:v1 -->
# Functions from R - U

**Module**: Bot Studio

## Definition
Return a random integer from a specified range, which is inclusive only at the starting end.

## Procedure
### Where to configure it
Gupshup Console → Bot Studio → Functions from R - U

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Functions from R - U**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- rand
- range
- removeProperty
- replace
- replaceIgnoreCase
- resolve
- reverse
- round
- select
- sentenceCase

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Reference (from source)
<!-- procedural:v2 -->
# Functions from R - U

**Module**: Bot Studio

## Overview
Return a random integer from a specified range, which is inclusive only at the starting end.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### rand

Return a random integer from a specified range, which is inclusive only at the starting end.

```
rand(<minValue>, <maxValue>)
```

Example

This example gets a random integer from the specified range, excluding the maximum value:

```
rand(1, 5)
```

And returns 1, 2, 3, or 4 as the result.

### range

Return an integer array that starts from a specified integer.

```
range(<startIndex>, <count>)
```

Example

This example creates an integer array that starts from the specified index 1 and has the specified number of integers as 4:

```
range(1, 4)
```

And returns the result [1, 2, 3, 4].

### removeProperty

Remove a property from an object and return the updated object.

```
removeProperty(<object>, '<property>')
```

Example

This example removes the accountLocation property from a customerProfile object, which is converted to JSON with the json() function, and returns the updated object:

```
removeProperty(json('customerProfile'), 'accountLocation')
```

### replace

Replace a substring with the specified string, and return the result string. This function is case-sensitive.

```
replace('<text>', '<oldText>', '<newText>')
```

Example 1

This example finds the substring old in the old string and replaces old with new:

```
replace('the old string', 'old', 'new')
```

The result is the string the new string.

Example 2

When dealing with escape characters, the expression engine handles the unescape for you. This function replaces strings with escape characters.

```
replace('hello\"', '\"', '\\n')  
replace('hello\\n', '\\n', '\\\\')  
@"replace('hello\\', '\\', '\\\\')"  
@"replace('hello\\n', '\\n', '\\\\')"
```

And returns the following results respectively:

- hello\n
- hello\\
- @"hello\\"
- @"hello\\"
### replaceIgnoreCase

Replace a substring with the specified string, and return the result string. This function is case-insensitive.

```
replaceIgnoreCase('<text>', '<oldText>', '<newText>')
```

Example

This example finds the substring old in the string the old string and replaces old with new:

```
replace('the old string', 'old', 'new')
```

And returns the result the new string.

### resolve

Return string of a given TimexProperty or Timex expression if it refers to a valid time. Valid time contains hours, minutes, and seconds.

```
resolve('<timestamp>')
```

Examples

These examples show if the given strings refer to valid time:

```
resolve(T14)  
resolve(2020-12-20)  
resolve(2020-12-20T14:20)
```

And returns the following results respectively:

- 14:00:00
- 2020-12-20
- 2020-12-20 14:20:00
### reverse

Reverse the order of the elements in a string or array.

```
reverse(<value>)
```

Examples

These examples reverse the elements of a string or array:

```
reverse(hello)  
reverse(concat(hello,world))
```

And return the following values respectively:

-The string olleh. -The string dlrowolleh.

### round

Round a value to the nearest integer or to the specified number of fractional digits.

```
round('<number>', '<precision-digits>')
```

Example 1

This example rounds the number 10.333:

```
round(10.333)
```

And returns the number 10.

Example 2

This example rounds the number 10.3313 to 2 fractional digits:

```
round(10.3313, 2)
```

And returns the number 10.33.

### select

Operate on each element and return the new collection of transformed elements.

```
select([<collection/instance>], <iteratorName>, <function>)
```

Example 1

This example generates a new collection:

```
select(createArray(0, 1, 2, 3), x, x + 1)
```

And returns the result [1, 2, 3, 4].

Example 2

These examples generate a new collection:

```
select(json("{'name': 'jack', 'age': '15'}"), x, concat(x.key, ':', x.value))  
select(json("{'name': 'jack', 'age': '15'}"), x=> concat(x.key, ':', x.value))
```

And return the result ['name:jack', 'age:15']. Note that the second expression is a lambda expression, which some find more readable.

### sentenceCase

Capitalize the first letter of the first word in a string in an optional locale format.

```
sentenceCase('<text>', '<locale>'?)
```

Example 1

These examples capitalize the first letter in a string:

```
sentenceCase('a')  
sentenceCase('abc def')  
sentenceCase('aBC dEF')
```

And return the following results respectively:

- A
- Abc def
- Abc def
Example 2

These examples capitalizes the first letter in a string in the specified locale format:

```
sentenceCase('a', 'fr-FR')  
sentenceCase('abc', 'en-US')  
sentenceCase('aBC', 'fr-FR')
```

And return the following results respectively:

- A
- Abc
- Abc
### setPathToValue

Retrieve the value of the specified property from the JSON object.

```
setPathToValue(<path>, <value>)
```

Example 1

The example below sets the value 1 to the path:

```
setPathToValue(path.x, 1)
```

And returns the result 1. path.x is set to 1.

Example 2

This example below sets the value:

```
setPathToValue(path.array[0], 7) + path.array[0]
```

And returns the result 14.

### setProperty

Set the value of an object's property and return the updated object. To add a new property, use this function or the addProperty() function.

```
setProperty(<object>, '<property>', <value>)
```

Example

This example sets the accountNumber property on a customerProfile object, which is converted to JSON with the json() function. The function assigns a value generated by the newGuid() function, and returns the updated JSON object:

```
setProperty(json('customerProfile'), 'accountNumber', newGuid())
```

### skip

Remove items from the front of a collection, and return all the other items.

```
skip([<collection>], <count>)
```

Example

This example removes one item, the number 1, from the front of the specified array:

```
skip(createArray(0, 1, 2, 3), 1)
```

And returns an array with the remaining items: [1,2,3].

### sortBy

Sort elements in the collection in ascending order and return the sorted collection.

```
sortBy([<collection>], '<property>')
```

Example 1

This example generates sorts the following collection:

```
sortBy(createArray(1, 2, 0, 3))
```

And return the result [0, 1, 2, 3].

Example 2

Suppose you have the following collection:

```
{  
  'nestedItems': [  
    {'x': 2},  
    {'x': 1},  
    {'x': 3}  
  ]  
}
```

This example generates a new sorted collection based on the x object property

```
sortBy(nestedItems, 'x')
```

And returns the result:

```
{  
  'nestedItems': [  
    {'x': 1},  
    {'x': 2},  
    {'x': 3}  
  ]  
}
```

### sortByDescending

Sort elements in the collection in descending order, and return the sorted collection.

```
sortBy([<collection>], '<property>')
```

Example 1

This example generates a new sorted collection:

```
sortByDescending(createArray(1, 2, 0, 3))
```

And returns the result [3, 2, 1, 0].

Example 2

Suppose you have the following collection:

```
{  
  'nestedItems': [  
    {'x': 2},  
    {'x': 1},  
    {'x': 3}  
  ]  
}
```

This example generates a new sorted collection based on the x object property:

sortByDescending(nestedItems, 'x')

And returns this result:

```
{  
  'nestedItems': [  
    {'x': 3},  
    {'x': 2},  
    {'x': 1}  
  ]  
}
```

### split

Return an array that contains substrings, separated by commas, based on the specified delimiter character in the original string.

```
split('<text>', '<delimiter>'?)
```

Examples

These examples create an array with substrings from the specified string based on the specified delimiter character:

```
split('a**b**c', '\*\*')  
split('hello', '')  
split('', 'e')  
split('', '')  
split('hello')
```

And returns the following arrays as the result respectively:

- ["a", "b", "c"]
- ["h", "e", "l", "l", "o"]
- [""], []
- ["h", "e", "l", "l", "o"]
### sqrt

Return the square root of a specified number.

```
sqrt(<number>)
```

Examples

These examples compute the square root of specified numbers:

```
sqrt(9)  
sqrt(0)
```

And return the following results respectively:

- 3
- 0
### startOfDay

Return the start of the day for a timestamp in an optional locale format.

```
startOfDay('<timestamp>', '<format>'?, '<locale>'?)
```

Example 1

This example finds the start of the day:

```
startOfDay('2018-03-15T13:30:30.000Z')
```

And returns the result 2018-03-15T00:00:00.000Z.

Example 2

This example finds the start of the day with the locale fr-FR:

```
startOfDay('2018-03-15T13:30:30.000Z', '', 'fr-FR')
```

And returns the result 15/03/2018 00:00:00.

### startOfHour

Return the start of the hour for a timestamp in an optional locale format.

```
startOfHour('<timestamp>', '<format>'?, '<locale>'?)
```

Example 1

This example finds the start of the hour:

```
startOfHour('2018-03-15T13:30:30.000Z')
```

And returns the result 2018-03-15T13:00:00.000Z.

Example 2

This example finds the start of the hour with the locale fr-FR:

```
startOfHour('2018-03-15T13:30:30.000Z', '', 'fr-FR')
```

And returns the result 15/03/2018 13:00:00.

### startOfMonth

Return the start of the month for a timestamp in an optional locale format.

```
startOfMonth('<timestamp>', '<format>'?, '<locale>'?)
```

Example 1

This example finds the start of the month:

```
startOfMonth('2018-03-15T13:30:30.000Z')
```

And returns the result 2018-03-01T00:00:00.000Z.

Example 2

This example finds the start of the month with the locale fr-FR:

```
startOfMonth('2018-03-15T13:30:30.000Z', '', 'fr-FR')
```

And returns the result 01/03/2018 00:00:00.

### startsWith

Check whether a string starts with a specific substring. Return true if the substring is found, or return false if not found. This function is case-insensitive.

```
startsWith('<text>', '<searchText>')
```

Example 1

This example checks whether the string hello world starts with the string hello:

```
startsWith('hello world', 'hello')
```

And returns the result true.

Example 2

This example checks whether the string hello world starts with the string greeting:

```
startsWith('hello world', 'greeting')
```

And returns the result false.

### string

Return the string version of a value in an optional locale format.

```
string(<value>, '<locale>'?)
```

Example 1

This example creates the string version of the number 10:

```
string(10)
```

And returns the string result 10.

Example 2

This example creates a string for the specified JSON object and uses the backslash character,\\, as an escape character for the double-quotation mark character, ".

```
string( { "name": "Sophie Owen" } )
```

And returns the result { "name": "Sophie Owen" }

Example 3

These example creates a string version of the number 10 in a specific locale:

string(100.1, 'fr-FR') string(100.1, 'en-US')

And returns the following strings respectively:

- 100,1
- 100.1
### stringOrValue

Wrap string interpolation to get the real value. For example, stringOrValue('${1}') returns the number 1, while stringOrValue('${1} item') returns the string "1 item".

```
stringOrValue(<string>)
```

Examples

These examples get the real value from the string:

```
stringOrValue('${one}')  
stringOrValue('${one} item')
```

And return the following results respectively:

- The number 1.0.
- The string 1 item.
### sub

Return the result from subtracting the second number from the first number.

```
sub(<minuend>, <subtrahend>)
```

Example

This example subtracts the second number from the first number:

```
sub(10.3, .3)
```

And returns the result 10.

### subArray

Returns a subarray from specified start and end positions. Index values start with the number 0.

```
subArray(<Array>, <startIndex>, <endIndex>)
```

Example

This example creates a subarray from the specified array:

```
subArray(createArray('H','e','l','l','o'), 2, 5)
```

And returns the result ["l", "l", "o"].

### substring

Return characters from a string, starting from the specified position or index. Index values start with the number 0.

```
substring('<text>', <startIndex>, <length>)
```

Example

This example creates a five-character substring from the specified string, starting from the index value 6:

```
substring('hello world', 6, 5)
```

And returns the result world.

### subtractFromTime

Subtract a number of time units from a timestamp in an optional locale format. See also getPastTime().

```
subtractFromTime('<timestamp>', <interval>, '<timeUnit>', '<format>'?, '<locale>'?)
```

Example 1

This example subtracts one day from a following timestamp:

```
subtractFromTime('2018-01-02T00:00.000Z', 1, 'Day')
```

And returns the result 2018-01-01T00:00:00.000Z.

Example 2

This example subtracts one day from a timestamp using the D format:

```
subtractFromTime('2018-01-02T00:00.000Z', 1, 'Day', 'D')
```

And returns the result Monday, January, 1, 2018.

Example 3

This example subtracts 1 hour from a timestamp in the de-DE locale:

```
subtractFromTime('2018-03-15T13:00:00.000Z', 1, 'Hour', '', 'de-DE')
```

And returns the result 15.03.18 12:00:00.

### sum

Return the result from adding numbers in a list.

```
sum([<list of numbers>])
```

Example

This example adds the specified numbers:

```
sum(createArray(1, 1.5))
```

And returns the result 2.5.

### take

Return items from the front of a collection.

```
take('<collection>', <count>)  
take([<collection>], <count>)
```

Example

These examples get the specified number of items from the front of these collections:

```
take('abcde', 3)  
take(createArray(0, 1, 2, 3, 4), 3)
```

And return the following results respectively:

- abc
- [0, 1, 2]
### ticks

Return the ticks property value of a specified timestamp. A tick is 100-nanosecond interval.

```
ticks('<timestamp>')
```

Example

This example converts a timestamp to its ticks property:

```
ticks('2018-01-01T08:00:00.000Z')
```

And returns the result 636503904000000000.

### ticksToDays

Convert a ticks property value to the number of days.

```
ticksToDays('ticks')
```

Example

This example converts a ticks property value to a number of days:

```
ticksToDays(2193385800000000)
```

And returns the number 2538.64097222.

### ticksToHours

Convert a ticks property value to the number of hours.

```
ticksToHours('ticks')
```

Example

This example converts a ticks property value to a number of hours:

```
ticksToHours(2193385800000000)
```

And returns the number 60927.383333333331.

### ticksToMinutes

Convert a ticks property value to the number of minutes.

```
ticksToMinutes('ticks')
```

Example

This example converts a ticks property value to a number of minutes:

```
ticksToMinutes(2193385800000000)
```

And returns the number 3655643.0185.

### titleCase

Capitalize the first letter of each word in a string in an optional local format.

```
titleCase('<text>', '<locale>'?)
```

Example 1

These examples capitalize the first letter of each word in a string:

```
titleCase('a')  
titleCase('abc def')  
titleCase('aBC dEF')
```

And return the following results respectively:

- A
- Abc Def
- Abc Def
Example 2

These examples capitalize the first letter in a string in the en-US format:

```
itleCase('a', 'en-US')  
titleCase('aBC dEF', 'en-US')
```

And return the following results respectively:

- A
- Abc Def
### toLower

Return a string in lowercase in an optional locale format. If a character in the string doesn't have a lowercase version, that character stays unchanged in the returned string.

```
toLower('<text>', '<locale>'?)
```

Example 1

This example converts a string to lowercase:

```
toLower('Hello World')
```

And returns the result hello world.

Example 2

This example converts a string to lowercase in the fr-FR format:

```
toUpper('Hello World', 'fr-FR')
```

And returns the result hello world.

### toUpper

Return a string in uppercase in an optional locale format. If a character in the string doesn't have an uppercase version, that character stays unchanged in the returned string.

```
toUpper('<text>', '<locale>'?)
```

Example 1

This example converts a string to uppercase:

```
toUpper('Hello World')
```

And returns the result HELLO WORLD.

Example 2

This example converts a string to uppercase in the fr-FR format:

```
toUpper('Hello World', 'fr-FR')
```

And returns the result HELLO WORLD.

### trim

Remove leading and trailing whitespace from a string, and return the updated string.

```
trim('<text>')
```

Example

This example removes the leading and trailing whitespace from the string " Hello World ":

```
trim(' Hello World  ')
```

And returns the trimmed result Hello World.

### union

Return a collection that has all the items from the specified collections. To appear in the result, an item can appear in any collection passed to this function. If one or more items have the same name, the last item with that name appears in the result.

```
union('<collection1>', '<collection2>', ...)  
union([<collection1>], [<collection2>], ...)
```

Example

This example gets all the items from the following collections:

```
union(createArray(1, 2, 3), createArray(1, 2, 10, 101))
```

And returns the result [1, 2, 3, 10, 101].

### unique

Remove all duplicates from an array.

```
unique([<collection>])
```

Example 1

This example removes duplicate elements from the following array:

```
unique(createArray(1, 2, 1))
```

And returns the result [1, 2].

### uriComponent

Return the binary version of a uniform resource identifier (URI) component.

```
uriComponent('<value>')
```

Example

This example creates a URI-encoded version of a string:

```
uriComponent('<https://contoso.com'>)
```

And returns the result http%3A%2F%2Fcontoso.com.

### uriComponentToString

Return the string version of a uniform resource identifier (URI) encoded string, effectively decoding the URI-encoded string.

```
uriComponentToString('<value>')
```

Example

This example creates the decoded string version of a URI-encoded string:

```
uriComponentToString('http%3A%2F%2Fcontoso.com')
```

And returns the result https://contoso.com.

### uriHost

Return the host value of a unified resource identifier (URI).

```
uriHost('<uri>')
```

Example

This example finds the host value of the following URI:

```
uriHost('<https://www.localhost.com:8080'>)
```

And returns the result www.localhost.com.

### uriPath

Return the path value of a unified resource identifier (URI).

```
uriPath('<uri>')
```

Example

This example finds the path value of the following URI:

```
uriPath('<http://www.contoso.com/catalog/shownew.htm?date=today'>)
```

And returns the result /catalog/shownew.htm.

### uriPathAndQuery

Return the path and query value of a unified resource identifier (URI).

```
uriPathAndQuery('<uri>')
```

Example

This example finds the path and query value of the following URI:

```
uriPathAndQuery('<http://www.contoso.com/catalog/shownew.htm?date=today'>)
```

And returns the result /catalog/shownew.htm?date=today.

### uriPort

Return the port value of a unified resource identifier (URI).

```
uriPort('<uri>')
```

Example

This example finds the port value of the following URI:

```
uriPort('<http://www.localhost:8080'>)
```

And returns the result 8080.

### uriQuery

Return the query value of a unified resource identifier (URI).

```
uriQuery('<uri>')
```

Example

This example finds the query value of the following URI:

```
uriQuery('<http://www.contoso.com/catalog/shownew.htm?date=today'>)
```

And returns the result ?date=today.

### uriScheme

Return the scheme value of a unified resource identifier (URI).

```
uriScheme('<uri>')
```

Example

This example finds the scheme value of the following URI:

```
uriQuery('<http://www.contoso.com/catalog/shownew.htm?date=today'>)
```

And returns the result http.

### utcNow

Return the current timestamp in an optional locale format as a string.

```
utcNow('<format>', '<locale>'?)
```

Optionally, you can specify a different format with the <format> parameter.

Example 1

Suppose the date is April 15, 2018 at 1:00:00 PM. This example gets the timestamp:

```
utcNow()
```

And returns the result 2018-04-15T13:00:00.000Z.

Example 2

Suppose the date is April 15, 2018 at 1:00:00 PM. This example gets the current timestamp using the optional D format:

```
utcNow('D')
```

And returns the result Sunday, April 15, 2018.

Example 3

Suppose the date is April 15, 2018 at 1:00:00 PM. This example gets the current timestamp using the de-DE locale:

```
utcNow('', 'de-DE')
```

And returns the result 15.04.18 13:00:00.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
