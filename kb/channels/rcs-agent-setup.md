source_url: https://api.dotgo.com/rcs/agent-onboarding

<!-- kb-golden:v10 -->
# RCS Agent Setup & Onboarding

**Module**: Channels

## Definition

RCS Agent setup is the process of registering and configuring a bot/agent for RCS messaging through Gupshup's Dotgo RBM platform. This includes creating the agent, submitting verification documents, registering credentials, and configuring webhooks for message delivery.

## Procedure

### Exact UI path
Gupshup Console → Channels → RCS → Agent Setup

### Prerequisites
- Business registration documents (business license, incorporation certificate)
- Brand details (name, logo, description, color)
- Contact information (phone, email, website)
- Webhook URL (for receiving message events and callbacks)
- Knowledge of GSMA or Google RBM API standards

### Steps to Register an RCS Agent

#### Step 1: Submit Agent Details to Dotgo
Submit the following information via the RBM Hub portal or Gupshup Console:

**Agent Metadata**:
- Agent name (40 chars max, alphanumeric)
- Agent summary (100 chars max)
- Privacy policy URL
- Terms & conditions URL
- Business platform type (GSMA API or Google API)
- Supported languages (e.g., English, Kannada)
- Agent message type (Transactional, Promotional, OTP, Multi-Use)
- Bot logo image (224x224px, <90KB, JPG/PNG)
- Bot banner image (1440x448px, <360KB, JPG/PNG)
- Agent color (RGB hex code, e.g., #dc2e2e)
- Bot description
- Brand name
- Carrier details (MCCMNCs for target carriers)
- Region (India / Rest of World)
- Whether carrier list is editable post-creation

#### Step 2: Agent Creation & Verification
Once details are submitted:
1. Dotgo creates the agent on the RBM Hub backend
2. Agent is assigned a unique **bot_id** (e.g., T3kTSv-wuFtWke8QOR56pg==)
3. Dotgo verifies agent credentials and documents
4. Agent verification status is updated (pending → verified)

#### Step 3: Credential Registration
After agent verification:
1. Dotgo generates **client ID** and **client secret**
2. Credentials are shared via email (subject: "Client Registration is Successful")
3. Register agent with RCS APIs platform:
   - Client ID and secret are used for authentication
   - Bot ID is used in all subsequent API calls
   - Webhook URL is registered for event delivery

## API Endpoints

### Create Agent (Bot Creation API)

**Endpoint**: `POST https://developer.dotgo.com/directory/secure/api/v1/bots/submit_bot`

**Authorization**: Bearer token (access token from Auth2 SSO)

**Request Parameters**:

| Field Name | Validation | Description | Example |
|-----------|-----------|-----------|---------|
| bot_name* | Max 40 chars, alphanumeric + underscore | Agent name | "tou_support_bot" |
| bot_summary* | Max 100 chars | Agent description | "Tou customer support chatbot" |
| privacy_url* | Valid URL, max 2048 chars | Privacy policy | https://www.example.com/privacy |
| term_condition_url* | Valid URL, max 2048 chars | Terms URL | https://www.example.com/terms |
| platform* | "GSMA API" or "Google API" | API style | "GSMA API" |
| email_list* | Max 3 emails, valid format | Contact emails | [{"value":"support@example.com","label":"Contact us"}] |
| website_list* | Max 3 URLs | Company websites | [{"value":"https://www.example.com","label":"Website"}] |
| phone_list* | Max 3 phones, valid format | Contact numbers | [{"value":"+919961000000","label":"Phone"}] |
| logo_image* | JPG/PNG, 224x224px, <90KB | Bot logo | multipart file upload |
| bg_image* | JPG/PNG, 1440x448px, <360KB | Bot banner | multipart file upload |
| agent_color* | Hex RGB code with # (4:5:1 contrast ratio) | Color code | "#000000" |
| lang_supported* | Comma-separated language codes | Languages | "English,Kannada" |
| agent_msg_type* | "Transactional", "Promotional", "OTP", "Multi-Use" | Message category | "Transactional" |
| billing_category* | "Conversational" or "Non_Conversational" | Will be mandatory soon | "Conversational" |
| rcs_bot | RCS bot config object | RCS-specific settings | {"lang_supported":"English","agent_msg_type":"OTP"} |
| bot_desc | Array of objects | Bot description details | [{"bot_name":"Tou Support","bot_summary":"Bot summary"}] |
| brand_details | Array | Brand name | [{"brand_name":"Tou"}] |
| carrier_details* | Valid carrier MCCMNCs + global reach flag | Carrier config | {"carrier_mccmnc":["62160","62402","310160"],"global_reach":false} |
| region | "India" or "Rest of World" | Geographic region | "India" |
| is_carrier_edited* | true/false | Editable post-creation | true |

**Response Parameters**:

| Field Name | Description | Example |
|-----------|-----------|---------|
| status_code | HTTP status | 200 |
| status_message | Success/error message | "success" |
| bot_id | Unique bot identifier (REQUIRED for future API calls) | "T3kTSv-wuFtWke8QOR56pg==" |
| brand_id | Unique brand identifier | "RqvK7giVULCFBQACtBjS8g==" |
| error | Error object if request failed | {"code":400,"message":"Bot name required"} |

### Update Agent (Bot Creation Update API)

**Endpoint**: `PUT https://developer.dotgo.com/directory/secure/api/v1/bots/submit_bot`

Use the same endpoint with PUT method to update existing agent details after creation.

## HTTP Response Codes

| Code | Description |
|------|-------------|
| 200 | Request accepted, agent created |
| 400 | Bad request (missing/invalid fields) |
| 403 | Forbidden (invalid credentials) |
| 500 | Internal server error |

### Common Validation Errors

- "Bot logo image must be of height 224px and width 224px" — Correct image dimensions
- "Logo image should not be more than 90kb" — Reduce file size
- "Bot name is required, max length allowed is 40" — Provide name (max 40 chars)
- "Bot description is required, max length allowed is 100" — Provide description
- "Agent color is required, max length allowed is 7 and must start with #" — Provide #XXXXXX format
- "Selected color has a contrast ratio of 3.92:1. Please specify a color with minimum 4.5:1 contrast ratio relative to white." — Adjust color contrast

## Field/Payload Examples

**Request Sample (Text)** — multipart/form-data

```json
{
  "creation_data": {
    "data": {
      "bot": {
        "privacy_url": "https://www.tou.com/privacy",
        "term_and_condition_url": "https://www.tou.com/terms",
        "platform": "GSMA API",
        "email_list": [
          {
            "value": "support@tou.com",
            "label": "Contact us"
          }
        ],
        "website_list": [
          {
            "value": "https://www.tou.com",
            "label": "Website"
          }
        ],
        "phone_list": [
          {
            "value": "+919961000000",
            "label": "Phone"
          }
        ]
      },
      "rcs_bot": {
        "lang_supported": "English",
        "agent_msg_type": "OTP"
      },
      "bot_desc": [
        {
          "bot_name": "Tou Support",
          "bot_summary": "Bot summary"
        }
      ],
      "brand_details": [
        {
          "brand_name": "Tou"
        }
      ],
      "carrier_details": {
        "carrier_mccmnc": ["62160", "62402", "310160"],
        "global_reach": false
      },
      "region": "India"
    }
  },
  "botLogoImage": "<file from system>",
  "bannerImage": "<file from system>"
}
```

**Response Sample** — 200 OK

```json
{
  "status_code": 200,
  "status_message": "success",
  "bot_id": "T3kTSv-wuFtWke8QOR56pg==",
  "brand_id": "RqvK7giVULCFBQACtBjS8g=="
}
```

## Options / variants

- **Platform choice**: Select GSMA API or Google API based on your integration preference
- **Carrier customization**: Choose between pre-defined carrier lists or custom MCCMNCs
- **Editable carriers**: Allow or restrict carrier list changes post-creation
- **Message type**: Different restrictions apply to Transactional vs. Promotional message types

## Cross-module workflow docs

- After agent creation, register with RCS APIs platform using bot_id
- Configure webhooks for message delivery and user interaction events
- Create message templates (see RCS Templates docs)
- Connect to Bot Studio or Campaign Manager for message routing

## Module disambiguation docs

Agent setup is at the channel/platform level. Once agents are created, use Channels configuration to associate them with bots or campaigns. Message logic and user flows are managed separately in Bot Studio.

## Reference (from source)

<!-- procedural:v2 -->
# RCS Agent Onboarding

Register your brand as an RCS agent on Gupshup's Dotgo RBM Hub to enable rich messaging capabilities.
