source_url: https://console-docs.gupshup.io/docs/timeout-in-prompt-nodes

<!-- kb-golden:v1 -->
# Timeout in Prompt Nodes

**Module**: Bot Studio

## Definition
The Prompt node is extensively utilized in Journey Builder for fetching responses or gathering user data, which is subsequently stored for future use within the bot. Typically, this information is utilized during the user conversation within the bot. However, in certain scenarios, timely access to this information is crucial for achieving specific use cases.

## Procedure
### Where to configure it
Gupshup Console → Bot Studio → Timeout in Prompt Nodes

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Timeout in Prompt Nodes**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- Overview:
- What's New!
- How to configure timeout in prompt node

## Notes
- _Add prerequisites, constraints, and rollout behavior._

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
