source_url: https://api.dotgo.com/rcs/templates

<!-- kb-golden:v10 -->
# RCS Message Templates

**Module**: Channels

## Definition

RCS Message Templates are pre-designed, pre-approved message formats that brands use to send consistent, compliant messaging to users. Templates support multiple formats: plain text, text with PDF, rich cards (standalone and carousel), with optional suggested actions and media attachments.

All templates must be submitted for approval before use. Once approved, templates can be sent via the messaging API with custom variables to personalize content per user.

## Template Types

### 1. Text Message Template
Simple text message with optional suggested replies or actions.

**Capabilities**:
- Up to 2500 characters (including variables)
- Up to 11 suggested replies/actions per message
- Optional fallback SMS for unsupported devices
- Custom variables for personalization (e.g., [name], [offers])

**Use cases**: Transactional alerts, order confirmations, appointment reminders

### 2. Text Message with PDF
Text message with an attached PDF document for approval.

**Capabilities**:
- Text content (up to 2500 chars)
- PDF attachment (<100MB)
- Suggested actions
- Message positioning (text at top or PDF at top)
- Optional fallback SMS

**Use cases**: Invoices, receipts, policy documents, contracts

### 3. Rich Card Standalone
Single rich card with image/GIF/video and up to 4 suggested actions.

**Capabilities**:
- Media (image, GIF, video)
- Card title (200 chars)
- Card description (2000 chars)
- Orientation: VERTICAL or HORIZONTAL
- Alignment: LEFT, RIGHT (for HORIZONTAL only)
- Height: SHORT_HEIGHT, MEDIUM_HEIGHT (for VERTICAL only)
- Up to 4 suggested actions

**Use cases**: Product showcases, promotional offers, image-based notifications

### 4. Rich Card Carousel
Multiple rich cards in a carousel (2-10 cards) with shared suggested actions.

**Capabilities**:
- 2-10 rich cards in sequence
- Each card can have image/GIF/video
- Up to 4 suggested actions per card
- Swipeable interface on RCS-capable devices
- Fallback to single card on limited devices

**Use cases**: Product catalogs, hotel availability, flight options, service menus

## API Endpoints

**Server Root**: `https://developer.dotgo.com/`

### Submit a Template

#### Text Message Template

**Endpoint**: `POST https://developer.dotgo.com/directory/secure/api/v1/bots/{botId}/templates`

**Request Parameters**:

| Field Name | Validation | Description | Remarks |
|-----------|-----------|-----------|---------|
| name* | Max 20, alphanumeric + underscore | Template name | "wtcfinaleng" |
| type* | Predefined: [text_message] | Template type | "text_message" |
| templateUseCase | One of: Transactional, Promotional, OTP | Category if agent type is Multi-Use | "Transactional" |
| textMessageContent* | Max 2500 chars (with variables) | Message body with custom variables in [brackets] | "Hi [Name], Time to go big or go home because it's India VS Australia FINALS!" |
| fallbackText | Max 160 chars (with variables) | SMS fallback for non-RCS devices | "Hi [name], your premium of [amount] is due on [date]. Please have sufficient funds in your account." |
| suggestionType | Predefined options | Type of suggestion (reply, url_action, dialer_action) | "reply" |
| displayText | Max 25 chars (with variables) | Suggestion display text | "Click to Win" |
| postback | Max 120 chars (with variables) | Postback data sent when clicked | "click_to_win" |
| phoneNumber | Valid phone | Phone number for dialer action | "+919876543212" |
| url | Valid URL | URL for URL action | "https://brandx.onelink.me/" |

**Response Parameters**:

| Field Name | Type | Description |
|-----------|------|-----------|
| name | String | Template name |
| type | String | Template type |
| textMessageContent | String | Stored message content |
| fallbackText | String | Stored fallback SMS |
| suggestionId | String | Unique ID for each suggestion |
| suggestionType | String | Stored suggestion type |
| displayText | String | Stored display text |
| postback | String | Stored postback |

**Request Sample (Without variables)**:

```json
{
  "rich_template_data": {
    "name": "wtcfinaleng",
    "type": "text_message",
    "textMessageContent": "Time to go big or go home because it's India VS Australia FINALS!",
    "fallbackText": "Hi, your premium of 785 is due. Please have sufficient funds in your account.",
    "templateUseCase": "Transactional",
    "suggestions": [
      {
        "suggestionType": "reply",
        "displayText": "Click to Win",
        "postback": "click_to_win"
      },
      {
        "suggestionType": "url_action",
        "url": "https://brandx.onelink.me/",
        "displayText": "Answer and Win",
        "postback": "answer_and_win"
      },
      {
        "suggestionType": "dialer_action",
        "phoneNumber": "+919876543212",
        "displayText": "Call Now",
        "postback": "call_now"
      }
    ]
  }
}
```

**Request Sample (With variables)**:

```json
{
  "rich_template_data": {
    "name": "wtcfinaleng",
    "type": "text_message",
    "textMessageContent": "Hi [Name], Time to go big or go home because it's India VS Australia FINALS!",
    "fallbackText": "Hi [name], your premium of [amount] is due on [date]. Please have sufficient funds in your account.",
    "templateUseCase": "Transactional",
    "suggestions": [
      {
        "suggestionType": "reply",
        "displayText": "Click to Win [Offers]",
        "postback": "click_to_win"
      },
      {
        "suggestionType": "url_action",
        "url": "https://brandx.onelink.me/",
        "displayText": "Answer and Win",
        "postback": "answer_and_win"
      },
      {
        "suggestionType": "dialer_action",
        "phoneNumber": "+919876543212",
        "displayText": "Call Now [Offers]",
        "postback": "call_now"
      }
    ]
  }
}
```

#### Text Message with PDF

**Endpoint**: `POST https://developer.dotgo.com/directory/secure/api/v1/bots/{botId}/templates`

**Special Requirements**:
- PDF file size <100MB
- Upload media as multipart file with key `multimedia_files`
- `documentFileName` must match uploaded filename

**Request Parameters** (extends text message):

| Field Name | Validation | Description |
|-----------|-----------|-----------|
| multimedia_files | PDF <100MB | PDF document to attach |
| documentFileName | Filename | Name of uploaded PDF |
| messageOrder | text_message_at_top or pdf_at_top | Content order |

**Request Sample**:

```json
{
  "rich_template_data": {
    "name": "wtcfinaleng",
    "type": "text_message_with_pdf",
    "textMessageContent": "Time to go big or go home because it's India VS Australia FINALS!",
    "documentFileName": "sample (4).pdf",
    "messageOrder": "text_message_at_top",
    "suggestions": [
      {
        "suggestionType": "reply",
        "displayText": "Click to Win",
        "postback": "click_to_win"
      }
    ]
  }
}
```

#### Rich Card Standalone

**Endpoint**: `POST https://developer.dotgo.com/directory/secure/api/v1/bots/{botId}/templates`

**Request Parameters**:

| Field Name | Validation | Description | Remarks |
|-----------|-----------|-----------|---------|
| multimedia_files | Image/GIF/Video | Media file (image, GIF, video) | (Media file uploaded name and 'fileName'/'thumbnailFileName' must be same) |
| name* | Max 20 chars | Template name | "wtcfinaleng" |
| type* | rich_card | Template type | "rich_card" |
| templateUseCase | Transactional, Promotional, OTP | If agent type is Multi-Use | "Transactional" |
| fallbackText | Max 160 chars | SMS fallback | "Hi [name], your premium of [amount] is due on [date]." |
| orientation* | VERTICAL, HORIZONTAL | Card layout | "VERTICAL" |
| alignment* (HORIZONTAL only) | LEFT, RIGHT | Alignment for HORIZONTAL | "LEFT" |
| height* (VERTICAL only) | SHORT_HEIGHT, MEDIUM_HEIGHT | Card height | "SHORT_HEIGHT" |
| cardTitle* | Max 200 chars | Card title | Card title text |
| cardDescription* | Max 2000 chars | Card description | Card description text |
| mediaUrl | Valid publicly accessible URL | Media URL | "https://brandx.onelink.me/temp.mp4" |
| thumbnailUrl | Valid URL | Thumbnail URL | "https://brandx.onelink.me/temp.jpeg" |
| fileName | Media filename | Media file uploaded name | Media file uploaded name |
| thumbnailFileName | Thumbnail filename | If video, thumbnail filename required | Thumbnail file name |
| suggestionType | Predefined options | Suggestion type | "reply" |
| displayText | Max 25 chars | Display text | "View Details" |
| postback | Max 120 chars | Postback data | "view_details" |

**Request Sample (Without variables)**:

```json
{
  "rich_template_data": {
    "multimedia_files": (Media file uploaded name and "fileName"/"thumbnailFileName" must be same),
    "name": "wtcfinaleng",
    "type": "rich_card",
    "fallbackText": "Hi, your premium of 785 is due. Please have sufficient funds in your account.",
    "orientation": "VERTICAL",
    "height": "SHORT_HEIGHT",
    "cardTitle": "This is a single rich card",
    "cardDescription": "This is the description of the rich card. It's the first field that will be truncated if it exceeds the maximum width or height of a card.",
    "mediaUrl": "https://brandx.onelink.me/temp.mp4",
    "thumbnailUrl": "https://brandx.onelink.me/temp.jpeg",
    "fileName": "Media File",
    "thumbnailFileName": "If the file type is video then need to give thumbnailFileName",
    "suggestions": [
      {
        "suggestionType": "reply",
        "displayText": "View Details",
        "postback": "view_details"
      }
    ]
  }
}
```

#### Rich Card Carousel

**Endpoint**: `POST https://developer.dotgo.com/directory/secure/api/v1/bots/{botId}/templates`

**Carousel Requirements**:
- Minimum 2 cards, maximum 10 cards
- Each card has independent media, title, description
- Suggested actions can vary per card

**Request Sample**:

Similar to Rich Card Standalone, but with multiple card objects in array format.

### Update a Template

**Endpoint**: `PUT https://developer.dotgo.com/directory/secure/api/v1/bots/{botId}/templates`

Same parameters as POST (create). Use PUT to modify existing templates.

### Delete Template

**Endpoint**: `DELETE https://developer.dotgo.com/directory/secure/api/v1/bots/{botId}/templates/{templateId}`

Delete a template by ID.

### Get Template Details

**Endpoint**: `GET https://developer.dotgo.com/directory/secure/api/v1/bots/{botId}/templates/{templateId}`

Retrieve full template details including approval status.

### Fetch Template List

**Endpoint**: `GET https://developer.dotgo.com/directory/secure/api/v1/bots/{botId}/templates`

List all templates for a bot.

### Get Template Status

**Endpoint**: `GET https://developer.dotgo.com/directory/secure/api/v1/bots/{botId}/templates/{templateId}/status`

Check approval status (pending, approved, rejected).

## Custom Variables

Templates support personalization via custom variables in square brackets. Variables must contain only alphanumeric characters and underscores.

**Example**: `"Hello [user_name], your balance is [amount]"`

When sending, substitute actual values: `user_name=Alice, amount=$100`

## HTTP Response Codes

| Code | Description |
|------|-------------|
| 202 | Template accepted for review |
| 400 | Bad request (validation error) |
| 403 | Forbidden (template with name already exists) |
| 500 | Internal server error |

### Common Validation Errors

| Error | Fix |
|-------|-----|
| "Template with name wtygqff45g is already present" | Use a unique template name |
| "Please provide a valid bot id" | Verify bot ID from agent creation |
| "Template type is predefined" | Use valid type: text_message, text_message_with_pdf, rich_card |
| Template not approved | Wait for Dotgo approval or contact support |

## Media Requirements

### Image Files
- **Formats**: JPG, JPEG, PNG, GIF
- **Max size**: 100MB (per file)
- **Recommended**: <5MB for optimal delivery

### Video Files
- **Formats**: H263, MP4, MPEG-4, WebM
- **Max size**: 100MB
- **Thumbnail**: Required (JPG/PNG, <5MB)

### PDF Files
- **Format**: PDF only
- **Max size**: 100MB
- **Text with PDF templates only**

## Field/Payload Examples

See request samples above for complete JSON structures.

## Cross-module workflow docs

- Create templates in Channels > RCS Templates
- Reference template IDs when sending messages via GSMA or Google APIs
- Track template approval status before sending
- Use custom variables to personalize content per user

## Options / variants

- **Template types**: Choose based on content (text, PDF, rich card, carousel)
- **Suggested actions**: Multiple suggestion types (reply, URL action, dialer, calendar, map)
- **Fallback SMS**: Always provide for UX on non-RCS devices
- **Approval tiers**: Different approval workflows for transactional vs. promotional

## Reference (from source)

<!-- procedural:v2 -->
# RCS Message Templates

Design, submit, and manage message templates for RCS campaigns. Templates must be approved before use.
