source_url: https://console-docs.gupshup.io/docs/location-request-node

<!-- kb-golden:v1 -->
# Location Request Node

**Module**: Bot Studio

## Definition
The Location Request Node(CTA Based) in Journey Builder allows businesses to send a location call-to-action (CTA) to users via WhatsApp. This feature enables users to share their current location or a specific location with ease, creating a more interactive and location-aware experience within a conversation.

## Procedure
### Where to configure it
Gupshup Console → Bot Studio → Location Request Node

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Location Request Node**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- Store Locator Assistance
- Emergency Services
- Delivery Address Confirmation

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Reference (from source)
<!-- procedural:v2 -->
# Location Request Node

**Module**: Bot Studio

## Overview
The Location Request Node(CTA Based) in Journey Builder allows businesses to send a location call-to-action (CTA) to users via WhatsApp. This feature enables users to share their current location or a specific location with ease, creating a more interactive and location-aware experience within a conversation.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
# Introduction

The Location Request Node(CTA Based) in Journey Builder allows businesses to send a location call-to-action (CTA) to users via WhatsApp. This feature enables users to share their current location or a specific location with ease, creating a more interactive and location-aware experience within a conversation.

# Key Aspects of the Feature

Location Sharing via WhatsApp: Businesses can send a prompt asking users to share their location, which users can respond to by providing their current or chosen location through WhatsApp.

Customizable Message: Bot designers can add a custom message body for the location request. This message appears alongside the location prompt, providing context for why the user’s location is being requested.

Response Stored in Variable: The user's location response is stored as a JSON object in an optional variable. This makes it easy for bot designers to extract relevant location data like latitude, longitude, or address details.

Timeout and Skip Options: The node supports a configurable timeout option, allowing bot designers to set a duration within which the user must respond. "Skip Node" option is also available, enabling the bot to move forward if the mapped variable already consists a value for that user

Persistent Message for Sticky Journeys: The persistent message checkbox or header is available for sticky journeys, ensuring that the location prompt remains visible throughout the conversation even if the user changed the context and came back to the sticky journey.

# Validation

Response Validation: The response must be of type location. If the response does not meet this requirement, validation will trigger, and the user may be prompted to provide a valid location.

Failure Message Handling: If the "Enable Failure Message" option is checked, the bot will send a failure message and prompt the user again, just like other prompt nodes. This ensures the user has another chance to provide the correct location.

# How to Use

Add the Location Node:

- In Journey Builder, insert the Location Node into your flow and configure the message body that will appear along with the location prompt.
- Choose only a JSON variable to store the response by selecting the ‘store response in’ field
Sample Payload for stored location info in the mapped variable:

```
{"latitude":"24.6845804","longitude":"92.5756971"}
```

Set Up Timeout and Failure Handling:

- Configure the timeout duration for how long the bot should wait for a response
- Enable failure message handling to retry the prompt with a custom failure message if the user’s response is invalid after all retries are over
Persistent Message:

- If the journey is set to be sticky, enable the persistent message checkbox to ensure the location prompt is resent with additional context once the user comes back to the sticky journey
# Use Cases:

Here are some use cases of the Location Node:

### Store Locator Assistance

- Scenario: The business wants users to find the nearest store of their brand based on their current location.
- Benefit: By using the Location Node, the bot can prompt users to share their location via WhatsApp, enabling the business to provide personalized store recommendations quickly.
### Emergency Services

- Scenario: A healthcare provider offers emergency services through WhatsApp, where users may need to share their current location for assistance.
- Benefit: The Location Node allows users to send their exact location during emergencies, ensuring timely and accurate support from the service provider.
### Delivery Address Confirmation

- Scenario: A food delivery service needs to confirm the customer’s delivery address during order processing.
- Benefit: By prompting the customer to share their location through WhatsApp, the bot can gather accurate location data and avoid delivery errors.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 9 months ago
