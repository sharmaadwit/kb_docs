source_url: https://console-docs.gupshup.io/docs/content-untraining
# AI Admin

## Content Untraining

# Content Untraining

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
