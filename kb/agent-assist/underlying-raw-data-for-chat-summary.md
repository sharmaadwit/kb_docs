source_url: https://console-docs.gupshup.io/docs/underlying-raw-data-for-chat-summary

<!-- procedural:v2 -->
# Underlying Raw Data for Chat Summary

**Module**: Agent Assist

## Overview
- id: A unique identifier internal to agent assist
- brand_key: A unique key identifying the brand associated with the chat session.
- session_id: A unique identifier for the specific chat session.
- team_id: The unique identifier for the team handling the chat session.
- is_customer_anonymous: Indicates whether the customer interacting in the chat is anonymous (e.g., not logged in or unidentified). This is not applicable for WhatsApp
- created_date: The date on which the chat session was created.
- creation_timestamp: A more precise timestamp capturing the exact moment the chat session was created.
- created_hour: The hour (in 24-hour format) when the chat session was initiated.
- worked_date: The date on which work or interaction occurred in the chat session.
- worked_hour: The hour during which the interaction occurred in the session.
- sc_bot_break_time: The time duration (in seconds or minutes) when a chatbot disengaged or transitioned the session to a human agent.
- status: The current status of the session (e.g., open, closed).
- priority: The assigned priority of the session, indicating its urgency or importance
- channel: The communication channel used for the session (e.g., WhatsApp, Instagram etc).
- team: The team or group assigned to handle the session.
- customer_id: A unique identifier for the customer involved in the chat.
- currently_assigned_to: The name or ID of the agent currently assigned to the session.
- Agent_name: The name of the agent interacting in the session.
- m_frt_sc_bh_only: The first response time (FRT) for the session, measured in business hours only. First Response sent by the agent - Bot Handover Time
- min_FRT: The minimum first response time across sessions.
- avg_Response_Time: The average time taken to respond to the customer during the session.
- max_Resolution_Time: The maximum time taken to resolve a session.
- m_resp_sc_bh_only: The response time in business hours only.
- m_rt_sc_bh_only: The resolution time (RT) in business hours only.
- m_frt_sc_cal_hrs: The first response time in calendar hours.
- m_resp_sc_cal_hrs: The response time in calendar hours.
- m_rt_sc_cal_hrs: The resolution time in calendar hours.
- m_frt_wu_bh_only: First response time in business hours for sessions worked by the agent.
- m_resp_wu_bh_only: Response time in business hours for sessions worked by the agent.
- m_rt_wu_bh_only: Resolution time in business hours for sessions worked by the agent.
- m_frt_wu_cal_hrs: First response time in calendar hours for sessions worked by the agent.
- m_resp_wu_cal_hrs: Response time in calendar hours for sessions worked by the agent.
- m_rt_wu_cal_hrs: Resolution time in calendar hours for sessions worked by the agent.
- m_imp_agent_msg: Count of important messages sent by the agent.
- m_imp_cust_msg: Count of important messages sent by the customer.
- m_spam_agent_msg: Count of spam messages sent by the agent.
- m_spam_cust_msg: Count of spam messages sent by the customer.
- m_deleted_agent_msg: Count of messages deleted by the agent.
- m_deleted_cust_msg: Count of messages deleted by the customer.
- m_assignment_changes: Number of times the session was reassigned to different agents.
- m_assignee_changes: Count of changes to the assigned agent.
- m_tag_changes: Count of tag modifications for the session.
- m_priority_changes: Count of priority level changes for the session.
- m_brand_msg: Count of messages sent by the brand for every customer message. It wont consider the count of messages sent by the agent repeatedly to the customer without the customer’s reply
- m_customer_msg: Count of messages sent by the customer.
- M_orphan_msg: This metric will be removed from the report as this feature is not applicable for WhatsApp chats
- is_session_created_in_bh: Indicates whether the session was initiated during business hours.
- sc_first_assignment_time: The timestamp of the first assignment of the session to an agent.
- Total Agent Messages: Total count of messages sent by all agents during the session.
- Total Worked/Not Worked: Categorization of sessions as worked or not worked.
- Sessions: This tells if the session was created in business hours or not
- FRT Bucket: Categorization of sessions into different time buckets based on first response time. IF ("min_FRT" <= 5 , '0-5 sec', IF ("min_FRT" > 5 AND "min_FRT" <= 10, '5-10 sec', IF ("min_FRT" > 10 AND "min_FRT" <= 30, '10-30 sec', IF ("min_FRT" > 30 AND "min_FRT"/60 <= 1, '30 sec-1 min', IF ("min_FRT"/60 > 1 AND "min_FRT"/60 <= 5, '1-5 min', IF ("min_FRT"/60 > 5 AND "min_FRT"/60 <= 10, '5-10 min', IF ("min_FRT"/60 > 10 AND "min_FRT"/60 <= 20, '10-20 min', IF ("min_FRT"/60 > 20, '> 20 min', null))))))))
- Category: This will either be assigned to an agent or handled by bot/ unassigned

## When to use
_Add the primary scenarios and personas._

## Setup path
_In Console: add the navigation path (e.g., `Module → Settings → …`)._

## Step-by-step configuration
- id: A unique identifier internal to agent assist
- brand_key: A unique key identifying the brand associated with the chat session.
- session_id: A unique identifier for the specific chat session.
- team_id: The unique identifier for the team handling the chat session.
- is_customer_anonymous: Indicates whether the customer interacting in the chat is anonymous (e.g., not logged in or unidentified). This is not applicable for WhatsApp
- created_date: The date on which the chat session was created.
- creation_timestamp: A more precise timestamp capturing the exact moment the chat session was created.
- created_hour: The hour (in 24-hour format) when the chat session was initiated.
- worked_date: The date on which work or interaction occurred in the chat session.
- worked_hour: The hour during which the interaction occurred in the session.
- sc_bot_break_time: The time duration (in seconds or minutes) when a chatbot disengaged or transitioned the session to a human agent.
- status: The current status of the session (e.g., open, closed).
- priority: The assigned priority of the session, indicating its urgency or importance
- channel: The communication channel used for the session (e.g., WhatsApp, Instagram etc).
- team: The team or group assigned to handle the session.
- customer_id: A unique identifier for the customer involved in the chat.
- currently_assigned_to: The name or ID of the agent currently assigned to the session.
- Agent_name: The name of the agent interacting in the session.
- m_frt_sc_bh_only: The first response time (FRT) for the session, measured in business hours only. First Response sent by the agent - Bot Handover Time
- min_FRT: The minimum first response time across sessions.
- avg_Response_Time: The average time taken to respond to the customer during the session.
- max_Resolution_Time: The maximum time taken to resolve a session.
- m_resp_sc_bh_only: The response time in business hours only.
- m_rt_sc_bh_only: The resolution time (RT) in business hours only.
- m_frt_sc_cal_hrs: The first response time in calendar hours.
- m_resp_sc_cal_hrs: The response time in calendar hours.
- m_rt_sc_cal_hrs: The resolution time in calendar hours.
- m_frt_wu_bh_only: First response time in business hours for sessions worked by the agent.
- m_resp_wu_bh_only: Response time in business hours for sessions worked by the agent.
- m_rt_wu_bh_only: Resolution time in business hours for sessions worked by the agent.
- m_frt_wu_cal_hrs: First response time in calendar hours for sessions worked by the agent.
- m_resp_wu_cal_hrs: Response time in calendar hours for sessions worked by the agent.
- m_rt_wu_cal_hrs: Resolution time in calendar hours for sessions worked by the agent.
- m_imp_agent_msg: Count of important messages sent by the agent.
- m_imp_cust_msg: Count of important messages sent by the customer.
- m_spam_agent_msg: Count of spam messages sent by the agent.
- m_spam_cust_msg: Count of spam messages sent by the customer.
- m_deleted_agent_msg: Count of messages deleted by the agent.
- m_deleted_cust_msg: Count of messages deleted by the customer.
- m_assignment_changes: Number of times the session was reassigned to different agents.
- m_assignee_changes: Count of changes to the assigned agent.
- m_tag_changes: Count of tag modifications for the session.
- m_priority_changes: Count of priority level changes for the session.
- m_brand_msg: Count of messages sent by the brand for every customer message. It wont consider the count of messages sent by the agent repeatedly to the customer without the customer’s reply
- m_customer_msg: Count of messages sent by the customer.
- M_orphan_msg: This metric will be removed from the report as this feature is not applicable for WhatsApp chats
- is_session_created_in_bh: Indicates whether the session was initiated during business hours.
- sc_first_assignment_time: The timestamp of the first assignment of the session to an agent.
- Total Agent Messages: Total count of messages sent by all agents during the session.
- Total Worked/Not Worked: Categorization of sessions as worked or not worked.
- Sessions: This tells if the session was created in business hours or not
- FRT Bucket: Categorization of sessions into different time buckets based on first response time. IF ("min_FRT" <= 5 , '0-5 sec', IF ("min_FRT" > 5 AND "min_FRT" <= 10, '5-10 sec', IF ("min_FRT" > 10 AND "min_FRT" <= 30, '10-30 sec', IF ("min_FRT" > 30 AND "min_FRT"/60 <= 1, '30 sec-1 min', IF ("min_FRT"/60 > 1 AND "min_FRT"/60 <= 5, '1-5 min', IF ("min_FRT"/60 > 5 AND "min_FRT"/60 <= 10, '5-10 min', IF ("min_FRT"/60 > 10 AND "min_FRT"/60 <= 20, '10-20 min', IF ("min_FRT"/60 > 20, '> 20 min', null))))))))
- Category: This will either be assigned to an agent or handled by bot/ unassigned

## Business hours vs after-hours behavior
Key notes found in source:

- - m_frt_sc_bh_only: The first response time (FRT) for the session, measured in business hours only. First Response sent by the agent - Bot Handover Time
- - m_resp_sc_bh_only: The response time in business hours only.
- - m_rt_sc_bh_only: The resolution time (RT) in business hours only.
- - m_frt_wu_bh_only: First response time in business hours for sessions worked by the agent.
- - m_resp_wu_bh_only: Response time in business hours for sessions worked by the agent.
- - m_rt_wu_bh_only: Resolution time in business hours for sessions worked by the agent.
- - is_session_created_in_bh: Indicates whether the session was initiated during business hours.
- - Sessions: This tells if the session was created in business hours or not

## Save/publish behavior
_Not specified._

**Last updated (from source)**: Updated 10 months ago
