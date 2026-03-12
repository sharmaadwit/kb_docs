source_url: https://console-docs.gupshup.io/docs/custom-events-in-customer360

<!-- procedural:v2 -->
# Custom events in Personalize

**Module**: Personalize

## Overview
Introduction:

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Introduction:

Once events are defined for a custom integration, they automatically appear on the events page, with events under the particular source/integration (eg: Razorpay).

Each custom event has an integration status and subscription.

- Integration status: This defines whether a particular integration is active or not (eg: event_1 is inactive, which means it's discarded in integrations module)
Integration status: This defines whether a particular integration is active or not (eg: event_1 is inactive, which means it's discarded in integrations module)

- Subscription: This defines whether Personalize can consume a particular event and what is the action necessary to allow the event to be consumed by Personalize. Activate the event: The integration needs to be activated to send events to Personalize Mapping pending: The mapping for phone number/E-mail (profile identifier) is pending Completed: The events can be consumed by Personalize
Subscription: This defines whether Personalize can consume a particular event and what is the action necessary to allow the event to be consumed by Personalize.

- Activate the event: The integration needs to be activated to send events to Personalize
- Mapping pending: The mapping for phone number/E-mail (profile identifier) is pending
- Completed: The events can be consumed by Personalize
When we click on an event we get to the mapping screen where properties defined in integrations can be mapped to profile properties in Personalize. To complete mapping phone number/E-mail mapping is must and other attributes can be mapped optionally. Post mapping, the attribute values are mapped to a profile and can be subsequently used in segmentation and automated campaigns.

Custom events in segmentation: All custom events with mapping completed status appear in the event drop-down. In the below example all the users who have performed "Signup" on "Website" with "city" = "Mumabi" at least once between the specific dates will be part of the segment. Now we can send a welcome nudge to these users to engage further with them.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 4 months ago
