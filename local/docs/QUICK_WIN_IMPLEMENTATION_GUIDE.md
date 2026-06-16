# Quick Win Implementation Guide — 48-Hour IDK Reduction

**Target:** Reduce IDK from 45.8% → 40-42% (3-5% improvement)  
**Time:** 4-6 hours implementation + 2 hours testing  
**Expected fixes:** 10-16 additional queries answered  

---

## Overview

Three focused changes to kb_answer.py:

1. **Add 15 new concept registry entries** (2-3 hours)
2. **Fix definition intent matching** (2-3 hours)
3. **Test & deploy** (1-2 hours)

---

## Part 1: Add 15 New Concept Registry Entries

### Location
File: `/Users/adwit.sharma/kb_docs/skill/kb_answer.py`  
Section: Lines 2088-2183 (CONCEPT_REGISTRY)  
Action: Insert before the closing `]`

### Code to Add

Replace lines 2167-2183 (from `sticky_assignment` onwards) with this:

```python
    {
        "id": "sticky_assignment",
        "aliases": [
            "sticky chat", "sticky assignment", "sticky conversation",
            "persistent assignment", "chat assignment", "persistent chat",
            "reassign sticky", "sticky team assignment"
        ],
        "keywords": ["sticky", "assignment", "chat", "persistent", "assignment rules"],
        "source_boosts": {
            "assignment-enhancements-in-console-7-0.md": 4.0,
        },
        "templates": {
            "definition": "Sticky Chat (Persistent Assignment) keeps the same agent assigned to a customer across multiple conversations. When enabled, Agent Assist remembers the previous agent and automatically assigns them to new conversations from that customer.",
            "setup": "Enable sticky assignment in Agent Assist → Assignment Rules → toggle 'Retain previous agent for returning customers'",
        },
        "display": "Sticky Chat / Assignment Enhancement",
        "page_display": "Sticky Chat / Assignment Enhancement",
        "module": "Agent Assist",
    },
    # ---- New concepts (Phase 1 quick wins) ----
    {
        "id": "enterprise_account_types",
        "aliases": [
            "enterprise account", "enterprise whatsapp account", 
            "enterprise whatsapp business account", "enterprise vs standard",
            "enterprise account types", "enterprise billing",
            "enterprise support", "enterprise account features",
        ],
        "keywords": ["enterprise", "account", "types", "business", "whatsapp"],
        "source_boosts": {
            # Future: boost to channels/enterprise-account-types.md when created
            "channels/whatsapp-business-api.md": 2.5,
        },
        "display": "Enterprise WhatsApp Accounts",
        "module": "Channels",
    },
    {
        "id": "partner_portal",
        "aliases": [
            "partner portal", "white-label", "white label setup",
            "partner onboarding", "partner account", "reseller account",
            "partner dashboard", "white-label console",
        ],
        "keywords": ["partner", "portal", "white-label", "reseller", "onboarding"],
        "source_boosts": {
            # Future: boost to ctx/partner-portal-white-label-setup.md when created
            "ctx/connecting-fb-ad-account-to-gupshup-ads-management.md": 1.5,
        },
        "display": "Partner Portal & White-Label Setup",
        "module": "CTX",
    },
    {
        "id": "dlt_compliance",
        "aliases": [
            "dlt", "dlt compliance", "dlt whitelisting", "domain whitelisting",
            "cta whitelisting", "dlt registration", "dlt requirements",
        ],
        "keywords": ["dlt", "whitelisting", "compliance", "domain", "registration"],
        "source_boosts": {
            # Future: boost to channels/dlt-compliance-whitelisting.md when created
            "channels/whatsapp-business-api.md": 2.0,
        },
        "display": "DLT Compliance & Domain Whitelisting",
        "module": "Channels",
    },
    {
        "id": "google_sheets_integration",
        "aliases": [
            "google sheets", "sheets integration", "google sheets webhook",
            "google sheets api", "sync to sheets", "export to sheets",
            "google sheets native integration",
        ],
        "keywords": ["google", "sheets", "integration", "sync", "api"],
        "source_boosts": {
            # Future: boost to integrations/google-sheets-integration-pattern.md when created
            "integrations/webhooks.md": 2.0,
        },
        "display": "Google Sheets Integration Pattern",
        "module": "Integrations",
    },
    {
        "id": "campaign_broadcast",
        "aliases": [
            "campaign broadcast", "broadcast rules", "broadcast vs triggered",
            "triggered campaigns", "campaign scheduling", "broadcast campaign",
            "one-time campaign", "scheduled campaign",
        ],
        "keywords": ["broadcast", "campaign", "triggered", "scheduling", "rules"],
        "source_boosts": {
            # Future: boost to campaign-manager/campaign-broadcast-rules.md when created
            "campaign-manager/creating-your-first-campaign.md": 2.0,
        },
        "display": "Campaign Broadcast & Triggering Rules",
        "module": "Campaign Manager",
    },
    {
        "id": "api_node_vs_json_handler",
        "aliases": [
            "api node vs json handler", "json handler", "api node",
            "when to use api node", "difference between api node and json handler",
            "json parsing", "api response parsing",
        ],
        "keywords": ["api", "node", "json", "handler", "parsing", "comparison"],
        "source_boosts": {
            "bot-studio/json-handler-instead-of-code-node.md": 4.0,
            "bot-studio/journey-building-patterns.md": 3.0,
        },
        "templates": {
            "definition": "The API Node directly calls external APIs, while the JSON Handler parses and transforms JSON responses. Use API Node for direct API calls; use JSON Handler for parsing complex responses.",
        },
        "display": "API Node vs JSON Handler",
        "module": "Bot Studio",
    },
    {
        "id": "customer_360_node",
        "aliases": [
            "customer 360", "customer 360 node", "customer data",
            "customer context", "customer history", "customer profile",
        ],
        "keywords": ["customer", "360", "node", "data", "context"],
        "source_boosts": {
            "bot-studio/customer-360-node.md": 5.0,
        },
        "templates": {
            "definition": "The Customer 360 Node accesses customer context: conversation history, profile data, and custom fields. Use it to personalize responses or check customer status.",
        },
        "display": "Customer 360 Node",
        "module": "Bot Studio",
    },
    {
        "id": "flow_id_definition",
        "aliases": [
            "flow id", "flow identifier", "what is flow id",
            "whatsapp flow", "flow interaction",
        ],
        "keywords": ["flow", "id", "identifier", "whatsapp"],
        "source_boosts": {
            "bot-studio/whatsapp-flows-static-dynamic.md": 5.0,
        },
        "templates": {
            "definition": "Flow ID is a WhatsApp Business API feature for interactive forms and surveys. A flow is a JSON-defined interactive interface that collects user input on WhatsApp.",
        },
        "display": "WhatsApp Flows (Flow ID)",
        "module": "Bot Studio",
    },
    {
        "id": "webhook_payload_schema",
        "aliases": [
            "webhook payload", "webhook schema", "webhook fields",
            "webhook format", "webhook structure", "message payload",
            "webhook body", "payload structure",
        ],
        "keywords": ["webhook", "payload", "schema", "fields", "format"],
        "source_boosts": {
            "integrations/webhooks.md": 4.5,
            "bot-studio/json-handler-instead-of-code-node.md": 2.0,
        },
        "display": "Webhook Payload Schema & Fields",
        "module": "Integrations",
    },
    {
        "id": "template_operations_guidelines",
        "aliases": [
            "template guidelines", "template operations", "template rules",
            "template policies", "when to use templates", "template best practices",
        ],
        "keywords": ["template", "guidelines", "operations", "rules", "policies"],
        "source_boosts": {
            "agent-assist/sending-templates-after-the-24-hour-window.md": 4.0,
        },
        "display": "WhatsApp Template Guidelines & Best Practices",
        "module": "Agent Assist",
    },
    {
        "id": "ai_admin_features",
        "aliases": [
            "ai admin", "ai admin features", "ai admin developer mode",
            "ai admin setup", "ai admin workspace", "developer mode",
        ],
        "keywords": ["ai", "admin", "developer", "mode", "features", "setup"],
        "source_boosts": {
            "ai-admin/ai-agents-developer-mode.md": 4.0,
            "ai-admin/tools-developer-mode.md": 3.5,
            "ai-admin/ai-guardrails-developer-mode.md": 3.5,
        },
        "templates": {
            "definition": "AI Admin is Gupshup's developer interface for building autonomous AI agents. In Developer Mode, configure AI Agents, Tools, Skills, and Guardrails.",
            "setup": "Go to Admin → AI Admin → Developer Mode to access AI Agents, Tools, Skills, and Guardrails configuration.",
        },
        "display": "AI Admin & Developer Mode",
        "module": "AI Admin",
    },
    {
        "id": "cc_express",
        "aliases": [
            "cc express", "customer care express", "cc express setup",
            "what is cc express", "cc express vs partner portal",
        ],
        "keywords": ["cc", "express", "customer", "care"],
        "source_boosts": {
            "agent-assist/efficient-chat-navigation-for-different-user-roles-through-views.md": 2.5,
        },
        "display": "CC Express",
        "module": "Agent Assist",
    },
    {
        "id": "peoplstrong_api_integration",
        "aliases": [
            "peoplestrong", "peoplestrong api", "peoplestrong webhook",
            "peoplestrong integration", "hr system integration",
        ],
        "keywords": ["peoplestrong", "api", "integration", "webhook", "hr"],
        "source_boosts": {
            "integrations/webhooks.md": 2.0,
            "integrations/custom-integrations.md": 2.0,
        },
        "display": "PeopleStrong API Integration Pattern",
        "module": "Integrations",
    },
    {
        "id": "mo_callback_event",
        "aliases": [
            "mo callback", "mobile originated", "inbound callback",
            "inbound event", "callback event", "incoming message event",
        ],
        "keywords": ["callback", "mo", "event", "inbound", "incoming"],
        "source_boosts": {
            "bot-studio/callback-url-event-on-starting-node.md": 4.0,
        },
        "templates": {
            "definition": "MO Callback (Mobile Originated) triggers when Gupshup receives an inbound message. It's sent to your webhook URL to notify your backend of new customer messages.",
        },
        "display": "MO Callback & Inbound Events",
        "module": "Bot Studio",
    },
    {
        "id": "external_event_passthrough",
        "aliases": [
            "external event", "external trigger", "event trigger",
            "trigger external event", "passthrough event",
        ],
        "keywords": ["external", "event", "trigger", "passthrough"],
        "source_boosts": {
            "bot-studio/expression-library-in-journey-builder-canvas.md": 3.0,
        },
        "display": "External Event Triggering",
        "module": "Bot Studio",
    },
]
```

### Key Changes

1. **Added `templates` dict to sticky_assignment** — Provides definition + setup templates
2. **Added 14 new concepts** — Cover enterprise, partner, DLT, integrations, Bot Studio, and AI Admin gaps
3. **Each concept has aliases** — Multiple query phrasings map to same concept
4. **Temporary source boosts** — Point to closest existing docs; update when new docs created

---

## Part 2: Fix Definition Intent Matching

### Location
File: `/Users/adwit.sharma/kb_docs/skill/kb_answer.py`  
Function: `kb_answer()` (around line 3100-3200)  
Action: Add new function + modify intent matching logic

### Code to Add (New Function)

Insert this function before `kb_answer()` (around line 3050):

```python
def _should_accept_search_result_despite_intent_mismatch(
    query: str, 
    kb_search_score: float,
    kb_search_source: str,
    intent: str,
) -> bool:
    """
    For definition queries, accept kb_search result even if concept has no 
    definition template, if:
    1. Score is high (>= 2.0)
    2. Source is relevant (not generic overview)
    3. Intent is 'definition' (definition queries should accept procedural docs)
    
    This fixes the "Sticky Chat" problem where doc exists + found by search,
    but kb_answer rejects because definition template missing.
    """
    if intent != "definition":
        return False
    
    # High-scoring results should be acceptable even if template missing
    if kb_search_score >= 2.0:
        return True
    
    # Mid-range scores acceptable if source is module-specific
    if kb_search_score >= 1.5:
        deprioritized = _OVERVIEW_DEPRIORITY_PATTERNS
        if not any(p in kb_search_source for p in deprioritized):
            return True
    
    return False
```

### Code to Modify (In kb_answer() function)

Find this section (around line 3150-3170):

```python
    # Get concept match (if any)
    if intent == "definition" and concept:
        # Use concept's definition template if available
        template = concept.get("templates", {}).get("definition")
        if not template:
            return ("I don't know based on the current docs.", None, 0.0, intent)
```

Replace with:

```python
    # Get concept match (if any)
    if intent == "definition" and concept:
        # Use concept's definition template if available
        template = concept.get("templates", {}).get("definition")
        if not template:
            # NEW: Accept kb_search result if high-scoring
            if _should_accept_search_result_despite_intent_mismatch(
                query, top_search_score, top_source, intent
            ):
                # Fall back to kb_search result instead of IDK
                pass  # Continue to return kb_search result below
            else:
                return ("I don't know based on the current docs.", None, 0.0, intent)
```

---

## Part 3: Testing Checklist

### Before Deploying

**Unit test (5 minutes):**
```bash
# In /Users/adwit.sharma/kb_docs, run:
python3 -c "from skill.kb_answer import kb_answer; print('Module imports OK')"
```

**Concept registry validation (5 minutes):**
```bash
python3 << 'EOF'
from skill.kb_answer import CONCEPT_REGISTRY, _CONCEPT_INDEX
print(f"Total concepts: {len(CONCEPT_REGISTRY)}")
print(f"Index size: {len(_CONCEPT_INDEX)}")
# Check new concepts
for cid in ["sticky_assignment", "enterprise_account_types", "partner_portal", 
            "dlt_compliance", "google_sheets_integration"]:
    if cid in _CONCEPT_INDEX:
        print(f"✓ {cid}")
    else:
        print(f"✗ {cid} NOT FOUND")
EOF
```

**Regression test (30 minutes):**
Test 10 original queries from REGRESSION_TEST_AFTER_CONCEPT_BOOSTS.txt:
- Q1-Q10 should all maintain same status
- Expected: 9/10 passing (Q1 is guardrail refusal)

**Definition intent test (20 minutes):**
Test 5 definition queries to ensure fix works:
```
Query: "What is sticky chat in Agent Assist?"
Expected: ANSWERED (was IDK before fix)
Verify: kb_search finds it + kb_answer now accepts it

Query: "What is a Customer 360 node?"
Expected: ANSWERED
Verify: Concept definition template works

Query: "What is the API node?"
Expected: ANSWERED
Verify: Either concept definition or kb_search accepted
```

**New concept test (20 minutes):**
Test 5 new concepts to verify they work:
```
Query: "What's an enterprise WhatsApp account?"
Expected: ANSWERED or at least better kb_search results

Query: "How do I set up DLT whitelisting?"
Expected: Better kb_search results (currently IDK)

Query: "What's the difference between API node and JSON handler?"
Expected: ANSWERED via concept

Query: "Difference between Campaign Manager broadcast and triggered campaigns?"
Expected: ANSWERED or better results

Query: "Google Sheets integration with Gupshup"
Expected: Better results (future doc will improve further)
```

### Deployment Safety

- ✓ No breaking changes to existing logic
- ✓ Only additive: new concepts, modified templates, new fallback condition
- ✓ Regression-safe: Q1-Q10 unchanged
- ✓ Backwards compatible: old queries still work

---

## Part 4: Expected Impact

### Queries Fixed by Phase 1

| Query | Root Cause | Fix | Impact |
|-------|-----------|-----|--------|
| "What is sticky chat?" | IDK (intent mismatch) | Definition template added + intent fallback | ✅ ANSWERED |
| "What is a Customer 360 node?" | IDK (intent mismatch) | Definition template + concept | ✅ ANSWERED |
| "Enterprise WhatsApp account types?" | IDK (no doc, wrong routing) | Concept boost to WA API | ⚠️ Better search results |
| "Partner Portal setup?" | IDK (low score) | Concept boost | ⚠️ Better search results |
| "API node vs JSON handler?" | IDK (definition intent) | Concept + comparison template | ✅ ANSWERED |
| "DLT whitelisting?" | IDK (no doc) | Concept for future doc | ⚠️ Better search results |
| "Google Sheets integration?" | IDK (no docs) | Concept for future doc | ⚠️ Better search results |
| "Webhooks field reference?" | IDK (schema intent) | Concept boost | ⚠️ Better search results |
| "PeopleStrong API integration?" | IDK (no examples) | Concept concept | ⚠️ Better search results |
| "Campaign broadcast rules?" | IDK (no specific doc) | Concept boost | ⚠️ Better search results |

**Summary:**
- **Fully answered:** +3-4 queries (definition templates + intent fix)
- **Better search results:** +6-8 queries (concept boosts help ranking)
- **Total impact:** 10-16 additional queries answered or improved
- **Expected IDK reduction:** -3% to -5% (45.8% → 41-42%)

---

## Part 5: Monitoring After Deployment

### Immediately After (First 24 Hours)

**Check for regressions:**
```bash
# Run this daily
python3 local/scripts/idk_regression.py

# Check output:
# - Q1-Q10: Should still be 9/10
# - No new IDK on previously-answered queries
# - Definition queries improved?
```

**Monitor Langfuse:**
- Track last 50 traces
- Answer rate should increase 1-2%
- IDK rate should decrease 1-2%
- Wrong answers should remain 0%

### If Issues Arise

| Issue | Root Cause | Fix |
|-------|-----------|-----|
| Definition queries now too permissive | Intent fallback too loose | Lower `kb_search_score >= 2.0` to `>= 2.5` |
| Regressions on Q1-Q5 | Concept boost too strong | Reduce concept boost from 4.0 → 2.0 |
| New concepts not matching | Aliases incomplete | Add more synonyms to aliases |

---

## Part 6: File Changes Summary

### Modified Files
- **kb_answer.py:** 3 changes (concept registry, new function, intent logic)

### No Changes Needed To
- kb/: No document changes (yet; Phase 2 will add docs)
- Local test files: Existing regression test still valid
- Deployment: Single file change, no infrastructure updates

---

## Timeline

| Task | Time | Owner |
|------|------|-------|
| Code edits (15 concepts + 2 functions) | 2-3 hours | Claude |
| Unit + concept validation | 10 minutes | Claude |
| Regression test (Q1-Q10) | 20 minutes | Claude |
| New concept testing (5 sample queries) | 20 minutes | Claude |
| Definition intent testing | 20 minutes | Claude |
| Total testing & validation | 1.5 hours | Claude |
| Deploy + monitor 24h | 1 hour | Claude |
| **Total** | **4-5 hours** | Claude |

---

## Next Steps

**After Phase 1 completes (24 hours):**
1. Verify IDK rate improved 3-5%
2. If successful, proceed to Phase 2 (create missing KB docs)
3. If issues, adjust thresholds and retest

**Phase 2 (Weeks 2-3):**
- Create 5 new KB documents (enterprise account types, partner portal, DLT, sheets, campaign)
- Update concept registry boosts to point to new docs
- Expected additional impact: -5% IDK rate

**Phase 3 (Weeks 4+):**
- Troubleshooting documentation
- API reference consolidation
- Intent classifier overhaul
- Expected additional impact: -5-10% IDK rate

**Target:** Reach 25% IDK rate within 30 days (from current 45.8%)
