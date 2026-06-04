---
title: "Enable Browser Agent"
description: "Turn on browser control so the AI can navigate websites for you"
module: SuperAgent
category: "Core Fundamentals / Browser Control"
slug: "guides/enable-browser-agent"
---

# Enable Browser Agent

**Module**: SuperAgent

> [!NOTE]
> **Prerequisites · ~2 minutes**
> You need a SuperAgent account. For extension mode, you also need Google Chrome.

Browser control lets the AI open web pages, click buttons, fill forms, and take screenshots. Follow these steps to enable it.

## See it in the app

## Choose a mode

SuperAgent offers two browser modes. Pick the one that fits your task:

- **Headless mode** — The AI uses a built-in browser that runs in the background. Good for public pages and tasks where you don't need to be logged in. No setup required.
- **Extension mode** — The AI controls your actual Chrome tab via the SuperAgent extension. Use this when the site requires your login session or you want to watch the AI work.

## Enable headless mode

### Step 1: Open a chat

Go to any chat — the main chat or an agent conversation.

### Step 2: Turn on Browser Control

In the chat input toolbar (below the message box), find the **Browser Control** toggle and switch it on. The AI can now open pages and interact with websites in headless mode.

### Step 3: Ask the AI to browse

Type a request like "Go to example.com and tell me what's on the page" or "Search Google for quarterly revenue reports." The AI will navigate, interact, and report back.

## Enable extension mode

### Step 1: Install the SuperAgent Chrome extension

Install the [Gupshup SuperAgent extension]((props) => ({
  type: 'icon',
  props: {
    name: 'icon'
  }
})) from the Chrome Web Store. Once installed, you'll see the SuperAgent icon in your browser toolbar.

### Step 2: Connect the extension

Click the SuperAgent extension icon and sign in with the same account you use in the web app. The extension links to your SuperAgent session automatically.

### Step 3: Switch to extension mode in the chat

In the chat input toolbar, turn on **Browser Control**, then select **Extension** as the mode. The AI will now control your actual Chrome tab instead of a background browser.

### Step 4: Try a task

Ask something like "Go to my Jira dashboard and list the open tickets." Since the extension uses your logged-in session, the AI can access pages that require authentication.

> [!TIP]
> **When to use which mode**
> Use **headless** for quick lookups on public sites. Use **extension** when the task needs your login or you want to watch the AI's actions in real time.

## What's next?

- [Browser Control Overview](/documentation/concepts/browser-control) — Learn more about how browser automation works
- [Create Agents](/documentation/guides/create-agent) — Build an agent with browser capabilities
- [Schedule a Task](/documentation/guides/schedule-task) — Automate browser-based workflows on a schedule
