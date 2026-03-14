source_url: https://console-docs.gupshup.io/docs/llm-consumption

<!-- kb-golden:v10 -->
# LLM Consumption

**Module**: Ai Admin

## Definition
This feature allows users to track API calls and token consumption during customer interactions with an LLM-powered chatbot. It provides valuable insights to:

## Procedure
### Exact UI path
Gupshup Console → Ai Admin → LLM Consumption

### Prerequisites
- Access to **Gupshup Console → Ai Admin → LLM Consumption** in Gupshup Console.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Ai Admin**.
3. Go to **LLM Consumption**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run a quick test and confirm the expected behavior appears in the target module/UI.

### Troubleshooting
- If something does not work as expected, re-check the exact UI path, required fields, and any save/deploy step.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Ai Admin**.
- Go to **LLM Consumption**.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Identify the upstream module where this is configured and the downstream module where the outcome is verified.

## Module disambiguation docs
- Distinguish this page from adjacent modules/settings before troubleshooting elsewhere.

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
