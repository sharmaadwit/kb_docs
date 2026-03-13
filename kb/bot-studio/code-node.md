source_url: https://console-docs.gupshup.io/docs/code-node

<!-- kb-golden:v9 -->
# Code Node

**Module**: Bot Studio

## Definition
****** THIS NODE IS DEPRECATED AND WILL NOT BE AVAILABLE IN BOT STUDIO *******

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Code Node

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Code Node**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- _Run a quick smoke test and confirm expected behavior._

### Fields to configure
- _List the fields/inputs you must set in the UI (and expected format)._

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- _Add common failure modes and how to fix them._

### Prerequisites
- Customized integrations, components, requirements, and anything can be coded for a better user journey.
- Node is used to complete the entire end-to-end journey flow, by writing code for components not included in the journey builder or code representing custom requirements for a brand.

### Setup path
- Go to **Bot Studio**.
- Go to **Code Node**.

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Code Node

**Module**: Bot Studio

## Overview
****** THIS NODE IS DEPRECATED AND WILL NOT BE AVAILABLE IN BOT STUDIO *******

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
****** THIS NODE IS DEPRECATED AND WILL NOT BE AVAILABLE IN BOT STUDIO *******

## THIS NODE IS DEPRECATED AND WILL NOT BE AVAILABLE IN BOT STUDIO

Node supports JavaScript code which can help you to make more customized conversation flows.

Customized integrations, components, requirements, and anything can be coded for a better user journey.

### When to use

Node is used to complete the entire end-to-end journey flow, by writing code for components not included in the journey builder or code representing custom requirements for a brand.

### Limitations

Code Node supports JavaScript code only.

### How to use

Example: Perform the operation of adding 2 variables and save the response in a result.

- Create a variable "num1" and "num2" on the Manage variable.
- Create a variable "sum" to store the result of the above computation.
- Create a journey, where the response from the user can be saved in variables "num1" and "num2" respectively
- Use the code node to add the two numbers and store the end result in a variable "sum".
- Show the result in any text node as a response from the chatbot. The final result would be shown using the sum variable.
### Code Node

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- Example: Perform the operation of adding 2 variables and save the response in a result.

**Last updated (from source)**: Updated 10 months ago
