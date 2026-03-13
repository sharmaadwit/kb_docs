source_url: https://console-docs.gupshup.io/docs/web-chat-aesthetics

<!-- kb-golden:v7 -->
# Chat Aesthetics

**Module**: Channels

## Definition
You can customize the look & feel of your Web chat widget via the Chat Aesthetics Settings.

## Procedure
### Exact path
Gupshup Console → Channels → Chat Aesthetics

### Where to configure it
Gupshup Console → Channels → Chat Aesthetics

### Prerequisites
- You can customize the colors of the following elements of your chat widget as per your brand requirements: Header Chat Background Bot Message Bubble User Message Bubble
- You can modify the size (height and width) of your chat widget as per your requirements.
- You can modify the size of your chat widget icon as per your requirements.

### Setup path
- Go to Google Fonts.

### Steps
1. Open Gupshup Console.
2. Go to Google Fonts.
3. Click Get Font in the top right corner. You will be redirected to a new page title "1 font family selected".
4. Click <> Get embed code.
5. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- Bot Name
- Bot Avatar Image
- Bot Logo Image
- Font Style
- Getting the Font URL
- Font Size
- Font Colours
- Widget Size
- Widget Position
- Icon Image

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation
- Channel setup governs connectivity and channel features; bot logic is configured separately in **Bot Studio**.

## Reference (from source)
<!-- procedural:v2 -->
# Chat Aesthetics

**Module**: Channels

## Overview
You can customize the look & feel of your Web chat widget via the Chat Aesthetics Settings.

## When to use
_Add the primary scenarios and personas._

## Setup path
- Go to Google Fonts.

## Step-by-step configuration
You can customize the look & feel of your Web chat widget via the Chat Aesthetics Settings.

## Identity

### Bot Name

- This text will be displayed in the header of the chat widget as the title.
- By default, the Bot Name is configured as "Virtual Assistant".
### Bot Avatar Image

- This image appears as the bot's persona along with each message sent by the bot in the conversation.
- We have provided 5 options from our end. By default, the first option is selected.
- You can upload a custom image for your Bot Avatar using the Upload option. The uploaded image should jpeg, jpg or png and its maximum size can be 1 MB.
### Bot Logo Image

- This image appears as the bot's logo in the header of the chat widget along with the Bot Name.
- By default, the Bot Logo is set to be the same as the Bot Avatar.
- You can uncheck the checkbox to configure a separate Bot Logo.
- We have provided 5 options from our end. You can upload a custom image for your Bot Logo using the Upload option. The uploaded image should jpeg, jpg or png and its maximum size can be 1 MB.
## Colours

- You can customize the colors of the following elements of your chat widget as per your brand requirements: Header Chat Background Bot Message Bubble User Message Bubble
- Header
- Chat Background
- Bot Message Bubble
- User Message Bubble
- We have provided 5 options from our end for each element. By default, the first option is selected.
- You can choose a custom color for any element using our custom color picker. You can choose a color using the eye dropper tool. You can also specify the RGB, HSL or HEX values for your preferred color.
- You can choose a color using the eye dropper tool.
- You can also specify the RGB, HSL or HEX values for your preferred color.
## Font

### Font Style

- You can change the font style of the text in your chat widget.
- We have provided 6 options to choose from - Sans Serif (selected by default) Arial Calibri Poppins Roboto Times New Roman
- Sans Serif (selected by default)
- Arial
- Calibri
- Poppins
- Roboto
- Times New Roman
- You can also choose to set a custom font style as per your brand requirements by selecting Custom in the dropdown. You need to provide the Font Family name and a public Font URL to set your custom font style. If the Font Family name does not match or the Font URL is inaccessible, the font style will fall back to "Sans Serif".
- You need to provide the Font Family name and a public Font URL to set your custom font style.
- If the Font Family name does not match or the Font URL is inaccessible, the font style will fall back to "Sans Serif".
#### Getting the Font URL

If you are hosting the font, please ensure that the URL is publicly accessible. If the font is available on Google Fonts, please follow the steps below to get the URL.

- Go to Google Fonts.
- Search for your preferred font and click on it.
- Click Get Font in the top right corner. You will be redirected to a new page title "1 font family selected".
- Click <> Get embed code.
- In the embed code for Web, the Font URL is present after the link href parameter. For example, the Web embed code for the font family Comic Neue is as shown below and the font URL is https://fonts.googleapis.com/css2?family=Comic+Neue:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&display=swap
- For example, the Web embed code for the font family Comic Neue is as shown below and the font URL is https://fonts.googleapis.com/css2?family=Comic+Neue:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&display=swap
```
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Comic+Neue:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&display=swap" rel="stylesheet">
```

### Font Size

- You can change the font size of the text in your chat widget.
- We have provided 4 options to choose from - 12 px, 14 px, 16 px and 18 px. By default, 12 px is set as the font size for bot and user messages.
- By default, 12 px is set as the font size for bot and user messages.
### Font Colours

- By default, the Font Colour is set as black (#000000) or white (#FFFFFF) based on the luminosity of its background. The above logic is followed for the font colours of Bot Messages, User Messages and Bot Name. If the header colour is on the lighter side (for example, yellow), font colour of the Bot Name is set as black whereas if the header colour is on the darker side (for example, blue), the font colour is set as white.
- The above logic is followed for the font colours of Bot Messages, User Messages and Bot Name.
- If the header colour is on the lighter side (for example, yellow), font colour of the Bot Name is set as black whereas if the header colour is on the darker side (for example, blue), the font colour is set as white.
- You can choose a custom font colour for Bot Messages, User Messages and Bot Name using a colour picker. Please note that the font colour you choose here will override the font colour logic mentioned above.
- Please note that the font colour you choose here will override the font colour logic mentioned above.
## Chat Widget

### Widget Size

- You can modify the size (height and width) of your chat widget as per your requirements.
- We have provided 3 options to choose from - Small (Width = 320 px, Height = 45% of screen height) Medium (Width = 360 px, Height = 60% of screen height) Large (Width = 420 px, Height = 85% of screen height) Full Screen (Width = 100% of screen width, Height = 100% of screen height)
- Small (Width = 320 px, Height = 45% of screen height)
- Medium (Width = 360 px, Height = 60% of screen height)
- Large (Width = 420 px, Height = 85% of screen height)
- Full Screen (Width = 100% of screen width, Height = 100% of screen height)
### Widget Position

- By default, the chat widget icon is positioned in the bottom right corner of the screen and the chat widget is aligned to the bottom and right side of the screen.
- You can change this positioning of the icon and alignment of the widget from Right to Left.
## Chat Widget Icon

### Icon Image

- The visual representation of your chat widget when it is in a closed state.
- We have provided 4 options with transparent backgrounds from our end. By default, the first option is selected.
- You can upload a custom image for your Bot Avatar using the Upload option. The uploaded image should jpeg, jpg or png and its maximum size can be 1 MB.
### Icon Size

- You can modify the size of your chat widget icon as per your requirements.
- We have provided 3 options to choose from - Small (Diameter = 45 px) Medium (Diameter = 70 px) Large (Diameter = 90 px)
- Small (Diameter = 45 px)
- Medium (Diameter = 70 px)
- Large (Diameter = 90 px)
Updated 9 months ago

- Greeting Message

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
