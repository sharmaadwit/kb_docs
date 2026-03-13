source_url: https://console-docs.gupshup.io/docs/clevertap-integration

<!-- kb-golden:v9 -->
# CleverTap Integration

**Module**: Integrations

## Definition
Enable CX experiences for your customers in Clevertap.

## Procedure
### Exact UI path
Gupshup Console → Integrations → CleverTap Integration

### Steps
1. Open Gupshup Console.
2. Go to the integrations tab, where you can find the CleverTap integration widget
3. Enable CX experiences for your customers in Clevertap.
4. Click on connect for CleverTap and agree to terms and conditions, and then click on connect.
5. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- _Run a quick smoke test and confirm expected behavior._

### Fields to configure
- _List the fields/inputs you must set in the UI (and expected format)._

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- _Add common failure modes and how to fix them._

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to the integrations tab, where you can find the CleverTap integration widget

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

## Cross-module workflow docs
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation docs
- Integrations configure connectivity/events; they don’t change bot conversation logic (Bot Studio) by themselves.

## Reference (from source)
<!-- procedural:v2 -->
# CleverTap Integration

**Module**: Integrations

## Overview
Enable CX experiences for your customers in Clevertap.

## When to use
_Add the primary scenarios and personas._

## Setup path
- Go to the integrations tab, where you can find the CleverTap integration widget

## Step-by-step configuration
Enable CX experiences for your customers in Clevertap.

In CleverTap Integration, we enable customers to easily launch WhatsApp campaigns directly from their CleverTap account with just a few clicks to complete integration.

How does the CleverTap integration help in achieving your business goals?

- Enhanced Messaging: Access the power to send bulk messages, automate your messaging, and gain insights through analytics, all seamlessly from your CleverTap account.
- Simplified Integration: Easily establish integration in just a few straightforward steps. By clicking "connect," you'll receive the necessary account credentials to configure on your respective integration dashboard. Remember to add a callback URL for receiving DLR (Delivery Report) events right within your CleverTap account.
- Empowering CX Experiences: Elevate your customer experience by deploying bots and other CX enhancements based on the performance of your campaigns, all directly from your Console account.
Steps involved in completing CleverTap integration:

- Go to the integrations tab, where you can find the CleverTap integration widget
- Click on connect for CleverTap and agree to terms and conditions, and then click on connect
- You would be receiving credentials for CleverTap that need to be configured on your CleverTap dashboard on your registered E-mail account.
- You will need to copy and paste the credentials on your CleverTap dashboard, and you can also copy the callback URL from here:
- Post logging in you can configure the fallback URL
Steps involved in template creation and sending messages from CleverTap dashboard:

- In order to create template, login to Console and click on Channels and select WhatsApp
- Now click on create template and add all the required details to create the template
- Upon successful submission the template needs to be reviewed by Meta (For most templates it typically takes few minutes but it can take up to 24 hours for approval from Meta's side)
- Once a template is approved, you can login to CleverTap and click on templates in WhatsApp section
- You can click on "+Template" and copy the content from Gupshup template dashboard
- Note: The content (Template name, category, header, body, footer) all needs to be exactly same as that of the approved template on Gupshup dashboard in order to be able to send campaigns. Else you would be getting an error.
- Now you are ready to send campaigns directly from CleverTap dashboard
- Analytics will be available on Gupshup (click on "All campaigns" and select the campaign) as well as CleverTap dashboard

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- In CleverTap Integration, we enable customers to easily launch WhatsApp campaigns directly from their CleverTap account with just a few clicks to complete integration.

**Last updated (from source)**: Updated 10 months ago
