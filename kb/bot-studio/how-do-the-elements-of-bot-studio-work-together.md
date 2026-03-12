source_url: https://console-docs.gupshup.io/docs/how-do-the-elements-of-bot-studio-work-together

<!-- kb-golden:v4 -->
# How do the Elements of Bot Studio Work Together?

**Module**: Bot Studio

## Definition
The Bot Studio has the following elements:

## Procedure
### Exact path
Gupshup Console → Bot Studio → How do the Elements of Bot Studio Work Together?

### Where to configure it
Gupshup Console → Bot Studio → How do the Elements of Bot Studio Work Together?

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → How do the Elements of Bot Studio Work Together?**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- Fallback Journey - The Fallback Journey is default journey that is called when a node in any journey fails to execute if user input is not received correctly

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation
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
