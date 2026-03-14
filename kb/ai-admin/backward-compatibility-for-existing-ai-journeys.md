source_url: https://console-docs.gupshup.io/docs/backward-compatibility-for-existing-ai-journeys

<!-- kb-golden:v10 -->
# Backward Compatibility for existing AI Journeys

**Module**: Ai Admin

## Definition
- Data Workspaces and associated content would move to individual newly created Workspace
- The name of the Workspace would be the respective Data Workspace name
- The system would create an intent “FAQ” in these workspaces
- A new content Tag would be created with the name “General_Content” in respective Workspaces which has the migrated content
### Intent and Entity Migration

## Procedure
### Exact UI path
Gupshup Console → Ai Admin → Backward Compatibility for existing AI Journeys

### Prerequisites
- Access to **Gupshup Console → Ai Admin → Backward Compatibility for existing AI Journeys** in Gupshup Console.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Ai Admin**.
3. Go to **Backward Compatibility for existing AI Journeys**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run a quick test and confirm the expected behavior appears in the target module/UI.

### Troubleshooting
- If something does not work as expected, re-check the exact UI path, required fields, and any save/deploy step.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Ai Admin**.
- Go to **Backward Compatibility for existing AI Journeys**.

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
# Backward Compatibility for existing AI Journeys

**Module**: Ai Admin

## Overview
- Data Workspaces and associated content would move to individual newly created Workspace
- The name of the Workspace would be the respective Data Workspace name
- The system would create an intent “FAQ” in these workspaces
- A new content Tag would be created with the name “General_Content” in respective Workspaces which has the migrated content
### Intent and Entity Migration

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
# Generic Workspace Migration:

## Data Workspaces Migration

- Data Workspaces and associated content would move to individual newly created Workspace
- The name of the Workspace would be the respective Data Workspace name
- The system would create an intent “FAQ” in these workspaces
- A new content Tag would be created with the name “General_Content” in respective Workspaces which has the migrated content
### Intent and Entity Migration

- Intent and Entities created in the AI Admin would move to a workspace with the name; Default Workspace
- By default post-migration, the Default Workspace will have migrated Intent and Entities and no Content
## Commerce Workspace Migration

### Data Workspaces Migration

- Data Workspaces and associated content on Commerce Workspace would move to individual newly created Multiple Workspace
- The name of the Workspace would be #DataWorkspace name
- The system would create an intent “Product Search, Q&A”
- A new category would be created with the name “General_Catalog” in respective Data Workspaces which has catalog and content
- The system would migrate the JSON in the Journey Builder AS-IS
Please note:- Workspaces were successfully migrated on 04 April 2024; please contact support if you experience any issues.

Updated 10 months ago

- Workspace Validation

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
