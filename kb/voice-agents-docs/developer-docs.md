# Gupshup - AI Agents

**Source:** https://voiceagents.gupshup.io/developer-docs

## Developer Docs

Gupshup Voice AI Console — Enterprise Edition Guide

## 01\. Platform Overview

### Introduction

The Gupshup Voice AI Agents Console is a cloud-based platform enabling organisations to design, deploy, and monitor AI-powered voice agents. Accessible at voiceagents.gupshup.io, the console provides a unified interface for the complete agent lifecycle — from initial prompt generation through production deployment and ongoing quality evaluation.

> ℹ NOTE This guide covers all 18 functional areas of the console. Screenshots referenced throughout this document correspond to the production environment as of April 2026.

### Intended Audience

This document is intended for:

  * Platform Administrators responsible for account setup and telephony configuration

  * Conversation Designers building agent workflows and system prompts

  * Quality Assurance Engineers running evaluation frameworks and scheduled tests

  * Business Analysts monitoring analytics and data collection dashboards




### Core Platform Capabilities

Capability| Description  
---|---  
AI Agent Management| Create, configure, version, and deploy voice AI agents  
Voice Synthesis| Design, clone, and remix custom voice personas  
Telephony Integration| PSTN and WhatsApp voice channel support via Knowlarity SR  
Knowledge Base (RAG)| Upload documents; configure Retrieval-Augmented Generation  
Evaluation Framework| Automated scenario-based testing and model comparison  
Analytics & Monitoring| Data collection metrics, latency insights, and call analytics  
Scheduled Automation| Cron-based recurring test run scheduling  
  
## 02\. Authentication

### Login Page

Navigate to <https://voiceagents.gupshup.io> to access the console login screen. Two authentication modes are supported:

Login Mode| Access Level| Recommended For  
---|---|---  
User Login| Standard — manage agents, view analytics, run evaluations| Conversation Designers, QA Engineers  
Admin Login| Elevated — account management, billing, integrations| Platform Administrators  
  
### Login Procedure

  1. Navigate to <https://voiceagents.gupshup.io>

  2. Select the appropriate tab: User Login or Admin Login

  3. Enter your registered Email Address

  4. Enter your Password

  5. Click Sign In to authenticate




> ⚠ IMPORTANT Admin Login credentials are provisioned separately from standard user accounts. Contact your platform administrator to request elevated access.

## 03\. My Agents — Dashboard

### Dashboard Overview

The My Agents dashboard is the primary landing page following authentication. It provides a centralised view of all configured agents and serves as the navigation hub for the entire platform.

### Interface Layout

Region| Component| Purpose  
---|---|---  
Left Sidebar| Navigation Menu| Access all platform sections  
Top Bar — Left| Gupshup Logo| Return to dashboard from any page  
Top Bar — Centre| Model Selector| Switch between model configurations (e.g., Model 1)  
Top Bar — Right| Help Button + Profile| Access support and account settings  
Main Content| Agent Card List| Browse, search, and open existing agents  
Main Content — Top| Action Buttons| Create agents via multiple methods  
  
### Agent Creation Methods

Button| Method| Best Used When  
---|---|---  
Create Agent with Voice| Wizard-based creation with voice pre-configured| Starting fresh with voice as a priority  
AI Prompt Generator| AI-assisted prompt generation before agent creation| Use case is defined; prompt writing is needed  
\+ Create Agent| Standard form-based creation| Experienced users with existing prompts  
  
### Agent Card Details

  * **Each agent is represented by a card displaying:**

  * **Agent Name:** Unique identifier with colour-coded avatar initials

  * **Created Date:** Timestamp of initial agent publication

  * **Last Modified Date:** Timestamp of the most recent update

  * **Analysis Button:** Direct navigation to Test Analysis for that agent




### Sidebar Navigation Reference

Sidebar Item| Purpose  
---|---  
My Agents| Dashboard — home screen with all agents  
Analytics| Call data collection and latency performance metrics  
Numbers Configuration| Phone number management and agent-to-number mapping  
Create An Agent| Direct access to new agent creation form  
Create Voice| Voice design, cloning, and remixing tools  
Tools| HTTP tool registry, Secrets, and Shopify (Admin API) connection  
Integrations| PSTN and WhatsApp telephony account configuration  
Evaluate Agent| Agent testing framework with scenario management  
Evaluate Models| Side-by-side AI model performance comparison  
Evaluate Models V2| Enhanced model comparison with improved metrics  
Scheduled Runs| Automated recurring test schedule management  
  
## 04\. Create Agent

### Agent Tab

The Agent tab is the primary configuration panel when creating or editing an agent. It is divided into two panels: Agent Configuration (left) and Voice & Language Settings (right).

### Left Panel — Agent Configuration

Field| Required| Description  
---|---|---  
Agent Name| Yes| A unique, descriptive identifier for the agent (e.g., 'Customer Support Bot')  
Tags| No| Comma-separated labels used for categorisation and filtering across the dashboard  
System Prompt| Yes| The core instruction set governing agent behaviour, persona, and capabilities  
First Message| No| The opening utterance when a call is connected. If left blank, the agent waits for the caller to speak first. Default: 'Hello! How can I help you today?'  
Dynamic Variables| No| Runtime placeholder variables using {{variable_name}} syntax, replaced with live values during calls  
  
### System Prompt Toolbar

  * **Three actions are available in the toolbar beneath the System Prompt text area:**

  * **Search:** Search within the prompt text for specific terms or phrases

  * **Edit / Expand:** Open the prompt in a full-screen editor for extended editing Improve with AI: Invoke AI optimisation on the existing prompt content (enabled only after content has been entered)




> ℹ NOTE A well-crafted System Prompt is the most critical factor in agent performance. Use the 'Improve with AI' function to refine prompts, and validate results using the Test Agent tab before publishing.

### Right Panel — Voice & Language Settings

Setting| Description  
---|---  
Voices| Select the primary voice persona. Default: 'Eric — Smooth, Trustworthy'. Additional voices can be added via '+ Add additional voice'. Use the play button to preview any voice.  
Expressive Mode (New)| Enhances speech with emotionally intelligent intonation and expressive audio tags. Enable or dismiss as appropriate for the use case.  
Language| Set the default conversation language. Additional languages can be added for multilingual agent support.  
LLM| Select the underlying AI language model provider and version. Default: gpt-4.1-mini.  
  
### Top Bar Actions

  * **Publish:** Deploys and activates the agent on the platform (new agents only) Tab Navigation: Agent | Tools | Knowledge Base | Advanced | Test Agent | Test Analysis



## 05\. Agent Tools

### Tools Tab

The Tools tab extends agent capabilities by attaching both custom integrations and built-in system actions. Tools empower agents to perform real-world operations during live calls.

### Interface Layout

  * **Left Section:** Custom tools list — initially empty for new agents

  * **Right Section:** System tools panel with individual enable/disable toggles




### Adding Custom Tools

  * Click Add tool (dropdown, top right) to add a new integration

  * Use the Search tools... bar to locate existing tools in your library




Filter using + Type or + Creator filters

Switch between the Tools and MCP sub-tabs as required

### System Tools Reference

System tools are platform-native capabilities that can be enabled independently for each agent:

System Tool| Description| Use Case  
---|---|---  
End Conversation| Programmatically terminates the call| Graceful call conclusion after task completion  
Detect Language| Automatically identifies the caller's spoken language| Multilingual deployments  
Skip Turn| Allows the agent to defer its conversational turn| Complex query handling scenarios  
Transfer to Agent| Routes the call to a designated human agent| Escalation and live agent handoff  
Transfer to Number| Forwards the call to a specified phone number| Departmental routing and warm transfers  
Play Keypad Touch Tone| Plays DTMF tones during the call| IVR navigation and third-party system interaction  
Voicemail Detection| Identifies if the call has reached a voicemail system| Automated outbound calling campaigns  
  
> ⚠ IMPORTANT The active tools counter at the top of the System Tools panel displays the number of currently enabled tools. Enable only the tools required for a given agent to maintain lean, predictable behaviour.

### Workspace Tools page (sidebar)

The **Tools** item in the workspace sidebar opens the HTTP tool registry: create tools, browse templates, manage Secrets, and connect **Shopify**. The Shopify panel lets you verify an Admin API access token against `GET /shop.json` and save `SHOPIFY_STORE` / `SHOPIFY_ACCESS_TOKEN` into Secrets, then use **Browse templates** for Shopify presets (order note, customer search, etc.) and attach them on each agent’s Tools tab.

## 06\. Knowledge Base

### Knowledge Base Tab

The Knowledge Base tab enables Retrieval-Augmented Generation (RAG), allowing agents to ground their responses in organisational documents. Uploaded files are indexed and queried in real time during conversations.

### Key Actions

Action| Description  
---|---  
Configure RAG| Opens RAG configuration: chunking strategy, embedding model, and retrieval parameters  
Add Document (dropdown)| Upload documents to the knowledge base. Supports PDF, plain text, Markdown, and other common formats  
Search Knowledge Base...| Full-text search across all uploaded documents within the agent  
\+ Type / + Creator filters| Filter the document list by file type or the user who uploaded the document  
  
### Configuration Procedure

  * Click Add Document and select the relevant file(s) from your local system



Allow the system to index the uploaded documents Click Configure RAG to adjust retrieval parameters including chunk size, embedding model, and similarity threshold The agent will reference these documents in real time to provide accurate, grounded responses

> ℹ NOTE For optimal RAG performance, upload well-structured documents (PDFs with clear headings, formatted FAQs). Configure the chunking strategy to match your document type — smaller chunks improve precision for Q&A workloads.

## 07\. Advanced Configuration

### Advanced Tab

The Advanced tab provides a read-only view of the underlying model infrastructure configuration for the selected agent. Voice-specific tuning parameters are managed from the Agent tab, not here.

### Model Infrastructure Details

Parameter| Value (Example)| Description  
---|---|---  
Provider| Model-1| The voice AI platform provider stack in use  
TTS Engine| Turbo v2.5| Text-to-Speech engine version handling speech synthesis  
ASR Provider| Built-in| Automatic Speech Recognition provider transcribing caller audio  
  
> ℹ NOTE Advanced settings — including voice stability, similarity boost, and speed parameters — are configured in the Agent tab under Voice Settings. This tab is read-only and reflects the infrastructure assigned to your account model.

## 08\. Test Agent

### Test Agent Tab

The Test Agent tab provides a live testing environment to validate agent behaviour prior to production deployment. This tab becomes active only after the agent has been saved for the first time.

### Prerequisites

> ⚠ IMPORTANT The agent must be saved (published) before the Test Agent tab becomes functional. On first access, the interface displays: 'Save this agent first, then set up a test agent.'

### Testing Procedure

Complete all Agent, Tools, and Knowledge Base configuration

  * Click Publish to save the agent


  1. Navigate to the Test Agent tab



Initiate a test call or chat session with the agent

Validate agent responses against the intended System Prompt behaviour

Return to the Agent tab to refine configuration as needed

### What to Validate

Agent responds accurately to the opening message scenario

System prompt constraints are observed (tone, scope, escalation triggers) Agent adhere to the conversational flow Evaluate Metrics like average latency, customer satisfaction, interruption etc

## 09\. Editing an Existing Agent

Edit View

Clicking any agent name from the My Agents dashboard opens the edit view. The interface is identical to the Create Agent form with the following additions:

### Edit View Additions

Element| Description  
---|---  
Agent ID| Unique system identifier displayed in the header bar (e.g., agent_6201kn65ma2jejdaz13qtj08knk0)  
Copy Agent ID| One-click button to copy the Agent ID to clipboard — required for API integrations  
Preview Button| Opens a live preview/demo of the agent in its current saved state  
Update Button| Replaces the 'Publish' button — saves changes to the existing deployed agent  
  
### Update Workflow

  * Click the agent name on the My Agents dashboard to open it Modify the required fields: name, system prompt, voice, tools, or knowledge base

  * Use the Test Agent tab to validate changes in isolation before saving

  * Click Update to apply and deploy the revised configuration




> ⚠ IMPORTANT Changes are applied immediately upon clicking Update. For mission-critical agents, validate all modifications in the Test Agent tab and Evaluate Agent framework before updating the production agent.

## 10\. AI Prompt Generator

AI Prompt Generator

The AI Prompt Generator accelerates agent development by automatically producing optimised System Prompts based on a structured description of the intended agent behaviour. It is accessible from the My Agents dashboard via the AI Prompt Generator button.

### Input Methods

Tab| Method| Best Suited For  
---|---|---  
From Text| Describe the agent's purpose in natural language| New agents without existing documentation  
From PDF Script| Upload an existing call script PDF for AI conversion| Migrating from legacy IVR scripts or existing SOPs  
  
### Configuration Fields

Field| Required| Options  
---|---|---  
Description| Yes| Free text — describe the agent's tasks, domain, and constraints in detail  
Agent Type| Yes| General Purpose, Customer Service, Sales, Technical Support, Appointment Booking, Survey/Feedback  
Tone| Yes| Professional, Friendly, Casual, Formal, Empathetic  
Agent Gender| Yes| Female, Male  
Additional Instructions| No| Specific constraints, language requirements, persona name, business rules  
  
Additional Instructions — Usage Examples 'Use only Script 1 from the uploaded PDF; disregard Script 2' 'Add Tamil and Marathi language support in addition to English' 'Agent persona name should be Priya' 'Never offer a discount exceeding 10% under any circumstances' 'Omit the objection handling section from the conversation flow'

### Generation Procedure

Enter a detailed description of the agent's intended purpose and domain

  2. Select the appropriate Agent Type, Tone, and Agent Gender Add any additional constraints or business rules in the Additional Instructions field


  * Click Generate Prompt to produce the optimised System Prompt Review the generated prompt and copy it into a new or existing agent's System Prompt field



> ⚠ IMPORTANT Always review AI-generated prompts before deploying to production. Test thoroughly using the Test Agent and Evaluate Agent frameworks to confirm the prompt produces the intended behaviour.

## 11\. Analytics

Analytics Dashboard

The Analytics page provides operational insights across two dimensions: Data Collection metrics (structured call data captured by agents) and Latency Metrics (performance timing for system components).

### Filtering Options

Filter| Description  
---|---  
Agent| Dropdown — filter analytics to a specific agent or view aggregated 'All Agents' data  
From Date| Start boundary of the analytics time window  
To Date| End boundary of the analytics time window  
  
Dashboard Tabs Dashboard: Data collection metrics showing structured fields captured during calls, with response counts and fill-rate percentages Latency Metrics: Performance timing data for ASR, LLM inference, and TTS components

### Data Collection Card Types

Field Name| Type| Description  
---|---|---  
Call Purpose| ENUM| Primary reason for the call. Options: product_information, pricing_inquiry, place_order, delivery_information, general_assistance, other  
Customer Name| TEXT| Full name of the caller, if volunteered during the conversation  
Customer Phone| TEXT| Caller's phone number, if provided during the call  
Flower Type| TEXT| Product category requested (example field — domain-specific)  
Occasion| TEXT| Context or occasion for the order  
Delivery Method| ENUM| Caller's fulfilment preference: delivery or pickup  
  
Each data collection card displays a data type badge (ENUM or TEXT), the field description, the total response count, and the fill-rate percentage. ENUM type cards also display the available option tags for at-a-glance distribution analysis.

## 12\. Numbers Configuration

Phone Number Management

The Numbers Configuration page manages the association between provisioned telephony numbers and deployed Voice AI Agents. A phone number must be linked to an agent before it can receive or make live calls.

### Purchasing a Voice Plan

Option| Description| Status  
---|---|---  
Add a Voice Plan| Provision a new PSTN phone number with an associated voice plan| Available  
Buy a New WA Voice Number| Provision a WhatsApp-voice-capable number| Currently disabled — contact support  
  
Configured Numbers Table

Column| Description  
---|---  
Channel| Telephony channel type badge (e.g., PSTN Voice)  
Number| Provisioned phone number in E.164 format (e.g., +918041949098)  
Plan ID| Unique identifier for the associated voice subscription plan  
AI Agent| Name of the Voice AI Agent currently linked to this number  
Actions| \+ Add (link an agent)  
  
### Configuration Procedure

  * Click Add a Voice Plan to provision a new number if required



Locate the target number in the Configured Numbers table

If the Actions column shows '+ Add', click it to link the number to an agent Numbers displaying 'IVR Allocated' are active. Click Reset to unlink and reassign

  * Click Refresh to reload the table and confirm changes



> ⚠ IMPORTANT A phone number must be linked to an agent before the Test Analysis tab can display call data. Ensure numbers are configured prior to initiating live testing or production deployment.

## 13\. Create Voice

Voice Creation Studio

The Create Voice page provides four methods for producing custom voice personas for use across your agent portfolio. Custom voices are stored in your account's voice library and can be assigned to any agent.

### Voice Creation Methods

Method| Description| Input Required  
---|---|---  
Voice Design| Generate an entirely new voice from a natural language text description| Descriptive text prompt  
Instant Voice Clone| Clone a target voice using a short audio sample| Minimum 10 seconds of clear audio  
Professional Voice Clone| Create a high-fidelity digital replica with maximum realism| Extended audio corpus  
Voice Remixing| Transform an existing voice using descriptive text prompts to produce variations| Select existing voice + text prompt  
  
### Voice Design Workflow

  2. Select the Voice Design tab (selected by default) In the description field, articulate the voice characteristics in detail — e.g., 'A warm, professional female voice with a slight Indian accent, suitable for customer support in a healthcare context'


  * Click Generate Previews to produce multiple voice candidates

  * Use the play button on each preview card to audition the generated voices



  2. Select the preferred voice — it will be saved to My Created Voices



My Created Voices The My Created Voices section below the creation tools lists all custom voices in your account library. Each voice card displays the voice name, type classification (e.g., Professional), a preview play button, and a Delete option.

> ℹ NOTE Voice names are visible to all agents within your account. Use descriptive, consistent naming conventions (e.g., 'Priya — Warm Healthcare EN') to facilitate efficient voice selection across large agent portfolios.

## 14\. Integrations

Telephony Account Configuration

The Integrations page configures the telephony provider accounts that underpin all voice call functionality on the platform. Both PSTN and WhatsApp voice accounts are managed here.

PSTN Voice Account (SR Account) The PSTN account is linked to your organisation's Knowlarity SuperReceptionist (SR) account and provides traditional telephone network connectivity.

Field| Description  
---|---  
Status| Real-time connection status. A green 'Connected' badge confirms active integration.  
Login to SR| Opens the Knowlarity SuperReceptionist administration panel in a new tab  
User ID| Your SR platform user identifier  
Email ID| The email address associated with the SR account  
Account Name| Your organisation's registered account name within Knowlarity  
Credits Available| Remaining call credit balance. Negative values indicate a deficit — top up before initiating campaigns.  
  
WhatsApp Voice Account (SR Account) WhatsApp Voice Account integration is currently marked as Coming Soon. This feature is not yet available. Contact your Gupshup account manager for release timelines.

### Maintenance Procedure

Verify the PSTN account shows a green 'Connected' status before running test or production calls Click Login to SR to manage telephony routing, SIP configuration, and call flows directly in Knowlarity Monitor Credits Available regularly; initiate top-up before balance falls below operational threshold

> ⚠ IMPORTANT Negative Credits Available will prevent outbound calls from being placed. Ensure sufficient credit balance is maintained for scheduled campaigns and high-volume inbound periods.

## 15\. Evaluate Agent

Agent Evaluation Framework

The Evaluate Agent page provides a structured framework for running automated test scenarios against deployed agents. It enables QA Engineers to define expected conversation flows and measure agent performance objectively.

### Agent List Table

Column| Description  
---|---  
Agent ID| Unique numeric identifier for the agent configuration in the evaluation framework  
Agent Name| Human-readable name of the agent under test  
Phone Number| The PSTN number linked to the agent — calls are placed to this number during evaluation  
Language| Primary language configured for the agent  
Actions| Edit (pencil icon) to modify configuration; Delete (trash icon) to remove from the evaluation list  
  
Toolbar Actions

Button| Colour| Function  
---|---|---  
\+ Agents| Green| Add a new agent configuration to the evaluation framework  
Scenarios| Orange| Define test scenarios with conversation scripts, expected responses, and pass/fail criteria  
View Results| Blue| Access the results of all previous evaluation runs, including scores and transcripts  
  
### Evaluation Procedure

  * Click + Agents to register agents in the evaluation framework Click Scenarios to create test scripts — define conversation turns, expected agent responses, and success criteria



Initiate an evaluation run to execute all scenarios against the selected agents Click View Results to analyse outcomes: pass/fail rates, scores, and full transcripts

## 16\. Evaluate Models

Model Comparison — V1 & V2

The Evaluate Models and Evaluate Models V2 pages provide side-by-side AI language model benchmarking against real agent test cases. This capability enables data-driven decisions when selecting or upgrading the LLM powering an agent.

### Interface Layout

Left Panel — Test Agents: Lists all registered agents with Agent ID and phone number. Use the Search bar to filter. Right Panel — Test Cases & Models: Activated after selecting an agent. Displays available test cases and model selection controls.

### Comparison Procedure

  * Select an agent from the left panel



Choose the test cases to include in the comparison run

  2. Select the AI models to benchmark (e.g.,gupshup, vapi, Elevenlabs)



Execute the evaluation run Review and compare results — response quality scores, latency, and accuracy metrics across models

### V1 vs V2 Comparison

Capability| V1| V2  
---|---|---  
Core workflow| Identical| Identical  
Evaluation metrics| Standard scoring| Enhanced metrics and scoring methodology  
Results visualisation| Tabular| Improved charts and comparison visualisation  
  
## 17\. Scheduled Runs

Scheduled Test Runs

The Scheduled Runs page automates agent evaluation on a recurring cron-based schedule, enabling continuous quality monitoring without manual intervention.

### Schedule Table Columns

Column| Description  
---|---  
Name| Descriptive schedule identifier (e.g., 'morning_check', 'swiggy_daily_run')  
Agent ID| The agent targeted by this scheduled evaluation  
Scenarios| Number of test scenarios included. Click the badge to view or edit the linked scenario set.  
Schedule| Human-readable cron expression (e.g., 'Every day at 9 AM')  
Last Run| Timestamp of the most recent scheduled execution  
Enabled| Toggle to activate or suspend the schedule without deleting it  
Actions| Delete icon to permanently remove the schedule  
  
### Creating a Scheduled Run

  * Click + New Schedule (top right)



Enter a descriptive Name for the schedule

Specify the Agent name to be tested

  2. Select the test Scenarios to include in each run Define the Schedule using a cron expression (e.g., '0 9 * * *' for daily at 9 AM)


  * Toggle Enabled to ON to activate the schedule immediately



## 18\. Test Analysis

Test Analysis

The Test Analysis page presents detailed results from agent evaluation runs, providing QA Engineers and platform administrators with the data needed to measure, track, and improve agent performance over time.

### Prerequisites

> ⚠ IMPORTANT A phone number must be linked to the agent in Numbers Configuration before Test Analysis can display call data. Without a linked number, the page will display: 'No phone number is linked to this agent.'

### Filters

Filter| Description  
---|---  
Agent| Select a specific agent to analyse, or choose 'All agents' for an aggregate view  
Date Range (From / To)| Define the start and end dates for the analysis window  
Clear| Reset all active filters to default state  
  
Accessing Test Analysis

  * **From the Dashboard:** Click the Analysis button on any agent card in My Agents

  * **From within an Agent:** Navigate to the Test Analysis tab in the agent edit view




### Available Metrics

Evaluation run results with overall pass/fail status

Per-scenario scores and success/failure breakdown

Full call transcripts for each test run

Historical trend data across the selected date range

End-to-End Deployment Workflow

The following workflow represents the recommended end-to-end process for deploying a production-ready Voice AI Agent on the Gupshup platform:

1| AI Prompt Generator| Define your agent's use case, tone, and type. Generate an optimised System Prompt and refine with Additional Instructions.  
---|---|---  
2| Create Agent — Agent Tab| Name the agent, paste the generated prompt, set the First Message, select voice and language, choose the LLM.  
3| Tools Tab| Enable required system tools (e.g., Transfer to Agent, End Conversation). Attach custom API tool integrations.  
4| Knowledge Base Tab| Upload relevant documents (product catalogues, FAQs, policies). Configure RAG settings.  
5| Publish| Click Publish to save and activate the agent on the platform.  
6| Numbers Configuration| Link a provisioned PSTN phone number to the agent.  
7| Test Agent Tab| Conduct test calls. Validate System Prompt behaviour, tool execution, and RAG responses.  
8| Evaluate Agent| Define structured test scenarios. Run evaluations. Review scores and transcripts via View Results.  
9| Evaluate Models| If applicable, benchmark alternative LLMs against test cases to determine optimal model selection.  
10| Scheduled Runs| Configure recurring evaluation schedules for continuous quality monitoring.  
11| Analytics| Monitor live call data collection, fill rates, and latency metrics post-deployment.  
  
> ⚠ IMPORTANT Always execute Steps 7 and 8 before directing production traffic to a new or significantly updated agent. The Test Agent and Evaluate Agent frameworks are the primary quality gates on the Gupshup platform.

Quick Reference

Platform Navigation

Sidebar Item| Primary Purpose| Key Action  
---|---|---  
My Agents| Agent inventory and creation| Create, search, and open agents  
Analytics| Call data and performance metrics| Monitor fill rates and latency  
Numbers Configuration| Phone number management| Link numbers to agents  
Create An Agent| New agent wizard| Build agents from scratch  
Create Voice| Voice persona management| Design and clone voices  
Integrations| Telephony account configuration| Monitor credits and SR connection  
Evaluate Agent| QA testing framework| Run scenario-based evaluations  
Evaluate Models| LLM benchmarking| Compare model performance  
Evaluate Models V2| Enhanced LLM benchmarking| Compare with improved metrics  
Scheduled Runs| Automated test scheduling| Configure recurring evaluations  
  
Key Terminology

Term| Definition  
---|---  
System Prompt| The core instruction set that defines an agent's persona, capabilities, scope, and behaviour  
RAG| Retrieval-Augmented Generation — grounding AI responses using indexed organisational documents  
TTS| Text-to-Speech — the engine that converts agent text output to synthesised voice audio  
ASR| Automatic Speech Recognition — the engine that transcribes caller speech to text for LLM processing  
LLM| Large Language Model — the AI model that processes transcribed input and generates agent responses  
IVR| Interactive Voice Response — the telephony routing layer that connects calls to agents  
PSTN| Public Switched Telephone Network — traditional telephone infrastructure for call delivery  
DTMF| Dual-Tone Multi-Frequency — keypad tones used for interactive telephony navigation  
SR Account| SuperReceptionist Account — Knowlarity's telephony platform integrated with Gupshup  
Dynamic Variable| A runtime placeholder ({{variable_name}}) in prompts replaced with live contextual data
