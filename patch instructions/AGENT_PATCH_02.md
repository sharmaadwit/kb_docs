# Patch 2 of 9 — Concept Registry Part B (Goal Node through Live Monitoring)

**File:** `kb_answer.py`
**Depends on:** Patch 1
**Risk:** Zero — adds data only. Old behavior unchanged.
**What it does:** Extends `CONCEPT_REGISTRY` with 9 more concepts: goal_node, prompt_node, whatsapp_flow, reassign_chat, business_hours, auto_replies, assignment_rules, sticky_assignment, live_monitoring.

> **IMPORTANT — DO NOT touch telemetry code.** All Langfuse integration, tracing, span logging, and telemetry-related functions/imports must remain exactly as they are. This patch does not modify telemetry and neither should you.

## Instructions

Find the closing of `CONCEPT_REGISTRY` and the `_CONCEPT_INDEX` line that Patch 1 added:

**Find (exact):**
```
]

# Pre-build lookup by id
_CONCEPT_INDEX: Dict[str, Dict] = {c["id"]: c for c in CONCEPT_REGISTRY}
```

**Replace with:**
```python
    {
        "id": "goal_node",
        "aliases": [
            "goal node", "track milestones", "goal analytics toggle",
            "track purchase milestone", "conversion milestone",
            "milestone tracking", "count toward goal analytics",
            "goal achievement inside the flow",
            "mark a purchase or signup milestone",
            "records that a user reached a conversion milestone",
            "how do i count toward goal analytics",
        ],
        "module_context": ["journey builder", "bot studio", "journey", "flow", "goal node", "milestone tracking"],
        "source_boosts": {"goal-node": 5.0},
        "source_penalties": {"goal-analytics": -2.0, "goals/": -2.0},
        "display": "Goal Node",
        "page_display": "Goal Node",
        "module": "Bot Studio",
        "templates": {
            "setup": (
                "The documentation indicates you should use `Goal Node` for this pattern.\n"
                "\n"
                "Recommended setup\n"
                "- Add `Goal Node` at the milestone you want to track in the journey.\n"
                "- Use it to track milestone attainment for users interacting with the bot and count that step toward `Goal Analytics`.\n"
                "- If useful, enable the analytics toggle to see traversal and drop-outs for that goal."
            ),
        },
        "compare_blurb": "You need to track a conversion milestone inside a journey.",
        "related": ["goal_analytics"],
    },
    {
        "id": "prompt_node",
        "aliases": [
            "collect text user input", "which node to collect text",
            "save free-text user replies", "save free text user replies",
            "collect user input", "collect user inputs",
            "collect user inputs in text and media",
            "text and media", "typed user reply", "text response",
            "text input capture", "typed user answers",
            "free form text", "free-form text answer",
            "open text replies", "free text node", "prompt node",
            "which node is meant to ask the user a question and collect a text response",
            "what bot studio node should i use for text input capture from the user",
            "which documented node collects typed user answers inside a journey",
            "which node should be used to collect text user input",
            "what node should i use for text input capture",
            "which node captures open text input and stores it in a variable",
            "accept user input",
            "accept a user reply and reuse it in later steps",
        ],
        "module_context": ["journey builder", "bot studio", "journey"],
        "source_boosts": {"prompt-nodes": 5.0, "timeout-in-prompt-nodes": 4.0, "free-text-node": 4.0},
        "source_penalties": {
            "whatsapp-carousel": -5.0, "send-message-node": -5.0,
            "journey-builder-platform-upgrade-and-node-deprecation": -5.0,
            "ctx-goal-nodes-and-conversions-api": -5.0,
        },
        "display": "Prompt Node",
        "page_display": "Prompt Nodes",
        "module": "Bot Studio",
        "templates": {
            "setup": (
                "The documentation points to **Prompt Node** for prompt-based capture and **Free Text Node** for free-form typed input in a journey.\n"
                "\n"
                "Recommended setup\n"
                "- Add a **Prompt Node** when you need a prompt-based user-input step.\n"
                "- Use **Free Text Node** when the clearest need is to capture a free-form typed answer such as a name, feedback, or other open text.\n"
                "- Configure the question/message and validation rules.\n"
                "- To save the reply for later use, store it in a variable: use **Manage Variables** to define the variable, and connect the captured output to that variable or use **Modify Variable Node** downstream.\n"
                "\n"
                "Relevant docs\n"
                "- Prompt Nodes (capture user details, questions). Timeout and fallback: Timeout in Prompt Nodes.\n"
                "- Free Text Node supports miscellaneous typed inputs, regex-based validation, retries, and storing the answer in a variable.\n"
                "- To reuse the value: Manage Variables, Modify Variable Node.\n"
                "\n"
                "Follow-up question\n"
                "- Do you want the documented capture node, the variable-storage step, or both?"
            ),
        },
        "compare_blurb": "You need to capture text or free-form user input in a journey.",
        "related": ["manage_variables", "modify_variable"],
    },
    {
        "id": "whatsapp_flow",
        "aliases": ["flow trigger", "launch a whatsapp flow", "whatsapp flow node"],
        "module_context": ["journey builder", "whatsapp flow"],
        "source_boosts": {"whatsapp-flow": 4.0, "flow-trigger": 4.0},
        "source_penalties": {},
        "display": "WhatsApp Flow Node",
        "page_display": "WhatsApp Flow Node",
        "module": "Bot Studio",
        "templates": {
            "setup": (
                "The documentation indicates you should use the `WhatsApp Flow Node` for this pattern.\n"
                "\n"
                "Recommended setup\n"
                "- Add the `WhatsApp Flow Node` at the point in the journey where the flow should be sent.\n"
                "- Configure the required fields available in the WhatsApp Flow Node.\n"
                "- Use that node to trigger the WhatsApp Flow from the user journey."
            ),
        },
        "compare_blurb": "You need to trigger a WhatsApp Flow from a journey.",
        "related": [],
    },
    {
        "id": "reassign_chat",
        "aliases": [
            "reassign a chat", "reassign chat", "reassign a conversation",
            "one agent to another", "another agent",
            "assigned to another agent", "different agent",
            "team assignment behavior", "agent assignment behavior",
            "move chats to a different agent",
            "changing agent or team assignment behavior",
        ],
        "module_context": ["agent assist", "agent console", "chat"],
        "source_boosts": {
            "chat-management-assignment-rules": 5.0,
            "assignment-enhancements-in-console-7-0": 5.0,
        },
        "source_penalties": {
            "response-management-auto-replies-and-customer-satisfaction": -6.0,
        },
        "display": "Assignment Rules",
        "page_display": "Chat Management: Assignment Rules",
        "module": "Agent Assist",
        "templates": {
            "setup": (
                "The closest documented control is `Assignment Rules` in Agent Assist.\n"
                "\n"
                "Exact UI path\n"
                "- `Agent Assist -> Settings -> Chat Management -> Assignment Rules`\n"
                "\n"
                "Documented setup\n"
                "- Open `Assignment Rules` and add or edit the relevant rule.\n"
                "- Define the conditions for the chat routing logic.\n"
                "- Choose `Sticky Assignment` or a `Team/Agent Name` as the assignment outcome.\n"
                "- Click `Save`.\n"
                "\n"
                "Related documented behavior\n"
                "- Automatic assignment requires an `Agent Handover Node` on the bot journey.\n"
                "- `Sticky Assignment` controls whether reopened chats go back to the same agent who previously handled them.\n"
                "\n"
                "What I could not verify from the available documentation\n"
                "- A separate step-by-step manual \"reassign this open chat now\" action in the agent console is not explicitly documented on the retrieved pages."
            ),
        },
        "compare_blurb": "You need to reassign or route chats between agents.",
        "related": ["assignment_rules", "agent_transfer"],
    },

    # ---- Agent Assist pages ----
    {
        "id": "business_hours",
        "aliases": [
            "business hours", "business hour",
            "after hours at the wrong time", "after hours timing",
            "working hour windows", "team support schedules",
            "support schedules", "schedule logic",
            "in hours versus after hours support timing",
            "team specific support timing",
            "business hour settings live",
            "support timing needs correction",
            "team support schedules for after hours routing",
            "working hour windows for agent assist teams",
            "business hour configuration",
        ],
        "module_context": [],
        "source_boosts": {"user-management-business-hours": 5.0},
        "source_penalties": {"views": -3.0, "android-native": -3.0},
        "display": "User Management: Business Hours",
        "page_display": "User Management: Business Hours",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- User Management: Business Hours\nRelevant details\n- Use this page to configure team working hours and the in-hours versus after-hours schedule.",
            "setup": "Exact page\n- User Management: Business Hours\n- Configure business hours there for in-hours versus after-hours behavior.",
        },
        "compare_blurb": "You need support schedule and working-hour configuration.",
        "related": ["auto_replies", "assignment_rules"],
    },
    {
        "id": "auto_replies",
        "aliases": [
            "customer facing away messages", "customer facing away",
            "customer auto reply sent outside support availability",
            "wrong away message", "away message",
            "away reply", "away replies",
            "customer reminders configured",
            "inactive conversations", "customer facing reminders",
            "system resolved chat responses",
            "customer reminder behavior rather than agent reminder behavior",
            "inactive customers not agents",
            "auto replies", "away response",
            "customer inactivity reminders",
            "customer reminder behavior",
            "after hours reply", "response behavior",
        ],
        "module_context": [],
        "source_boosts": {"response-management-auto-replies-and-customer-satisfaction": 5.0},
        "source_penalties": {"views": -3.0, "user-management-teams": -3.0},
        "display": "Response Management: Auto Replies & Customer Satisfaction",
        "page_display": "Response Management: Auto Replies & Customer Satisfaction",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- Response Management: Auto Replies & Customer Satisfaction\nRelevant details\n- Use this page for away messages, customer reminders, and responses sent when chats are resolved.",
        },
        "compare_blurb": "You need customer-facing away replies, reminders, and resolved-chat responses.",
        "related": ["business_hours"],
    },
    {
        "id": "assignment_rules",
        "aliases": [
            "assignment rules", "channel and tags",
            "routing to the expected team",
            "routing depends on tags and channel",
        ],
        "module_context": ["agent assist"],
        "source_boosts": {"chat-management-assignment-rules": 5.0},
        "source_penalties": {"android-native": -3.0},
        "display": "Chat Management: Assignment Rules",
        "page_display": "Chat Management: Assignment Rules",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- Chat Management: Assignment Rules\n- `Agent Assist -> Settings -> Chat Management -> Assignment Rules`",
        },
        "compare_blurb": "You need tag-based or team-based chat routing.",
        "related": ["business_hours", "agent_transfer"],
    },
    {
        "id": "sticky_assignment",
        "aliases": [
            "sticky assignment", "previous assignee",
            "same agent handling", "sticky ownership",
            "bouncing to new agents", "reopened support threads",
            "reopened thread same owner",
            "stick to the same agent", "stick to the same",
            "same agent", "same owner",
            "reopened conversations", "reopened chat",
        ],
        "module_context": [],
        "source_boosts": {"chat-management-assignment-rules": 5.0},
        "source_penalties": {},
        "display": "Sticky Assignment",
        "page_display": "Chat Management: Assignment Rules",
        "module": "Agent Assist",
        "templates": {
            "behavior": "What happens\n- `Sticky Assignment` controls whether reopened chats go back to the previous owner/agent when possible.",
        },
        "compare_blurb": "You need to control whether reopened chats return to the same agent.",
        "related": ["assignment_rules"],
    },
    {
        "id": "live_monitoring",
        "aliases": [
            "ongoing chats no rule matched chats and agent availability",
            "response metrics as well as active busy and offline counts",
            "queue pressure before assignment alongside agent status",
            "real time monitoring of assignment backlog and response times",
            "waiting for assignment volume in real time",
            "live assignment queues and current agent state counts together",
            "live counts for available occupied and offline support agents",
            "available occupied and offline support agents",
            "available occupied and offline agent counts live",
            "ongoing chats bot chats and no rule matched conversations",
            "agent state plus unresolved queue signals",
            "wait time related metrics",
            "piling up before assignment",
            "waiting for assignment and no rule matched signals",
            "live monitoring dashboard", "live monitoring",
            "wait time metrics", "agent state metrics",
        ],
        "module_context": [],
        "source_boosts": {"live-monitoring-dashboard-real-time-chat-analytics-and-performance-insights": 5.0},
        "source_penalties": {"dashboard": -3.0, "agent-timesheet": -3.0},
        "display": "Live Monitoring Dashboard",
        "page_display": "Live Monitoring Dashboard",
        "module": "Agent Assist",
        "templates": {
            "page_lookup": "Exact page\n- Live Monitoring Dashboard\nRelevant details\n- Use this dashboard for queue signals like `Waiting for Assignment`, ongoing chats, and agent-state metrics.",
        },
        "compare_blurb": "You need real-time queue, assignment, and agent-state metrics.",
        "related": [],
    },
]

# Pre-build lookup by id
_CONCEPT_INDEX: Dict[str, Dict] = {c["id"]: c for c in CONCEPT_REGISTRY}
```

## Test

Run `kb_answer({"query": "test your bot"})`. Should still return the same answer as before — registry is data only. Confirm no syntax error.

---
**Next:** Patch 3 adds concepts 19-29 plus COMPARE_OVERRIDES.
