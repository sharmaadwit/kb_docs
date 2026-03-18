# Patch 4 of 9 — Entity extraction + Intent classification + Page display map

**File:** `kb_answer.py`
**Depends on:** Patch 3
**Risk:** Zero — adds new functions only.

> **IMPORTANT — DO NOT touch telemetry code.** All Langfuse integration, tracing, span logging, and telemetry-related functions/imports must remain exactly as they are. This patch does not modify telemetry and neither should you.

## Step 0a — Add aliases to live_monitoring (from Patch 2)

In `CONCEPT_REGISTRY`, find the `live_monitoring` entry. In its `"aliases"` list, find:

```
            "wait time metrics", "agent state metrics",
        ],
```

Replace with:

```python
            "wait time metrics", "agent state metrics",
            "agent availability", "live agent",
        ],
```

## Step 0b — Harden guardrail term lists

Find `OFFTOPIC_TERMS` near the top of the file. In its list, find:

```
    "tv show", "phone to buy", "workout routine", "travel plan",
    "cricket score",
]
```

Replace with:

```python
    "tv show", "phone to buy", "workout routine", "travel plan",
    "cricket score", "salesforce", "hubspot", "zoho",
]
```

Find `SENSITIVE_PATTERNS`. In its list, find:

```
    "do not say i don t know make the most likely answer up",
```

Replace with:

```python
    "do not say i don t know make the most likely answer up",
    "hack into", "hack the", "exploit",
```

## Step 1 — Add _PAGE_DISPLAY_MAP and _canonical_page_name after _module_from_source

**Find the end of the `_module_from_source` function** (it ends with `return "General"`). After that function, add:

```python


_PAGE_DISPLAY_MAP = [
    ("test-your-bot", "Test your Bot"),
    ("user-management-business-hours", "User Management: Business Hours"),
    ("response-management-auto-replies-and-customer-satisfaction",
     "Response Management: Auto Replies & Customer Satisfaction"),
    ("chat-management-assignment-rules", "Chat Management: Assignment Rules"),
    ("live-monitoring-dashboard-real-time-chat-analytics-and-performance-insights",
     "Live Monitoring Dashboard"),
    ("go-live-with-instagram", "Go Live with Instagram"),
    ("retain-customer-chat-history", "Retain Customer Chat History"),
    ("integrations/webhooks", "Webhooks"),
    ("campaign-analytics", "Campaign Analytics"),
    ("goal-analytics", "Goal Analytics"),
    ("ctwa-to-bot-to-goals", "Ctwa To Bot To Goals"),
    ("save-vs-save-deploy", "Save Vs Save & Deploy"),
    ("save-save-and-deploy", "Save Vs Save & Deploy"),
    ("timeout-in-prompt-nodes", "Timeout in Prompt Nodes"),
    ("workflows/webhooks-to-delivery-analytics", "Webhooks To Delivery Analytics"),
    ("how-to-measure-click-through-rates", "Campaign Analytics"),
    ("json-handler", "JSON Handler"),
    ("condition-node", "Condition Node"),
    ("manage-variables", "Manage Variables"),
    ("modify-variable-node", "Modify Variable Node"),
    ("prompt-nodes", "Prompt Nodes"),
    ("free-text-node", "Free Text Node"),
    ("api-node-http-status-code-branching", "API Node: HTTP Status Code Branching"),
    ("api-node", "API Node"),
    ("trigger-event-node", "Trigger Event Node"),
    ("call-and-return-node", "Call & Return Node"),
    ("agent-transfer-node", "Agent Transfer Node"),
    ("goal-node", "Goal Node"),
]


def _canonical_page_name(source: str, heading_path: List[str] = None, heading: str = "") -> str:
    low = (source or "").lower()
    for token, label in _PAGE_DISPLAY_MAP:
        if token in low:
            return label
    if heading_path:
        for item in heading_path:
            clean = re.sub(r"^[#\-\*\s]+", "", str(item)).strip()
            clean = re.sub(r"\*\*", "", clean)
            if clean:
                return clean
    if heading:
        clean = re.sub(r"^[#\-\*\s]+", "", heading).strip()
        return re.sub(r"\*\*", "", clean)
    return ""
```

## Step 2 — Add _extract_entities, signal lists, and _classify_intent after _canonical_page_name

**After the `_canonical_page_name` function you just added, add:**

```python


# ---------------------------------------------------------------------------
# Section 6 — Entity extraction and intent classification
# ---------------------------------------------------------------------------

def _extract_entities(query: str) -> List[Dict]:
    """Identify which concepts from the registry are mentioned in the query.
    Results are sorted by match quality (total matched alias length) so the
    most specific match is first."""
    q = _normalize_query_for_match(query)
    matched = []
    matched_ids = set()

    for concept in CONCEPT_REGISTRY:
        if concept["id"] in matched_ids:
            continue
        hits = [a for a in concept["aliases"] if a in q]
        if not hits:
            continue
        match_score = sum(len(a) for a in hits)
        if concept.get("module_context") and any(ctx in q for ctx in concept["module_context"]):
            match_score += 5
        matched.append((match_score, concept))
        matched_ids.add(concept["id"])

    matched.sort(key=lambda pair: pair[0], reverse=True)
    return [pair[1] for pair in matched]


_COMPARE_SIGNALS = [" vs ", " versus ", " difference ", " compare "]
_CHOOSE_SIGNALS = [
    "which one should", "which is better", "when should i use",
    "which page should i", "which should i use",
    "which page controls", "which two",
    "should i check", "first or", "or go straight",
    "or should i", "check first",
]
_PAGE_LOOKUP_SIGNALS = [
    "which page", "where do i", "where exactly", "which dashboard",
    "which report", "what page", "where can i monitor",
    "which screen", "which doc", "which settings page",
    "what doc", "what screen", "what settings", "where is",
]
_DEFINITION_SIGNALS = ["what is", "what does", "mean in"]
_BEHAVIOR_SIGNALS = [
    "what happens", "how do timeouts work", "when enabled", "when disabled",
    "after hours", "anonymous users", "returning customers",
    "real time operations view", "explain why", "why a customer",
    "why the customer", "why hours later",
]
_TROUBLESHOOT_SIGNALS = [
    "what should we check", "what should i check", "missing",
    "not seeing", "wrong", "troubleshoot", "issue",
]
_SCHEMA_SIGNALS = [
    "schema", "payload", "statuses", "fields to store",
    "how should we store",
]

INTENT_TYPES = [
    "compare", "choose_between", "page_lookup", "definition",
    "behavior", "troubleshooting", "schema", "chain", "setup",
]


def _classify_intent(query: str, entities: List[Dict]) -> str:
    """Determine the primary intent type for this query."""
    q = _normalize_query_for_match(query)

    is_compare = any(x in q for x in _COMPARE_SIGNALS)
    is_choose = any(x in q for x in _CHOOSE_SIGNALS)
    is_page = any(x in q for x in _PAGE_LOOKUP_SIGNALS)
    is_definition = any(x in q for x in _DEFINITION_SIGNALS)
    is_behavior = any(x in q for x in _BEHAVIOR_SIGNALS)
    is_troubleshoot = any(x in q for x in _TROUBLESHOOT_SIGNALS)
    is_schema = any(x in q for x in _SCHEMA_SIGNALS)

    if is_compare:
        return "compare"
    if is_choose and len(entities) >= 2:
        return "compare"
    if len(entities) >= 2 and " or " in q:
        return "compare"
    if is_page:
        if len(entities) >= 2:
            return "compare"
        return "page_lookup"
    if is_schema:
        return "schema"
    if is_behavior:
        return "behavior"
    if is_definition:
        return "definition"
    if is_troubleshoot:
        return "troubleshooting"
    if len(entities) >= 3:
        return "chain"
    return "setup"
```

## Step 3 — Replace existing _detect_intents with updated version

**Find the existing `def _detect_intents` function and replace the entire function with:**

```python
def _detect_intents(query: str) -> List[str]:
    """Legacy-compatible: return list of intent labels."""
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

## Test

Run `kb_answer({"query": "test your bot"})`. Should still return the same answer — new functions exist but nothing calls them yet.

### Smoke test — entity extraction and intent (verify new functions work)

These new functions are not yet wired into `kb_answer()`, but you can test them directly in a Python console or test script:

**Single-intent queries:**

| Query | Expected entities | Expected intent |
|-------|------------------|-----------------|
| `"Where do I configure business hours?"` | `business_hours` | `page_lookup` |
| `"What is sticky assignment?"` | `sticky_assignment` | `definition` |
| `"How do I test my bot before going live?"` | `test_your_bot` | `setup` |
| `"What does Goal Achieved mean in goal analytics?"` | `goal_analytics` | `definition` |
| `"Where do I add a webhook callback URL?"` | `webhooks` | `page_lookup` |
| `"How do I collect text user input in a journey?"` | `prompt_node` | `setup` |
| `"What happens when a prompt node times out?"` | `prompt_timeout` | `behavior` |
| `"Which dashboard shows ongoing chats and wait time metrics?"` | `live_monitoring` | `page_lookup` |

**Multi-intent / Compare queries:**

| Query | Expected entities | Expected intent |
|-------|------------------|-----------------|
| `"Should I check business hours or auto replies for away messages?"` | `business_hours`, `auto_replies` | `compare` |
| `"Which page shows campaign click metrics vs goal conversions?"` | `campaign_analytics`, `goal_analytics` | `compare` |
| `"Where do I configure sticky assignment vs assignment rules?"` | `sticky_assignment`, `assignment_rules` | `compare` |
| `"CTWA traffic or campaign analytics — where do I check conversions?"` | `ctwa_to_goals`, `campaign_analytics` | `compare` |

**Negative / Off-topic queries (should return empty entity list):**

| Query | Expected entities | Notes |
|-------|------------------|-------|
| `"How do I make pizza?"` | `[]` | Off-topic, no product match |
| `"Tell me about Salesforce CRM integrations"` | `[]` | Off-topic, blocked by OFFTOPIC_TERMS |

---
**Next:** Patch 5 adds _score_chunk_v2 and evidence selection + answer composition functions.
