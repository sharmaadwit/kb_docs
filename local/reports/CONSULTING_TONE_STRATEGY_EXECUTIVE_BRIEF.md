# Consulting-Tone Implementation: Executive Brief
## Strategic Framework for Phased Rollout with Quantitative Gates

**Prepared for:** Project stakeholders, PM, Tech Lead  
**Date:** 2026-08-11  
**Status:** Ready for execution  

---

## THE QUESTION

**Can we improve KB answer engagement without sacrificing accuracy by adopting a "consulting tone"?**

This means:
- Instead of "Here's the answer, take it or leave it" (problem-solution)
- Try "Let me understand your situation first" (consulting)

**Our answer:** Maybe. But we need to measure it carefully before going system-wide.

---

## THE STRATEGY: 4-Phase Gated Approach

### Why This Approach?

**Risk:** Consulting tone could hurt accuracy if misimplemented
**Opportunity:** Could drive 3-4x engagement multiplier if it works
**Solution:** Test on 1 module first (RCS), measure rigorously, gate each phase on real data

### Timeline: 4 Weeks

```
Week 1: Phase 0 (RCS-only MVP)
Week 1 EOD: Decision Gate 1 (go/no-go Phase 1?)
Week 2: Phase 1 (Soft gradient system-wide) — IF Gate 1 passes
Week 2 EOD: Decision Gate 2 (Phase 2 vs 3 vs consolidate?)
Week 3-4: Phase 2 OR Phase 3 — IF Gate 2 passes
Week 4 EOD: Final consolidation decision
```

---

## PHASE 0: The MVP (Week 1, RCS Only)

### What We're Doing
Implement consulting-tone answer generation for **RCS module only** (1 of 6 modules).

Example:
```
OLD (Problem-Solution):
User: "How do I optimize RCS for mobile?"
System: "Use rich cards with images. Test on Android and iOS."
(User gets answer, conversation ends, 1 turn)

NEW (Consulting-Tone):
User: "How do I optimize RCS for mobile?"
System: "Great question—optimization depends on your goal. Are you optimizing for 
engagement rate (use carousels), conversion (use buttons), or delivery speed (use text)?
Let me give you the right approach..."
(User refines intent, system gives targeted answer, 3-5 turns)
```

### Why RCS?
- **Isolated:** RCS is self-contained (no dependencies on other modules)
- **Volume:** 18% of all queries (meaningful signal in 1 week)
- **Pre-tested:** RCS consulting questions already validated in RCS_CONSULTING_QUESTIONS_TEST.md
- **Rollback:** If it fails, revert single module (not entire system)

### Success Metrics (Measure in Week 1)

| Metric | Baseline | Target | Why |
|--------|----------|--------|-----|
| **Engagement Lift** | Follow-ups: 8% of responses | ≥9.6% (20% relative lift) | Shows users are more interested |
| **Accuracy Hold** | Application accuracy: 70% | ≥65% (max -5pp drift) | Ensure we're not making wrong answers |
| **IDK Reduction** | IDK rate: 45.7% | ≤40% | Fewer false "I don't know" responses |

### Decision Gate 1 (Friday Week 1)

```
IF engagement_lift ≥20% AND accuracy ≥65% THEN
  ✓ PROCEED to Phase 1 (apply soft gradient system-wide)

ELIF engagement_lift ≥15% AND accuracy ≥65% THEN
  ◐ PROCEED TO PHASE 1 WITH EXTENDED MONITORING
  (Marginal signal; watch closely)

ELSE
  ✗ STOP consulting-tone project
  (No engagement signal or accuracy regression)
```

**Key Point:** We don't proceed unless data supports it.

---

## PHASE 1: Soft Gradient (Week 2, System-Wide) — IF Gate 1 Passes

### What We're Doing
Replace binary confidence threshold (0.5 = answer or IDK) with 4 graduated tiers:

```
Confidence 0.80+  → Full answer (high confidence)
Confidence 0.60-0.79  → Answer + context check (medium confidence)
Confidence 0.40-0.59  → Consulting question (low confidence, but answerable)
Confidence <0.40  → "I don't know" (genuinely lost)
```

### Why Soft Gradient?
Currently, we have a hard boundary:
- Confidence 0.49 → "I don't know" (user frustrated, conversation ends, 8% satisfaction)
- Confidence 0.51 → Answer (user gets it, conversation may continue, 75% satisfaction)

This is wasteful. For the 0.40-0.59 band, we should *engage the user* instead of dismissing them:
- Ask "Help me understand: are you looking for [use case A] or [use case B]?"
- User clarifies
- We give better-targeted answer
- Result: user more invested, better satisfaction, longer conversation

### Success Metrics (Measure in Week 2)

| Metric | Phase 0 Baseline | Phase 1 Target | Why |
|--------|------------------|-----------------|-----|
| **IDK Rate** | 45.7% | ≤30% | Soft gradient bridges false negatives |
| **Follow-Up Rate** | 8% (from Phase 0) | ≥25% | Users asking follow-ups = engagement |
| **Conversation Depth** | 1.2 turns | ≥2.0 turns | Longer conversations = stickiness |
| **Application Accuracy** | 70% | ≥65% (CRITICAL) | No regression |
| **Calibration Error** | ±0.18 | ≤±0.08 | Confidence scores more honest |

### Decision Gate 2 (Friday Week 2)

```
CRITICAL CHECK: Accuracy ≥65%?
  If NO → ROLLBACK Phase 1 immediately (accuracy regression)
  If YES → Continue to next check

IF all other targets met THEN
  ✓ PROCEED to Phase 2 or 3 (decide based on engagement vs accuracy gains)

ELIF IDK ≤35% AND follow-up ≥20% THEN
  ◐ CONTINUE PHASE 1 WITH EXTENDED MONITORING
  (Some targets hit, others close; investigate and recheck)

ELSE
  ⚠ EXTEND PHASE 1 BY 1 WEEK
  (Data unclear; more time needed)
```

---

## PHASE 2 vs 3: The Branching Decision (Week 2 EOD)

### Phase 2: Consulting Questions
**What:** For low-confidence queries, ask diagnostic questions instead of IDK
**Example:** "Best practices for RCS" → "Are you optimizing for engagement, conversion, or delivery?"
**Target:** 40-50% follow-up rate, 4-6 turn conversations
**Trade-off:** Requires more user input; slower first response

### Phase 3: Context-Gating
**What:** Track user context (tech level, use case, scale); adjust confidence based on fit
**Example:** Same webhook question, but know user is beginner → simpler answer; expert user → advanced patterns
**Target:** 80%+ confidence calibration, +25% accuracy on ambiguous queries
**Trade-off:** Requires context tracking across conversation

### Decision Logic

```
IF engagement_lift_phase1 ≥ 3.0x (8% → 24%+) THEN
  → PHASE 2 (users love being asked; double down)

ELIF calibration_improved_phase1 ≥ 40% THEN
  → PHASE 3 (context-gating is the lever; use it)

ELIF both positive THEN
  → BOTH PHASES (Phase 2 week 3, Phase 3 week 4)

ELSE
  → CONSOLIDATE at Phase 1 (modest gains; skip 2 & 3)
```

---

## CRITICAL SAFETY RAILS

### 1. Accuracy Always Comes First
**Rule:** If accuracy drops >5pp at any gate, we **rollback immediately**.

Engagement gains on wrong answers are worthless. We don't trade accuracy for engagement.

### 2. Measure Real Behavior, Not Proxies
**We measure:**
- Actual follow-ups (users coming back within 5 min)
- Actual satisfaction (thumbs up/down from users)
- Actual outcomes (did user say "thanks, that worked"?)

**We don't measure:**
- Confidence scores (proxy, not reality)
- Retrieval scores (doesn't mean answer is applicable)
- System metrics (doesn't mean users are happy)

### 3. No Sunk-Cost Fallacy
**If Phase 0 fails:** We stop. No "let's try harder" or "let's skip to Phase 1."
**If Phase 1 shows regression:** We rollback. No "but engagement was up."

Data decides. Not assumptions.

---

## EXPECTED OUTCOMES (If All Gates Pass)

### By End of Week 2 (Phase 1)
- **IDK rate:** 45.7% → 25-30%
- **Follow-up rate:** 8% → 25-40%
- **Conversation depth:** 1.2 → 2.5 turns
- **Satisfaction (overall):** 44.7% → 60-65%

### By End of Week 4 (Phase 2 or 3)
- **IDK rate:** 25-30% → 12-20%
- **Follow-up rate:** 25-40% → 40-60%
- **Conversation depth:** 2.5 → 4-6 turns
- **Application accuracy:** ≥75% (improved from 70%)
- **Repeat user rate:** 12% → 30%+

### Long-Term Impact
- Users engage 3-4x longer per session
- More questions lead to better answers (better context)
- Higher repeat rate (users trust we'll help)
- Calibration improves (we're more honest about what we know)

---

## THE DECISION TREE (For Quick Reference)

```
START: Phase 0 (RCS-only, 1 week)
  ↓
  [Measure engagement + accuracy]
  ↓
GATE 1: engagement ≥20% AND accuracy hold?
  ├─ YES → Phase 1 (system-wide)
  ├─ MAYBE → Phase 1 with monitoring
  └─ NO → STOP + investigate
         (Why didn't consulting-tone work?)

(If Phase 1 proceeds)
  ↓
  [Measure IDK drop, follow-up increase]
  ↓
GATE 2: IDK ≤30% AND follow-up ≥25% AND accuracy ≥65%?
  ├─ YES → Choose Phase 2 or 3
  ├─ PARTIAL → Extend Phase 1 + recheck
  └─ CRITICAL (accuracy <65%) → ROLLBACK Phase 1

(If Phase 2 or 3 proceeds)
  ↓
  [Measure phase-specific metrics]
  ↓
FINAL: Consolidate into standard answer generation
  OR Archive for future iteration
```

---

## RESOURCE REQUIREMENTS

### Engineering
- **Phase 0:** 1 engineer, 3-4 days (RCS consulting-tone + feature flag)
- **Phase 1:** 1 engineer, 2-3 days (confidence tiers + routing logic)
- **Phase 2 or 3:** 1 engineer, 4-5 days (consulting Qs or context-gating)
- **Total:** ~10-15 engineer-days over 4 weeks

### Analytics
- **Data collection:** Continuous (automated Langfuse tracking)
- **Decision reports:** End of Week 1, 2, 4 (6-8 hours each)
- **Total:** ~24-30 analytics-hours over 4 weeks

### QA/Testing
- **Regression testing:** Phase 0, 1, 2/3 each (2-3 days per phase)
- **Accuracy spot checks:** Manual review of 50-100 responses per phase
- **Total:** ~8-12 QA-days over 4 weeks

### PM/Leadership
- **Decision gates:** Friday decisions (2-3 hours each × 4 gates)
- **Stakeholder communication:** Weekly updates
- **Total:** ~10-15 hours over 4 weeks

---

## RISKS & MITIGATION

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Accuracy regression** | Customers get wrong answers | Gate 2 explicitly checks accuracy; rollback if <65% |
| **Users frustrate on consulting Qs** | Abandonment after questions | Only ask on genuinely ambiguous queries; provide answer + question together |
| **Confidence scores drop** | Looks like regression (but isn't) | Document that lower confidence is *more honest*; track calibration error (primary metric) |
| **RCS-only test shows no signal** | Wasted week 1 | If lift <15%, we stop (no sunk cost); iteration for week 2 |
| **Langfuse data incomplete** | Can't measure properly | Add validation; alert if >5% of responses missing data; reprocess if needed |

---

## APPROVAL CHECKLIST

Before proceeding, confirm:

- [ ] **Data infrastructure ready:** Langfuse tracking for engagement + accuracy metrics
- [ ] **Team aligned:** PM, Tech Lead, Analytics, QA all understand phases + gates
- [ ] **Feature flags prepared:** CONSULTING_TONE_RCS_ENABLED, CONSULTING_TONE_PHASE1_ENABLED
- [ ] **Rollback plan documented:** How to revert each phase if needed
- [ ] **Measurement scripts written:** Scripts to calculate engagement_lift, accuracy_hold, etc.
- [ ] **Stakeholder buy-in:** Leadership understands we may stop at Gate 1 or 2

---

## NEXT STEPS

### Immediate (This Week)
1. **Approval:** Stakeholders review + approve this strategy
2. **Setup:** Create Langfuse dashboard for Phase 0 metrics
3. **Code:** Implement _compose_answer_consulting_rcs() + feature flag
4. **Testing:** Local testing of consulting-tone on 10 RCS queries

### Week 1 (Phase 0)
1. **Deploy:** Phase 0 to staging (Thu), then production (10% traffic Fri)
2. **Monitor:** Langfuse tracking + no critical errors
3. **Scale:** 100% RCS traffic Mon
4. **Measure:** Full week of engagement data (Tue-Fri)

### End of Week 1 (Decision Gate 1)
1. **Report:** Generate Phase 0 impact (engagement_lift, accuracy_hold, IDK_rate)
2. **Decide:** Proceed to Phase 1? (Yes/Maybe/No)
3. **Communicate:** Message to stakeholders

### Week 2 (Phase 1, Conditional)
1. **Implement:** Soft gradient confidence tiers (if Gate 1 passed)
2. **Deploy:** Phase 1 to production (Wed)
3. **Measure:** Full week of system-wide data

### End of Week 2 (Decision Gate 2)
1. **Report:** Phase 1 full-system impact
2. **Decide:** Phase 2 vs 3 vs Consolidate?
3. **Proceed:** Week 3-4 implementation (if applicable)

---

## DOCUMENT MAP

For more details, refer to:

| Document | Purpose |
|----------|---------|
| **CONSULTING_TONE_OPTIMAL_IMPLEMENTATION_SEQUENCE.md** | Full technical roadmap with code examples + testing framework |
| **DECISION_TREE_CONSULTING_TONE.md** | Visual decision tree + quick metrics reference |
| **CONSULTING_TONE_PHASE_GATING_LOGIC.md** | Quantitative decision criteria + report templates |
| **consulting_tone_impact_analysis.md** | Theory: why consulting-tone should work (accuracy + engagement) |
| **RCS_CONSULTING_QUESTIONS_TEST.md** | Pre-testing results: RCS KB ready for consulting-tone |

---

## SUCCESS DEFINITION

This strategy succeeds if **any one of these is true at the end of Week 4:**

1. **Phase 1 consolidated:** Soft gradient stays as permanent system improvement (IDK ≤30%, accuracy ≥70%)
2. **Phase 2 consolidated:** Consulting questions drive engagement (follow-up ≥40%, accuracy ≥70%)
3. **Phase 3 consolidated:** Context-gating improves accuracy (calibration ±0.04, accuracy ≥75%)
4. **Learnings documented:** Even if we stop at Gate 1 or 2, we document why and iterate later

We don't need all phases to pass. We need *one working lever* that improves engagement without hurting accuracy.

---

## EXECUTIVE SUMMARY

**Can consulting tone improve engagement without sacrificing accuracy?**

**Our answer:** We don't know. But we have a disciplined plan to find out.

**Phase 0 (Week 1):** Test on RCS only (lowest risk)  
**Gate 1 (Fri Week 1):** Measure engagement + accuracy  
**Phase 1 (Week 2):** Scale if Gate 1 passes  
**Gate 2 (Fri Week 2):** Decide Phase 2 vs 3 vs stop  
**Phase 2/3 (Week 3-4):** Conditional based on data  

**Safety:** Accuracy always comes first. Rollback at any sign of regression.

**Investment:** ~10-15 engineer-days, 24-30 analytics-hours, 8-12 QA-days over 4 weeks

**Upside:** 3-4x engagement multiplier, 20-30% repeat user increase, if all phases pass

**Downside:** We learn what doesn't work and iterate; no permanent damage

---

**Status:** Ready for approval and execution  
**Owner:** [PM Name]  
**Contact:** [Lead Engineer Email]

---

*This document is a strategic framework, not a guarantee. Success depends on data at each gate. We follow the data, not assumptions.*
