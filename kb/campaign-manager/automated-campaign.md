source_url: https://console-docs.gupshup.io/docs/automated-campaign

<!-- kb-golden:v10 -->
# Automated campaign

**Module**: Campaign Manager

## Definition
Introduction:

## Procedure
### Exact UI path
Gupshup Console → Campaign Manager → Automated campaign

### Prerequisites
- Access to Campaign Manager for the target brand/project.
- A campaign or campaign draft relevant to this configuration.

### Fields to configure
- No explicit fields were identified in the source; use the UI controls shown on this page.

### Steps
1. Open Gupshup Console.
2. Go to **Campaign Manager**.
3. Go to **Automated campaign**.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Run a small test send and confirm the expected campaign status/metrics appear in Campaign Manager.

### Troubleshooting
- If data is missing or stale, confirm the campaign has actually run and refresh/reopen the analytics view.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Campaign Manager**.
- Go to **Automated campaign**.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Identify the upstream module where this is configured and the downstream module where the outcome is verified.

## Module disambiguation docs
- Campaign creation/config is in **Campaign Manager**; delivery status can also be observed via **Webhooks** (Integrations).

## Reference (from source)
<!-- procedural:v2 -->
# Automated campaign

**Module**: Campaign Manager

## Overview
Introduction:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Introduction:

Automated Campaign is a new feature available on Gupshup's Console product. The Goal of the feature is to support sending trigger based messages to users, for example let's say your Shopify store is connected with Gupshup and if the user abandons the cart, you can send a personalized message to nudge user to complete the purchase. Many such powerful use cases will be addressed through the Automated Campaigns feature.

Since it's a Beta feature we currently support events from 2 sources:

- Shopify
- WhatsApp
Updated 10 months ago

- Sending an Automated Campaign

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
