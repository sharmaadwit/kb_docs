source_url: https://console-docs.gupshup.io/docs/workspace-validation

<!-- procedural:v2 -->
# Workspace Validation

**Module**: Ai Admin

## Overview
Introduction: Workspace validation feature will validate user actions in a workspace against a set of pre defined conditions to show Warnings & Recommendations. Complying with these pre defined conditions improves overall bot performance for AI powered journeys. Validation features assist users in settings up the workspace according to best practices.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Introduction: Workspace validation feature will validate user actions in a workspace against a set of pre defined conditions to show Warnings & Recommendations. Complying with these pre defined conditions improves overall bot performance for AI powered journeys. Validation features assist users in settings up the workspace according to best practices.

Key Highlights:

- Validation icon introduced at workspace level to show warnings & recommendations in separate tabs
- Validation conditions are checked after every save & train operation
- User is redirected to relevant page to take corrective action on warnings & recommendations
- Validation icon is be visible inside the workspace if at least 1 warning or recommendation is there
- Error icon is introduced workspace having warning or recommendation on workspace listing page
Validation Conditions:

Warnings

Recommendations

Condition: No Content Uploaded in content section

Title: Content Missing in Content section Description: Add training data in workspace for answering questions

- *Condition: less than 10 utterances ( AI + Manual) trained for a single Intent - ** Title: Less than 10 utterances mapped to intent Description: Sample utterances help improve consistency in intent detection
Condition: No Workspace Instructions for answers in the Settings Tab

Title: Instructions for answers missing in Settings section Description: Workspace instructions provides more context to the bot on its role and improves overall behavior

Condition: No Sample Values: #Entity 1, #Entity2

Title: Sample values missing for Entity Description: Improves consistency for certain entity values

- *Condition: No Entity mapped to Intent ** Title: Intent-Entity Mapping Missing Description: Entity detection will be skipped for intent related utterances
Condition: No Extended Values:#Entity 1, #Entity2

Title: Add extended values for Entity Description: Improves handling of input variability and better generalization in recognizing entity

Condition: Precision Threshold is lower than 30%

Title: Precision Threshold less than 30% Description: Low threshold may lead to inaccurate answers from bot

Condition: No Manual Utterances mapped to Intent

Title: Manual Utterance not added for intent Description: Manual utterances improves accuracy of model prediction

Updated 10 months ago

- Intent & Entity

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Validation conditions are checked after every save & train operation

