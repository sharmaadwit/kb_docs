# Strategic Roadmap: Consulting-Tone Shift & P1/P2 Reassessment
**Date:** 2026-08-11  
**Analysis:** High-effort multi-agent strategic assessment  
**Status:** Ready for decision

---

## Executive Summary

**The Current Plan (P1 → P2 → Consulting) Should Be Inverted.**

Your accuracy is already stable at 70-72%. The strategic shift from accuracy-maximization to engagement-maximization requires a different implementation sequence:

1. **Fill content gaps first (P2)** — 2 weeks, 15-20 hours
2. **Pilot consulting tone (RCS-only Phase 0)** — 1 week, with accuracy gate ≥65%
3. **Abandon original P1; adopt calibration approach** — Phase 3, embedded in consulting rollout

**Why:** 
- Original P1 (gate low-confidence to IDK) conflicts with consulting-tone engagement goal
- P2 (content coverage) is NOT superseded — consulting tone can't frame evidence that doesn't exist
- Consulting tone + P2 content can maintain 70% accuracy while driving 25-40% engagement lift
- Reframed P1 (IDK threshold calibration using post-pilot data) is still needed but becomes Phase 3

---

## Part 1: The P1 Problem — Original Design Should Be Abandoned

### What Original P1 Does
```
IF confidence >= 3.0:
  return answer
ELSE:
  return "I don't know" + log near-miss
```

**Expected impact:** +2-4pp accuracy, +5-10pp IDK rate  
**Target:** Remove low-confidence false positives

### Why Original P1 Conflicts With Consulting Tone

Your confidence formula (from `kb_answer.py:5834`) is:
```
confidence = 0.7 * query_token_overlap + 0.3 * normalized_retrieval_score
```

This measures **retrieval match quality**, not **answer applicability to user's context**. 

**Example from CONSULTING_TONE_STABILITY_RISK_ANALYSIS.md:**
- Query: "How do I configure webhooks?"
- Retrieved evidence: Comprehensive webhook article
- Confidence: 0.85 (high, queries match perfectly)
- **Actual accuracy:** 0.33 (answer only applies to 1 of 3 integration paths user might be on)

**The problem:** P1 gates on retrieval match (confidence 3.0+), not on contextual correctness. It would increase IDK using a metric that doesn't correlate with actual answer quality.

### What Consulting Tone Does Instead

Consulting tone reframes medium-confidence answers (0.40-0.79 confidence band):

| Confidence Band | Old Behavior (P1) | Consulting Behavior |
|---|---|---|
| ≥0.80 | Return full answer | Return full answer (unchanged) |
| 0.60-0.79 | Return full answer (sometimes wrong) | Return answer + context check |
| 0.40-0.59 | P1 would return IDK | Consulting returns diagnostic question |
| <0.40 | Return IDK | Return IDK |

**Example:** Instead of IDK for a medium-confidence webhook answer, consulting says:
> "I can help with webhook configuration, but it depends on your setup. Are you using: (A) Standalone RCS integration, (B) Gupshup's native webhooks, or (C) Custom HTTP endpoints? I'll give you the exact steps for your case."

This converts a false IDK into an engagement opportunity. P1 gates those directly to IDK — opposite of what you want.

### Verdict on Original P1

**Do NOT implement as designed.** It would:
1. Increase IDK rate in the exact band consulting tone wants to convert to follow-up conversations
2. Gate on retrieval match instead of actual answer correctness (wrong signal)
3. Create recalibration debt when consulting tone ships (you'd have to reset the threshold)

**However, the underlying idea (systematic IDK threshold) is still needed — just reframed.**

---

## Part 2: P2 (Content Gaps) is NOT Superseded

### What P2 Does
- Writes 3 new KB articles: WhatsApp error codes, Bot Studio patterns, multi-channel strategy
- Creates 24-36 new chunks with 8-12 chunks per article
- Tests against 50 synthetic queries
- Expected impact: +5-10pp accuracy

### Why Consulting Tone Can't Replace P2

Consulting tone improves **framing** of existing answers. P2 solves **retrieval coverage** — fundamentally different problems.

**Evidence:** Your own CONSULTING_TONE_STABILITY_RISK_ANALYSIS.md documents that consulting questions (diagnostic paths) still need evidence to frame:
> "Consulting question → resolution rate ≥50% is a success criterion. If consulting diagnostic fails to route to usable content, users hit cascading IDKs and churn faster than single-turn IDK."

### Multi-Turn As Partial Substitute?

Could multi-turn conversations make P2 unnecessary? **No, with high risk:**

- **Multi-turn helps with ambiguity:** User asks vague question, clarification narrows to covered topic. ✓
- **Multi-turn does NOT help with missing content:** User asks follow-up on WhatsApp error codes, KB still has no error code documentation. ✗

Users who hit IDK after diagnostic question (no content to frame) churn faster than users who hit single-turn IDK. They've already invested cognitive load.

### Resource ROI

| Initiative | Hours | Expected Impact | ROI per Hour |
|---|---|---|---|
| P2 (content gaps) | 15-20 | +5-10pp accuracy | 0.5pp/hour (accuracy) |
| Consulting tone | 40-60 | +25-40% engagement | Unknown for accuracy |
| Reframed P1 | 5-10 | Hold ≥70% accuracy | Critical for stability |

P2's accuracy ROI is highest. Consulting tone's engagement ROI is highest. They're complementary, not substitutes.

### Verdict on P2

**P2 Must NOT Be Skipped.** Content gaps remain gaps regardless of framing. The only scenario for deprioritizing P2 is if multi-turn data shows users naturally pivot gap queries to covered topics — requires empirical evidence, not assumptions.

---

## Part 3: Reframed P1 — Calibration Instead of Gating

### The Right Version of P1

Instead of binary "gate at threshold," P1 should be:
> "What is the optimal confidence threshold to return IDK vs. ask a consulting question vs. return a full answer?"

This threshold can ONLY be calibrated using post-consulting-tone data because consulting tone changes what "medium confidence" means.

### When To Do Reframed P1

**Phase 3 (Week 3-4 of rollout), not Phase 1.**

After the RCS consulting pilot, you'll have data on:
- Which confidence bands convert to follow-up (consulting diagnostic is useful)
- Which confidence bands lead to abandonment (consulting question was friction)
- Actual accuracy by confidence band (is high confidence = high accuracy? does it vary by module?)

**Only with that data can you set the true IDK floor.**

### What Reframed P1 Actually Measures

Using post-pilot data:
```
For each confidence band (e.g., 0.40-0.59):
  - What % of answers satisfied users? (satisfaction)
  - What % led to follow-up? (engagement)
  - What % led to abandonment? (churn)
  - Is confidence correlated with satisfaction? (r > 0.70?)
  - False negative rate: queries that IDK but KB has relevant content?
```

**Decision rule:** "Set IDK threshold so that false negative rate < 5% while maintaining satisfaction ≥70%."

This is very different from original P1's "increase IDK to +5-10pp" target.

---

## Part 4: Recommended Implementation Sequence

### Current Assumption (Likely Suboptimal)
```
P1 (confidence gating) → P2 (content gaps) → Consulting tone (RCS pilot)
Timeline: 3-4 weeks, compound complexity, uncertain outcome
```

### Recommended Sequence (Lower Risk, Faster Signal)
```
Phase 0: P2 (content gaps) [Week 1-2]
Phase 1: Consulting tone (RCS pilot) [Week 2-3]
Phase 2: Scale consulting (other modules) [Week 3-4]
Phase 3: Reframed P1 (calibration) [Week 4-5]
```

### Why This Order

**P2 First (2 weeks, 15-20 hours):**
- Lowest complexity, highest accuracy ROI
- Isolates variables for consulting pilot (better content = better signal on whether consulting framing works)
- Decouples from consulting-tone uncertainty
- If consulting tone shows accuracy regression, you already have better content as a mitigation

**Consulting Tone on RCS (1 week):**
- Your Phase 0 plan is correct — RCS is new module, low breakage risk
- Measure: engagement lift ≥20%, accuracy ≥65%
- Generate real data on confidence → satisfaction correlation
- Identify which consulting questions convert, which are friction

**Scale Consulting (1-2 weeks):**
- Expand to high-volume modules (Channels, WhatsApp, Bot Studio)
- Watch accuracy by module — if any drops >5pp, revert that module
- Compile accuracy-by-confidence-band data across all modules

**Reframed P1 Calibration (Phase 3-4):**
- With full dataset, compute optimal IDK threshold
- Answer: "At what confidence should we give up and return IDK?"
- Implement as a systematic rule (e.g., "if confidence < 0.25 AND no consulting question helps, return IDK")
- This is not a standalone phase, but an analytical exercise embedded in consulting rollout

---

## Part 5: Accuracy Stability — Can You Hit 70%?

### Baseline Assessment
Your current accuracy is **70-72%** (depends on module). You're already stable.

### Risk Scenarios

**Scenario A: Consulting tone alone (no P2, no reframed P1)**
- Risk: "It depends" framing generates vague answers that score as incorrect
- Consultant tone would drop confidence 0.12-0.18 for unknown-context queries
- Estimated accuracy: 55-60% for high-ambiguity topics, 65-70% overall
- **Verdict:** Does NOT hold 70%. Not recommended.

**Scenario B: Consulting + P2 (no reframed P1)**
- Better retrieval evidence means consulting answers have actual content to frame
- Medium-confidence band shrinks because more content = more specific answers
- Estimated accuracy: 68-72% overall
- **Verdict:** Probably holds 70%, but risky. Depends on P2 article quality.

**Scenario C: Consulting + P2 + Reframed P1 (Full Stack)**
- P2 fills content gaps (retrieval improvement)
- Consulting frames medium-confidence answers (presentation improvement)
- Reframed P1 sets IDK threshold to minimize false negatives (safety valve)
- Estimated accuracy: 71-75% overall
- **Verdict:** Holds 70%+ with high confidence. Recommended.

### Which Scenario For You?

**Go with Scenario B short-term, Scenario C long-term:**

1. **Weeks 1-2:** Implement P2 (content gaps)
2. **Weeks 2-4:** Pilot consulting tone on RCS; measure accuracy
3. **Weeks 4-5:** If accuracy ≥65% on RCS pilot, scale to other modules
4. **Weeks 5-6:** Implement reframed P1 calibration using full dataset

This sequence lets you prove each step before adding complexity. If consulting alone drops accuracy below 65%, P2 content becomes critical (you haven't wasted time on P1). If consulting + P2 holds accuracy, reframed P1 is a refinement, not a rescue.

---

## Part 6: Metrics & Rollback Triggers

### Success Criteria (Consulting Pilot Phase)

| Metric | Target | Why |
|---|---|---|
| Follow-up rate (multi-turn %) | ≥9.6% | 20% lift from 8% baseline (engagement proof) |
| Accuracy (RCS module) | ≥65% | ≤5pp regression acceptable for pilot |
| Consulting question → resolution | ≥50% | Diagnostic questions must be useful, not friction |
| Module routing accuracy | ≥90% | Must maintain routing integrity |
| Segment A satisfaction (quick-answer users) | No drop >5pp | Some users prefer definitive answers |

### Rollback Triggers (Automatic Revert)

| Trigger | Action | Rationale |
|---|---|---|
| Accuracy drops >5pp in any module | Revert that module; investigate | Accuracy floor of 70% is non-negotiable |
| Consulting question conversion <35% | Revert to soft gradient + follow-ups | Questions are creating friction, not value |
| Module routing accuracy <90% | Immediate revert; fix routing first | Routing is prerequisite for consulting |
| IDK rate rises (not falls) post-consulting | Revert; threshold miscalibrated | Consulting should reduce IDK, not increase |
| Segment A satisfaction drops >5pp | Apply consulting only to Segment B | Some users need definitive answers |

### Daily Monitoring Dashboard

```
Real-time (per hour):
- Answer rate (%) — should hold ≥60%
- IDK rate (%) — should drop 2-5pp week 1, then hold
- Multi-turn % — should rise from 8% → 10-12%
- Avg time per user (seconds) — should rise 15-30%

Weekly:
- Module accuracy by topic (WhatsApp, Bot Studio, Channels, etc.)
- Confidence → satisfaction correlation (r value)
- Follow-up question effectiveness (% that resolve in follow-up)
- User satisfaction scores (thumbs up/down ratio)

Gate before next phase:
- No module drops >5pp accuracy
- Multi-turn engagement ≥20% lift from baseline
- Confidence scores correlate with satisfaction (r ≥0.60)
```

---

## Part 7: Decision Matrix — What To Do Now

### Decision 1: Implement Original P1 (Confidence Gating)?
**Answer: NO. Abandon as designed.**
- Conflicts with consulting-tone engagement goal
- Gates on wrong signal (retrieval match, not contextual correctness)
- Would increase IDK in the exact band consulting tone wants to convert
- Creates recalibration debt when consulting ships

### Decision 2: Implement P2 (Content Gaps)?
**Answer: YES. Do it first, before consulting pilot.**
- Not superseded by consulting tone
- Highest accuracy ROI per hour (0.5pp/hour)
- Isolates variables for consulting pilot
- Can't be recovered by follow-up conversations if content doesn't exist

### Decision 3: Implement Consulting Tone?
**Answer: YES. Pilot on RCS only, measure carefully.**
- Gate on engagement ≥20% lift AND accuracy ≥65%
- Roll out to other modules only if pilot meets gates
- Embed reframed P1 calibration work in Phase 3

### Decision 4: Implement Reframed P1 (Threshold Calibration)?
**Answer: YES, but as Phase 3, not Phase 1.**
- Only implement after consulting pilot has real data
- Use post-pilot accuracy-by-confidence-band distribution
- Calibrate IDK threshold to minimize false negatives (<5%)
- This is analytical work embedded in Phase 3, not a standalone initiative

---

## Part 8: Timeline

```
WEEK 1-2: P2 Implementation (Content Gaps)
├─ Write 3 KB articles (WhatsApp errors, Bot Studio, multi-channel)
├─ Generate ~30 chunks at 620 chars avg
├─ Test against 50 synthetic queries
├─ Target: answer coverage +5-10pp for gap topics
└─ Gate: All 3 articles verified before moving to Phase 1

WEEK 2-3: Consulting Pilot Phase (RCS Module Only)
├─ Implement consulting-tone answer generation on RCS queries only
├─ A/B test: 50% RCS traffic on consulting, 50% control
├─ Measure: engagement lift, accuracy hold, confidence correlation
├─ Daily monitoring: answer rate, IDK rate, multi-turn %, satisfaction
└─ Gate: engagement ≥20% AND accuracy ≥65% before Phase 2

WEEK 3-4: Scale Consulting (High-Volume Modules)
├─ Expand to Channels, WhatsApp, Bot Studio
├─ Monitor accuracy by module (auto-revert if >5pp drop)
├─ Compile full dataset: confidence-by-satisfaction, consulting-question-conversion
└─ Gate: All modules ≥65% accuracy before Phase 3

WEEK 4-5: Reframed P1 Calibration (Phase 3)
├─ Analyze confidence bands post-consulting
├─ Compute optimal IDK threshold (minimize false negatives <5%)
├─ Implement systematic rule (e.g., "confidence <0.25 AND no consulting help → IDK")
├─ Deploy phase 3 settings (new IDK threshold)
└─ Target: Hold accuracy ≥70%, maintain engagement lift

POST-WEEK 5: Monitor & Optimize
├─ Weekly accuracy by module
├─ Monthly engagement metrics (multi-turn %, avg time/user, satisfaction)
├─ Continuous calibration of consulting-question effectiveness
└─ Backlog: advanced consulting patterns (context memory, multi-step guidance)
```

---

## Part 9: Summary Table — Do P1/P2 Still Make Sense?

| Initiative | Original Plan | Recommended | Rationale |
|---|---|---|---|
| **P1 (Confidence Gating)** | Do first | Abandon; reframe as Phase 3 calibration | Original design gates on wrong signal; conflicts with consulting engagement |
| **P2 (Content Gaps)** | Do second | Do first (Week 1-2) | Highest accuracy ROI; isolates variables for consulting pilot; not superseded |
| **Consulting Tone** | Do third | Do second as RCS pilot (Week 2-3) | Your existing Phase 0 plan is correct; measure carefully before scaling |
| **Reframed P1** | N/A | Do third (Week 4-5) | Embed as analytical phase using post-pilot data; unnecessary before consulting ships |

**Net Change:** Swap P1 and P2. Reframe P1 as Phase 3 calibration.

---

## Success Looks Like

✅ **Week 2 (P2 complete):**
- 3 KB articles written and tested
- WhatsApp error, Bot Studio, multi-channel answer coverage +7-10pp
- Ready for consulting pilot with better retrieval baseline

✅ **Week 4 (Consulting pilot + scale):**
- RCS module: +25% engagement lift, accuracy ≥65%
- Consulting questions converting ≥50% of the time
- Expanded to 3 high-volume modules, all ≥65% accuracy
- Confidence-by-satisfaction correlation ≥0.60

✅ **Week 6 (Full stack):**
- All modules at ≥70% accuracy
- Multi-turn conversations up 25-40%
- Avg time per user up 30-45%
- Reframed P1 threshold calibrated, IDK false negative rate <5%

---

## Failure Modes & Recovery

| If This Happens | Then Do This |
|---|---|
| P2 articles don't lift accuracy | Revert Phase 1; diagnose retrieval problem (is it coverage or ranking?) |
| Consulting pilot drops accuracy >5pp | Revert RCS module; inspect where confidence → satisfaction breaks; refine consulting questions |
| Consulting questions convert <35% | Stop question-based routing; stay in soft-gradient mode with follow-up buttons instead |
| Multi-turn engagement doesn't improve | Consulting questions may be creating friction; pivot to simpler follow-up patterns |
| Segment A satisfaction drops | Consulting tone only for Segment B; keep problem-solution for users who prefer definitive answers |

---

## Recommendation: PROCEED

**Implement the recommended sequence (P2 → Consulting → Reframed P1) over the original plan.**

This sequence:
1. ✅ Fills content gaps with highest accuracy ROI first
2. ✅ Pilots consulting tone safely on new RCS module with measurement gates
3. ✅ Abandons original P1 design (wrong signal, wrong timing)
4. ✅ Adopts reframed P1 as Phase 3 using real post-pilot data
5. ✅ Maintains ≥70% accuracy floor while driving 25-40% engagement lift
6. ✅ Enables multi-turn conversations to drive down average time per user

**Timeline:** 5-6 weeks to full deployment  
**Risk:** Low (each phase gates before next; rollback triggers defined)  
**Engagement potential:** 25-40% multi-turn lift + 30-45% time-per-user increase

---

**Prepared by:** Strategic Analysis Agent + High-Effort Consulting-Tone Pivot Workflow  
**Date:** 2026-08-11  
**Next Step:** Approve roadmap → Begin P2 implementation (Week 1)
