source_url: https://console-docs.gupshup.io/docs/user-management-business-hours

<!-- kb-golden:v12 -->
# Agent Assist Availability Vs Auto Replies

**Module**: Workflows

## Definition
Use this workflow when you need to distinguish between:

- where team working hours are defined
- where offline responses are defined

## What Each Page Controls
- `Business Hours` lets you set working hours for teams of agents so chats are assigned based on those hours.
- `Auto Replies` includes responses when agents are offline, and those responses vary based on business hours.

## Business Hours
From the source page:

1. Go to `Settings`.
2. Click `Business Hours`.
3. Click `Add New`.
4. Configure naming, time zone, daily hours, and holidays.

## Auto Replies
From the source page:

- `Agents Offline/Busy During Business Hours` is sent when agents are unavailable during business hours.
- `Agents Not Available Outside Business Hours` is sent for chats received outside business hours.
- `Handover to Bot` can be used when agents are offline during either business hours or non-business hours.

## Practical Split
- Use `Business Hours` to define when teams are working.
- Use `Auto Replies` to define what response is sent when agents are offline or outside business hours.

## Source Notes
- This workflow page combines:
  - `https://console-docs.gupshup.io/docs/user-management-business-hours`
  - `https://console-docs.gupshup.io/docs/response-management-auto-replies-customer-satisfaction`
