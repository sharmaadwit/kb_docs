source_url: https://console-docs.gupshup.io/docs/manage-api

<!-- kb-golden:v9 -->
# Manage API

**Module**: Bot Studio

## Definition
It is a section where you can set all the APIs to integrate with external systems.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Manage API

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Manage API**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

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
- Go to **Bot Studio**.
- Go to **Manage API**.

## Options / variants
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Field/payload examples
- _Add a minimal example payload or field/value example._

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
