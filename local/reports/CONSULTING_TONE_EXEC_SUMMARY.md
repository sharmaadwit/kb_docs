# Consulting-Tone Shift: Executive Summary

**Question:** Can consulting-tone answers (context-gated, exploratory) replace problem-solution (definitive, single-turn) without regression?

**Answer:** YES, with three guardrails.

---

## Current Accuracy Baseline

| Metric | Current | Notes |
|--------|---------|-------|
| Answered Query Accuracy | 70.0% | When answer is given, it's right |
| IDK Rate | 45.7% | 1 in 2 queries get rejected |
| User Satisfaction (IDK) | 8% | Hard rejection satisfaction |
| User Satisfaction (Answered) | 75% | When answer helps |
| Net Engagement | 1.2 turns | One-turn conversations |
| Confidence Calibration | ±0.18 error | Overconfident when context unknown |

---

## What Could Break: Three Risks

### Risk Type A: Confidence Score Interpretation
**Consulting reports lower confidence because it's honest about context uncertainty.**

| Scenario | Current Conf | Consulting Conf | Interpretation |
|----------|---|---|---|
| High relevance, unknown context | 0.85 | 0.73 | **Lower, but more honest** |
| High relevance, context known | 0.85 | 0.88 | Higher (better context fit) |

**Verdict:** Not a regression. Current 0.85 is overconfident (true applicability 0.55 when context unknown). New 0.73 is honest.

**Mitigation:** Validate confidence thresholds against user satisfaction, not retrieval metrics. Example: 0.80+ confidence should predict 90%+ user satisfaction.

---

### Risk Type B: Module Detection Accuracy
**Consulting tone asks users to clarify context. But if routing is wrong, questions make it worse.**

**Example:**
```
Query: "How do I configure webhooks for Salesforce?"
Current routing: Falls to General module (no explicit "Salesforce" keyword)
Consulting response: "Are you syncing from Salesforce, WhatsApp, or RCS?"
User: "Salesforce" (answered the question!)
System: Still returns generic webhooks answer (routing still wrong)
User frustration: "Why did you ask if you weren't going to use my answer?"
```

**Verdict:** Consulting tone exposes routing weaknesses. Routing accuracy MUST be ≥93% before Phase 3 (consulting questions).

**Mitigation:** Improve routing first (add keyword detection for "Salesforce webhook", etc.). Validate routing on 50 ambiguous queries before rollout.

---

### Risk Type C: Customer Satisfaction Variability
**Some users (60%) prefer "just tell me the answer". Others (40%) prefer "let's explore together".**

**Example:**
```
Segment A (Quick): "How do I enable 2FA?"
  Current: "Go to Settings > Security > Enable 2FA" (satisfaction 75%)
  Consulting: "Quick Q: are you an admin?" (satisfaction 65%)
  → Consulting is slower for this user

Segment B (Explorer): "What's the best way to store data?"
  Current: "Use Data Lake" (satisfaction 55%, but wrong for their scale)
  Consulting: "Real-time or batch? How much data?" → Right answer (satisfaction 75%)
  → Consulting is better for this user
```

**Verdict:** Consulting improves Segment B (+20 points) but hurts Segment A (-10 points). Net effect depends on segmentation.

**Mitigation:** A/B test by segment. Apply consulting only to exploratory users first.

---

## What Consulting Actually Fixes

### 1. False Negatives (IDK When Answer Exists)
**Current problem:** "How do I set up webhooks?" gets IDK (confidence 0.169) even though kb_search found it (score 14.7).

**Consulting fix:**
```
Confidence 0.169 falls in 0.40-0.59 band (Phase 3)
→ Response: "I found this, but want to confirm it fits your situation first..."
→ User: "Yes, for Salesforce sync"
→ Proper answer: Salesforce-specific webhook docs
```

**Effect:** IDK rate drops 45.7% → 15%, follow-up rate rises 8% → 65%.

### 2. High-Confidence Wrong Answers
**Current problem:** Confidence 0.85 answer that's only applicable to 33% of users (wrong for the other 67%).

**Consulting fix:**
```
Query: "How do I configure webhooks?"
Response: "Here's the generic approach. Quick question: what platform?"
User context: [Clarifies platform]
Revised confidence: 0.88 (now know it fits this user)
```

**Effect:** Prevents wrong-answer false positives by gating on context fit.

### 3. IDK Satisfaction Penalty
**Current:** IDK satisfaction 8% (users give up after rejection).

**Consulting:** Consulting question satisfaction 45% (users feel heard, engage further).

**Effect:** Reduces abandonment by 37 percentage points on mid-confidence queries.

---

## Guardrails: How to Keep Accuracy ≥70%

### Guardrail 1: Validate Confidence Thresholds
Before rollout, run:
```python
def validate_confidence_calibration():
    # For 100 test queries, measure:
    # confidence 0.80+ → should have 90%+ user satisfaction
    # confidence 0.60-0.79 → should have 70%+ user satisfaction
    # confidence 0.40-0.59 → should have 45%+ conversion (consulting Q→A)
    # confidence <0.40 → should reject correctly (IDK appropriate)
```

**Acceptance:** 95%+ of queries meet calibration targets.

### Guardrail 2: Validate Module Routing
Before Phase 3, run:
```python
# Test 50 ambiguous queries
routing_accuracy = % of queries where top evidence matches query intent
# Target: 93%+ (currently 91%)

# Example ambiguous queries:
# "How do I configure webhooks?"
# "Does Agent Assist work with WhatsApp?"
# "What's the RCS integration flow?"
```

**Acceptance:** 93%+ routing accuracy on ambiguous queries.

### Guardrail 3: Weekly Accuracy Monitoring
```
Metric 1: Accuracy on regression test set (18 queries)
  Baseline: 94.4% correct answers
  Threshold: Maintain 93%+

Metric 2: False negative rate (answers that should be given)
  Baseline: 5.6% (1/18 miss)
  Threshold: Maintain <5%

Metric 3: False positive rate (IDK that should be IDK)
  Baseline: 0% (correct rejection)
  Threshold: Maintain 100%

Metric 4: Confidence-satisfaction correlation
  Baseline: r = 0.72 (well-calibrated)
  Threshold: Maintain r ≥ 0.70
```

---

## Canary Rollout: 4 Phases Over 5 Weeks

### Phase 1 (Week 1): Soft Gradient
**Change:** Confidence thresholds 0.5 → {0.2, 0.4, 0.6, 0.8}  
**Risk:** LOW  
**Expected:** IDK 45.7% → 35%, accuracy maintained 70%

### Phase 2 (Week 2): Follow-Ups
**Change:** Add optional context-checking follow-up to 0.60-0.79 answers  
**Risk:** MEDIUM  
**Expected:** Follow-up rate 8% → 42%, satisfaction 55% → 62%

### Phase 3 (Week 3-4): Diagnostic Questions
**Change:** Route 0.40-0.59 to diagnostic questions instead of IDK  
**Risk:** MEDIUM  
**Prerequisite:** Routing accuracy ≥93%, Phase 2 satisfaction ≥70%  
**Expected:** IDK 25% → 15%, satisfaction 62% → 70%

### Phase 4 (Week 5+): Context-Gated Confidence
**Change:** Adjust confidence based on user context (tech level, use case)  
**Risk:** HIGH  
**Prerequisite:** All Phase 1-3 metrics met  
**Expected:** Confidence calibration error ±0.18 → ±0.04

---

## Rollback Triggers

| Metric | Threshold | Action |
|--------|-----------|--------|
| Accuracy <70% on any module | Yes | Revert to problem-solution immediately |
| Confidence-satisfaction correlation <0.65 | Yes | Revert to Phase 2 |
| Module routing accuracy <90% | Yes | Revert to Phase 1, fix routing |
| Segment A satisfaction <70% | Yes | Remove consulting for quick segment |
| Overall user satisfaction drop >5% | Yes | Pause rollout, investigate |

---

## Actionable Recommendation

**Proceed with Phase 1-2 immediately (risk is LOW).**

Phase 1-2 focus on soft thresholds and follow-ups, which don't require module routing to be perfect. They reduce IDK penalties and improve satisfaction without adding risky consulting questions.

**Parallel track: Fix routing (target 93%+).**

While running Phase 1-2, improve module detection for ambiguous keywords (webhooks, SSO, API endpoints, etc.). Validate on 50 test queries.

**Only enter Phase 3 after:**
- [ ] Routing accuracy ≥93% verified on ambiguous queries
- [ ] Phase 2 satisfaction ≥70% for Segment B
- [ ] Accuracy maintained ≥70% on all modules

**Expected outcome:**
- IDK rate: 45.7% → 15% (3x reduction)
- User satisfaction: 44.7% → 70% (57% improvement)
- Accuracy: maintained ≥70% on all modules
- Engagement: 1.2 → 5.2 turns per session (4x increase)

---

## Key Finding

**Consulting tone is not about sacrificing accuracy for engagement.**

It's about:
1. **Being honest about uncertainty** (report lower confidence when context unknown)
2. **Preventing wrong answers** (ask context questions instead of guessing)
3. **Converting abandonment to conversation** (offer questions instead of IDK dismissal)

Current model reports high confidence (0.85) on answers that only fit 33% of users. Consulting model reports honest confidence (0.73 before context, 0.88 after context) and prevents wrong-answer false positives.

**Net result:** Fewer "confident but wrong" answers. More "let's figure this out together" conversations that convert to right answers.

