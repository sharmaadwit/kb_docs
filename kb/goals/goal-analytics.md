source_url: https://console-docs.gupshup.io/docs/goal-analytics

<!-- kb-golden:v12 -->
# Goal Analytics

**Module**: Goals

## Definition
- After creating a Goal and implementing it within a journey, you can track it through `Goal Analytics`.
- You can access Goal Analytics for a goal by clicking the analytics icon on the Goals dashboard.

## Procedure
### Exact UI path
Gupshup Console -> Goals -> Goal Analytics

### Steps
1. Open Gupshup Console.
2. Go to **Goals**.
3. Open **Goal Analytics**.
4. Click the analytics icon for the target goal from the Goals dashboard.
5. Select the date range.
6. Review `Goal Achieved`, `Unique Users`, and `Trends`.
7. Use `Table View` if you need trends in tabular format.
8. Use export if you need customer data for milestones or the full goal.

### Validation / where to check
- Check the graph hover state to view the exact count of each milestone for the selected time interval.
- Check the milestones table for `Achieved` and `Unique Users` counts of individual milestones and their trackers.
- Use the export file if you need milestone-level customer data.

### Save / publish / deploy behavior
- Goal Analytics is a reporting view; no save action is described on this page.

### Prerequisites
- A goal already created in **Goals**.
- The goal implemented within a journey.

## Options / variants
- `Trends` can be viewed in graph format or with the `Table View` toggle.
- `Achieved` is selected by default in the dropdown.
- `Type` can be changed to `Unique Users`.
- Export is available at `Milestone Level` and `Goal Level`.

## Field mapping / schemas
- Exported goal analytics can include:
  - **DateTime**
  - **Customer ID**
  - **Source Type** such as Organic, Marketing, or Click to Chat (CTX)
  - **Source Value** such as conversation ID, campaign ID, or CTWA ad ID
  - Tracker columns with tracker names and tracker values

## Cross-module workflow docs
- CTWA / Campaign -> Bot Studio journey -> Goal hit -> Goal Analytics
- Bot Studio live journey -> milestone reached -> Goal Analytics trend / export

## Module disambiguation docs
- **Goal Analytics** is the **Goals** reporting dashboard for conversions.
- **Campaign Analytics** is the **Campaign Manager** dashboard for campaign send, delivery, read, click, and failure metrics.
- **Goal Analytics** shows goal and milestone achievement data.
- **Goal Node** is implemented in **Bot Studio**; it is not the reporting screen.
