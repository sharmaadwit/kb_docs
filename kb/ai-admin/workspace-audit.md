source_url: https://console-docs.gupshup.io/docs/workspace-audit

<!-- kb-golden:v10 -->
# Workspace Audit

**Module**: Ai Admin

## Definition
The Workspace Audit feature provides a complete record of all changes made in a workspace. It allows users to audit actions such as content training/untraining, intents & entities creation, updating workspace settings, etc. Audit records will help users in transparent change tracking, issue debugging & regulatory compliance.

## Procedure
### Exact UI path
Gupshup Console → Ai Admin → Workspace Audit

### Prerequisites
- Access to **Gupshup Console → Ai Admin → Workspace Audit** in Gupshup Console.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Ai Admin**.
3. Go to **Workspace Audit**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run a quick test and confirm the expected behavior appears in the target module/UI.

### Troubleshooting
- If something does not work as expected, re-check the exact UI path, required fields, and any save/deploy step.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Ai Admin**.
- Go to **Workspace Audit**.

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
# Workspace Audit

**Module**: Ai Admin

## Overview
The Workspace Audit feature provides a complete record of all changes made in a workspace. It allows users to audit actions such as content training/untraining, intents & entities creation, updating workspace settings, etc. Audit records will help users in transparent change tracking, issue debugging & regulatory compliance.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
The Workspace Audit feature provides a complete record of all changes made in a workspace. It allows users to audit actions such as content training/untraining, intents & entities creation, updating workspace settings, etc. Audit records will help users in transparent change tracking, issue debugging & regulatory compliance.

Key Highlights:

- Coverage: Intent, Entity, Content, Teach & Settings Module
- Data Refresh: Real Time
- Retention Period: Last 90 Days
Here’s what you can do:

- View Audit records in Table: User can see individual records for each save & train operation in the tabular format. For detailed audit information user can click on a record and a summary side hug will appear showing important information like Training Status, Failure Reason, Training Duration, Module (Intent, Entity, Content, Settings) specific training information, and more.
- Filter Data: Users can select Workspace & Training Status filter options & click on the apply button to view the filtered data. Also the audit data of last 90 days can be seen by applying the date range.
Note: When Training Status is selected as NA then all the records where Settings Module configuration is updated will be visible.

- Export Audit Data: Audit data can be exported in async way by clicking on export button present inside the Workspace audit tab. User can enter the file name and select relevant columns in a UI for async export. Previous exports of last 7 days are also visible in the export summary. Summary can be viewed by clicking on View Export Summary button present in the export UI.
Updated 10 months ago

- LLM Consumption

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
