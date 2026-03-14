source_url: https://console-docs.gupshup.io/docs/inactivity-nudge-for-location-request-node

<!-- kb-golden:v10 -->
# Inactivity Nudge for Location Request Node

**Module**: Bot Studio

## Definition
Click on Node Settings

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Inactivity Nudge for Location Request Node

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- desired
- Timeout duration
- Message content

### Steps
1. Open Gupshup Console.
2. Go to **Bot Studio**.
3. Go to **Inactivity Nudge for Location Request Node**.
4. Click on Node Settings.
5. Configure Nudge Settings: Set the desired inactivity timeout duration. Choose or create a custom nudge message that will be sent to users when they don’t respond within the specified time.
6. Set the desired inactivity timeout duration.
7. Choose or create a custom nudge message that will be sent to users when they don’t respond within the specified time.
8. Click **Save** (or **Save & Deploy**) to apply changes.

### Validation / where to check
- Testing and Verification: During testing, verify that the nudge behaves as configured, prompting users after the inactivity period, similar to other prompt nodes.
- During testing, verify that the nudge behaves as configured, prompting users after the inactivity period, similar to other prompt nodes.
- Scenario: A food delivery service needs to confirm a user’s location for accurate order delivery.
- Scenario: A local business requests location verification to confirm if a customer is within a serviceable area.

### Troubleshooting
- If behavior is unchanged, confirm you updated the correct node and used **Save & Deploy** for live channels.
- If the wrong branch/path runs, re-check conditions, connected nodes, and fallback connectors.

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Go to **Bot Studio**.
- Go to **Inactivity Nudge for Location Request Node**.

## Options / variants
- Set the desired inactivity timeout duration.
- Choose or create a custom nudge message that will be sent to users when they don’t respond within the specified time.

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
# Inactivity Nudge for Location Request Node

**Module**: Bot Studio

## Overview
Click on Node Settings

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Click on Node Settings

Get the Inactivity Nudge option

# Introduction

The Inactivity Nudge for Location Request Node is an enhancement that enables proactive reminders to users when they don’t respond promptly to location requests within the Journey Builder. This feature aligns with existing inactivity settings across other prompt nodes, ensuring a consistent user experience and effective follow-up in cases of delayed responses.

# Key Aspects of the Feature

- Enhanced Engagement: Helps retain user engagement by prompting for a response if they don't reply to location requests within a set time.
- Replicated Functionality: Inactivity settings mirror those on other prompt nodes, making it easy for bot designers to configure and implement nudges consistently.
- Seamless User Interface: The settings for inactivity nudges are integrated directly into the Location Request Node settings, ensuring ease of use for bot designers.
# How to Use

- Access Inactivity Nudge Settings: In the Journey Builder, select the Location Request Node within a flow. Open the Node Settings to configure inactivity nudge options.
- In the Journey Builder, select the Location Request Node within a flow.
- Open the Node Settings to configure inactivity nudge options.
- Configure Nudge Settings: Set the desired inactivity timeout duration. Choose or create a custom nudge message that will be sent to users when they don’t respond within the specified time.
- Set the desired inactivity timeout duration.
- Choose or create a custom nudge message that will be sent to users when they don’t respond within the specified time.
- Testing and Verification: During testing, verify that the nudge behaves as configured, prompting users after the inactivity period, similar to other prompt nodes.
- During testing, verify that the nudge behaves as configured, prompting users after the inactivity period, similar to other prompt nodes.
# Use Cases

- Location Confirmation in Delivery Services Scenario: A food delivery service needs to confirm a user’s location for accurate order delivery. Benefit: The inactivity nudge prompts users if they haven’t shared their location within a specified time, reducing the risk of delivery delays.\
- Scenario: A food delivery service needs to confirm a user’s location for accurate order delivery.
- Benefit: The inactivity nudge prompts users if they haven’t shared their location within a specified time, reducing the risk of delivery delays.\
- Serviceable Location Confirmation for Local Businesses Scenario: A local business requests location verification to confirm if a customer is within a serviceable area. Benefit: The inactivity nudge helps ensure users respond promptly, enabling quick confirmation and improved service efficiency.
- Scenario: A local business requests location verification to confirm if a customer is within a serviceable area.
- Benefit: The inactivity nudge helps ensure users respond promptly, enabling quick confirmation and improved service efficiency.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
