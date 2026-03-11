source_url: https://console-docs.gupshup.io/docs/phone-node
# BOT STUDIO

## Phone Node

# Phone Node

Phone Node

The Phone node is a Prompt node which should be used to take user's phone number as input and store the response in a variable after validating it alongside the regex condition that is applied in the validation box (default). This node waits for the user's response to continue with the journey. More details are discussed below:

## When to Use

Use this node whenever there's a need to take phone number as input and store them

Some example scenarios can be:

- Asking the user's phone number for appointment booking
- Asking the user's phone number for promotional offers
## How to Use

Persistent, Question, Answer

Persistent Message - Enable the sticky journey to use the Persistent message feature in the free text node. Find more about the persistent feature here - Proactive Persistent Message

Question - Add the text/question here which you want to send to the user

Answer - Validate and set restrictions on the input provided by using the field to enter a regex

Validation Section - Use to customize bot behavior on validation failure of user input.

- Number of retries - Set the number of time you want to give chance to the user to give correct input (within the validation rules). After the retries are over, the node goes to the fallback connector
- Failure Message - Enable failure message to be sent to the user when the input does not follow the validation rule. Write the failure message to be shown, in the failure message box.
- Enable Timeout -Also you can enable timeout message to select the time in which you want the message to expire.
Store in Variable - Store the input given by the user in the variable here.

Updated 10 months ago
