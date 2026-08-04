---
title: Agent Tools
description: Custom tools and system tools integration for agents
source: https://voiceagents.gupshup.io/developer-docs
---

# Agent Tools

## Tools Tab

The Tools tab extends agent capabilities by attaching both custom integrations and built-in system actions. Tools empower agents to perform real-world operations during live calls.

### Interface Layout

  * **Left Section:** Custom tools list — initially empty for new agents

  * **Right Section:** System tools panel with individual enable/disable toggles

### Adding Custom Tools

  * Click Add tool (dropdown, top right) to add a new integration

  * Use the Search tools... bar to locate existing tools in your library

Filter using + Type or + Creator filters

Switch between the Tools and MCP sub-tabs as required

### System Tools Reference

System tools are platform-native capabilities that can be enabled independently for each agent:

| System Tool | Description | Use Case |
|---|---|---|
| End Conversation | Programmatically terminates the call | Graceful call conclusion after task completion |
| Detect Language | Automatically identifies the caller's spoken language | Multilingual deployments |
| Skip Turn | Allows the agent to defer its conversational turn | Complex query handling scenarios |
| Transfer to Agent | Routes the call to a designated human agent | Escalation and live agent handoff |
| Transfer to Number | Forwards the call to a specified phone number | Departmental routing and warm transfers |
| Play Keypad Touch Tone | Plays DTMF tones during the call | IVR navigation and third-party system interaction |
| Voicemail Detection | Identifies if the call has reached a voicemail system | Automated outbound calling campaigns |

> ⚠ IMPORTANT The active tools counter at the top of the System Tools panel displays the number of currently enabled tools. Enable only the tools required for a given agent to maintain lean, predictable behaviour.

## Workspace Tools Page

The **Tools** item in the workspace sidebar opens the HTTP tool registry: create tools, browse templates, manage Secrets, and connect **Shopify**. The Shopify panel lets you verify an Admin API access token against `GET /shop.json` and save `SHOPIFY_STORE` / `SHOPIFY_ACCESS_TOKEN` into Secrets, then use **Browse templates** for Shopify presets (order note, customer search, etc.) and attach them on each agent's Tools tab.
