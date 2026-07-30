# KB Test Query Sets
**Complete test data for all 3 phases (69 total queries)**

---

## Phase 1: Baseline Queries (10 Queries)

These are the critical-path queries used in `local/test_10_queries.py`.

### Format: [Q#] Query → Expected Outcome

```
Q1.  Where do I find my API keys in the Gupshup Console?
     Expected: REFUSAL (guardrail) ✓
     Why: Security-sensitive (prevents accidental API key exposure)

Q2.  How do I structure JSON for WhatsApp quick reply buttons?
     Expected: ANSWERED
     Why: Baseline - should work (doc exists: stateful-buttons.md)

Q3.  What's the pattern for collecting user input, validating it, then sending 
     a response in a journey?
     Expected: ANSWERED
     Why: Baseline - pattern matching (doc: journey-building-patterns.md)

Q4.  How do I set up a WhatsApp Business Account WABA and connect it to Gupshup?
     Expected: ANSWERED
     Why: Baseline - setup guide exists (doc: waba-setup-detailed.md)

Q5.  What are the steps to onboard an RCS agent through Dotgo RBM Hub?
     Expected: ANSWERED
     Why: Baseline - RCS setup (doc: rcs-agent-setup.md)

Q6.  How do I sync customer data from Salesforce to Gupshup through webhooks?
     Expected: ANSWERED (was IDK before fix)
     Why: PHASE 1 FIX - needs confidence boost
     Before: confidence 0.7 (below 1.2 threshold)
     After:  confidence 0.95 (above 0.8 threshold)

Q7.  How do I configure a WABA in the Gupshup Console and register webhook 
     endpoints?
     Expected: ANSWERED (was IDK before fix)
     Why: PHASE 1 FIX - needs concept registry boost
     Before: confidence 1.4 (below 1.2 threshold)
     After:  confidence 1.40 + waba_console boost

Q8.  What are the API rate limits for sending messages, and how do I handle 
     429 responses?
     Expected: ANSWERED (was IDK before fix)
     Why: PHASE 1 FIX - coverage threshold too strict
     Before: confidence 0.95 (way below 4.0 threshold)
     After:  confidence 4.45 (above 1.0 threshold)

Q9.  What are the steps to create and send my first campaign to 1000 contacts?
     Expected: ANSWERED (was IDK before fix)
     Why: PHASE 1 FIX - intent coverage too strict
     Before: confidence 1.1 (below 1.2 threshold)
     After:  confidence 4.10 (above 0.8 threshold)

Q10. What's the recommended message design best practice for RCS rich cards to 
     maximize engagement?
     Expected: ANSWERED
     Why: Baseline - RCS design (doc: rcs-overview.md)
```

**Phase 1 Success Criteria:**
- ✅ Q1 = REFUSAL (guardrail working)
- ✅ Q2-Q5, Q10 = ANSWERED (no regressions)
- ✅ Q6-Q9 = ANSWERED (all 4 fixed)
- ✅ **Overall: 9/10 (90%)**

---

## Phase 2: IDK Reduction Queries (51 Queries)

These are real production failures from Langfuse. Complete data in:
`local/reports/idk_regression_baseline.json`

### Top 20 High-Priority IDK Queries

```
IDK1.  What are the different console roles and their permissions?
       Top score: 1.40 | Issue: Coverage threshold too high

IDK2.  How would Gupshup Console be used in a retail demo scenario?
       Top score: 1.10 | Issue: Intent classification

IDK3.  What is a Flow ID in WhatsApp Flows?
       Top score: 5.55 | Issue: High score but evidence not selected

IDK4.  How do I create in-app API/JSON/Agent support nodes in Journey Builder?
       Top score: 10.05 | Issue: Evidence filtering bug

IDK5.  What fields are available in webhook payloads?
       Top score: 6.25 | Issue: Schema → intent mapping

IDK6.  How do I set up a webhook server to receive events from Gupshup?
       Top score: 9.75 | Issue: Setup guide exists, coverage refinement

IDK7.  How is retained chat history handled in Gupshup?
       Top score: 1.55 | Issue: Definition query, entity detection

IDK8.  How do I access and view WhatsApp delivery logs and status?
       Top score: 1.55 | Issue: Ops/status feature, module detection

IDK9.  How do I set up an MO callback with an external URL?
       Top score: 1.10 | Issue: Callback pattern not found

IDK10. How do I trigger an external event from an external system?
       Top score: 1.45 | Issue: Trigger mechanism, intent classification

IDK11. What is sticky chat in Agent Assist?
       Top score: 0.0 | Issue: Concept not in KB

IDK12. How do I download leads from Gupshup Console?
       Top score: 0.0 | Issue: Operations/export feature missing

IDK13. What is an Enterprise WhatsApp account?
       Top score: 0.0 | Issue: Account type classification

IDK14. What is Partner portal in Gupshup for WhatsApp onboarding?
       Top score: 0.0 | Issue: Partner feature not documented

IDK15. What is the 'All agents' section in SuperAgent?
       Top score: 0.0 | Issue: SuperAgent feature not documented

IDK16. What short domain should be whitelisted as CTA on DLT?
       Top score: 0.0 | Issue: DLT compliance feature

IDK17. Does Journey Builder support native Google Sheets integration?
       Top score: 0.0 | Issue: Third-party integration capability

IDK18. Do Campaign Manager or Journey Builder support triggered WhatsApp campaigns?
       Top score: 0.0 | Issue: Campaign triggering mechanism

IDK19. Can I use PeopleStrong API REST webhook custom integration?
       Top score: 0.0 | Issue: Specific integration example missing

IDK20. How do I set up custom integrations for external systems?
       Top score: 0.0 | Issue: Generic custom integration pattern
```

### Remaining 31 IDK Queries (IDK21-IDK51)

[Complete list available in `local/reports/idk_regression_baseline.json`]

These cover:
- Bot Studio features (flows, nodes, canvas)
- Channel-specific operations (WhatsApp, RCS, Email)
- Integration patterns (webhooks, APIs, external systems)
- Agent Assist features (templates, SLA, chat routing)
- CTX/Overview features (roles, analytics, onboarding)
- AI Admin tools and developer mode

**Phase 2 Success Criteria:**
- ✅ 45+ of 51 answered (88%+)
- ✅ IDK rate: 35-38%
- ✅ No regressions from Phase 1
- ✅ Module-specific rates >75%

---

## Phase 3: High-Score Failures (8 Queries)

These are queries where `kb_search` found good documents (score > 5.0) 
but `kb_answer` returned IDK. These represent "low-hanging fruit" fixes.

```
HS1.  In-app API/JSON/Agent support nodes in Journey Builder
      Search score: 10.05
      Source: kb/bot-studio/json-handler-instead-of-code-node.md
      Issue: Answer composition, evidence filtering
      Expected fix: Phase 3 answer composition improvements

HS2.  How do I set up a webhook server to receive events from Gupshup?
      Search score: 9.75
      Source: kb/integrations/webhooks.md
      Issue: Setup guide exists but not selected
      Expected fix: Evidence selection refinement

HS3.  What fields are available in webhook payloads (schema)?
      Search score: 6.25
      Source: kb/integrations/webhooks.md
      Issue: Schema query not recognized as "schema" intent
      Expected fix: Intent → evidence mapping

HS4.  What are Webhook V3 modes and how do they differ?
      Search score: 5.90
      Source: kb/integrations/webhooks.md
      Issue: Mode documentation exists but gap in composition
      Expected fix: Multi-answer synthesis

HS5.  What happens when a journey completes? (event handling)
      Search score: 5.15
      Source: kb/bot-studio/whatsapp-flows-static-dynamic.md
      Issue: Event-oriented query not extracting event docs
      Expected fix: Intent-specific evidence filtering

HS6.  How do I migrate from template to AI journey?
      Search score: 2.40
      Source: kb/bot-studio/whatsapp-carousel-message-using-the-send-message-node.md
      Issue: Intent mismatch (setup vs. migration pattern)
      Expected fix: Intent classification refinement

HS7.  What is Catalog message API and when do I use it?
      Search score: 0.85
      Source: kb/channels/whatsapp-business-api.md
      Issue: API discovery pattern weak
      Expected fix: Concept registry addition (catalog_api)

HS8.  How do I set up a custom REST webhook integration for external systems?
      Search score: N/A (no search result)
      Issue: Integration example documentation missing
      Expected fix: Create stub doc for custom integration pattern
```

**Phase 3 Success Criteria:**
- ✅ 7-8 of 8 answered (88-100%)
- ✅ IDK rate: 20-25%
- ✅ Overall answer rate: 75-80%
- ✅ High-score gap closed (<0.5)

---

## Complete Query List (CSV Format)

For bulk testing/comparison:

```csv
id,query,expected,phase,source,issue,priority
Q1,"Where do I find my API keys in the Gupshup Console?",refusal,1,guardrail,security,p0
Q2,"How do I structure JSON for WhatsApp quick reply buttons?",answer,1,baseline,button-json,p0
Q3,"What's the pattern for collecting user input, validating it, then sending a response in a journey?",answer,1,baseline,input-validation,p0
Q4,"How do I set up a WhatsApp Business Account WABA and connect it to Gupshup?",answer,1,baseline,waba-setup,p0
Q5,"What are the steps to onboard an RCS agent through Dotgo RBM Hub?",answer,1,baseline,rcs-setup,p0
Q6,"How do I sync customer data from Salesforce to Gupshup through webhooks?",answer,1,fix,webhook-salesforce,p0
Q7,"How do I configure a WABA in the Gupshup Console and register webhook endpoints?",answer,1,fix,waba-webhook,p0
Q8,"What are the API rate limits for sending messages, and how do I handle 429 responses?",answer,1,fix,api-limits,p0
Q9,"What are the steps to create and send my first campaign to 1000 contacts?",answer,1,fix,campaign-creation,p0
Q10,"What's the recommended message design best practice for RCS rich cards to maximize engagement?",answer,1,baseline,rcs-design,p0
IDK1,"What are the different console roles and their permissions?",answer,2,langfuse,console-roles,p1
IDK2,"How would Gupshup Console be used in a retail demo scenario?",answer,2,langfuse,retail-demo,p1
IDK3,"What is a Flow ID in WhatsApp Flows?",answer,2,langfuse,flow-id,p1
... (41 more IDK queries)
HS1,"In-app API/JSON/Agent support nodes in Journey Builder",answer,3,langfuse,api-nodes,p2
HS2,"How do I set up a webhook server to receive events from Gupshup?",answer,3,langfuse,webhook-server,p2
... (6 more HS queries)
```

---

## How to Use This File

### For Phase 1 Testing
Copy Q1-Q10 into `local/test_10_queries.py` TEST_QUERIES list if updating.

### For Phase 2 Testing
Query list stored in `local/reports/idk_regression_baseline.json` 
Use with `python3 local/run_comprehensive_test.py --phase 2`

### For Phase 3 Testing
Create high-score query list in `local/reports/high_score_failures.json`
Use with `python3 local/run_comprehensive_test.py --phase 3`

### For Custom Testing
Copy/paste specific queries into a Python script:

```python
test_queries = [
    "Where do I find my API keys in the Gupshup Console?",
    "How do I structure JSON for WhatsApp quick reply buttons?",
    # ... more queries
]

for query in test_queries:
    result = kb_answer.answer(query)
    print(f"Query: {query}")
    print(f"Answered: {not result.is_idk}")
    print()
```

---

## Query Characteristics

### By Intent
- **Setup** (13): Q4, Q5, Q7, Q9, IDK6, IDK8, IDK9, HS2, HS4, HS8, ...
- **Definition** (12): Q2, Q3, Q10, IDK1, IDK7, IDK11, IDK13, ...
- **Schema** (8): Q8, IDK5, IDK20, HS3, ...
- **Troubleshooting** (4): IDK16, IDK18, ...
- **Overview** (3): IDK2, IDK12, IDK14, ...
- **Refusal** (1): Q1

### By Module
- **Bot Studio** (16): Q3, Q9, IDK3, IDK4, IDK9, HS1, HS5, ...
- **Channels** (12): Q2, Q4, Q5, IDK8, IDK13, ...
- **Integrations** (14): Q6, Q7, Q8, IDK20, HS2, HS3, HS7, ...
- **Agent Assist** (8): IDK1, IDK11, IDK17, ...
- **CTX/Overview** (6): IDK2, IDK12, IDK14, IDK15, ...
- **AI Admin** (4): IDK16, IDK19, ...
- **General/Cross** (9): Q1, Q10, ...

### By Difficulty
- **Easy (Q2, Q4, Q10):** Straightforward doc lookup
- **Medium (Q3, Q5, Q6, Q7, Q9):** Pattern matching + entity recognition
- **Hard (Q8, IDK1-IDK20):** Multi-concept, coverage, intent classification
- **Very Hard (HS1-HS8, IDK21+):** High search scores but answer composition issues

---

## Extending the Test Set

To add more test queries:

1. **Get them from Langfuse traces:** `python3 local/scripts/fetch_recent_idk.py`
2. **Manually add:** Edit `local/reports/idk_regression_baseline.json`
3. **Update test runner:** Add to `local/run_comprehensive_test.py`
4. **Record expected outcome:** Expected to be ANSWERED unless otherwise noted

---

**Created:** 2026-06-16  
**Total Queries:** 69 (10 baseline + 51 IDK + 8 high-score)  
**Last Updated:** 2026-06-16
