source_url: https://console-docs.gupshup.io/docs/starting-nodes
# BOT STUDIO

## Starting Nodes

# Starting Nodes

### What is a Starting Node?

The Starting Node in Journey Builder is the foundational point where a journey begins. It serves as the trigger or condition that activates the flow, such as user actions, scheduled events, or system updates. Every journey requires a starting node to define its initiation, ensuring a structured and seamless progression. It provides flexibility to tailor the journey's entry criteria, setting the context for subsequent interactions.

### How to configure

- Click on the Starting Node to open the Node configuration on the right side
- Select from the the available list of Event based on which you would like to trigger the journey
- There are three available selection viz. No Event, User Input and AI Trigger(available with AI Recipe)
- You can also add custom Conditions if required to personalize the event triggers
### Event Types:

- No Event: This option is selected when you don't want this journey to be trigger with any user action. Ideally journeys used with Call & Return nodes are used with No Event to ensure its triggered only through the Call & Return Node.
- User Input: This event is selected to trigger the journey based on a match with user input. You can select from list of available operations(contains, equals to etc.) to validate the user input and trigger the journey.
- AI Trigger(available with AI Recipe only): This event is selected when there are intents trained in the AI Admin and the journey should be triggered when a specific intent is detected. AI Trigger is the most efficient and dynamic way of triggering journeys as it can retain the context of the intent and the entities mentioned on the user input sentence/keyword. AI Trigger has few additional configurations which are as follows: Intents: Intents are trained on the AI Admin Model and can be used for triggering journeys based on that. You can customize your intent based on the domain and the LLM model will create utterances based on the description in order to provide a preview of the type of utterance that the Intent can detect. Local/Global Entities: You can create Intent Based Entities or Global Level Entities to have more information captured from the users message and use them in the journey. Example for a user input like "Book a flight from Mumbai to Brazil for 25th of Dec" have multiple entities like the source and destination along with the date for which the user wanted to book the ticket. These entities will be detected if there are Local Entities mapped with the intent and can be tightly coupled with a variable to update the variable value and use it later. Entity<>Variable mappings are tightly coupled and any update on the value of entity or variable will update the other as well.
- Intents: Intents are trained on the AI Admin Model and can be used for triggering journeys based on that. You can customize your intent based on the domain and the LLM model will create utterances based on the description in order to provide a preview of the type of utterance that the Intent can detect.
- Local/Global Entities: You can create Intent Based Entities or Global Level Entities to have more information captured from the users message and use them in the journey. Example for a user input like "Book a flight from Mumbai to Brazil for 25th of Dec" have multiple entities like the source and destination along with the date for which the user wanted to book the ticket. These entities will be detected if there are Local Entities mapped with the intent and can be tightly coupled with a variable to update the variable value and use it later. Entity<>Variable mappings are tightly coupled and any update on the value of entity or variable will update the other as well.
### Additional Condition:

Bot designers will also have provision to personalize or put conditional check for the events triggered before responding with a journey. These conditions can be added in the Start Node based on the available variables.

Example: The bot can check for the Channel from which the user is responding and respond based on that.

Note:

- Journey Builder will support up to 5 Events in the Starting Node
- Only 1 out of 5 Event can be selected User Event or AI Trigger
- 5 out of 5 can be selected as Customer Event
Updated 10 months ago
