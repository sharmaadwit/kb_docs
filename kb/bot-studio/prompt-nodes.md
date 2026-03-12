source_url: https://console-docs.gupshup.io/docs/prompts

<!-- kb-golden:v4 -->
# Prompt Nodes

**Module**: Bot Studio

## Definition
We need to capture user details and ask them basic questions like their Name, Email, Phone number, Date of Birthn and Numbers. Prompts are used to add such types of questions in the chatbot conversation.

## Procedure
### Exact path
Gupshup Console → Bot Studio → Prompt Nodes

### Where to configure it
Gupshup Console → Bot Studio → Prompt Nodes

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Prompt Nodes**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- Types of Prompt Nodes
- Prompt’s Elements
- How to use

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- The behaviour of the bot can be customised if the validation of user input fails. If the validation of user input fails, the validation section helps to set the behaviour of the bot.
- Enable Failure Message - By default on validation failure the Question prompt is repeated. If there is a need to customise the prompt sent to user when user input has failed, this checkbox needs to be checked.

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Prompt Nodes

**Module**: Bot Studio

## Overview
We need to capture user details and ask them basic questions like their Name, Email, Phone number, Date of Birthn and Numbers. Prompts are used to add such types of questions in the chatbot conversation.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
We need to capture user details and ask them basic questions like their Name, Email, Phone number, Date of Birthn and Numbers. Prompts are used to add such types of questions in the chatbot conversation.

If a prompt is used, the chatbot waits for user input, validates it, and moves forward in the conversation flow.

### Types of Prompt Nodes

- Free Text
- Phone Node
- Email Node
- Date Node
- Number Node
- Location Request Node
### When to use

- Prompts can be used to generate qualified leads.
- A regular expression (Reg-ex) can be used along with a prompt to validate user input. For Instance: Chatbot asks the customer for their phone number to generate a lead, and they enter an invalid phone number containing characters as well. The prompt will validate the input and fallback if the input is not according to the reg-ex set. Reg-ex can be changed as per the requirements.
- The behaviour of the bot can be customised if the validation of user input fails. If the validation of user input fails, the validation section helps to set the behaviour of the bot.
### Limitations

- A question is mandatory to be asked in the prompt.
- Character limit of 640 characters.
### Prompt’s Elements

- Question Text Box (640 Character Limit)
- Persistent Message (for Sticky Journeys)
- Answer Validation (Field to enter a regex + Number of retries + Failure Message)
- Validation Section - This can be use to customise bot behaviour on validation failure of user input. Number of Retries - On Validation Failure of User Input, this dropdown specifies the number of times the Bot repeats the prompt to the user. If the number of retries is set to 0, the bot immediately proceed to the fallback connector. If the numbers of retries is set to a value between 1 and 5, the bot repeats the prompts that many times and then proceeds to fallback connector on repeated unsuccessful validation. For instance, if the prompt is a mandatory input which is required from the user, number of retries can be set to infinite. the default value is set to 3. Enable Failure Message - By default on validation failure the Question prompt is repeated. If there is a need to customise the prompt sent to user when user input has failed, this checkbox needs to be checked. Failure message - Field to enter customised failure message. (640 Character Limit)
- Number of Retries - On Validation Failure of User Input, this dropdown specifies the number of times the Bot repeats the prompt to the user. If the number of retries is set to 0, the bot immediately proceed to the fallback connector. If the numbers of retries is set to a value between 1 and 5, the bot repeats the prompts that many times and then proceeds to fallback connector on repeated unsuccessful validation. For instance, if the prompt is a mandatory input which is required from the user, number of retries can be set to infinite. the default value is set to 3.
- Enable Failure Message - By default on validation failure the Question prompt is repeated. If there is a need to customise the prompt sent to user when user input has failed, this checkbox needs to be checked.
- Failure message - Field to enter customised failure message. (640 Character Limit)
- Enable Timeout - The bot will wait for the user input till the set timeout value and will proceed to the fallback path once timed out
- Store user response in a defined variable.
- Skip this node
### How to use

To add a prompt, you can select it from the menu on the canvas or in the prompts menu on the left-hand side panel.

Updated 10 months ago

- Skip Node

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
