source_url: https://console-docs.gupshup.io/docs/privacy-policy

<!-- kb-golden:v11 -->
# Privacy Policy

**Module**: Channels

## Definition
- Use this page when you need to show a **privacy-policy acknowledgement or consent link in the web chat widget**.
- For web widget setup, the privacy-policy experience is typically configured through **Channels -> Pre-Chat Form**, where users can see consent text and a hyperlink before they start messaging.
- If you are asking **“How do I add a privacy policy to the web widget, and where does it appear to the customer?”** -> configure it in **Channels -> Pre-Chat Form** and place the privacy-policy link in the consent text shown before chat starts.

## Procedure
### Exact UI path
Gupshup Console -> Channels -> Pre-Chat Form

### Where to configure it
- Open the **Pre-Chat Form** settings for the web widget.
- Use the consent text and hyperlink fields to point users to your privacy-policy URL.

### Prerequisites
- Access to the **Web channel** settings.
- A privacy-policy URL that should be shown to customers.
- A connected bot/widget already available for testing.

### Fields to configure
- **Checkbox Text**: consent text shown to the user.
- **Hyperlinked Text**: clickable privacy-policy label.
- **URL for Hyperlinked Text**: destination privacy-policy URL.
- **Global Button Text**: button users click to continue after accepting the form.

### Steps
1. Open Gupshup Console.
2. Go to **Channels**.
3. Open **Pre-Chat Form** for the web widget.
4. Enable the pre-chat form if it is not already enabled.
5. Add consent text that mentions your privacy policy.
6. Add the **Hyperlinked Text** that users should click, such as `Privacy Policy`.
7. Enter the **URL for Hyperlinked Text**.
8. Save the widget settings.

### Validation / where to check
- Open the web widget as an end user.
- Confirm the privacy-policy consent text appears before chat starts.
- Confirm the hyperlink opens the expected privacy-policy URL.
- Confirm users can proceed only after completing the expected pre-chat action.

### Troubleshooting
- If the privacy-policy link is not visible, confirm the **Pre-Chat Form** is enabled.
- If users can start chatting without seeing the consent text, re-check the widget configuration and whether the pre-chat form is being bypassed for that user type.
- If the wrong URL opens, verify the **URL for Hyperlinked Text** field in the pre-chat form.

### Save / publish / deploy behavior
- Save the widget configuration after updating privacy-policy text or URL.
- Re-test in the widget after saving to confirm the latest consent experience is visible.

## Options / variants
- New anonymous users can be required to see and submit the pre-chat form before messaging.
- Logged-in users may see the form differently depending on other widget settings such as chat-history retention.

## Cross-module workflow docs
- Channels -> Pre-Chat Form -> widget opens -> user sees privacy-policy text/link -> user starts chat

## Module disambiguation docs
- **Privacy Policy** for the web widget is a **Channels / widget configuration** topic.
- **Bot Studio** controls conversation logic after the user starts chatting; it does not place the privacy-policy link in the widget.
- A generic company legal/privacy page is not the same as the widget configuration step.
