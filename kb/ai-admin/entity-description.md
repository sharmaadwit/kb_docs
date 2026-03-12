source_url: https://console-docs.gupshup.io/docs/entity-description-1

<!-- kb-golden:v1 -->
# Entity Description

**Module**: Ai Admin

## Definition
An entity is a piece of specific information extracted from user input.

## Procedure
### Where to configure it
Gupshup Console → Ai Admin → Entity Description

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Ai Admin → Entity Description**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Reference (from source)
<!-- procedural:v2 -->
# Entity Description

**Module**: Ai Admin

## Overview
An entity is a piece of specific information extracted from user input.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
An entity is a piece of specific information extracted from user input.

When writing descriptions for entities:

- Define the entity type: Clearly state what kind of information the entity represents.
- Specify the format: Describe the expected format or structure of the entity.
- List possible values: If applicable, provide a range or set of possible values.
- Explain the context (Optional): Not mandatory, but in case of overlapping entity scope between two or more entities. Only include example(s) for those entities wherever required.
- Include examples: Provide several examples of the entity in different contexts.
Here are few examples of entity description:

- Description without example): Entity: car_year
Description: The year of manufacture of a car.

- Example 2 (with example): Entity: Date
Description: Represents a calendar date in various formats. Date can be expressed as MM/DD/YYYY, Month Day, Year, or relative terms like "tomorrow" or "next Tuesday".

- Description in example 2 can be extended for additional context if required. User can mention that entity is related to intent of scheduling, booking, or any time-specific actions.
Note: If it is observed that few variations are not being handled by the entity, then some examples with respective entity values can be added in the teach mode and annotated the values for the respective entity. Also few variations can be added in description as examples.

Examples:

- "05/20/2023"
- "June 15th"
- "next Friday"
Always remember to maintain consistency in formatting and level of detail across all your intent and entity descriptions. This consistency, along with considering context and variations, will greatly enhance the LLM's ability to understand and process the intents and entities accurately.

Updated 10 months ago

- Naming Guidelines for Intent & Entity

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
