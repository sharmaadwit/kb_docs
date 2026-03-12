source_url: https://console-docs.gupshup.io/docs/website-re-training-scheduler

<!-- kb-golden:v4 -->
# Website Re-training Scheduler (Developer Mode)

**Module**: Ai Admin

## Definition
Introduction: The Website Re-Training Scheduler is a powerful feature designed to automate the process of re-training your website URLs, significantly reducing manual content training efforts. This is particularly beneficial for businesses that frequently update their online content, ensuring your AI models are always up-to-date with the latest information.

## Procedure
### Exact path
Gupshup Console → Ai Admin → Website Re-training Scheduler (Developer Mode)

### Where to configure it
Gupshup Console → Ai Admin → Website Re-training Scheduler (Developer Mode)

### Prerequisites
- _List required access, assets, and upstream setup needed before configuration._

### Setup path
- _Add the click-by-click navigation path for this page._

### Steps
1. Open Gupshup Console.
2. Navigate to **Gupshup Console → Ai Admin → Website Re-training Scheduler (Developer Mode)**.
3. Configure the required fields.
4. Click **Save** (or **Save & Deploy**) to apply changes.

### Save/publish behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Validation
- _Run a quick smoke test and confirm expected behavior._

## Available options
- _List the key variants/toggles visible in the UI._

## Notes
- _Add prerequisites, constraints, and rollout behavior._

## Troubleshooting
- End Date: (View Only) This date is automatically calculated based on the Start Date, Interval, and Frequency. You cannot manually select or change this field.
- (View Only) This date is automatically calculated based on the Start Date, Interval, and Frequency. You cannot manually select or change this field.

## Field mapping / schemas
- _If this feature emits/consumes payloads or requires mapping, document the fields and examples._

## Cross-module workflows
- _Link this feature to upstream/downstream modules (e.g., Bot Studio ↔ Channels ↔ Analytics)._

## Module disambiguation
- _Add 1–2 bullets distinguishing this module from adjacent modules to reduce retrieval drift._

## Reference (from source)
<!-- procedural:v2 -->
# Website Re-training Scheduler (Developer Mode)

**Module**: Ai Admin

## Overview
Introduction: The Website Re-Training Scheduler is a powerful feature designed to automate the process of re-training your website URLs, significantly reducing manual content training efforts. This is particularly beneficial for businesses that frequently update their online content, ensuring your AI models are always up-to-date with the latest information.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Introduction: The Website Re-Training Scheduler is a powerful feature designed to automate the process of re-training your website URLs, significantly reducing manual content training efforts. This is particularly beneficial for businesses that frequently update their online content, ensuring your AI models are always up-to-date with the latest information.

Scheduler automatically untrain old content and retrain the latest content of URLs, ensuring relevance and accuracy of AI responses over time.

Accessibility: You can access the Scheduler by clicking the Scheduler Icon located in the Website Links section within the Content Tab.

Feature Description: The Website Re-Training Scheduler consists of two main components: the Scheduler Creation Modal and the Scheduler Listing Page.

Key Components of the Scheduler Creation Modal:

- Content Tag: (Read-Only) Displays the content tag that was selected before clicking the Scheduler Icon. This indicates which group of URLs the scheduler will manage.
- Name: A brief, descriptive name for your scheduler (e.g., "Debit Card Offer Updates"). Constraints: Minimum 5, maximum 50 characters. Special characters are not allowed.
- A brief, descriptive name for your scheduler (e.g., "Debit Card Offer Updates").
- Constraints: Minimum 5, maximum 50 characters. Special characters are not allowed.
- Start Date: The date on which the scheduler will begin its first execution. Selection Limit: You can select a date up to 1 year from the current date. Default Value: Defaults to the current date + 1 day.
- The date on which the scheduler will begin its first execution.
- Selection Limit: You can select a date up to 1 year from the current date.
- Default Value: Defaults to the current date + 1 day.
- Interval: Determines the recurring period between each scheduled training execution. Available Selections: Daily, Weekly, Monthly. Default Value: Weekly.
- Determines the recurring period between each scheduled training execution.
- Available Selections: Daily, Weekly, Monthly.
- Default Value: Weekly.
- Frequency: Specifies the number of times the training task will run based on the defined interval. Example: If the Interval is "Monthly" and the Frequency is "2", the scheduler will run once a month for two consecutive months. Available Selections: 1-5. Default Value: 1.
- Specifies the number of times the training task will run based on the defined interval.
- Example: If the Interval is "Monthly" and the Frequency is "2", the scheduler will run once a month for two consecutive months.
- Available Selections: 1-5.
- Default Value: 1.
- End Date: (View Only) This date is automatically calculated based on the Start Date, Interval, and Frequency. You cannot manually select or change this field.
- (View Only) This date is automatically calculated based on the Start Date, Interval, and Frequency. You cannot manually select or change this field.
- Default Training Time for different intervals: DAILY: The scheduler will run every day at 8:00 AM UTC. WEEKLY: The scheduler will run on the same weekday as the Start Date, at 8:00 AM UTC. MONTHLY: The scheduler will run on the same day of the month as the Start Date, at 8:00 AM UTC.
- DAILY: The scheduler will run every day at 8:00 AM UTC.
- WEEKLY: The scheduler will run on the same weekday as the Start Date, at 8:00 AM UTC.
- MONTHLY: The scheduler will run on the same day of the month as the Start Date, at 8:00 AM UTC.
Key components of Scheduler Listing Page: The Scheduler Listing Page provides an overview of all your scheduled re-training tasks, categorized by their status.

Important Rules and Behaviors:

- Active Scheduler Limit: Only one scheduler can be active at a time for a given content tag.
- Run Icon State: If there's an active scheduler, the "Run" icon for all other inactive schedulers will be disabled.
- Add New Button: A "Add New" button is available to create a new scheduler. However, if any scheduler is currently active, this button will be disabled. You must pause the active scheduler before creating a new one.
- Scheduler Order: Active schedulers will always appear at the top of the list. Schedulers are generally arranged by their "Created On" date, with the latest scheduler appearing first.
- Status Indicators: A scheduler that is currently running will display an "Active" status. A paused scheduler will display an "Inactive" status. If a scheduler completes all its scheduled runs or reaches its execution time on the End Date, its status will be marked "Completed." For inactive schedulers, they will also be marked "Completed" on their End Date.
- A scheduler that is currently running will display an "Active" status.
- A paused scheduler will display an "Inactive" status.
- If a scheduler completes all its scheduled runs or reaches its execution time on the End Date, its status will be marked "Completed." For inactive schedulers, they will also be marked "Completed" on their End Date.
- Deletion: You can delete an active or running scheduler. A confirmation modal will appear before deletion. If a scheduler is running, deleting it will not impact the ongoing training that is already in progress.
- You can delete an active or running scheduler.
- A confirmation modal will appear before deletion.
- If a scheduler is running, deleting it will not impact the ongoing training that is already in progress.
- Completed Schedulers: Once a scheduler's status is "Completed," all action icons in the "Action" column will disappear, and a "—" will be displayed instead.
Handling URL Untraining

- Untraining All URLs: If you untrain all URLs associated with a content tag that has an active scheduler, the active scheduler will automatically be paused.
- Adding New URLs: If new URLs are subsequently added to the content tag, the previously paused scheduler will not be activated automatically. You will need to manually reactivate it by clicking on run icon.
Updated 9 months ago

- Catalog Training

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
_Not specified._
