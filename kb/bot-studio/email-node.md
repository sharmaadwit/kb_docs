source_url: https://console-docs.gupshup.io/docs/email-node

<!-- kb-golden:v10 -->
# Email Node

**Module**: Bot Studio

## Definition
This prompt is used to get the user's email ID and store it in a variable after validating the input shared by the user.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Email Node

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Email Node**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- For Instance: You need to capture a customer’s email ID for a Lead Generation use case. Using the Phone prompt, you can save the user response in a variable and validate it.

### Troubleshooting
- If behavior is unchanged, confirm you updated the correct node and used **Save & Deploy** for live channels.
- If the wrong branch/path runs, re-check conditions, connected nodes, and fallback connectors.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Bot Studio**.
- Go to **Email Node**.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Email Node

**Module**: Bot Studio

## Overview
This prompt is used to get the user's email ID and store it in a variable after validating the input shared by the user.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
This prompt is used to get the user's email ID and store it in a variable after validating the input shared by the user.

For Instance: You need to capture a customer’s email ID for a Lead Generation use case. Using the Phone prompt, you can save the user response in a variable and validate it.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- For Instance: You need to capture a customer’s email ID for a Lead Generation use case. Using the Phone prompt, you can save the user response in a variable and validate it.

**Last updated (from source)**: Updated 10 months ago
