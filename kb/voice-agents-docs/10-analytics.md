---
title: Analytics & Monitoring
description: Analytics dashboard, data collection metrics, and latency insights
source: https://voiceagents.gupshup.io/developer-docs
---

# Analytics

## Analytics Dashboard

The Analytics page provides operational insights across two dimensions: Data Collection metrics (structured call data captured by agents) and Latency Metrics (performance timing for system components).

### Filtering Options

| Filter | Description |
|---|---|
| Agent | Dropdown — filter analytics to a specific agent or view aggregated 'All Agents' data |
| From Date | Start boundary of the analytics time window |
| To Date | End boundary of the analytics time window |

### Dashboard Tabs

  * **Dashboard:** Data collection metrics showing structured fields captured during calls, with response counts and fill-rate percentages

  * **Latency Metrics:** Performance timing data for ASR, LLM inference, and TTS components

### Data Collection Card Types

| Field Name | Type | Description |
|---|---|---|
| Call Purpose | ENUM | Primary reason for the call. Options: product_information, pricing_inquiry, place_order, delivery_information, general_assistance, other |
| Customer Name | TEXT | Full name of the caller, if volunteered during the conversation |
| Customer Phone | TEXT | Caller's phone number, if provided during the call |
| Flower Type | TEXT | Product category requested (example field — domain-specific) |
| Occasion | TEXT | Context or occasion for the order |
| Delivery Method | ENUM | Caller's fulfilment preference: delivery or pickup |

Each data collection card displays a data type badge (ENUM or TEXT), the field description, the total response count, and the fill-rate percentage. ENUM type cards also display the available option tags for at-a-glance distribution analysis.
