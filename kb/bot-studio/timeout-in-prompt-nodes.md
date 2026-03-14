source_url: https://console-docs.gupshup.io/docs/timeout-in-prompt-nodes

<!-- kb-golden:v12 -->
# Timeout in Prompt Nodes

**Module**: Bot Studio

## Definition
The timeout setting in prompt nodes lets bot designers configure a predefined timeout duration and an associated fallback path. If the user does not provide the required information within the timeout period, the bot follows the fallback path.

## Why To Use It
The source page uses the example of OTP collection where the bot expects input within a limited validity window.

## Steps
1. Select the prompt node that requires configuration.
2. Configure the message and validation as needed to prompt the user for input.
3. Enable the `Timeout` option located at the bottom of the prompt node settings.
4. Provide the desired timeout duration in minutes or hours.
5. Ensure that the fallback connector is configured for timeout or error scenarios.

## Limits
- Minimum duration: `1 second`
- Maximum duration: `60 minutes`

## Runtime Behavior
- Once the journey is deployed, the bot waits for user input on the prompt node until the timeout duration is reached.
- Once the timeout elapses, the bot triggers the configured fallback path.
