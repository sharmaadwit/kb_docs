source_url: https://console-docs.gupshup.io/docs/enhanced-list-nodedynamic

<!-- kb-golden:v9 -->
# Enhanced List Node(Dynamic)

**Module**: Bot Studio

## Definition
Send Dynamic Sections and Rows above and beyond the Channel Limit using Bot Studios Enhanced List Node functionality.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Enhanced List Node(Dynamic)

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Enhanced List Node(Dynamic)**.
4. Provide selection of different Cities(in rows) where service centers are available in different States(in section).
5. Click **Save** (or **Save & Deploy**) to apply changes.

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
- Go to **Enhanced List Node(Dynamic)**.

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
# Enhanced List Node(Dynamic)

**Module**: Bot Studio

## Overview
Send Dynamic Sections and Rows above and beyond the Channel Limit using Bot Studios Enhanced List Node functionality.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Send Dynamic Sections and Rows above and beyond the Channel Limit using Bot Studios Enhanced List Node functionality.

WhatsApp has a default limitation of only up to 10 items that can be shared in a List Message. But with just click of a checkbox you can send up to 100 items without any need to split them into different lists or option. This feature makes your end user conversational experience 10x better by providing a limitless experience of browsing products or searching through different available options on a list.

In the How to use Dynamic List you have learnt on how a JSON Payload can be passed for the dynamic sectionss/row within WhatsApp limit of 10 items.

Now with the new enhanced feature you can just tick the checkbox if your dynamic JSON payload can contain more that 10 items and we will make sure the end user get the items in multiple lists with a default Navigation option as shown below:

### Representation on Bot Studio Canvas

### Representation on WhatsApp:

This lets you cover simple to complex use cases such as:

- Provide selection of different Cities(in rows) where service centers are available in different States(in section)
- List of available Time slots(in rows) for different Dates(in section)
- List of user searched Products(in rows) for different Categories(in section)

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
