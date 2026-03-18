# Patch 1 of 9 — Concept Registry Part A (Bot Studio nodes)

**File:** `kb_answer.py`
**Depends on:** nothing (first patch)
**What it does:** Adds the first 9 concept entries (API Node through Agent Transfer) that replace the old `FEATURE_RULES` scoring dict. This is pure data — no behavior change yet.

> **IMPORTANT — DO NOT touch telemetry code.** All Langfuse integration, tracing, span logging, and telemetry-related functions/imports must remain exactly as they are. This patch does not modify telemetry and neither should you.

## Step 1 — Update the import line

**Find (exact):**
```
from typing import Dict, List
```

**Replace with:**
```
from typing import Dict, List, Tuple
```

If the import already has `Tuple`, skip this step.

## Step 2 — Add the concept registry after guardrails

**Find the line:**
```
GLOBAL_PENALTY_SOURCES = [
```

**After the closing `]` of that list, add all of the following code:**

```python


# ---------------------------------------------------------------------------
# Section 3 — Concept Registry
#
# Each concept is the single source of truth for:
#   aliases        – trigger phrases (matched in normalized query)
#   source_boosts  – {source_substring: float} for scoring
#   source_penalties – {source_substring: float} for scoring
#   display        – human-readable name
#   page_display   – canonical page name for page_lookup answers
#   module         – owning product module
#   templates      – {intent: answer_string} pre-composed answers
#   compare_blurb  – one-liner for the compare composer
#   related        – concept ids often used together
# ---------------------------------------------------------------------------

CONCEPT_REGISTRY: List[Dict] = [
    # ---- Bot Studio nodes ----
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
        "module_context": ["journey builder", "bot studio"],
        "source_boosts": {"api-node": 5.0, "api-node-http-status-code-branching": 2.5},
        "source_penalties": {
            "how-to-create-whatsapp-static-flows": -8.0,
            "flow-trigger": -4.0, "whatsapp-flow": -4.0,
        },
        "display": "API Node",
        "page_display": "API Node",
        "module": "Bot Studio",
        "templates": {
            "setup": (
                "The documentation indicates you should use the API Node in Journey Builder for this pattern.\n"
                "\n"
                "Recommended setup\n"
                "- Capture the input or journey data you want to send in a variable.\n"
                "- Add an API Node at the point in the journey where you need to call the external or backend API.\n"
                "- Configure the API Node to call your target endpoint and store the API response in a variable for later use.\n"
                "- Use the returned API response to control the next step in the journey.\n"
                "\n"
                "Useful related components\n"
                "- Use `API Node: HTTP Status Code Branching` if you want routing based on response codes.\n"
                "- Use `JSON Handler` if you need to extract fields from the backend response.\n"
                "\n"
                "What I could not verify from the available documentation\n"
                "- The exact request payload format and the exact response schema for your specific backend API."
            ),
        },
        "compare_blurb": "You need to call an external or backend API from a journey.",
        "related": ["json_handler", "api_node_branching", "condition_node"],
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
        "module_context": ["journey builder", "bot studio", "api node"],
        "source_boosts": {
            "api-node-http-status-code-branching": 5.0,
            "api-node": 2.5,
        },
        "source_penalties": {
            "how-to-create-whatsapp-static-flows": -8.0,
            "flow-trigger": -4.0, "whatsapp-flow": -4.0,
        },
        "display": "API Node: HTTP Status Code Branching",
        "page_display": "API Node: HTTP Status Code Branching",
        "module": "Bot Studio",
        "templates": {
            "setup": (
                "The documentation indicates you should use `API Node: HTTP Status Code Branching` for this pattern.\n"
                "\n"
                "Recommended setup\n"
                "- Add and configure the `API Node` first.\n"
                "- Enable the `HTTP Status Code` switch.\n"
                "- Add connectors and tag them with the response codes you want to handle, such as `200`, `400`, `401`, or `503`.\n"
                "- Route each tagged connector to the correct next path in the journey.\n"
                "\n"
                "Useful related components\n"
                "- Use `JSON Handler` if you also need to parse fields from the API response body."
            ),
        },
        "compare_blurb": "You need to route a journey based on API response codes.",
        "related": ["api_node", "json_handler"],
    },
    {
        "id": "json_handler",
        "aliases": [
            "json handler", "json parser", "parse response",
            "parse api response", "parse fields from api response",
            "parse fields from an api response", "extract response fields",
            "extract fields from api response", "response fields",
            "extract fields from response", "parse json response",
            "response stored in a variable",
            "api response stored in a variable",
        ],
        "module_context": [],
        "source_boosts": {"json-handler": 5.0, "json-handler-instead-of-code-node": 3.0},
        "source_penalties": {
            "how-to-create-whatsapp-static-flows": -4.0,
            "flow-trigger": -4.0, "whatsapp-flow": -4.0,
            "ctx-goal-nodes-and-conversions-api": -5.0,
        },
        "display": "JSON Handler",
        "page_display": "JSON Handler",
        "module": "Bot Studio",
        "templates": {
            "setup": (
                "The documentation indicates you should use `JSON Handler` for this pattern.\n"
                "\n"
                "Recommended setup\n"
                "- Call the external or backend API first and store the response in a variable.\n"
                "- Add `JSON Handler` in the journey after the API response is available.\n"
                "- Select the variable that contains the JSON response.\n"
                "- Map the JSON attributes you want to extract for later journey steps.\n"
                "\n"
                "Useful related components\n"
                "- Use `API Node` to call the external system and store the response.\n"
                "- Use `Condition Node` or response-based branching after extraction if the next step depends on the parsed value.\n"
                "\n"
                "What I could not verify from the available documentation\n"
                "- The exact response schema for your backend API."
            ),
        },
        "compare_blurb": "You need to parse fields from an API response.",
        "related": ["api_node", "condition_node"],
    },
    {
        "id": "condition_node",
        "aliases": [
            "condition node", "branch based on variable",
            "branch based on a variable value",
            "branching based on a variable value",
            "if else branching", "if else",
            "fallback path", "fallback branch logic", "branch logic",
            "else path when none of the condition checks match",
            "configure an else path",
            "fallback handling when branch conditions fail",
            "conditional routing from parsed response values",
        ],
        "module_context": ["journey builder", "bot studio", "journey"],
        "source_boosts": {"condition-node": 5.0},
        "source_penalties": {
            "trigger-event-node": -4.0,
            "how-to-create-whatsapp-static-flows": -4.0,
            "modify-variable-node": -4.0,
        },
        "display": "Condition Node",
        "page_display": "Condition Node",
        "module": "Bot Studio",
        "templates": {
            "setup": (
                "The documentation indicates you should use `Condition Node` for this pattern.\n"
                "\n"
                "Recommended setup\n"
                "- Open the target journey in `Journey Builder` and add or open `Condition Node`.\n"
                "- Select whether the condition should evaluate the current user message or another variable.\n"
                "- Configure the condition/operator and comparison value.\n"
                "- Connect each branch to the correct next node and configure the fallback path.\n"
                "\n"
                "Validation\n"
                "- Use `Test your Bot` to trigger each expected branch value and confirm unmatched input follows the fallback path."
            ),
        },
        "compare_blurb": "You need to branch a journey based on a variable value.",
        "related": ["manage_variables", "modify_variable"],
    },
    {
        "id": "manage_variables",
        "aliases": [
            "manage variables", "save user input into a variable",
            "reuse it later", "store user input",
            "define reusable journey variables",
            "reusable journey variables",
            "create a variable so multiple nodes can reference",
            "manages variables used across a journey",
            "set up variables before capturing user input",
            "prepare journey variables ahead of",
        ],
        "module_context": ["journey builder", "bot studio", "journey"],
        "source_boosts": {"manage-variables": 4.5, "modify-variable-node": 3.0},
        "source_penalties": {
            "expression-library-in-journey-builder-canvas": -4.0,
            "how-to-trigger-a-user-journey": -4.0,
        },
        "display": "Manage Variables",
        "page_display": "Manage Variables",
        "module": "Bot Studio",
        "templates": {
            "setup": (
                "The documentation indicates you should use `Manage Variables` for this pattern.\n"
                "\n"
                "Recommended setup\n"
                "- Create or select the required variable in `Bot Studio -> Manage Variables`.\n"
                "- Store the user input into that variable so it can be reused later in the journey.\n"
                "- If you need to transform or update the value after capture, use `Modify Variable Node`.\n"
                "\n"
                "Useful related components\n"
                "- `Manage Variables` defines and manages the variable.\n"
                "- `Modify Variable Node` is used when you need to update or transform the stored value."
            ),
        },
        "compare_blurb": "You need to define or store variables in a journey.",
        "related": ["modify_variable", "prompt_node"],
    },
    {
        "id": "modify_variable",
        "aliases": [
            "modify variable node", "transform a variable value",
            "updates an existing variable after it has already been stored",
            "variable transformation rather than initial creation",
            "saved variable needs to be updated", "change stored values",
        ],
        "module_context": ["journey builder", "bot studio", "journey", "variable"],
        "source_boosts": {"modify-variable-node": 4.5},
        "source_penalties": {},
        "display": "Modify Variable Node",
        "page_display": "Modify Variable Node",
        "module": "Bot Studio",
        "templates": {
            "setup": (
                "The documentation indicates you should use `Modify Variable Node` for this pattern.\n"
                "\n"
                "Recommended setup\n"
                "- Ensure the variable already exists (create it in `Manage Variables` if needed).\n"
                "- Add `Modify Variable Node` at the point where the stored value should be updated or transformed.\n"
                "- Select the variable and the operation (e.g. set, append, increment).\n"
                "- Use the modified value in later steps or in `Condition Node` for branching.\n"
                "\n"
                "Useful related components\n"
                "- `Manage Variables` defines the variable; `Modify Variable Node` updates it inside the journey."
            ),
        },
        "compare_blurb": "You need to update or transform an existing variable inside a journey.",
        "related": ["manage_variables", "condition_node"],
    },
    {
        "id": "trigger_event",
        "aliases": [
            "trigger event node", "send custom event", "event manager",
            "save in personalize",
            "custom integrations on events",
            "integrations triggered by events",
            "event triggered integrations",
            "create an integration in journey builder",
            "create an integration",
            "event driven integration",
            "emit a custom event during runtime",
            "integrate event flows",
            "journey builder integration",
        ],
        "module_context": ["journey builder", "bot studio"],
        "source_boosts": {"trigger-event-node": 5.0, "custom-integrations": 3.5},
        "source_penalties": {
            "ai-trigger-event": -4.0, "starting-node": -4.0,
            "carousel-and-lto-template": -6.0,
            "send-message-node": -6.0,
            "journey-builder-platform-upgrade-and-node-deprecation": -6.0,
            "expression-library-in-journey-builder-canvas": -6.0,
        },
        "display": "Trigger Event Node",
        "page_display": "Trigger Event Node",
        "module": "Bot Studio",
        "templates": {
            "setup": (
                "The documentation points to two related patterns depending on what you need.\n"
                "\n"
                "If the journey should emit an event during execution\n"
                "- Use `Trigger Event Node` in `Journey Builder`.\n"
                "- First create the custom event in `Event Manager`.\n"
                "- Then drag `Trigger Event Node` onto the canvas, choose the event category and event name, "
                "map local/global variables, and click `Save & Deploy`.\n"
                "\n"
                "If an external system should send events into Console\n"
                "- Use `Integrations -> Custom Integrations`.\n"
                "- Create the integration, define the unique event identifier path, and use the generated callback URL and authorization token.\n"
                "\n"
                "What I could not verify from the available documentation\n"
                "- The exact payload schema for every event-driven integration pattern is not fully specified on these pages."
            ),
        },
        "compare_blurb": "You need to emit or consume custom events in a journey.",
        "related": ["api_node"],
    },
    {
        "id": "call_return",
        "aliases": [
            "call and return node", "call return node",
            "call another journey",
            "return back to the same journey", "sub journey",
        ],
        "module_context": ["journey builder", "bot studio"],
        "source_boosts": {"call-and-return-node": 5.0, "multi-journey-user-journeys": 4.0},
        "source_penalties": {"campaign-journey": -4.0},
        "display": "Call & Return Node",
        "page_display": "Call & Return Node",
        "module": "Bot Studio",
        "templates": {
            "setup": (
                "The documentation indicates you should use `Call & Return Node` for this pattern.\n"
                "\n"
                "Recommended setup\n"
                "- Add `Call & Return Node` where the current journey should invoke another journey.\n"
                "- Use it to call the secondary journey.\n"
                "- Return to the original journey when the called journey finishes execution."
            ),
        },
        "compare_blurb": "You need to invoke a sub-journey and return.",
        "related": [],
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
            "agent transfer does not happen",
            "earlier flow or agent",
        ],
        "module_context": [],
        "source_boosts": {"agent-transfer-node": 5.0, "chat-management-assignment-rules": 4.0},
        "source_penalties": {
            "agent-personality": -4.0,
            "response-management-auto-replies-and-customer-satisfaction": -5.0,
        },
        "display": "Agent Transfer Node",
        "page_display": "Agent Transfer Node",
        "module": "Bot Studio",
        "templates": {
            "setup": (
                "The documentation indicates you should use `Agent Transfer Node` for this pattern.\n"
                "\n"
                "Recommended setup\n"
                "- Add `Agent Transfer Node` at the point where the bot should hand over to a human agent.\n"
                "- Save the change in Bot Studio and use `Save & Deploy` if the handover should affect the live channel."
            ),
            "behavior": (
                "The documentation indicates this involves both `Agent Transfer Node` in Bot Studio and `Assignment Rules` in Agent Assist.\n"
                "\n"
                "Documented behavior to check\n"
                "- `Agent Transfer Node` / agent handover is the documented bot-to-agent transfer step.\n"
                "- `Assignment Rules` decide how chats are assigned to agents or teams.\n"
                "- If agents are unavailable when the chat comes for assignment, the system retries assignment for the next 30 minutes.\n"
                "- If agents become available during that time, the chat is assigned; otherwise it moves to unassigned chats for manual supervisor assignment.\n"
                "- `Sticky Assignment` controls whether reopened chats go back to the same agent who previously handled them.\n"
                "\n"
                "What I could not verify from the available documentation\n"
                "- Exact session-persistence or timeout behavior beyond the documented assignment retry window and reopened-chat routing is not explicitly specified."
            ),
        },
        "compare_blurb": "You need to hand over from bot to a human agent.",
        "related": ["assignment_rules", "business_hours"],
    },
]

# Pre-build lookup by id
_CONCEPT_INDEX: Dict[str, Dict] = {c["id"]: c for c in CONCEPT_REGISTRY}
```

## Test

Run the `kb_answer` skill. It should still work exactly as before — the `CONCEPT_REGISTRY` is just data, nothing uses it yet. Confirm the file has no syntax errors by checking that `kb_answer({"query": "test your bot"})` still returns a response.

---
**Next:** Patch 2 adds concepts 10-18 (Goal Node through Live Monitoring).
