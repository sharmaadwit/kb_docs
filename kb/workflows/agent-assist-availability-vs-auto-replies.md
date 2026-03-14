source_url: https://console-docs.gupshup.io/docs/user-management-business-hours

<!-- kb-golden:v10 -->
# Agent Assist Availability Vs Auto Replies

**Module**: Workflows

## Definition
Use this workflow when you need to decide:
- **where agent availability is defined**
- **where the after-hours / offline message is configured**

Business Hours determines **when** a team is considered available. Auto Replies determines **what message or workflow fires** when agents are offline, busy, or outside business hours.

## Procedure
### Exact UI path
Agent Assist → Settings → User Management → Business Hours
Agent Assist → Settings → Response Management → Auto Replies

### Prerequisites
- Access to **Agent Assist → Settings**.
- The target **team** already exists.
- A test chat path is available so you can validate business-hours vs after-hours behavior.
- If you plan to use **Handover to Bot**, the bot flow must already be available.

### Fields to configure
- **Business Hours**: team, timezone, working days/hours, holidays
- **Auto Replies**: scenario, message text, business-hours vs after-hours variant
- **Optional**: Handover to Bot for offline scenarios

### Steps
1. Open **Agent Assist**.
2. Go to **Settings → User Management → Business Hours**.
3. Create or update the business hours for the target team, including timezone and daily schedule.
4. Click **Save**.
5. Go to **Settings → Response Management → Auto Replies**.
6. Open the relevant offline scenario such as **Responses When Agents Are Offline**.
7. Configure the message for:
8. **Offline/busy during business hours** if agents are unavailable during configured hours.
9. **Not available outside business hours** if the chat arrives after-hours.
10. Optionally enable **Handover to Bot** for the offline scenario.
11. Click **Save**.

### Validation / where to check
- Test one chat **during configured business hours** and confirm the after-hours message does **not** fire unless the agents are actually unavailable/busy.
- Test one chat **outside configured business hours** and confirm the **after-hours** reply fires.
- If handover is enabled, confirm the chat moves to the expected bot experience only in the intended offline scenario.

### Troubleshooting
- If customers see the **after-hours** reply while agents are online, re-check the **team timezone**, working hours, and holiday schedule in **Business Hours**.
- Confirm you edited the correct Auto Replies variant: **during business hours** vs **outside business hours**.
- Validate on a **new incoming chat** after saving; existing conversations may not reflect the updated setup.
- If only one team is affected, confirm the correct team is mapped to the intended business hours configuration.

### Save / publish / deploy behavior
- Click **Save** in **Business Hours** after changing availability windows.
- Click **Save** in **Auto Replies** after changing message behavior.
- Validate on **new incoming chats** after both changes are saved.

## Options / variants
- **Offline/busy during business hours**
- **Not available outside business hours**
- **Handover to Bot**

## Cross-module workflow docs
- User Management → Business Hours → Response Management → Auto Replies → Chats
- Team availability setup → offline/after-hours message behavior → customer-visible outcome

## Module disambiguation docs
- **Business Hours** controls **when** the team is available.
- **Auto Replies** controls **what the customer sees** for that availability state.
- If the problem is “wrong message fired,” check **Auto Replies**.
- If the problem is “wrong availability window fired,” check **Business Hours**.

## Reference (from source)
- Business Hours: `kb/agent-assist/user-management-business-hours.md`
- Auto Replies: `kb/agent-assist/response-management-auto-replies-and-customer-satisfaction.md`
