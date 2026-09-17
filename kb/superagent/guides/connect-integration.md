---
title: "Connect an Integration"
description: "Link your tools and services so the AI can work with your data"
module: SuperAgent
category: "Core Fundamentals / Integrations"
slug: "guides/connect-integration"
---

# Connect an Integration

**Module**: SuperAgent

> [!NOTE]
> **Prerequisites · ~2 minutes**
> You need a SuperAgent account and access to the service you want to connect (e.g., a Google account for Gmail, Sheets, Calendar, Drive, or Docs).

Integrations let SuperAgent access your Gmail, Google Sheets, Calendar, Drive, Google Docs, Jira, and other services. Once connected, you can ask the AI to read emails, update spreadsheets, manage files and documents, create calendar events, and more.

## See it in the app

The **integrations** menu opens from the chat input toolbar (same layout as the real app). The walkthrough shows Connect, then the On/Off toggle after you connect.

### Step 1: Open the integrations menu from the chat input toolbar

In the chat screen, use the **integrations** control in the input bar (next to attach, skills, and other shortcuts). Click it to open the integrations menu above the input.

### Step 2: Choose a service and click Connect

In the menu, you'll see available services—Gmail, Google Sheets, Google Calendar, Google Drive, Google Docs, Jira, and others. Click the service you want, then click the **Connect** button on that row.

### Step 3: Authorize in the browser popup

A browser popup will open asking you to sign in to the service and grant SuperAgent permission. Sign in with your account and approve the requested access. When you're done, the popup closes and the integration shows as connected.

### Step 4: Use the On/Off toggle to enable or disable

Once connected, the row shows an **On** / **Off** toggle. You can turn the integration on or off without disconnecting—useful to temporarily pause access. When on, you can ask the AI to use that service (e.g. "Show my unread emails" or "Add a row to my spreadsheet").

---

## Managing your integrations

### Enabling and disabling

You can turn an integration on or off without disconnecting it. When disabled, the AI won't use that service until you enable it again. This is useful if you want to keep the connection but temporarily pause access.

### Disconnecting

To fully remove an integration, go back to the integrations area and click "Disconnect" for that service. This revokes SuperAgent's access. You can reconnect anytime by following the same steps above.

### Troubleshooting connection issues

- **Popup blocked** — If the authorization popup doesn't appear, check your browser's popup blocker. Allow popups for SuperAgent and try again.
- **Connection failed** — Make sure you completed the sign-in and approval in the popup. If you closed it early, the connection may not have finished. Try connecting again.
- **Permission denied** — Some services require specific permissions. If the AI can't perform an action, you may need to reconnect and grant additional access when prompted.

> [!WARNING]
> **Security**
> SuperAgent only accesses what you authorize. You can disconnect any integration at any time to revoke access.

## What's next?

- [Create Agents](/documentation/guides/create-agent) — Build an agent that uses your connected integrations
- [Schedule a Task](/documentation/guides/schedule-task) — Automate tasks that use your integrations on a recurring basis
- [Manage Skills](/documentation/guides/manage-skills) — Enable additional capabilities for your AI
