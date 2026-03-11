source_url: https://console-docs.gupshup.io/docs/default-journeys
# BOT STUDIO

## Default Journeys

# Default Journeys

Each bot has three journeys by default in the User Journeys section -

- Configuration Journey - Click to find more about this journey
Configuration Journey - Click to find more about this journey

- Fallback Journey -This default journey is triggered when a node fails to proceed forward based on the user input or some technical failures such as API failed to respond etc. In such cases the fallback journey gets triggered to send an invalid input message or error message. By default, the fallback journey contains a text node which can be edited or customized - Incase there is a need to sent a customized fallback message on any user inputs then the fallback connecter of the node can be linked with a Text Node and then back to the same node in order to repeat the invalid message as shown below. Incase the fallback connector is left empty then the Fallback Journey will be triggered. The fallback journey can also be customized to provide quick replies and other suggestions in order to make the conversational experience better.
Fallback Journey -This default journey is triggered when a node fails to proceed forward based on the user input or some technical failures such as API failed to respond etc. In such cases the fallback journey gets triggered to send an invalid input message or error message. By default, the fallback journey contains a text node which can be edited or customized -

Incase there is a need to sent a customized fallback message on any user inputs then the fallback connecter of the node can be linked with a Text Node and then back to the same node in order to repeat the invalid message as shown below. Incase the fallback connector is left empty then the Fallback Journey will be triggered.

The fallback journey can also be customized to provide quick replies and other suggestions in order to make the conversational experience better.

- Welcome Journey - Welcome Journey is triggered when the user input doesn't matches with any of the configured events on the start nodes of all journeys. This enables bot builders to leverage the Welcome Journey as a greeting journey for new users if they type in gibberish keywords which doesn't triggers any configured journeys. Its suggested to keep the Welcome Journey interactive in order to let the users know what all things the bot can help them with. The way how Welcome Journey differentiates from Fallback is based on the user state. Incase the user is already traversing a journey and then enters an invalid input then the Fallback Journey or Node connecter will respond. But if the user is not inside any Journey or the session(72hours) has expired from the last traversed journey then in such cases the Welcome Journey will be triggered.
Welcome Journey - Welcome Journey is triggered when the user input doesn't matches with any of the configured events on the start nodes of all journeys. This enables bot builders to leverage the Welcome Journey as a greeting journey for new users if they type in gibberish keywords which doesn't triggers any configured journeys.

Its suggested to keep the Welcome Journey interactive in order to let the users know what all things the bot can help them with.

The way how Welcome Journey differentiates from Fallback is based on the user state. Incase the user is already traversing a journey and then enters an invalid input then the Fallback Journey or Node connecter will respond. But if the user is not inside any Journey or the session(72hours) has expired from the last traversed journey then in such cases the Welcome Journey will be triggered.

Note: If the bot responds with "Welcome" for user inputs and another user journey needs to be triggered instead , please check if the intended User Journey to be triggered has the keywords configured in the start node.

### Limitations:

- The names of default journeys can not be changed or duplicated.
- Configuration Journey is view only. Please contact console-support@gupshup.io for changes in configuration journey.
Updated 10 months ago
