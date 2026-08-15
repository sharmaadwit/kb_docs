# Consulting-Tone Implementation: Technical Specification

**Document:** Implementation guide for kb_answer.py consulting-tone rollout  
**Target Audience:** Engineers implementing Phase 1-4  
**Current Code Location:** /skill/kb_answer.py  

---

## Phase 1: Soft Gradient (Week 1)

### Goal
Replace binary confidence threshold (0.5) with graduated response bands. No response format changes.

### Code Changes

#### Change 1: Add Confidence Band Constants
```python
# kb_answer.py line ~1060 (near MIN_EVIDENCE_SCORE)

# Confidence thresholds for graduated response tiers
CONFIDENCE_TIER_FULL = 0.80      # Full answer, no caveats
CONFIDENCE_TIER_ANSWER = 0.60    # Answer + optional follow-up prompt
CONFIDENCE_TIER_CONSULT = 0.40   # Consulting question instead of full answer
# CONFIDENCE_TIER_IDK = 0.0       # Below 0.40 = IDK (implicit)
```

#### Change 2: Add Confidence Banding Function
```python
# kb_answer.py line ~5840 (after _reported_confidence)

def _confidence_band(confidence: float) -> str:
    """Map confidence to response tier.
    
    Returns one of: "full", "answer", "consult", "idk"
    """
    if confidence >= CONFIDENCE_TIER_FULL:
        return "full"
    elif confidence >= CONFIDENCE_TIER_ANSWER:
        return "answer"
    elif confidence >= CONFIDENCE_TIER_CONSULT:
        return "consult"
    else:
        return "idk"
```

#### Change 3: Modify Evidence Selection Logic
```python
# kb_answer.py line ~6654 (in kb_answer() function, after evidence selection)

# BEFORE (current):
evidence = _select_evidence(query, scored, intent, explicit_module)
answer = _compose_answer(query, intent, entities, evidence, explicit_module)
if not evidence or "i don't know" in answer.lower():
    # Hard boundary at confidence < 0.5
    return IDK_RESPONSE

# AFTER (Phase 1):
evidence = _select_evidence(query, scored, intent, explicit_module)
confidence = _reported_confidence(query, evidence)
band = _confidence_band(confidence)

if band in ("full", "answer", "consult"):
    # Proceed to answer composition even for low/medium confidence
    answer = _compose_answer(query, intent, entities, evidence, explicit_module)
    if not evidence:
        # Still no evidence found
        answer = "I don't know based on the current docs."
    # Ensure answer text reflects confidence tier (add to metadata, not text)
else:
    # band == "idk"
    answer = "I don't know based on the current docs."
```

#### Change 4: Return Confidence Tier in Langfuse
```python
# kb_answer.py line ~7320 (in langfuse metadata)

# BEFORE:
langfuse_data = {
    "confidence": _reported_confidence(query, evidence),
    ...
}

# AFTER:
confidence = _reported_confidence(query, evidence)
langfuse_data = {
    "confidence": confidence,
    "confidence_tier": _confidence_band(confidence),  # NEW
    ...
}
```

### Testing (Phase 1)

```python
# local/scripts/test_phase1_soft_gradient.py

import json
from skill import kb_answer

def test_confidence_bands():
    test_cases = [
        ("How do I set up WhatsApp?", "full"),  # Should be 0.80+
        ("How do I set up my first campaign?", "full"),  # Should be 0.80+
        ("Does Gupshup Console support SAML 2.0?", "answer"),  # Medium conf
        ("How do I set up webhooks?", "consult"),  # Currently 0.169, should attempt answer
        ("what is the refund policy", "idk"),  # Should stay IDK
    ]
    
    for query, expected_band in test_cases:
        result = kb_answer.kb_answer({"query": query})
        conf = result.get("langfuse", {}).get("metadata", {}).get("confidence", 0)
        band = _confidence_band(conf)
        
        assert band == expected_band, f"Query '{query}': expected {expected_band}, got {band} (conf: {conf})"
        
        # Check that we're not returning IDK for medium-confidence queries
        if expected_band != "idk":
            answer = (result.get("answer") or "").lower()
            assert "i don't know" not in answer or expected_band == "idk", \
                f"Query '{query}': expected {expected_band} but got IDK (conf: {conf})"

if __name__ == "__main__":
    test_confidence_bands()
    print("✓ All Phase 1 tests passed")
```

### Acceptance Criteria (Phase 1)

- [ ] Confidence thresholds correctly mapped to bands (0.80/0.60/0.40)
- [ ] Regression test accuracy maintained ≥93% (17/18 correct answers)
- [ ] False negative rate <5% (at most 1 query still returns IDK when it shouldn't)
- [ ] IDK rate drops to 35% (from 45.7% baseline)
- [ ] Confidence_tier field added to Langfuse metadata

---

## Phase 2: Consulting Follow-Ups (Week 2)

### Goal
Add optional follow-up prompts to medium-confidence (0.60-0.79) answers. Helps users verify context fit.

### Code Changes

#### Change 1: Add Follow-Up Templates
```python
# kb_answer.py line ~6700 (after answer composition functions)

def _follow_up_for_intent(intent: str, entities: List[Dict]) -> Optional[str]:
    """Generate context-checking follow-up for medium-confidence answers.
    
    Returns a follow-up question, or None if not applicable.
    """
    if not entities:
        return None
    
    # Setup intent: ask if prerequisites are met
    if intent == "setup":
        entity_name = entities[0].get("name", "this feature")
        return f"Quick check: Before you start, do you have the necessary permissions to {entity_name}?"
    
    # Definition intent: ask if they want implementation details
    if intent == "definition":
        return "Would you like to know how to implement this, or just the conceptual definition?"
    
    # Behavior intent: ask about their specific scenario
    if intent == "behavior":
        return "Does this behavior apply to your specific setup, or are you running into something different?"
    
    # Troubleshooting: ask about error symptoms
    if intent == "troubleshooting":
        return "Are you seeing any specific error messages? That might help me narrow down the root cause."
    
    return None
```

#### Change 2: Wrap Response with Follow-Up
```python
# kb_answer.py line ~7655 (after answer composition, before langfuse send)

# BEFORE:
answer = _compose_answer(query, intent, entities, evidence, explicit_module)

# AFTER:
answer = _compose_answer(query, intent, entities, evidence, explicit_module)
confidence = _reported_confidence(query, evidence)
band = _confidence_band(confidence)

# Add follow-up for medium-confidence answers
response_meta = {}
if band == "answer" and confidence >= CONFIDENCE_TIER_ANSWER:
    # Medium confidence: add follow-up prompt
    follow_up = _follow_up_for_intent(intent, entities)
    if follow_up:
        response_meta["follow_up"] = follow_up
        response_meta["confidence_tier"] = "answer_with_followup"
```

#### Change 3: Include Meta in Response
```python
# kb_answer.py line ~7780 (return statement)

# BEFORE:
return {
    "ok": True,
    "query": query,
    "answer": answer,
    "citations": [],
    "langfuse": langfuse,
}

# AFTER:
response = {
    "ok": True,
    "query": query,
    "answer": answer,
    "citations": [],
    "langfuse": langfuse,
}

# Add follow-up metadata if applicable
if "follow_up" in response_meta:
    response["follow_up"] = response_meta["follow_up"]

return response
```

### Testing (Phase 2)

```python
# local/scripts/test_phase2_followups.py

def test_followup_presence():
    # Medium-confidence queries should have follow-ups
    test_cases = [
        ("Does Gupshup Console support SAML 2.0?", True),   # Medium conf, should have followup
        ("How do I set up WhatsApp?", False),               # High conf, no followup needed
        ("what is the refund policy", False),               # IDK, no followup
    ]
    
    for query, should_have_followup in test_cases:
        result = kb_answer.kb_answer({"query": query})
        has_followup = "follow_up" in result
        
        assert has_followup == should_have_followup, \
            f"Query '{query}': expected followup={should_have_followup}, got {has_followup}"

def test_followup_relevance():
    # Follow-ups should match intent
    result = kb_answer.kb_answer({"query": "How do I configure webhooks?"})
    followup = result.get("follow_up", "").lower()
    
    if followup:
        # Setup intent should ask about prerequisites or validation
        assert any(word in followup for word in ["before", "prerequisite", "permission", "check"]), \
            f"Setup followup not asking for prerequisites: {followup}"

if __name__ == "__main__":
    test_followup_presence()
    test_followup_relevance()
    print("✓ All Phase 2 tests passed")
```

### Acceptance Criteria (Phase 2)

- [ ] Follow-ups present for 0.60-0.79 confidence answers
- [ ] Follow-ups absent for 0.80+ confidence answers
- [ ] Follow-up relevance to intent ≥90% (manual review of 10 queries)
- [ ] User follow-up propensity rises from 8% to 35%+ (from Langfuse tracking)
- [ ] User satisfaction on answered queries maintained ≥70%

---

## Phase 3: Consulting Questions (Week 3-4)

### Goal
Route 0.40-0.59 confidence queries to diagnostic questions instead of IDK. Requires improved routing accuracy ≥93%.

### Prerequisites
- [ ] Routing accuracy validated at ≥93% on 50 ambiguous queries
- [ ] Phase 2 user satisfaction ≥70%
- [ ] Module detection improvements deployed

### Code Changes

#### Change 1: Add Diagnostic Questions
```python
# kb_answer.py line ~6900 (new section for diagnostic questions)

def _diagnostic_questions(
    query: str, intent: str, entities: List[Dict], explicit_module: str
) -> Optional[str]:
    """Generate diagnostic questions for ambiguous/low-confidence queries.
    
    Returns a consulting-style question that helps narrow scope, or None if N/A.
    """
    
    # Webhook configuration: ask which platform
    if "webhook" in query.lower() and intent == "setup":
        return (
            "I can help with webhooks setup. Just to clarify: are you integrating with "
            "Salesforce, WhatsApp, RCS, or another platform? That changes the exact steps."
        )
    
    # Data storage: ask about access pattern
    if any(term in query.lower() for term in ["store", "storage", "data"]):
        if intent in ("page_lookup", "definition"):
            return (
                "Before I point you to the docs: are you looking for real-time access "
                "to the data, or batch processing? That determines which storage option makes sense."
            )
    
    # SSO/authentication: ask about user type
    if any(term in query.lower() for term in ["sso", "saml", "authentication", "login"]):
        return (
            "Quick context: are you setting this up for your team admins, or for "
            "all users? The configuration differs slightly."
        )
    
    # Scale/performance: ask about expected load
    if any(term in query.lower() for term in ["scale", "performance", "throughput", "rate limit"]):
        return (
            "To give you the right recommendation: what's your expected volume? "
            "(e.g., 100 messages/day, 1M/day, something else?)"
        )
    
    # Ambiguous module mentions: ask user to clarify
    if explicit_module == "General" and intent in ("setup", "page_lookup"):
        if entities:
            entity_name = entities[0].get("name", "feature")
            return f"Can you tell me a bit more about your use case for {entity_name}? That'll help me give you the right answer."
    
    return None
```

#### Change 2: Route Low-Confidence to Diagnostic Questions
```python
# kb_answer.py line ~7660 (modify response path for 0.40-0.59 band)

band = _confidence_band(confidence)

if band == "consult":
    # Low-confidence: try diagnostic question before IDK
    diagnostic_q = _diagnostic_questions(query, intent, entities, explicit_module)
    
    if diagnostic_q:
        # Return consulting question instead of IDK
        answer = diagnostic_q
        response_meta["response_type"] = "consulting_question"
        response_meta["original_query_confidence"] = confidence
    else:
        # No diagnostic question applicable; fall back to IDK
        answer = "I don't know based on the current docs."
        response_meta["response_type"] = "idk"
elif band == "idk":
    # Confidence < 0.40: straight IDK
    answer = "I don't know based on the current docs."
    response_meta["response_type"] = "idk"
```

#### Change 3: Track Response Type in Langfuse
```python
# kb_answer.py line ~7330 (langfuse metadata)

langfuse_data = {
    "confidence": confidence,
    "confidence_tier": _confidence_band(confidence),
    "response_type": response_meta.get("response_type", "answer"),  # NEW
    ...
}
```

### Testing (Phase 3)

```python
# local/scripts/test_phase3_diagnostic.py

def test_diagnostic_questions():
    # Low-confidence ambiguous queries should get questions, not IDK
    test_cases = [
        ("How do I configure webhooks?", True),  # Should get diagnostic Q
        ("What's the best way to store data?", True),  # Should get diagnostic Q
        ("How do I set up SSO?", True),  # Should get diagnostic Q
        ("How do I set up WhatsApp?", False),  # High confidence, no diagnostic Q
        ("asdkfj qweqwe zxcvzxcv", False),  # Nonsense query, should get IDK
    ]
    
    for query, should_have_diagnostic in test_cases:
        result = kb_answer.kb_answer({"query": query})
        response_type = result.get("langfuse", {}).get("metadata", {}).get("response_type")
        has_diagnostic = response_type == "consulting_question"
        
        assert has_diagnostic == should_have_diagnostic, \
            f"Query '{query}': expected diagnostic={should_have_diagnostic}, got {response_type}"

def test_diagnostic_relevance():
    # Diagnostic questions should be relevant to the query domain
    result = kb_answer.kb_answer({"query": "How do I configure webhooks?"})
    response_type = result.get("langfuse", {}).get("metadata", {}).get("response_type")
    
    if response_type == "consulting_question":
        answer = (result.get("answer") or "").lower()
        # Should ask about platform/integration type, not random questions
        assert any(word in answer for word in ["salesforce", "whatsapp", "rcs", "platform", "integrate"]), \
            f"Diagnostic question doesn't match webhook domain: {answer}"

def test_conversion_rate():
    # Track: what % of diagnostic Q answers get follow-up → actual answer?
    # This requires Langfuse tracing, but mock for now
    pass

if __name__ == "__main__":
    test_diagnostic_questions()
    test_diagnostic_relevance()
    print("✓ All Phase 3 tests passed")
```

### Acceptance Criteria (Phase 3)

- [ ] Diagnostic questions generated for ≥80% of 0.40-0.59 band queries
- [ ] Question relevance ≥90% (match query domain)
- [ ] Conversion rate ≥50% (users who see diagnostic Q → follow-up with context → real answer)
- [ ] IDK rate drops to 15% (from 25% after Phase 2)
- [ ] User satisfaction on consulting Q→A path ≥70%
- [ ] No module routing degradation (accuracy maintained ≥93%)

---

## Phase 4: Context-Gated Confidence (Week 5+)

### Goal
Adjust confidence reporting based on user context (tech level, use case, scale). Improves calibration.

### Code Changes

#### Change 1: Add User Context Tracking
```python
# kb_answer.py line ~7420 (in kb_answer function, after query extraction)

def _infer_user_context(params: dict, previous_turns: Optional[List[Dict]] = None) -> dict:
    """Infer user context from parameters and conversation history.
    
    Returns dict with keys: tech_level, use_case, scale, etc.
    """
    context = {}
    
    # From explicit params (if user provides via API)
    if "tech_level" in params:
        context["tech_level"] = params["tech_level"]  # "beginner", "intermediate", "expert"
    if "use_case" in params:
        context["use_case"] = params["use_case"]
    if "scale" in params:
        context["scale"] = params["scale"]
    
    # Infer from question type (if empty context)
    if not context.get("tech_level") and previous_turns:
        # Count API jargon in previous queries
        api_terms = sum(
            1 for turn in previous_turns
            if any(term in turn.get("query", "").lower() 
                   for term in ["api", "webhook", "endpoint", "payload", "authentication"])
        )
        if api_terms >= 2:
            context["tech_level"] = "expert"
    
    return context
```

#### Change 2: Add Context-Aware Confidence
```python
# kb_answer.py line ~5850 (new function after _reported_confidence)

def _consulting_confidence(
    query: str,
    evidence: List[Dict],
    user_context: Optional[dict] = None,
    entities: List[Dict] = None,
) -> float:
    """Confidence that this answer will solve user's problem, given their context.
    
    Blends retrieval confidence with context fit.
    """
    retrieval_confidence = _reported_confidence(query, evidence)
    
    if not evidence:
        return 0.0
    
    # Start with baseline context confidence
    if not user_context:
        context_confidence = 0.6  # Unknown context = modest confidence
    else:
        factors = []
        
        # Does evidence cover user's use case?
        if "use_case" in user_context:
            use_case_mentions = sum(
                1 for c in evidence
                if user_context["use_case"].lower() in str(c.get("text", "")).lower()
            )
            use_case_fit = min(1.0, use_case_mentions / max(1, len(evidence)))
            factors.append(use_case_fit)
        
        # Is the user's scale in documented bounds?
        if "scale" in user_context:
            scale_mentions = sum(
                1 for c in evidence
                if user_context["scale"].lower() in str(c.get("text", "")).lower()
            )
            scale_fit = min(1.0, 0.5 + (scale_mentions / max(1, len(evidence) * 2)))
            factors.append(scale_fit)
        
        context_confidence = sum(factors) / len(factors) if factors else 0.7
    
    # Blend: retrieval dominates, but context is meaningful
    final_confidence = 0.6 * retrieval_confidence + 0.4 * context_confidence
    return min(1.0, max(0.0, final_confidence))
```

#### Change 3: Use Context-Aware Confidence in Response
```python
# kb_answer.py line ~7660 (when computing confidence for response)

# BEFORE:
confidence = _reported_confidence(query, evidence)

# AFTER:
user_context = _infer_user_context(params, previous_turns=None)  # TODO: add conversation history
confidence = _consulting_confidence(query, evidence, user_context, entities)
```

### Testing (Phase 4)

```python
# local/scripts/test_phase4_context.py

def test_context_aware_confidence():
    # Same query, different context → different confidence
    query = "What's the best way to store customer data?"
    
    # Scenario 1: Real-time use case (cache + DB) → should be confident
    result1 = kb_answer.kb_answer({
        "query": query,
        "use_case": "real-time lookups",
        "scale": "50K records"
    })
    conf1 = result1.get("langfuse", {}).get("metadata", {}).get("confidence", 0)
    
    # Scenario 2: Batch use case (data lake) → should be confident
    result2 = kb_answer.kb_answer({
        "query": query,
        "use_case": "batch analytics",
        "scale": "100M records"
    })
    conf2 = result2.get("langfuse", {}).get("metadata", {}).get("confidence", 0)
    
    # Scenario 3: No context → should be less confident
    result3 = kb_answer.kb_answer({
        "query": query,
    })
    conf3 = result3.get("langfuse", {}).get("metadata", {}).get("confidence", 0)
    
    # Confidence should be higher when context matches evidence
    assert conf1 > 0.65, f"Real-time use case confidence too low: {conf1}"
    assert conf2 > 0.65, f"Batch use case confidence too low: {conf2}"
    assert conf3 < 0.75, f"No-context confidence should be lower: {conf3}"

def test_calibration_improvement():
    # Confidence-satisfaction correlation should improve
    # This requires Langfuse data; mock Pearson correlation calculation
    
    test_queries = [
        ("How do I set up WhatsApp?", True, 0.85),
        ("How do I set up webhooks?", True, 0.73),
        ("what is the refund policy", False, 0.24),
    ]
    
    for query, user_satisfied, expected_conf in test_queries:
        result = kb_answer.kb_answer({"query": query})
        conf = result.get("langfuse", {}).get("metadata", {}).get("confidence", 0)
        
        # After Phase 4, confidence should better predict satisfaction
        if user_satisfied:
            assert conf >= 0.65, f"Query '{query}': unsatisfied but high confidence"
        else:
            assert conf < 0.65, f"Query '{query}': satisfied but low confidence"

if __name__ == "__main__":
    test_context_aware_confidence()
    test_calibration_improvement()
    print("✓ All Phase 4 tests passed")
```

### Acceptance Criteria (Phase 4)

- [ ] User context captured in ≥60% of conversations
- [ ] Confidence-satisfaction correlation r ≥ 0.75 (improved from 0.72)
- [ ] Context-aware confidence calibration error ±0.04 (improved from ±0.18)
- [ ] Accuracy maintained ≥70% on all modules
- [ ] IDK rate stabilized at ≤12%

---

## Rollback Procedure

### Quick Rollback (if any metric drops >5%)

```bash
# Revert to previous stable version
git revert <commit-hash>

# Identify which phase introduced regression
git log --oneline | head -10

# Rollback in stages:
# - If Phase 4 broke: revert Phase 4, stay in Phase 3
# - If Phase 3 broke: revert Phase 3, stay in Phase 2
# - If Phase 2 broke: revert Phase 2, stay in Phase 1
# - If Phase 1 broke: revert to problem-solution baseline
```

### Investigation Checklist

- [ ] Check confidence-satisfaction correlation (should be ≥0.70)
- [ ] Check accuracy by module (should be ≥70% all modules)
- [ ] Check IDK rate (should match phase target)
- [ ] Check module routing accuracy (should be ≥90%)
- [ ] Review Langfuse traces for failed queries

---

## Monitoring & Alerting

### Weekly Metrics Report

```python
# local/scripts/monitor_consulting_tone.py

def weekly_report():
    """Generate weekly metrics for consulting-tone rollout."""
    
    metrics = {
        "accuracy": {
            "regression_set": (17, 18, "94.4%"),  # (correct, total, %)
            "by_module": {
                "RCS": "71.4%",
                "Agent Assist": "69.8%",
                "WhatsApp": "70.1%",
                "BizAI": "65.2%",
                "General": "57.9%",
            },
        },
        "engagement": {
            "idk_rate": "35.0%",  # Phase 1 target
            "follow_up_propensity": "35%",
            "avg_conversation_depth": 1.8,
        },
        "calibration": {
            "confidence_satisfaction_corr": 0.72,
            "calibration_error": 0.18,
        },
        "rollback_triggers": {
            "accuracy_below_70": False,
            "idk_rate_above_target": False,
            "satisfaction_below_70": False,
            "module_routing_below_90": False,
        },
    }
    
    return metrics
```

### Alert Thresholds

| Metric | Alert Threshold | Action |
|--------|---|---|
| Accuracy <70% on any module | YES | Page on-call, investigate immediately |
| Confidence-satisfaction correlation <0.65 | YES | Pause rollout, review Phase 4 |
| IDK rate misses phase target by >10% | NO | Monitor, adjust diagnostics |
| Module routing <90% | YES | Revert to Phase 1, fix routing |
| User satisfaction drops >5% | YES | Pause phase, root cause analysis |

---

## Summary: Implementation Checklist

### Phase 1 (Week 1)
- [ ] Add confidence band constants
- [ ] Implement `_confidence_band()` function
- [ ] Modify evidence selection to use bands
- [ ] Add `confidence_tier` to Langfuse metadata
- [ ] Run test suite, verify ≥93% accuracy on regression set
- [ ] Deploy to staging
- [ ] Monitor IDK rate (target: 45.7% → 35%)

### Phase 2 (Week 2)
- [ ] Implement `_follow_up_for_intent()` function
- [ ] Add follow-up wrapping in response
- [ ] Include follow-up metadata in response
- [ ] Run test suite, verify follow-up relevance ≥90%
- [ ] A/B test: 50% Segment B gets follow-ups
- [ ] Monitor user satisfaction (target: 55% → 62%)

### Phase 3 (Week 3-4)
- [ ] Prerequisite: Validate routing accuracy ≥93%
- [ ] Implement `_diagnostic_questions()` function
- [ ] Route 0.40-0.59 band to diagnostic questions
- [ ] Add `response_type` tracking in Langfuse
- [ ] Run test suite, verify question relevance ≥90%
- [ ] Monitor conversion rate (diagnostic Q → follow-up → answer)
- [ ] Monitor user satisfaction (target: 62% → 70%)

### Phase 4 (Week 5+)
- [ ] Prerequisite: All Phase 1-3 metrics met
- [ ] Implement `_infer_user_context()` function
- [ ] Implement `_consulting_confidence()` function
- [ ] Integrate context into confidence calculation
- [ ] Measure confidence-satisfaction correlation (target: r ≥ 0.75)
- [ ] Monitor calibration error (target: ±0.04)

---

**Document Updated:** 2026-08-11  
**Status:** Ready for implementation

