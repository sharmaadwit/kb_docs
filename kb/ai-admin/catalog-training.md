source_url: https://console-docs.gupshup.io/docs/catalog-training-1

<!-- kb-golden:v7 -->
# Catalog Training

**Module**: Ai Admin

## Definition
User can upload & train their product catalog to answer customer queries regarding product availability, specifications, pricing, and more.

## Procedure
### Exact path
Gupshup Console → Ai Admin → Catalog Training

### Where to configure it
Gupshup Console → Ai Admin → Catalog Training

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to "Files" section in Content Tab.

### Steps
1. Open Gupshup Console.
2. Go to "Files" section in Content Tab.
3. Click on choose File to upload single/multiple files.
4. Click on "Save & Train".

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- The names of the csv files are strict and should not be changed. for e.g. products.csv cannot be renamed.
- The columns and column headers inside the csv are strict and should not be changed. for e.g. the id column should be in the first column and the column header should be id and cannot be changed, deleted or reordered.

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation
- _Add 1–2 bullets distinguishing this module from adjacent modules to reduce retrieval drift._

## Reference (from source)
<!-- procedural:v2 -->
# Catalog Training

**Module**: Ai Admin

## Overview
User can upload & train their product catalog to answer customer queries regarding product availability, specifications, pricing, and more.

## When to use
_Add the primary scenarios and personas._

## Setup path
- Go to "Files" section in Content Tab.

## Step-by-step configuration
User can upload & train their product catalog to answer customer queries regarding product availability, specifications, pricing, and more.

Steps to train Catalog in commerce workspace:

- Go to "Files" section in Content Tab.
- Click on choose File to upload single/multiple files.
- Click on "Save & Train".
Guidelines to upload the Catalog:

- The catalog file is a zip file which directly contains csv files.
- Make sure catalog have 3 mandatory files, shop_details.csv, products.csv, data_import_config.csv. Make sure language present in shop_details.csv is as same as content language (language present in content tab of workspace)
- The names of the csv files are strict and should not be changed. for e.g. products.csv cannot be renamed.
- The columns and column headers inside the csv are strict and should not be changed. for e.g. the id column should be in the first column and the column header should be id and cannot be changed, deleted or reordered.
Updated 10 months ago

- Document Training

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Click on "Save & Train".
