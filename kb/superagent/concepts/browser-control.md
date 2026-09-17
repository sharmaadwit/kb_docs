---
title: "Browser Control"
description: "Let agents navigate the web, fill forms, and interact with websites on your behalf"
module: SuperAgent
category: "Core Fundamentals / Browser Control"
slug: "concepts/browser-control"
---

# Browser Control

**Module**: SuperAgent

Browser Control lets your AI assistant navigate web pages, click elements, fill forms, and take screenshots—as if it were using a browser for you. When a task requires interacting with a website that doesn't have an integration, Browser Control steps in.

## What is Browser Control?

Browser Control gives the AI the ability to see and interact with web pages. It can open URLs, click buttons, type into fields, scroll, and capture what's on screen. The AI decides what to do based on your request and what it sees—for example, filling out a form, checking a status page, or gathering information from a site.

## Two modes

You can use Browser Control in two ways:

- **Headless mode** — Uses a built-in browser that runs in the background. Good for tasks that don't require you to see the page or be logged in. The AI works independently without opening a visible window.
- **Extension mode** — Uses your Chrome browser via a SuperAgent extension. The AI controls your actual browser tab. Best when you need to be logged in (e.g., a site that requires your credentials) or when you want to watch the AI work in real time.

## When to use it

Browser Control is useful for web-based tasks the AI can't do through an integration. For example:

- Filling out a form on a website that has no API
- Checking a status or result on a page you use
- Gathering information from multiple pages
- Interacting with tools that only exist in a browser

If a service has an integration (like Gmail or Jira), use that instead—it's faster and more reliable.

## How it works

At a high level, the AI sees the page structure, decides what to click or type, and takes actions. It can take screenshots to verify what's on screen and adjust its approach if something doesn't look right. You describe the task; the AI figures out the steps.

## Safety and control

You stay in control. You can pause the AI, take over manually, or stop a task at any time. Browser Control doesn't run without your permission—you choose when to enable it and which mode to use.

> [!NOTE]
> **Sites that require login**
> Some sites require you to log in first. In extension mode, you can log in yourself, then hand control back to the AI. The AI will work within your logged-in session. For headless mode, the AI can only access public pages or sites that don't require authentication.

## Real-world examples

- **Fill out a web form** — "Go to our internal request portal and submit a new laptop request with these details."
- **Check a status page** — "Visit the deployment dashboard and tell me if the latest build passed."
- **Scrape public data** — "Open this product page and extract the price and availability."
- **Automate repetitive clicks** — "Go to our analytics tool, export the weekly report as CSV, and summarize the key numbers."

## What's next?

- [Enable Browser Agent](/documentation/guides/enable-browser-agent) — Step-by-step guide to turn on browser control
- [Integrations](/documentation/concepts/integrations) — Use direct connections for supported services (faster and more reliable)
- [Create Agents](/documentation/guides/create-agent) — Build an agent with browser capabilities
