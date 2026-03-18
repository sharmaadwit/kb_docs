# Patch 2 of 3 — CONCEPT_REGISTRY Expansion (28 new entries)

**Files**: `product_introduction_kb/kb_answer.py`, `product_introduction_kb/kb_search.py`
**Risk**: Low (data-only, no logic changes)
**Telemetry**: Do NOT touch any Langfuse/telemetry code.

---

## Overview

This patch adds 28 new CONCEPT_REGISTRY entries to both files, covering:
- Bot Studio nodes: expression_library, wait_for_event, address_node, ai_node, sticky_journey
- Agent Assist features: agent_assist_overview, tags_mgmt, views_mgmt, csat, canned_responses, sla, global_search, bulk_actions, insights_agent, insights_chat, insights_raw_data, template_window
- Integrations: integrations_webhooks
- Wallet: wallet
- AI Admin: ai_admin_workspace, ai_admin_training, ai_admin_intents, ai_admin_entities, ai_admin_evaluate, ai_admin_monitoring, ai_admin_teach, ai_admin_tags, ai_agent
- Also adds missing `whatsapp_flow` entry to kb_search.py

## Step 1 — Add entries to `CONCEPT_REGISTRY` in `kb_answer.py`

Find the LAST entry in the `CONCEPT_REGISTRY` list (the `goal_analytics` entry ending with `},`). 

**After** that entry and **before** the closing `]`, insert the following entries:

```python
    # ---- Phase 4a: double-zero categories ----
    {
        "id": "expression_library",
        "aliases": [
            "expression library", "expression functions", "build expression",
            "modify variable expression", "expression editor",
            "data manipulation expression", "pre built functions",
            "expression instead of code node", "expression library functions",
        ],
        "module_context": ["bot studio"],
        "source_boosts": {
            "expression-library-in-journey-builder-canvas": 6.0,
            "extracting-and-manipulating-data-using-expression-library-functions": 5.0,
        },
        "source_penalties": {},
        "display": "Expression Library",
        "page_display": "Expression Library in Journey Builder Canvas",
        "module": "Bot Studio",
        "templates": {
            "page_lookup": "Exact page\n- Expression Library in Journey Builder Canvas\nRelevant details\n- Use the Expression Library in the Modify Variable node to manipulate data with pre-built functions instead of custom Code Nodes.",
            "definition": "Exact page\n- Expression Library\nRelevant details\n- The Expression Library provides pre-built functions for data manipulation directly in the Modify Variable node, eliminating the need for custom code nodes.",
            "setup": "Exact page\n- Expression Library\nRelevant details\n- Open the Modify Variable node, select Expression from the Modifier dropdown, click Build Expression, add sample values, and test before saving.",
        },
        "compare_blurb": "Use the Expression Library for no-code data manipulation in the Modify Variable node.",
        "related": ["modify_variable"],
    },
    {
        "id": "wait_for_event",
        "aliases": [
            "wait for event", "wait for event node", "pause bot execution",
            "wait for user input", "event timeout", "wait node",
            "hold the flow", "inactivity nudge", "wait for trigger",
        ],
        "module_context": ["bot studio"],
        "source_boosts": {"wait-for-event": 6.0},
        "source_penalties": {},
        "display": "Wait for Event Node",
        "page_display": "Wait for Event",
        "module": "Bot Studio",
        "templates": {
            "page_lookup": "Exact page\n- Wait for Event\nRelevant details\n- Use the Wait for Event Node to pause bot execution until a specific user input or time-based trigger occurs.",
            "definition": "Exact page\n- Wait for Event\nRelevant details\n- The Wait for Event Node pauses the bot's execution and waits for a specific user input or a time-based trigger before proceeding. Maximum timeout is 24 hours.",
            "setup": "Exact page\n- Wait for Event\nRelevant details\n- Add the Wait for Event Node in Journey Builder, configure the event type and timeout duration, then Save & Deploy.",
        },
        "compare_blurb": "Use the Wait for Event Node to pause bot flow until a user event or timeout occurs.",
        "related": ["prompt_node", "trigger_event"],
    },
    {
        "id": "address_node",
        "aliases": [
            "address node", "collect address", "address form",
            "whatsapp address", "waba address", "location collection",
            "address collection node",
        ],
        "module_context": ["bot studio"],
        "source_boosts": {"address-node": 6.0},
        "source_penalties": {},
        "display": "Address Node",
        "page_display": "Address Node",
        "module": "Bot Studio",
        "templates": {
            "page_lookup": "Exact page\n- Address Node\nRelevant details\n- Use the Address Node to collect user addresses via a WhatsApp form. Supported WABA regions include India and Singapore.",
            "definition": "Exact page\n- Address Node\nRelevant details\n- The Address Node sends an address form on WhatsApp for users to input their details. Configure by selecting India or Singapore as the WABA region.",
            "setup": "Exact page\n- Address Node\nRelevant details\n- Add the Address Node in Journey Builder, select the WABA region (India or Singapore), deploy the journey, and users will receive the address form on WhatsApp.",
        },
        "compare_blurb": "Use the Address Node for collecting user addresses via WhatsApp forms.",
        "related": ["prompt_node"],
    },
    {
        "id": "ai_node",
        "aliases": [
            "ai node", "ai admin node", "link ai workspace",
            "ai enabled journey", "ai faq", "ai workspace node",
            "connect ai admin", "trained workspace",
        ],
        "module_context": ["bot studio"],
        "source_boosts": {"ai-node": 6.0},
        "source_penalties": {},
        "display": "AI Node",
        "page_display": "AI Node",
        "module": "Bot Studio",
        "templates": {
            "page_lookup": "Exact page\n- AI Node\nRelevant details\n- Use the AI Node to link journeys with trained AI Admin workspaces for answering customer FAQs.",
            "definition": "Exact page\n- AI Node\nRelevant details\n- The AI Node links Journey Builder journeys with trained AI Admin workspaces. When a user asks a query, the AI-enabled journey provides the best relevant answer.",
            "setup": "Exact page\n- AI Node\nRelevant details\n- Add the AI Node in Journey Builder, select the trained AI Admin workspace, configure the response format, then Save & Deploy.",
        },
        "compare_blurb": "Use the AI Node to connect Journey Builder with AI Admin trained workspaces.",
        "related": ["prompt_node"],
    },
    {
        "id": "sticky_journey",
        "aliases": [
            "sticky journey", "proactive persistent message",
            "persistent node", "sticky journey upgrade",
            "unfinished journey", "return to journey",
            "persistent prompt", "sticky bot",
        ],
        "module_context": ["bot studio"],
        "source_boosts": {"proactive-persistent-message": 6.0},
        "source_penalties": {},
        "display": "Sticky Journey (Proactive Persistent Message)",
        "page_display": "Proactive Persistent Message (Sticky Journey Upgrade)",
        "module": "Bot Studio",
        "templates": {
            "page_lookup": "Exact page\n- Proactive Persistent Message (Sticky Journey Upgrade)\nRelevant details\n- Sticky Journeys let users return to an unfinished journey. Prompt, Reply, Quick Reply, and List Nodes can act as persistent nodes.",
            "definition": "Exact page\n- Proactive Persistent Message\nRelevant details\n- For sticky journeys, wait-for-event based nodes feature a customizable experience ensuring end users can return to unfinished journeys if context changes.",
        },
        "compare_blurb": "Use Sticky Journeys to let users resume unfinished bot flows.",
        "related": ["prompt_node", "wait_for_event"],
    },
    {
        "id": "agent_assist_overview",
        "aliases": [
            "about agent assist", "what is agent assist",
            "agent assist overview", "agent assist platform",
            "omnichannel conversation platform", "agent assist module",
        ],
        "module_context": ["agent assist"],
        "source_boosts": {"about-agent-assist": 6.0},
        "source_penalties": {},
        "display": "About Agent Assist",
        "page_display": "About Agent Assist",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- About Agent Assist\nRelevant details\n- Agent Assist is an omnichannel conversation platform that unifies messaging channels, streamlines customer support operations, and enhances agent productivity.",
            "definition": "Exact page\n- About Agent Assist\nRelevant details\n- Agent Assist is an omnichannel conversation platform that unifies messaging channels, streamlines support operations, and enhances agent productivity with workflows and analytics.",
        },
        "compare_blurb": "Agent Assist is the live-agent conversation platform with routing, analytics, and automation.",
        "related": ["assignment_rules", "live_monitoring"],
    },
    {
        "id": "tags_mgmt",
        "aliases": [
            "tags", "chat tags", "create tags", "tag management",
            "auto assign tags", "filter by tags", "tag based routing",
            "add tag to chat",
        ],
        "module_context": ["agent assist"],
        "source_boosts": {"others-tags": 6.0},
        "source_penalties": {},
        "display": "Tags",
        "page_display": "Others: Tags",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- Others: Tags\nRelevant details\n- Tags are used to define a set of chats. Add tags to chats for custom views, auto-assignment, filtering, and analytics.",
            "definition": "Exact page\n- Others: Tags\nRelevant details\n- Tags let brands categorize chats for custom views, automatic assignment, filtering, and better analytics.",
            "setup": "Exact page\n- Others: Tags\nRelevant details\n- Go to Agent Assist → Settings → Others → Tags, create a new tag, then use it in views or assignment rules.",
        },
        "compare_blurb": "Use Tags to categorize chats for filtering, auto-assignment, and analytics.",
        "related": ["assignment_rules"],
    },
    {
        "id": "views_mgmt",
        "aliases": [
            "views", "chat views", "default views", "shared views",
            "my views", "create view", "custom view", "view settings",
            "agent views", "chat navigation views",
        ],
        "module_context": ["agent assist"],
        "source_boosts": {
            "others-views": 6.0,
            "efficient-chat-navigation-for-different-user-roles-through-views": 4.0,
        },
        "source_penalties": {},
        "display": "Views",
        "page_display": "Others: Views",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- Others: Views\nRelevant details\n- Views let agents access chats of a particular category in a dedicated bucket. Types: Default, Shared, and My Views.",
            "definition": "Exact page\n- Others: Views\nRelevant details\n- A View is a dedicated bucket for chats matching specified conditions. Views can be team-wide (Shared) or personal (My Views).",
            "setup": "Exact page\n- Others: Views\nRelevant details\n- Go to Agent Assist → Settings → Views → Add View. Specify name, access level (team or individual), and matching conditions.",
        },
        "compare_blurb": "Use Views to create filtered chat buckets for agents based on conditions like tags or status.",
        "related": ["tags_mgmt"],
    },
    {
        "id": "integrations_webhooks",
        "aliases": [
            "integrations webhooks", "webhook integration",
            "integration webhook setup", "webhook callback url",
            "webhook events", "webhook configuration integration",
        ],
        "module_context": ["integrations"],
        "source_boosts": {"integrations/webhooks": 5.0, "webhooks": 4.0},
        "source_penalties": {},
        "display": "Integrations: Webhooks",
        "page_display": "Webhooks (Integrations)",
        "module": "Integrations",
        "templates": {
            "page_lookup": "Exact page\n- Webhooks (Integrations)\nRelevant details\n- Use the Integrations Webhooks page to configure callback URLs for events like message delivery, read receipts, and more.",
            "setup": "Exact page\n- Webhooks (Integrations)\nRelevant details\n- Navigate to Integrations → Webhooks, add your callback URL, select events, and save.",
        },
        "compare_blurb": "Use Integrations Webhooks to configure callback URLs for platform events.",
        "related": ["webhooks"],
    },
    # ---- Phase 4b: high-impact partial categories ----
    {
        "id": "csat",
        "aliases": [
            "customer satisfaction", "csat", "feedback form",
            "satisfaction survey", "feedback rating", "thumbs stars emoji",
            "conditional questions", "customer feedback",
        ],
        "module_context": ["agent assist"],
        "source_boosts": {
            "response-management-customer-satisfaction": 6.0,
            "insights-customer-feedback-dashboard": 4.0,
        },
        "source_penalties": {},
        "display": "Customer Satisfaction (CSAT)",
        "page_display": "Response Management: Customer Satisfaction",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- Response Management: Customer Satisfaction\nRelevant details\n- Use this page to configure feedback forms for collecting customer ratings and suggestions.",
            "definition": "Exact page\n- Customer Satisfaction\nRelevant details\n- CSAT feedback forms collect customer feedback, measure satisfaction levels, identify improvement areas, and gather product suggestions. Rating types include Thumbs, Stars, and Emoji.",
            "setup": "Exact page\n- Response Management: Customer Satisfaction\nRelevant details\n- Go to Agent Assist → Settings → Response Management → Customer Satisfaction, create a feedback form with rating type and conditional questions, then activate.",
        },
        "compare_blurb": "Use CSAT feedback forms to collect customer satisfaction ratings and suggestions.",
        "related": ["auto_replies"],
    },
    {
        "id": "canned_responses",
        "aliases": [
            "canned responses", "canned reply", "template response",
            "quick reply template", "saved responses", "response templates",
            "canned response categories",
        ],
        "module_context": ["agent assist"],
        "source_boosts": {"others-canned-responses": 6.0},
        "source_penalties": {},
        "display": "Canned Responses",
        "page_display": "Others: Canned Responses",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- Others: Canned Responses\nRelevant details\n- Canned Responses let agents save and reuse template replies for common customer inquiries.",
            "setup": "Exact page\n- Others: Canned Responses\nRelevant details\n- Go to Agent Assist → Settings → Others → Canned Responses, create categories, and add template responses for agents to use.",
        },
        "compare_blurb": "Use Canned Responses for pre-saved template replies agents can use for common inquiries.",
        "related": ["auto_replies"],
    },
    {
        "id": "sla",
        "aliases": [
            "sla", "service level agreement", "first response time",
            "resolution time", "response time sla", "sla settings",
            "sla conditions", "frt sla", "art sla",
        ],
        "module_context": ["agent assist"],
        "source_boosts": {"chat-management-sla": 6.0},
        "source_penalties": {},
        "display": "Chat Management: SLA",
        "page_display": "Chat Management: SLA",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- Chat Management: SLA\nRelevant details\n- SLA settings define conditions and time targets for First Response Time, Response Time, and Resolution Time.",
            "definition": "Exact page\n- Chat Management: SLA\nRelevant details\n- Service Level Agreements set time-based targets for agent responses. Configure conditions for First Response Time (FRT), Response Time, and Resolution Time.",
        },
        "compare_blurb": "Use SLA to define time targets for first response, response, and resolution.",
        "related": ["assignment_rules", "live_monitoring"],
    },
    {
        "id": "global_search",
        "aliases": [
            "global search", "search chats", "find chats",
            "search archived chats", "export csv", "chat export",
            "search all chats", "export chat data",
        ],
        "module_context": ["agent assist"],
        "source_boosts": {"simplify-your-search-with-global-search": 6.0},
        "source_penalties": {},
        "display": "Global Search",
        "page_display": "Global Search",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- Global Search\nRelevant details\n- Use Global Search to find all chats in the system. Search archived chats up to 6 months and export data as CSV.",
            "setup": "Exact page\n- Global Search\nRelevant details\n- Open Agent Assist → Global Search, enter search criteria, filter by date/status/tags, and optionally export results as CSV with selectable columns.",
        },
        "compare_blurb": "Use Global Search to find and export chat data across the system.",
        "related": ["views_mgmt"],
    },
    {
        "id": "bulk_actions",
        "aliases": [
            "bulk actions", "bulk assignment", "bulk tagging",
            "bulk resolution", "bulk reply", "multiple chats",
            "bulk priority", "bulk operations",
        ],
        "module_context": ["agent assist"],
        "source_boosts": {"streamlining-your-workflow-with-bulk-actions": 6.0},
        "source_penalties": {},
        "display": "Bulk Actions",
        "page_display": "Bulk Actions",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- Bulk Actions\nRelevant details\n- Perform bulk operations on multiple chats: assignment, tagging, priority changes, resolution, private notes, and bulk replies.",
            "setup": "Exact page\n- Bulk Actions\nRelevant details\n- Select multiple chats in Agent Assist, then use the bulk actions menu for assignment, tagging, priority, resolution, or bulk reply.",
        },
        "compare_blurb": "Use Bulk Actions to perform operations on multiple chats simultaneously.",
        "related": ["tags_mgmt", "assignment_rules"],
    },
    {
        "id": "insights_agent",
        "aliases": [
            "agent summary", "agent report", "agent productivity",
            "agent timesheet", "agent performance", "insights agent",
            "agent frt", "agent art", "agent resolution time",
            "agent aht", "agent login logout",
        ],
        "module_context": ["agent assist"],
        "source_boosts": {
            "insights-agent-summary": 6.0,
            "insights-agent-timesheet": 5.0,
        },
        "source_penalties": {},
        "display": "Insights: Agent Summary",
        "page_display": "Insights: Agent Summary",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- Insights: Agent Summary\nRelevant details\n- The Agent Summary report shows Chats Assigned, FRT, ART, Resolution Time, and AHT per agent.",
            "definition": "Exact page\n- Insights: Agent Summary\nRelevant details\n- Agent Summary provides productivity metrics, efficiency data, response times, and SLA adherence. The Agent Timesheet shows Login/Logout, Active/Inactive, Activity, and Duration tabs.",
        },
        "compare_blurb": "Use Agent Summary for agent productivity, response times, and SLA adherence metrics.",
        "related": ["live_monitoring", "sla"],
    },
    {
        "id": "insights_chat",
        "aliases": [
            "chat summary", "chat report", "chat analytics",
            "insights chat", "frt buckets", "resolution time report",
            "business hours metrics", "calendar hours metrics",
            "chat volume", "chat insights",
        ],
        "module_context": ["agent assist"],
        "source_boosts": {"insights-chat-summary": 6.0},
        "source_penalties": {},
        "display": "Insights: Chat Summary",
        "page_display": "Insights: Chat Summary",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- Insights: Chat Summary\nRelevant details\n- Chat Summary shows chat-level analytics including FRT buckets, resolution time, and volume trends.",
            "definition": "Exact page\n- Insights: Chat Summary\nRelevant details\n- Chat Summary analytics includes Business Hours vs Calendar Hours metrics, FRT buckets (0-5s, 5-10s, 10-30s, 30s-1min), and resolution time distribution.",
        },
        "compare_blurb": "Use Chat Summary for chat-level analytics, FRT distribution, and resolution metrics.",
        "related": ["insights_agent", "sla"],
    },
    {
        "id": "insights_raw_data",
        "aliases": [
            "raw data export", "export raw data", "chat data export",
            "insights export", "csv export", "raw data fields",
            "session id", "underlying raw data",
        ],
        "module_context": ["agent assist"],
        "source_boosts": {
            "exploring-insights-and-exporting-raw-data": 6.0,
            "underlying-raw-data-for-chat-summary": 5.0,
        },
        "source_penalties": {},
        "display": "Insights: Raw Data Export",
        "page_display": "Exploring Insights & Exporting Raw Data",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- Exploring Insights & Exporting Raw Data\nRelevant details\n- Export raw data fields including session_id, team_id, FRT, Resolution Time, and more as CSV.",
            "definition": "Exact page\n- Exploring Insights & Exporting Raw Data\nRelevant details\n- The raw data export provides chat performance, agent productivity, team metrics, and customer feedback data in CSV format.",
        },
        "compare_blurb": "Use Raw Data Export for detailed CSV exports of chat and agent metrics.",
        "related": ["insights_chat", "insights_agent"],
    },
    {
        "id": "template_window",
        "aliases": [
            "24 hour window", "messaging window", "template after window",
            "send template after", "whatsapp window", "24 hour messaging",
            "window expires", "template window",
        ],
        "module_context": ["agent assist"],
        "source_boosts": {"sending-templates-after-the-24-hour-window": 6.0},
        "source_penalties": {},
        "display": "Sending Templates After 24-Hour Window",
        "page_display": "Sending Templates After the 24-Hour Window",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- Sending Templates After the 24-Hour Window\nRelevant details\n- Use this page to learn how to send marketing templates after the WhatsApp 24-hour messaging window expires.",
            "setup": "Exact page\n- Sending Templates After the 24-Hour Window\nRelevant details\n- When the 24-hour window expires, use pre-approved marketing templates to re-engage customers while staying compliant.",
        },
        "compare_blurb": "Use approved templates to message customers after the 24-hour WhatsApp window.",
        "related": ["auto_replies"],
    },
    {
        "id": "wallet",
        "aliases": [
            "wallet", "wallet overview", "billing wallet",
            "gupshup wallet", "payment wallet", "converse wallet",
            "wallet balance", "top up wallet",
        ],
        "module_context": ["wallet"],
        "source_boosts": {"wallet-overview": 6.0},
        "source_penalties": {},
        "display": "Wallet Overview",
        "page_display": "Wallet Overview",
        "module": "Wallet",
        "templates": {
            "page_lookup": "Exact page\n- Wallet Overview\nRelevant details\n- The Gupshup Wallet is used for paying for WhatsApp and Instagram usage on Converse.",
            "definition": "Exact page\n- Wallet Overview\nRelevant details\n- The Wallet is the billing mechanism for WhatsApp and Instagram message usage on the Gupshup Converse platform.",
        },
        "compare_blurb": "Use the Wallet for billing and payment of WhatsApp/Instagram messaging.",
        "related": [],
    },
    # ---- Phase 4c: AI Admin / Agent categories ----
    {
        "id": "ai_admin_workspace",
        "aliases": [
            "ai workspace", "create workspace", "ai admin workspace",
            "workspace validation", "workspace audit",
            "ai admin create workspace", "workspace settings",
        ],
        "module_context": ["ai admin"],
        "source_boosts": {
            "creating-a-workspace": 6.0,
            "workspace-validation": 5.0,
            "workspace-audit": 5.0,
            "workspace": 4.0,
        },
        "source_penalties": {},
        "display": "AI Admin: Workspace",
        "page_display": "Creating a Workspace",
        "module": "AI Admin",
        "templates": {
            "page_lookup": "Exact page\n- Creating a Workspace\nRelevant details\n- The workspace is the configuration hub for defining AI agent components. It is the first step to integrate an agent into a journey.",
            "definition": "Exact page\n- AI Admin: Workspace\nRelevant details\n- The workspace defines and manages AI agent components. Workspace Validation checks predefined conditions; Workspace Audit shows change history.",
            "setup": "Exact page\n- Creating a Workspace\nRelevant details\n- Go to AI Admin, click Create Workspace, configure the agent components, then validate and publish.",
        },
        "compare_blurb": "Use the AI Admin Workspace to create and configure AI agents.",
        "related": ["ai_node"],
    },
    {
        "id": "ai_admin_training",
        "aliases": [
            "ai training", "train ai", "website training", "document training",
            "text training", "catalog training", "train using url",
            "train using documents", "upload training data",
            "scraping depth", "content training", "ai admin training",
        ],
        "module_context": ["ai admin"],
        "source_boosts": {
            "website-training": 6.0,
            "document-training": 6.0,
            "text-training": 6.0,
            "catalog-training": 6.0,
            "content-training": 5.0,
        },
        "source_penalties": {},
        "display": "AI Admin: Training",
        "page_display": "AI Admin Training",
        "module": "AI Admin",
        "templates": {
            "page_lookup": "Exact page\n- AI Admin Training (Website / Document / Text / Catalog)\nRelevant details\n- Train AI using website URLs with scraping depth controls, uploaded documents, plain text input, or product catalog data.",
            "setup": "Exact page\n- AI Admin Training\nRelevant details\n- Go to AI Admin → Workspace → Training, choose a source type (Website, Document, Text, or Catalog), upload or enter data, and publish the workspace.",
        },
        "compare_blurb": "Use AI Admin Training to feed data into AI workspaces from URLs, documents, text, or catalogs.",
        "related": ["ai_admin_workspace"],
    },
    {
        "id": "ai_admin_intents",
        "aliases": [
            "ai intents", "intent creation", "create intent",
            "intent naming", "intent description", "ai admin intents",
            "intent guidelines", "user intent",
        ],
        "module_context": ["ai admin"],
        "source_boosts": {
            "intent-creation": 6.0,
            "intent-and-entity": 5.0,
            "naming-guidelines-for-intent-and-entity": 4.0,
            "intent-description": 4.0,
        },
        "source_penalties": {},
        "display": "AI Admin: Intents",
        "page_display": "Intent Creation",
        "module": "AI Admin",
        "templates": {
            "page_lookup": "Exact page\n- Intent Creation\nRelevant details\n- Create intents to define the goal or purpose behind user input (e.g., track_order_status).",
            "definition": "Exact page\n- AI Admin: Intents\nRelevant details\n- Intents represent the goal or purpose behind user input. Use naming guidelines like snake_case and descriptive names.",
        },
        "compare_blurb": "Intents define the goal behind user input in AI Admin.",
        "related": ["ai_admin_entities"],
    },
    {
        "id": "ai_admin_entities",
        "aliases": [
            "ai entities", "entity creation", "create entity",
            "entity description", "ai admin entities",
            "entities in ai admin",
        ],
        "module_context": ["ai admin"],
        "source_boosts": {
            "entity-creation": 6.0,
            "entity-description": 5.0,
            "intent-and-entity": 4.0,
        },
        "source_penalties": {},
        "display": "AI Admin: Entities",
        "page_display": "Entity Creation",
        "module": "AI Admin",
        "templates": {
            "page_lookup": "Exact page\n- Entity Creation\nRelevant details\n- Create entities to define specific pieces of information in user input (e.g., destination, date).",
            "definition": "Exact page\n- AI Admin: Entities\nRelevant details\n- Entities are specific pieces of information within user input, such as destination, date, or product name.",
        },
        "compare_blurb": "Entities define specific data pieces in user input (e.g., dates, locations).",
        "related": ["ai_admin_intents"],
    },
    {
        "id": "ai_admin_evaluate",
        "aliases": [
            "evaluate ai", "ai evaluate", "evaluate workspace",
            "ai admin evaluate", "generate qa", "evaluate tab",
            "ai testing", "evaluate performance",
        ],
        "module_context": ["ai admin"],
        "source_boosts": {"evaluate": 6.0},
        "source_penalties": {},
        "display": "AI Admin: Evaluate",
        "page_display": "Evaluate",
        "module": "AI Admin",
        "templates": {
            "page_lookup": "Exact page\n- Evaluate\nRelevant details\n- Use the Evaluate tab to generate Q&A from trained content via topic prompt or file upload to test workspace accuracy.",
            "setup": "Exact page\n- Evaluate\nRelevant details\n- Go to AI Admin → Workspace → Evaluate, generate Q&A from trained content, and review results to improve accuracy.",
        },
        "compare_blurb": "Use Evaluate to test AI workspace accuracy with generated Q&A pairs.",
        "related": ["ai_admin_workspace", "ai_admin_training"],
    },
    {
        "id": "ai_admin_monitoring",
        "aliases": [
            "ai monitoring", "ai admin monitoring", "workspace monitoring",
            "llm consumption", "ai dashboard", "monitoring dashboard",
            "ai admin dashboard",
        ],
        "module_context": ["ai admin"],
        "source_boosts": {"monitoring": 6.0, "llm-consumption": 5.0},
        "source_penalties": {},
        "display": "AI Admin: Monitoring",
        "page_display": "Monitoring",
        "module": "AI Admin",
        "templates": {
            "page_lookup": "Exact page\n- Monitoring\nRelevant details\n- The AI Admin Monitoring dashboard shows workspace changes and LLM consumption metrics.",
            "definition": "Exact page\n- AI Admin: Monitoring\nRelevant details\n- View workspace changes, LLM consumption, and usage metrics from the AI Admin monitoring dashboard.",
        },
        "compare_blurb": "Use AI Admin Monitoring to track workspace changes and LLM usage.",
        "related": ["ai_admin_workspace"],
    },
    {
        "id": "ai_admin_teach",
        "aliases": [
            "ai teach", "teach utterances", "teach csv",
            "ai admin teach", "utterance training",
            "faq intent", "product search intent",
        ],
        "module_context": ["ai admin"],
        "source_boosts": {
            "teach": 6.0,
            "teach-csv-file": 5.0,
            "teach-utterance-untraining": 4.0,
        },
        "source_penalties": {},
        "display": "AI Admin: Teach",
        "page_display": "Teach",
        "module": "AI Admin",
        "templates": {
            "page_lookup": "Exact page\n- Teach\nRelevant details\n- Add utterances manually or via CSV to train intent/entity mappings. Includes FAQ and Product Search intent types.",
            "setup": "Exact page\n- Teach\nRelevant details\n- Go to AI Admin → Workspace → Teach, add utterances manually or upload CSV, then map intents and entities.",
        },
        "compare_blurb": "Use Teach to add utterances and map intents/entities for AI training.",
        "related": ["ai_admin_intents", "ai_admin_entities"],
    },
    {
        "id": "ai_admin_tags",
        "aliases": [
            "content tags", "ai content tags", "ai admin tags",
            "content labeling", "tag content", "categorize content",
        ],
        "module_context": ["ai admin"],
        "source_boosts": {"content-tags": 6.0},
        "source_penalties": {},
        "display": "AI Admin: Content Tags",
        "page_display": "Content Tags",
        "module": "AI Admin",
        "templates": {
            "page_lookup": "Exact page\n- Content Tags\nRelevant details\n- Content tags are labels to categorize uploaded content by subject, context, or theme for easier retrieval and differentiated responses.",
            "definition": "Exact page\n- Content Tags\nRelevant details\n- Content Tags label training content by subject or theme so the AI can differentiate responses based on context.",
        },
        "compare_blurb": "Use Content Tags to categorize training content for context-aware AI responses.",
        "related": ["ai_admin_training"],
    },
    {
        "id": "ai_agent",
        "aliases": [
            "ai agent", "ai agents", "agentic llm", "ace llm",
            "ai agent developer mode", "ai skills", "ai tools",
            "digital assistant", "generative ai agent",
            "ai agent guardrails", "agent personality",
        ],
        "module_context": ["ai admin"],
        "source_boosts": {
            "ace-and-agentic-llm-overview": 6.0,
            "ai-agents-developer-mode": 6.0,
            "ai-agent-guardrails-developer-mode": 5.0,
            "skills-developer-mode": 4.0,
            "tools-developer-mode": 4.0,
        },
        "source_penalties": {},
        "display": "AI Agent",
        "page_display": "AI Agent (Developer Mode)",
        "module": "AI Admin",
        "templates": {
            "page_lookup": "Exact page\n- AI Agents (Developer Mode)\nRelevant details\n- AI Agents are digital assistants for multi-turn conversations on WhatsApp and Web, powered by Gupshup's ACE Agentic LLM.",
            "definition": "Exact page\n- AI Agent\nRelevant details\n- Gupshup AI Agents are generative AI digital assistants for marketing, commerce, and support conversations. The ACE Agentic LLM powers multi-turn conversations.",
            "setup": "Exact page\n- AI Agents (Developer Mode)\nRelevant details\n- In AI Admin, go to Developer Mode → AI Agents, configure Skills and Tools, set guardrails, and publish.",
        },
        "compare_blurb": "AI Agents are generative assistants powered by ACE Agentic LLM for multi-turn conversations.",
        "related": ["ai_admin_workspace", "ai_admin_training"],
    },
```

## Step 2 — Add entries to `CONCEPT_REGISTRY` in `kb_search.py`

Find the LAST entry in the `CONCEPT_REGISTRY` list (the `privacy_policy` entry ending with `},`).

**After** that entry and **before** the closing `]`, insert the following entries:

```python
    {
        "id": "whatsapp_flow",
        "aliases": [
            "whatsapp flow", "flow trigger", "static flow", "dynamic flow",
            "launch a whatsapp flow", "whatsapp flow node",
            "whatsapp static flow", "whatsapp dynamic flow",
            "terminal node flow", "flow response",
        ],
        "source_boosts": {
            "whatsapp-flow": 6.0,
            "flow-trigger": 5.0,
            "how-to-create-whatsapp-static-flows": 4.0,
        },
        "source_penalties": {},
    },
    # ---- Phase 4a: double-zero categories ----
    {
        "id": "expression_library",
        "aliases": [
            "expression library", "expression functions", "build expression",
            "modify variable expression", "expression editor",
            "data manipulation expression", "pre built functions",
            "expression instead of code node", "expression library functions",
        ],
        "source_boosts": {
            "expression-library-in-journey-builder-canvas": 6.0,
            "extracting-and-manipulating-data-using-expression-library-functions": 5.0,
        },
        "source_penalties": {},
    },
    {
        "id": "wait_for_event",
        "aliases": [
            "wait for event", "wait for event node", "pause bot execution",
            "wait for user input", "event timeout", "wait node",
            "hold the flow", "inactivity nudge", "wait for trigger",
        ],
        "source_boosts": {"wait-for-event": 6.0},
        "source_penalties": {},
    },
    {
        "id": "address_node",
        "aliases": [
            "address node", "collect address", "address form",
            "whatsapp address", "waba address", "location collection",
            "address collection node",
        ],
        "source_boosts": {"address-node": 6.0},
        "source_penalties": {},
    },
    {
        "id": "ai_node",
        "aliases": [
            "ai node", "ai admin node", "link ai workspace",
            "ai enabled journey", "ai faq", "ai workspace node",
            "connect ai admin", "trained workspace",
        ],
        "source_boosts": {"ai-node": 6.0},
        "source_penalties": {},
    },
    {
        "id": "sticky_journey",
        "aliases": [
            "sticky journey", "proactive persistent message",
            "persistent node", "sticky journey upgrade",
            "unfinished journey", "return to journey",
            "persistent prompt", "sticky bot",
        ],
        "source_boosts": {"proactive-persistent-message": 6.0},
        "source_penalties": {},
    },
    {
        "id": "agent_assist_overview",
        "aliases": [
            "about agent assist", "what is agent assist",
            "agent assist overview", "agent assist platform",
            "omnichannel conversation platform", "agent assist module",
        ],
        "source_boosts": {"about-agent-assist": 6.0},
        "source_penalties": {},
    },
    {
        "id": "tags_mgmt",
        "aliases": [
            "tags", "chat tags", "create tags", "tag management",
            "auto assign tags", "filter by tags", "tag based routing",
            "add tag to chat",
        ],
        "source_boosts": {"others-tags": 6.0},
        "source_penalties": {},
    },
    {
        "id": "views_mgmt",
        "aliases": [
            "views", "chat views", "default views", "shared views",
            "my views", "create view", "custom view", "view settings",
            "agent views", "chat navigation views",
        ],
        "source_boosts": {
            "others-views": 6.0,
            "efficient-chat-navigation-for-different-user-roles-through-views": 4.0,
        },
        "source_penalties": {},
    },
    {
        "id": "integrations_webhooks",
        "aliases": [
            "integrations webhooks", "webhook integration",
            "integration webhook setup", "webhook callback url",
            "webhook events", "webhook configuration integration",
        ],
        "source_boosts": {"integrations/webhooks": 5.0, "webhooks": 4.0},
        "source_penalties": {},
    },
    # ---- Phase 4b: high-impact partial categories ----
    {
        "id": "csat",
        "aliases": [
            "customer satisfaction", "csat", "feedback form",
            "satisfaction survey", "feedback rating", "thumbs stars emoji",
            "conditional questions", "customer feedback",
        ],
        "source_boosts": {
            "response-management-customer-satisfaction": 6.0,
            "insights-customer-feedback-dashboard": 4.0,
        },
        "source_penalties": {},
    },
    {
        "id": "canned_responses",
        "aliases": [
            "canned responses", "canned reply", "template response",
            "quick reply template", "saved responses", "response templates",
            "canned response categories",
        ],
        "source_boosts": {"others-canned-responses": 6.0},
        "source_penalties": {},
    },
    {
        "id": "sla",
        "aliases": [
            "sla", "service level agreement", "first response time",
            "resolution time", "response time sla", "sla settings",
            "sla conditions", "frt sla", "art sla",
        ],
        "source_boosts": {"chat-management-sla": 6.0},
        "source_penalties": {},
    },
    {
        "id": "global_search",
        "aliases": [
            "global search", "search chats", "find chats",
            "search archived chats", "export csv", "chat export",
            "search all chats", "export chat data",
        ],
        "source_boosts": {"simplify-your-search-with-global-search": 6.0},
        "source_penalties": {},
    },
    {
        "id": "bulk_actions",
        "aliases": [
            "bulk actions", "bulk assignment", "bulk tagging",
            "bulk resolution", "bulk reply", "multiple chats",
            "bulk priority", "bulk operations",
        ],
        "source_boosts": {"streamlining-your-workflow-with-bulk-actions": 6.0},
        "source_penalties": {},
    },
    {
        "id": "insights_agent",
        "aliases": [
            "agent summary", "agent report", "agent productivity",
            "agent timesheet", "agent performance", "insights agent",
            "agent frt", "agent art", "agent resolution time",
            "agent aht", "agent login logout",
        ],
        "source_boosts": {
            "insights-agent-summary": 6.0,
            "insights-agent-timesheet": 5.0,
        },
        "source_penalties": {},
    },
    {
        "id": "insights_chat",
        "aliases": [
            "chat summary", "chat report", "chat analytics",
            "insights chat", "frt buckets", "resolution time report",
            "business hours metrics", "calendar hours metrics",
            "chat volume", "chat insights",
        ],
        "source_boosts": {"insights-chat-summary": 6.0},
        "source_penalties": {},
    },
    {
        "id": "insights_raw_data",
        "aliases": [
            "raw data export", "export raw data", "chat data export",
            "insights export", "csv export", "raw data fields",
            "session id", "underlying raw data",
        ],
        "source_boosts": {
            "exploring-insights-and-exporting-raw-data": 6.0,
            "underlying-raw-data-for-chat-summary": 5.0,
        },
        "source_penalties": {},
    },
    {
        "id": "template_window",
        "aliases": [
            "24 hour window", "messaging window", "template after window",
            "send template after", "whatsapp window", "24 hour messaging",
            "window expires", "template window",
        ],
        "source_boosts": {"sending-templates-after-the-24-hour-window": 6.0},
        "source_penalties": {},
    },
    {
        "id": "wallet",
        "aliases": [
            "wallet", "wallet overview", "billing wallet",
            "gupshup wallet", "payment wallet", "converse wallet",
            "wallet balance", "top up wallet",
        ],
        "source_boosts": {"wallet-overview": 6.0},
        "source_penalties": {},
    },
    # ---- Phase 4c: AI Admin / Agent categories ----
    {
        "id": "ai_admin_workspace",
        "aliases": [
            "ai workspace", "create workspace", "ai admin workspace",
            "workspace validation", "workspace audit",
            "ai admin create workspace", "workspace settings",
        ],
        "source_boosts": {
            "creating-a-workspace": 6.0,
            "workspace-validation": 5.0,
            "workspace-audit": 5.0,
            "workspace": 4.0,
        },
        "source_penalties": {},
    },
    {
        "id": "ai_admin_training",
        "aliases": [
            "ai training", "train ai", "website training", "document training",
            "text training", "catalog training", "train using url",
            "train using documents", "upload training data",
            "scraping depth", "content training", "ai admin training",
        ],
        "source_boosts": {
            "website-training": 6.0,
            "document-training": 6.0,
            "text-training": 6.0,
            "catalog-training": 6.0,
            "content-training": 5.0,
        },
        "source_penalties": {},
    },
    {
        "id": "ai_admin_intents",
        "aliases": [
            "ai intents", "intent creation", "create intent",
            "intent naming", "intent description", "ai admin intents",
            "intent guidelines", "user intent",
        ],
        "source_boosts": {
            "intent-creation": 6.0,
            "intent-and-entity": 5.0,
            "naming-guidelines-for-intent-and-entity": 4.0,
            "intent-description": 4.0,
        },
        "source_penalties": {},
    },
    {
        "id": "ai_admin_entities",
        "aliases": [
            "ai entities", "entity creation", "create entity",
            "entity description", "ai admin entities",
            "entities in ai admin",
        ],
        "source_boosts": {
            "entity-creation": 6.0,
            "entity-description": 5.0,
            "intent-and-entity": 4.0,
        },
        "source_penalties": {},
    },
    {
        "id": "ai_admin_evaluate",
        "aliases": [
            "evaluate ai", "ai evaluate", "evaluate workspace",
            "ai admin evaluate", "generate qa", "evaluate tab",
            "ai testing", "evaluate performance",
        ],
        "source_boosts": {"evaluate": 6.0},
        "source_penalties": {},
    },
    {
        "id": "ai_admin_monitoring",
        "aliases": [
            "ai monitoring", "ai admin monitoring", "workspace monitoring",
            "llm consumption", "ai dashboard", "monitoring dashboard",
            "ai admin dashboard",
        ],
        "source_boosts": {"monitoring": 6.0, "llm-consumption": 5.0},
        "source_penalties": {},
    },
    {
        "id": "ai_admin_teach",
        "aliases": [
            "ai teach", "teach utterances", "teach csv",
            "ai admin teach", "utterance training",
            "faq intent", "product search intent",
        ],
        "source_boosts": {
            "teach": 6.0,
            "teach-csv-file": 5.0,
            "teach-utterance-untraining": 4.0,
        },
        "source_penalties": {},
    },
    {
        "id": "ai_admin_tags",
        "aliases": [
            "content tags", "ai content tags", "ai admin tags",
            "content labeling", "tag content", "categorize content",
        ],
        "source_boosts": {"content-tags": 6.0},
        "source_penalties": {},
    },
    {
        "id": "ai_agent",
        "aliases": [
            "ai agent", "ai agents", "agentic llm", "ace llm",
            "ai agent developer mode", "ai skills", "ai tools",
            "digital assistant", "generative ai agent",
            "ai agent guardrails", "agent personality",
        ],
        "source_boosts": {
            "ace-and-agentic-llm-overview": 6.0,
            "ai-agents-developer-mode": 6.0,
            "ai-agent-guardrails-developer-mode": 5.0,
            "skills-developer-mode": 4.0,
            "tools-developer-mode": 4.0,
        },
        "source_penalties": {},
    },
```

## Step 3 — Add new COMPARE_OVERRIDES to `kb_answer.py`

Find the `COMPARE_OVERRIDES` dictionary. After the existing entry for `("business_hours", "auto_replies", "assignment_rules")`, add these 3 new entries:

```python
    ("ai_admin_intents", "ai_admin_entities"): (
        "Use Intents when\n"
        "- You need to define the goal or purpose behind user input (e.g., track_order_status).\n"
        "Use Entities when\n"
        "- You need to extract specific data pieces from user input (e.g., destination, date, product)."
    ),
    ("insights_agent", "insights_chat"): (
        "Use Agent Summary when\n"
        "- You need per-agent productivity metrics like FRT, ART, Resolution Time, and AHT.\n"
        "Use Chat Summary when\n"
        "- You need chat-level analytics like FRT buckets, resolution time distribution, and volume trends."
    ),
    ("wait_for_event", "prompt_node"): (
        "Use Wait for Event Node when\n"
        "- You need to pause the flow and wait for an external event or timeout (up to 24 hours).\n"
        "Use Prompt Node when\n"
        "- You need to collect direct user input with validation and timeout handling."
    ),
```

---

## Smoke Tests

### kb_answer

| ID | Query | Expected |
|----|-------|----------|
| A-S1 | "What is the Expression Library and how many functions does it have?" | Answer mentions Expression Library |
| A-S2 | "What is the Wait for Event Node and what is its maximum timeout?" | Answer mentions Wait for Event |
| A-S3 | "What is Agent Assist and what does it do?" | Answer mentions Agent Assist, omnichannel |
| A-S4 | "How do I create canned responses with categories for agents?" | Answer mentions Canned Responses |
| A-S5 | "How do I create an AI workspace in AI Admin?" | Answer mentions Creating a Workspace |
| A-S6 | "How do I add Skills to an AI Agent in developer mode?" | Answer mentions AI Agents |
| A-S7 | "What is live monitoring dashboard?" | Answer mentions Live Monitoring Dashboard (existing, not regressed) |

### kb_search

| ID | Query | Expected |
|----|-------|----------|
| B-S1 | "expression library" | Top source contains expression-library |
| B-S2 | "wait for event node" | Top source contains wait-for-event |
| B-S3 | "canned responses" | Top source contains others-canned-responses |
| B-S4 | "ai admin workspace" | Top source contains creating-a-workspace |
| B-S5 | "whatsapp flow" | Top source contains whatsapp-flow (NOT empty) |
| B-S6 | "condition node" | Top source contains condition-node (existing, not regressed) |

---

## Validation Checklist

- [ ] `kb_answer` action executes successfully
- [ ] `kb_search` action executes successfully
- [ ] All smoke tests pass
- [ ] No telemetry code was modified
