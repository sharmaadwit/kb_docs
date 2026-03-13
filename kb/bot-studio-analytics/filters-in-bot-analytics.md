source_url: https://console-docs.gupshup.io/docs/bot-analytics-filters

<!-- kb-golden:v7 -->
# Filters in Bot Analytics

**Module**: Bot Studio Analytics

## Definition
If you change your filter selections but don't click Apply , the metrics will be displayed as per the previously implemented filter selections.

## Procedure
### Exact path
Gupshup Console → Bot Studio Analytics → Filters in Bot Analytics

### Where to configure it
Gupshup Console → Bot Studio Analytics → Filters in Bot Analytics

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio Analytics**.
- Go to **Filters in Bot Analytics**.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio Analytics**.
3. Go to **Filters in Bot Analytics**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- Clicking the Apply button implements your filter selections.

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation
- _Add 1–2 bullets distinguishing this module from adjacent modules to reduce retrieval drift._

## Reference (from source)
<!-- procedural:v2 -->
# Filters in Bot Analytics

**Module**: Bot Studio Analytics

## Overview
If you change your filter selections but don't click Apply , the metrics will be displayed as per the previously implemented filter selections.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### Clicking the Apply button implements your filter selections.

If you change your filter selections but don't click Apply , the metrics will be displayed as per the previously implemented filter selections.

## Date

- The start and end dates can be selected using the date filter.
- All metrics below the date filter will update based on the selected date range.
- By default, the metrics and graphs display data from the last 7 days for all tabs except AI (30 days).
## Channel

- The Channel filter can select specific messaging channels for analysis.
- It also offers the ‘Select All’ option in case all the messaging channels are to be selected.
- All metrics below the Channel filter will be updated based on the selected channel(s).
- By default, the metrics display data for the all channels.
## Journey

- The Journey filter can be used to select specific deployed journeys.
- It also offers the ‘Select All’ option in case all the deployed journeys are to be selected.
- All metrics below the Journey filter will update based on the selected journey(s).
- By default, the metrics display data for the all journeys.
## Source Type

- The Source Type filter can be used to select specific conversation sources (Organic, Marketing or CTX).
- It also offers the ‘Select All’ option in case all the source types are to be selected.
- All metrics below the Source Type filter will update based on the selected source type(s).
- By default, the metrics display data for the all applicable source types.
## Source Value

- The Source Value filter can be used to select the Marketing campaign ID or CTX ad ID.
- Source Value filter will be empty when only "Organic" is selected in the Source Type filter.
- All metrics below the Source Value filter will update based on the selected source value(s).
- By default, the metrics display data for the all applicable source types.
## Workspace

- The Workspace filter can select specific workspaces with a 'Select All' option.
- All metrics below the Workspace filter will update based on the chosen workspaces.
- By default, the data displayed includes all available workspaces.
If you don't select any option in a particular filter, clicking Apply will select all options from that filter.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
