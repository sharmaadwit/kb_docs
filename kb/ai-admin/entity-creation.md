source_url: https://console-docs.gupshup.io/docs/intent-description

<!-- procedural:v2 -->
# Entity Creation

**Module**: Ai Admin

## Overview
An "entity" refers to a specific piece of information within a user's input or utterance. Essentially, it's like a key detail or variable that the AI needs to understand to provide a relevant response or take appropriate action. For example, if someone says, "Book a flight to Paris on Saturday," the entities in this utterance would likely be "Paris" (the destination) and "Saturday" (the date).

## When to use
_Add the primary scenarios and personas._

## Setup path
- Go to the Description section and change the description as per the redefined piece of information that needs to be extracted.

## Step-by-step configuration
An "entity" refers to a specific piece of information within a user's input or utterance. Essentially, it's like a key detail or variable that the AI needs to understand to provide a relevant response or take appropriate action. For example, if someone says, "Book a flight to Paris on Saturday," the entities in this utterance would likely be "Paris" (the destination) and "Saturday" (the date).

By identifying and understanding entities, AI systems can better grasp the meaning behind user requests and respond accurately.

The Entities screen on the workspace in the AI Admin section of Bot Studio lets users create an Entity to extract specific pieces of information as per the Intent created.

# Creating an Entity in a Workspace.

Empty Entity Screen

- Click on the Entities tab on Workspace and click on Create Entity button to create an Entity.
- Provide the Name of Entity, choose the type of Entity between Global or Intent related Entity, provide a short description of the Entity, and link with the Intents already created.
- Click on "Additional Parameters" to add any further details for the Entity being created.
- The Additional Parameters section is optional where the user will be able to provide some more parameters for the entity that is being created.
- The Sample Values is where the user will be able to add a value or a synonym for a particular term being used in the Entity. For example: Entity Airline can have sample values such as Indigo, Air India, Spice Jet, and Vistara.
- The Extended Values is a part of the validations section. Every term has a root value and an extended value. Here the root value can be specified along with its extended values. For Example: Entity Destination City will have Root Value Mumbai and Extended Values Bombay, BOM, and Navi Mumbai.
- Regex is a regular expression that can also be specified in certain use cases to perform text-based tasks like validating user inputs. For Example: Accepting only 10 digit phone numbers from user input.
Entity Editing:The Entities created can be edited by changing the Description, Type of Entity, and the respective values that were added in Additional Parameters.

- Click on the Entity that you want to edit from the List of Entities that got created which can be found in the Types of Entity dropdown.
- Click on Type of Entity* dropdown to change the Entity type from Intent-Related Entity to Global Entity.
- Go to the Description section and change the description as per the redefined piece of information that needs to be extracted.
- Click on Associate Intents dropdown to associate the entity with the pre-created Intents.
- Change the values in the Additional Parameters as per the revised use case.
- Click on the Save button to save the Entity edited.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Click on the Save button to save the Entity edited.

**Last updated (from source)**: Updated 10 months ago
