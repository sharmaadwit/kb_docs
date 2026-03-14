source_url: https://console-docs.gupshup.io/docs/insights-team-summary







<!-- agent-assist-golden:v11 -->
# Insights: Team Summary

**Module**: Agent Assist

## What this feature does
Overview The Team Summary Report provides team-level productivity metrics across four specialized tabs: Summary, FRT Summary, Resolution Summary, and Response Summary. Each tab offers insights into different aspects of team performance.

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
- Important Notes

## Reference (from source)
### Overview
Overview The Team Summary Report provides team-level productivity metrics across four specialized tabs: Summary, FRT Summary, Resolution Summary, and Response Summary. Each tab offers insights into different aspects of team performance.

### When to use
_Add the primary scenarios and personas._

### Details
Overview The Team Summary Report provides team-level productivity metrics across four specialized tabs: Summary, FRT Summary, Resolution Summary, and Response Summary. Each tab offers insights into different aspects of team performance.

Tab 1: Summary This tab provides high-level metrics about chat volume and team productivity. Columns

- Team Name: Name of the customer service team
- Total Fresh Chats Assigned: Number of new conversations assigned to the team during the selected period
- Total Chats Worked Upon: Number of conversations where team members performed any action
- Total Chats Completed: Number of conversations successfully resolved by the team
Tab 2: FRT (First Response Time) Summary This tab analyzes the team's initial response speed to customer inquiries, divided into business hours and calendar hours perspectives.

Business Hours Table Measures FRT metrics considering only defined business operating hours:

- Min FRT: Fastest first response time achieved by the team
- Average FRT: Mean time taken by the team to send first responses
- Max FRT: Longest first response time recorded for the team
Calendar Hours Table

- Measures FRT metrics across all hours (24/7):
- Min FRT: Fastest first response time achieved by the team (including non-business hours)
- Average FRT: Mean time taken by the team to send first responses (including non-business hours)
- Max FRT: Longest first response time recorded for the team (including non-business hours)
Tab 3: Resolution Summary This tab tracks how quickly teams resolve customer issues, with separate views for business hours and calendar hours. Business Hours Table Measures resolution metrics during business hours:

- Min Resolution Time: Fastest time taken to resolve a chat
- Average Resolution Time: Mean time taken to resolve chats
- Max Resolution Time: Longest time taken to resolve a chat
Calendar Hours Table Measures resolution metrics across all hours (24/7):

- Min Resolution Time: Fastest resolution time (including non-business hours)
- Average Resolution Time: Mean resolution time (including non-business hours)
- Max Resolution Time: Longest resolution time (including non-business hours)
Tab 4: Response Summary This tab analyzes ongoing conversation response times, separated into business hours and calendar hours views.

Business Hours Table Measures response metrics during business hours:

- Min Response Time: Fastest time taken to respond to customer messages
- Average Response Time: Mean time taken to respond to customer messages
- Max Response Time: Longest time taken to respond to customer messages
Calendar Hours Table Measures response metrics across all hours (24/7):

- Min Response Time: Fastest response time (including non-business hours)
- Average Response Time: Mean response time (including non-business hours)
- Max Response Time: Longest response time (including non-business hours)
Important Notes

- Business Hours vs Calendar Hours Business Hours: Only counts time during defined operating hours Calendar Hours: Counts all hours continuously (24/7)
- Business Hours: Only counts time during defined operating hours
- Calendar Hours: Counts all hours continuously (24/7)
- Time Calculations All time metrics are typically displayed in HH:MM:SS format Business hours calculations exclude non-operating hours Calendar hours calculations include all time periods
- All time metrics are typically displayed in HH:MM:SS format
- Business hours calculations exclude non-operating hours
- Calendar hours calculations include all time periods
- Metric Definitions First Response Time (FRT): Time from chat assignment to first agent response Resolution Time: Time from chat start to successful completion Response Time: Time between customer message and agent response Best Practices for Report Usage Compare business hours and calendar hours metrics to understand impact of operating hours Use Summary tab for quick team performance overview Use detailed timing tabs (FRT, Resolution, Response) for in-depth analysis Consider seasonal and time-zone impacts when analyzing metrics Use these metrics for: Team performance evaluation Resource allocation decisions Identifying training needs Setting team goals and benchmarks
- First Response Time (FRT): Time from chat assignment to first agent response
- Resolution Time: Time from chat start to successful completion
- Response Time: Time between customer message and agent response Best Practices for Report Usage
- Compare business hours and calendar hours metrics to understand impact of operating hours
- Use Summary tab for quick team performance overview
- Use detailed timing tabs (FRT, Resolution, Response) for in-depth analysis
- Consider seasonal and time-zone impacts when analyzing metrics
- Use these metrics for: Team performance evaluation Resource allocation decisions Identifying training needs Setting team goals and benchmarks
- Team performance evaluation
- Resource allocation decisions
- Identifying training needs
- Setting team goals and benchmarks
