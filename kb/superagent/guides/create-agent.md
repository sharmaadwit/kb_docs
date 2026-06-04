---
title: "Create an Agent"
description: "Build a focused AI assistant for a specific job — from first message to API access"
module: SuperAgent
category: "Core Fundamentals / Agents"
slug: "guides/create-agent"
---

# Create an Agent

**Module**: SuperAgent

> [!NOTE]
> **Prerequisites · ~5 minutes**
> You need a SuperAgent account. No skills or integrations are required to create your first agent — you can add those after.

This walkthrough takes you from opening the Agents workspace all the way to chatting with a live agent. The interactive preview below mirrors the real app — click it to pause or play.

## See it in the app

### Step 1: Click All agents in the sidebar

Click **All agents** in the left sidebar. The Agents workspace opens, showing a featured template banner and your agents listed under the **My agents** tab. Click **Templates** to browse ready-made starters.

### Step 2: Click + New agent

Click **+ New agent** in the top-right area. A dialog slides open over the workspace — or click **Browse templates** to install a ready-made agent instead. Templates are independent copies; editing yours will not affect anyone else's.

### Step 3: Name your agent and click Create

In the dialog, fill in:

- **Agent name** — pick something that describes the job, e.g. *Support Assistant*
- **Description** (optional) — helps teammates know when to use it

Click **Create**. Your agent is saved immediately.

### Step 4: Your agent is live — explore the detail page

The agent detail page opens showing the agent name and an **Interact** section with five cards: **Chat**, **Automate**, **Slack**, **WhatsApp**, and **Embed**. Each card is a separate deployment option for your agent.

### Step 5: Open API access

Click the **</> API** button in the top-right to open the API Information dialog. This is where you create keys and copy request examples for external apps.

### Step 6: Get your API key

Click **+ Create Key** in the API Information dialog to generate a key.

> [!WARNING]
> **Copy your key now**
> The full API key is shown only once. Copy it and store it securely before closing the dialog — it cannot be recovered afterwards.

Use the key in the `X-API-Key` header when calling `POST /api/agents/chat` or `POST /api/agents/chat/stream`.

### Step 7: Add connectors

Click the connectors area to open the **Agent connectors** dialog. Select the integrations this agent can access in private chats, schedules, and webhooks — Gmail, Google Sheets, Google Calendar, Google Drive, Jira, Salesforce, and more. Connectors you assign here are never exposed to anonymous embed visitors.

### Step 8: Write Instructions and Guardrails

Scroll down (or open the agent settings) to find the **Instructions** and **Guardrails** fields.

- **Instructions** — tell the agent how to behave. Type `@` to mention a skill or connector inline. Example: *"Always cite your sources when summarizing documents."*
- **Guardrails** — hard limits the agent must never cross. Example: *"Never share customer PII. Never make pricing commitments."*

### Step 9: Chat with your agent

Click **Chat** on the Interact section. The chat screen opens with *Chat with [name]* as the heading and the agent badge pre-selected in the input bar. Type a message and press **Send** — your agent replies using the instructions you wrote.

---

## Tips for a great agent

- **One job, one agent.** A support agent handles tickets; a data agent pulls reports. Mixing purposes leads to confused responses.
- **Be specific in instructions.** "Summarize in bullet points" works better than "keep it short." The AI follows your rules literally.
- **Start with 2–3 skills.** Assign only what the agent actually needs. You can always add more after testing.
- **Test before deploying.** Send a few real-world messages and check that the agent responds the way you expect. Adjust instructions if it drifts off track.

## What's next

- [Add Skills](/documentation/guides/manage-skills) — give your agent the tools it needs
- [Embed your Agent](/documentation/guides/embed-agent) — add it to any website or external app
- [Connect Integrations](/documentation/guides/connect-integration) — link Gmail, Sheets, Jira, and more
- [Agents overview](/documentation/concepts/agents) — understand all the features in one place
