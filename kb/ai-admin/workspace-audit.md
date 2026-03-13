source_url: https://console-docs.gupshup.io/docs/workspace-audit

<!-- kb-golden:v7 -->
# Workspace Audit

**Module**: Ai Admin

## Definition
The Workspace Audit feature provides a complete record of all changes made in a workspace. It allows users to audit actions such as content training/untraining, intents & entities creation, updating workspace settings, etc. Audit records will help users in transparent change tracking, issue debugging & regulatory compliance.

## Procedure
### Exact path
Gupshup Console → Ai Admin → Workspace Audit

### Where to configure it
Gupshup Console → Ai Admin → Workspace Audit

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Ai Admin**.
- Go to **Workspace Audit**.

### Steps
1. Open Gupshup Console.
2. Go to **Ai Admin**.
3. Go to **Workspace Audit**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- _List the key variants/toggles visible in the UI._

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
