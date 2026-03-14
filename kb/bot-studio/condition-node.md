source_url: https://console-docs.gupshup.io/docs/condition-node

<!-- kb-golden:v10 -->
# Condition Node

**Module**: Bot Studio

## Definition
Use **Condition Node** to branch a journey based on the current user message or any other variable. This is the primary Bot Studio control for **if/else-style branching**.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Journey Builder → Condition Node

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- **Input source**: current user message or another variable
- **Condition / operator**
- **Compare value**
- **Fallback path**

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Open the target journey in **Journey Builder**.
4. Add or open the **Condition Node**.
5. Select whether the condition should evaluate the **current user message** or another variable.
6. Configure the condition/operator and comparison value.
7. Connect the resulting branches to the correct next nodes.
8. Configure the **fallback** path.
9. Click **Save**.
10. If you need the change live on the channel, click **Save & Deploy**.

### Validation / where to check
- Run the flow in **Test your Bot** and trigger each expected branch value.
- Confirm the conversation reaches the correct next node for each branch.
- Confirm unmatched input follows the **fallback** path.
- If the change must affect live traffic, use **Save & Deploy** and verify on the target channel.

### Troubleshooting
- If behavior is unchanged, confirm you updated the correct node and used **Save & Deploy** for live channels.
- If the wrong branch/path runs, re-check conditions, connected nodes, and fallback connectors.
- If the condition never matches, verify the **value field is not empty** and the evaluated variable actually contains the expected data.

### Save / publish / deploy behavior
- **Save** stores the updated node logic in Bot Studio.
- **Save & Deploy** is required for the updated branch logic to affect the live channel.

### Setup path
- Go to **Bot Studio**.
- Open **Journey Builder**.
- Open or add **Condition Node**.

## Options / variants
- Condition on the **current user message**
- Condition on **another variable**
- **Fallback** path for unmatched cases

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Test your Bot → branch validation
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.
- **Condition Node** is for branching logic; **Quick Replies / Buttons** collect structured input but are not the main branching control by themselves.

## Reference (from source)
<!-- procedural:v2 -->
# Condition Node

**Module**: Bot Studio

## Overview
These are automatically created when quick responses or buttons are used. By default, the condition will be on the current user message but you can create logic or conditions based on any other variable (any type).

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
These are automatically created when quick responses or buttons are used. By default, the condition will be on the current user message but you can create logic or conditions based on any other variable (any type).

All conditions will have a fallback option.

### When to use

Condition Node can be used in various scenarios: To create branching in the flow. Compare user input against different conditions and personalize the conversation flow. To optimize the conversations

### Limitations

Condition Node is a very powerful node and very effective to use, on the other hand, the limitations of using condition nodes are also very limited. The only limitation of the condition node is:

- The value field in the condition node can’t be empty.
### Condition Node

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
