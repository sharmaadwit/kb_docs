source_url: https://console.gupshup.io/rcs/templates

<!-- kb-golden:v10 -->
# RCS Templates in Gupshup Console

**Module**: Channels

## Definition

How to create, manage, and use RCS templates from the Gupshup Console. Templates are required for all outbound messages sent outside an active 24-hour conversation window. Console supports text, standalone rich card, and rich card carousel templates.

---

## Where to find it

**Console > Templates** — When a project has both WhatsApp and RCS, Console first asks which account to open. A project has only one RCS account. From this menu you can create, update, delete, clone, and test RCS templates.

---

## Template Types

| Type | Contents | Variable support |
|------|----------|-----------------|
| Text | Message text plus suggestion chips | In text, suggestion text, and postback data |
| Rich card (standalone) | Media (image, video, or PDF), orientation, height, card title, card description, suggestions | In title and description; in media URL when using a variable image/PDF/video URL |
| Rich card carousel | Up to 10 rich cards, each with its own suggestions | Same as standalone rich card, per card |

Variables can be sourced from a column in the upload file, a Customer360 (C360) property, or a fallback value.

---

## Suggestion (Button) Types

| Suggestion type | Extra fields | Notes |
|-----------------|-------------|-------|
| Reply | Suggestion text, postback | Both can use variables |
| URL action | URL | URL can use variables |
| Dialer action | Phone number | Number is static |
| View location (lat/long) | Latitude, longitude, label | |
| View location (query) | Search query | |
| Share location | — | Prompts the user to share their location |
| Create calendar event | Date and time, title, description | |

Every suggestion has a suggestion text (max 25 characters) and a postback data field.

---

## Content Limits and Media Specs

| Element | Limit |
|---------|-------|
| Suggestion text (action or reply) | 25 characters |
| Suggestions per rich card | 4 |
| Suggestion chip list | 11 chips |
| Carousel | 2 to 10 cards |
| Message or rich card payload | 250 KB |
| Dial action number format | Leading +, country code and area code, no separators (e.g. +14155555555) |
| Standalone card image, vertical, short height | 3:1 ratio, 1440 × 480 px, max 2 MB |
| Standalone card image, vertical, medium height | 2:1 ratio, 1440 × 720 px, max 2 MB |
| Standalone card image, horizontal | 3:4 ratio, 768 × 1024 px, max 2 MB |
| Standalone card video | Max 10 MB |
| Carousel image | 4:3 ratio, 960 × 720 px, max 1 MB |
| Carousel video | Max 5 MB |
| Image formats | JPEG, JPG, PNG, GIF |

---

## Design Tips

- Personalise with the customer's name instead of a generic greeting.
- Include a STOP opt-out option so users can unsubscribe easily.
- In carousels, use at most 2 suggestions per card and keep descriptions under 50 characters. Longer text can hide suggestions on some devices.
- Keep logos and text away from image edges — some devices crop them.

---

## iOS Templates (India only)

For iOS delivery via the Jio iOS agent in India, follow the iOS creative limits shown in the **Add Template** section of the Console UI. These differ from standard Android limits.

---

## Related docs

- rcs-console-agent-setup.md for launching the agent before creating templates
- rcs-console-campaigns.md for using approved templates in broadcast campaigns
- rcs-templates.md for the RCS Template API reference (developer use)
