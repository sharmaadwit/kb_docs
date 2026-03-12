source_url: https://console-docs.gupshup.io/docs/backward-compatibility-for-existing-ai-journeys

<!-- kb-golden:v4 -->
# Backward Compatibility for existing AI Journeys

**Module**: Ai Admin

## Definition
- Data Workspaces and associated content would move to individual newly created Workspace
- The name of the Workspace would be the respective Data Workspace name
- The system would create an intent “FAQ” in these workspaces
- A new content Tag would be created with the name “General_Content” in respective Workspaces which has the migrated content
### Intent and Entity Migration

## Procedure
### Exact path
Gupshup Console → Ai Admin → Backward Compatibility for existing AI Journeys

### Where to configure it
Gupshup Console → Ai Admin → Backward Compatibility for existing AI Journeys

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Ai Admin → Backward Compatibility for existing AI Journeys**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- Intent and Entity Migration
- Data Workspaces Migration

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
