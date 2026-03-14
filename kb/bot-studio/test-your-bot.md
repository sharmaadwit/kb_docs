source_url: https://console-docs.gupshup.io/docs/test-your-bot

<!-- kb-golden:v12 -->
# Test your Bot

**Module**: Bot Studio

## Definition
Use `Test your Bot` to test and debug your bot while you build it on console.

- The feature is available on the journey listing page in `Bot Studio > Journeys`.
- You can use the widget to send messages and initiate a conversation using the configured trigger inputs on the starting node.
- `Message Log` is available for every user message and renders the payload generated after the user message is sent.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Journeys → Test your Bot

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Journeys**.
4. Open `Test your Bot`.
5. Send messages using the widget.
6. Use the configured trigger inputs on the starting node if required.
7. Open `Message Log` for a user message.
8. Review `Basic Info` and `Payload`.

### Validation / where to check
- Check `Basic Info` to view detailed information about the journeys and nodes executed.
- Check `Payload` to view the backend JSON payload generated after a user message is sent.

### Fields to configure
- Starting Node trigger inputs (if required)
- Message Log sections: `Basic Info` and `Payload`

### Save / publish / deploy behavior
- No save or publish action is described on this page.

### Prerequisites
- Access to `Bot Studio > Journeys`.
- A created journey that can be tested.

## Options / variants
- `Message Log -> Basic Info`
- `Message Log -> Payload`

## Field mapping / schemas
- `Payload` shows the backend JSON payload generated after a user message is sent.

## Cross-module workflow docs
- Bot Studio journey build -> Test your Bot -> debug before go-live

## Module disambiguation docs
- `Test your Bot` is for testing and debugging during build time.
- Analytics or channel go-live pages are separate from this testing widget.

## Reference (from source)
- Journey Builder is equipped with a Test Bot functionality to help you test and debug your bot while you build it on console.
