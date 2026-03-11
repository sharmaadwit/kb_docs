source_url: https://console-docs.gupshup.io/docs/chat-management-assignment-rules-chat-rules-slas-re-open-time
# AGENT ASSIST

## Chat Management: Assignment Rules

# Chat Management: Assignment Rules

Section 1: Introduction

Definition: Chat Management in Agent Assist refer to the tools and strategies used to streamline the process of handling customer chats, assigning them to the appropriate agents or teams, and maintaining service quality and efficiency.

Uses: Chat management and assignment rules are crucial in ensuring that customer queries and requests are handled promptly, assigned to the right agents or teams, and adhere to service level agreements (SLAs).

Section 2: Default Assignment Rule

Definition: The Default Assignment Rule is an automated rule that assigns chats to agents or teams without specific assignment preferences. It operates continuously, ensuring that chats are assigned as soon as agents are added.

Uses: The default assignment rule is useful for brands with no specific assignment preferences, as it ensures prompt chat assignment and minimizes manual configuration.

Steps to Customize Assignment Rules for Your Operations:

Step 1: Accessing the Assignment Rules Page

- Navigate to the "Settings" tab on the bottom left side of your Agent Assist dashboard.
- Select "Assignment Rules."
Step 2: Creating a New Rule

- Click on the "Add New Rule" button to create a new rule.
- Specify the name of the rule.
Step 3: Adding Conditions to the Rule

- Add conditions to the rule, such as "Channel is equal to WhatsApp," to specify which chats the rule should apply to.
Step 4: Specifying Actions for the Rule

- Choose between "Sticky Assignment" or specify a "Team/Agent Name" to assign chats to.
- "Sticky Assignment" ensures that reopened chats go to the same agent.
Step 5: Saving the Rule

- Click "Save" to save the rule.
Note: For automatic assignment to happen, Please make sure you have added Agent Handover Node on the Bot Journey

Note: Whenever a chat comes for assignment and the agents are not available to take the chat then the system will retry the chat for assignment for next 30 minutes. If agents are available within that time then the chat will be assigned to them else the chat will move to unassigned chats. The Supervisor will then have to manually assign the chats to the agents

Section 3: The Role of Tags in Assigning Chats

Definition: Tags are labels or identifiers that can be applied to chats to categorize them based on specific criteria, such as team structure or bot journeys.

Uses: Tags play a significant role in chat assignment by allowing brands to direct chats to teams based on tags, making it easier to manage and assign chats efficiently.

Steps to Use Tags for Chat Assignment:

Step 1: Create Tags

- In Agent Assist, go to "Settings" > "Tags."
- Create tags as per the teams or bot journeys you've defined.
Step 2: Create Assignment Rules

- Go to "Assignment Rules" in the "Settings" section.
- In the condition, select "chat tags includes any of the following" and choose one of the created tags.
- In the action, select the team to which you want to map the tag in the condition.
Step 3: Map Tags in Bot Studio

- In the agent handover node on a specific journey in Bot Studio, click on the tags dropdown and select the tag to map it with the journey.
Section 4: Sticky Assignment

Definition: Sticky Assignment is a feature that assigns reopened chats to the same agent who previously handled them, ensuring chat continuity.

Uses: Sticky Assignment enhances customer-agent relationships by ensuring that customers interact with the same agent when reopening chats, thereby improving the overall customer experience.

There are a few scenarios in which Sticky assignment works depending on the configuration:

- If Sticky Assignment is disabled then if the chat is re-opening from resolve then the chat will go for re-assignment and it will try to match the assignment rules. If the chat matches with the assignment rules then the chat will be assigned to the agents according to the matched assignment rule
- If Sticky assignment is set to Active Agent only then whenever the chat is re-opening from resolve then the system will check if the previously assigned agent is available. If the agent is available and online then the chat will be assigned to that same agent else it will get assigned to another available agent
- If Sticky assignment is set to all agents then whenever the chat is re-opening from resolve then the system will assign the chat to the same agent who addressed the chat even if the agent is available or busy
Note: When the chat re-opens from awaiting response or pending response then the chats remain assigned to the same agent even if the agent has logged out. This is to insure that the consistency between the customer and agent is maintained

Section 5: External Assignment Rule

Definition: The External Assignment Rule allows integration with Customer Relationship Management (CRM) systems to map customers to specific agents or account managers.

Uses: External Assignment Rules are beneficial for brands looking to align their CRM data with chat assignment, ensuring that customers are directed to the most appropriate agents based on CRM information.

Steps to Configure External Assignment Rule:

Step 1: Go to Assignment Rules

- In Agent Assist, go to "Assignment Rules."
Step 2: Add Conditions

- Add conditions based on your CRM data integration needs.
Step 3: Specify Actions

- Select "External Assignment" in the action.
- Enter the API format you've created.
- Execute and verify the response for a dummy value.
Step 4: Optional - Forceful Assignment

- If needed, choose to forcefully assign the chat to the agent, even if the agent is unavailable.
Step 5: Set Fall-Back Team

- Select a fall-back team to assign the chat if the API fails or the agent is unavailable.
Note: To enable this feature, contact console-support@gupshup.io. The API doc can also be requested from support team

Updated 10 months ago

- Assignment Enhancements in Console 7.0
