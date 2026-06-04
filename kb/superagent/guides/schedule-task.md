---
title: "Schedule a Task"
description: "Set up automated and recurring tasks for the AI to run"
module: SuperAgent
category: "Core Fundamentals / Scheduled Tasks"
slug: "guides/schedule-task"
---

# Schedule a Task

**Module**: SuperAgent

> [!NOTE]
> **Prerequisites · ~3 minutes**
> You need a SuperAgent account. For tasks that use integrations (e.g., sending emails or updating sheets), [connect them first](/documentation/guides/connect-integration).

Scheduled tasks let the AI run automatically—on a schedule (daily, weekly) or when triggered by an event. Follow these steps to create your first scheduled task.

> [!INFO]
> **If you’re scheduling an agent**
> If you want a specific agent to run on a schedule or from a webhook, create an automation from that agent (open the agent → Automations). This guide is for tasks created from Settings → Scheduled Tasks.

## See it in the app

### Step 1: Open Settings from the sidebar

Click **Settings** in the sidebar footer (the user area at the bottom of the sidebar). The Settings modal opens with Profile, Channels, Scheduled Tasks, and Credits tabs.

### Step 2: Click the Scheduled Tasks tab

In the left navigation of the Settings modal, click **Scheduled Tasks**. You'll see the **Scheduled** and **Completed** tabs, along with a **+ New Task** button.

### Step 3: Click + New Task to open the form

Click **+ New Task** in the top-right corner. The Create Task form appears with fields for Title, Task Prompt, and scheduling options.

### Step 4: Fill in the Create Task form and set schedule

Enter a **Title** and describe what the AI should do in the **Task Prompt**. Choose **Schedule** (with Repeat, Date, and Time) or **Trigger** (webhook). Click **Create Task** to save.

### Step 5: View the Completed tab

Switch to the **Completed** tab to see finished tasks and their execution history. You can edit, pause, resume, or delete tasks anytime from the Scheduled tab.

---

## Tips for scheduled tasks

- Keep prompts clear and specific so the AI knows exactly what to do.
- Use confirmation for tasks that make changes (e.g., sending emails) until you're comfortable.
- Check the run history to see if tasks completed successfully and adjust as needed.

> [!WARNING]
> **Be careful**
> Scheduled tasks run automatically. Avoid prompts that could cause unintended side effects—for example, sending messages to many people or deleting data—unless you've tested them first.

## What's next?

- [Connect an Integration](/documentation/guides/connect-integration) — Link services so your scheduled tasks can access them
- [Create Agents](/documentation/guides/create-agent) — Build a dedicated agent for your automated workflows
