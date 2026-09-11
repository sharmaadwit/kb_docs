> Source: https://console-docs.gupshup.io/docs/goal-analytics
> Last updated: 2026-09-11

After creating a Goal and implementing within a journey, you can track it through **Goal Analytics**.

You can access Goal Analytics for a Goal by clicking the Analytics (pie chart) icon on the Goals Dashboard.

<Image alt="Analytics icon can be seen when you hover on the Goal" align="center" border={true} src="https://files.readme.io/de10a89473f2b2cf7a690e914050b5d115b9be4402269180fd4a9b1b5f0e4a75-Screenshot_2025-04-22_092536.png">
  Analytics icon appears when you hover on the Goal
</Image>

## Goal Metrics & Visualizations

<Image alt="Goal Analytics" align="center" border={true} src="https://files.readme.io/0987aaef5d5d2e7561ea0f8c3c2d139c9860aaba2cec1be0a32f534b795c04be-Screenshot_2024-12-03_181207.png">
  Goal Analytics
</Image>

* The name and description of the Goal are present at the top of the screen.
* You can select the time period for your Goal's analytics using the start date and end date filters.
  * By default, Goal Analytics is displayed for the last 7 days.
* **Goal Achieved** represents the number of times all Milestones of that Goal were achieved.
* **Unique Users** represents the number of unique customer IDs that achieved all Milestones of that Goal.
* By default, **Trends** is a line graph that displays the time-interval spaced progress of the Milestones being achieved.
  * Each Milestone is represented by a separate line in the graph.
  * Hovering on the graph will display the exact count of each Milestone for that particular time interval.
* The data in **Trends** will be displayed in terms of Unique Users by choosing the "Unique Users" option from the **Type** dropdown.
  * "Achieved" representing Milestone Achieved is selected by default in the dropdown.
* You can view **Trends** data in a tabular format by switching the on the **Table View** toggle.

<Image alt="Trends - Table View" align="center" border={true} src="https://files.readme.io/cc709d777a158e0fb38da460d961568e8ed009caa7c194f5dd9242309db9f5bc-Screenshot_2024-12-03_181318.png">
  Trends - Table View
</Image>

* The Milestones table displays the **Achieved** & **Unique Users** counts of individual Milestones and their Trackers.
  * **Achieved** represents the number of times the Milestone was achieved.
  * **Unique Users** represents the number of unique customer IDs that achieved the Milestone.

<Image alt="Milestones Table" align="center" border={true} src="https://files.readme.io/6d61c34458e105e2a0c7e4ed26d854286bd63f6330d4070a22a0d25f5e7cc7c4-Screenshot_2024-12-03_181359.png">
  Milestones Table
</Image>

## Exporting Customer Data from Goal Analytics

### Milestone Level

* The **Export** option next to each Milestone provides an Excel file containing a list of all values entered by users for the Trackers of that Milestone.
* The Excel file has the following columns:
  * **DateTime** displays the timestamp when the milestone was achieved.
  * **Customer ID** displays the unique identifier of the customer on that channel. For example, phone number is the Customer ID for the WhatsApp channel.
  * **Source Type** displays the source of the conversation - Organic, Marketing or Click to Chat (CTX). 
  * **Source Value** displays the Organic Conversation ID, the Marketing Campaign ID, or the Click to Chat Ad ID.
* A column will be present for each Tracker with the Tracker Name as the column header and Tracker Values below it.
  * All Tracker Values entered by a user for a single Milestone will appear in the same row.

<Image alt="Downloaded tracker data" align="center" border={true} src="https://files.readme.io/11a919b9afa7577c93308e3a1f7e3b821de632f3e4bf1010f66abfcda16b09c8-Tracker_Data_Sheet_2.png">
  Downloaded Excel sheet sample
</Image>

> 🚧 If a Milestone is skipped and a Milestone after it in the sequence of creation is achieved, the Tracker Values for that milestone are automatically filled with the respective Default Values against the user’s customer ID.
>
> For example, if a user achieves the third Milestone without achieving the first and second Milestones, the respective Default Values are set as Tracker Values entered by that user in the first and second Milestones.

### Goal Level

* The **Export** button at the top right of the Goal Analytics page provides an Excel file containing a list of all values entered by users for the Trackers of all Milestones present in the Goal.
* Customer data from each Milestone is present in the Excel in a separate sub-sheet titled with the sequence number of the Milestone and the Milestone Name.
  * For example, if the Milestone named "Qualified Lead" is 2nd in the sequence of Milestones within the Goal, the sub-sheet will be titled "2. Qualified Lead".
* The aggregate data from the Trends table is also present in a separate sub-sheet titled "Trends".