source_url: https://console-docs.gupshup.io/docs/date-node
# BOT STUDIO

## Date Node

# Date Node

## Introduction

Date Node

The Date node is a Prompt node which allows for date input in various formats and includes additional functionalities for applying conditions on the input date which are discussed below:

## When to Use

When a specific date is asked from the user, then the Date node should be used to take input. Some example scenarios can be:

- Asking for appointment time
- Slot Booking
- Asking for date of birth
## How to Use

Persistent, Question, Answer

Persistent Message - Enable the sticky journey to use the Persistent message feature in the date node. Find more about the persistent feature here - Proactive Persistent Message

Question - Add the text/question here which you want to send to the user

Answer - Select format of the date in which the user needs to input the date

Range, Timezone, Exclusion, Validation

Range - Apply the condition on the input date from the various options in the dropdown to give a strict range.

Timezone - Choose the timezone where the bot is servicing so that the bot calculates the date and time accordingly. It helps the bot to treat the input as past or future relative to the timezone.

Exclusion - Specifically exclude the week days that should not be acceptable in the input date.

Validation - Write the regex for the input character constraints.

Retries, Failure Message, Enable Timeout, Store in Variable

Number of retries - Set the number of time you want to give chance to the user to give correct input (within the validation rules). After the retries are over, the node goes to the fallback connector

Failure Message - Enable failure message to be sent to the user when the input does not follow the validation rule. Write the failure message to be shown, in the failure message box.

Enable Timeout -Also you can enable timeout message to select the time in which you want the message to expire.

Store in Variable - Store the input date by the user in the variable here.

Updated 10 months ago

Next up, read some more detailed use case for the date node and how to apply them (Date Prompt Validation Enhancement)
