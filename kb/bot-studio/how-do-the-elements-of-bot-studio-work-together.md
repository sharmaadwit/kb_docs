source_url: https://console-docs.gupshup.io/docs/how-do-the-elements-of-bot-studio-work-together

<!-- kb-golden:v9 -->
# How do the Elements of Bot Studio Work Together?

**Module**: Bot Studio

## Definition
The Bot Studio has the following elements:

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → How do the Elements of Bot Studio Work Together?

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **How do the Elements of Bot Studio Work Together?**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- _Run a quick smoke test and confirm expected behavior._

### Fields to configure
- _List the fields/inputs you must set in the UI (and expected format)._

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Troubleshooting
- Fallback Journey - The Fallback Journey is default journey that is called when a node in any journey fails to execute if user input is not received correctly

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- Go to **Bot Studio**.
- Go to **How do the Elements of Bot Studio Work Together?**.

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
# How do the Elements of Bot Studio Work Together?

**Module**: Bot Studio

## Overview
The Bot Studio has the following elements:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
The Bot Studio has the following elements:

- Nodes - Building blocks of each journey Message Nodes Prompt Nodes Action Nodes
- Message Nodes
- Prompt Nodes
- Action Nodes
- Controls on Bot Studio Canvas - Makes the usage of canvas easy
- Journey Templates - Pre-built ready to deploy templates
- User Journeys - Consists of multi-journeys which are triggered by user inputs and default journeys that define the logic of the Bot User Journeys designed by Bot Designer - These Journeys are triggered based on user inputs Default Journeys - Configuration Journey - View Only Overview of the Bot Logic. This shows the user journeys that will be triggered for user inputs, marketing journeys that will be triggered for marketing campaigns and ad journeys that will be triggered for ads. Fallback Journey - The Fallback Journey is default journey that is called when a node in any journey fails to execute if user input is not received correctly Welcome Journey - The Welcome Journey is the first journey triggered for users when their inputs are unable to trigger a user journey. This can be overwritten by using user input as triggers for user journeys Triggering a User Journey - The Start Node of each journey can be used to configure user inputs for which journeys will be triggered in run-time
- User Journeys designed by Bot Designer - These Journeys are triggered based on user inputs
- Default Journeys - Configuration Journey - View Only Overview of the Bot Logic. This shows the user journeys that will be triggered for user inputs, marketing journeys that will be triggered for marketing campaigns and ad journeys that will be triggered for ads. Fallback Journey - The Fallback Journey is default journey that is called when a node in any journey fails to execute if user input is not received correctly Welcome Journey - The Welcome Journey is the first journey triggered for users when their inputs are unable to trigger a user journey. This can be overwritten by using user input as triggers for user journeys
- Configuration Journey - View Only Overview of the Bot Logic. This shows the user journeys that will be triggered for user inputs, marketing journeys that will be triggered for marketing campaigns and ad journeys that will be triggered for ads.
- Fallback Journey - The Fallback Journey is default journey that is called when a node in any journey fails to execute if user input is not received correctly
- Welcome Journey - The Welcome Journey is the first journey triggered for users when their inputs are unable to trigger a user journey. This can be overwritten by using user input as triggers for user journeys
- Triggering a User Journey - The Start Node of each journey can be used to configure user inputs for which journeys will be triggered in run-time
- Saving and Deploying Journeys - A Journey can be Saved and Deployed at different instances. Deploying a journey makes it live in rum-time
- Manage API - Interact with entities outside Bot Studio with APIs
- Manage Variable - Save data in variables and use them during Bot runtime
- Campaign Journeys for Marketing - Convert one-way campaign journeys to interactive journeys when customer responds to the marketing campaign
- Ad Journeys for Ads Campaigns - Trigger interactive ad journeys when customer responds to an ad on Facebook or Instagram
- Additional Language support

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Journey Templates - Pre-built ready to deploy templates
- - Manage Variable - Save data in variables and use them during Bot runtime

**Last updated (from source)**: Updated 10 months ago
