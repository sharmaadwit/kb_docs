source_url: https://console-docs.gupshup.io/docs/insights-chat-summary







<!-- agent-assist-golden:v11 -->
# Insights: Chat Summary

**Module**: Agent Assist

## What this feature does
Tab 1: Overall Summary

## Exact UI path
Agent Assist → Insights

## Prerequisites
- Access to the relevant Insights dashboard in Agent Assist.
- Underlying chat/agent activity available for the reporting window you want to inspect.

## Setup path
- _Add the click-path in Console (breadcrumbs)._

## Fields to configure
- No explicit fields were identified in the source; use the controls shown on this page.

## Steps
1. Open Agent Assist.
2. _Add the click-path in Console (breadcrumbs)._

## Validation / where to check
- Confirm the expected data appears in the dashboard/report for a known recent test case or date range.

## Save / publish / deploy behavior
- No save/publish step is required for this page unless explicitly stated in the UI.

## Troubleshooting
- If data looks incomplete, re-check filters/date range and confirm the underlying activity actually occurred.

## Options / variants
- No explicit UI variants/toggles were identified in the source for this page.

## Cross-module workflow docs
- Chats / assignments / resolutions → Insights dashboards

## Module disambiguation docs
- Insights pages are for monitoring/reporting; they do not change live routing or chat behavior.

## Notes
- Important Notes Business Hours vs Calendar Hours Business Hours: Only counts time during operating hours Calendar Hours: Counts all hours continuously (24/7)

## Reference (from source)
### Overview
Tab 1: Overall Summary

### When to use
_Add the primary scenarios and personas._

### Details
Tab 1: Overall Summary

Section 1: Overall Metrics

- Average FRT in Minutes: Mean time taken for first response across all chats
- Average Response Time: Mean time taken to respond to customer messages
- Resolution Time: Average time taken to resolve chats
- Total Chats: Total number of chat conversations
- Unassigned Chats: Number of chats not assigned to any agent
- Resolved Chats: Number of successfully completed conversations
Section 2: Business Hours Metrics

- Total Chats: Number of chats initiated during business hours
- Assigned Chats: Number of chats assigned to agents
- Unassigned Chats: Number of chats pending assignment
- Total Chats Worked Upon: Number of chats where any agent action occurred
- Total Chats - Open Status: Number of currently active chats
- Total Chats Closed/Resolved: Number of completed conversations
- Total Customers: Count of unique customers
- Total Customers Not Responded To: Count of customers who received no response
- Average Wait Duration (Business Hours): Mean waiting time during business hours
- Min Wait Duration (Business Hours): Shortest waiting time during business hours
- Max Wait Duration (Business Hours): Longest waiting time during business hours
- Average Chat Duration: Mean length of chat conversations
- Min Chat Duration: Shortest chat conversation length
- Max Chat Duration: Longest chat conversation length
Section 3: Non-Business Hours Metrics

Same metrics as Section 2, but measured in calendar hours for chats created outside business hours

Tab 2: Chat Trend

Four distinct trend visualizations:

- Hourly Chats Trend Y-axis: Total chat volume X-axis: Created hour Lines: Total worked upon chats Not worked upon chats
- Status-wise Trend Y-axis: Total chats X-axis: Created hour Status Categories: New Open Pending Awaiting Response Resolved Closed
- Daily Chats Trend Y-axis: Total chats X-axis: Created date Lines: Total worked upon Not worked upon
- Priority-wise Trend Y-axis: Total chats X-axis: Created hour Priority Levels: Urgent High Low
Tab 3: Status and Priority Split

Two pie chart visualizations:

Status Distribution: Percentage breakdown of chats by status: New Open Pending Awaiting Response Resolved Closed

Priority Distribution: Percentage breakdown of chats by priority: Urgent High Low

Tab 4: FRT (First Response Time) Summary

Business Hours Metrics

- Min Wait Duration: Shortest time to first response
- Max Wait Duration: Longest time to first response
- Average Wait Duration: Mean time to first response
- Wait Duration Trend: Y-axis: Average wait duration in business hours X-axis: Created hour
Calendar Hours Metrics Same metrics as above but measured in calendar hours (24/7)

Tab 5: Resolution Summary

Business Hours Metrics

- Min Chat Duration: Shortest resolution time
- Max Chat Duration: Longest resolution time
- Average Chat Duration: Mean resolution time Duration Trend: Y-axis: Average chat duration X-axis: Created hour
Calendar Hours Metrics Same metrics as above but measured in calendar hours (24/7)

Tab 6: Response Summary

Business Hours Metrics

- Min Response Time: Shortest time between messages
- Max Response Time: Longest time between messages
- FRT Bucket refers to the different intervals in which the agents have responded
- Average Response Time: Mean time between messages Response Time Trend: Y-axis: Average response time X-axis: Created hour
Calendar Hours Metrics Same metrics as above but measured in calendar hours (24/7)

Important Notes Business Hours vs Calendar Hours Business Hours: Only counts time during operating hours Calendar Hours: Counts all hours continuously (24/7)

Time Measurements All durations are displayed in minutes unless specified otherwise Trends are plotted against creation time/date Wait duration specifically refers to time until first response

Status Definitions New: Fresh unassigned chats Open: Assigned but unresolved Pending: Awaiting internal action Awaiting Response: Waiting for customer reply Resolved: Successfully completed Closed: Administratively completed

Best Practices for Report Usage Use Overall Summary for quick performance snapshots Analyze trends to identify peak hours and resource needs Compare business hours vs calendar hours metrics for service coverage assessment Monitor status distribution for workflow optimization Use priority distribution for resource allocation decisions
