source_url: https://console-docs.gupshup.io/docs/clear-context-nodedev-mode-only

<!-- kb-golden:v1 -->
# Clear Context Node (Gupshup Dev Access Only)

**Module**: Bot Studio

## Definition
Clear Context Node is a special node accessible to Gupshup Developers only where the business logic requires to clear the previous journey stack after completion of a journey or at some other point. Clear Context node will delete the Journey stack which is created at backend to keep track of the journeys which user has traversed and switched the context midway.

## Procedure
### Where to configure it
Gupshup Console → Bot Studio → Clear Context Node (Gupshup Dev Access Only)

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Bot Studio → Clear Context Node (Gupshup Dev Access Only)**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Reference (from source)
<!-- procedural:v2 -->
# Clear Context Node (Gupshup Dev Access Only)

**Module**: Bot Studio

## Overview
Clear Context Node is a special node accessible to Gupshup Developers only where the business logic requires to clear the previous journey stack after completion of a journey or at some other point. Clear Context node will delete the Journey stack which is created at backend to keep track of the journeys which user has traversed and switched the context midway.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
# Introduction

Clear Context Node is a special node accessible to Gupshup Developers only where the business logic requires to clear the previous journey stack after completion of a journey or at some other point. Clear Context node will delete the Journey stack which is created at backend to keep track of the journeys which user has traversed and switched the context midway.

# Functional Details to Understand the Feature:

Journey Builder backend keeps track of the context of user journeys and maintains the same on a stack to ensure that the bot is able to hold the context even if the user switches it midway during a journey. The switching of context can happen due to a call and return journey being invoked or the user has invoked any other journey trigger keyword or intent. The clear context node when executed will clear out the stack and the user can also clear the Global Variables that are stored during the previous journey executions by checking the checkbox available on the node.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
