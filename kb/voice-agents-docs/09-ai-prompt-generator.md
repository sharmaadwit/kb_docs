---
title: AI Prompt Generator
description: Automated system prompt generation from natural language descriptions
source: https://voiceagents.gupshup.io/developer-docs
---

# AI Prompt Generator

## Overview

The AI Prompt Generator accelerates agent development by automatically producing optimised System Prompts based on a structured description of the intended agent behaviour. It is accessible from the My Agents dashboard via the AI Prompt Generator button.

## Input Methods

| Tab | Method | Best Suited For |
|---|---|---|
| From Text | Describe the agent's purpose in natural language | New agents without existing documentation |
| From PDF Script | Upload an existing call script PDF for AI conversion | Migrating from legacy IVR scripts or existing SOPs |

## Configuration Fields

| Field | Required | Options |
|---|---|---|
| Description | Yes | Free text — describe the agent's tasks, domain, and constraints in detail |
| Agent Type | Yes | General Purpose, Customer Service, Sales, Technical Support, Appointment Booking, Survey/Feedback |
| Tone | Yes | Professional, Friendly, Casual, Formal, Empathetic |
| Agent Gender | Yes | Female, Male |
| Additional Instructions | No | Specific constraints, language requirements, persona name, business rules |

### Additional Instructions — Usage Examples

  * 'Use only Script 1 from the uploaded PDF; disregard Script 2'
  * 'Add Tamil and Marathi language support in addition to English'
  * 'Agent persona name should be Priya'
  * 'Never offer a discount exceeding 10% under any circumstances'
  * 'Omit the objection handling section from the conversation flow'

## Generation Procedure

1. Enter a detailed description of the agent's intended purpose and domain

2. Select the appropriate Agent Type, Tone, and Agent Gender

3. Add any additional constraints or business rules in the Additional Instructions field

4. Click Generate Prompt to produce the optimised System Prompt

5. Review the generated prompt and copy it into a new or existing agent's System Prompt field

> ⚠ IMPORTANT Always review AI-generated prompts before deploying to production. Test thoroughly using the Test Agent and Evaluate Agent frameworks to confirm the prompt produces the intended behaviour.
