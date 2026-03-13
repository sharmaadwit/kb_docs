source_url: https://console-docs.gupshup.io/docs/entity-creation

<!-- kb-golden:v7 -->
# Naming Guidelines for Intent & Entity

**Module**: Ai Admin

## Definition
Intents and Named Entity Recognition (NER) are key tasks when leveraging a Language Model for zero-shot predictions. Effective names are crucial to ensure the language model understands the inputs better and performs tasks optimally.

## Procedure
### Exact path
Gupshup Console → Ai Admin → Naming Guidelines for Intent & Entity

### Where to configure it
Gupshup Console → Ai Admin → Naming Guidelines for Intent & Entity

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Ai Admin**.
- Go to **Naming Guidelines for Intent & Entity**.

### Steps
1. Open Gupshup Console.
2. Go to **Ai Admin**.
3. Go to **Naming Guidelines for Intent & Entity**.
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
- Excluded from NER: Any abstract concept or entity which does not have a definite identifier or cannot be categorized under any known category may not be captured correctly in an NER task.

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation
- _Add 1–2 bullets distinguishing this module from adjacent modules to reduce retrieval drift._

## Reference (from source)
<!-- procedural:v2 -->
# Naming Guidelines for Intent & Entity

**Module**: Ai Admin

## Overview
Intents and Named Entity Recognition (NER) are key tasks when leveraging a Language Model for zero-shot predictions. Effective names are crucial to ensure the language model understands the inputs better and performs tasks optimally.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Intents and Named Entity Recognition (NER) are key tasks when leveraging a Language Model for zero-shot predictions. Effective names are crucial to ensure the language model understands the inputs better and performs tasks optimally.

Here are some guidelines that can help you come up with better names for Intents and NERs:

- Use Clear and Descriptive Names: Make sure the name represents the task or intention clearly. This makes it easier for the model to predict the right outcome based on the intent's name.
Example: Use "book_flight_ticket" instead of "task_1" for an intent that is meant to book flight tickets.

- Keep it simple: Choose descriptive names that reflect the intent or named entity being targeted. Avoid using complex or ambiguous terms that may confuse the model.
Example: Instead of naming an intent "do_something_with_weather_today," consider a simpler and clearer name like "get_weather_forecast."

- Keep it short: Try to keep your intent and NER names short but meaningful. It's easier for the model to comprehend and reduces chances of errors.
Example: Instead of naming an intent "banking.product-account-number", consider a simpler and shorter name like "account-number".

Example: Instead of using "DetermineTimeZoneInGivenLocation", you can simply use "GetTimeZone".

- Avoid Ambiguity: The names of intent and NER should not be ambiguous to prevent confusion for the language model.
Example: "order_food" is a better name for intent rather than "order" because "order" could mean anything (e.g., to order a taxi, or to rank something).

- Be Consistent: Establish a naming convention and stick to it. If you're using camelCase, stick to it throughout. Inconsistency might confuse the model, especially with capital letters.
Example: "BookFlightTicket" or "book_flight_ticket" is better than "bookflightticket".

- Be Domain Specific: If your project is domain-specific, include that information where possible.
Example: If an intent is specifically designed to predict weather conditions, you could name it "predict_weather_condition" instead of a vague "result_prediction".

Example: If building a travel-related assistant, naming an intent "book_flight" or "find_hotels" provides better clarity than generic names like "flight" or "hotel"

- Use specific action verbs: Incorporate action words in intent names to clearly convey the purpose or action the user wants the model to perform. This helps the model understand the intent more accurately.
Example: Instead of naming an intent "weather," use verbs like "check_weather" or "get_weather"

- Avoid overlapping names: Ensure that the names chosen for different intents or NERs are unique and do not overlap in meaning. Overlapping names can lead to ambiguity and confusion during prediction.
Example: If there is an intent named "get_weather_forecast" and another named "check_weather", it may be confusing for the model to distinguish between the two

More NER specific Guidelines: NER, Named Entity Recognition, is a subtask of information extraction in Natural Language Processing (NLP) that identifies named entities within a text such as Person, Location, Organization, Date, Time, Percent, Money, etc.

- Follow convention: Typically, it is good practice to use verbs for intents and proper nouns for NERs. Please note that the custom NER should conform to the definition of a named entity: They are things in the real world that can be defined by a name, number, or some other kind of identifier.
Example: Expecting language model to predict prepositions (from, to, in, at etc.), verbs/adverbs (find, tell, get, temporarily, permanently, etc.), adjectives (good, new, first, last, long, sweet, bad etc.) as named entities is not ideal (though it is not a limitation).

- Excluded from NER: Any abstract concept or entity which does not have a definite identifier or cannot be categorized under any known category may not be captured correctly in an NER task.
Example: emotions, thoughts, ideas, etc.

- Consider Entity Types: When naming entities, include the type of entities you are considering.
Example: If you are trying to recognize the model of cars, use "car_model" instead of just "model" to make it clear that the language model should be recognizing models of cars and not any other models like laptop models, washing machine models etc.

Remember, the names of intents or NERs are for the model's understanding and comprehension. The better and more intuitive your names are, the more accurately your model can perform tasks.

Updated 10 months ago

- AI Enhanced Description Writing

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
