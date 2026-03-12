source_url: https://console-docs.gupshup.io/docs/phone-node

<!-- kb-golden:v4 -->
# Phone Node

**Module**: Bot Studio

## Definition
Phone Node

## Procedure
### Exact path
Gupshup Console → Bot Studio → Phone Node

### Where to configure it
Gupshup Console → Bot Studio → Phone Node

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Phone Node**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- Answer - Validate and set restrictions on the input provided by using the field to enter a regex

## Available options
- Enable Timeout -Also you can enable timeout message to select the time in which you want the message to expire.

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

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
# Phone Node

**Module**: Bot Studio

## Overview
Phone Node

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
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

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
