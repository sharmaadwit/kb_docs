source_url: https://console-docs.gupshup.io/docs/insights-agent-summary




<!-- agent-assist-golden:v8 -->
# Insights: Agent Summary

**Module**: Agent Assist

## What this feature does
Overview The Agent Summary Report provides comprehensive productivity metrics for agent performance in handling customer interactions. This report helps measure efficiency, response times, and service level adherence.

## Where to configure it
Agent Assist → Insights

## Exact path
Agent Assist → Insights

## Prerequisites
- _List required roles/access, teams, and any upstream configuration._

## Setup path
- _Add the click-path in Console (breadcrumbs)._

## Steps
1. Open Agent Assist.
2. _Add the click-path in Console (breadcrumbs)._

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
Overview The Agent Summary Report provides comprehensive productivity metrics for agent performance in handling customer interactions. This report helps measure efficiency, response times, and service level adherence.

### When to use
_Add the primary scenarios and personas._

### Details
Overview The Agent Summary Report provides comprehensive productivity metrics for agent performance in handling customer interactions. This report helps measure efficiency, response times, and service level adherence.

Available Filters

- Time-based Filters Date: Select specific dates for analysis Time Duration: Choose specific time periods within days
- Date: Select specific dates for analysis
- Time Duration: Choose specific time periods within days
- Organizational Filters Team: Filter by specific team assignments Agent: Filter by individual agent names Status: Filter by chat status (e.g., open, closed, reassigned)
- Team: Filter by specific team assignments
- Agent: Filter by individual agent names
- Status: Filter by chat status (e.g., open, closed, reassigned)
- Interaction Filters Priority: Filter by chat priority levels
- Priority: Filter by chat priority levels
Metrics Definitions Volume Metrics

- Chats Assigned: Total number of chat conversations allocated to an agent during the selected time period
- Chats Closed: Total number of chat conversations successfully resolved and closed by the agent
- Chats Worked Upon: Number of conversations where the agent performed at least one action (e.g., sending a message)
- Chats Reassigned: Number of conversations transferred or reassigned to other agents
- Customers Handled: Unique count of customers the agent interacted with
- Responded Chats: Number of conversations where the agent sent at least one message
- First Response Time (FRT) Metrics Average FRT: Mean time taken by an agent to send their first response after a chat is assigned MAX FRT: Longest time taken by an agent to send their first response Min FRT: Shortest time taken by an agent to send their first response
- Average FRT: Mean time taken by an agent to send their first response after a chat is assigned
- MAX FRT: Longest time taken by an agent to send their first response
- Min FRT: Shortest time taken by an agent to send their first response
- Average Response Time (ART) Metrics Average Response Time: Mean time taken by an agent to respond to customer messages throughout the conversation Max Response Time: Longest time taken to respond to a customer message Min Response Time: Shortest time taken to respond to a customer message
- Average Response Time: Mean time taken by an agent to respond to customer messages throughout the conversation
- Max Response Time: Longest time taken to respond to a customer message
- Min Response Time: Shortest time taken to respond to a customer message
- Resolution Time (RT) Metrics Average Resolution Time: Mean time between chat assignment and resolution Max Resolution Time: Longest time taken to resolve a chat Min Resolution Time: Shortest time taken to resolve a chat
- Average Resolution Time: Mean time between chat assignment and resolution
- Max Resolution Time: Longest time taken to resolve a chat
- Min Resolution Time: Shortest time taken to resolve a chat
- Handling Time Metrics AHT (Average Handling Time): Mean duration a chat remains in open status before being reassigned or resolved Max Handling Time: Longest duration a chat remained in open status Min Handling Time: Shortest duration a chat remained in open status
- AHT (Average Handling Time): Mean duration a chat remains in open status before being reassigned or resolved
- Max Handling Time: Longest duration a chat remained in open status
- Min Handling Time: Shortest duration a chat remained in open status
- Service Level Agreement (SLA) Metrics SLA Breach - FRT %: Percentage of chats where the First Response Time exceeded the defined SLA threshold SLA Breach ART %: Percentage of chats where the Average Response Time exceeded the defined SLA threshold SLA Breach RT %: Percentage of chats where the Resolution Time exceeded the defined SLA threshold
- SLA Breach - FRT %: Percentage of chats where the First Response Time exceeded the defined SLA threshold
- SLA Breach ART %: Percentage of chats where the Average Response Time exceeded the defined SLA threshold
- SLA Breach RT %: Percentage of chats where the Resolution Time exceeded the defined SLA threshold
Calculation Notes

- All time-based metrics are calculated in minutes unless otherwise specified
- Percentage metrics are rounded to two decimal places
- SLA breaches are calculated based on configured thresholds for each metric
- Average metrics exclude outliers beyond the 99th percentile to ensure accuracy
Best Practices for Report Usage

- Use date filters to analyze trends over specific time periods
- Compare team-level metrics to identify performance patterns
- Monitor SLA breach percentages to maintain service quality
- Track resolution times alongside response times for complete performance assessment
- Use tag filters to analyze performance for specific types of interactions
Common Use Cases

- Agent Performance Review: Compare individual metrics against team averages
- Quality Monitoring: Track SLA compliance and response times
- Workload Analysis: Evaluate chat distribution and reassignment patterns
- Training Needs Assessment: Identify areas for improvement based on handling times
- Resource Planning: Use volume metrics to optimize agent scheduling
