source_url: https://console-docs.gupshup.io/docs/user-management-business-hours






<!-- agent-assist-golden:v10 -->
# User Management: Business Hours

**Module**: Agent Assist

## What this feature does
Agent Assist simplifies chat assignment by creating default business hours when a brand is established. The default business hours are set to operate 24 hours a day, 7 days a week. They are pre-mapped to the default team within the system. This means that as soon as agents are added to the platform, chats begin to be automatically assigned to them, ensuring a prompt response to customer inquiries.

If you’re asking **“Where do I configure Business Hours for agent availability?”** → open **Agent Assist → Settings → User Management → Business Hours**.

Business Hours define **agent availability windows** (working hours) used by Agent Assist for assignment/availability behavior.

## Exact UI path
Agent Assist → Settings → User Management → Business Hours

## Setup path
- Go to **Settings**.
- Open **User Management**.
- Click **Business Hours**.

## Steps
1. Open Agent Assist.
2. Go to **Settings → User Management → Business Hours**.
3. Click **Add New**.
4. Configure the business hours name, timezone, and working days/hours.
5. Add holidays if those days should be treated as non-working hours.
6. Click **Save**.

## Validation / where to check
- Confirm the team is considered **available** during the configured window.
- Test a chat during business hours vs outside business hours and confirm assignment/behavior matches expectations.

## Fields to configure
- **Business hours name**
- **Timezone**
- **Working days / hours**
- **Holiday / non-working days**

## Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy** if available) to apply changes.

## Troubleshooting
- If chats behave as if the team is offline at the wrong time, re-check the **timezone** and holiday schedule.
- If only some chats are affected, confirm the correct **team** is linked to the expected business hours setup.
- If the wrong customer message fires, also check **Auto Replies** because Business Hours controls availability, not message content.

## Prerequisites
- Access to **Agent Assist → Settings → User Management**.
- The target **team** already exists.

## Options / variants
- Create a **new** business hours schedule
- Add **holidays / non-working days**

## Cross-module workflow docs
- Business Hours → Auto Replies / after-hours customer messaging
- Business Hours → Assignment / team availability behavior

## Module disambiguation docs
- **Business Hours** decides **when** a team is considered available.
- **Auto Replies** decides **what the customer sees** for that availability state.
- **Teams** defines membership/assignment policy; it does not define the working-hour schedule by itself.

## Reference (from source)
### Overview
Section 1: Business Hours Configuration

### When to use
_Add the primary scenarios and personas._

### Details
Section 1: Business Hours Configuration

Defining Team Working Hours

Agent Assist simplifies chat assignment by creating default business hours when a brand is established. The default business hours are set to operate 24 hours a day, 7 days a week. They are pre-mapped to the default team within the system. This means that as soon as agents are added to the platform, chats begin to be automatically assigned to them, ensuring a prompt response to customer inquiries.

This setup enhances efficiency and ensures that your team can handle customer interactions effectively right from the start.

Business hours allow you to set working hours for teams of agents, enabling the system to assign chats based on these hours. Here's how to set up business hours:

- Go to settings and click on "Business Hours."
- Click "Add New" to configure business hours, including naming, time zone, and daily hours.
- You can also include holidays to automatically designate those days as non-working hours.
With business hours in place, you can ensure chats are assigned to agents during their operational hours, enhancing efficient chat management.
