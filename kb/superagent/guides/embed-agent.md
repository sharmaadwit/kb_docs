---
title: "Embed an Agent"
description: "Add your agent to any website, portal, or external app as a chat widget"
module: SuperAgent
category: "Core Fundamentals / Agents"
slug: "guides/embed-agent"
---

# Embed an Agent

**Module**: SuperAgent

Embedding lets you put any agent directly on your own website or internal tool as a chat widget. Visitors interact with your agent without ever opening SuperAgent — it looks and feels like part of your product.

## Who pays for embedded chats?

Embedded chats always use the agent owner's credits. Signed-in visitors can bring their own identity and connectors, but billing still stays with the agent owner.

| Visitor access | Who is billed | Best for |
| --- | --- | --- |
| Anonymous visitors | Your credits, every conversation | Public support, lead capture, and customer-facing assistants |
| Signed-in SuperAgent users | Your credits, every conversation | Internal portals where users need their own connectors |

## iframe vs floating widget

Two embed formats are available. Choose the one that fits your site layout:

| Property | iframe | Script (floating widget) |
| --- | --- | --- |
| How to add | Single <iframe> tag in your HTML | <script> tag, usually before </body> |
| Appearance | Inline — fits inside a page section | Floating bubble pinned to a corner |
| Best for | Dedicated chat or support pages | Adding to every page without redesigning |
| Customize position | Set width/height on the iframe | Override position with CSS |

## How to embed your agent

### Step 1: Open the agent you want to embed

Click **All agents** in the sidebar, then click the agent card to open its detail page.

### Step 2: Click the Embed card in the Interact section

On the agent detail page, find the **Interact** section. Click the **Embed** card — it reads *"Add this agent to any site with an iframe."* The embed configuration panel opens.

### Step 3: Turn the embed on

Toggle the embed **On**. A unique public ID is created for your agent. The iframe and script snippets become available to copy.

### Step 4: Choose visitor access

Choose **Anonymous visitors** for a public chat experience, or **SuperAgent users** when visitors should sign in and use their own connected accounts. Your wallet pays for both access modes.

### Step 5: Copy and paste the snippet into your website

Copy either the **iframe** snippet or the **Script** snippet and paste it into your website's HTML. See the *iframe vs floating widget* table above to decide which format suits your site.

## What embedded users can do

What a visitor can access depends on whether they are signed in to SuperAgent:

| Visitor type | Agent skills & recipes | Connectors | Billing |
| --- | --- | --- | --- |
| Anonymous visitor | ✓ | None | Owner pays |
| Signed-in SuperAgent user | ✓ | Their own connectors | Owner pays |

> [!INFO]
> **Your private connectors never run for anonymous visitors**
> The embed is a public surface. To protect your data, your Gmail, Sheets, and other personal integrations are never accessible to anonymous embedded users. Signed-in visitors can use their own connected accounts.

> [!INFO]
> **Treat embed links as public**
> Anyone with the iframe URL or script snippet can load the embed while it is enabled. Share snippets only with sites you control, monitor usage, and turn the embed off if you need to stop public access.

## Pre-launch checklist

| Check | Why it matters |
| --- | --- |
| ✓Visitor access is intentional | Signed-in mode lets visitors use their own connected accounts |
| ✓Credit usage is planned | Every embedded conversation uses your credits; review budget before going live |
| ✓Instructions are tested | Send a few messages as an anonymous visitor to verify the agent behaves correctly |
| ✓Embed toggle is On | The widget returns an error if the embed is toggled Off |

## Turn off an embed

Toggle the embed **Off** in the agent's Embed panel at any time. The public ID is deactivated immediately — the widget on your website will stop responding until you turn it back on. No code changes needed on your site.

## What's next

- [Agents overview](/documentation/concepts/agents) — understand all agent features including Slack, WhatsApp, and automations
- [Create an Agent](/documentation/guides/create-agent) — step-by-step guide to building your first agent
- [Connect Integrations](/documentation/guides/connect-integration) — add Gmail, Sheets, Jira, and more to your agent
