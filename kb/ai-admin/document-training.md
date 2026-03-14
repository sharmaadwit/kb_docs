source_url: https://console-docs.gupshup.io/docs/document-training

<!-- kb-golden:v10 -->
# Document Training

**Module**: Ai Admin

## Definition
Steps to train documents:

## Procedure
### Exact UI path
Gupshup Console → Ai Admin → Document Training

### Prerequisites
- Access to **Gupshup Console → Ai Admin → Document Training** in Gupshup Console.

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
- If something does not work as expected, re-check the exact UI path, required fields, and any save/deploy step.

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
# Document Training

**Module**: Ai Admin

## Overview
Steps to train documents:

## When to use
_Add the primary scenarios and personas._

## Setup path
- Go to "Files" section in Content Tab.

## Step-by-step configuration
Steps to train documents:

- Go to "Files" section in Content Tab.
- Click on choose File to upload single/multiple files.
- Click on "Save & Train".
Note:

- Allowed file format are .pdf, .txt, .csv.
- Maximum file size can be 20 MB.
- Maximum 20 files can be uploaded in a single training.
### Advanced Pdf Parser

Advanced mode introduced for parsing pdfs containing images and complex tabular data to enhance content training capabilities. Advanced parsing is done using GPT-4O model. User can select Advanced option in the file upload modal which appears when user clicks on "Choose File" in Content Tab.

Value Delivered:

- Increased run time AI accuracy in response generation for PDF-based content
- Reduced manual effort during content training as no pre processing required for complex pdf
- Supports real-world business documents like, brochures, reports and more
Basic vs Advanced Usage Guidelines

Basic: Default Parsing option for all the pdf files. Simple pdfs which contains some images and mainly text can be easily parsed using Basic option.

Advanced: Use Advanced option only when PDF contains lots of images and nested tabular data (High training time & cost as compared to Basic)

Key Limitations:

- Parsing accuracy will be based on clarity of the image text
- Slow & Costly content extraction
- Final content extraction accuracy depends on the performance of LLM Model (Gpt-4O)
- Extraction is subjected to Azure content moderation policy - if it detects certain words in the content then it can get blocked
- Model may not perform optimally when handling images with text of non-Latin alphabets, such as Japanese or Korea
- The model may misinterpret rotated or upside-down text and images
- Not suggested for medical use cases like interpreting CT scan images

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Click on "Save & Train".

**Last updated (from source)**: Updated 10 months ago
