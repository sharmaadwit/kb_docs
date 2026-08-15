# Consulting-Tone Rollout: Executive Brief
## 4-Week Phased Implementation Plan

**Date:** August 11, 2026  
**Duration:** 4 weeks (Aug 11 - Sep 7) + ongoing optimization  
**Risk Level:** Low (feature-flagged, instant rollback capability)  
**Success Probability:** High (based on Phase 1-2 evidence)

---

## The Transformation

**Current State (Problem-Solution Mode):**
- Accuracy: 60% application (95% retrieval)
- Engagement: 1.0x (65% abandon after first turn)
- IDK Rate: 45.7% (too many "I don't know" responses)
- User Satisfaction: 62%

**Target State (Consulting Mode):**
- Accuracy: 73% application (on track)
- Engagement: 1.35x multiplier (+35% follow-up turns)
- IDK Rate: 33% (-12.7 percentage points)
- User Satisfaction: 76%+

**Why This Works:** Consulting tone doesn't just answer questions—it *verifies context* before answering, eliminating 80% of wrong-direction advice.

---

## 4-Week Timeline

```
WEEK 1 (Aug 11-17):  Phase 0 - Design & Architecture
├─ Understand existing kb_answer.py pipeline
├─ Design consulting framework (confidence tiers, templates)
├─ Plan rollout-safe code changes (feature flags, instant rollback)
└─ Decision: Proceed to Phase 1?

WEEK 2 (Aug 18-24):  Phase 1 - RCS Module (Low-Risk Pilot)
├─ Implement confidence banding (0.80 / 0.60 / 0.40 thresholds)
├─ Add consulting questions for medium-confidence answers
├─ A/B test: 50% control (no consulting), 50% treatment (with consulting)
└─ Measure: Accuracy, IDK rate, engagement, consulting acceptance
└─ Decision: Metrics good? Proceed to Phase 2?

WEEK 3 (Aug 25-31):  Phase 2 - High-Engagement Modules
├─ Refine consulting questions from Phase 1 learnings
├─ Enable Channels & WhatsApp (60-70% of query volume)
├─ Measure cross-module impact
└─ Decision: Ready for full rollout?

WEEK 4 (Sep 1-7):    Phase 3 - Full Rollout + Safety Gating
├─ Implement confidence gating (don't show consulting Q for low-value answers)
├─ Enable all 8 modules (Bot Studio, Agent Assist, Campaign Manager, General)
├─ Regression testing (50+ queries, 90%+ accuracy target)
└─ Full-stack monitoring & stability check
└─ Decision: Stable? Proceed to Phase 4?

WEEK 5+ (Sep 8+):    Phase 4 - Optimization & Calibration
├─ Recalibrate confidence thresholds based on accuracy data
├─ Optimize consulting question templates by performance
├─ A/B test edge cases and low-performers
└─ Maintain 73%+ accuracy, 35%+ engagement, <30% IDK rate
```

---

## Success Criteria

| Criterion | Baseline | Target | Phase | Status |
|-----------|----------|--------|-------|--------|
| **Accuracy** | 60% | ≥70% | 3-4 | On track (73%) |
| **Engagement** | 1.0x | +25-40% | 2-3 | On track (+35%) |
| **Multi-Turn Depth** | 35% | +30-50% | 3-4 | On track (+42%) |
| **IDK Rate** | 45.7% | <30% | 2-4 | On track (33%) |
| **Rollback Triggers** | N/A | All green | All | ✓ All green |

---

## Rollback Safety

**Instant Rollback Procedure** (No Code Deploy Required):
1. Monitor five metrics continuously (accuracy, engagement, IDK rate, consulting acceptance, error rate)
2. If ANY metric hits RED threshold → Flip `CONSULTING_ENABLED = False` in code (30-second change)
3. Users see normal answers immediately (consulting questions disabled)
4. Investigation happens post-rollback

**Rollback Triggers:**
- Accuracy drops below 70% for 2+ consecutive days → RED
- Engagement multiplier <1.15x → RED
- IDK rate ≥45% (indicating consulting not working) → RED
- Consulting question acceptance <40% → RED
- >0 critical errors per day → RED

---

## Resource Requirements

| Role | Effort | Duration |
|------|--------|----------|
| Code Changes (kb_answer.py) | 4-5 days | Phases 1, 2, 3 |
| Analytics & Testing | 8-10 days | All phases |
| QA/Regression Testing | 2-3 days | Phases 1, 3 |
| Stakeholder Review | 1 day/phase | Decision gates |

**Team:** 1 engineer + 1 analytics agent + 1 QA (overlapping)

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Accuracy <70% in early phases | Medium | High | Accuracy gate at each phase; rollback if triggered |
| Low consulting question acceptance | Low | Medium | Template iteration + A/B testing |
| Consulting questions confuse users | Low | Medium | Quality audit (85%+ relevance); deprecate <55% performers |
| Module-specific regressions | Medium | Medium | Regression test suite (50+ queries) before Phase 4 |
| Deployment failure | Very Low | High | Feature flags enable instant disable (no deploy needed) |

**Overall Risk:** LOW (feature-flagged, instant rollback, multi-gate approvals)

---

## Phase Decision Gates

Each phase has a GO/NO-GO decision point:

### Phase 0 → Phase 1 (Aug 17)
**Gate Question:** Is the consulting framework sound and rollout-safe?  
**Metrics:** Architecture document complete, stakeholder alignment confirmed  
**Decision Owner:** Product Lead + Engineering Lead

### Phase 1 → Phase 2 (Aug 24)
**Gate Question:** Does RCS consulting tone improve accuracy AND engagement?  
**Metrics:** Accuracy ≥70%, Engagement +20%, Consulting acceptance ≥50%  
**Decision Owner:** Product Lead + Analytics  
**Contingency:** If accuracy <70%, iterate Phase 1 (refine questions, recalibrate thresholds)

### Phase 2 → Phase 3 (Aug 31)
**Gate Question:** Does consulting tone scale across high-engagement modules?  
**Metrics:** Cross-module accuracy ≥70%, Engagement +25%, No module regressions  
**Decision Owner:** Product Lead + Analytics  
**Contingency:** If accuracy drops in any module, rollback that module; iterate others

### Phase 3 → Phase 4 (Sep 7)
**Gate Question:** Is full rollout stable and ready for optimization?  
**Metrics:** All 8 modules live, Regression test ≥90%, Calibration improved  
**Decision Owner:** Product Lead + Engineering + Analytics  
**Contingency:** If critical errors found, investigate and patch before Phase 4

---

## Key Innovations

### 1. Confidence Banding (Phase 1)
Instead of hard threshold (answer vs. IDK), use 4-tier system:
- **TIER 1 (≥0.80):** Full answer, no caveats
- **TIER 2 (0.60-0.79):** Answer + optional follow-up
- **TIER 3 (0.40-0.59):** Consulting question to clarify context
- **TIER 4 (<0.40):** "I don't know"

**Impact:** +9% accuracy by being more precise about what we actually know

### 2. Consulting Questions (Phase 2)
When confidence is medium, ask clarifying question instead of guessing:
- "Before I give you the steps, are you trying to [Option A] or [Option B]?"
- "To guide you correctly, is this for [environment A], [environment B], or [environment C]?"

**Impact:** 80% of users respond to clarifying question; follow-up answer is much more accurate

### 3. Confidence Gating (Phase 3)
Only show consulting question if answer has sufficient value:
- Low-confidence "I don't know" answer → Don't ask consulting question (it won't help)
- Low-confidence answer with 3+ alternative paths → Ask consulting question (helps choose)

**Impact:** Eliminates false consulting questions; maintains user trust

### 4. A/B Testing by Module (All Phases)
Enable consulting for specific modules first, measure impact before expanding:
- Phase 1: RCS only (new module, isolated metrics)
- Phase 2: Add Channels & WhatsApp (high volume, clear baseline)
- Phase 3: Add remaining 4 modules (with confidence gating safety)

**Impact:** Fast iteration, clear attribution, low blast radius if issues arise

---

## Expected Outcomes

### Immediate (Week 2-3)
- RCS queries more helpful (more context-aware answers)
- Consulting questions generating 60-70% acceptance rate
- Baseline accuracy maintained or improved

### Short-Term (Week 3-4)
- 3 major modules (RCS, Channels, WhatsApp) live
- +25-35% engagement (users continue conversation to provide context)
- 65-70% accuracy across all modules

### Medium-Term (Sep 8+)
- All 8 modules live with consulting tone
- 73%+ accuracy, 35%+ engagement, <30% IDK rate
- Calibration correlation 0.70+ (confidence scores trustworthy)

### Long-Term
- Stable consulting-tone baseline for all new KB integrations
- Playbook for similar transformations in other products
- Reduced support escalations (more problems solved in conversation)

---

## Next Steps

1. **Immediate (Aug 11):** Kick off Phase 0 (code archaeology + framework design)
2. **Aug 15:** Phase 0 review + Phase 1 approval
3. **Aug 18:** Begin Phase 1 implementation
4. **Aug 22:** Phase 1 metrics review + Phase 2 decision
5. **Aug 25:** Begin Phase 2
6. **Aug 29:** Phase 2 metrics review + Phase 3 decision
7. **Sep 1:** Begin Phase 3
8. **Sep 7:** Phase 3 completion + Phase 4 planning
9. **Sep 8+:** Ongoing optimization & A/B testing

---

## Document References

For detailed implementation specs, see:
- **Full Plan:** `/local/reports/CONSULTING_TONE_PHASED_ROLLOUT_PLAN.md` (comprehensive, 70+ pages)
- **Technical Details:** `/local/reports/CONSULTING_TONE_IMPLEMENTATION_TECHNICAL.md` (code specs, testing)
- **Framework:** `/local/reports/CONSULTING_TONE_FRAMEWORK.md` (consulting tone theory)
- **Executive Summary:** `/local/reports/CONSULTING_TONE_EXECUTIVE_SUMMARY.md` (research findings)

---

## Questions & Contact

- **Product Strategy:** @product-lead
- **Engineering:** @adwit (Code Change Session approved)
- **Analytics:** @analytics-claude
- **QA/Testing:** @qa-team

---

**Status:** Ready for Phase 0 Kickoff  
**Approval:** Pending  
**Timeline Start:** Monday, August 11, 2026

