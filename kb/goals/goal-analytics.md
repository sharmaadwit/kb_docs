source_url: https://console-docs.gupshup.io/docs/goal-analytics

<!-- kb-golden:v11 -->
# Goal Analytics

**Module**: Goals

## Definition
- Use **Goal Analytics** to view conversion performance after a goal is implemented in a live bot journey.
- **Goal Analytics** answers questions like:
  - where to see goal conversions
  - whether a goal fired
  - which milestone was achieved
  - how many unique users completed the goal
- If you are asking **“Where do I view goal analytics for CTWA traffic after the campaign goes live?”** -> open **Goals -> Goal Analytics**.

## Procedure
### Exact UI path
Gupshup Console -> Goals -> Goal Analytics

### Steps
1. Open Gupshup Console.
2. Go to **Goals**.
3. Open **Goal Analytics**.
4. Open the target goal from the Goals dashboard using the analytics icon if needed.
5. Select the date range.
6. Review **Goal Achieved**, **Unique Users**, **Trends**, and milestone-level progress.
7. Use **Table View** if you need a tabular trend breakdown.
8. Export milestone-level or goal-level customer data if you need to verify who converted.

### Validation / where to check
- Trigger the goal in a controlled journey test and confirm the goal appears in **Goal Analytics**.
- Check the milestone trend or export data to verify the correct user reached the expected conversion point.
- If the goal should fire from CTWA traffic, confirm the source appears as the expected CTWA / campaign source in the export.

### Save / publish / deploy behavior
- Goal Analytics is a reporting view; there is no save action here.
- If analytics are missing, validate that the upstream **Bot Studio** journey was **Save & Deploy**'d and the goal is implemented on the live path.

### Troubleshooting
- If clicks are happening but no conversions appear, confirm the goal is implemented at the correct journey step, not only defined in Goals.
- If the bot path works but Goal Analytics is empty, re-check the goal node or milestone implementation in the live journey.
- If the wrong step seems to be firing the goal, run a controlled journey test and inspect which milestone count changes in Goal Analytics.
- If data looks stale, re-check the selected date range before assuming the goal did not fire.

### Prerequisites
- A goal already created in **Goals**.
- The goal implemented in the relevant **Bot Studio** journey.
- Live traffic or a test run that can reach the goal step.

## Options / variants
- **Goal Achieved**: number of completed goals.
- **Unique Users**: unique users who completed the goal.
- **Trends**: milestone progress over time.
- **Export**: milestone-level or goal-level customer data.

## Field mapping / schemas
- Exported goal analytics can include:
  - **DateTime**
  - **Customer ID**
  - **Source Type** such as Organic, Marketing, or Click to Chat (CTX)
  - **Source Value** such as conversation ID, campaign ID, or CTWA ad ID

## Cross-module workflow docs
- CTWA / Campaign -> Bot Studio journey -> Goal hit -> Goal Analytics
- Bot Studio live journey -> milestone reached -> Goal Analytics trend / export

## Module disambiguation docs
- **Goal Analytics** is the **Goals** reporting dashboard for conversions.
- **Campaign Analytics** is the **Campaign Manager** dashboard for campaign send, delivery, read, click, and failure metrics.
- **Goal Analytics** tells you whether the intended conversion happened.
- **Campaign Analytics** tells you how the campaign delivery performed.
- **Goal Node** is implemented in **Bot Studio**; it is not the reporting screen.
