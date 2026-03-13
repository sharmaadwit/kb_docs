source_url: https://console-docs.gupshup.io/docs/ai-analytics

<!-- kb-golden:v7 -->
# AI Analytics

**Module**: Bot Studio Analytics

## Definition
AI Analytics is a feature to monitor and evaluate the utterances on your bot. This feature assists users in identifying and classifying utterances, offering valuable insights into both recognized and unrecognized intents.

## Procedure
### Exact path
Gupshup Console → Bot Studio Analytics → AI Analytics

### Where to configure it
Gupshup Console → Bot Studio Analytics → AI Analytics

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio Analytics**.
- Go to **AI Analytics**.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio Analytics**.
3. Go to **AI Analytics**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- The data in Bot Studio Analytics is retained for a period of one year.

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
