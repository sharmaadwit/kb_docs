source_url: https://console-docs.gupshup.io/docs/webhook




<!-- agent-assist-golden:v8 -->
# Others: Webhooks

**Module**: Agent Assist

## What this feature does
By leveraging the Webhooks feature, a brand can receive notifications for specific actions occurring on Agent Assist. Consider a scenario where a brand intends to send Push Notifications to its app users when they fail to respond. To achieve this, the brand can set up a webhook API within the configuration. By incorporating a reminder event in the webhook settings, the brand will receive reminder notifications through the API. These reminders can then be utilized internally to trigger Push Notifications, prompting customer engagement.

## Where to configure it
Agent Assist → Settings → Others

## Exact path
Agent Assist → Settings → Others

## Prerequisites
- _List required roles/access, teams, and any upstream configuration._

## Setup path
- Navigate to Settings > Webhooks > Create Webhook.

## Steps
1. Open Agent Assist.
2. Navigate to Settings > Webhooks > Create Webhook.
3. Click **Save** to apply changes.
4. Navigate to Settings > Webhooks > Create Webhook.
5. Provide a Name and description for the webhook.
6. Choose the authentication method - either Basic Authentication or API key based on your API equirements.

## Save/publish behavior
- Click **Save** (or **Save & Deploy** if available) to apply changes.

## Validation
- _Run a quick test (new chat / assignment / workflow) and confirm expected behavior._

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- _Link this feature to adjacent modules (e.g., Business Hours ↔ Auto Replies; Assignment Rules ↔ Teams ↔ Views)._

## Module disambiguation
- _Add 1–2 bullets distinguishing this feature from adjacent settings to reduce retrieval drift._

## Reference (from source)
### Overview
By leveraging the Webhooks feature, a brand can receive notifications for specific actions occurring on Agent Assist. Consider a scenario where a brand intends to send Push Notifications to its app users when they fail to respond. To achieve this, the brand can set up a webhook API within the configuration. By incorporating a reminder event in the webhook settings, the brand will receive reminder notifications through the API. These reminders can then be utilized internally to trigger Push Notifications, prompting customer engagement.

### When to use
_Add the primary scenarios and personas._

### Details
By leveraging the Webhooks feature, a brand can receive notifications for specific actions occurring on Agent Assist. Consider a scenario where a brand intends to send Push Notifications to its app users when they fail to respond. To achieve this, the brand can set up a webhook API within the configuration. By incorporating a reminder event in the webhook settings, the brand will receive reminder notifications through the API. These reminders can then be utilized internally to trigger Push Notifications, prompting customer engagement.

Configuration

To set up this configuration, follow the steps outlined below:

- Navigate to Settings > Webhooks > Create Webhook.
Navigate to Settings > Webhooks > Create Webhook.

- Provide a Name and description for the webhook.
Provide a Name and description for the webhook.

- Specify the endpoint URL where Agent Assist will trigger the event. Format can be found here: Webhook format
Specify the endpoint URL where Agent Assist will trigger the event. Format can be found here: Webhook format

- Choose the authentication method - either Basic Authentication or API key based on your API equirements.
Choose the authentication method - either Basic Authentication or API key based on your API equirements.

- Validate the configuration by clicking on "Test Webhook," ensuring the accuracy of the configured API and viewing a sample response sent as a payload in the API.
Validate the configuration by clicking on "Test Webhook," ensuring the accuracy of the configured API and viewing a sample response sent as a payload in the API.

- Lastly, select either Reminder or Assignment as the event type based on your specific use case.
Lastly, select either Reminder or Assignment as the event type based on your specific use case.

Events

- Reminder Event: Reminder event is triggered every time a customer reminder is sent to the user. For this event to work you have to configure the customer reminders in auto replies. For every reminder message configured, you will receive a different event. Please note that, Customer Reminder has Reminder and Resolve settings and for the event both reminder and resolve are considered
Reminder Event: Reminder event is triggered every time a customer reminder is sent to the user. For this event to work you have to configure the customer reminders in auto replies. For every reminder message configured, you will receive a different event. Please note that, Customer Reminder has Reminder and Resolve settings and for the event both reminder and resolve are considered

- Assignment Event: This event refers to the event which is triggered every time assignment happens in the system
Assignment Event: This event refers to the event which is triggered every time assignment happens in the system
