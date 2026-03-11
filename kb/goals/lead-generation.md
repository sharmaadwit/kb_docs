source_url: https://console-docs.gupshup.io/docs/lead-generation-goal
# Goals

## Lead Generation

# Lead Generation

Let's take an example of a lead generation journey.

The user details being captured in the journey are name, phone number and email address in that exact order, without any chance of skipping.

### Milestones are sequential in nature. Their sequence is set as per creation, NOT implementation in journeys.

For example, if a Goal has been created with three Milestones in the sequence M1 followed by M2 followed by M3, their sequence remains the same even if M2 and M3 is implemented in a Goal node before M1.

### If a Milestone is skipped and a Milestone after it in the sequence of creation is achieved, the Tracker Values for that milestone are automatically filled with the respective Default Values against the user’s customer ID.

For example, if a user achieves the third Milestone without achieving the first and second Milestones, the respective Default Values are set as Tracker Values entered by that user in the first and second Milestones.

Your Goal for this journey can be named as "Lead Generation", meaning capturing all user details mentioned above.

Your milestones and trackers can be as follows:

- First, you will need to create the goal using the above mentioned details.
First, you will need to create the goal using the above mentioned details.

- Next, you need to insert a Goal Node in the journey right after the user's name has been captured.
Next, you need to insert a Goal Node in the journey right after the user's name has been captured.

- Store the user's name in a local variable (if not done already).
Store the user's name in a local variable (if not done already).

- Select the "Lead Generation" Goal and "Capturing the name" Milestone from the respective dropdowns.
Select the "Lead Generation" Goal and "Capturing the name" Milestone from the respective dropdowns.

- The "Name" tracker will automatically appear under Key Trackers along with a "Value" field. Enter the variable which stores the user's name in the "Value" field.
The "Name" tracker will automatically appear under Key Trackers along with a "Value" field. Enter the variable which stores the user's name in the "Value" field.

- Now, repeat steps 2 to 5 for the phone number and the email address as well.
Now, repeat steps 2 to 5 for the phone number and the email address as well.

Updated 10 months ago
