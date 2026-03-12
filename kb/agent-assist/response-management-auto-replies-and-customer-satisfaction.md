source_url: https://console-docs.gupshup.io/docs/response-management-auto-replies-customer-satisfaction

<!-- agent-assist-golden:v2 -->
# Response Management: Auto Replies & Customer Satisfaction

**Module**: Agent Assist

## What this feature does
Auto Replies lets you configure **what message/workflow is triggered** for key chat states (welcome, resolved, offline/after-hours, inactivity reminders). Customer Satisfaction lets you collect feedback after a chat resolves.

**Disambiguation (important for setup and retrieval):**
- **Business Hours** controls **when agents are considered available** (availability windows for teams).
- **Auto Replies** controls **what message or workflow is triggered** in each chat state (during business hours vs after-hours).

## Where to configure it
Agent Assist → Settings → Response Management → Auto Replies

## Prerequisites
- **Business Hours configured** for the relevant teams (otherwise “business hours vs after-hours” behavior may not match expectations).
- **Bot available** if you enable “Handover to Bot” for offline scenarios.

## Setup path
- Agent Assist → Settings → Response Management → Auto Replies

## Steps
1. Open **Agent Assist**.
2. Go to **Settings**.
3. Click **Response Management**.
4. Open **Auto Replies**.
5. Select the scenario (e.g., **Welcome Message**, **When Agents Are Offline**).
6. Configure the message/workflow fields for that scenario.
7. Click **Save** to apply changes.

## Fields you can configure (common)
- **Message content** (text shown to the customer).
- **Scenario selection** (which chat state the message applies to).
- **Business hours vs after-hours behavior** (where applicable).
- **Handover to Bot** (where applicable; requires a bot to be available).

## Behavior by scenario
### Welcome message
**Where**: Auto Replies → Standard Responses → Welcome Message  
**Configure**: welcome message text  
**Save**: click **Save**

### Resolved chat message
**Where**: Auto Replies → Standard Responses → Responses When Chats are Resolved  
**Variants**:
- **Agent resolved**: response sent when an agent resolves the chat
- **System resolved**: response sent when the system resolves the chat  
**Configure**: message text per variant  
**Save**: click **Save**

### Agents offline (business hours vs after-hours)
**Where**: Auto Replies → Responses When Agents Are Offline  
**Variants**:
- **Offline/busy during business hours**: message when agents can’t take chats during configured hours
- **Not available outside business hours**: message for chats received after-hours  
**Configure**: message text per variant  
**Optional**: enable **Handover to Bot** (requires bot availability)  
**Save**: click **Save**

### Customer reminder (customer inactivity)
**Where**: Auto Replies → Customer Reminder  
**Variants**:
- **Reminder + Resolve**: send reminder(s), then resolve after last reminder
- **Resolve**: resolve after a specified inactivity time  
**Configure**: reminder message(s), inactivity time, and resolve behavior  
**Save**: click **Save**

### Agent reminder (agent unresponsiveness)
**Where**: Auto Replies → Agent Reminder  
**Variants**:
- **Reassign the Chat**: reassign to another agent after unresponsiveness
- **Reminder & Resolve**: send reminders, add tag, then auto-resolve after configured time  
**Configure**: thresholds/timers, reassignment vs resolve behavior  
**Save**: click **Save**

## Save/publish behavior
- Click **Save** to apply changes.
- Changes typically apply to **new/incoming chats** (validate on a test conversation after saving).

## Notes
- If you’re seeing answers drift toward Business Hours when asking “what message will the user see?”, anchor your query on **Auto Replies** + the specific scenario (Welcome / Offline / Reminder / Resolved).

## Reference (from source)
Introduction

Definition: Auto Replies encompass a range of features that allow brands to set up automated responses to end customers based on specific conditions. Additionally, Customer Satisfaction tools enable the collection of feedback from customers to assess their level of satisfaction and gather insights for improvement.

Uses: Auto Replies streamline communication by sending automated messages at different points in the chat process. Customer Satisfaction tools gather feedback to enhance services and customer experiences.

Standard Responses

Definition: Standard Responses in Auto Replies include automated messages for specific chat events, including the Welcome Message, Responses when chats are resolved by agents, and Responses when chats are resolved by the system.

Uses: Standard Responses improve user experience and ensure consistent communication during critical chat events.

1: Welcome Message

Definition: The Welcome Message is an automated response sent when a chat is assigned to an agent, initiating the conversation.

Uses: The Welcome Message is used to greet customers and set the tone for the chat.

2: Responses When Chats are Resolved

Definition: Responses When Chats are Resolved are automated messages sent to customers upon the completion of a chat, whether by an agent or the system.

Uses: These responses are used to provide closure to the chat interaction, offer support, or express gratitude to the customer.

2.1: Response Sent to Customers When the Agent Has Resolved the Chat

Definition: This automated message is sent to the customer when an agent resolves the chat.

Uses: This response confirms the resolution of the customer's query or issue.

2.2: Response Sent to Customers When the System Has Resolved the Chat

Definition: This automated message is sent to the customer when the system automatically resolves the chat.

Uses: This message provides closure when the system autonomously concludes the chat.

3: Responses When Agents Are Offline

Definition: Responses When Agents Are Offline are automated messages sent when agents are unavailable or offline. These messages vary based on business hours.

Uses: These messages reassure customers and provide guidance when agents are not available.

3.1: Agents Offline/Busy During Business Hours

Definition: This message is sent when agents are unavailable to take chats during business hours.

Uses: This message provides alternatives or sets expectations for customers.

3.2: Agents Not Available Outside Business Hours

Definition: This message is sent for chats received outside of business hours.

Uses: It informs customers of the situation and guides them accordingly.

3.3: Handover to Bot

Definition: The "Handover to Bot" option is used when agents are offline during either business hours or non-business hours. It facilitates chat transfer to a bot.

Uses: This option ensures continuous service by transferring chats to a bot when agents are unavailable.

Customer Reminder

Definition: Customer Reminder automatically sends messages and resolves chats if customers are inactive for a specific period. It includes Reminder + Resolve and Resolve settings.

Uses: Customer Reminder encourages customer engagement and resolves chats efficiently.

1.1: Reminder + Resolve

Definition: This option sends reminder messages to customers and resolves chats after sending all reminders.

Uses: Reminder messages prompt customer engagement before chat resolution.

1.2: Resolve

Definition: This setting automatically resolves the chat after a specified period.

Uses: Resolve ensures that inactive chats are closed, streamlining chat management.

Agent Reminder

Definition: The Agent Reminder feature sends reminders, reassigns chats, or resolves chats when agents are unresponsive.

Uses: Agent Reminder ensures agent engagement and timely chat resolution.

1.1: Reassign the Chat

Definition: This option reassigns chats to other agents if the assigned agent is unresponsive.

Uses: Reassignment ensures that chats are addressed promptly.

1.2: Reminder & Resolve

Definition: This option sends reminders to agents and customers, adds a tag, and automatically resolves the chat after a configured time.

Uses: Reminder & Resolve enhances agent responsiveness and chat management.

**Last updated (from source)**: Updated 10 months ago
