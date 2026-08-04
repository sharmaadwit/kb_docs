---
title: Evaluation Framework
description: Agent evaluation, model comparison, and testing frameworks
source: https://voiceagents.gupshup.io/developer-docs
---

# Evaluation Framework

## Evaluate Agent

### Agent Evaluation Framework

The Evaluate Agent page provides a structured framework for running automated test scenarios against deployed agents. It enables QA Engineers to define expected conversation flows and measure agent performance objectively.

### Agent List Table

| Column | Description |
|---|---|
| Agent ID | Unique numeric identifier for the agent configuration in the evaluation framework |
| Agent Name | Human-readable name of the agent under test |
| Phone Number | The PSTN number linked to the agent — calls are placed to this number during evaluation |
| Language | Primary language configured for the agent |
| Actions | Edit (pencil icon) to modify configuration; Delete (trash icon) to remove from the evaluation list |

### Toolbar Actions

| Button | Colour | Function |
|---|---|---|
| \+ Agents | Green | Add a new agent configuration to the evaluation framework |
| Scenarios | Orange | Define test scenarios with conversation scripts, expected responses, and pass/fail criteria |
| View Results | Blue | Access the results of all previous evaluation runs, including scores and transcripts |

### Evaluation Procedure

1. Click + Agents to register agents in the evaluation framework

2. Click Scenarios to create test scripts — define conversation turns, expected agent responses, and success criteria

3. Initiate an evaluation run to execute all scenarios against the selected agents

4. Click View Results to analyse outcomes: pass/fail rates, scores, and full transcripts

## Evaluate Models

### Model Comparison — V1 & V2

The Evaluate Models and Evaluate Models V2 pages provide side-by-side AI language model benchmarking against real agent test cases. This capability enables data-driven decisions when selecting or upgrading the LLM powering an agent.

### Interface Layout

  * **Left Panel — Test Agents:** Lists all registered agents with Agent ID and phone number. Use the Search bar to filter.

  * **Right Panel — Test Cases & Models:** Activated after selecting an agent. Displays available test cases and model selection controls.

### Comparison Procedure

1. Select an agent from the left panel

2. Choose the test cases to include in the comparison run

3. Select the AI models to benchmark (e.g., gupshup, vapi, Elevenlabs)

4. Execute the evaluation run

5. Review and compare results — response quality scores, latency, and accuracy metrics across models

### V1 vs V2 Comparison

| Capability | V1 | V2 |
|---|---|---|
| Core workflow | Identical | Identical |
| Evaluation metrics | Standard scoring | Enhanced metrics and scoring methodology |
| Results visualisation | Tabular | Improved charts and comparison visualisation |
