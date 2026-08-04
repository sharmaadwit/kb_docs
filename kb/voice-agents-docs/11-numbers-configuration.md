---
title: Numbers Configuration
description: Phone number management and agent-to-number linking
source: https://voiceagents.gupshup.io/developer-docs
---

# Numbers Configuration

## Phone Number Management

The Numbers Configuration page manages the association between provisioned telephony numbers and deployed Voice AI Agents. A phone number must be linked to an agent before it can receive or make live calls.

## Purchasing a Voice Plan

| Option | Description | Status |
|---|---|---|
| Add a Voice Plan | Provision a new PSTN phone number with an associated voice plan | Available |
| Buy a New WA Voice Number | Provision a WhatsApp-voice-capable number | Currently disabled — contact support |

## Configured Numbers Table

| Column | Description |
|---|---|
| Channel | Telephony channel type badge (e.g., PSTN Voice) |
| Number | Provisioned phone number in E.164 format (e.g., +918041949098) |
| Plan ID | Unique identifier for the associated voice subscription plan |
| AI Agent | Name of the Voice AI Agent currently linked to this number |
| Actions | \+ Add (link an agent) |

## Configuration Procedure

  * Click Add a Voice Plan to provision a new number if required

  * Locate the target number in the Configured Numbers table

  * If the Actions column shows '+ Add', click it to link the number to an agent

  * Numbers displaying 'IVR Allocated' are active. Click Reset to unlink and reassign

  * Click Refresh to reload the table and confirm changes

> ⚠ IMPORTANT A phone number must be linked to an agent before the Test Analysis tab can display call data. Ensure numbers are configured prior to initiating live testing or production deployment.
