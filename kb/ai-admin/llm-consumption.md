source_url: https://console-docs.gupshup.io/docs/llm-consumption

<!-- kb-golden:v9 -->
# LLM Consumption

**Module**: Ai Admin

## Definition
This feature allows users to track API calls and token consumption during customer interactions with an LLM-powered chatbot. It provides valuable insights to:

## Procedure
### Exact UI path
Gupshup Console → Ai Admin → LLM Consumption

### Steps
1. Open Gupshup Console.
2. Go to **Ai Admin**.
3. Go to **LLM Consumption**.
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
- Go to **Ai Admin**.
- Go to **LLM Consumption**.

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation docs
- _Add 1–2 bullets distinguishing this module from adjacent modules to reduce retrieval drift._

## Reference (from source)
<!-- procedural:v2 -->
# LLM Consumption

**Module**: Ai Admin

## Overview
This feature allows users to track API calls and token consumption during customer interactions with an LLM-powered chatbot. It provides valuable insights to:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
This feature allows users to track API calls and token consumption during customer interactions with an LLM-powered chatbot. It provides valuable insights to:

- Monitor usage patterns
- Support billing reconciliation
- Manage project costs effectively
Also, the consumption data will be populated once daily at Workspace & LLM level.

Key Highlights:

- Coverage: Workspace Training & AI Inference Calls
- Data Refresh: Once Daily
- Retention Period: 1 year
Here’s what you can do

- Check the total count of API calls & tokens consumed in widgets.
- Track the Consumption trend in the Line Chart: User can check the consumption trend in the line chart by applying a single select Data Parameter (API Call, Token) Filter. The Y-axis on the chart will display the Data parameter value against time periods on the X-axis, such as months, weeks, or days.
- View Workspace Level Consumption Info in Table: User can track the date-wise consumption at workspace level for each LLM in the table.
- Filter Data: User can select Workspace & LLM filter options (multi-select) & click on apply button to view the filtered data. Also, the consumption data for the last 1 year can be seen by applying the date range.
- Export Consumption Data: LLM consumption data can be exported in async way by clicking on export button present inside the LLM consumption tab. User can enter the file name and select relevant columns in a UI for async export. Previous exports of last 7 days are also visible in the export summary. Summary can be viewed by clicking on View Export Summary button present in the export UI.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
