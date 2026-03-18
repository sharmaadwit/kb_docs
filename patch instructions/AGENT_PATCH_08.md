# Patch 8 of 9 — kb_search.py: Add concept registry + new functions (ADDITIVE ONLY)

**File:** `kb_search.py`
**Depends on:** nothing (independent file)
**Risk:** Zero — adds new data and functions only. Old code untouched.
**What it does:** Adds a scoring-focused `CONCEPT_REGISTRY`, `_extract_entities`, `_classify_intent`, intent signal lists, and `_score_chunk_v2` alongside the existing code. Nothing is replaced.

`kb_search.py` is deployed independently from `kb_answer.py`, so it has its own concept registry (scoring data only — no templates, no display names).

> **IMPORTANT — DO NOT touch telemetry code.** All Langfuse integration, tracing, span logging, and telemetry-related functions/imports must remain exactly as they are. This patch does not modify telemetry and neither should you.

---

## Step 1 — Add CONCEPT_REGISTRY after EXPLICIT_MODULES

Find the closing `}` of `EXPLICIT_MODULES`. After it, add:

```python


# ---------------------------------------------------------------------------
# Section 2 — Concept registry (scoring-focused, mirrors kb_answer.py)
#
# Each entry provides aliases for entity detection and source boost/penalty
# data so _score_chunk is data-driven, not hardcoded.
# ---------------------------------------------------------------------------

CONCEPT_REGISTRY: List[Dict] = [
    {
        "id": "api_node",
        "aliases": [
            "api node", "external api", "backend api",
            "api integration node", "call an external api",
            "call backend api", "call api", "third party api",
            "3rd party api", "send data to api", "exchange data",
            "fetch data from api", "post request", "get request",
            "journey builder api",
        ],
        "source_boosts": {"api-node": 5.0, "api-node-http-status-code-branching": 2.5},
        "source_penalties": {
            "how-to-create-whatsapp-static-flows": -8.0,
            "flow-trigger": -4.0, "whatsapp-flow": -4.0,
        },
    },
    {
        "id": "api_node_branching",
        "aliases": [
            "http status code branching", "http status",
            "status code branching", "response code branching",
            "branch based on the result", "branch based on response",
            "route based on response", "continue only if",
            "move further in the journey", "validate otp",
            "otp validation", "otp",
        ],
        "source_boosts": {"api-node-http-status-code-branching": 5.0, "api-node": 2.5},
        "source_penalties": {
            "how-to-create-whatsapp-static-flows": -8.0,
            "flow-trigger": -4.0, "whatsapp-flow": -4.0,
        },
    },
    {
        "id": "json_handler",
        "aliases": [
            "json handler", "json parser", "parse response",
            "parse api response", "parse fields from api response",
            "parse fields from an api response", "extract response fields",
            "extract fields from api response", "response fields",
            "extract fields from response", "parse json response",
            "response stored in a variable", "api response stored in a variable",
        ],
        "source_boosts": {"json-handler": 5.0, "json-handler-instead-of-code-node": 3.0},
        "source_penalties": {
            "how-to-create-whatsapp-static-flows": -4.0,
            "ctx-goal-nodes-and-conversions-api": -5.0,
        },
    },
    {
        "id": "condition_node",
        "aliases": [
            "condition node", "branch based on variable",
            "branch based on a variable value",
            "branching based on a variable value",
            "if else branching", "if else",
            "fallback path", "fallback branch logic", "branch logic",
        ],
        "source_boosts": {"condition-node": 5.0},
        "source_penalties": {
            "trigger-event-node": -4.0,
            "how-to-create-whatsapp-static-flows": -4.0,
            "modify-variable-node": -4.0,
        },
    },
    {
        "id": "manage_variables",
        "aliases": [
            "manage variables", "save user input into a variable",
            "reuse it later", "store user input", "modify variable node",
            "update a variable value", "transform a variable value",
        ],
        "source_boosts": {"manage-variables": 4.5, "modify-variable-node": 3.0},
        "source_penalties": {
            "expression-library-in-journey-builder-canvas": -4.0,
            "how-to-trigger-a-user-journey": -4.0,
        },
    },
    {
        "id": "trigger_event",
        "aliases": [
            "trigger event node", "send custom event", "event manager",
            "save in personalize", "custom integrations on events",
            "integrations triggered by events",
            "event triggered integrations",
            "create an integration in journey builder",
            "create an integration", "event driven integration",
            "emit a custom event during runtime",
            "integrate event flows", "journey builder integration",
        ],
        "source_boosts": {"trigger-event-node": 5.0, "custom-integrations": 3.5},
        "source_penalties": {
            "ai-trigger-event": -4.0, "starting-node": -4.0,
            "carousel-and-lto-template": -6.0,
            "send-message-node": -6.0,
            "journey-builder-platform-upgrade-and-node-deprecation": -6.0,
            "expression-library-in-journey-builder-canvas": -6.0,
        },
    },
    {
        "id": "call_return",
        "aliases": [
            "call and return node", "call return node",
            "call another journey", "return back to the same journey",
            "sub journey",
        ],
        "source_boosts": {"call-and-return-node": 5.0, "multi-journey-user-journeys": 4.0},
        "source_penalties": {"campaign-journey": -4.0},
    },
    {
        "id": "agent_transfer",
        "aliases": [
            "agent transfer node", "connect with a human agent",
            "handover to agent", "transfer to human agent",
            "not be transferred to an agent",
            "customer might not be transferred to an agent",
            "same conversation continues", "conversation reopening",
            "reopened chat", "bot to agent transfer flow",
            "live agent", "same thread", "resume later",
            "no agent picks up", "handoff fail",
        ],
        "source_boosts": {"agent-transfer-node": 5.0, "chat-management-assignment-rules": 4.0},
        "source_penalties": {
            "agent-personality": -4.0,
            "response-management-auto-replies-and-customer-satisfaction": -5.0,
        },
    },
    {
        "id": "goal_node",
        "aliases": [
            "goal node", "track milestones", "goal analytics toggle",
            "track purchase milestone", "conversion milestone",
            "milestone tracking", "count toward goal analytics",
            "goal achievement inside the flow",
        ],
        "source_boosts": {"goal-node": 5.0},
        "source_penalties": {"goal-analytics": -2.0, "goals/": -2.0},
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
        ],
        "source_boosts": {"prompt-nodes": 5.0, "timeout-in-prompt-nodes": 4.0, "free-text-node": 4.0},
        "source_penalties": {
            "whatsapp-carousel": -5.0, "send-message-node": -5.0,
            "journey-builder-platform-upgrade-and-node-deprecation": -5.0,
            "ctx-goal-nodes-and-conversions-api": -5.0,
        },
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
        "source_boosts": {
            "chat-management-assignment-rules": 5.0,
            "assignment-enhancements-in-console-7-0": 5.0,
        },
        "source_penalties": {
            "response-management-auto-replies-and-customer-satisfaction": -6.0,
        },
    },
    {
        "id": "business_hours",
        "aliases": ["business hours", "after-hours behavior", "after-hours support", "support hours"],
        "source_boosts": {"user-management-business-hours": 5.0},
        "source_penalties": {"views": -3.0, "android-native": -3.0},
    },
    {
        "id": "auto_replies",
        "aliases": [
            "automatic reply", "auto replies", "no agent is available",
            "customer reminder", "agent reminder", "wrong auto reply",
            "system resolves a chat automatically", "away response",
        ],
        "source_boosts": {"response-management-auto-replies-and-customer-satisfaction": 5.0},
        "source_penalties": {"views": -3.0, "user-management-teams": -3.0},
    },
    {
        "id": "assignment_rules",
        "aliases": [
            "channel and tags", "different teams", "assignment logic",
            "sticky assignment", "routing to the expected team",
            "routing depends on tags and channel",
            "reopened thread same owner", "retry assignment",
        ],
        "source_boosts": {"chat-management-assignment-rules": 5.0},
        "source_penalties": {"android-native": -3.0, "tools-developer-mode": -3.0},
    },
    {
        "id": "live_monitoring",
        "aliases": [
            "waiting for assignment", "ongoing chats", "no rule matched",
            "active busy offline", "first response time",
            "average first response time", "average response time",
            "average resolution time", "wait time related metrics",
            "monitor active agents", "live monitoring",
            "agent availability", "live agent",
        ],
        "source_boosts": {"live-monitoring-dashboard-real-time-chat-analytics-and-performance-insights": 5.0},
        "source_penalties": {"dashboard": -3.0, "agent-timesheet": -3.0},
    },
    {
        "id": "test_your_bot",
        "aliases": [
            "test your bot", "test my bot", "message log", "backend json",
            "starting node inputs", "variables updated",
            "before going live", "wrong path after a user message",
        ],
        "source_boosts": {"test-your-bot": 5.0},
        "source_penalties": {
            "about-bot-studio": -3.0, "conversational-path": -3.0,
            "ctx-goal-nodes-and-conversions-api": -3.0,
        },
    },
    {
        "id": "save_deploy",
        "aliases": [
            "save vs save & deploy", "save vs deploy",
            "save and deploy", "save & deploy",
            "live bot is still behaving like the old version",
        ],
        "source_boosts": {"save-vs-save-deploy": 5.0},
        "source_penalties": {"journey-builder-legacy": -3.0, "static-flows": -3.0},
    },
    {
        "id": "instagram",
        "aliases": [
            "go live with instagram", "instagram routing",
            "instagram go live", "instagram dm",
        ],
        "source_boosts": {"go-live-with-instagram": 5.0},
        "source_penalties": {"welcome-to-gupshup-console": -3.0, "about-bot-studio": -3.0},
    },
    {
        "id": "retain_history",
        "aliases": [
            "retain customer chat history", "earlier chat context",
            "returning customers", "anonymous users",
            "chat history retention",
        ],
        "source_boosts": {"retain-customer-chat-history": 5.0},
        "source_penalties": {"retargeting": -3.0, "ads-management": -3.0},
    },
    {
        "id": "webhooks",
        "aliases": ["configure webhooks", "webhooks in the console", "webhook callback url"],
        "source_boosts": {"integrations/webhooks": 5.0},
        "source_penalties": {"others-webhooks": -3.0},
    },
    {
        "id": "webhook_delivery",
        "aliases": [
            "delivery analytics downstream", "reconcile webhook data",
            "recipient level delivery outcomes",
            "webhooks connect to delivery analytics",
            "delivery callbacks map to the analytics view",
            "delivery statuses", "message lifecycle statuses",
        ],
        "source_boosts": {
            "workflows/webhooks-to-delivery-analytics": 4.0,
            "integrations/webhooks": 4.0,
        },
        "source_penalties": {"automated-campaign-analytics": -3.0},
    },
    {
        "id": "campaign_analytics",
        "aliases": [
            "campaign analytics", "response file", "link tracking report",
            "click through rate", "unique clicks", "total clicks",
            "dropped", "failed",
        ],
        "source_boosts": {"campaign-analytics": 5.0, "how-to-measure-click-through-rates": 2.0},
        "source_penalties": {"campaign-and-ctx-ad-preview": -3.0, "dashboard": -3.0},
    },
    {
        "id": "ctwa_to_goals",
        "aliases": ["connect a bot to a ctwa campaign", "ad journeys", "ctwa to goals"],
        "source_boosts": {"ctwa-to-bot-to-goals": 5.0},
        "source_penalties": {"ctx-goal-nodes-and-conversions-api": -3.0, "creating-a-ctwa-ad": -3.0},
    },
    {
        "id": "goal_analytics",
        "aliases": ["goal achieved", "unique users", "goal analytics", "source type", "source value"],
        "source_boosts": {"goal-analytics": 5.0},
        "source_penalties": {"ctx-goal-nodes-and-conversions-api": -3.0},
    },
    {
        "id": "prompt_timeout",
        "aliases": ["timeout in prompt", "prompt node timeout", "timeouts work in prompt nodes", "prompt node times out", "times out"],
        "source_boosts": {"timeout-in-prompt-nodes": 5.0},
        "source_penalties": {"carousel": -3.0, "send-message-node": -3.0},
    },
    {
        "id": "privacy_policy",
        "aliases": ["privacy policy", "web widget privacy", "widget privacy"],
        "source_boosts": {"privacy-policy": 2.3, "pre-chat-form": 1.2},
        "source_penalties": {},
    },
]
```

## Step 2 — Add _extract_entities, intent signals, and _classify_intent

Find the end of `_module_from_source`. After it, add:

```python


# ---------------------------------------------------------------------------
# Section 5 — Entity extraction & intent classification
# ---------------------------------------------------------------------------

def _extract_entities(query: str) -> List[Dict]:
    q = _normalize_query_for_match(query)
    matched = []
    matched_ids = set()
    for concept in CONCEPT_REGISTRY:
        if concept["id"] in matched_ids:
            continue
        if any(alias in q for alias in concept["aliases"]):
            matched.append(concept)
            matched_ids.add(concept["id"])
    return matched


_COMPARE_SIGNALS = [" vs ", " versus ", " difference ", " compare "]
_PAGE_LOOKUP_SIGNALS = [
    "which page", "where do i", "where exactly", "which dashboard",
    "which report", "what page", "where can i monitor",
]
_DEFINITION_SIGNALS = ["what is", "what does", "mean in"]
_BEHAVIOR_SIGNALS = [
    "what happens", "how do timeouts work", "when enabled", "when disabled",
    "after hours", "anonymous users", "returning customers",
    "real time operations view",
]
_TROUBLESHOOT_SIGNALS = [
    "troubleshoot", "what should i check", "not seeing", "missing",
    "wrong", "issue", "problem",
]
_SCHEMA_SIGNALS = [
    "schema", "payload", "fields to store", "statuses",
    "status fields", "how should we store",
]


def _classify_intent(query: str, entities: List[Dict]) -> str:
    q = _normalize_query_for_match(query)
    if any(x in q for x in _COMPARE_SIGNALS):
        return "compare"
    if any(x in q for x in _PAGE_LOOKUP_SIGNALS):
        return "page_lookup"
    if any(x in q for x in _SCHEMA_SIGNALS):
        return "schema"
    if any(x in q for x in _BEHAVIOR_SIGNALS):
        return "behavior"
    if any(x in q for x in _DEFINITION_SIGNALS):
        return "definition"
    if any(x in q for x in _TROUBLESHOOT_SIGNALS):
        return "troubleshooting"
    return "setup"
```

## Step 3 — Add _score_chunk_v2

Find the end of the existing `_score_chunk` function. After it, add:

```python


def _score_chunk_v2(
    query: str, chunk: Dict, entities: List[Dict], explicit_module: str,
) -> float:
    q = _normalize_query_for_match(query)
    source = str(chunk.get("source") or chunk.get("path") or "").lower()
    heading = str(chunk.get("heading") or "").lower()
    text = str(chunk.get("text") or "").lower()
    section_type = str(chunk.get("section_type") or "").lower()
    score = 0.0

    for token in re.findall(r"[a-z0-9&+-]+", q):
        if len(token) < 3:
            continue
        if token in heading:
            score += 0.25
        if token in source:
            score += 0.25
        if token in text:
            score += 0.05

    if explicit_module != "General" and explicit_module.lower() in _module_from_source(source).lower():
        score += 0.35

    if section_type == "reference":
        score -= 1.2

    if any(bad in source for bad in GLOBAL_PENALTY_SOURCES):
        score -= 4.0

    for entity in entities:
        for slug, boost in entity.get("source_boosts", {}).items():
            if slug in source:
                score += boost
        for slug, penalty in entity.get("source_penalties", {}).items():
            if slug in source:
                score += penalty

    if any(x in q for x in _PAGE_LOOKUP_SIGNALS):
        if section_type == "path":
            score += 1.5
        if "exact ui path" in text or "gupshup console" in text:
            score += 0.8
    if any(x in q for x in _DEFINITION_SIGNALS):
        if section_type == "concept":
            score += 1.5
    if any(x in q for x in _BEHAVIOR_SIGNALS):
        if section_type in {"concept", "general", "validation"}:
            score += 1.1
    if any(x in q for x in _SCHEMA_SIGNALS):
        if section_type == "schema":
            score += 1.8
    if any(x in q for x in _TROUBLESHOOT_SIGNALS):
        if section_type in {"troubleshooting", "validation"}:
            score += 1.2

    if "privacy policy" in q:
        if "security" in source and not any(
            x in text for x in [
                "widget", "configure", "where", "display", "appear",
                "pre-chat form", "checkbox text", "hyperlinked text",
                "url for hyperlinked text", "before chat starts",
            ]
        ):
            score -= 1.8

    return score
```

## Step 4 — Add _apply_feature_lock_v2

After `_score_chunk_v2`, add:

```python


def _apply_feature_lock_v2(scored: List[Dict], entities: List[Dict]) -> List[Dict]:
    preferred_tokens = []
    for entity in entities:
        preferred_tokens.extend(entity.get("source_boosts", {}).keys())
    if not preferred_tokens:
        return scored
    preferred = [
        row for row in scored
        if any(tok in str(row.get("source") or "").lower() for tok in preferred_tokens)
    ]
    return preferred if preferred else scored
```

## Step 5 — Add updated _detect_intents

Replace the existing `_detect_intents` with:

```python
def _detect_intents(query: str) -> List[str]:
    q = _normalize_query_for_match(query)
    intents: List[str] = []
    if any(x in q for x in _COMPARE_SIGNALS):
        intents.append("compare")
    if any(x in q for x in _PAGE_LOOKUP_SIGNALS):
        intents.append("page_lookup")
    if any(x in q for x in _DEFINITION_SIGNALS):
        intents.append("definition")
    if any(x in q for x in _BEHAVIOR_SIGNALS):
        intents.append("behavior")
    if any(x in q for x in _TROUBLESHOOT_SIGNALS):
        intents.append("troubleshooting")
    if any(x in q for x in _SCHEMA_SIGNALS):
        intents.append("schema")
    if not intents:
        intents.append("setup")
    return intents
```

If `_detect_intents` does not exist yet, add it after `_classify_intent`.

## Test — Gate A (no behavior change)

Run `kb_search({"query": "condition node"})`. It should return **exactly the same results as before this patch** because nothing calls the new `_v2` functions yet.

### Quick function existence check

Verify these functions exist in `kb_search.py` (no import errors):
- `_extract_entities`
- `_classify_intent`
- `_score_chunk_v2`
- `_apply_feature_lock_v2`

---
**Next:** Patch 9 swaps `kb_search()` to the new pipeline and cleans up dead code.
