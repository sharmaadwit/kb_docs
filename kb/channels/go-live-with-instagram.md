source_url: https://console-docs.gupshup.io/docs/go-live-with-instagram

<!-- kb-golden:v12 -->
# Go Live with Instagram

**Module**: Channels

## Definition
Use this page to connect an Instagram account and make Bot Studio journeys active on Instagram DM.

## Steps
1. Log in to Gupshup Conversational Cloud and go to `Instagram` under `Channels`.
2. Ensure that you have all the prerequisites and click `Go Live`.
3. Log in with your Instagram credentials in the new window.
4. Ensure that all permissions are selected and click `Allow`.
5. After the success popup, click `Next` to access settings where Instagram-only features such as `Ice Breakers` and `Persistent Menu` can be enabled.

## Channel Behavior
- Once you go live, all journeys in Bot Studio will be active on Instagram DM.
- By default, autoresponders are enabled once you go live with Instagram.

## Related Instagram Journey Behavior
From the linked Instagram docs:

- For existing or ongoing conversations, the user enters the `Fallback Journey`.
- For new conversations, the user enters the `Welcome Journey`.

The `Default Journeys` page also states:

- `Welcome Journey` is triggered when the user input does not match configured start-node events and the user is not already inside a journey, or the previous session has expired.
- `Fallback Journey` is triggered when a node fails to proceed based on user input or technical failures.

## Multiple Channels
The Instagram autoresponders page states that channel-based differentiation can be handled in `Welcome Journey` and `Fallback Journey` by using the system variable `channel` and adding conditions for values such as:

- `instagram`
- `whatsapp`
- `gipwebchannel`

## Source Notes
- Primary source: `https://console-docs.gupshup.io/docs/go-live-with-instagram`
- Additional sources used for journey behavior:
  - `https://console-docs.gupshup.io/docs/default-journeys`
  - `https://console-docs.gupshup.io/docs/instagram-autoresponders`
