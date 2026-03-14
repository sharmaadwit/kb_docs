source_url: https://console-docs.gupshup.io/docs/catalog-training-1

<!-- kb-golden:v10 -->
# Catalog Training

**Module**: Ai Admin

## Definition
User can upload & train their product catalog to answer customer queries regarding product availability, specifications, pricing, and more.

## Procedure
### Exact UI path
Gupshup Console → Ai Admin → Catalog Training

### Prerequisites
- Access to **Gupshup Console → Ai Admin → Catalog Training** in Gupshup Console.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to "Files" section in Content Tab.
3. Click on choose File to upload single/multiple files.
4. Click on "Save & Train".

### Validation / where to check
- Run a quick test and confirm the expected behavior appears in the target module/UI.

### Troubleshooting
- The names of the csv files are strict and should not be changed. for e.g. products.csv cannot be renamed.
- The columns and column headers inside the csv are strict and should not be changed. for e.g. the id column should be in the first column and the column header should be id and cannot be changed, deleted or reordered.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to "Files" section in Content Tab.

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
