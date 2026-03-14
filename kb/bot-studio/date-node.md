source_url: https://console-docs.gupshup.io/docs/date-node

<!-- kb-golden:v10 -->
# Date Node

**Module**: Bot Studio

## Definition
Date Node

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Date Node

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- Timeout duration
- Message content

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Date Node**.
4. Enable Timeout -Also you can enable timeout message to select the time in which you want the message to expire.
5. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run the flow in **Test your Bot** and confirm the expected node/path executes.
- If the change must affect live traffic, use **Save & Deploy** and verify on the target channel.

### Troubleshooting
- If behavior is unchanged, confirm you updated the correct node and used **Save & Deploy** for live channels.
- If the wrong branch/path runs, re-check conditions, connected nodes, and fallback connectors.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Bot Studio**.
- Go to **Date Node**.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Date Node

**Module**: Bot Studio

## Overview
Date Node

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
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

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
