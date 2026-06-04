---
title: "Troubleshooting"
description: "Solutions to common issues you might encounter while using SuperAgent."
module: SuperAgent
category: "Help"
slug: "troubleshooting"
---

# Troubleshooting

**Module**: SuperAgent

## Connection Issues

I can't connect an integration

If the authorization popup doesn't appear or closes immediately, try these steps:

- Make sure pop-ups are allowed in your browser for this site
- Try a different browser or clear your browser cache
- Disconnect the integration and try connecting again
- Check that you're using an account that has permission to authorize the service

My integration stopped working

Integrations sometimes need to be re-authorized, especially if a long time has passed or your account permissions changed. Try disconnecting and reconnecting the integration. See [Connect an Integration](/documentation/guides/connect-integration) for the full setup steps.

---

## Chat Issues

The AI isn't using the skill I expect
- Make sure the skill is enabled in your Skills panel
- Try mentioning the skill by name in your message
- Be specific about what you want — vague requests may lead to different tool choices

The AI seems to be stuck or unresponsive

Complex tasks can take a moment. If the AI appears stuck:

- Wait up to 30 seconds for long-running operations
- Use the stop button to cancel the current response
- Start a new conversation if the issue persists
- Refresh the page as a last resort

I got an unexpected or incorrect response
- Try editing your message to be more specific
- Use the version switcher to see alternative responses
- Provide more context about what you need
- If using an agent, review its custom instructions

---

## Skill Issues

A skill says it's missing required configuration

Some skills need additional setup, like connecting to a specific service. Contact the skill owner or check if the skill description mentions any prerequisites.

I can't access a skill

Skills have different access levels. If you see a skill but can't use it, you can request access from the skill owner through the Skills panel. See [Manage Skills](/documentation/guides/manage-skills) for details.

---

## Scheduled Task Issues

My scheduled task didn't run
- Check that the task is not paused
- Verify the schedule timing is correct
- Look at the task's run history for error details
- If using a trigger, make sure the webhook URL was called correctly

For setup help, see [Schedule a Task](/documentation/guides/schedule-task).

A task ran but didn't do what I expected

Review the task prompt — the AI follows it exactly as written. Try making the instructions more specific or adding details about the expected outcome.

---

## Browser Control Issues

The AI can't interact with a website
- Some websites block automated browsing — try a different approach
- If the site requires login, switch to extension mode and log in manually first
- Complex multi-step flows may need to be broken into smaller requests

Learn more about how it works in [Browser Control](/documentation/concepts/browser-control).

---

## Account Issues

I can't sign in
- Make sure you're using a Google account that has been approved for access
- Try clearing your browser cookies and signing in again
- Check if your organization has any restrictions on third-party sign-in

> [!INFO]
> **Still need help?**
> If none of these solutions work, reach out to your team's SuperAgent administrator or check the [FAQ](/documentation/faq) for more answers.
