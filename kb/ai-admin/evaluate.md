source_url: https://console-docs.gupshup.io/docs/generate-qa

<!-- kb-golden:v10 -->
# Evaluate

**Module**: Ai Admin

## Definition
Introduction: User can now generate Q&A from the trained content via topic prompt or file upload in the new Evaluate tab of AI Admin.

## Procedure
### Exact UI path
Gupshup Console → Ai Admin → Evaluate

### Prerequisites
- Access to **Gupshup Console → Ai Admin → Evaluate** in Gupshup Console.

### Fields to configure
- file name for export
- Topic Prompt & Question count for generation

### Steps
1. Open Gupshup Console.
2. Go to **Ai Admin**.
3. Go to **Evaluate**.
4. Enter file name for export.
5. Select All or Individual Content tags.
6. Enter Topic Prompt & Question count for generation.
7. Select LLM Configuration (Model, Answer Type & Precision).
8. Click on Generate button.
9. Click on Generate button.
10. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run a quick test and confirm the expected behavior appears in the target module/UI.

### Troubleshooting
- Only 1 generation/regeneration request allowed at a given time in the workspace.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Ai Admin**.
- Go to **Evaluate**.

## Options / variants
- Enter file name for export
- Select All or Individual Content tags.
- Enter Topic Prompt & Question count for generation.
- Select LLM Configuration (Model, Answer Type & Precision)

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
# Evaluate

**Module**: Ai Admin

## Overview
Introduction: User can now generate Q&A from the trained content via topic prompt or file upload in the new Evaluate tab of AI Admin.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Introduction: User can now generate Q&A from the trained content via topic prompt or file upload in the new Evaluate tab of AI Admin.

Key Benefits:

- Allows users to ensure that the generated answers align with the trained content
- Identify gaps or inconsistencies in the training data for corrective actions
- Modify answers to retrain the LLM with expected answers
Steps to Generate Q&A via Prompt

- Enter file name for export
- Select All or Individual Content tags.
- Enter Topic Prompt & Question count for generation.
- Select LLM Configuration (Model, Answer Type & Precision)
- Click on Generate button
- View generated source file on in the generate prompt tile.
Additional Info:

- Max 50 questions allowed in a single generate operation via prompt
- Default values visible in the LLM configuration will be same as configuration present in workspace settings tab
- Based on available content & context generated questions can be less than or equal to the question count entered by the user
Steps to Generate Q&A via Upload

- Select All or Individual Content tags.
- Upload questions in sample csv format.
- Select LLM Configuration (Model, Answer Type & Precision)
- Click on Generate button.
- View generated source file on in the generate upload tile.
Additional Info:

- Max 100 unique question are allowed in csv for answer generation. Duplicate questions will be ignored.
Tile View In Evaluate Tab: For every Generate operation a new tile will be generated and source file will be present in the tile. Source file can be downloaded in csv format & if content tag is trained with new content user can regenerate the answers for same set of questions by clicking on regenerate icon.

Key Highlights:

- Content Sources Covered: Docs, Website URL, Text, Files. Product Catalog is not referred.
- Data Retention: 365 Days
- Workspace Availability: Both Generic & Commerce Workspaces
- Generate Q&A csv compatible with teach module
- Max 50 generation request allowed in a workspace. No limit on regeneration. To create new generation request, user can delete existing tiles when 50 limit is reached.
- Only 1 generation/regeneration request allowed at a given time in the workspace.
- User can change LLM configuration parameters (Model, Answer Type & Precision Threshold) to evaluate the impact on generated Q&A.
Updated 10 months ago

- AI Agents (Beta)

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
