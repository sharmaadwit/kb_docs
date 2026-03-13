source_url: https://console-docs.gupshup.io/docs/entity-description-1

<!-- kb-golden:v9 -->
# Entity Description

**Module**: Ai Admin

## Definition
An entity is a piece of specific information extracted from user input.

## Procedure
### Exact UI path
Gupshup Console → Ai Admin → Entity Description

### Steps
1. Open Gupshup Console.
2. Go to **Ai Admin**.
3. Go to **Entity Description**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- _Run a quick smoke test and confirm expected behavior._

### Fields to configure
- _List the fields/inputs you must set in the UI (and expected format)._

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- _Add common failure modes and how to fix them._

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Ai Admin**.
- Go to **Entity Description**.

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation docs
- _Add 1–2 bullets distinguishing this module from adjacent modules to reduce retrieval drift._

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
