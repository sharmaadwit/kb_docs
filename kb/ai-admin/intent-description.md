source_url: https://console-docs.gupshup.io/docs/intent-description-1

<!-- kb-golden:v4 -->
# Intent Description

**Module**: Ai Admin

## Definition
When writing effective intent descriptions user needs to follow below guidelines:

## Procedure
### Exact path
Gupshup Console → Ai Admin → Intent Description

### Where to configure it
Gupshup Console → Ai Admin → Intent Description

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Ai Admin → Intent Description**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation
- _Add 1–2 bullets distinguishing this module from adjacent modules to reduce retrieval drift._

## Reference (from source)
<!-- procedural:v2 -->
# Intent Description

**Module**: Ai Admin

## Overview
When writing effective intent descriptions user needs to follow below guidelines:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
When writing effective intent descriptions user needs to follow below guidelines:

- Be clear and concise: Describe the intent in a single, straightforward sentence.
- Use action-oriented language: Start with a verb that describes what the user wants to accomplish.
- Avoid technical jargon: Use simple, easy-to-understand language.
- Include key parameters: Mention important variables the intent might contain.
- Provide an example in descriptions (Optional): Not mandatory, but in case of overlapping intent scope between two or more intents. Only include example(s) for those ambiguous intents wherever required.
- Use consistent formatting: Maintain a uniform structure across all intent descriptions to improve readability and processing by the LLM.
- Consider context and variations: Account for different ways users might express the same intent and include relevant contextual information.
Here are few examples of Intent description:

- Description without utterance example:
Intent: buy_car

Description: User wants to buy a car.

- Description with utterance example:
Intent: book_flight

Description: Allow users to book a flight by specifying origin, destination, and travel dates. Example: "I want to book a flight from New York to London for next week."

- Description with utterance example and additional context:
Intent: book_flight

Description: Allow users to book a flight by specifying origin, destination, and travel dates. May be part of a larger travel planning process. Example: "I want to book a flight from New York to London for next week."

Additionally, “Key Parameters” and “context” also plays a vital roles as can be seen in above examples (i.e. Key Parameters: origin, destination, travel_date, Context: May be part of a larger travel planning process).

Note:

- “Key Parameters” and “context” are only to be included in case the intent scope requires additional context and parameters. For example: update_email vs email_account_statement may require “key parameters” as well as additional “context”.
- If the specific intent based use case has wider variety of variation than that can be included first in the teach mode and later if required than can be included as examples under description:
Example (of possible variations):

Variations:

- "I need to fly to [destination]"
- "Book me a ticket to [destination] from [origin]"
- "What flights are available for [travel_date]?"
When a user writes an ineffective description for a natural language processing (NLP) task on LLM, particularly for intent and entity identification, several issues can arise. Here are 4 key points on what happens:

Reduced Context: An ineffective description often lacks crucial context. This makes it harder for the LLM model to accurately interpret the user's intent. Without sufficient context, the model may misinterpret ambiguous phrases or fail to capture the nuanced meaning behind the user's words.

Increased Ambiguity: Vague or imprecise language in the description can lead to increased ambiguity. This makes it challenging for the model to distinguish between similar intents or entities. As a result, the model may incorrectly classify the user's intent or fail to identify relevant entities.

Missed Key Information: If the description omits important details or key terms, the LLM model may miss critical information needed for accurate intent and entity identification. This can lead to incomplete or incorrect interpretations of the user's request.

Overfitting to Limited Examples: When descriptions are consistently ineffective, it can lead to the model overfitting to a limited set of examples. This means the model may struggle to generalize well to new, slightly different inputs, reducing its overall accuracy and robustness.

These factors collectively contribute to reduced accuracy in intent identification. To improve results, users should be encouraged to provide clear, specific, and context-rich descriptions that accurately represent their intentions and include relevant entities.

Additional Tips

- Consistency is Key: Maintain the same style and format to ensure the system remains organized.
- Be User-Centric: Always frame intents and entities from the user's perspective.
- Avoid Ambiguity: Use clear and specific language to prevent misunderstandings.
- Update Regularly: As new user needs are identified, continue to expand your intents and entities accordingly.
Updated 10 months ago

- Entity Creation

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
