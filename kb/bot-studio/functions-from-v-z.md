source_url: https://console-docs.gupshup.io/docs/functions-from-v-z

<!-- kb-golden:v7 -->
# Functions from V - Z

**Module**: Bot Studio

## Definition
Filter on each element and return the new collection of filtered elements which match a specific condition.

## Procedure
### Exact path
Gupshup Console → Bot Studio → Functions from V - Z

### Where to configure it
Gupshup Console → Bot Studio → Functions from V - Z

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **Functions from V - Z**.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Functions from V - Z**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- where
- xml
- xPath
- year

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
# Functions from V - Z

**Module**: Bot Studio

## Overview
Filter on each element and return the new collection of filtered elements which match a specific condition.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### where

Filter on each element and return the new collection of filtered elements which match a specific condition.

```
where([<collection/instance>], <iteratorName>, <function>)
```

Example 1

This example generates a new collection:

```
where(createArray(0, 1, 2, 3), x, x > 1)
```

And returns the result [2, 3].

Example 2

These examples generate a new collection:

```
where(json("{'name': 'jack', 'age': '15'}"), x, x.value == 'jack')  
where(json("{'name': 'jack', 'age': '15'}"), x=> x.value == 'jack')
```

And return the result ['name:jack', 'age:15']. Note that the second expression is a lambda expression, which some find more readable.

### xml

Return the XML version of a string that contains a JSON object.

```
xml('<value>')
```

Example 1

This example creates the XML version for a string, which contains a JSON object:

xml(json('{ \"name\": \"Sophia Owen\" }'))

And returns the result XML:

Example 2

Suppose you have a person JSON object, seen below:

```
{  
  "person": {  
    "name": "Sophia Owen",  
    "city": "Seattle"  
  }  
}
```

This example creates XML of a string that contains this JSON object:

xml(json('{\"person\": {\"name\": \"Sophia Owen\", \"city\": \"Seattle\"}}'))

And returns the result XML:

```
<person>
  <name>Sophia Owen</name>
  <city>Seattle</city>
<person
```

### xPath

Check XML for nodes or values that match an XPath (XML Path Language) expression, and return the matching nodes or values. An XPath expression (referred to as XPath) helps you navigate an XML document structure so that you can select nodes or compute values in the XML content.

```
xPath('<xml>', '<xpath>')
```

Example 1

This example finds nodes that match the <name></name> node in the specified arguments, and returns an array with those node values:

```
xPath(items, '/produce/item/name')
```

The arguments include the items string, which contains this XML:

```
"<?xml version="1.0"?> <produce> <item> <name>Gala</name> <type>apple</type> <count>20</count> </item> <item> <name>Honeycrisp</name> <type>apple</type> <count>10</count> </item> </produce>"
```

Here's the resulting array with the nodes that match <name></name>:

[ Gala, Honeycrisp ]

Example 2

Following example 1, this example finds nodes that match the <count></count> node and adds those node values with the sum() function:

```
xPath(xml(parameters('items')), 'sum(/produce/item/count)')
```

And returns the result 30.

### year

Return the year of the specified timestamp.

```
year('<timestamp>')
```

Example

This example evaluates the timestamp for the year:

```
year('2018-03-15T00:00:00.000Z')
```

And it returns the result 2018.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
