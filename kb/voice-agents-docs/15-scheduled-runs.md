---
title: Scheduled Runs
description: Automated recurring test run scheduling via cron expressions
source: https://voiceagents.gupshup.io/developer-docs
---

# Scheduled Runs

## Scheduled Test Runs

The Scheduled Runs page automates agent evaluation on a recurring cron-based schedule, enabling continuous quality monitoring without manual intervention.

## Schedule Table Columns

| Column | Description |
|---|---|
| Name | Descriptive schedule identifier (e.g., 'morning_check', 'swiggy_daily_run') |
| Agent ID | The agent targeted by this scheduled evaluation |
| Scenarios | Number of test scenarios included. Click the badge to view or edit the linked scenario set. |
| Schedule | Human-readable cron expression (e.g., 'Every day at 9 AM') |
| Last Run | Timestamp of the most recent scheduled execution |
| Enabled | Toggle to activate or suspend the schedule without deleting it |
| Actions | Delete icon to permanently remove the schedule |

## Creating a Scheduled Run

1. Click + New Schedule (top right)

2. Enter a descriptive Name for the schedule

3. Specify the Agent name to be tested

4. Select the test Scenarios to include in each run

5. Define the Schedule using a cron expression (e.g., '0 9 * * *' for daily at 9 AM)

6. Toggle Enabled to ON to activate the schedule immediately
