---
title: Integrations
description: Telephony account configuration and integration setup
source: https://voiceagents.gupshup.io/developer-docs
---

# Integrations

## Telephony Account Configuration

The Integrations page configures the telephony provider accounts that underpin all voice call functionality on the platform. Both PSTN and WhatsApp voice accounts are managed here.

## PSTN Voice Account (SR Account)

The PSTN account is linked to your organisation's Knowlarity SuperReceptionist (SR) account and provides traditional telephone network connectivity.

| Field | Description |
|---|---|
| Status | Real-time connection status. A green 'Connected' badge confirms active integration. |
| Login to SR | Opens the Knowlarity SuperReceptionist administration panel in a new tab |
| User ID | Your SR platform user identifier |
| Email ID | The email address associated with the SR account |
| Account Name | Your organisation's registered account name within Knowlarity |
| Credits Available | Remaining call credit balance. Negative values indicate a deficit — top up before initiating campaigns. |

## WhatsApp Voice Account (SR Account)

WhatsApp Voice Account integration is currently marked as Coming Soon. This feature is not yet available. Contact your Gupshup account manager for release timelines.

## Maintenance Procedure

  * Verify the PSTN account shows a green 'Connected' status before running test or production calls

  * Click Login to SR to manage telephony routing, SIP configuration, and call flows directly in Knowlarity

  * Monitor Credits Available regularly; initiate top-up before balance falls below operational threshold

> ⚠ IMPORTANT Negative Credits Available will prevent outbound calls from being placed. Ensure sufficient credit balance is maintained for scheduled campaigns and high-volume inbound periods.
