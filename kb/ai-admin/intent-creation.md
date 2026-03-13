source_url: https://console-docs.gupshup.io/docs/intent-creation

<!-- kb-golden:v9 -->
# Intent Creation

**Module**: Ai Admin

## Definition
Intent refers to the goal or purpose behind a user's input or query. It represents what the user wants to achieve or convey through their text or speech. For example, when a user types or says, "I ordered a bag last week. When will you deliver it" the intent is to track_order_status.

## Procedure
### Exact UI path
Gupshup Console → Ai Admin → Intent Creation

### Steps
1. Open Gupshup Console.
2. Go to Intent section & Select the required intent to start the untraining
3. Navigate to the utterance you want to untrain & click on the Delete icon. If the Delete icon is accidentally clicked for an utterance then you can revert the action by clicking on the undo icon.
4. Click on Create Intent button present in Intents tag.
5. Enter the Intent Name & Description.
6. Click on Generate Utterances button. AI will generate utterances based on provided intent description.
7. Add few manual utterances to include more variations. (Optional).
8. Click on Save & Train.
9. Click on Save & Train button to complete the untraining.

### Validation / where to check
- _Run a quick smoke test and confirm expected behavior._

### Fields to configure
- Intent Name & Description
- few manual utterances to include more variations. (Optional)

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- _Add common failure modes and how to fix them._

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to Intent section & Select the required intent to start the untraining
- Navigate to the utterance you want to untrain & click on the Delete icon. If the Delete icon is accidentally clicked for an utterance then you can revert the action by clicking on the undo icon.

## Options / variants
- Enter the Intent Name & Description.
- Add few manual utterances to include more variations. (Optional)

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
# Intent Creation

**Module**: Ai Admin

## Overview
Intent refers to the goal or purpose behind a user's input or query. It represents what the user wants to achieve or convey through their text or speech. For example, when a user types or says, "I ordered a bag last week. When will you deliver it" the intent is to track_order_status.

## When to use
_Add the primary scenarios and personas._

## Setup path
- Go to Intent section & Select the required intent to start the untraining
- Navigate to the utterance you want to untrain & click on the Delete icon. If the Delete icon is accidentally clicked for an utterance then you can revert the action by clicking on the undo icon.

## Step-by-step configuration
## Introduction

Intent refers to the goal or purpose behind a user's input or query. It represents what the user wants to achieve or convey through their text or speech. For example, when a user types or says, "I ordered a bag last week. When will you deliver it" the intent is to track_order_status.

Types of Intent:

- System Intent: Intents automatically created when content is trained in workspace. Product Search, Q&A intent is the system intent for Commerce domain workspace & FAQ intent for generic domain.
- Custom Intent: Intents created by manually by user.
In a single workspace maximum of 20 intents (System & Custom) can be created.

Steps to Create a custom Intent:

- Click on Create Intent button present in Intents tag.
- Enter the Intent Name & Description.
- Click on Generate Utterances button. AI will generate utterances based on provided intent description.
- Add few manual utterances to include more variations. (Optional)
- Click on Save & Train
Adding Utterances for Intent Training: User can ask AI to generate utterances based on provided intent description and also add the utterances manually in the training data.

## Intent Utterance Training

Intent Utterance Untraining allows users to delete specific utterances from an intent that has already been trained in the ACE LLM model ensuring more precise and accurate model fine tuning.

Steps to Untrain Intent Utterances:

- Go to Intent section & Select the required intent to start the untraining
- Navigate to the utterance you want to untrain & click on the Delete icon. If the Delete icon is accidentally clicked for an utterance then you can revert the action by clicking on the undo icon.
Note: At present you can only untrain the manually added user utterances. Untraining of AI generated utterances is not allowed at the moment.

- Click on Save & Train button to complete the untraining.
Updated 10 months ago

- Intent Description

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Click on Save & Train
- - Click on Save & Train button to complete the untraining.
