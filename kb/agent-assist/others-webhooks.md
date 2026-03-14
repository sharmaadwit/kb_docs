source_url: https://console-docs.gupshup.io/docs/webhook







<!-- agent-assist-golden:v11 -->
# Others: Webhooks

**Module**: Agent Assist

## What this feature does
By leveraging the Webhooks feature, a brand can receive notifications for specific actions occurring on Agent Assist. Consider a scenario where a brand intends to send Push Notifications to its app users when they fail to respond. To achieve this, the brand can set up a webhook API within the configuration. By incorporating a reminder event in the webhook settings, the brand will receive reminder notifications through the API. These reminders can then be utilized internally to trigger Push Notifications, prompting customer engagement.

## Exact UI path
Agent Assist → Settings → Others

## Prerequisites
- Access to the relevant Agent Assist module/page.

## Setup path
- Navigate to Settings > Webhooks > Create Webhook.

## Fields to configure
- a Name and description for the webhook

## Steps
1. Open Agent Assist.
2. Navigate to Settings > Webhooks > Create Webhook.
3. Click **Save** to apply changes.
4. Provide a Name and description for the webhook.
5. Choose the authentication method - either Basic Authentication or API key based on your API equirements.

## Validation / where to check
- Run a quick test and confirm the expected behavior in Agent Assist.

## Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy** if available) to apply changes.

## Troubleshooting
- If something does not work as expected, re-check the exact path, required fields, and save step.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

## Cross-module workflow docs
- Identify the upstream Agent Assist setting and the downstream chat/reporting behavior it affects.

## Module disambiguation docs
- Distinguish this page from adjacent Agent Assist settings before troubleshooting elsewhere.

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
