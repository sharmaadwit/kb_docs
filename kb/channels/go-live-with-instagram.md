source_url: https://console-docs.gupshup.io/docs/go-live-with-instagram

<!-- kb-golden:v11 -->
# Go Live with Instagram

**Module**: Channels

## Definition
- Use this page to connect Instagram to Gupshup and make the live bot available on Instagram DM.
- After Instagram is live, your active **Bot Studio** journeys can respond on Instagram.
- If you are asking **“Instagram is connected but incoming messages are not reaching the intended journey”** or **“WhatsApp works but Instagram does not”**, start with this page and then isolate channel connection, journey mapping, and live deployment.

## Procedure
### Exact UI path
Gupshup Console -> Channels -> Go Live with Instagram

### Prerequisites
- Access to the Instagram channel setup in Gupshup Console.
- Valid Instagram credentials and permissions required for connection.
- A Bot Studio journey already ready for live traffic.

### Steps
1. Open Gupshup Console.
2. Go to **Channels**.
3. Open **Go Live with Instagram**.
4. Click **Go Live**.
5. Log in with the Instagram account when prompted.
6. Allow the required permissions.
7. Complete the connection flow and return to Gupshup.
8. Open the channel settings and confirm Instagram-only features if needed.
9. Re-test the live Instagram DM experience.

### Validation / where to check
- Send a test DM from Instagram and confirm the bot responds.
- Confirm the message enters the intended live Bot Studio journey.
- If the same bot should work on WhatsApp and Instagram, verify both channels reach the expected live path after deployment.

### Troubleshooting
- If Instagram is connected but the wrong journey starts, verify the live Bot Studio journey and any channel-specific routing or mapping rules.
- If WhatsApp works but Instagram does not, isolate the issue in this order: **channel connection -> channel mapping/config -> Bot Studio live journey**.
- If Instagram still shows old behavior, confirm the bot changes were **Save & Deploy**'d after the channel was connected.
- If the connection flow succeeds but no messages arrive, re-check permissions and whether the correct Instagram account was connected.

### Save / publish / deploy behavior
- Connecting Instagram makes the channel live.
- If the conversation logic changes later, use **Save & Deploy** in **Bot Studio** so Instagram receives the latest live journey behavior.

## Options / variants
- Instagram-only features can be enabled after the channel goes live.
- Shared bot logic can be used across WhatsApp and Instagram, but channel connection and mapping still need to be correct.

## Cross-module workflow docs
- Channels -> Instagram connection -> Bot Studio live journey -> Instagram DM response
- WhatsApp channel live -> Instagram channel live -> verify shared journey behavior on both channels

## Module disambiguation docs
- **Channels** controls the Instagram connection and channel availability.
- **Bot Studio** controls the live journey behavior after the Instagram message enters the bot.
- A channel connection problem is different from a journey logic problem.
