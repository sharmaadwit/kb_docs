source_url: https://console-docs.gupshup.io/docs/timeout-in-prompt-nodes

<!-- kb-golden:v9 -->
# Timeout in Prompt Nodes

**Module**: Bot Studio

## Definition
The Prompt node is extensively utilized in Journey Builder for fetching responses or gathering user data, which is subsequently stored for future use within the bot. Typically, this information is utilized during the user conversation within the bot. However, in certain scenarios, timely access to this information is crucial for achieving specific use cases.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Journey Builder → Prompt Node → Timeout

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Journey Builder**.
4. Go to **Prompt Node**.
5. Go to **Timeout**.
6. Select the prompt node that requires configuration.
7. Configure the message and validation as needed to prompt the user for input.
8. Enable the Timeout option located at the bottom of the prompt node settings.
9. Provide the desired timeout duration in minutes or hours.
10. Note that the minimum duration is 1 second, and the maximum duration is 60 minutes.
11. Ensure that the fallback connector is properly configured with the desired action for any error or timeout scenarios.
12. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Send a test message that reaches the prompt node and reply within the timeout window.
- Confirm the journey continues on the expected success path instead of the fallback path.
- Test again with no reply and confirm the fallback connector fires only after the configured timeout duration.

### Fields to configure
- Message content
- Validation rules
- Timeout duration
- Fallback connector path

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- Ensure that the fallback connector is properly configured with the desired action for any error or timeout scenarios.
- If the prompt node times out even when the user replies, check:
- **Variables / capture setup**: confirm the prompt is configured to capture the expected input and validation rules are not rejecting the reply.
- **Node wiring**: confirm the success connector from the prompt node leads to the next intended node and the fallback connector is reserved for timeout/error handling.
- **Deployment state**: if you changed timeout or prompt logic, use **Save & Deploy** so the live channel gets the latest journey version.
- **Validation logic**: if regex or prompt validation fails, the reply may not count as a valid answer even though the user responded.
- **Timeout value**: confirm the timeout is long enough for the use case and within the supported range (1 second to 60 minutes).

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **Journey Builder**.
- Go to **Prompt Node**.
- Go to **Timeout**.

## Options / variants
- Select the prompt node that requires configuration.
- Enable the Timeout option located at the bottom of the prompt node settings.

## Notes
- If you fix timeout behavior in the builder but the live bot still times out, the most common cause is that the updated journey was **saved but not deployed**.

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Timeout in Prompt Nodes

**Module**: Bot Studio

## Overview
The Prompt node is extensively utilized in Journey Builder for fetching responses or gathering user data, which is subsequently stored for future use within the bot. Typically, this information is utilized during the user conversation within the bot. However, in certain scenarios, timely access to this information is crucial for achieving specific use cases.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### Overview:

The Prompt node is extensively utilized in Journey Builder for fetching responses or gathering user data, which is subsequently stored for future use within the bot. Typically, this information is utilized during the user conversation within the bot. However, in certain scenarios, timely access to this information is crucial for achieving specific use cases.

For instance, consider a scenario where the bot sends an OTP to the user with a validity of 5 minutes. In such cases, the bot anticipates the user to input the OTP within the stipulated time frame; otherwise, the information becomes invalid for the bot to process at a later stage. Such use cases necessitate proactive actions based on timeouts by the bot when the user fails to provide the required information within the specified time frame.

### What's New!

The timeout setting in prompt nodes enables bot designers to configure them with a predefined timeout duration and an associated fallback path. This ensures that if the user fails to provide the required information within the specified timeout period, the bot will proactively follow the fallback path.

### How to configure timeout in prompt node

To configure the prompt node with a timeout and fallback path as described, follow these steps:

- Select the prompt node that requires configuration.
- Configure the message and validation as needed to prompt the user for input.
- Enable the Timeout option located at the bottom of the prompt node settings.
- Provide the desired timeout duration in minutes or hours.
- Note that the minimum duration is 1 second, and the maximum duration is 60 minutes.
- Ensure that the fallback connector is properly configured with the desired action for any error or timeout scenarios.
- Once the journey is deployed, the bot will wait for user input on the prompt node until the timeout duration is reached.
- Once the timeout elapses, the bot will trigger the fallback path as configured.
By following these steps, you can effectively set up the prompt node with timeout and fallback path in your bot's journey

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
