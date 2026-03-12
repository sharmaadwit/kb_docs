source_url: https://console-docs.gupshup.io/docs/list-node

<!-- kb-golden:v1 -->
# List Node

**Module**: Bot Studio

## Definition
This node helps to create a list of a maximum of 10 Items that can be put into sections/categories.

## Procedure
### Where to configure it
Gupshup Console → Bot Studio → List Node

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → List Node**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- Adding the Message title, Button title and Footer
- Define the List Node section and row titles statically
- Define the List Node section and row titles dynamically
- Introduction
- How to use Synonyms in Button Titles?
- Use Cases
- Customer Profile Completion:
- Support Ticket Management:
- E-commerce Checkout:

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Reference (from source)
<!-- procedural:v2 -->
# List Node

**Module**: Bot Studio

## Overview
This node helps to create a list of a maximum of 10 Items that can be put into sections/categories.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
This node helps to create a list of a maximum of 10 Items that can be put into sections/categories.

There is a main message along with sections, rows, and descriptions to create a list message.

## List Node Elements

List Message has the following fields:

- Main Message (Body)
- A button (To open the list)
- Footer Field (To add short supporting text)
- Rows (To add Items)
- Section Title (To add categories)
The elements rows and section titles can be filled dynamically as well from a JSON variable at run-time and an example is given below.

## When to use

Send a small catalog of 10 items to your customers over WhatsApp. You can define categories and subcategories in the list. A description can be added to the products, however, it is optional to add.

## Limitations

- Message can’t be empty
- The button title can’t be empty (1 button mandatory)
- Row title can not be empty (1 row mandatory)
- Elements and their respective character limits:
- When dynamically populating the section and row titles, the JSON should contain values adhering to channel limitations of character limit. If the character limit is exceeded, the node will not execute properly on the channel.
- Applicable for Whatsapp channel
## How to use List Node

#### Adding the Message title, Button title and Footer

List Node elements - section titles and row titles - can be filled statically at design time or dynamically at run-time based on values contained a JSON.

### Define the List Node section and row titles statically

On Canvas -

On Whatsapp Channel -

Video of static population in list node:

### Define the List Node section and row titles dynamically

Dynamic population of the section and row titles can be done if JSON structure is known at design time. The JSON can be defined by a user or be obtained from an API response. At run-time, the section and row titles will be fetched from JSON used.

Sample JSON

For the given JSON, the values in key "name" are to be populated in Section titles and the values in key "items" are to be populated in row titles at run-time. Let's see how to design this dynamic journey and the execution during run-time.

On Canvas -

The "response" variable stores the JSON.

Configuration on List Node - Section Title

The iterable key "categories" is selected as the "section_element". Please note that "categories" is an array of items. In the given example, the titles that need to be populated in section titles are - Men's Clothes and Accessories. Hence, "section_element.name" is mentioned in the section titles. Here "section_element.name" corresponds to response.categories.name in the original JSON.

Configuration on List Node - Row Title

Row elements are used to populate row titles. Row element can be selected again from the dropdown, or section element can be re-used as the row element.

On Whatsapp Channel -

VIDEO COMING SOON

## Support for Synonyms in List Node

### Introduction

Bot designers can now add Synonyms for the List Row and Reply Button titles to ensure that the user inputs matching the title synonyms also gets captured as a valid input from the user.

### How to use Synonyms in Button Titles?

Bot designers can create nodes with the required button titles and then click on "More Options" to open the accordion containing the Synonym field. Synonyms can be typed, and then the user can press enter to save the synonym. Multiple synonyms can be entered for a single button to provide more flexibility to end-users in selecting input

## Skip Node Feature

### Introduction

The Skip Node feature exists on Journey Builder Prompt Nodes, allowing businesses to skip a question where the bot is designed to ask for information from the user. If the Skip Node checkbox is enabled, the bot checks the variable mapped to the node, and if the variable already contains a value, it skips the node and proceeds to the next one.

This feature helps businesses reduce the number of repeated questions asked by the bot, making it smarter by reusing information already gathered at earlier stages or through API integrations.

### Use Cases

Here are a few use cases that demonstrate the benefits of the Skip Node feature:

#### Customer Profile Completion:

Scenario - A customer has already provided their email address during the initial registration process.

Benefit - When the bot asks for the email address again in a subsequent conversation, it can skip this question if the email address is already stored, thereby avoiding redundancy and improving user experience.

#### Support Ticket Management:

Scenario - A user previously reported an issue and provided their device information.

Benefit - When the bot assists the same user in a new conversation, it can skip asking for the device information again if it is already stored, streamlining the support process.

#### E-commerce Checkout:

Scenario - A returning customer is making another purchase and had previously entered their shipping address.

Benefit - The bot can skip the address prompt if the shipping address is already on file, making the checkout process faster and more efficient.

These use cases illustrate how the Skip Node feature can make interactions more efficient and user-friendly by reusing previously gathered information.

More on Skip Node functionality here: Existing Console Doc Link

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
