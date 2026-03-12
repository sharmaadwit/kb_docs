source_url: https://console-docs.gupshup.io/docs/configuration-journey

<!-- kb-golden:v1 -->
# Configuration Journey

**Module**: Bot Studio

## Definition
It is a system-generated journey that needs no alterations and is view-only to provide an overview of different journeys being handled by the Bot.

## Procedure
### Where to configure it
Gupshup Console → Bot Studio → Configuration Journey

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Configuration Journey**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- Configuration Journey

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Reference (from source)
<!-- procedural:v2 -->
# Configuration Journey

**Module**: Bot Studio

## Overview
It is a system-generated journey that needs no alterations and is view-only to provide an overview of different journeys being handled by the Bot.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
It is a system-generated journey that needs no alterations and is view-only to provide an overview of different journeys being handled by the Bot.

The configuration journey carries information about the campaign and its associated journey.

It has the following nodes set in logic:

- Start Node
- Condition Node With Events
- Marketing Module Node - This contains all mappings between campaigns and associated journeys.
- Ad Campaign Module Node - This contains all mappings between ads and associated journeys.
- Keyword Trigger Node - This contains all mappings between user input and the associated user journey that can be triggered. For example, if Journey "Welcome" is linked to keyword "Hi", this journey will be triggered when a user says "Hi".
- Return Failure Node
In this journey, you can view keyword-based triggers, for eg, when a user says "Hi", journey Hi can be triggered.

The contains all mappings between campaigns and associated journeys.

### Configuration Journey

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
