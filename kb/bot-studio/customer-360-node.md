source_url: https://console-docs.gupshup.io/docs/cdp-goal-node-beta

<!-- kb-golden:v9 -->
# Customer 360 Node

**Module**: Bot Studio

## Definition
While customers interact with a Bot, businesses can view these interactions on the Customer 360 module in the console.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Customer 360 Node

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Customer 360 Node**.
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
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **Customer 360 Node**.

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
# Customer 360 Node

**Module**: Bot Studio

## Overview
While customers interact with a Bot, businesses can view these interactions on the Customer 360 module in the console.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### When to use

While customers interact with a Bot, businesses can view these interactions on the Customer 360 module in the console.

Businesses can also view if a customer completes a Goal by providing information while interacting with the Bot. This can be achieved by using the CDP Goal Node in Bot Studio. This means that the customer has provided information that can be viewed in the Customer 360 module.

### How to use

Let us consider an example where a customer provides information about preferred Insurance while interacting with a bot. Each time a customer selects an Insurance Preference, the journey sends this information to the Customer 360 module at run-time using CDP Goal Node.

At design-time:

- In the Customer 360 module, a profile property named "Insurance Preference" can be added. To learn more about the same on Customer 360 module, contact us at console-support@gupshup.io.
- Now that the profile property is added in the Customer 360 module, it can be fetched in the CDP Goal Node in the Bot Studio Journey. Select the attribute(i.e. the profile property added in Customer 360) and either type a value or select a variable.
- At run-time, when a customer responds to the Bot, the CDP Goal Node sends this information to Customer 360 module. To view this in Customer 360 module, contact us at console-support@gupshup.io.
### Limitations:

- CDP Goal Node is available in Left Node panel only if Customer360 module is available in console recipe
- Only text attributes are allowed.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
