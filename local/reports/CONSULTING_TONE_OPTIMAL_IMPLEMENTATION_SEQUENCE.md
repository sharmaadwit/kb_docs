# Consulting-Tone Implementation: Optimal Phased Approach
## Strategic Design for Minimum Viable Change → Maximum Impact Measurement

**Date:** 2026-08-11  
**Document:** Implementation strategy addressing Phase 0 (MVP test), decision tree logic, and risk-gated phase progression  
**Audience:** Project stakeholders, engineers, product team  
**Status:** Strategy Framework (Ready for execution)

---

## EXECUTIVE SUMMARY

This document outlines a **risk-stratified phased approach** to consulting-tone implementation that prioritizes:

1. **Phase 0 (Week 1): RCS-only MVP** — Implement consulting-tone answer generation on RCS module only (safest, lowest-risk test)
2. **Decision Gate 1 (End of Week 1)** — Measure engagement lift + accuracy hold; decide if P1 proceeds
3. **Phase 1 (Week 2): Soft Gradient** — Roll out graduated confidence tiers if P0 shows +20% engagement lift
4. **Decision Gate 2 (End of Week 2)** — Evaluate P1 data; decide: does P2 still make sense? Is P3 needed?
5. **Phase 2-3 (Week 3-4): Conditional Rollout** — Implement consulting questions and context-gating only if Gates 1 and 2 show positive ROI

### Key Principle
**Never assume consulting tone improves accuracy or engagement. Measure everything. Gate each phase on real data.**

---

## PART 1: MINIMUM VIABLE CHANGE (Phase 0)

### Goal
Test consulting-tone impact WITHOUT breaking accuracy, by implementing ONLY on RCS module (1 of 6 modules).

### Why RCS First?
- **Low risk:** RCS is self-contained module (no cross-module dependencies)
- **High volume:** RCS queries represent ~18% of all queries (measurable signal in 1 week)
- **Well-defined scope:** RCS consulting questions already tested in RCS_CONSULTING_QUESTIONS_TEST.md
- **Clear success metric:** RCS engagement (follow-ups, conversation depth) vs. accuracy (false negatives, satisfaction)
- **Rollback plan:** If RCS shows negative impact, revert single module (not entire system)

### Phase 0 Implementation (RCS Only)

#### What Changes
Replace RCS answer generation with consulting-tone version that:
1. **Keeps** current answer text (no format changes)
2. **Adds** context-checking follow-up (optional metadata)
3. **Gates** answer on user context assumptions (documented in response)
4. **Reduces** false confidence on ambiguous RCS queries

#### What Stays the Same
- WhatsApp, Bot Studio, Campaigns, Webhooks, Authentication modules: **UNCHANGED**
- Answer routing logic: **UNCHANGED**
- Confidence scoring algorithm: **UNCHANGED** (only interpretation changes)
- Langfuse data schema: **UNCHANGED** (add new fields only)

#### Code Changes (Phase 0 RCS)

```python
# kb_answer.py line ~6480 (in _compose_answer function)

def _compose_answer(query, intent, entities, evidence, explicit_module="General"):
    """Main answer composition: pick strategy based on intent + entities + MODULE."""
    
    # PHASE 0: RCS module gets consulting tone
    if explicit_module == "rcs":
        return _compose_answer_consulting_rcs(
            query=query,
            intent=intent,
            entities=entities,
            evidence=evidence
        )
    
    # All other modules: keep current problem-solution logic
    # (campaigns, bot_studio, webhooks, authentication, whatsapp, general)
    return _compose_answer_problem_solution(
        query=query,
        intent=intent,
        entities=entities,
        evidence=evidence,
        explicit_module=explicit_module
    )


def _compose_answer_consulting_rcs(query, intent, entities, evidence):
    """
    RCS-specific consulting-tone answer generation.
    
    Strategy:
    - For setup/configuration questions: answer + context assumptions
    - For ambiguous strategy questions: consulting follow-up instead of default IDK
    - For high-confidence evidence: keep simple answer (no change)
    """
    if not evidence or not evidence[0].get("score", 0):
        return "I don't know based on the current docs."
    
    top_chunk = evidence[0]
    score = top_chunk.get("score", 0)
    
    # HIGH confidence: return answer as-is, no changes
    if score >= 8.0:
        lines = top_chunk.get("lines", [])
        heading = top_chunk.get("heading", "")
        return f"**{heading}**\n" + "\n- ".join(lines[:5])
    
    # MEDIUM confidence (5.0-8.0): Answer + context check
    if score >= 5.0:
        lines = top_chunk.get("lines", [])
        heading = top_chunk.get("heading", "")
        answer_text = f"**{heading}**\n" + "\n- ".join(lines[:5])
        
        # Add consulting follow-up based on intent
        followup = _followup_for_rcs_intent(intent, entities)
        
        return {
            "answer": answer_text,
            "follow_up": followup,
            "confidence": score / 8.0,  # Normalized to [0,1]
            "context_assumptions": _context_assumptions_for_rcs(intent, entities),
            "consulting_tone": True
        }
    
    # LOW confidence (2.0-5.0): Consulting question or answer?
    if score >= 2.0:
        # For genuinely ambiguous queries (e.g., "best practices", "how to optimize")
        # ask consulting question instead of guessing
        if intent in ("strategy", "optimization", "decision"):
            return {
                "response_type": "consulting_question",
                "question": _diagnostic_question_for_rcs(query, entities),
                "why": "Your question has multiple valid answers depending on your use case. Let me ask first to give you the most relevant advice.",
                "confidence": 0.3,
                "consulting_tone": True
            }
        else:
            # For concrete questions (setup, error), still attempt answer
            lines = top_chunk.get("lines", [])
            heading = top_chunk.get("heading", "")
            return f"**{heading}**\n" + "\n- ".join(lines[:5])
    
    # VERY LOW confidence: IDK
    return "I don't know based on the current docs."


def _followup_for_rcs_intent(intent, entities):
    """Generate context-checking follow-up for RCS answers."""
    intent_map = {
        "setup": "Does this match your integration method? (e.g., using Gupshup SDK, REST API, or no-code integration)",
        "template": "Are you using text templates, rich cards, or carousels? That affects the exact steps.",
        "webhook": "Is this for inbound messages, delivery callbacks, or read receipts? Each has different setup.",
        "campaign": "Are you sending to a specific segment, or a broad audience? That changes the recommended approach.",
        "error": "Are you still seeing this issue, or has the setup changed since the error started?",
        "metrics": "Are you tracking engagement for one campaign type, or comparing across multiple? (Affects which metrics matter most)",
    }
    return intent_map.get(intent, "Does this match your specific use case?")


def _diagnostic_question_for_rcs(query, entities):
    """Generate diagnostic question for low-confidence RCS strategy queries."""
    strategy_questions = {
        "optimization": "Are you optimizing for delivery speed, engagement rate, or cost efficiency?",
        "best_practices": "Are you running promotional campaigns, transactional alerts, or customer support?",
        "decision": "What's your primary constraint: speed, cost, interactivity, or compliance?",
        "scale": "How many messages are you planning to send per day, and across how many users?",
    }
    # Return most likely question based on entity detection
    return strategy_questions.get(entities[0].get("type") if entities else "optimization", 
                                  "What's your primary use case for RCS?")


def _context_assumptions_for_rcs(intent, entities):
    """List assumptions we're making about user context."""
    assumptions = []
    if intent == "setup":
        assumptions.append("You have basic API integration knowledge")
        assumptions.append("Your organization has already registered as an RCS Agent")
    elif intent == "campaign":
        assumptions.append("You have customer data ready to segment")
        assumptions.append("You've already created message templates")
    return assumptions
```

#### Testing Phase 0

```python
# local/scripts/test_phase0_rcs_consulting.py

def test_rcs_consulting_tone():
    """
    Test Phase 0: RCS consulting-tone answers.
    
    Success criteria:
    1. All RCS queries return either full answer or consulting question
    2. No false negatives: if kb_search finds score>5, kb_answer provides response
    3. Confidence scores accurately reflect answer applicability
    4. Consulting follow-ups are actually helpful (manual review)
    """
    
    rcs_test_cases = [
        {
            "query": "What are the best practices for running holiday campaigns with RCS?",
            "expected_type": "consulting_question",  # Ambiguous strategy question
            "min_score": 2.8,
            "should_engage": True  # Should prompt follow-up
        },
        {
            "query": "How do I set up RCS authentication?",
            "expected_type": "answer_with_followup",  # Concrete + medium confidence
            "min_score": 5.0,
            "should_engage": True
        },
        {
            "query": "How do I enable OAuth2 for RCS?",
            "expected_type": "answer",  # Concrete setup, high confidence
            "min_score": 8.0,
            "should_engage": False  # Answer is clear, no follow-up needed
        },
        {
            "query": "RCS webhook payload structure",
            "expected_type": "answer",
            "min_score": 5.0,
            "should_engage": False
        },
    ]
    
    for test in rcs_test_cases:
        result = kb_answer.kb_answer({
            "query": test["query"],
            "module": "rcs"  # FORCE RCS MODULE
        })
        
        # Check response type
        if isinstance(result.get("answer"), dict):
            response_type = result["answer"].get("response_type", "answer_with_followup")
        else:
            response_type = "answer"
        
        # Verify scoring
        score = result.get("langfuse", {}).get("score", 0)
        assert score >= test["min_score"], \
            f"Query '{test['query']}': score {score} below min {test['min_score']}"
        
        # Verify engagement prompt
        has_followup = isinstance(result.get("answer"), dict) and "follow_up" in result["answer"]
        assert has_followup == test["should_engage"], \
            f"Query '{test['query']}': expected follow_up={test['should_engage']}, got {has_followup}"
    
    print("✓ Phase 0 RCS consulting-tone tests passed")


def measure_phase0_impact():
    """
    Measure Phase 0 engagement impact (1 week post-deployment).
    
    Metrics:
    - RCS engagement lift vs baseline
    - Accuracy hold: no regression in false negatives
    - Consulting tone adoption: % of RCS responses with follow-up
    """
    
    # Fetch Langfuse data for RCS queries over 7-day window
    rcs_queries_before = fetch_langfuse("channel=rcs AND date<2026-08-11", 7)
    rcs_queries_after = fetch_langfuse("channel=rcs AND date>=2026-08-11", 7)
    
    # Calculate engagement metrics
    before = {
        "idk_rate": sum(1 for q in rcs_queries_before if "i don't know" in q.get("answer", "").lower()) / len(rcs_queries_before),
        "follow_up_rate": sum(1 for q in rcs_queries_before if q.get("has_followup")) / len(rcs_queries_before),
        "avg_turns": avg_turns_for_queries(rcs_queries_before),
        "satisfaction": avg_satisfaction(rcs_queries_before),
    }
    
    after = {
        "idk_rate": sum(1 for q in rcs_queries_after if "i don't know" in q.get("answer", "").lower()) / len(rcs_queries_after),
        "follow_up_rate": sum(1 for q in rcs_queries_after if q.get("has_followup")) / len(rcs_queries_after),
        "avg_turns": avg_turns_for_queries(rcs_queries_after),
        "satisfaction": avg_satisfaction(rcs_queries_after),
    }
    
    print(f"""
    === PHASE 0 RCS IMPACT REPORT ===
    
    IDK Rate:           {before['idk_rate']:.1%} → {after['idk_rate']:.1%} ({(after['idk_rate']-before['idk_rate'])*100:+.1f}pp)
    Follow-Up Rate:     {before['follow_up_rate']:.1%} → {after['follow_up_rate']:.1%} ({(after['follow_up_rate']-before['follow_up_rate'])*100:+.1f}pp)
    Avg Turns/Session:  {before['avg_turns']:.1f} → {after['avg_turns']:.1f} ({((after['avg_turns']/before['avg_turns']-1)*100):+.0f}%)
    Satisfaction:       {before['satisfaction']:.1%} → {after['satisfaction']:.1%} ({(after['satisfaction']-before['satisfaction'])*100:+.1f}pp)
    """)
    
    # Decision gate logic
    engagement_lift = (after['follow_up_rate'] - before['follow_up_rate']) / before['follow_up_rate']
    accuracy_hold = after['idk_rate'] <= before['idk_rate'] + 0.05  # Allow 5pp drift
    
    decision = "PROCEED" if engagement_lift >= 0.20 and accuracy_hold else "INVESTIGATE"
    
    return {
        "phase0_passed": engagement_lift >= 0.20,
        "accuracy_held": accuracy_hold,
        "engagement_lift_pct": engagement_lift * 100,
        "recommendation": decision,
        "details": {"before": before, "after": after}
    }
```

#### Deployment (Phase 0)

```bash
# 1. Create feature flag (optional but recommended)
# In kb_answer.py or .env:
CONSULTING_TONE_RCS_ENABLED=true
CONSULTING_TONE_RCS_ONLY=true  # Don't apply to other modules

# 2. Deploy to staging
git commit -m "Phase 0: Implement consulting-tone answer generation for RCS module (low-risk MVP)"
git push origin feature/consulting-tone-rcs-phase0

# 3. Run regression tests (ensure other modules unaffected)
pytest skill/test_kb_answer.py -k "not rcs"  # Other modules should pass

# 4. Monitor Langfuse
# - Filter by channel=rcs
# - Track: IDK rate, follow-up rate, avg turns, satisfaction
# - Wait 7 days for statistical significance

# 5. Run decision gate measurement
python local/scripts/test_phase0_rcs_consulting.py && python local/scripts/measure_phase0_impact.py
```

---

## PART 2: DECISION TREE & PHASE GATES

### Decision Gate 1 (End of Week 1): RCS Consulting Tone Impact

#### Data to Collect

| Metric | Success Threshold | Rationale |
|--------|-------------------|-----------|
| **Engagement Lift** | +20% (relative) on follow-up rate | Shows users are more invested in answering |
| **Accuracy Hold** | IDK rate ≤ baseline + 5pp | Ensure we're not trading accuracy for engagement |
| **Satisfaction Alignment** | Consulting-tone responses rated ≥65% positive | Verify answers actually help |
| **False Negative Rate** | <5% (at most 1 query returns IDK when score>5) | Measure accuracy directly |

#### Decision Logic

```
IF engagement_lift >= 20% AND accuracy_hold == true THEN
    "Phase 1 APPROVED: Soft gradient confidence tiers"
    → PROCEED to Phase 1 with full system
    
ELIF engagement_lift >= 15% AND accuracy_hold == true THEN
    "Phase 1 CONDITIONAL: Positive signal but marginal"
    → PROCEED to Phase 1 with extended monitoring
    → Set engagement_lift target to +25% for Phase 1
    
ELIF engagement_lift < 15% OR accuracy_hold == false THEN
    "Phase 0 BLOCKED: Insufficient evidence or accuracy regression"
    → STOP all consulting-tone work
    → Investigate root cause (e.g., follow-ups not helpful)
    → Revert RCS to problem-solution mode
    
ELSE (ambiguous data)
    "Phase 0 EXTENDED: Run second week of RCS-only testing"
    → Extend Phase 0 by 7 days
    → Adjust consulting-tone parameters (e.g., confidence thresholds)
    → Re-measure and re-decide
```

---

### Decision Gate 2 (End of Week 2): Phase 1 Full-System Impact

#### Phase 1 Hypothesis
"Soft gradient confidence tiers (replacing hard 0.5 threshold) reduce IDK penalty while maintaining accuracy."

#### Phase 1 Data to Collect

| Metric | Phase 0 Baseline | Phase 1 Target | Rationale |
|--------|------------------|-----------------|-----------|
| **System-Wide IDK Rate** | 45.7% | <35% | Soft gradient bridges false negatives |
| **Follow-Up Rate** | 8% | >25% | Consulting questions drive engagement |
| **Avg Conversation Depth** | 1.2 turns | >2.0 turns | Longer conversations = stickier users |
| **Satisfaction (Answered)** | 75% | ≥75% | No regression on accuracy |
| **Satisfaction (IDK)** | 8% | ≥20% | Hard boundary reduced |
| **Confidence Calibration** | ±0.18 | ±0.08 | Confidence actually predicts accuracy |

#### Decision Logic for Phase 2

```
IF all_phase1_targets_met THEN
    "Phase 2 APPROVED: Consulting follow-ups + context gathering"
    → PROCEED to Phase 2 immediately
    → Phase 2 hypothesis: context-gating improves accuracy further
    
ELIF idk_rate_drop >= 10pp AND follow_up_rate >= 20% THEN
    "Phase 2 CONDITIONAL: Positive engagement, but accuracy uncertain"
    → PROCEED to Phase 2 WITH EXTENDED MONITORING
    → Add accuracy tracking dashboard before Phase 2 launch
    → Set Phase 2 accuracy target: maintain 75% satisfaction
    
ELIF idk_rate_drop < 10pp OR follow_up_rate < 15% THEN
    "Phase 2 BLOCKED: Insufficient engagement lift"
    → STAY WITH PHASE 1 (soft gradient only)
    → Investigate why follow-ups not resonating
    → Consider Phase 2 deprioritized (optional future work)
    
ELIF satisfaction_regression > 5pp THEN
    "CRITICAL: Accuracy regression detected"
    → IMMEDIATE ROLLBACK to Phase 0 (RCS only)
    → Disable Phase 1 system-wide
    → Investigate: why did soft gradient hurt accuracy?
    → DO NOT PROCEED to Phase 2
```

---

### Decision Gate 3 (End of Week 3): Phase 2 vs Phase 3 Trade-Off

#### Situation at Week 3

At this point, we've measured:
- **Phase 1:** Soft gradient impact on engagement + accuracy
- **Phase 2A (partial):** Early consulting follow-ups + data

#### The Question
"Do we pursue Phase 2 (more consulting questions) or Phase 3 (context-gating)?

**Trade-off:**
- **Phase 2 Path:** "Ask more questions before answering" → Higher engagement, but requires more user input
- **Phase 3 Path:** "Store + use user context" → More personalized, but requires tracking user state across conversations

#### Decision Logic

```
IF engagement_lift_phase1_2 >= 30% AND user_feedback_says_questions_helpful THEN
    "Phase 2 PRIMARY PATH: Users like being asked"
    → PRIORITIZE Phase 2 (consulting questions)
    → Phase 3 (context tracking) becomes optional enhancement
    → Phase 2 end-goal: 50%+ follow-up rate, 5+ avg turns
    
ELIF accuracy_improvement_phase1_2 >= 15% AND user_context_tracking_feasible THEN
    "Phase 3 PRIMARY PATH: Context-gating is the win"
    → PRIORITIZE Phase 3 (context tracking + confident confidence calibration)
    → Phase 2 (more questions) becomes secondary
    → Phase 3 end-goal: 80%+ confidence calibration, +25% accuracy on ambiguous queries
    
ELIF both_phase2_and_phase3_positive THEN
    "EXECUTE BOTH (but sequenced)"
    → Phase 2 Week 3-4 (consulting questions)
    → Phase 3 Week 4-5 (context-gating)
    → Measure incremental impact
    
ELSE (neither showing strong ROI)
    "CONSOLIDATE at Phase 1"
    → Keep soft gradient (Phase 1) as permanent change
    → Archive Phase 2 and Phase 3 as "future optimization"
    → Document lessons learned for next iteration
```

---

## PART 3: PHASE IMPLEMENTATION ROADMAP

### Timeline & Responsibilities

#### **Week 1: Phase 0 (RCS-Only MVP)**
| Day | Task | Owner | Success Criteria |
|-----|------|-------|------------------|
| Mon-Tue | Implement consulting-tone answer generation for RCS module only | Engineer | Code reviewed, feature flagged |
| Wed | Deploy to staging + run regression tests | QA | No regressions in non-RCS modules |
| Thu | Deploy to production (small rollout: 10% RCS traffic) | DevOps | Langfuse tracking activated |
| Fri | Initial monitoring (24h data) | Analytics | No critical errors, data flowing |
| Mon | Full RCS rollout (100% traffic) | DevOps | Monitoring stable |
| Tue-Fri | Collect full week of engagement data | Analytics | Prepare for Decision Gate 1 |

#### **End of Week 1: Decision Gate 1**
| Timing | Task | Owner | Deliverable |
|--------|------|-------|-------------|
| Friday EOD | Generate Phase 0 impact report | Analytics | Go/No-Go recommendation |
| Friday EOD | Review engagement + accuracy metrics | PM + Tech Lead | Decision: Proceed to Phase 1? |
| Mon 9am | Communicate decision to team | PM | Message to stakeholders |

#### **Week 2: Phase 1 (Soft Gradient) IF GATE 1 PASSED**
| Day | Task | Owner | Success Criteria |
|-----|------|-------|------------------|
| Mon-Tue | Implement confidence tiers (0.80/0.60/0.40/0.0) | Engineer | Code reviewed, tested on RCS only |
| Wed | Test soft gradient with RCS + one other module (Campaigns) | QA | 2 modules tested in staging |
| Thu | Deploy to production (Campaigns module added) | DevOps | Feature flagged for rollback |
| Fri | Initial monitoring (48h data) | Analytics | Confidence tier distribution tracked |
| Tue-Fri | Collect full week of Phase 1 system-wide data | Analytics | Prepare for Decision Gate 2 |

#### **End of Week 2: Decision Gate 2**
| Timing | Task | Owner | Deliverable |
|--------|------|-------|-------------|
| Friday EOD | Generate Phase 1 full-system impact report | Analytics | IDK rate, follow-up rate, satisfaction |
| Friday EOD | Review accuracy regression (critical check) | Data Scientist | Calibration analysis |
| Mon 9am | Decide: Phase 2 vs Phase 3 vs Consolidate | PM + Tech Lead | Official roadmap decision |

#### **Week 3-4: Phase 2 and/or Phase 3 (Conditional)**
- **IF Phase 2:** Consulting questions (diagnostic questions for ambiguous queries)
- **IF Phase 3:** Context-gating (track user context, adjust confidence based on fit)
- **IF Neither:** Keep Phase 1, archive Phase 2/3 for future

---

## PART 4: SUCCESS METRICS & MEASUREMENT FRAMEWORK

### Tier 1: Core Engagement Metrics (Measure Real-Time)

#### Metric 1: IDK Rate
**Definition:** % of answered queries that return "I don't know"

```
IDK Rate = (Count of "I don't know" responses) / (Total responses) × 100%

Current Baseline: 45.7%
Phase 0 Target: 35-40% (10-15pp reduction)
Phase 1 Target: 25-30% (15-20pp reduction)
```

**How to track:**
```python
# Langfuse query:
filter: status = "success" AND response contains "i don't know"
group_by: channel, date
metric: count / total_responses
```

**Why it matters:**
- IDK is the strongest satisfaction killer (8% satisfaction vs. 75% when answered)
- Measuring IDK directly measures "are we helping users or dismissing them?"
- Phase 0/1 success rides on this metric

---

#### Metric 2: Follow-Up Propensity (Engagement Lift)
**Definition:** % of responses followed by user turn within 5 minutes

```
Follow-Up Propensity = (Responses with follow-up turn within 5min) / (Total responses) × 100%

Current Baseline: 8%
Phase 0 Target: 15-25% (7-17pp increase)
Phase 1 Target: 30-50% (22-42pp increase)
```

**How to track:**
```python
# Langfuse query:
filter: turn_type = "assistant" AND timestamp < T
group_by: response_id
join_next: turn_type = "user" AND timestamp < T+300s
metric: count_with_followup / count_total
```

**Why it matters:**
- Follow-ups = users aren't abandoning (they're engaged)
- Shows consulting tone is *inviting* rather than *dismissive*
- Direct measure of engagement multiplier (1-turn vs. 4+ turns)

---

#### Metric 3: Conversation Depth (Turns per Session)
**Definition:** Average number of turns in a single conversation before end

```
Avg Turns = Sum(turns per session) / Count(sessions)

Current Baseline: 1.2 turns/session
Phase 0 Target: 1.5-2.0 turns/session
Phase 1 Target: 2.5-3.5 turns/session
Phase 2+ Target: 4-6 turns/session
```

**Why it matters:**
- Longer conversations = more stickiness (user explores multiple topics)
- Correlates with repeat user rate
- Multiplies engagement: 5 turns × 0.65 satisfaction = higher value than 1 turn × 0.75 satisfaction

---

### Tier 2: Accuracy & Calibration Metrics (Measure Weekly)

#### Metric 4: Confidence Calibration Error
**Definition:** Difference between reported confidence and actual user satisfaction

```
Calibration Error = |Reported Confidence - Actual Satisfaction|

Where:
- Reported Confidence = kb_answer's confidence score (0-1)
- Actual Satisfaction = Thumbs up / total responses by confidence bucket

Example:
  Confidence 0.8 group: 85% users give thumbs up → Error = |0.8 - 0.85| = 0.05 ✓ (good)
  Confidence 0.8 group: 60% users give thumbs up → Error = |0.8 - 0.60| = 0.20 ✗ (bad)
```

**Why it matters:**
- Shows if consulting-tone answers are actually more accurate
- Indicates if we're being honest about what we know
- Phase 1/2/3 should *reduce* calibration error (from ±0.18 to ±0.04)

**How to track:**
```python
# Segment responses by confidence bucket (0-0.2, 0.2-0.4, 0.4-0.6, 0.6-0.8, 0.8-1.0)
# For each bucket:
#   Satisfaction = avg(thumbs_up) for that bucket
#   Calibration Error = |confidence_bucket_midpoint - satisfaction|
# Report: mean + std dev of calibration error
```

---

#### Metric 5: False Negative Rate
**Definition:** % of queries where kb_answer says IDK but kb_search found a good result (score > 5)

```
False Negative Rate = (Count of IDK despite search score > 5) / (Total search hits > 5) × 100%

Current Baseline: ~15-20% (estimated; need to measure)
Phase 0 Target: <10%
Phase 1 Target: <5%
```

**Why it matters:**
- Directly measures if consulting tone *prevents* "we don't know it" errors
- KB search + kb_answer mismatch is addressable (means we're being overly conservative)
- Phase 0/1 should eliminate most of these

---

#### Metric 6: Application Accuracy (Spot Checks)
**Definition:** % of responses where user confirms "yes, that worked" vs "no, that didn't help"

```
Application Accuracy = (Responses user says worked) / (Total responses with feedback) × 100%

Measure via:
- Thumbs up/down reactions (immediate)
- Follow-up queries (if user refines, suggests original answer wasn't perfect)
- Session success (did user achieve their goal, or abandon?)

Current Baseline: ~70% (from thumbs-up data)
Phase 1 Target: ≥70% (hold steady; no regression)
Phase 2+ Target: ≥75% (improve via context-gating)
```

**Why it matters:**
- Ensures we're not trading accuracy for engagement
- Consulting tone should improve this (context-gating) not hurt it
- Must hold steady through all phases

---

### Tier 3: Business Metrics (Measure Monthly)

#### Metric 7: Repeat User Rate
**Definition:** % of users who return with follow-up question within 30 days

```
Repeat User Rate = (Unique users with 2+ conversations within 30 days) / (Unique users total) × 100%

Current Baseline: 12%
Phase 1 Target: 18-25%
Phase 2+ Target: 30-40%
```

**Why it matters:**
- Shows if consulting tone creates "habit-forming" product behavior
- Repeat users = higher customer lifetime value
- Long-term success metric (not just engagement)

---

### Measurement Dashboard (Langfuse + Custom)

```python
# local/scripts/build_consulting_tone_dashboard.py

class ConsultingToneDashboard:
    
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.langfuse = LangfuseClient()
    
    def measure_all_metrics(self):
        """Run all 7 metrics + generate decision gates."""
        
        tier1 = {
            "idk_rate": self.measure_idk_rate(),
            "followup_propensity": self.measure_followup_propensity(),
            "avg_conversation_depth": self.measure_conversation_depth(),
        }
        
        tier2 = {
            "confidence_calibration_error": self.measure_calibration_error(),
            "false_negative_rate": self.measure_false_negatives(),
            "application_accuracy": self.measure_application_accuracy(),
        }
        
        tier3 = {
            "repeat_user_rate": self.measure_repeat_users(),
        }
        
        return {
            "tier1_engagement": tier1,
            "tier2_accuracy": tier2,
            "tier3_business": tier3,
            "recommendation": self.generate_recommendation(tier1, tier2, tier3),
        }
    
    def generate_recommendation(self, tier1, tier2, tier3):
        """Logic for decision gates."""
        
        # Gate 1 criteria (Phase 0 → Phase 1)
        engagement_lift = tier1["followup_propensity"]["delta"] / tier1["followup_propensity"]["baseline"]
        accuracy_hold = tier2["application_accuracy"]["delta"] >= -0.05  # Allow 5pp drop
        
        gate1_pass = engagement_lift >= 0.20 and accuracy_hold
        
        # Gate 2 criteria (Phase 1 → Phase 2)
        idk_drop = tier1["idk_rate"]["delta"]
        followup_rate = tier1["followup_propensity"]["current"]
        
        gate2_pass = idk_drop >= 10 and followup_rate >= 0.25
        
        return {
            "gate1_pass": gate1_pass,  # Proceed to Phase 1?
            "gate2_pass": gate2_pass,  # Proceed to Phase 2?
            "next_action": "Phase 1" if gate1_pass else "Investigate",
            "confidence_level": "HIGH" if gate1_pass else "MEDIUM" if engagement_lift >= 0.15 else "LOW",
        }
```

---

## PART 5: RISK MITIGATION & ROLLBACK PLAN

### Risk 1: "Consulting Tone Reduces Accuracy"

**Symptom:** Application accuracy drops below 70%, users report wrong answers more

**Mitigation:**
- Gate each phase on accuracy metrics
- If regression detected at any gate, rollback immediately
- Requires: calibration tracking + thumbs-up/down feedback loop

**Rollback Plan:**
```bash
# If accuracy drops > 5pp at any decision gate:
# 1. Stop Phase N immediately (revert to previous phase)
# 2. Investigate root cause
# 3. Don't proceed until root cause fixed

# Example: Phase 1 causes accuracy regression
git revert <commit_hash_of_phase1>
git push origin main
# Restart Phase 1 investigation after fix
```

---

### Risk 2: "Consulting Tone Delays Answers"

**Symptom:** Users complain about follow-up questions slowing them down

**Mitigation:**
- Only ask consulting questions on *genuinely ambiguous* queries (intent detection)
- For clear setup/error queries, provide fast answer + optional follow-up
- UI can show "Answer" tab + "Ask clarifying questions" tab

**Monitor for:**
- Sentiment analysis (negative feedback on follow-ups)
- Abandonment after consulting question (% who don't respond)
- Session abandonment rate (stayed flat or increased)

---

### Risk 3: "Consulting Confidence Scores Lower Than Before"

**Symptom:** Average confidence drops from 0.72 to 0.65, looks like regression

**Mitigation:**
- This is **intentional calibration**, not a bug
- Old 0.72 was overconfident (true fit was ~0.60)
- New 0.65 accurately reflects true fit
- Communicate: "We're reporting more honest confidence"
- Measure: calibration error should *improve* (±0.18 → ±0.04)

---

### Risk 4: "RCS Phase 0 Shows No Engagement Lift"

**Symptom:** Follow-up rate stays at 8%, IDK rate only drops 5pp

**Mitigation (Decision Gate 1 Logic):**
- If engagement_lift < 15%, extend Phase 0 by 1 week
- Investigate: Why aren't consulting follow-ups helping?
  - Are follow-up questions poorly phrased?
  - Are consulting questions only for ambiguous queries? (Should be broader?)
  - Is RCS module too small to show signal? (15% of queries)
- Adjust consulting-tone approach based on feedback
- Re-measure week 2

---

### Risk 5: "Langfuse Data Contamination"

**Symptom:** Confidence tier field not properly logged, breaking analysis

**Mitigation:**
- Add data validation: every RCS response must have confidence_tier field
- Test logging in staging: ensure field always present
- Alert if >5% of responses missing confidence_tier
- Reprocess old data if logging failure detected

---

## PART 6: DECISION TREE (Quick Reference)

```
START: Phase 0 (RCS-only, Week 1)
  ↓
MEASURE: Engagement lift (follow-up rate), Accuracy hold
  ↓
DECISION GATE 1 (End of Week 1)
  ├─ YES (engagement ≥20% AND accuracy ≥baseline-5pp)
  │  → PROCEED to Phase 1 (Soft gradient, Week 2)
  │
  ├─ MAYBE (engagement ≥15% AND accuracy ≥baseline-5pp)
  │  → PROCEED to Phase 1 WITH monitoring
  │  → Set higher target for Phase 1
  │
  └─ NO (engagement <15% OR accuracy regressed)
     → STOP consulting-tone project
     → Revert RCS to problem-solution
     → Root cause analysis: why didn't it work?

(If Phase 1 proceeds)
PHASE 1 (System-wide soft gradient, Week 2)
  ↓
MEASURE: IDK rate, follow-up rate, calibration error, satisfaction hold
  ↓
DECISION GATE 2 (End of Week 2)
  ├─ YES (all targets met)
  │  → DECIDE: Phase 2 vs Phase 3 vs Consolidate
  │  → IF engagement_lift ≥30% → Phase 2 (consulting questions)
  │  → IF accuracy_improve ≥15% → Phase 3 (context-gating)
  │  → ELSE → Stay at Phase 1
  │
  ├─ PARTIAL (some targets met)
  │  → Continue Phase 1 with extended monitoring
  │  → Investigate underperforming metrics
  │  → Decide Phase 2/3 after investigation
  │
  └─ CRITICAL (accuracy regression)
     → ROLLBACK Phase 1
     → Revert to baseline
     → Debug root cause

(If Phase 2 or Phase 3 proceeds)
PHASE 2/3 (Week 3-4)
  ↓
MEASURE: Incremental impact on engagement + accuracy
  ↓
DECISION (End of Week 4)
  ├─ YES → Consolidate Phase 2/3 into standard answer generation
  │
  └─ NO → Archive for future; keep Phase 1
     → Document lessons learned
```

---

## PART 7: IMPLEMENTATION CHECKLIST

### Pre-Implementation (Before Phase 0)

- [ ] Review consulting_tone_impact_analysis.md (confidence + engagement theory)
- [ ] Review RCS_CONSULTING_QUESTIONS_TEST.md (testing framework)
- [ ] Create Langfuse dashboard: RCS queries by date + metric
- [ ] Set up decision gate measurement scripts (test Phase 0 impact)
- [ ] Identify on-call engineer for quick rollback if needed

### Phase 0 Implementation (Week 1)

- [ ] Implement _compose_answer_consulting_rcs() function
- [ ] Implement consulting follow-up logic for RCS intents
- [ ] Test locally: 10 RCS queries return consulting-tone responses
- [ ] Feature flag: CONSULTING_TONE_RCS_ENABLED
- [ ] Code review + approval
- [ ] Deploy to staging + regression test (non-RCS modules)
- [ ] Deploy to production (10% RCS traffic, Thu)
- [ ] Monitor: No errors in first 24h
- [ ] Roll out to 100% RCS traffic (Fri-Mon)
- [ ] Collect full week of data (Tue-Fri)

### Decision Gate 1 (End of Week 1)

- [ ] Run measurement script: measure_phase0_impact()
- [ ] Review: engagement_lift ≥20%? accuracy_hold?
- [ ] Decision: Proceed to Phase 1? (Yes/No/Maybe)
- [ ] Document: Phase 0 impact report
- [ ] Communicate: Decision to team + stakeholders

### Phase 1 Implementation (Week 2, if Gate 1 passes)

- [ ] Add confidence tier constants (0.80/0.60/0.40)
- [ ] Implement _confidence_band() function
- [ ] Modify kb_answer() logic: graduated response vs hard boundary
- [ ] Test locally: confidence bands correctly map to response tiers
- [ ] Feature flag: CONSULTING_TONE_PHASE1_ENABLED
- [ ] Deploy to staging + regression test
- [ ] Deploy to production (Campaigns module added, Thu)
- [ ] Collect full week of data (Fri-Mon)

### Decision Gate 2 (End of Week 2)

- [ ] Run full measurement: tier1 + tier2 metrics
- [ ] Critical check: accuracy regression?
- [ ] Decision: Phase 2 vs Phase 3 vs Consolidate?
- [ ] Document: Phase 1 impact report
- [ ] Communicate: Phase 2/3 roadmap decision

### Phase 2/3 Implementation (Week 3-4, conditional)

- [ ] Implement chosen phase (consulting questions OR context-gating)
- [ ] Test locally + regression test
- [ ] Deploy + monitor
- [ ] Collect 2 weeks of data
- [ ] Measure incremental impact
- [ ] Final decision: Consolidate or Archive?

---

## CONCLUSION

This strategy ensures that **consulting-tone implementation is data-driven, risk-mitigated, and incrementally validated**.

**Key Principle:** *Never assume consulting tone improves accuracy or engagement. Gate each phase on real measurement. Rollback if accuracy regresses.*

**Expected Outcome (if all gates pass):**
- Week 1-2: 35% IDK rate (from 45.7%), 25% follow-up rate (from 8%)
- Week 2-4: 25% IDK rate, 50%+ follow-up rate, 4-6 turn average conversations
- Month 2: 30%+ repeat user rate, +25% application accuracy on ambiguous queries

**If any gate fails:** Rollback, investigate, and iterate. No sunk cost fallacy.

---

**Document Status:** Ready for implementation  
**Next Step:** Approval from stakeholders (PM + Tech Lead) → Execute Phase 0
