source_url: https://console-docs.gupshup.io/docs/bot-constants-in-jb
# BOT STUDIO

## Bot Constants in JB

# Bot Constants in JB

## Introduction:

The Bot Constants is a variable type that streamlines the management of key values—such as interest rates, discount percentages, and event dates—that are consistent across all users at a given time but may change periodically. This feature allows bot designers to define and update these constants centrally, ensuring that all conversations happening with the bot are using the most up-to-date information. By making these constants accessible across the journeys, Bot Constants enhance operational efficiency, reduce the risk of errors, and ensure that all users are aligned with the latest data. This leads to more accurate and reliable bot interactions, enhancing overall project performance.

Constant variables in Manage Variable tab

## How it Works:

- The Bot Constants are editable Constant Variables that are global in scope and apply across the entire project, rather than being tied to individual users.
- Editable by any bot designer from JB Canvas but readable only during runtime.
- The default value of the Constants can be updated only from the Variable Management screen in any journey canvas and it will reflect the same value on all journeys.
- It has no scope for runtime value updation.
- Bot Constants won't show in fields wherever a value can be stored on a variable.
## How to Use:

It is pretty easy to make a variable of ‘Constant’ type:

- Go on any journey
- Choose the ‘Manage Variable’
- At the top, choose ‘Constant’ type from the dropdown
- Click on the ‘Add Row’ button to make a new variable
- Give a name to the variable, choose the data type and finally enter the constant value you want to store in the variable
- Click on ‘Save’
- The Constant variable is ready to be used in any journey
## Use Cases:

Here are a few use cases that demonstrate the benefits of the validations added:

### Dynamic Pricing Updates:

Scenario: An online store runs a chatbot that provides product pricing information. The store often updates its pricing based on market conditions. Benefit: By using Bot Constants for pricing, the bot can always refer to the most up-to-date prices without needing to manually update each journey. This ensures consistency across all customer interactions and prevents outdated pricing information from being shared.

### Seasonal Campaign Adjustments:

Scenario: A retail brand's chatbot promotes different seasonal campaigns, each with unique discount codes and offer percentages. Benefit: When a new campaign starts, the bot designer can quickly update the discount percentage in the Bot Constants, allowing the bot to immediately start promoting the new offer across all relevant conversations. This reduces the time needed to roll out new campaigns and keeps the promotions consistent.

### Event Reminder Customization:

Scenario: A company uses a chatbot to remind users about upcoming webinars or events, with dates that occasionally change. Benefit: By setting event dates as Bot Constants, the bot automatically uses the updated event date in all reminder messages. This avoids the need to manually update each journey, ensuring users receive accurate and timely reminders.

Updated 10 months ago
