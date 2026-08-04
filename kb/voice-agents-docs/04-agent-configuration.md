---
title: Agent Configuration
description: Create Agent configuration, system prompts, voice settings, and publishing
source: https://voiceagents.gupshup.io/developer-docs
---

# Create Agent

## Agent Tab

The Agent tab is the primary configuration panel when creating or editing an agent. It is divided into two panels: Agent Configuration (left) and Voice & Language Settings (right).

### Left Panel — Agent Configuration

| Field | Required | Description |
|---|---|---|
| Agent Name | Yes | A unique, descriptive identifier for the agent (e.g., 'Customer Support Bot') |
| Tags | No | Comma-separated labels used for categorisation and filtering across the dashboard |
| System Prompt | Yes | The core instruction set governing agent behaviour, persona, and capabilities |
| First Message | No | The opening utterance when a call is connected. If left blank, the agent waits for the caller to speak first. Default: 'Hello! How can I help you today?' |
| Dynamic Variables | No | Runtime placeholder variables using {{variable_name}} syntax, replaced with live values during calls |

### System Prompt Toolbar

Three actions are available in the toolbar beneath the System Prompt text area:

  * **Search:** Search within the prompt text for specific terms or phrases

  * **Edit / Expand:** Open the prompt in a full-screen editor for extended editing

  * **Improve with AI:** Invoke AI optimisation on the existing prompt content (enabled only after content has been entered)

> ℹ NOTE A well-crafted System Prompt is the most critical factor in agent performance. Use the 'Improve with AI' function to refine prompts, and validate results using the Test Agent tab before publishing.

### Right Panel — Voice & Language Settings

| Setting | Description |
|---|---|
| Voices | Select the primary voice persona. Default: 'Eric — Smooth, Trustworthy'. Additional voices can be added via '+ Add additional voice'. Use the play button to preview any voice. |
| Expressive Mode (New) | Enhances speech with emotionally intelligent intonation and expressive audio tags. Enable or dismiss as appropriate for the use case. |
| Language | Set the default conversation language. Additional languages can be added for multilingual agent support. |
| LLM | Select the underlying AI language model provider and version. Default: gpt-4.1-mini. |

### Top Bar Actions

  * **Publish:** Deploys and activates the agent on the platform (new agents only)

Tab Navigation: Agent | Tools | Knowledge Base | Advanced | Test Agent | Test Analysis
