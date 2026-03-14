source_url: https://console-docs.gupshup.io/docs/prompt-enhancer

<!-- kb-golden:v10 -->
# Skill Prompt Enhancer (Developer Mode)

**Module**: Ai Admin

## Definition
Introduction: Skill Prompt Enhancer, a powerful new feature designed to help you craft highly effective and optimized skill instructions for your AI agents. Enhancer directly addresses common challenges in prompt engineering, ensuring your agents perform at their best.

## Procedure
### Exact UI path
Gupshup Console → Ai Admin → Skill Prompt Enhancer (Developer Mode)

### Prerequisites
- Access to **Gupshup Console → Ai Admin → Skill Prompt Enhancer (Developer Mode)** in Gupshup Console.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Ai Admin**.
3. Go to **Skill Prompt Enhancer (Developer Mode)**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run a quick test and confirm the expected behavior appears in the target module/UI.

### Troubleshooting
- Inefficient Iterations: Providing guided feedback to streamline the prompt refinement process, reducing manual trial and error.
- Retry After Failure: If an enhancement fails, you are allowed a maximum of 1 retry.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Ai Admin**.
- Go to **Skill Prompt Enhancer (Developer Mode)**.

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
# Skill Prompt Enhancer (Developer Mode)

**Module**: Ai Admin

## Overview
Introduction: Skill Prompt Enhancer, a powerful new feature designed to help you craft highly effective and optimized skill instructions for your AI agents. Enhancer directly addresses common challenges in prompt engineering, ensuring your agents perform at their best.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Introduction: Skill Prompt Enhancer, a powerful new feature designed to help you craft highly effective and optimized skill instructions for your AI agents. Enhancer directly addresses common challenges in prompt engineering, ensuring your agents perform at their best.

## Understanding the Skill Prompt Enhancer:

The performance of an AI agent is heavily reliant on the clarity, completeness, and contextual relevance of its skill prompts. The Skill Prompt Enhancer is an AI-powered assistant that helps you overcome common issues such as:

- Vague or Complex Instructions: Transforming unclear prompts into precise and actionable directives.
- Inconsistent Tone or Structure: Standardizing the voice and format across different skills within your agent.
- Unclear Engagement Flows: Enhancing the reliability and predictability of your agent's behavior.
- Inefficient Iterations: Providing guided feedback to streamline the prompt refinement process, reducing manual trial and error.
## Enhancing Your Skill Prompts

The enhancement process is interactive and gives you control over the suggestions.

- Field Selection & Additional Remarks
- Upon clicking "Enhance with AI" button in Instructions section on Skill creation page field selection modal will appear.
- Field Selection: You'll see a list of fields from your skill instructions that can be enhanced. By default, all fields are unselected. Select the specific fields you want the AI to enhance.
Note: A field must have a minimum of 50 characters in its base prompt to be available for selection. If a field doesn't meet this criteria, it will be disabled

- Additional Remarks (Optional): You can provide up to 200 characters of additional context or specific instructions for the AI to consider during the enhancement.
- Enhancement in Progress: A loader screen will appear, displaying a progress bar and text, indicating that the enhancement is in progress. You can click the "Stop Enhancement" button at any time to halt the process and close the modal.
- Reviewing Enhanced Prompts
- After the enhancement is complete, the "Enhanced Prompt Modal" will display the results for your review:
- Enhancement Summary: At the top, you'll find a summary (up to 100 words, typically 3-5 lines) of the enhancements made. This summary provides valuable feedback to help you improve your prompt writing techniques.
- User Prompt vs. Enhanced Prompt Comparison: This side-by-side view visually compares your original prompt with the AI-enhanced version. Color coding highlights text deletions and additions for easy review.
- Field-Level Accept/Discard Option: By default, all enhanced prompt fields will be selected (indicated by a checkmark ☑️).
- To discard an enhanced prompt for a specific field and retain your original text, click the discard icon (✖️) next to that field.
- The boundary of the user prompt field will be highlighted if you discard the enhanced version, and the enhanced prompt field's boundary will be highlighted if it's accepted.
- Split Instructions Fields: For easier review, the instructions are split into different sections. You can navigate between these sections using the "Prev" and "Next" buttons.
- Saving Enhanced Prompts: The "Save" button on the enhanced prompt modal will only be enabled once you have reviewed all sections by clicking through them using the "Next" button.
- Clicking "Save" will apply the accepted enhanced prompts to your skill instructions.
## Feature Usage Restrictions & UI Validations

To ensure optimal performance and fair usage, certain restrictions and UI behaviors are in place:

- Enhancement Limit: You can perform a maximum of 5 enhancements per skill/per day.
- Retry After Failure: If an enhancement fails, you are allowed a maximum of 1 retry.
- "Enhance with AI" Button State: For a new user it will be enabled once instructions are generated and skill is saved.
- After a successful enhancement, the button will be disabled. It will re-enable once you edit the instructions.
- Modal State Retention: The enhancer modal will not retain its state if you click the save button or the 'X' icon, or if you navigate away from the page while enhancement is in progress.
Updated 8 months ago

- Tools (Developer Mode)

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Saving Enhanced Prompts: The "Save" button on the enhanced prompt modal will only be enabled once you have reviewed all sections by clicking through them using the "Next" button.
- - Clicking "Save" will apply the accepted enhanced prompts to your skill instructions.
- - Modal State Retention: The enhancer modal will not retain its state if you click the save button or the 'X' icon, or if you navigate away from the page while enhancement is in progress.
