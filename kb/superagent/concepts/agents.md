---
title: "Agents"
description: "Focused AI assistants you configure for a specific job"
module: SuperAgent
category: "Core Fundamentals / Agents"
slug: "concepts/agents"
---

# Agents

**Module**: SuperAgent

An Agent is an AI assistant you build once and use everywhere. Give it a name, a purpose, the right skills, and a set of instructions — then deploy it in chat, on Slack, on WhatsApp, or via API. It always shows up ready for its job, with no re-explaining needed.

## How an agent works

Every time someone sends a message to your agent, it reads your custom instructions, picks the skills and connectors you have assigned, and produces a response. You control all three layers — what it knows, what it can do, and how it behaves.

## What you configure

### Name, description, and avatar

Give your agent a clear name that describes its role — for example, *Support Assistant* or *Data Analyst*. The description helps teammates understand when to use it. Pick an avatar icon to make it easy to spot in the sidebar.

### Skills and recipes

Skills are the tools your agent can use — things like reading emails, querying a spreadsheet, generating a chart, or running custom code. Recipes are step-by-step workflow templates. Assign only the skills and recipes that match the agent's purpose. The AI only sees what you give it, which keeps it focused and prevents it from using the wrong tool.

### Custom instructions

Instructions tell the agent how to behave on every conversation. Write them in plain English: "Always cite your sources", "Keep responses under 200 words", "When in doubt, ask a clarifying question." The agent follows these every time, without you needing to repeat them.

### Guardrails

Guardrails are safety constraints. Use them to prevent the agent from going outside its intended scope — for example, "Do not discuss pricing" or "Only answer questions about our product." If a user asks something outside those limits, the agent declines politely.

### Connectors (integrations)

Connectors let your agent access external services — Gmail, Google Sheets, Google Docs, Google Drive, Calendar, Jira, Salesforce, and more. Enable only the connectors the agent needs. You can always add or remove them later.

> [!WARNING]
> **Connectors on public channels**
> When your agent is connected to Slack or WhatsApp, **your private connectors are blocked**. Anyone in that channel or with that number can message the agent, so it runs without access to your personal accounts. The agent can still use its skills, recipes, and instructions — just not your Gmail, Sheets, or other private integrations.

## Ways to deploy your agent

Every agent you create can be deployed in five different ways. Each surface has a different audience and a different set of capabilities:

| Interact with users | How to access | Audience | Connectors |
| --- | --- | --- | --- |
| Chat | Click Chat on the agent detail page | You and your team inside SuperAgent | ✓ Full access |
| Automate | Click Automate → set a schedule or prompt | Runs unattended on a schedule | ✓ Full access |
| Slack | Click Slack → connect a workspace channel | Anyone in that Slack channel | Blocked |
| WhatsApp | Click WhatsApp → connect a WABA number | Anyone with the phone number | Blocked |
| Embed | Click Embed → copy iframe or script snippet | Visitors on your website | Signed-in users only |

> [!INFO]
> **API access is separate**
> Any agent can also be called directly via HTTP using an API key — ideal for integrating the agent into your own app or automation pipeline. Create a key from the **</> API** button on the agent detail page.

## Connect to Slack

Open an agent, click **Slack**, and click **+ Connect Slack**. Install the SuperAgent Slack app in your workspace, then bind the agent to a channel. Once connected, channel members can mention the agent using its handle to get a reply.

You can connect the same agent to multiple channels, or connect different agents to different channels — each with its own handle and purpose.

> [!WARNING]
> **What's blocked on Slack**
> Anyone in the Slack channel can chat with this agent. To keep your data safe, connectors and other owner-private tools are blocked. The agent can still use its configured instructions, skills, and recipes.

## Connect to WhatsApp

Open an agent, click **WhatsApp**, and click **+ Connect number**. Enter your Gupshup WABA (WhatsApp Business API) number, then paste the callback URL shown into your Gupshup app dashboard. Once verified, anyone messaging that number will be handled by your agent.

> [!WARNING]
> **What's blocked on WhatsApp**
> Anyone with this WhatsApp number can chat with this agent. Connectors and other owner-private tools are blocked. The agent can still use its configured instructions, skills, and recipes.

## Use your agent via API

Every agent can be called from your own app, script, or automation using an API key. Open the agent, click **API**, then click **Create Key**. Send the key in the `X-API-Key` header with every request.

**Endpoints:**

- `POST /api/agents/chat` — non-streaming; returns a single JSON response
- `POST /api/agents/chat/stream` — Server-Sent Events stream for real-time responses

**Required fields in the request body:** `message`, `session_id`, `user_email_id` (the end-user's email). Optional: `conversation_id` (continue a thread), `model`, `tenant_context`.

> [!WARNING]
> **Save your API key immediately**
> When you create an API key, **copy it straight away**. You will only see the full key once. After you close the dialog, it cannot be recovered — you would need to delete it and create a new one.

### Who pays for API usage?

Each API key has a **credit mode**:

- **Owner pays** — your credits are deducted for every API call, regardless of who made the request. Use this when you are building a product for your own customers.
- **User pays** — the caller must include their own SuperAgent Bearer token. Their credits are deducted. Use this when your API callers are SuperAgent users themselves.

## Automations

Automations are scheduled tasks tied to a specific agent. Open an agent, click **Automate**, and create a task — you set a prompt and a schedule (daily, weekly, or a custom cron pattern). The agent runs that task automatically at the times you choose, without you needing to be online.

> [!INFO]
> **Managing agent automations**
> Tasks created from an agent's Automations panel are owned by that agent. If they appear in Settings → Scheduled Tasks, they show a **"Created by micro agent"** badge and their edit, pause, and delete buttons are disabled there. To manage them, open the agent and use its Automations panel.

## Share with your team

You can publish an agent as a template so your teammates can install their own copy:

- **Org sharing** — visible to everyone in your organization. They can browse it, install it, and use it independently. Edits to your working agent do not affect their copies.
- **Global template** — visible to all SuperAgent users. Only administrators can publish or unpublish global templates.

When you publish an agent, SuperAgent creates an independent snapshot. Your working agent and the published template are separate — you can keep improving yours without changing what others already have.

## What works where

Depending on how your agent is accessed, some features are available and some are not. Here is a quick reference:

| Interact with users | Skills & Recipes | Your Connectors | Automations |
| --- | --- | --- | --- |
| SuperAgent chat | ✓ | ✓ | ✓ |
| Slack channel | ✓ | Blocked | — |
| WhatsApp number | ✓ | Blocked | — |
| API (external app) | ✓ | Blocked | — |
| Embed (your website) | ✓ | Signed-in users only | — |

> [!TIP]
> **Keep it focused**
> The best agents do one job well. A support agent handles tickets; a data agent pulls reports. Assigning too many skills or writing vague instructions leads to unpredictable responses. Start narrow and expand as you learn what your agent needs.

## What's next

- [Create an Agent](/documentation/guides/create-agent) — step-by-step walkthrough with an interactive demo
- [Embed an Agent](/documentation/guides/embed-agent) — add your agent to any website or app
- [Skills](/documentation/concepts/skills) — learn about the tools you can assign
- [Recipes](/documentation/concepts/recipes) — reusable workflow templates for your agent
- [Scheduled Tasks](/documentation/concepts/scheduled-tasks) — automate work on a recurring schedule
