source_url: https://console-docs.gupshup.io/docs/creating-a-tiktok-specific-bot-journey

<!-- kb-golden:v12 -->
# Ctwa To Bot To Goals

**Module**: Workflows

## Definition
This workflow combines:

- connecting an ad journey to a CTWA campaign
- measuring campaign delivery and clicks in Campaign Analytics
- measuring conversion after goal implementation in Goal Analytics

## Connect Bot To CTWA Campaign
From the CTWA source page:

1. Click `Click to Chat Ads -> Ad Management -> Ad Campaigns`.
2. Search for the campaign configured for TikTok to WhatsApp and click `View Ads`.
3. Click `Connect Bot`, then click `Confirm`.
4. In the bot setup page, select the `Ad Journey` and click `Publish`.

## Prepare The Ad Journey
From the Bot Studio source page:

- Only `Ad Journeys` can be connected to CTWA ads.
- To prepare one:
  1. Go to `Bot Studio -> Journeys`.
  2. Open `Ad Journeys`.
  3. Click `+Create Ad Journey`.
  4. Add a `Call and Return` action.
  5. Select the desired user journey.
  6. Click `Save and Deploy`.

## Campaign Analytics
From `Campaign Analytics`:

- Available for campaigns that are `sent`.
- Metrics shown include:
  - `Targeted`
  - `Sent`
  - `Delivered`
  - `Read`
  - `Dropped`
  - `Failed`
  - `Unique Clicks`
  - `Total Clicks`
  - `Click Through Rate`
- `Response file` gives a timewise summary of all delivery events for all phone numbers.

## Goal Analytics
From `Goal Analytics`:

- After creating a Goal and implementing it within a journey, you can track it through Goal Analytics.
- You can access Goal Analytics by clicking the analytics icon on the Goals dashboard.
- Goal Analytics shows:
  - `Goal Achieved`
  - `Unique Users`
  - `Trends`
  - milestone-level exports

## Source Notes
- CTWA campaign source: `https://console-docs.gupshup.io/docs/creating-a-tiktok-specific-bot-journey`
- Ad-journey source: `https://console-docs.gupshup.io/docs/connecting-ad-to-bot-in-gupshup-console`
- Campaign analytics source: `https://console-docs.gupshup.io/docs/campaign-analytics`
- Goal analytics source: `https://console-docs.gupshup.io/docs/goal-analytics`
