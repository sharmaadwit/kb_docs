source_url: https://console-docs.gupshup.io/docs/free-text-node

<!-- kb-golden:v10 -->
# Free Text Node

**Module**: Bot Studio

## Definition
Free Text Node

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Free Text Node

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- Timeout duration
- Message content

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Free Text Node**.
4. Enable Timeout -Also you can enable timeout message to select the time in which you want the message to expire.
5. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Answer - Validate and set restrictions on the input provided by using the field to enter a regex

### Troubleshooting
- If behavior is unchanged, confirm you updated the correct node and used **Save & Deploy** for live channels.
- If the wrong branch/path runs, re-check conditions, connected nodes, and fallback connectors.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Bot Studio**.
- Go to **Free Text Node**.

## Options / variants
- Enable Timeout -Also you can enable timeout message to select the time in which you want the message to expire.

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
# Free Text Node

**Module**: Bot Studio

## Overview
Free Text Node

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
## Introduction

Free Text Node

The Free Text node is a Prompt node which should be used to take any sort of input from the user and store the response in a variable after validating it alongside any condition using a regex. This node waits for the user's response to continue with the journey. More details are discussed below:

## When to Use

Use this node whenever there's a need to take miscellaneous inputs, like for feedback, name or anywhere where the input boundary lines are not clear.

Some example scenarios can be:

- Asking the user for it's name
- Taking feedback for a service provided
- Taking suggestions for an event
## How to Use

Persistent, Question, Answer

Persistent Message - Enable the sticky journey to use the Persistent message feature in the free text node. Find more about the persistent feature here - Proactive Persistent Message

Question - Add the text/question here which you want to send to the user

Answer - Validate and set restrictions on the input provided by using the field to enter a regex

Validation Section, Store in Variable

Validation Section - Use to customize bot behavior on validation failure of user input.

- Number of retries - Set the number of time you want to give chance to the user to give correct input (within the validation rules). After the retries are over, the node goes to the fallback connector
- Failure Message - Enable failure message to be sent to the user when the input does not follow the validation rule. Write the failure message to be shown, in the failure message box.
- Enable Timeout -Also you can enable timeout message to select the time in which you want the message to expire.
Store in Variable - Store the input given by the user in the variable here.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
