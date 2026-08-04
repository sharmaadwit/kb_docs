---
title: End-to-End Deployment Workflow
description: Recommended steps for deploying production-ready Voice AI agents
source: https://voiceagents.gupshup.io/developer-docs
---

# End-to-End Deployment Workflow

## Overview

The following workflow represents the recommended end-to-end process for deploying a production-ready Voice AI Agent on the Gupshup platform:

| Step | Phase | Description |
|---|---|---|
| 1 | AI Prompt Generator | Define your agent's use case, tone, and type. Generate an optimised System Prompt and refine with Additional Instructions. |
| 2 | Create Agent — Agent Tab | Name the agent, paste the generated prompt, set the First Message, select voice and language, choose the LLM. |
| 3 | Tools Tab | Enable required system tools (e.g., Transfer to Agent, End Conversation). Attach custom API tool integrations. |
| 4 | Knowledge Base Tab | Upload relevant documents (product catalogues, FAQs, policies). Configure RAG settings. |
| 5 | Publish | Click Publish to save and activate the agent on the platform. |
| 6 | Numbers Configuration | Link a provisioned PSTN phone number to the agent. |
| 7 | Test Agent Tab | Conduct test calls. Validate System Prompt behaviour, tool execution, and RAG responses. |
| 8 | Evaluate Agent | Define structured test scenarios. Run evaluations. Review scores and transcripts via View Results. |
| 9 | Evaluate Models | If applicable, benchmark alternative LLMs against test cases to determine optimal model selection. |
| 10 | Scheduled Runs | Configure recurring evaluation schedules for continuous quality monitoring. |
| 11 | Analytics | Monitor live call data collection, fill rates, and latency metrics post-deployment. |

> ⚠ IMPORTANT Always execute Steps 7 and 8 before directing production traffic to a new or significantly updated agent. The Test Agent and Evaluate Agent frameworks are the primary quality gates on the Gupshup platform.
