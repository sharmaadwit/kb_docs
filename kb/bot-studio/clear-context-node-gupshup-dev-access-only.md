source_url: https://console-docs.gupshup.io/docs/clear-context-nodedev-mode-only
# BOT STUDIO

## Clear Context Node (Gupshup Dev Access Only)

# Clear Context Node (Gupshup Dev Access Only)

# Introduction

Clear Context Node is a special node accessible to Gupshup Developers only where the business logic requires to clear the previous journey stack after completion of a journey or at some other point. Clear Context node will delete the Journey stack which is created at backend to keep track of the journeys which user has traversed and switched the context midway.

# Functional Details to Understand the Feature:

Journey Builder backend keeps track of the context of user journeys and maintains the same on a stack to ensure that the bot is able to hold the context even if the user switches it midway during a journey. The switching of context can happen due to a call and return journey being invoked or the user has invoked any other journey trigger keyword or intent. The clear context node when executed will clear out the stack and the user can also clear the Global Variables that are stored during the previous journey executions by checking the checkbox available on the node.

Updated 10 months ago
