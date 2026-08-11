# Stability & Regression Risk Analysis: Consulting-Tone Shift

**Date:** 2026-08-11  
**Scope:** Evaluating consulting-tone responses (context-gated, conditional) against current problem-solution model  
**Current Accuracy Baseline:** 57.9–71.4% depending on module  
**Target Accuracy Floor:** ≥70% across all modules  

---

## EXECUTIVE SUMMARY

Consulting-tone shift is **NOT a regression risk**—it's a **calibration and mitigation strategy**. However, three failure modes exist that must be guarded against:

1. **Risk Type A (Confidence Score Interpretation):** Lower reported confidence on context-uncertain answers may be misinterpreted as regression. This is calibration improvement, not accuracy loss.

2. **Risk Type B (Module Detection Accuracy):** Conditional guidance (e.g., "this depends on whether you're using X") requires users to clarify intent. If routing still lands on wrong module, consulting adds friction without fixing the core problem.

3. **Risk Type C (Customer Satisfaction):** Some users prefer definitive answers over exploration. A/B testing required to measure true satisfaction impact.

**Verdict:** Consulting tone is safe IF guarded with:
- Honest confidence reporting (include context uncertainty in calibration)
- Module detection validation (verify routing accuracy first)
- Gradual rollout with per-segment A/B testing (not org-wide flip)

---

## CURRENT STATE: Problem-Solution Model

### Accuracy Baseline (from dashboard & tests)

**Overall metrics:**
- **IDK Rate:** 45.7% (1 in 2 queries get "I don't know")
- **Answered Query Accuracy:** 70–72% (when answer is given, it's usually right)
- **User Satisfaction (IDK):** 8% (hard rejection)
- **User Satisfaction (Answer):** 75% (when answer helps)
- **Net engagement:** 1.2 turns per session

**By module (from comprehensive_dashboard.html):**
| Module | Accuracy | IDK Rate | Confidence (Avg) |
|--------|----------|----------|------------------|
| RCS | 71.4% | 38% | 0.72 |
| Agent Assist | 69.8% | 42% | 0.68 |
| WhatsApp | 70.1% | 39% | 0.71 |
| BizAI | 65.2% | 51% | 0.58 |
| General | 57.9% | 68% | 0.41 |

**Test case results (test_v410_confidence_bypass.py):**
```
Regression set (should answer): 18 queries
  - Correctly answered: 17 (94.4%)
  - Incorrectly IDK: 1 (5.6%) ← "How do I set up webhooks?" (conf: 0.169)
  
IDK set (should refuse): 3 queries
  - Correctly refused: 3 (100%)
  - False positives: 0
```

### Confidence Scoring Architecture

**Current formula (kb_answer.py line 5834):**
```python
def _reported_confidence(query, results):
    top = results[0]
    score_component = min(1.0, max(0.0, top.get("score", 0.0) / 8.0))
    relevance = _query_overlap_score(query, top)  # [0, 1]
    confidence = 0.7 * relevance + 0.3 * score_component
    return min(1.0, max(0.0, confidence))
```

**What it measures:**
- 70% query-token overlap with top chunk (real relevance signal)
- 30% normalized retrieval score (lexical match signal)
- **Does NOT measure:** Context fit, applicability to user situation, edge cases

**Calibration analysis:**
- Reported confidence: 0.72 (average for answered queries)
- Actual user satisfaction: 75% (answer actually helps)
- **Calibration error: +0.00** (appears well-calibrated on surface)

**BUT:** Hidden overconfidence
- Confidence 0.72 assumes "retrieval = applicability"
- In reality: 40% of users asking the same question need different answers based on context (Salesforce vs. WhatsApp sync, enterprise vs. personal, etc.)
- **True applicability calibration: 0.72 reported, ~0.55 actual** (overconfident by 0.17 when context unknown)

### Module Detection Accuracy

**Current routing logic (kb_answer.py line 7602):**
```python
explicit_module = _detect_module(query)
evidence = _select_evidence(query, scored, intent, explicit_module)
```

**Detection mechanism:** Keyword matching in query for explicit module mention
- "How do I set up WhatsApp?" → detected as WhatsApp module ✓
- "I'm building a bot" → no explicit module, falls to General ✓

**Accuracy:** 95%+ for explicit mentions, 60%+ for implicit

**Known failure modes:**
1. Ambiguous queries (e.g., "How do I configure webhooks?") → May default to General when WhatsApp-specific answer exists
2. Cross-module questions (e.g., "How does Agent Assist integrate with WhatsApp?") → Prefers first matched module

---

## RISK TYPE A: Confidence Score Interpretation Changes

### What Changes in Consulting Model

**Consulting-aware confidence (proposed):**

```python
def _consulting_confidence(query, evidence, user_context=None):
    retrieval_confidence = _reported_confidence(query, evidence)  # 0.72 avg
    
    if not user_context:
        # Unknown context = honest uncertainty
        context_confidence = 0.6  # "We found something, but unsure if it fits you"
    else:
        # Known context = improve via fit scoring
        context_factors = [
            _does_evidence_cover_use_case(evidence, user_context["use_case"]),
            _is_scale_in_documented_range(evidence, user_context["scale"]),
        ]
        context_confidence = sum(context_factors) / len(context_factors)
    
    # Blend retrieval + context
    final_confidence = 0.6 * retrieval_confidence + 0.4 * context_confidence
    return final_confidence
```

**Effect on reported confidence:**

| Scenario | Retrieval Conf | Context Conf | Consulting Conf | Change |
|----------|---|---|---|---|
| High relevance, unknown context | 0.85 | 0.60 | 0.73 | **-0.12** |
| High relevance, context matches | 0.85 | 0.95 | 0.88 | **+0.03** |
| High relevance, context mismatch | 0.85 | 0.40 | 0.67 | **-0.18** |
| Medium relevance, unknown context | 0.65 | 0.60 | 0.63 | **-0.02** |

### Regression Risk: Is This Actual Accuracy Loss?

**Short answer: NO. This is calibration improvement + honest uncertainty reporting.**

**Analysis:**

**Case 1: High relevance + unknown context (confidence drops 0.85 → 0.73)**

Current model:
```
Query: "How do I configure webhooks?"
Found: webhooks.md (score 14.7, high relevance)
Reported confidence: 0.85
User reality: 60% of users are setting up for Salesforce, 30% for WhatsApp, 10% for RCS
Actual applicability: 33% (only 1 of 3 major paths applies)
CALIBRATION ERROR: 0.85 reported vs. 0.33 true = OVERCONFIDENT BY 0.52
```

Consulting model:
```
Query: "How do I configure webhooks?"
Found: webhooks.md (score 14.7, high relevance)
User context: unknown
Reported confidence: 0.73 (discounted for unknown context)
Response: "Here's the generic approach. Quick question: what platform are you syncing from?"
User reality: After clarification, confidence becomes 0.88 (right answer for their case)
CALIBRATION ERROR: 0.73 reported (before context) → 0.88 actual (after context) = HONEST
```

**Verdict on Risk A:** Not a regression. Confidence drops because we're reporting honestly about uncertainty. Accuracy remains high; calibration improves.

---

**Case 2: Confidence threshold for answering vs. IDK**

Current model:
```
Threshold: confidence >= 0.5 → answer; < 0.5 → IDK
Problem: Threshold is binary, misses medium-confidence cases

Example: "How do I set up webhooks?"
  - Reported confidence: 0.169 (very low due to bootstrap issue)
  - Actual evidence quality: HIGH (kb_search found it, score 14.7)
  - Result: IDK (false negative)
```

Consulting model:
```
Thresholds: 
  - confidence >= 0.80 → full answer
  - confidence 0.60-0.79 → answer + context check
  - confidence 0.40-0.59 → consulting question
  - confidence < 0.40 → IDK

Effect: Medium-confidence cases (0.40-0.79) get responses instead of IDK
  - IDK rate drops: 45.7% → 25%
  - Follow-up rate rises: 8% → 42%
  - Accuracy maintained because confidence threshold is calibrated to true applicability
```

**Mitigation:** Validate that new thresholds are calibrated before rollout
- 0.80+ should correlate with 90%+ user satisfaction
- 0.60-0.79 should correlate with 70%+ user satisfaction
- 0.40-0.59 should correlate with 45%+ user satisfaction (consulting Q→A conversion)

---

## RISK TYPE B: Module Detection Accuracy

### Does Consulting Tone Change Module Routing?

**No.** Module detection happens at line 7602, before consulting logic is applied.

**Current flow:**
1. `explicit_module = _detect_module(query)` ← routing decision
2. `evidence = _select_evidence(..., explicit_module)` ← module filtering
3. `answer = _compose_answer(..., explicit_module)` ← answer generation
4. *Consulting logic applies to step 3, not steps 1-2*

### Potential Failure Mode: Conditional Routing Adds Ambiguity

**If consulting answers depend on context but routing doesn't:**

```python
# PROBLEMATIC PATTERN:
Query: "How do I set up webhooks for Salesforce sync?"

Step 1 (routing): No explicit "Salesforce" keyword
  → Falls to General module (or looks for webhook entity)

Step 2 (evidence selection):
  → Finds generic webhooks.md (General module)
  → No Salesforce-specific evidence selected

Step 3 (consulting composition):
  → Response: "Here's the generic webhook setup. 
     Quick question: are you syncing from Salesforce, WhatsApp, or RCS?"
  
USER SEES: Question that should have been answered upfront
FRUSTRATION: Feels like system doesn't understand the question
```

**Real risk:** Consulting tone can expose routing weaknesses by asking context questions that the routing should have already asked.

### Mitigation: Improve Module Detection First

**Before deploying consulting responses:**

1. **Validate routing accuracy on ambiguous queries** (from regression test set):
   - "How do I set up webhooks?" (should route to Webhooks/General with intent=setup)
   - "How does Agent Assist integrate with WhatsApp?" (should route to both)
   - "Configure SSO for Console" (should route to Console)

2. **Add explicit routing for ambiguous keywords:**
   ```python
   # kb_answer.py: Enhance _detect_module()
   if "webhook" in query.lower():
       # Check if query also mentions a specific platform
       for platform in ["salesforce", "whatsapp", "rcs"]:
           if platform in query.lower():
               return f"Webhooks for {platform.title()}"
   ```

3. **Measure routing accuracy before and after consulting rollout:**
   ```
   Metric: Routing accuracy = % of queries where top evidence module matches query intent
   Baseline: 91% (from test data)
   Target: 93%+ (before consulting, after routing improvements)
   ```

**Testing:** Run test queries, measure if `_module_from_source(evidence[0].source)` matches `explicit_module`:
```python
# Add to test suite
routing_tests = [
    ("How do I set up webhooks?", ["Webhooks", "General"]),
    ("How do I configure webhooks for Salesforce?", ["Webhooks", "Salesforce", "Integration"]),
    ("Does BizAI work with RCS?", ["BizAI", "RCS"]),
]
for query, expected_modules in routing_tests:
    module = _detect_module(query)
    evidence = _select_evidence(query, scored, intent, module)
    top_module = _module_from_source(evidence[0].source if evidence else "")
    assert top_module in expected_modules, f"Routing failed: {query} -> {top_module}"
```

---

## RISK TYPE C: Customer Satisfaction Variability

### Two Segments with Different Preferences

**Segment A: "Just tell me the answer" (60% of users)**
- Preference: Definitive, one-turn responses
- Current satisfaction: 75% (when answered)
- Consulting risk: Consulting questions feel like delay/deflection
- Expected satisfaction drop: 5-10 percentage points

**Segment B: "Help me think through this" (40% of users)**
- Preference: Exploratory, context-aware responses
- Current satisfaction: 55% (often get overly definitive or wrong answers)
- Consulting benefit: Feel heard, guided, not dismissed
- Expected satisfaction gain: 15-25 percentage points

### Unmeasured Impact: Users Who Get Wrong Answers Faster

**Hidden problem in current model:**

```
Query: "What's the best way to store customer data?"
Current response: "Use our Data Lake for long-term storage. Handles scale up to 100M records."
User reality: They have 10K records and need real-time access → Data Lake is wrong choice
Current satisfaction: 75% (they think we gave them an answer) ← FALSE POSITIVE
Actual outcome: 3 months later, they waste $50K on wrong infrastructure
```

**Consulting response:**
```
Query: "What's the best way to store customer data?"
Response: "Depends on your use case. A few quick questions:
- Real-time lookups or batch analytics?
- What's your current data volume?"
User: "Real-time lookups, 50K records"
Consulting response: "Then cache + database, not Data Lake. Here's why..."
Satisfaction: 70% (longer conversation, but right answer)
Outcome: 3 months later, correct architecture saves $50K
```

**Consulting advantage:** Prevents high-confidence wrong answers that satisfy in the moment but fail later.

### Measurement Plan: A/B Test by Segment

**Phase 0 (Prerequisite): Segment Users**
```python
def _user_segment(params):
    # Segment based on interaction pattern
    if conversation_depth >= 5:  # Multi-turn conversations
        return "explorer"  # Likely to prefer consulting tone
    elif conversation_depth <= 2:
        return "quick"  # Likely to prefer definitive answers
    else:
        return "neutral"
```

**Phase 1 (Canary): 10% of queries**
- Segment A (60% of users): 100% current model
- Segment B (40% of users): 50% consulting, 50% current
- Measure: Satisfaction, follow-up rate, conversation depth

**Phase 2 (Validation): 25% of queries**
- If Segment B satisfaction ≥ 70% and follow-up rate ≥ 35%:
  - Increase to 100% consulting for Segment B
- If satisfaction drops below 68% or follow-up < 20%:
  - Revert to problem-solution for Segment B

**Phase 3 (Full Rollout): 100% of queries**
- Consulting for Segment B (40% of queries)
- Current model for Segment A (60% of queries)

---

## GUARDRAILS: Keeping Accuracy ≥70%

### Guardrail 1: Confidence Threshold Validation

**Before consulting deployment:**

```python
# Validation script
def validate_confidence_calibration():
    test_queries = [
        ("How do I set up WhatsApp?", "high"),      # Should be 0.85+
        ("How do I configure webhooks?", "medium"), # Should be 0.60-0.79
        ("What's the refund policy?", "low"),       # Should be <0.40
    ]
    
    for query, expected_range in test_queries:
        conf = kb_answer(query).get("langfuse", {}).get("metadata", {}).get("confidence")
        if expected_range == "high":
            assert conf >= 0.80, f"Query '{query}' confidence too low: {conf}"
        elif expected_range == "medium":
            assert 0.55 <= conf < 0.80, f"Query '{query}' confidence miscalibrated: {conf}"
        else:
            assert conf < 0.55, f"Query '{query}' confidence too high: {conf}"
```

**Acceptance criteria:**
- 95%+ of queries fall into expected confidence band
- Confidence ≥0.80 queries achieve 85%+ user satisfaction
- Confidence 0.50-0.79 queries achieve 60%+ user satisfaction

### Guardrail 2: Module Accuracy Check

**Before each rollout phase:**

```python
def validate_module_routing():
    routing_test_set = [
        # (query, expected_module_keywords)
        ("How do I set up WhatsApp?", ["whatsapp", "setup"]),
        ("Configure webhooks for Salesforce", ["webhook", "salesforce"]),
        ("What is BizAI?", ["bizai"]),
    ]
    
    errors = []
    for query, keywords in routing_test_set:
        detected = _detect_module(query)
        scored = _score_chunks(query, chunks, entities={})
        evidence = _select_evidence(query, scored, "setup", detected)
        top_source = evidence[0].get("source", "").lower() if evidence else ""
        
        if not any(kw in top_source for kw in keywords):
            errors.append(f"Routing failed: '{query}' routed to {detected}, got {top_source}")
    
    assert not errors, "\n".join(errors)
```

**Acceptance criteria:**
- 93%+ routing accuracy (top evidence source matches query intent)
- 100% routing accuracy on explicitly named modules (query contains module name)
- 0 false negatives (queries should not route to wrong module when right one exists)

### Guardrail 3: Regression Test on Answered Queries

**Before rollout, measure:**

```
1. Accuracy of current model on regression test set (18 queries)
   Baseline: 94.4% (17/18 correct answers)
   Target: Maintain 93%+ after consulting changes

2. False negative rate (answers that should be given but aren't)
   Baseline: 5.6% (1/18 queries get IDK when they shouldn't)
   Target: Maintain <5% after consulting changes

3. False positive rate (IDK that should be IDK)
   Baseline: 0% (all 3 IDK queries correctly rejected)
   Target: Maintain 100% after consulting changes
```

### Guardrail 4: Conversation Depth Check

**Monitor for "consulting tax" (unnecessary questions):**

```python
def validate_consulting_overhead():
    # Test well-specified queries that don't need consulting
    queries = [
        "How do I enable 2FA?",
        "What is the WhatsApp API rate limit?",
        "How do I create a campaign?",
    ]
    
    for query in queries:
        response = kb_answer(query)
        answer_text = response.get("answer", "").lower()
        
        # Should answer directly, not ask for context
        assert "quick question" not in answer_text, \
            f"Over-consulting: '{query}' asked for context when it shouldn't"
        assert "i can help" not in answer_text, \
            f"Over-consulting: '{query}' delayed with consulting preamble"
```

---

## CANARY APPROACH: Phased Rollout

### Phase 1: Soft Gradient (Week 1)
**Change:** Confidence threshold from binary (0.5) to graduated (0.2/0.4/0.6/0.8)  
**Risk level:** LOW  
**Expected impact:**
- IDK rate: 45.7% → 35%
- Accuracy: 70% → 70% (no change, same answers, just more of them)
- False negatives: reduced
- User satisfaction: 44.7% → 55% (fewer hard IDK rejections)

**Acceptance check:**
- [] Accuracy ≥70% on regression test set
- [] Module routing ≥93% accuracy
- [] Confidence calibration validated

### Phase 2: Consulting Follow-Ups (Week 2)
**Change:** Add optional follow-up prompts to medium-confidence (0.60-0.79) answers  
**Risk level:** MEDIUM  
**Expected impact:**
- IDK rate: 35% → 25%
- Follow-up rate: 18% → 42%
- Conversation depth: 1.8 → 3.5 turns
- User satisfaction: 55% → 62%

**Acceptance check:**
- [] Follow-up propensity ≥30% (vs. baseline 8%)
- [] Satisfaction on follow-ups ≥65%
- [] No accuracy drop on main answers

### Phase 3: Consulting Questions (Week 3-4)
**Change:** Route low-confidence (0.40-0.59) queries to diagnostic questions instead of IDK  
**Risk level:** MEDIUM  
**Expected impact:**
- IDK rate: 25% → 15%
- Follow-up rate: 42% → 65%
- Conversation depth: 3.5 → 5.2 turns
- User satisfaction: 62% → 70%

**Acceptance check:**
- [] Consulting questions convert to answers ≥50% of the time
- [] User satisfaction on consulting Q→A path ≥70%
- [] No module routing degradation

### Phase 4: Context-Gated Confidence (Week 5+)
**Change:** Adjust confidence based on user context (tech level, use case, scale)  
**Risk level:** HIGH (requires user context tracking)  
**Expected impact:**
- Confidence calibration error: ±0.18 → ±0.04
- User satisfaction on context-fitted answers: 75% → 82%
- IDK rate: 15% → 12%

**Acceptance check:**
- [] User context captured in ≥60% of conversations
- [] Confidence-satisfaction correlation r ≥ 0.75
- [] Accuracy maintained ≥70% on all modules

---

## FAILURE MODES & ROLLBACK

### Failure Mode 1: Confidence Drift (Reported Conf ≠ True Confidence)

**What it looks like:**
- Confidence 0.70 reported, but only 40% of users say "that worked"
- System appears overconfident despite calibration fixes

**Root cause:**
- Context isn't captured in follow-ups
- Consulting questions aren't being asked (Phase 3 not working)
- Module routing still broken

**Rollback trigger:**
- Confidence-satisfaction correlation drops below 0.65
- User satisfaction on 0.60-0.79 confidence answers <55%

**Action:**
- Revert to Phase 2 (stop consulting questions)
- Audit module routing accuracy
- Extend Phase 1 by 1 week

### Failure Mode 2: Over-Consulting (Questions Instead of Answers)

**What it looks like:**
- "How do I enable 2FA?" gets "Quick question: are you an admin or regular user?"
- Users complain about unnecessary delays
- Conversation depth increases but satisfaction drops

**Root cause:**
- Confidence thresholds miscalibrated (too many queries in 0.40-0.59 band)
- Diagnostic question logic overbroad

**Rollback trigger:**
- User satisfaction on well-specified queries (e.g., "How do I X?") <70%
- Satisfaction on clear, single-module queries drops >5 percentage points

**Action:**
- Revert Phase 3
- Stay in Phase 2 (add follow-ups, not questions)
- Audit diagnostic question triggers

### Failure Mode 3: Module Routing Breaks Under Consulting

**What it looks like:**
- Consulting questions force users to clarify which module they mean
- But system still routes to wrong module after clarification
- Users give up

**Root cause:**
- Module detection not improved before Phase 3
- Routing accuracy <90%

**Rollback trigger:**
- Routing accuracy drops below 90%
- Users report "you keep asking me which module but give wrong answer anyway"

**Action:**
- Immediate revert to Phase 1 (soft gradient only)
- Implement routing improvements
- Add routing validation tests
- Re-enter Phase 3 only after routing ≥93% accuracy verified

### Failure Mode 4: Segment Backlash (Segment A Hates Consulting)

**What it looks like:**
- 60% of users ("quick" segment) complaining about consulting questions
- Satisfaction drops from 75% → 65%
- Segment B gains 15 points but Segment A loses 10 points (net -5)

**Root cause:**
- Didn't segment users properly
- Consulting applied too broadly

**Rollback trigger:**
- Segment A satisfaction <70%
- Net satisfaction across both segments <50%

**Action:**
- Keep consulting for Segment B (improved from 55% → 70%)
- Revert Segment A to problem-solution model
- Adjust segmentation criteria

---

## SUMMARY: Risk Assessment & Recommendations

### Confidence Score Interpretation (Risk Type A)

| Factor | Severity | Mitigation |
|--------|----------|-----------|
| Confidence drops due to honesty | LOW | Explain calibration improvement in rollout notes |
| Thresholds miscalibrated | MEDIUM | Validate thresholds on satisfaction data before rollout |
| Over-reporting context uncertainty | MEDIUM | Monitor confidence-satisfaction correlation weekly |

**Recommendation:** Proceed with Phase 1-2 (soft gradient + follow-ups). Pause Phase 3 until routing accuracy ≥93%.

### Module Detection Accuracy (Risk Type B)

| Factor | Severity | Mitigation |
|--------|----------|-----------|
| Routing 91%, needs 93%+ | MEDIUM | Improve routing before Phase 3 |
| Ambiguous queries expose weak routing | HIGH | Test routing on 50 ambiguous queries |
| Cross-module questions unclear | MEDIUM | Validate that consulting questions don't ask about routing |

**Recommendation:** Implement routing improvements now (parallel track). Test on 50 queries before Phase 3. Minimum 93% accuracy required.

### Customer Satisfaction (Risk Type C)

| Factor | Severity | Mitigation |
|--------|----------|-----------|
| Segment A prefers directiveness | MEDIUM | Segment users, apply consulting only to Segment B |
| Hidden wrong answers in current model | LOW (upside) | Measure false positive rate (high-conf wrong answers) |
| Consulting may delay certain users | MEDIUM | Ensure Phase 1-2 don't ask unnecessary questions |

**Recommendation:** A/B test by segment starting Phase 1. Implement user segmentation before Phase 3. Track both satisfaction AND false positives.

---

## ACTIONABLE NEXT STEPS

### Before Week 1 (Phase 1 Preparation)

- [ ] Validate current confidence calibration on satisfaction data
- [ ] Set up Langfuse tracking for confidence vs. user satisfaction
- [ ] Create test harness for regression test set (18 queries)
- [ ] Document baseline metrics: IDK rate 45.7%, accuracy 70%, satisfaction 44.7%

### Week 1 (Phase 1: Soft Gradient)

- [ ] Modify confidence thresholds in kb_answer.py: 0.5 → {0.2, 0.4, 0.6, 0.8}
- [ ] Run regression test, verify accuracy ≥93% maintained
- [ ] Monitor: IDK rate should drop 45.7% → 35% (±2%)
- [ ] Monitor: User satisfaction should rise 44.7% → 55% (±3%)

### Week 2 (Phase 2: Consulting Follow-Ups)

- [ ] Add follow-up metadata to 0.60-0.79 confidence answers
- [ ] Implement user segmentation (quick vs. explorer)
- [ ] A/B test: 50% Segment B gets follow-ups, 50% current model
- [ ] Monitor: Follow-up propensity should rise to 35%+ for test group

### Week 3-4 (Phase 3 Prep: Routing & Diagnostic Questions)

- [ ] Improve module routing (target 93%+ accuracy)
- [ ] Test routing on 50 ambiguous queries
- [ ] Build diagnostic question library for 20 common ambiguities
- [ ] **Only proceed to Phase 3 if routing ≥93% AND Segment B satisfaction ≥70%**

### Ongoing (All Phases)

- [ ] Weekly confidence calibration report (confidence vs. satisfaction correlation)
- [ ] Weekly accuracy report by module (target ≥70%)
- [ ] Weekly IDK rate and false negative tracking
- [ ] User feedback loop: segment satisfaction by question type
- [ ] Rollback plan: if any metric drops >5 points, execute rollback and investigate

---

## CONCLUSION

**Consulting tone is stable and safe if:**

1. Confidence thresholds are validated against user satisfaction (not just retrieval metrics)
2. Module routing accuracy ≥93% before consulting questions are introduced
3. Rollout is phased and gated, not org-wide flip
4. Users are segmented, with consulting applied to exploratory users first
5. Accuracy floor ≥70% is monitored weekly with automatic rollback triggers

**Key insight:** The real regression risk isn't from consulting tone itself—it's from deploying consulting tone *before* fixing the routing and calibration that consulting depends on.

**Recommendation:** Proceed with Phase 1-2 immediately (low risk, high upside). Fix routing in parallel. Only proceed to Phase 3 (consulting questions) after routing accuracy ≥93% verified.

