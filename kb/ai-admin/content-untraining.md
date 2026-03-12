source_url: https://console-docs.gupshup.io/docs/content-untraining

<!-- kb-golden:v1 -->
# Content Untraining

**Module**: Ai Admin

## Definition
Content Untraining enhancement allows users to manage their trained content more effectively by enabling the removal of previously trained content.

## Procedure
### Where to configure it
Gupshup Console → Ai Admin → Content Untraining

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Ai Admin → Content Untraining**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Reference (from source)
<!-- procedural:v2 -->
# Content Untraining

**Module**: Ai Admin

## Overview
Content Untraining enhancement allows users to manage their trained content more effectively by enabling the removal of previously trained content.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Content Untraining enhancement allows users to manage their trained content more effectively by enabling the removal of previously trained content.

Here’s what you can do:

- Untrain Website Links: You can easily untrain specific URLs previously used to train the LLM. This ensures the AI no longer references content from those sources in its responses.
Steps to Untrain the Website Links:

- Click on the Untrain Website Links button present in the Website Links section to open a modal that contains all the trained URLs. Untrain button gets enabled when the user clicks on Edit Content button.
- Select all the URLs you want to untrain & click on the Review Link Button.
Additional Info:

- In a single untrain operation users can select up to a maximum of 50 links. If more links are selected then the Review Links button will go into disabled state.
- Users can discard link selection by clicking on the Discard Selection text button.
- URL search functionality is also available in scenarios when a large number of trained URLs are present.
- After link selection if the user closes the modal by clicking on X icon then user will be notified for pending action warning.
- Review all the selected links in review modal before sending them for untraining. After the review, click on Untrain Links Button for successful addition of links for untraining operation.
Additional Info:

- If the user wants to add or remove more links then click on back icon present on the top left of modal & make the required changes.
- User can cancel the untraining operation by clicking on the Exit Untraining button.
- During the link review if user closes the modal by clicking on X icon then user will be notified for pending action warning.
- Click on the Save & Train button present in the Content section to complete the Untraining.
CSV Report for Untrained Links: After untraining, users can now download a detailed CSV report that lists all the untrained URLs. This provides transparency and documentation for content management activities.

- Untrain Documents: Remove specific documents from the training data, ensuring that the AI no longer includes the information from these documents in its answers.
Steps to Untrain the Documents

- Click on the Edit Content button present in the Content section.
- Click on the Delete icon present on each file you want to untrain. If the Delete icon is accidentally clicked for a file then you can revert the action by clicking on undo icon.
- Click on Save & Train button present in Content section to complete the Untraining.
Additional Info: Once untraining is done then AI will no longer refer the untrained content once any of the following condition is met

- User initiates a new chat session
- If FAQ was not triggered in last 6 user messages in the same session
Updated 10 months ago

- Teach

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Click on the Save & Train button present in the Content section to complete the Untraining.
- - Click on Save & Train button present in Content section to complete the Untraining.
