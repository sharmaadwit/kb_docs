source_url: https://console-docs.gupshup.io/docs/timeout-in-prompt-nodes
# BOT STUDIO

## Timeout in Prompt Nodes

# Timeout in Prompt Nodes

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

Updated 10 months ago
