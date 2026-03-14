source_url: https://console-docs.gupshup.io/docs/ai-analytics

<!-- kb-golden:v10 -->
# AI Analytics

**Module**: Bot Studio Analytics

## Definition
AI Analytics is a feature to monitor and evaluate the utterances on your bot. This feature assists users in identifying and classifying utterances, offering valuable insights into both recognized and unrecognized intents.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio Analytics → AI Analytics

### Prerequisites
- Access to **Gupshup Console → Bot Studio Analytics → AI Analytics** in Gupshup Console.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio Analytics**.
3. Go to **AI Analytics**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run a test event/journey and confirm the expected analytics or goal data appears in the UI.

### Troubleshooting
- If something does not work as expected, re-check the exact UI path, required fields, and any save/deploy step.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Bot Studio Analytics**.
- Go to **AI Analytics**.

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
# AI Analytics

**Module**: Bot Studio Analytics

## Overview
AI Analytics is a feature to monitor and evaluate the utterances on your bot. This feature assists users in identifying and classifying utterances, offering valuable insights into both recognized and unrecognized intents.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
AI Analytics is a feature to monitor and evaluate the utterances on your bot. This feature assists users in identifying and classifying utterances, offering valuable insights into both recognized and unrecognized intents.

## Total Utterances

- Total Utterances represents the number of all utterances classified either as specific intents or unidentified intents.
- Unidentified Intents represents the number of utterances that the system was unable to classify into any specific intent category.
- Identified Intents represents the number of utterances successfully classified into specific intent categories by the system.
## FAQ Utterances

- Total FAQs Utterances represents the number of all utterances that have been successfully categorized as belonging to the FAQ (Frequently Asked Questions) intent.
- Answered FAQ represents the number of utterances classified as FAQ intents that have been responded to with an appropriate answer.
- Unanswered FAQrepresents the number of utterances classified as FAQ intents that did not receive a corresponding answer.
FAQ Utterances will be available for you only if you have created a Generic Workspace in AI Admin.

## Product Search & Query Utterances

- Total Product Search & Query Utterances represents the number of all utterances that have been successfully categorized as belonging to the Product Search & Query intent.
- Answered represents the number of utterances classified as Product Search & Query intents that have been responded to with an appropriate answer.
- Unanswered represents the number of utterances classified as Product Search & Query intents that did not receive a corresponding answer.
Product Search & Query Utterances will be available for you only if you have created a Commerce Workspace in AI Admin.

### The data in Bot Studio Analytics is retained for a period of one year.

Please export required data within a year and store it on your end for later reference.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
