---
title: Testing Agents
description: Test Agent tab, editing agents, and test analysis
source: https://voiceagents.gupshup.io/developer-docs
---

# Testing Agents

## Test Agent Tab

The Test Agent tab provides a live testing environment to validate agent behaviour prior to production deployment. This tab becomes active only after the agent has been saved for the first time.

### Prerequisites

> ⚠ IMPORTANT The agent must be saved (published) before the Test Agent tab becomes functional. On first access, the interface displays: 'Save this agent first, then set up a test agent.'

### Testing Procedure

1. Complete all Agent, Tools, and Knowledge Base configuration

2. Click Publish to save the agent

3. Navigate to the Test Agent tab

4. Initiate a test call or chat session with the agent

5. Validate agent responses against the intended System Prompt behaviour

6. Return to the Agent tab to refine configuration as needed

### What to Validate

  * Agent responds accurately to the opening message scenario

  * System prompt constraints are observed (tone, scope, escalation triggers)

  * Agent adhere to the conversational flow

  * Evaluate Metrics like average latency, customer satisfaction, interruption etc

## Editing an Existing Agent

### Edit View

Clicking any agent name from the My Agents dashboard opens the edit view. The interface is identical to the Create Agent form with the following additions:

| Element | Description |
|---|---|
| Agent ID | Unique system identifier displayed in the header bar (e.g., agent_6201kn65ma2jejdaz13qtj08knk0) |
| Copy Agent ID | One-click button to copy the Agent ID to clipboard — required for API integrations |
| Preview Button | Opens a live preview/demo of the agent in its current saved state |
| Update Button | Replaces the 'Publish' button — saves changes to the existing deployed agent |

### Update Workflow

  * Click the agent name on the My Agents dashboard to open it

  * Modify the required fields: name, system prompt, voice, tools, or knowledge base

  * Use the Test Agent tab to validate changes in isolation before saving

  * Click Update to apply and deploy the revised configuration

> ⚠ IMPORTANT Changes are applied immediately upon clicking Update. For mission-critical agents, validate all modifications in the Test Agent tab and Evaluate Agent framework before updating the production agent.

## Test Analysis

The Test Analysis page presents detailed results from agent evaluation runs, providing QA Engineers and platform administrators with the data needed to measure, track, and improve agent performance over time.

### Prerequisites

> ⚠ IMPORTANT A phone number must be linked to the agent in Numbers Configuration before Test Analysis can display call data. Without a linked number, the page will display: 'No phone number is linked to this agent.'

### Filters

| Filter | Description |
|---|---|
| Agent | Select a specific agent to analyse, or choose 'All agents' for an aggregate view |
| Date Range (From / To) | Define the start and end dates for the analysis window |
| Clear | Reset all active filters to default state |

### Accessing Test Analysis

  * **From the Dashboard:** Click the Analysis button on any agent card in My Agents

  * **From within an Agent:** Navigate to the Test Analysis tab in the agent edit view

### Available Metrics

  * Evaluation run results with overall pass/fail status

  * Per-scenario scores and success/failure breakdown

  * Full call transcripts for each test run

  * Historical trend data across the selected date range
