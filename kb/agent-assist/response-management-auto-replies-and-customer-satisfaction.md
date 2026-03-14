source_url: https://console-docs.gupshup.io/docs/response-management-auto-replies-customer-satisfaction

<!-- agent-assist-golden:v12 -->
# Response Management: Auto Replies & Customer Satisfaction

**Module**: Agent Assist

## Definition
Auto Replies allow brands to set up automated responses to end customers based on specific conditions. Customer Satisfaction tools collect feedback from customers to assess satisfaction and gather insights for improvement.

## Standard Responses
Standard Responses include automated messages for specific chat events:

- `Welcome Message`
- `Responses when chats are resolved by agents`
- `Responses when chats are resolved by the system`

### Welcome Message
- Sent when a chat is assigned to an agent.
- Used to greet customers and set the tone for the chat.

### Responses When Chats Are Resolved
- Sent when a chat is completed by an agent or by the system.

#### Response Sent to Customers When the Agent Has Resolved the Chat
- Sent when an agent resolves the chat.
- Confirms the resolution of the customer's query or issue.

#### Response Sent to Customers When the System Has Resolved the Chat
- Sent when the system automatically resolves the chat.
- Provides closure when the system autonomously concludes the chat.

### Responses When Agents Are Offline
- Sent when agents are unavailable or offline.
- These messages vary based on business hours.

#### Agents Offline/Busy During Business Hours
- Sent when agents are unavailable to take chats during business hours.

#### Agents Not Available Outside Business Hours
- Sent for chats received outside of business hours.

#### Handover to Bot
- Used when agents are offline during either business hours or non-business hours.
- Facilitates chat transfer to a bot.

## Customer Reminder
Customer Reminder automatically sends messages and resolves chats if customers are inactive for a specific period.

### Reminder + Resolve
- Sends reminder messages to customers.
- Resolves chats after sending all reminders.

### Resolve
- Automatically resolves the chat after a specified period.

## Agent Reminder
Agent Reminder sends reminders, reassigns chats, or resolves chats when agents are unresponsive.

### Reassign the Chat
- Reassigns chats to other agents if the assigned agent is unresponsive.

### Reminder & Resolve
- Sends reminders to agents and customers.
- Adds a tag.
- Automatically resolves the chat after a configured time.

## Business Hours Relation
- The source page states that offline responses vary based on business hours.
- For business-hours configuration itself, use `kb/agent-assist/user-management-business-hours.md`.

## Source Notes
- The source page documents the response types and their uses.
- The source page does not provide click-by-click navigation steps.
