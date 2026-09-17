---
title: "Integrations"
description: "Connect your apps and services so your AI can work with your real data"
module: SuperAgent
category: "Core Fundamentals / Integrations"
slug: "concepts/integrations"
---

# Integrations

**Module**: SuperAgent

Integrations are connections to external services your AI assistant can use. When you connect an integration, you give SuperAgent permission to read from and act on your behalf in that service—so you can ask things like "Show my unread emails" or "Create a Jira ticket for this bug" and the AI will do it.

## What are integrations?

Integrations let your AI work with the tools you already use every day. Instead of copying data manually or switching between apps, you can stay in the chat and ask the AI to handle it. The AI uses secure, authorized connections to access your accounts—you control which services are connected and can disconnect them anytime.

## Available integrations

SuperAgent supports connections to these popular services. Each card shows what the AI can do once connected:

**Gmail**Read emails, send replies, search your inbox, draft messages

**Google Sheets**Add rows, update cells, read data, create charts

**Google Calendar**Check your schedule, create events, find free slots

**Google Drive**List files, read documents, organize folders

**Google Docs**Search documents, read content, create docs, edit text

**Jira**Create tickets, update status, search issues, add comments

**Salesforce**Look up contacts, create leads, update records

## How connecting works

Connecting an integration is simple. Go to the Integrations area, find the service you want, and click** Connect**. A popup will open asking you to sign in and authorize SuperAgent to access your account. Once you approve, the connection is established—no technical setup required.

> [!INFO]
> **Authorization**
> You'll sign in through the service's own login page (e.g., Google or Atlassian). SuperAgent never sees your password; it only receives a secure token that allows it to act on your behalf within the permissions you grant.

## Enabling and disabling integrations

After you connect an integration, you can turn it on or off without disconnecting. When disabled, the AI won't use that service—useful if you want to keep the connection for later but don't need it for current tasks. Re-enable it anytime with a single toggle.

Just describe what you need in plain language—the AI figures out which integration to use and how to do it.

## What can you ask?

Here are example prompts you can try once an integration is connected:

- **Gmail** — "Show my unread emails from today" · "Draft a reply to Sarah's last message"
- **Google Sheets** — "Add a new row to my expenses sheet" · "Create a chart from column B"
- **Google Calendar** — "What meetings do I have tomorrow?" · "Schedule a 30-min call with Alex on Friday"
- **Google Drive** — "Find the Q4 report in my Drive" · "List files shared with me this week"
- **Google Docs** — "Find my meeting notes doc and summarize it" · "Create a new doc titled Weekly update with a short intro"
- **Jira** — "Create a bug ticket for the login issue" · "Show my open tickets"
- **Salesforce** — "Look up the contact info for Acme Corp" · "Create a new lead"

> [!TIP]
> **Combine integrations**
> You can use multiple integrations in a single prompt. For example: "Check my calendar for tomorrow and draft a prep email for each meeting using Gmail."

## What's next?

- [Connect an Integration](/documentation/guides/connect-integration) — Step-by-step setup guide
- [Agents](/documentation/concepts/agents) — Build agents that use your integrations
- [Scheduled Tasks](/documentation/concepts/scheduled-tasks) — Automate integration-powered workflows
