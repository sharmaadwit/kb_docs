source_url: https://console-docs.gupshup.io/docs/backward-compatibility-for-existing-ai-journeys

<!-- kb-golden:v9 -->
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

### Steps
1. Open Gupshup Console.
2. Go to **Ai Admin**.
3. Go to **Backward Compatibility for existing AI Journeys**.
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
- Go to **Backward Compatibility for existing AI Journeys**.

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
