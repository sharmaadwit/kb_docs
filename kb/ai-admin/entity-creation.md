> Source: https://console-docs.gupshup.io/docs/entity-creation
> Last updated: 2026-09-11

Intents and Named Entity Recognition (NER) are key tasks when leveraging a Language Model for zero-shot predictions. Effective names are crucial to ensure the language model understands the inputs better and performs tasks optimally. 

Here are some guidelines that can help you come up with better names for Intents and NERs:

1. **Use Clear and Descriptive Names:** Make sure the name represents the task or intention clearly. This makes it easier for the model to predict the right outcome based on the intent's name.

Example: Use "book\_flight\_ticket" instead of "task\_1" for an intent that is meant to book flight tickets.

2. **Keep it simple:** Choose descriptive names that reflect the intent or named entity being targeted. Avoid using complex or ambiguous terms that may confuse the model.

Example: Instead of naming an intent "do\_something\_with\_weather\_today," consider a simpler and clearer name like "get\_weather\_forecast."

3. **Keep it short:** Try to keep your intent and NER names short but meaningful. It's easier for the model to comprehend and reduces chances of errors. 

Example: Instead of naming an intent "banking.product-account-number", consider a simpler and shorter name like "account-number".

Example: Instead of using "DetermineTimeZoneInGivenLocation", you can simply use "GetTimeZone".

4. **Avoid Ambiguity:** The names of intent and NER should not be ambiguous to prevent confusion for the language model. 

Example: "order\_food" is a better name for intent rather than "order" because "order" could mean anything (e.g., to order a taxi, or to rank something).

5. **Be Consistent:** Establish a naming convention and stick to it. If you're using camelCase, stick to it throughout. Inconsistency might confuse the model, especially with capital letters. 

Example: "BookFlightTicket" or "book\_flight\_ticket" is better than "bookflightticket".

6. **Be Domain Specific:** If your project is domain-specific, include that information where possible. 

Example: If an intent is specifically designed to predict weather conditions, you could name it "predict\_weather\_condition" instead of a vague "result\_prediction".

Example: If building a travel-related assistant, naming an intent "book\_flight" or "find\_hotels" provides better clarity than generic names like "flight" or "hotel"

7. **Use specific action verbs**: Incorporate action words in intent names to clearly convey the purpose or action the user wants the model to perform. This helps the model understand the intent more accurately.

Example: Instead of naming an intent "weather," use verbs like "check\_weather" or "get\_weather"

8. **Avoid overlapping names**: Ensure that the names chosen for different intents or NERs are unique and do not overlap in meaning. Overlapping names can lead to ambiguity and confusion during prediction.

Example: If there is an intent named "get\_weather\_forecast" and another named "check\_weather", it may be confusing for the model to distinguish between the two

**More NER specific Guidelines:**\
NER, Named Entity Recognition, is a subtask of information extraction in Natural Language Processing (NLP) that identifies named entities within a text such as Person, Location, Organization, Date, Time, Percent, Money, etc.

1. **Follow convention:** Typically, it is good practice to use verbs for intents and proper nouns for NERs. Please note that the custom NER should conform to the definition of a named entity: They are things in the real world that can be defined by a name, number, or some other kind of identifier.

Example: Expecting language model to predict prepositions (from, to, in, at etc.), verbs/adverbs (find, tell, get, temporarily, permanently, etc.), adjectives (good, new, first, last, long, sweet, bad etc.) as named entities is not ideal (though it is not a limitation). 

2. **Excluded from NER:** Any abstract concept or entity which does not have a definite identifier or cannot be categorized under any known category may not be captured correctly in an NER task. 

Example: emotions, thoughts, ideas, etc.

3. **Consider Entity Types:** When naming entities, include the type of entities you are considering. 

Example: If you are trying to recognize the model of cars, use "car\_model" instead of just "model" to make it clear that the language model should be recognizing models of cars and not any other models like laptop models, washing machine models etc.

Remember, the names of intents or NERs are for the model's understanding and comprehension. The better and more intuitive your names are, the more accurately your model can perform tasks.