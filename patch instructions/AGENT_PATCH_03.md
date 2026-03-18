# Patch 3 of 9 — Concept Registry Part C + Compare Overrides

**File:** `kb_answer.py`  
**Depends on:** Patch 2  
**Risk:** Zero — data only  

**What it does:** Adds concepts test_your_bot through goal_analytics and the `COMPARE_OVERRIDES` dictionary for known multi-concept pairs.

> **IMPORTANT — DO NOT touch telemetry code.** All Langfuse integration, tracing, span logging, and telemetry-related functions/imports must remain exactly as they are. This patch does not modify telemetry and neither should you.

## Instructions

Find the closing `]` of `CONCEPT_REGISTRY` and the `_CONCEPT_INDEX` line from Patch 2:

**Find (exact):**
```
]

# Pre-build lookup by id
_CONCEPT_INDEX: Dict[str, Dict] = {c["id"]: c for c in CONCEPT_REGISTRY}
```

**Replace with:**
```python
    # ---- Bot Studio pages ----
    {
        "id": "test_your_bot",
        "aliases": [
            "test your bot", "test my bot", "message log",
            "validate trigger inputs before publishing a journey",
            "inspect backend payloads while testing a flow",
            "debug executed nodes and payload details during bot testing",
            "test the journey before it is live on a channel",
            "test a journey", "test the journey",
            "message log basics and payload details",
            "bot behaves oddly in the test widget",
            "wrong path after a user message",
            "wrong branch in a journey",
            "should i debug in test your bot before checking live channel behavior",
            "troubleshoot inside test your bot or on the live channel first",
            "where do i test a bot before going live",
            "backend json", "raw payload",
            "payload debugging", "inspect payloads",
            "debugging before go live",
        ],
        "module_context": [],
        "source_boosts": {"test-your-bot": 5.0},
        "source_penalties": {
            "about-bot-studio": -3.0,
            "conversational-path": -3.0,
            "ctx-goal-nodes-and-conversions-api": -3.0,
        },
        "display": "Test your Bot",
        "page_display": "Test your Bot",
        "module": "Bot Studio",
        "templates": {
            "page_lookup": "Exact page\n- Test your Bot\nRelevant details\n- Use `Message Log` to validate trigger inputs, inspect executed nodes, and review backend payloads before go-live.",
        },
        "compare_blurb": "You need to test, debug, and inspect journey behavior before go-live.",
        "related": ["save_deploy"],
    },
    {
        "id": "save_deploy",
        "aliases": [
            "save vs save and deploy", "save and deploy",
            "save vs deploy", "save & deploy",
            "saved changes are not yet live on the channel",
            "concept explains why saved",
            "not yet live on the channel",
            "draft is updated but production behavior is still old",
            "production behavior is still old",
            "saved versus actually live",
            "merely saved versus actually live",
            "pushing live behavior", "push it live", "push live",
            "live rollout", "deployment status",
            "verify live", "go live and deploy",
            "gap between saving progress and pushing live",
            "customers still see the old bot",
            "production bot still behaves old",
            "production still shows the old journey",
            "changes are merely saved versus actually live",
            "testing looks right but customers still see the old bot",
            "live channel still see old behavior",
            "live channel behavior after deployment",
        ],
        "module_context": [],
        "source_boosts": {"save-vs-save-deploy": 5.0},
        "source_penalties": {
            "journey-builder-legacy": -3.0,
            "static-flows": -3.0,
            "how-do-the-elements-of-bot-studio-work-together": -3.0,
        },
        "display": "Save Vs Save & Deploy",
        "page_display": "Save Vs Save & Deploy",
        "module": "Bot Studio",
        "templates": {
            "page_lookup": (
                "Exact page\n"
                "- Save Vs Save & Deploy\n"
                "- Save Deploy behavior for making Bot Studio changes live on the channel.\n"
                "Use Save when\n"
                "- `Save` stores progress in Bot Studio.\n"
                "Use Save & Deploy when\n"
                "- `Save & Deploy` pushes the latest saved changes live to the channel."
            ),
            "compare": (
                "Use Save when\n"
                "- `Save` stores your progress in Bot Studio.\n"
                "Use Save & Deploy when\n"
                "- `Save & Deploy` pushes the saved bot to live channels."
            ),
            "behavior": (
                "Exact page\n"
                "- Save Vs Save & Deploy\n"
                "Use Save when\n"
                "- `Save` stores progress in Bot Studio.\n"
                "Use Save & Deploy when\n"
                "- `Save & Deploy` pushes the latest saved changes live to the channel."
            ),
        },
        "compare_blurb": "You need to understand the gap between saving and deploying live.",
        "related": ["test_your_bot"],
    },
    {
        "id": "prompt_timeout",
        "aliases": [
            "never replies to a prompt in time",
            "prompt timeouts seem too aggressive",
            "timeout in prompt nodes", "prompt node timeout",
            "prompt node times out", "times out",
        ],
        "module_context": [],
        "source_boosts": {"timeout-in-prompt-nodes": 5.0},
        "source_penalties": {"carousel": -3.0, "send-message-node": -3.0},
        "display": "Timeout in Prompt Nodes",
        "page_display": "Timeout in Prompt Nodes",
        "module": "Bot Studio",
        "templates": {
            "behavior": "Exact page\n- Timeout in Prompt Nodes\nRelevant details\n- This page explains timeout duration, what happens when the user does not reply in time, and the fallback path.",
        },
        "compare_blurb": "You need to understand prompt timeout and fallback behavior.",
        "related": ["prompt_node"],
    },
    {
        "id": "bot_variables_in_nodes",
        "aliases": [
            "variable types documented",
            "how variables can be mapped directly into nodes",
            "interpolation syntax inside message nodes",
        ],
        "module_context": ["journey builder", "bot studio"],
        "source_boosts": {"manage-variables": 4.0, "modify-variable-node": 3.0},
        "source_penalties": {},
        "display": "Manage Variables",
        "page_display": "Manage Variables",
        "module": "Bot Studio",
        "templates": {
            "behavior": (
                "What the docs confirm\n"
                "- Use `Bot Studio -> Manage Variables` to create or select variables used in Journey Builder.\n"
                "- The docs say variables can be mapped directly into nodes for data handling or personalization.\n"
                "- If you need to update or transform a value, use `Modify Variable Node`.\n"
                "Supported variable details\n"
                "- Variable types documented are `Local`, `Global`, `System`, `Constant`, and `CDP`.\n"
                "- Documented system variables include `user_input`, `channel`, `user_name`, `ai_intent`, and `payloadJson`.\n"
                "What the docs do not confirm\n"
                "- The current docs do not clearly specify the exact interpolation syntax inside message nodes."
            ),
        },
        "compare_blurb": "You need to understand how variables work inside journey nodes.",
        "related": ["manage_variables", "modify_variable"],
    },

    # ---- Channels ----
    {
        "id": "instagram",
        "aliases": [
            "go live with instagram",
            "instagram conversations are landing in the wrong journey",
            "instagram is connected but traffic is not entering the intended flow",
            "journeys active on instagram dm",
            "configure or review instagram go live behavior",
            "instagram go live behavior documented for bot routing",
        ],
        "module_context": [],
        "source_boosts": {"go-live-with-instagram": 5.0},
        "source_penalties": {"welcome-to-gupshup-console": -3.0, "about-bot-studio": -3.0},
        "display": "Go Live with Instagram",
        "page_display": "Go Live with Instagram",
        "module": "Channels",
        "templates": {
            "page_lookup": "Exact page\n- Go Live with Instagram\nRelevant details\n- Use this page to connect Instagram and ensure Bot Studio journeys are active on Instagram DM.",
        },
        "compare_blurb": "You need to connect Instagram and route DM traffic to bot journeys.",
        "related": [],
    },
    {
        "id": "retain_history",
        "aliases": [
            "retain customer chat history",
            "repeat anonymous visitors",
            "retained customer chat history configured for the web widget",
            "returning customers see earlier conversation context",
            "same browser should resume earlier chat context",
            "prior web widget chat context",
            "earlier conversation context",
        ],
        "module_context": [],
        "source_boosts": {"retain-customer-chat-history": 5.0},
        "source_penalties": {"retargeting": -3.0, "ads-management": -3.0},
        "display": "Retain Customer Chat History",
        "page_display": "Retain Customer Chat History",
        "module": "Channels",
        "templates": {
            "page_lookup": "Exact page\n- Retain Customer Chat History\nRelevant details\n- Use this page for retained web-widget chat context for returning users on the same browser/device.",
            "behavior": "Exact page\n- Retain Customer Chat History\nRelevant details\n- Use this page for retained web-widget chat context for returning users on the same browser/device.",
        },
        "compare_blurb": "You need web-widget chat history retention for returning users.",
        "related": [],
    },

    # ---- Integrations ----
    {
        "id": "webhooks",
        "aliases": [
            "add a webhook callback url",
            "configure campaign related callback events",
            "which webhook page should i open",
            "where in the console do i add a webhook callback url",
            "configure webhooks", "webhooks in the console",
        ],
        "module_context": [],
        "source_boosts": {"integrations/webhooks": 5.0},
        "source_penalties": {"others-webhooks": -3.0},
        "display": "Webhooks",
        "page_display": "Webhooks",
        "module": "Integrations",
        "templates": {
            "page_lookup": "Exact page\n- Webhooks\n- Gupshup Console → App → Integration → Webhooks",
            "schema": (
                "Key fields to store\n"
                "- Store delivery statuses like `SENT`, `DELIVERED`, `READ`, and `FAILED`.\n"
                "- Preserve fields such as `eventType`, `externalId`, `cause`, `errorCode`, `destAddr`, `srcAddr`, `eventTs`, `conversation.id`, and `pricing.category`."
            ),
        },
        "compare_blurb": "You need live callback data and delivery-event identifiers.",
        "related": ["campaign_analytics", "webhook_delivery"],
    },
    {
        "id": "webhook_delivery",
        "aliases": [
            "warehouse for delivery state tracking",
            "delivery status values matter most",
            "payload attributes should we preserve",
            "model sent delivered read and failed webhook events",
            "lose delivery identifiers",
            "which webhook fields should we warehouse",
            "downstream webhook reporting",
            "delivery statuses", "message lifecycle statuses",
            "delivery timelines", "delivery events",
            "recipient level delivery",
        ],
        "module_context": [],
        "source_boosts": {
            "integrations/webhooks": 4.0,
            "workflows/webhooks-to-delivery-analytics": 4.0,
        },
        "source_penalties": {"automated-campaign-analytics": -3.0},
        "display": "Webhooks To Delivery Analytics",
        "page_display": "Webhooks To Delivery Analytics",
        "module": "Workflows",
        "templates": {
            "schema": (
                "Key fields to store\n"
                "- Store delivery statuses like `SENT`, `DELIVERED`, `READ`, and `FAILED`.\n"
                "- Preserve fields such as `eventType`, `externalId`, `cause`, `errorCode`, `destAddr`, `srcAddr`, `eventTs`, `conversation.id`, and `pricing.category`."
            ),
        },
        "compare_blurb": "You need the page that connects webhook delivery events to campaign reporting.",
        "related": ["webhooks", "campaign_analytics"],
    },

    # ---- Campaign & Goals ----
    {
        "id": "campaign_analytics",
        "aliases": [
            "campaign analytics", "response file", "link tracking report",
            "click through rate", "click through rates",
            "unique clicks", "total clicks",
            "dropped", "failed",
            "defines dropped and failed campaign outcomes",
            "inspect campaign click metrics after a campaign is sent",
            "campaign level delivery timelines",
            "meaning of campaign result labels like dropped",
            "timewise delivery events for all phone numbers",
            "click metrics", "delivery performance",
        ],
        "module_context": [],
        "source_boosts": {
            "campaign-analytics": 5.0,
            "how-to-measure-click-through-rates": 2.0,
        },
        "source_penalties": {"campaign-and-ctx-ad-preview": -3.0, "dashboard": -3.0},
        "display": "Campaign Analytics",
        "page_display": "Campaign Analytics",
        "module": "Campaign Manager",
        "templates": {
            "page_lookup": "Exact page\n- Campaign Analytics\nRelevant details\n- Use this page for campaign delivery outcomes, click metrics, and definitions like `Dropped` and `Failed`.",
            "definition": "Exact page\n- Campaign Analytics\nRelevant details\n- Use this page for click-through rate, unique clicks, and total clicks after a campaign is sent.",
        },
        "compare_blurb": "You need delivery, read, and click performance.",
        "related": ["goal_analytics", "ctwa_to_goals"],
    },
    {
        "id": "ctwa_to_goals",
        "aliases": [
            "ctwa page explains why only ad journeys are available during connection",
            "ctwa bot connection flow documented from connect bot through publish",
            "ctwa bot connection procedure",
            "converting the journey for ctwa and then publishing it live",
            "what step after choosing the bot journey actually activates the ctwa setup",
            "ad journeys appear", "ad journey",
            "ctwa campaign", "after a ctwa",
            "ctwa traffic", "ctwa driven",
        ],
        "module_context": ["ctwa"],
        "source_boosts": {"ctwa-to-bot-to-goals": 5.0},
        "source_penalties": {"ctx-goal-nodes-and-conversions-api": -3.0, "creating-a-ctwa-ad": -3.0},
        "display": "Ctwa To Bot To Goals",
        "page_display": "Ctwa To Bot To Goals",
        "module": "CTX",
        "templates": {
            "page_lookup": "Exact page\n- Ctwa To Bot To Goals\nRelevant details\n- Use this workflow page for connecting CTWA traffic to a bot journey, selecting the `Ad Journey`, and publishing it live.",
        },
        "compare_blurb": "You need the CTWA-to-bot workflow that connects campaign traffic to the goal path.",
        "related": ["campaign_analytics", "goal_analytics"],
    },
    {
        "id": "goal_analytics",
        "aliases": [
            "goal analytics page explains goal achieved versus unique users",
            "analytics page explains goal achieved versus unique users",
            "open goal analytics for a configured goal",
            "milestone level goal records with source fields",
            "source type documented for ctwa or campaign driven goal traffic",
            "goal metric definitions and milestone export fields",
            "goal achieved", "unique users", "goal analytics",
            "goal conversions", "goal completion",
            "conversions are missing",
        ],
        "module_context": [],
        "source_boosts": {"goal-analytics": 5.0},
        "source_penalties": {"ctx-goal-nodes-and-conversions-api": -3.0},
        "display": "Goal Analytics",
        "page_display": "Goal Analytics",
        "module": "Goals",
        "templates": {
            "page_lookup": "Exact page\n- Goal Analytics\nRelevant details\n- Use this page for goal metric definitions like `Goal Achieved` and `Unique Users`, and for milestone export/source fields.",
            "definition": "Exact page\n- Goal Analytics\nRelevant details\n- This page defines both `Goal Achieved` and `Unique Users`.",
        },
        "compare_blurb": "You need post-click conversion performance and goal completion data.",
        "related": ["campaign_analytics", "ctwa_to_goals"],
    },
]

# Pre-build lookup by id
_CONCEPT_INDEX: Dict[str, Dict] = {c["id"]: c for c in CONCEPT_REGISTRY}

# ---------------------------------------------------------------------------
# Section 4 — Compare overrides for known multi-concept pairs
# ---------------------------------------------------------------------------

COMPARE_OVERRIDES: Dict[Tuple[str, ...], str] = {
    ("business_hours", "auto_replies"): (
        "Use Business Hours when\n"
        "- You need support schedule and working-hour configuration.\n"
        "Use Auto Replies when\n"
        "- You need customer-facing away replies, reminders, and resolved-chat responses."
    ),
    ("campaign_analytics", "goal_analytics"): (
        "Use Campaign Analytics when\n"
        "- You need delivery, read, and click performance.\n"
        "Use Goal Analytics when\n"
        "- You need post-click conversion performance and goal completion data.\n"
        "Use Ctwa To Bot To Goals when\n"
        "- You need the CTWA-to-bot workflow that connects campaign traffic to the goal path."
    ),
    ("test_your_bot", "save_deploy"): (
        "Use Test your Bot first\n"
        "- Validate triggers, inspect payloads, and debug journey behavior before release.\n"
        "Use Save Vs Save & Deploy next\n"
        "- Confirm whether changes are only saved or actually pushed live to channels."
    ),
    ("webhooks", "campaign_analytics"): (
        "Use Webhooks when\n"
        "- You need live callback data and delivery-event identifiers.\n"
        "Use Response file when\n"
        "- You need phone-number-level delivery timelines from campaign reporting.\n"
        "Use Link Tracking Report when\n"
        "- You need click metadata like original URL, device, and OS.\n"
        "Use Webhooks To Delivery Analytics when\n"
        "- You need the page that connects webhook delivery events to campaign reporting."
    ),
    ("assignment_rules", "agent_transfer"): (
        "Check these two modules together\n"
        "- `Agent Assist -> Settings -> Chat Management -> Assignment Rules` for tag-based or team-based routing conditions.\n"
        "- `Bot Studio -> Journey Builder -> Agent Transfer Node` for the documented bot-to-agent handover step."
    ),
    ("business_hours", "auto_replies", "assignment_rules"): (
        "Configure these areas together\n"
        "- `User Management: Business Hours` for support schedules and after-hours timing.\n"
        "- `Response Management: Auto Replies & Customer Satisfaction` for away replies and reminder behavior.\n"
        "- If you also need agent routing behavior the next morning, review `Assignment Rules` for the routing outcome."
    ),
}
```

## Test

Run `kb_answer({"query": "test your bot"})`. Should still return a response — registry is data only, no behavior change.

Verify these entries are in `CONCEPT_REGISTRY` by checking the file:
- `test_your_bot` has alias `"test my bot"`
- `prompt_timeout` has alias `"prompt node times out"`
- `COMPARE_OVERRIDES` dict exists with at least one key

---
**Next:** Patch 4 adds entity extraction, intent classification, and page display mapping.
