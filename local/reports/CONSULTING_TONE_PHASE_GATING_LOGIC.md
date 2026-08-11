# Consulting-Tone Implementation: Phase Gating Logic & Decision Framework

**Purpose:** Define quantitative decision criteria for Phase 0 → Phase 1 → Phase 2/3 progression  
**Audience:** PM, Tech Lead, Analytics  
**Date:** 2026-08-11

---

## OVERVIEW: Why Phase Gating?

**Problem:** Without gates, we risk:
- Implementing consulting-tone system-wide if RCS-only test shows even marginal improvement
- Pursuing Phase 2 (consulting questions) when Phase 1 (soft gradient) is doing all the work
- Continuing after accuracy regression (false positives that actually hurt)

**Solution:** Clear, quantitative decision gates that:
1. Are measurable within 1-2 weeks
2. Gate phase progression on **accuracy first, engagement second**
3. Allow for rollback without sunk-cost fallacy
4. Provide clear "proceed/investigate/stop" signals

---

## GATE 1: RCS-Only MVP → System-Wide Phase 1

### Timing
**Measurement Period:** Monday Week 1 - Friday Week 1 (7 days RCS queries)  
**Decision Date:** Friday EOD Week 1  
**Decision Makers:** PM + Tech Lead

### Hypothesis Being Tested
"Consulting-tone answer generation for RCS increases user engagement (follow-up rate) without sacrificing accuracy."

### Success Criteria (All Must Pass)

#### Criterion 1A: Engagement Lift (Primary)
```
Metric: Follow-Up Propensity (% of responses with user turn within 5 min)

Success Threshold: ≥20% relative increase
  Current (RCS baseline): 8%
  Required minimum: 9.6% (8% × 1.20)
  Target: 12-16% (8% × 1.50-2.0)

Logic:
  If follow_up_rate_after / follow_up_rate_before ≥ 1.20:
    PASS (users engaging with consulting-tone answers)
  Else:
    FAIL (no engagement signal; consult not compelling)
```

**Why this matters:**
- Direct measure of "is consulting tone inviting follow-up?"
- Follow-up = conversation depth = stickiness
- 20% lift is conservative: even small improvements show signal

**What to watch for:**
- If lift is 15-20% (marginal): Extend Phase 0 by 1 week for more data
- If lift is 10-15% (weak): Investigate why (Q quality? intent detection? wrong module?)
- If lift is <10%: No engagement signal; stop project

---

#### Criterion 1B: Accuracy Hold (Critical)
```
Metric: Application Accuracy (% of responses user confirms as helpful)

Success Threshold: ≥70% maintained, no regression >5pp
  Current baseline: ~70% (from thumbs-up/thumbs-down data)
  Acceptable drift: -5pp (70% → 65%)
  Target: ≥70% maintained (no change)

Logic:
  If application_accuracy_after ≥ (application_accuracy_before - 0.05):
    PASS (consulting tone didn't hurt accuracy)
  Else:
    FAIL IMMEDIATELY (accuracy regression; this is critical)
```

**Why this matters:**
- Consulting tone MUST NOT make wrong answers more common
- If accuracy drops, engagement gains are hollow (users get bad advice)
- 5pp tolerance: small noise, but >5pp = real regression

**What to watch for:**
- If accuracy ≥70%: Clear pass
- If accuracy 65-70% (below baseline but >65%): Review thumbs-down comments; may be measurement noise
- If accuracy <65%: STOP; revert RCS immediately

**How to measure:**
```python
# Via Langfuse thumbs-up/thumbs-down reactions
application_accuracy = count(thumbs_up) / (count(thumbs_up) + count(thumbs_down))

# Filter: channel="rcs" AND date >= [Phase0Start] AND date < [Phase0End]
# Group by: response_id, thumbs_reaction
# Calculate: % thumbs_up of all reactions
```

---

#### Criterion 1C: IDK Rate Improvement (Supportive)
```
Metric: IDK Rate (% of queries returning "I don't know")

Success Threshold: Reduced to 35-40% (from 45.7% baseline)
  This is NOT a hard gate; just confirms consulting-tone intent

Logic:
  If idk_rate_after ≤ 40%:
    GOOD (consulting tone reducing false IDKs)
  Else:
    NEUTRAL (IDK didn't drop, but engagement might still be up)
```

**Why this matters:**
- Soft indicator of "are we helping users who would have gotten IDK?"
- IDK reduction = fewer frustrated users
- NOT a hard gate because consulting tone might reduce IDK via better questions, not just more answers

---

### Decision Logic: Gate 1 Pass/Fail

```python
def gate1_decision(metrics):
    """
    Decision logic for Phase 0 → Phase 1 progression.
    
    metrics = {
        "engagement_lift": 0.25,          # e.g., 25% = follow-up 8% → 10%
        "accuracy_hold": True,            # e.g., 70% → 69% (no regression)
        "idk_rate": 0.38,                 # e.g., 38% (down from 45.7%)
    }
    """
    
    engagement_lift = metrics["engagement_lift"]
    accuracy_hold = metrics["accuracy_hold"]
    idk_rate = metrics["idk_rate"]
    
    # HARD gates (must both pass)
    hard_gates_pass = (
        engagement_lift >= 0.20 and
        accuracy_hold == True
    )
    
    if not hard_gates_pass:
        # Check if marginal (worth extending Phase 0)
        if 0.15 <= engagement_lift < 0.20 and accuracy_hold:
            return "MAYBE: Marginal engagement signal. Extend Phase 0 by 1 week."
        else:
            return "STOP: Insufficient engagement lift or accuracy regression. Investigate root cause."
    
    # Soft gates (supportive)
    soft_gates_pass = idk_rate <= 0.40
    
    if hard_gates_pass and soft_gates_pass:
        return "PROCEED (HIGH CONFIDENCE): All criteria met. Phase 1 approved."
    elif hard_gates_pass and not soft_gates_pass:
        return "PROCEED (MEDIUM CONFIDENCE): Engagement OK, but IDK didn't drop. Monitor in Phase 1."
    
    # Should never reach here (hard gates decide above)
```

### Report Template: Gate 1

```
═══════════════════════════════════════════════════════════════════
DECISION GATE 1 REPORT: RCS Phase 0 → Phase 1
Period: Mon 2026-08-11 to Fri 2026-08-15
Sample Size: [N RCS queries, M unique users]
═══════════════════════════════════════════════════════════════════

ENGAGEMENT METRICS (Hard Gate)
──────────────────────────────
Follow-Up Rate (before):    8.0%
Follow-Up Rate (after):     [X]%
Lift:                       [Y]% relative
Required:                   ≥20%
Status:                     [✓ PASS / ✗ FAIL]

ACCURACY METRICS (Critical Gate)
─────────────────────────────────
Application Accuracy (before):  70%
Application Accuracy (after):   [X]%
Drift:                          [Y]pp (allow -5pp)
Status:                         [✓ PASS / ✗ FAIL]

IDK RATE (Supportive)
─────────────────────
IDK Rate (before):          45.7%
IDK Rate (after):           [X]%
Target:                     ≤40%
Status:                     [✓ GOOD / ◎ NEUTRAL]

RECOMMENDATION
───────────────
Gate 1 Result:  [PASS / FAIL / MAYBE]
Decision:       [PROCEED to Phase 1 / INVESTIGATE / STOP]
Confidence:     [HIGH / MEDIUM / LOW]

NEXT STEPS
──────────
[If PASS: Deploy Phase 1 week 2]
[If MAYBE: Extend Phase 0 for 1 week]
[If FAIL: Root cause analysis + iterate Phase 0]

Approved By: [Name]
Date: [Date]
═══════════════════════════════════════════════════════════════════
```

---

## GATE 2: Phase 1 → Phase 2/3 Decision

### Timing
**Measurement Period:** Mon Week 2 - Fri Week 2 (7 days system-wide queries)  
**Decision Date:** Friday EOD Week 2  
**Decision Makers:** PM + Tech Lead + Analytics

### Hypothesis Being Tested
"Soft gradient confidence tiers (0.80/0.60/0.40 instead of binary 0.5) improve system-wide engagement without accuracy regression."

### Success Criteria (Ranked by Priority)

#### Criterion 2A: Accuracy Hold (CRITICAL - Gate Failure Criterion)
```
Metric: Application Accuracy (% of responses user confirms helpful)

Success Threshold: ≥70% maintained, no regression >5pp
  Phase 1 Baseline (from Gate 1): ~70%
  Acceptable drift: -5pp (70% → 65%)
  CRITICAL FAILURE: <65% (beyond tolerance)

Logic:
  If application_accuracy_phase1 < 0.65:
    IMMEDIATE ROLLBACK (do not pass go, do not collect $200)
    Consulting-tone made answers worse
  Else if application_accuracy_phase1 < 0.70:
    PASS but INVESTIGATE (drifted but within tolerance)
  Else:
    PASS with CONFIDENCE (accuracy held)
```

**Why this is CRITICAL:**
- Single most important metric
- If we sacrifice accuracy for engagement, we've failed
- Rollback is automatic if accuracy <65%

**Measurement:**
```python
# Langfuse: All queries (system-wide, not just RCS)
application_accuracy = count(thumbs_up) / (count(thumbs_up) + count(thumbs_down))
filter: date >= [Phase1Start] AND date < [Phase1End]
```

---

#### Criterion 2B: IDK Rate Reduction (Primary)
```
Metric: IDK Rate (% of queries returning "I don't know")

Success Threshold: ≤30% (from 45.7% baseline → 30%)
  This is the main mechanism: soft gradient bridges false negatives
  Required drop: 15.7pp
  Target: 25-30%

Logic:
  If idk_rate_phase1 ≤ 0.30:
    PASS (soft gradient working)
  Elif idk_rate_phase1 ≤ 0.35:
    PARTIAL (modest improvement, but target missed)
  Else:
    FAIL (no improvement; soft gradient not helping)
```

**Why this matters:**
- Soft gradient's primary job: reduce false IDK without hurting accuracy
- If IDK drops but accuracy drops too, consult worked
- If IDK stays high, soft gradient isn't gaining much

---

#### Criterion 2C: Follow-Up Rate (Secondary Engagement)
```
Metric: Follow-Up Propensity (% of responses followed by user turn within 5 min)

Success Threshold: ≥25% (from 8% baseline, 17pp increase)
  This compounds IDK reduction + engagement lift
  Target: 25-50%

Logic:
  If followup_rate_phase1 ≥ 0.25:
    PASS (users engaging more)
  Elif followup_rate_phase1 ≥ 0.20:
    PARTIAL (some lift, but modest)
  Else:
    FAIL (no engagement lift from soft gradient)
```

**Why this matters:**
- If IDK drops but follow-up doesn't increase, we're not really helping
- Follow-up = users exploring deeper = higher stickiness
- Shows soft gradient is actually inviting user participation

---

#### Criterion 2D: Confidence Calibration (Accuracy Health Check)
```
Metric: Calibration Error (|Reported Confidence - Actual User Satisfaction|)

Success Threshold: ≤±0.08 (improved from ±0.18)
  This is the consulting-tone "honesty" metric
  Current: Confidence reports are overconfident (±0.18)
  Phase 1 should improve this (context-aware scoring)

Logic:
  If calibration_error ≤ 0.08:
    PASS (consulting-tone calibration working)
  Elif calibration_error ≤ 0.12:
    PARTIAL (improved but not perfect)
  Else:
    NEUTRAL (no improvement; but not critical)
```

**Why this matters:**
- Shows if consulting-tone confidence is actually more honest
- If calibration improves, Phase 3 (context-gating) will help further
- If calibration worsens, something broke in Phase 1 logic

**Measurement:**
```python
# Segment responses by confidence bucket
confidence_buckets = {
    "0.0-0.2": responses_in_bucket,
    "0.2-0.4": responses_in_bucket,
    "0.4-0.6": responses_in_bucket,
    "0.6-0.8": responses_in_bucket,
    "0.8-1.0": responses_in_bucket,
}

for bucket, responses in confidence_buckets.items():
    satisfaction = avg(thumbs_up for r in responses)
    bucket_midpoint = (bucket_min + bucket_max) / 2
    error = abs(bucket_midpoint - satisfaction)
    
# Mean calibration error = avg(error across all buckets)
```

---

### Decision Logic: Gate 2 Pass/Fail

```python
def gate2_decision(metrics):
    """
    Decision logic for Phase 1 → Phase 2/3 decision.
    
    metrics = {
        "application_accuracy": 0.68,     # e.g., 68% (allow 70% → 65%)
        "idk_rate": 0.28,                 # e.g., 28% (down from 45.7%)
        "followup_rate": 0.32,            # e.g., 32% (up from 8%)
        "calibration_error": 0.09,        # e.g., ±0.09 (down from ±0.18)
    }
    """
    
    # CRITICAL gate: Accuracy must be protected
    if metrics["application_accuracy"] < 0.65:
        return {
            "status": "CRITICAL FAILURE",
            "action": "IMMEDIATE ROLLBACK Phase 1",
            "reason": "Accuracy regression below 65%; consulting-tone made answers worse"
        }
    
    if 0.65 <= metrics["application_accuracy"] < 0.70:
        accuracy_status = "PARTIAL (drifted but within tolerance)"
    else:
        accuracy_status = "PASS (maintained)"
    
    # Check other gates
    idk_pass = metrics["idk_rate"] <= 0.35  # Allow some flexibility
    followup_pass = metrics["followup_rate"] >= 0.20  # Lower bar for partial pass
    
    if idk_pass and followup_pass and metrics["application_accuracy"] >= 0.65:
        return {
            "status": "PASS",
            "action": "PROCEED to Phase 2/3 decision",
            "next_step": "Determine which phase based on engagement vs accuracy improvements"
        }
    elif idk_pass and metrics["application_accuracy"] >= 0.65:
        return {
            "status": "PARTIAL PASS",
            "action": "Continue Phase 1 with extended monitoring",
            "reason": "IDK improved but follow-up modest; investigate and re-measure"
        }
    else:
        return {
            "status": "INVESTIGATE",
            "action": "Extend Phase 1 by 1 week",
            "reason": "Some metrics underperforming; check data quality and rerun"
        }
```

### Next Decision: Phase 2 vs Phase 3

Once Gate 2 passes, choose:

```python
def phase2_vs_phase3_decision(metrics, engagement_data):
    """
    After Phase 1 passes: which phase next?
    
    engagement_lift_phase1 = followup_rate_after / followup_rate_before - 1
    accuracy_improve_phase1 = (calibration_error_before - calibration_error_after) / calibration_error_before
    """
    
    engagement_lift_pct = engagement_data["engagement_lift_pct"]  # e.g., 3.0 = 300% = 8% → 24%
    accuracy_improve_pct = engagement_data["accuracy_improve_pct"]  # e.g., 0.40 = 40% better calibration
    
    # Path selection logic
    if engagement_lift_pct >= 3.0:  # 3x multiplier (8% → 24%+)
        return {
            "primary": "PHASE 2 (Consulting Questions)",
            "rationale": "Engagement lift is strong; keep momentum with more questions",
            "secondary": "Phase 3 later (if accuracy stalls)"
        }
    
    elif accuracy_improve_pct >= 0.40:  # 40%+ calibration improvement
        return {
            "primary": "PHASE 3 (Context-Gating)",
            "rationale": "Accuracy/calibration improving; double down with context awareness",
            "secondary": "Phase 2 optional enhancement"
        }
    
    elif engagement_lift_pct >= 1.5 and accuracy_improve_pct >= 0.25:
        return {
            "primary": "BOTH PHASES (Sequenced)",
            "rationale": "Both engagement and accuracy improving; run Phase 2 then Phase 3",
            "schedule": "Phase 2: Week 3, Phase 3: Week 4"
        }
    
    else:
        return {
            "primary": "CONSOLIDATE at Phase 1",
            "rationale": "Phase 1 gains are modest; Phase 2/3 ROI unclear",
            "next": "Document Phase 1 as permanent improvement; archive Phase 2/3 for future"
        }
```

### Report Template: Gate 2

```
═══════════════════════════════════════════════════════════════════
DECISION GATE 2 REPORT: Phase 1 Full-System Impact
Period: Mon 2026-08-18 to Fri 2026-08-22
Sample Size: [N total queries, M unique users across all modules]
═══════════════════════════════════════════════════════════════════

ACCURACY METRICS (CRITICAL GATE)
─────────────────────────────────
Application Accuracy (before):  70%
Application Accuracy (after):   [X]%
Drift:                          [Y]pp (allow -5pp, fail <-5pp)
Status:                         [✓ PASS / ✗ CRITICAL FAILURE]

[If ✗ FAILURE: STOP HERE. Immediate rollback.]

PRIMARY GATES
─────────────
IDK Rate (before):              45.7%
IDK Rate (after):               [X]%
Target:                         ≤30%
Status:                         [✓ PASS / ◎ PARTIAL / ✗ FAIL]

Follow-Up Rate (before):        8%
Follow-Up Rate (after):         [X]%
Target:                         ≥25%
Status:                         [✓ PASS / ◎ PARTIAL / ✗ FAIL]

SUPPORTING METRICS
───────────────────
Calibration Error (before):     ±0.18
Calibration Error (after):      ±[X]
Target:                         ±0.08
Status:                         [✓ IMPROVED / ◎ NEUTRAL]

Avg Conversation Depth (before): 1.2 turns
Avg Conversation Depth (after):  [X] turns
Target:                         ≥2.0 turns
Status:                         [✓ GOOD / ◎ NEUTRAL]

OVERALL ASSESSMENT
───────────────────
Gate 2 Result:  [PASS / PARTIAL / INVESTIGATE]
Decision:       [PHASE 2 vs 3 / Continue Phase 1 / Investigate]

PHASE 2 vs 3 ANALYSIS
─────────────────────
Engagement Lift:    [X]% (Phase 1 follow-up multiplier)
Accuracy Improvement: [Y]% (Phase 1 calibration improvement)
Recommendation:     [Phase 2 (engagement) / Phase 3 (accuracy) / Both]

NEXT PHASE KICKOFF
───────────────────
Phase to implement:  [Phase 2 or 3]
Start date:          [Week 3 Mon]
Target metrics:      [List from chosen phase]

Approved By: [Name]
Date: [Date]
═══════════════════════════════════════════════════════════════════
```

---

## GATE 3: Phase 2/3 → Consolidation (Week 4)

### Timing
**Measurement Period:** Mon Week 3/4 - Fri Week 4 (14 days)  
**Decision Date:** Friday EOD Week 4  
**Decision Makers:** PM + Tech Lead

### Hypothesis
Depending on what was chosen:
- **Phase 2:** "Consulting questions for low-confidence queries drive deeper engagement without accuracy loss"
- **Phase 3:** "Context-gating improves confidence calibration and prevents wrong-direction answers"

### Success Criteria

#### If Phase 2 Chosen:
```
1. Follow-Up Rate: ≥40% (doubled from Phase 1 ~25%)
2. Conversation Depth: ≥3.5 turns (up from Phase 1 ~2.5)
3. Accuracy Maintained: ≥70% (no regression)
4. Question Quality: >65% of consulting questions actually lead to answers (not abandonment)
```

#### If Phase 3 Chosen:
```
1. Calibration Error: ≤±0.04 (down from Phase 1 ±0.08)
2. False Negative Rate: <5% (IDK despite search score > 5)
3. Accuracy Improved: ≥72% (up from Phase 1 ~70%)
4. Context Tracking: >70% of users provide context info when asked
```

---

## CRITICAL DECISION PRINCIPLES

### 1. Accuracy First, Always
```
RULE: If accuracy regresses at ANY gate, STOP.
      Do not proceed. Rollback immediately.
      Engagement gains on wrong answers are worthless.
```

### 2. Measure Real User Behavior, Not Proxies
```
RULE: Measure actual engagement (follow-ups, turns) 
      not just system metrics (confidence scores).
      
      Measure actual accuracy (thumbs up/down, actual outcomes)
      not just retrieval scores.
```

### 3. Gate Each Phase on Data, Not Assumptions
```
RULE: Do not proceed to Phase N+1 based on theory.
      Only proceed on measured Phase N success.
      
      If data is ambiguous, extend Phase N by 1 week.
      If data is negative, STOP + investigate.
```

### 4. Rollback is Not Failure
```
RULE: Rollback is success if it prevents accuracy regression.
      
      If we deploy Phase 1 and accuracy drops,
      rolling back is the right decision (prevents harm).
      
      Document what went wrong and iterate.
```

---

## SUMMARY TABLE: Gate Criteria

| Gate | Primary Metrics | Success Threshold | Failure = |
|------|-----------------|-------------------|-----------|
| **Gate 1 (P0→P1)** | Engagement lift, Accuracy hold | ≥20% engagement + ≥70% accuracy | STOP |
| **Gate 2 (P1→P2/3)** | IDK rate, Follow-up rate, Accuracy hold (critical) | ≤30% IDK + ≥25% follow-up + ≥65% accuracy | ROLLBACK |
| **Gate 3 (P2/3→Consolidate)** | Phase-specific metrics | Phase 2: ≥40% follow-up; Phase 3: ≤±0.04 calibration | Archive phase |

---

**Status:** Ready for implementation  
**Use with:** CONSULTING_TONE_OPTIMAL_IMPLEMENTATION_SEQUENCE.md (full details)
