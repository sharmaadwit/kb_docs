source_url: https://console-docs.gupshup.io/docs/assignment-20-covering-consultative-sales-usecases

<!-- procedural:v2 -->
# Assignment Enhancements in Console 7.0

**Module**: Agent Assist

## Overview
Assignment enhancements targets to assign all the chats coming for assignment to the agents automatically & optimising the agent's threshold so that the agents work only on the chats where customers are active. Below are the detailed understanding of different features launched to solve the above to objective.

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
Introduction

Assignment enhancements targets to assign all the chats coming for assignment to the agents automatically & optimising the agent's threshold so that the agents work only on the chats where customers are active. Below are the detailed understanding of different features launched to solve the above to objective.

Assigning all the chats coming for assignment automatically

In the previous assignment, whenever agents were not available to take the chat because they were busy or didn't have any bandwidth then the system used to wait for 30 minutes before sending the chats to unassigned queue. The brands then had to manually assign the chats to the agents. Now in this release, we have added No rules matched, Waiting for assignment and non business hours queue where instead of getting unassigned, the chats will be moved to these queues for specified time and will enhance the system's capability to automatically assign the chats

No Rules Matched

With the new feature of "No Rules Matched", the brands will be able to see the chats that have not matched with any assignment rules and then once they identify the pattern, the brands can edit the assignment rules so that once assignment rules are corrected, the chats will be automatically assigned to the respective teams

More details on the feature can be found here: What happens if a chat doesn't match with any assignment rule

Waiting on Assignment Queue

With the new addition of waiting for assignment queue, any chat the comes for assignment will be sent to waiting for assignment queue and the system will keep on trying the chat for assignment based on the configurable "Assignment Wait Time". Past limit was 30 minutes because of which brands often had to manually assign the chats after the 30 minutes time limit was over. Now the system will retry based on what any brand has configured in assignment wait time. By default assignment wait timeout is configured for 24 hours, post which a chat is closed and assigned back to the bot.

To distinguish such chats, each chat displayed in chat views will feature a team tag indicating that the specific chat is awaiting assignment for that particular team. Once clicked on that tag, the user will be redirected to the search page where all the chats that are waiting for assignment for that particular team will be shown

Assignment Wait Timeout

Using this configuration, brands can define the amount of time a chat has to be in waiting queue. Once the assignment wait timeout is hit, the chats are closed automatically and assigned back to the bot. By default the value of assignment wait timeout is 24 hours.

Assignment wait timeout can be configured on the team level where each time can have their own set of Assignment Wait Timeout. To configure, Go to teams > Edit Team > Assignment Wait Timeout

Non Business Hours Assignment

Using this, the brands can choose certain actions for the chats coming in outside of office hours for a specific team. Below are the different configurations:

- Assign to agent: Brands can opt for automating agent assignments for the following day, whereby conversations will be designated to agents when they come back online during the next day's business hours. In this process, brands need to define a specific threshold number for these conversations. By setting this threshold, the system ensures that agents do not exceed the designated number of assigned chats. This threshold specifically applies to conversations that originated outside of regular business hours. Consequently, the total number of chats an agent can handle comprises the sum of the load balancer threshold and the threshold for non-business hours chats. Additionally, since the automation is limited to the next day's business hours, brands have the flexibility to either assign the remaining chats to a chatbot or close those conversations.
- Assign to bot: In this scenario, the brand has the option to automatically transfer a chat back to the chatbot when it arrives during non-office hours for reassignment.
- Close: Chats received outside of office hours will be automatically closed
Non Business hours assignment is team level configuration where the brand can customise the configuration on the basis of its teams office hours. To access, go to Teams > Edit a team > Non Business Hour Assignment

Optimising Agent Assignment Threshold from the Load Balancer

With this configuration, brands have the option to determine whether chats with an "awaiting response" or "pending" status should be retained in the agent queue during load balancer assignment. Previously, when an agent moved a chat to "awaiting response," these chats were factored into the agent's threshold for assignment. However, by selecting the option that "awaiting response" chats should not be included in the load balancer threshold, they will be removed from the agent's queue, freeing up space for the agent to handle more open chats.

Below are the detailed understanding of the configuration:

Threshold Number:After choosing the load balancer, the initial step for the brand is to set the threshold count. This count determines the number of chats that will be allocated to an agent simultaneously.

Selecting chat status to be considered in the threshold

In this setup, the brand must choose which chat statuses to include when calculating the agent's bandwidth. By default, "Open," "Pending," and "Awaiting Response" are selected. The brand can opt to deselect "Awaiting Response" which is marked whenever there's a customer dependency. If both "awaiting response" and "pending" status chats are excluded from the threshold calculation, only chats in the "open" status will be considered for the agent's threshold assignment.

Sticky Assignment

Upon implementing the aforementioned configuration to exclude "Awaiting Response" and "Pending" status chats, brands can customize how the assignment process should operate when customers respond to the chat. Brands have the flexibility to choose from the following three options:

- Assigned to any available agent: Upon selection, if a customer returns, the chat will be assigned to any available agent.
- Force assigned the chat to the same agent: Once chosen, if the customer returns, the chat will be assigned to the same agent who placed the chat on "awaiting response," regardless of the agent's current status and bandwidth.
- Stickiness Wait Timeout: Upon selection, if the customer returns, the system will attempt to assign the chat to the same agent until the configured time elapses. The default value is 24 hours, meaning if the customer returns within this time frame, the system will try to assign the chat to the original agent for the next 24 hours & assign to the different agent only when 24 hours are passed. If the stickiness wait timeout is set to 0, the system will check for the availability of the original agent; if unavailable, the chat will be assigned to any other available agent. If the timeout is nonzero, the system will follow the same agent assignment approach within the specified timeframe.
This configuration is on team level where brand can implement different assignment policies for different teams. To access, go to Teams > Edit a team > Select load balancer > Select the necessary configurations based on the above details

Updated 10 months ago

- What happens if a chat doesn't match with any assignment rule?
- Chat Management: Assignment Rules

## Business hours vs after-hours behavior
Key notes found in source:

- In the previous assignment, whenever agents were not available to take the chat because they were busy or didn't have any bandwidth then the system used to wait for 30 minutes before sending the chats to unassigned queue. The brands then had to manually assign the chats to the agents. Now in this release, we have added No rules matched, Waiting for assignment and non business hours queue where instead of getting unassigned, the chats will be moved to these queues for specified time and will enhance the system's capability to automatically assign the chats
- Non Business Hours Assignment
- - Assign to agent: Brands can opt for automating agent assignments for the following day, whereby conversations will be designated to agents when they come back online during the next day's business hours. In this process, brands need to define a specific threshold number for these conversations. By setting this threshold, the system ensures that agents do not exceed the designated number of assigned chats. This threshold specifically applies to conversations that originated outside of regular business hours. Consequently, the total number of chats an agent can handle comprises the sum of the load balancer threshold and the threshold for non-business hours chats. Additionally, since the automation is limited to the next day's business hours, brands have the flexibility to either assign the remaining chats to a chatbot or close those conversations.
- Non Business hours assignment is team level configuration where the brand can customise the configuration on the basis of its teams office hours. To access, go to Teams > Edit a team > Non Business Hour Assignment

## Save/publish behavior
_Not specified._

