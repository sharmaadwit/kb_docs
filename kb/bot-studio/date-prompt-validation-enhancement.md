source_url: https://console-docs.gupshup.io/docs/date-prompt-validation-enhancement

<!-- procedural:v2 -->
# Date Prompt Validation Enhancement

**Module**: Bot Studio

## Overview
Date node

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
# Introduction:

Date node

Date Prompt Node in Journey Builder canvas is now enhanced with validation logic that can be implemented to ensure proper validation of the dates. This allows business to define a proper date range based on which the user input date will be validated. In addition to the previously available validations viz. Past Dates and Future Dates, bot designers can now also take into account the Timezone for which this range is valid and also the current date should be considered in the same range or not.Two more additional validations such as Past Dates including Today and Future Dates including Today are added. This enhances the possibility to handle various appointment bookings, ticket bookings and other use cases.

# Use Cases:

Here are a few use cases that demonstrate the benefits of the validations added:

### Same-Day Appointment Scheduling:

- Scenario: A healthcare provider offers same-day appointments for urgent care.
- Benefit: The "Future Dates including Today" validation ensures that users can select today's date for an appointment, enhancing the flexibility for urgent care bookings.
### Same-Day Delivery Services:

- Scenario: An e-commerce platform provides same-day delivery options.
- Benefit: The "Future Dates including Today" validation allows customers to choose today's date for delivery, improving customer satisfaction with faster delivery options.
### Expense Reporting:

- Scenario: A business allows employees to submit expense reports for past travel dates, including the current day.
- Benefit: The "Past Dates including Today" validation allows employees to report expenses incurred on the current day as well as previous days. This ensures timely and accurate expense tracking, especially for employees who travel frequently and may not have immediate access to reporting tools.
- Example: An employee on a business trip can submit expenses for meals and transportation incurred over the past few days and include today's expenses as well. This ensures all expenses are reported promptly and reimbursed in a timely manner.
### Note:

There will be no backend operation done on the user-entered time, regardless of the user's timezone. Validation will be performed based on the date entered by the user and the timezone selected on the node. If the user provides a date in a different timezone than the one selected on the node, the bot will validate the date as entered.

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Scenario: A business allows employees to submit expense reports for past travel dates, including the current day.

**Last updated (from source)**: Updated 10 months ago
