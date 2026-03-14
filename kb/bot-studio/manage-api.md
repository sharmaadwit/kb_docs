source_url: https://console-docs.gupshup.io/docs/manage-api

<!-- kb-golden:v10 -->
# Manage API

**Module**: Bot Studio

## Definition
It is a section where you can set all the APIs to integrate with external systems.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Manage API

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Manage API**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run the flow in **Test your Bot** and confirm the expected node/path executes.
- If the change must affect live traffic, use **Save & Deploy** and verify on the target channel.

### Troubleshooting
- If behavior is unchanged, confirm you updated the correct node and used **Save & Deploy** for live channels.
- If the wrong branch/path runs, re-check conditions, connected nodes, and fallback connectors.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Bot Studio**.
- Go to **Manage API**.

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
# Manage API

**Module**: Bot Studio

## Overview
It is a section where you can set all the APIs to integrate with external systems.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
### Manage APIs

It is a section where you can set all the APIs to integrate with external systems.

### When to use

Setting up an API is required when you need to communicate with any external system to get, push or read some details.

For instance: You want to send user details captured on the chatbot to a CRM tool. This is possible using Manage API, here, all the APIs can be set and used in the flow accordingly.

### Limitations

- API names can’t be the same.
- API names field can’t be empty.
- API URL field can’t be empty.
- Key and Value both are required.
Note: There is no limitation on the number of APIs that you want to set.

### How to Use

There are two methods provided to set an API in a chatbot journey:

- Create an API
- Import APIs
A new API can be created by clicking on the New API button on the screen, all the details required (URL, API method, Key, and Value) are to be entered manually.

Import APIs can be used if a collection of APIs is to be imported from Postman. Using import APIs all the details are auto-filled on the screen.

### Manage APIs Screen

To use APIs in middle of journeys, use the API Node.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
