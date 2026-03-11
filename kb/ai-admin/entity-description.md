source_url: https://console-docs.gupshup.io/docs/entity-description-1
# AI Admin

## Entity Description

# Entity Description

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
