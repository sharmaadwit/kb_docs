source_url: https://console-docs.gupshup.io/docs/code-node

<!-- kb-golden:v10 -->
# Code Node

**Module**: Bot Studio

## Definition
****** THIS NODE IS DEPRECATED AND WILL NOT BE AVAILABLE IN BOT STUDIO *******

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Code Node

### Prerequisites
- Customized integrations, components, requirements, and anything can be coded for a better user journey.
- Node is used to complete the entire end-to-end journey flow, by writing code for components not included in the journey builder or code representing custom requirements for a brand.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Code Node**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

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
- Go to **Code Node**.

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
