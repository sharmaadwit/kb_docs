source_url: https://console-docs.gupshup.io/docs/insights-agent-timesheet




<!-- agent-assist-golden:v8 -->
# Insights: Agent Timesheet

**Module**: Agent Assist

## What this feature does
Overview The Agent Timesheet Report provides comprehensive insights into agent activity and time management across four distinct tabs. This guide explains each tab's purpose and its constituent columns.

## Where to configure it
Agent Assist → Insights

## Exact path
Agent Assist → Insights

## Prerequisites
- _List required roles/access, teams, and any upstream configuration._

## Setup path
- Login: Moment when agent signs into the system

## Steps
1. Open Agent Assist.
2. Login: Moment when agent signs into the system

## Save/publish behavior
- _No save/publish step is required for this page unless explicitly stated in the UI._

## Validation
- _Run a quick test (new chat / assignment / workflow) and confirm expected behavior._

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- _Add common failure modes and how to fix them._

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- _Link this feature to adjacent modules (e.g., Business Hours ↔ Auto Replies; Assignment Rules ↔ Teams ↔ Views)._

## Module disambiguation
- _Add 1–2 bullets distinguishing this feature from adjacent settings to reduce retrieval drift._

## Reference (from source)
### Overview
Overview The Agent Timesheet Report provides comprehensive insights into agent activity and time management across four distinct tabs. This guide explains each tab's purpose and its constituent columns.

### When to use
_Add the primary scenarios and personas._

### Details
Overview The Agent Timesheet Report provides comprehensive insights into agent activity and time management across four distinct tabs. This guide explains each tab's purpose and its constituent columns.

Tab 1: Login & Logout Duration This tab tracks the daily login and logout times for each agent. Columns

- Agent Name: The full name of the customer service agent
- Email: Agent's registered email address
- Date: The date of the recorded activity (YYYY-MM-DD format)
- First Login Time: Timestamp of the agent's first login for the day
- Last Logout Time: Timestamp of the agent's final logout for the day
Tab 2: Active & Inactive Time This tab monitors when agents are available or unavailable during their shift.

Columns

- Agent Name: The full name of the customer service agent
- Email: Agent's registered email address
- Date: The date of the recorded activity (YYYY-MM-DD format)
- First Active Time: Timestamp when the agent first became available for customer interactions
- Last Inactive Time: Timestamp when the agent last became unavailable for customer interactions
Tab 3: Overall Activity Time This tab provides a detailed breakdown of agent status changes throughout their shift.

Columns

- Agent Name: The full name of the customer service agent
- Email: Agent's registered email address
- Date: The date of the recorded activity (YYYY-MM-DD format)
- Activity Type: Default status categories including: Available: Agent is ready to handle customer interactions Away: Agent is temporarily unavailable Offline: Agent is not logged into the system Login: Moment when agent signs into the system Logout: Moment when agent signs out of the system
- Available: Agent is ready to handle customer interactions
- Away: Agent is temporarily unavailable
- Offline: Agent is not logged into the system
- Login: Moment when agent signs into the system
- Logout: Moment when agent signs out of the system
- Reason: Specific status message that corresponds to the Activity Type. This can include both default and custom status messages.
Tab 4: Activity Duration Summary This tab summarizes the total time spent in each activity state.

Columns

- Date: The date of the recorded activity (YYYY-MM-DD format)
- Agent Name: The full name of the customer service agent
- Activity Type: The category of activity being measured
- Reason: Specific status message associated with the activity
- Duration (HH:MM:SS): Time spent in the activity state in hours, minutes, and seconds format
- Duration (Hours): Time spent in the activity state expressed in decimal hours
Usage Tips

- Use Tab 1 to monitor attendance patterns and shift adherence
- Use Tab 2 to track agent availability and service coverage
- Use Tab 3 to analyze detailed agent status patterns and behavior
- Use Tab 4 for high-level productivity analysis and time allocation insights
Note All timestamps are recorded in your system's configured timezone. Duration calculations account for the entire time period between status changes.
