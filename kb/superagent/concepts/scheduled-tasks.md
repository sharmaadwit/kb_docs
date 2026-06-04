---
title: "Scheduled Tasks"
description: "Automate recurring work with scheduling and triggers"
module: SuperAgent
category: "Core Fundamentals / Scheduled Tasks"
slug: "concepts/scheduled-tasks"
---

# Scheduled Tasks

**Module**: SuperAgent

Scheduled tasks are automated tasks that run at set times or when triggered—without you having to start them manually. You define what the AI should do, when it should run, and optionally whether you want to approve each run before it executes.

> [!INFO]
> **Note on agent-owned tasks**
> Some tasks are created by an agent automation (for example, an agent running hourly or via webhook). Those tasks are managed from the agent itself (open the agent → Automations). In Settings → Scheduled Tasks, they may appear as “Created by micro agent” and can’t be edited there.

## What are scheduled tasks?

Instead of asking the AI to do the same thing every day or every week, you create a scheduled task once. The AI then runs automatically on the schedule you set—for example, a daily email summary, a weekly report, or a reminder to check something. You can also trigger tasks via a webhook URL, so external systems can start an AI task when something happens.

## Two types of tasks

- **Schedule** — Runs at specific times. You choose the frequency: daily, weekly, or a custom pattern. The task runs automatically at the configured time (e.g., every Monday at 9 AM or every day at noon).
- **Trigger** — Runs when you call a webhook URL. You get a unique URL; when that URL is requested (e.g., from another app, a form, or a manual click), the task runs. Useful for event-driven workflows like "when a form is submitted" or "when a build completes."

## What you configure

When creating a scheduled task, you set:

- **Prompt** — What the AI should do. Describe the task in plain language, just like a chat message (e.g., "Summarize my unread emails from today and send the summary to my team channel").
- **Schedule or trigger** — For schedule tasks: when it runs (daily, weekly, etc.). For trigger tasks: the webhook URL is generated for you.
- **Confirmation** — Optional. If enabled, the AI will wait for your approval before executing each run. You can review the planned actions and approve or skip.

## Viewing task run history

Each task keeps a history of its runs. You can see when it ran, whether it succeeded, and what it did. This helps you verify that automation is working as expected and troubleshoot if something goes wrong.

## Pausing and resuming

You can pause a task at any time. When paused, it won't run on its schedule or respond to triggers until you resume it. Useful when you're on vacation, changing the task, or temporarily don't need the automation.

> [!TIP]
> **Start simple**
> Begin with a simple task—like a daily summary—to see how it works. Once you're comfortable, add more complex prompts or use triggers for event-driven workflows.

## Example tasks

- **Daily email digest** — "Every morning at 8 AM, summarize my unread emails and send the summary to my WhatsApp."
- **Weekly analytics report** — "Every Monday at 9 AM, pull data from my Google Sheet, generate a chart, and email it to my team."
- **CI/CD webhook** — Trigger a task via webhook when your build pipeline finishes to summarize results and post them to a channel.
- **Meeting prep** — "Every weekday at 8:30 AM, check my calendar and send me a summary of today's meetings with relevant context."

## What's next?

- [Schedule a Task](/documentation/guides/schedule-task) — Step-by-step setup guide
- [Integrations](/documentation/concepts/integrations) — Connect the services your tasks will use
- [Use Messaging Channels](/documentation/guides/use-channels) — Receive task results on WhatsApp or Telegram
