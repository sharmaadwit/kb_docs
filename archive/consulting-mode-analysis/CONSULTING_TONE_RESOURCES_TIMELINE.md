# Consulting-Tone Rollout: Resource Allocation & Timeline
## Detailed Implementation Schedule

**Planning Date:** August 11, 2026  
**Start Date:** August 11, 2026 (Phase 0)  
**Completion Date:** September 7, 2026 (Phase 3 complete)  
**Duration:** 4 weeks  

---

## Resource Requirements Summary

### People & Roles

| Role | Effort | Duration | Availability | Assigned |
|------|--------|----------|---------------|----------|
| **Backend Engineer** (kb_answer.py) | 4-5 days | Phases 1, 2, 3 | Full-time | @adwit (pre-approved Code Change Session) |
| **Analytics/QA Agent** | 8-10 days | All phases | Full-time | @analytics-claude |
| **QA/Regression Testing** | 2-3 days | Phases 1, 3 | Part-time (10 hrs/week) | @qa-team or embedded |
| **Product Lead** (decisions) | 4-5 hrs | All phases (decision gates) | Part-time (30 min per gate) | @product-lead |
| **Stakeholder Review** | 2-3 hrs | All phases (gates) | Part-time (30 min per phase) | @engineering-lead |

**Total Effort:** ~17-20 person-days (4 weeks, 1.5 FTE team)

### Skills Required

- Python/kb_answer.py expertise (backend engineer)
- Langfuse API knowledge (analytics agent)
- A/B testing & metrics (analytics agent)
- Regression testing (QA)
- Product strategy & gating (product lead)

### Infrastructure & Tools

- **Langfuse** (existing): Trace collection, metadata capture
- **Git/GitHub/GitLab**: Code versioning, PR reviews
- **Python scripts**: Test harnesses, metrics collection
- **HTML dashboards**: Visualization of metrics (generate locally)
- **Slack/Email**: Stakeholder communication

---

## Phase-by-Phase Breakdown

## PHASE 0: Code Archaeology & Framework Design
**Weeks:** Aug 11-17 (5 business days)  
**Effort:** 7 person-days  
**Team:** Backend Engineer (2 days) + Analytics Agent (5 days)

### Task 0.1: Map Answer Generation Pipeline (1 day)
**Owner:** Analytics Agent  
**Effort:** 8 hours  
**Dependencies:** None

**Deliverables:**
- [ ] `/local/reports/PHASE_0_PIPELINE_ARCHITECTURE.md` (2 pages)
  - Query flow diagram (sanitize → translate → detect module → classify intent → extract entities)
  - Evidence selection logic (kb_search integration)
  - Confidence calculation
  - Answer composition
  - Langfuse telemetry
  - Module-specific code paths mapped

**Activities:**
- Day 1 (Mon Aug 11): Read kb_answer.py line by line, document flow
- Output: Architecture doc + critical line numbers identified

**Acceptance:**
- [ ] Pipeline mapped with line numbers (±5 lines)
- [ ] Module routing logic understood
- [ ] Confidence calculation process documented

---

### Task 0.2: Design Consulting-Tone Framework (2 days)
**Owner:** Analytics Agent + Backend Engineer (1 day review)  
**Effort:** 16 hours (14 Analytics + 2 Engineer review)  
**Dependencies:** Task 0.1

**Deliverables:**
- [ ] `/local/reports/PHASE_0_CONSULTING_FRAMEWORK.md` (8-10 pages)
  - Confidence tier model (0.80 / 0.60 / 0.40 thresholds)
  - 5+ consulting question templates per major intent (how_to, setup, troubleshoot)
  - Risk gates & accuracy thresholds (min 70% per module)
  - Follow-up routing logic
  - Telemetry instrumentation spec (tags, metadata fields)
  - Rollback strategy

**Activities:**
- Day 2-3 (Tue-Wed Aug 12-13):
  - Research: Review existing consulting-tone examples from earlier analysis
  - Design: Create framework doc with tiers, templates, safety gates
  - Review: Engineer reviews for feasibility (2 hours)

**Acceptance:**
- [ ] 4+ confidence tiers defined with decision logic
- [ ] 5+ consulting question templates per intent
- [ ] Accuracy safety gates clear (≥70% per module)
- [ ] Telemetry schema defined
- [ ] Engineer sign-off on feasibility

---

### Task 0.3: Design Rollout-Safe Code Changes (1 day)
**Owner:** Backend Engineer  
**Effort:** 8 hours  
**Dependencies:** Tasks 0.1, 0.2

**Deliverables:**
- [ ] `/local/reports/PHASE_0_ROLLOUT_SAFE_DESIGN.md` (6-8 pages)
  - Non-breaking code changes (add new functions, don't modify signatures)
  - Feature flag architecture (CONSULTING_ENABLED dict by module)
  - Rollback procedures (flip flag, no code deploy needed)
  - A/B testing framework (user_id % 2 split or random)
  - Confidence tier telemetry (tags + metadata fields)

**Activities:**
- Day 4 (Thu Aug 14):
  - Design: Create code change document
  - Outline: Function signatures, feature flags, metadata schema
  - Plan: Where to insert code in kb_answer.py (line numbers)

**Acceptance:**
- [ ] All changes backward-compatible (no signature changes)
- [ ] Rollback requires only flag change
- [ ] A/B test framework designed
- [ ] Zero impact if consulting disabled

---

### Task 0.4: Phase 0 Stakeholder Review & Phase 1 Approval (1 day)
**Owner:** Product Lead + Engineering Lead  
**Effort:** 4 hours (2 hrs review + 1 hr decision + 1 hr kickoff)  
**Dependencies:** All Phase 0 tasks

**Activities:**
- Day 5 (Fri Aug 15):
  - 10:00-11:00 AM: Framework + design review (product lead, engineer, analytics)
  - 11:00 AM-12:00 PM: Decision: Proceed to Phase 1?
  - 12:00-1:00 PM: Phase 1 kickoff planning (confirm engineer start date, resources)

**Decision Criteria:**
- [ ] Framework is sound and leverages existing codebase
- [ ] Rollout-safe design enables instant rollback
- [ ] Stakeholders aligned on 4-week timeline
- [ ] RCS module identified and ready for Phase 1

**Expected Outcome:** GO/PROCEED to Phase 1

---

## PHASE 1: RCS Module Soft Gradient & Consulting (Pilot)
**Weeks:** Aug 18-24 (5 business days)  
**Effort:** 12 person-days  
**Team:** Backend Engineer (3-4 days) + Analytics Agent (6-7 days) + QA (2 days)

### Task 1.1: Implement Confidence Banding & Soft Gradient (1 day)
**Owner:** Backend Engineer  
**Effort:** 8 hours  
**Dependencies:** Phase 0 complete

**Deliverables:**
- [ ] Code merged: Confidence constants + `_confidence_band()` function
- [ ] Code merged: Updated answer logic (attempt answer even for low-conf if consulting enabled)
- [ ] Code merged: Langfuse metadata includes `confidence_tier` tag
- [ ] Test script: `test_phase1_soft_gradient.py`

**Activities:**
- Day 1 (Mon Aug 18):
  - 9:00-10:00 AM: Code review of existing answer composition logic
  - 10:00 AM-12:30 PM: Implement constants + confidence banding function
  - 1:00-3:00 PM: Update answer logic + Langfuse metadata
  - 3:00-4:00 PM: Create test script, verify no regressions

**Code Changes:**
- Add 10 lines: Constants (CONFIDENCE_TIER_FULL, etc.)
- Add 15 lines: `_confidence_band()` function
- Modify 20 lines: Answer logic (soft gradient instead of hard cutoff)
- Add 5 lines: Langfuse metadata update
- Total: ~50 lines added/modified

**Testing:**
```
test_phase1_soft_gradient.py
├─ Confidence band mapping (0.80+ → "full", 0.60-0.80 → "answer", etc.)
├─ Answer returned for low-confidence (not just IDK)
├─ Langfuse metadata includes confidence_tier
└─ No regression: high-confidence answers unchanged
```

**Acceptance:**
- [ ] All 4 tiers map correctly
- [ ] Low-confidence answers attempted (not auto-IDK)
- [ ] Langfuse captures confidence_tier
- [ ] Regression test passes (50+ existing queries unaffected)

---

### Task 1.2: Implement Consulting Questions for RCS (1 day)
**Owner:** Backend Engineer  
**Effort:** 8 hours  
**Dependencies:** Task 1.1

**Deliverables:**
- [ ] Code merged: `_consulting_question_for_intent()` function (templates for RCS)
- [ ] Code merged: `_format_answer_with_consultation()` function
- [ ] Code merged: Integration into answer logic (show consulting Q for TIER 3)
- [ ] Code merged: Langfuse metadata + tags updated
- [ ] Test script: `test_phase1_consulting_questions.py`

**Activities:**
- Day 2 (Tue Aug 19):
  - 9:00-10:00 AM: Design consulting question templates for RCS
  - 10:00 AM-12:00 PM: Implement question generator function
  - 1:00-2:00 PM: Implement answer formatting with consultation
  - 2:00-3:00 PM: Integration into main answer logic
  - 3:00-4:00 PM: Create test script, verify question quality

**Code Changes:**
- Add 50 lines: `_consulting_question_for_intent()` with RCS-specific templates
- Add 20 lines: `_format_answer_with_consultation()`
- Modify 15 lines: Answer logic to inject consulting question
- Add 5 lines: Langfuse tagging for consulting_question_shown
- Total: ~90 lines

**Testing:**
```
test_phase1_consulting_questions.py
├─ Consulting questions generated for TIER 3 (medium confidence)
├─ Questions NOT shown for TIER 1-2 (high confidence) or TIER 4 (IDK)
├─ Question text references KB content
├─ Langfuse captures consulting_question_shown flag
└─ Regression: TIER 1-2 answers unchanged
```

**Acceptance:**
- [ ] Consulting questions only for TIER 3
- [ ] Questions generated from validated KB alternatives
- [ ] Langfuse captures flag correctly
- [ ] Question quality audit: 85%+ relevance (manual spot-check)

---

### Task 1.3: A/B Test RCS Queries (2-3 days)
**Owner:** Analytics Agent + Backend Engineer (deployment)  
**Effort:** 20 hours  
**Dependencies:** Tasks 1.1, 1.2

**Activities:**
- Day 2-3 (Tue-Wed Aug 19-20): Deploy code to production (feature flag for RCS only)
  - Engineer: Tag release as v1.0-phase1-rcs
  - Analytics: Monitor Langfuse traces for first 1 hour (watch for errors)
  - Setup: Enable CONSULTING_ENABLED["RCS"] = True, randomize 50/50 control/treatment

- Day 4-5 (Thu-Fri Aug 21-22): Collect A/B test data
  - Collect: RCS queries for 48 hours (target 50+ control, 50+ treatment)
  - Monitor: Accuracy, IDK rate, engagement, consulting acceptance
  - Dashboard: Create phase1_rcs_metrics.html with results

**Deliverables:**
- [ ] Production deployment with A/B test framework
- [ ] `/local/reports/phase1_rcs_metrics.html` (updated daily)
  - Control group metrics (soft gradient, no consulting)
  - Treatment group metrics (soft gradient + consulting)
  - Comparison: accuracy, IDK rate, engagement, consulting acceptance
  - Sample queries with consulting questions shown

**Metrics to Capture:**
```
Control Group:
  - Total queries: N
  - IDK rate: X%
  - Accuracy: Y%
  - Avg confidence: Z
  - Follow-up rate: W%

Treatment Group:
  - Total queries: N
  - IDK rate: X%
  - Accuracy: Y%
  - Avg confidence: Z
  - Consulting shown: A% of answers
  - Consulting acceptance: B%
  - Follow-up rate: W%
  - Follow-up success: V% (answer resolved)

Difference (Treatment - Control):
  - IDK rate change: ∆X
  - Accuracy change: ∆Y
  - Follow-up rate change: ∆W
```

**Acceptance:**
- [ ] A/B test deployed to 50% of RCS queries
- [ ] 48+ hours of data collected (target 100+ queries per group)
- [ ] Metrics dashboard created and updated
- [ ] Accuracy ≥70% confirmed (or issue flagged)
- [ ] Consulting acceptance ≥50% confirmed (or questions refined)

---

### Task 1.4: Phase 1 Analysis & Phase 2 Decision (1 day)
**Owner:** Analytics Agent  
**Effort:** 8 hours  
**Dependencies:** Task 1.3

**Activities:**
- Day 5 (Fri Aug 22):
  - 9:00-10:00 AM: Analyze A/B test results
  - 10:00-11:00 AM: Compare treatment vs. control, flag any issues
  - 11:00 AM-12:00 PM: Draft Phase 1 results summary
  - 1:00-2:00 PM: Present findings to product lead + engineer
  - 2:00-3:00 PM: Decision: Proceed to Phase 2?

**Decision Criteria:**
- [ ] Accuracy ≥70% (or >baseline 60%)
- [ ] Engagement improved (follow-up rate +15% vs. control)
- [ ] Consulting acceptance ≥50%
- [ ] No critical errors (0 per day)
- [ ] IDK rate decreased (<45%, baseline 45.7%)

**Expected Outcome:** GO/PROCEED to Phase 2

**Deliverables:**
- [ ] `/local/reports/PHASE_1_RESULTS_SUMMARY.md` (2 pages)
  - A/B test results (control vs. treatment)
  - Key findings (accuracy, engagement, consulting quality)
  - Recommendations for Phase 2 (template changes, threshold adjustments)
  - Decision: Proceed to Phase 2?

---

## PHASE 2: Channels & WhatsApp High-Engagement Modules
**Weeks:** Aug 25-31 (5 business days)  
**Effort:** 10 person-days  
**Team:** Backend Engineer (2-3 days) + Analytics Agent (5-6 days) + QA (1-2 days)

### Task 2.1: Refine Consulting Questions from Phase 1 (1 day)
**Owner:** Analytics Agent  
**Effort:** 8 hours  
**Dependencies:** Phase 1 results

**Activities:**
- Day 1 (Mon Aug 25):
  - 9:00-10:00 AM: Analyze Phase 1 consulting questions (acceptance rates)
  - 10:00 AM-12:00 PM: Identify top performers & low performers
  - 1:00-3:00 PM: Design refinements for Phase 2 (new templates)
  - 3:00-4:00 PM: Document learnings

**Deliverables:**
- [ ] `/local/reports/PHASE_1_CONSULTING_LEARNINGS.md` (2 pages)
  - Questions ranked by acceptance rate
  - Top performers (72%+): Keep, use more often
  - Low performers (<55%): Remove or replace
  - Recommendations: Persona-specific variations for Channels & WhatsApp

**Acceptance:**
- [ ] Top performers identified (with acceptance % and usage count)
- [ ] Low performers flagged for removal
- [ ] New templates designed for Phase 2 modules

---

### Task 2.2: Enable Consulting for Channels & WhatsApp (1 day)
**Owner:** Backend Engineer  
**Effort:** 8 hours  
**Dependencies:** Task 2.1

**Activities:**
- Day 2 (Tue Aug 26):
  - 9:00-10:00 AM: Add Channels & WhatsApp to CONSULTING_ENABLED flag
  - 10:00 AM-12:00 PM: Implement module-specific consulting questions
  - 1:00-2:00 PM: Update Langfuse tagging (module-specific tags)
  - 2:00-3:00 PM: Test consulting questions for both modules
  - 3:00-4:00 PM: Verify no regressions, deploy

**Code Changes:**
- Modify 5 lines: CONSULTING_ENABLED["Channels"] = True, ["WhatsApp"] = True
- Add 30 lines: Module-specific question templates
- Modify 10 lines: Question selection logic (choose template by module)
- Modify 5 lines: Langfuse tagging (add module-specific tags)
- Total: ~50 lines

**Testing:**
```
test_phase2_channels_whatsapp.py
├─ Consulting questions generated for Channels queries
├─ Consulting questions generated for WhatsApp queries
├─ Module-specific variations applied correctly
├─ Langfuse tags include consulting_channels, consulting_whatsapp
└─ No regression in other modules (Bot Studio, Agent Assist)
```

**Acceptance:**
- [ ] Consulting enabled for both modules
- [ ] Module-specific questions implemented
- [ ] Test script passes
- [ ] No regressions in baseline

---

### Task 2.3: Measure Cross-Module Impact (3 days)
**Owner:** Analytics Agent  
**Effort:** 24 hours  
**Dependencies:** Task 2.2 deployed

**Activities:**
- Day 3-4 (Wed-Thu Aug 27-28): Deploy + collect data
  - Collect: Queries from all 3 modules (RCS, Channels, WhatsApp) for 48 hours
  - Monitor: Per-module accuracy, IDK rate, engagement
  - Alert: If any module accuracy drops below 70%, investigate immediately

- Day 5 (Fri Aug 29): Analysis + Phase 3 decision
  - Analyze: Cross-module metrics, rollback triggers
  - Create: phase2_cross_module_metrics.html dashboard
  - Decide: Proceed to Phase 3?

**Deliverables:**
- [ ] `/local/reports/phase2_cross_module_metrics.html` (dashboard)
  - Per-module comparison: accuracy, IDK rate, engagement, consulting acceptance
  - Global metrics: accuracy, IDK rate, engagement multiplier
  - Rollback trigger status (all 5 triggers: green or red?)
  - Recommendation: Proceed to Phase 3?

**Metrics:**
```
Module      │ Queries │ Accuracy │ IDK %  │ Engagement │ Consulting
─────────────┼─────────┼──────────┼────────┼────────────┼──────────
RCS         │ 120     │ 71% ✓    │ 35%    │ 1.48x ✓    │ 42 (35%)
Channels    │ 287     │ 69% ✓    │ 39%    │ 1.44x ✓    │ 121 (42%)
WhatsApp    │ 156     │ 68% ✓    │ 36%    │ 1.40x ✓    │ 59 (38%)
─────────────┴─────────┴──────────┴────────┴────────────┴──────────
Global      │ 563     │ 69% ✓    │ 37%    │ 1.44x ✓    │ 28% avg
```

**Acceptance Criteria:**
- [ ] Cross-module accuracy ≥70% for all 3 modules
- [ ] IDK rate <40% for all modules
- [ ] Engagement +25-40% (actual: ~1.44x = +44%)
- [ ] No new errors or critical issues
- [ ] Consulting question acceptance ≥50% per module

**Decision Gates:**
- [ ] Accuracy ≥70% across all 3 modules (GO to Phase 3)
- [ ] If any module <70%, ITERATE Phase 2 (don't proceed)
- [ ] If engagement <1.15x, investigate consulting question quality
- [ ] If consulting acceptance <50%, refine templates before Phase 3

**Expected Outcome:** GO/PROCEED to Phase 3

---

## PHASE 3: Full Rollout + Confidence Gating
**Weeks:** Sep 1-7 (5 business days)  
**Effort:** 15 person-days  
**Team:** Backend Engineer (3-4 days) + Analytics Agent (8-9 days) + QA (3 days)

### Task 3.1: Implement Confidence Gating (1 day)
**Owner:** Backend Engineer  
**Effort:** 8 hours  
**Dependencies:** Phase 2 complete

**Activities:**
- Day 1 (Mon Sep 1):
  - 9:00-10:00 AM: Review confidence gating design from Phase 0
  - 10:00 AM-12:00 PM: Implement `_answer_value_score()` function (assess answer quality)
  - 1:00-2:00 PM: Implement `_should_show_consulting_question_gated()`
  - 2:00-3:00 PM: Integrate into answer logic
  - 3:00-4:00 PM: Create test script, verify gating works

**Code Changes:**
- Add 30 lines: `_answer_value_score()` (length, evidence count, keyword heuristics)
- Add 15 lines: `_should_show_consulting_question_gated()`
- Modify 20 lines: Answer logic (check value score before showing consulting Q)
- Add 5 lines: Langfuse metadata (answer_value_score, consulting_gated)
- Total: ~70 lines

**Testing:**
```
test_phase3_confidence_gating.py
├─ High-confidence + high-value answer: Show consulting question ✓
├─ High-confidence + low-value answer: Don't show ✓
├─ Low-confidence + high-value answer: Show consulting question ✓
├─ Low-confidence + low-value answer (IDK): Don't show ✓
└─ Langfuse captures answer_value_score and consulting_gated flags
```

**Acceptance:**
- [ ] Value score calculated correctly
- [ ] Consulting questions gated properly (not shown for low-value answers)
- [ ] Langfuse metadata updated
- [ ] Test script passes all 4 cases

---

### Task 3.2: Enable Consulting for All 8 Modules (1 day)
**Owner:** Backend Engineer  
**Effort:** 8 hours  
**Dependencies:** Task 3.1

**Activities:**
- Day 2 (Tue Sep 2):
  - 9:00-10:00 AM: Design consulting question templates for remaining 4 modules
  - 10:00 AM-12:00 PM: Implement templates in code
  - 1:00-2:00 PM: Test consulting questions for all 4 new modules
  - 2:00-3:00 PM: Verify no regressions, deploy
  - 3:00-4:00 PM: Monitor Langfuse traces for errors

**Code Changes:**
- Modify 8 lines: CONSULTING_ENABLED for all 8 modules = True
- Add 50 lines: Consulting question templates for Bot Studio, Agent Assist, Campaign Manager, General
- Modify 10 lines: Template selection logic (choose by module + intent)
- Total: ~68 lines

**Testing:**
```
test_phase3_all_modules.py
├─ Consulting questions for Bot Studio queries
├─ Consulting questions for Agent Assist queries
├─ Consulting questions for Campaign Manager queries
├─ Consulting questions for General queries
└─ All existing modules still working (RCS, Channels, WhatsApp)
```

**Acceptance:**
- [ ] All 8 modules enabled (CONSULTING_ENABLED = all True)
- [ ] Question templates created for new modules
- [ ] Test script passes for all modules
- [ ] No regressions in accuracy or engagement

---

### Task 3.3: Comprehensive Regression Testing (2-3 days)
**Owner:** QA + Analytics Agent  
**Effort:** 24 hours  
**Dependencies:** Tasks 3.1, 3.2 deployed

**Activities:**
- Day 2-3 (Tue-Wed Sep 2-3): Run regression test suite
  - QA: Execute phase3_regression_test.py (50+ queries)
  - Track: Pass/fail for each query + reason
  - Report: Accuracy, failures, outliers

- Day 3-4 (Wed-Thu Sep 3-4): Stability monitoring
  - Monitor: Langfuse traces for errors, latency spikes, exceptions
  - Alert: If error rate >1%, investigate immediately
  - Collect: Cross-module metrics (accuracy per module)

- Day 5 (Fri Sep 7): Final analysis + Phase 4 planning
  - Compile: Regression test results + cross-module metrics
  - Create: phase3_full_stack_metrics.html dashboard
  - Decide: All green? Ready for Phase 4?

**Deliverables:**
- [ ] `phase3_regression_test.py` output (50+ queries, accuracy ≥90%)
- [ ] `/local/reports/phase3_full_stack_metrics.html` (dashboard)
  - All 8 modules: accuracy, IDK rate, engagement, consulting acceptance
  - Global metrics: 73%+ accuracy, <30% IDK, 1.35x engagement
  - Rollback triggers: all green
  - Consulting question quality audit (85%+ relevance)

**Acceptance Criteria:**
- [ ] Regression test accuracy ≥90% (all 50+ queries pass or have clear reason)
- [ ] Module-specific accuracy ≥65% for new modules (Phase 3)
- [ ] Consulting question quality audit ≥85%
- [ ] No critical errors (0 per day for 48 hours)
- [ ] Calibration correlation ≥0.70
- [ ] All rollback triggers green

**Decision Gates:**
- [ ] Regression accuracy ≥90% (GO to Phase 4)
- [ ] If <90%, ITERATE Phase 3 (fix issues, re-test)
- [ ] All 8 modules live + stable = PROCEED

**Expected Outcome:** GO/PROCEED to Phase 4 (ongoing optimization)

---

## PHASE 4: Optimization & Calibration
**Weeks:** Sep 8+ (Ongoing)  
**Effort:** 8-10 person-days (spread over 4+ weeks)  
**Team:** Analytics Agent (80%) + Backend Engineer (20%)

### Task 4.1: Recalibrate Confidence Thresholds
**Owner:** Analytics Agent  
**Effort:** 16 hours (2 days, spread over week 1 of Phase 4)  

**Activities:**
- Week 1 of Phase 4:
  - Analyze: Accuracy at each confidence level (e.g., 0.80-0.89 → 94% accuracy, etc.)
  - Identify: Optimal thresholds for each tier
  - Recommendation: Update CONFIDENCE_TIER_* constants if data supports
  - Test: Measure accuracy impact of new thresholds
  - Deploy: If improvement >2%, update thresholds in code

**Deliverables:**
- [ ] `/local/reports/PHASE_4_CONFIDENCE_CALIBRATION.md`
  - Confidence level vs. accuracy analysis
  - Recommended thresholds
  - Accuracy improvement predicted

**Expected Outcome:** +2-5% accuracy improvement via threshold adjustment

---

### Task 4.2: Optimize Consulting Templates by Performance
**Owner:** Analytics Agent  
**Effort:** 16 hours (2 days, spread over week 2 of Phase 4)  

**Activities:**
- Week 2 of Phase 4:
  - Rank: Consulting questions by acceptance rate
  - Identify: Top performers (70%+) and low performers (<55%)
  - A/B Test: Design variations for medium performers
  - Iterate: Deploy variations, measure for 1 week

**Expected Outcome:** +5-10% consulting acceptance via template optimization

---

### Task 4.3: Module-Specific Optimization
**Owner:** Analytics Agent  
**Effort:** 16 hours (2 days, spread over weeks 3-4 of Phase 4)  

**Activities:**
- Week 3-4 of Phase 4:
  - Per-module analysis: Which questions work best in each module?
  - Recommendations: Focus high-performers, deprecate low-performers
  - A/B test results: Validate improvements

**Expected Outcome:** Stable 73%+ accuracy, 35%+ engagement per module

---

### Task 4.4: Ongoing Monitoring & Dashboards
**Owner:** Analytics Agent  
**Effort:** 8 hours/week (ongoing maintenance)  

**Activities:**
- Daily: Check rollback triggers (accuracy, engagement, IDK rate, errors)
- Weekly: Generate metrics dashboard (phase4_success_measurement.html)
- Monthly: Prepare optimization report + recommendations

**Deliverables:**
- [ ] `/local/reports/phase4_success_measurement.html` (updated weekly)
- [ ] Ongoing A/B testing framework
- [ ] Monthly optimization reports

---

## Summary Timeline Gantt

```
┌─────────────────────────────────────────────────────────────────┐
│ WEEK 1 (Aug 11-17): Phase 0 - Design & Architecture            │
├─────────────────────────────────────────────────────────────────┤
│ Mon Aug 11  ▓▓▓▓▓ Task 0.1: Pipeline archaeology (Analytics)   │
│ Tue Aug 12  ▓▓▓▓▓▓▓ Task 0.2: Consulting framework (Analytics)  │
│ Wed Aug 13  ▓▓▓▓▓▓▓ Task 0.2 cont'd (Analytics)                │
│ Thu Aug 14  ▓▓▓▓▓ Task 0.3: Rollout-safe design (Engineer)     │
│ Fri Aug 15  ▓▓ Task 0.4: Stakeholder review & go/no-go         │
│             Decision: PROCEED to Phase 1                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ WEEK 2 (Aug 18-24): Phase 1 - RCS Pilot                         │
├─────────────────────────────────────────────────────────────────┤
│ Mon Aug 18  ▓▓▓▓▓ Task 1.1: Confidence banding (Engineer)       │
│ Tue Aug 19  ▓▓▓▓▓ Task 1.2: Consulting questions (Engineer)     │
│ Tue Aug 19  ▓▓▓ Task 1.3a: Deploy to prod, start A/B test       │
│ Wed Aug 20  ▓▓▓▓▓▓▓▓▓▓ Task 1.3b: Collect A/B data (Analytics)  │
│ Thu Aug 21  ▓▓▓▓▓▓▓▓▓▓ Task 1.3 cont'd: Monitor & refine        │
│ Fri Aug 22  ▓▓▓▓▓ Task 1.4: Analysis & go/no-go decision        │
│             Decision: PROCEED to Phase 2                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ WEEK 3 (Aug 25-31): Phase 2 - Channels & WhatsApp              │
├─────────────────────────────────────────────────────────────────┤
│ Mon Aug 25  ▓▓▓▓▓ Task 2.1: Refine from Phase 1 (Analytics)     │
│ Tue Aug 26  ▓▓▓▓▓ Task 2.2: Enable Channels & WhatsApp (Eng)    │
│ Tue Aug 26  ▓▓▓ Task 2.3a: Deploy, start data collection        │
│ Wed Aug 27  ▓▓▓▓▓▓▓▓▓▓ Task 2.3b: Collect cross-module data      │
│ Thu Aug 28  ▓▓▓▓▓▓▓▓▓▓ Task 2.3 cont'd: Monitor & analyze       │
│ Fri Aug 29  ▓▓▓▓▓ Task 2.3c: Analysis & go/no-go                │
│             Decision: PROCEED to Phase 3                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ WEEK 4 (Sep 1-7): Phase 3 - Full Rollout + Gating              │
├─────────────────────────────────────────────────────────────────┤
│ Mon Sep 1   ▓▓▓▓▓ Task 3.1: Implement confidence gating (Eng)    │
│ Tue Sep 2   ▓▓▓▓▓ Task 3.2: Enable all 8 modules (Engineer)      │
│ Tue Sep 2   ▓▓▓ Task 3.3a: Deploy, start monitoring (QA)        │
│ Wed Sep 3   ▓▓▓▓▓▓▓▓▓▓ Task 3.3b: Regression testing (QA)       │
│ Thu Sep 4   ▓▓▓▓▓▓▓▓▓▓ Task 3.3: Stability monitoring (Analytics)│
│ Fri Sep 7   ▓▓▓▓▓ Task 3.3c: Analysis & Phase 4 planning         │
│             Decision: PROCEED to Phase 4 (ongoing optimization)  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ WEEK 5+ (Sep 8+): Phase 4 - Optimization & Calibration         │
├─────────────────────────────────────────────────────────────────┤
│ Week 5   ▓▓ Task 4.1: Recalibrate confidence thresholds         │
│ Week 6   ▓▓ Task 4.2: Optimize consulting templates             │
│ Week 7-8 ▓▓ Task 4.3: Module-specific optimization             │
│ Ongoing  ▓▓ Task 4.4: Monitoring & dashboards (1-2 hrs/week)   │
└─────────────────────────────────────────────────────────────────┘

Legend:
▓▓▓▓▓ = 8 hours (1 person-day)
▓▓▓▓▓▓▓ = 16 hours (2 person-days)
▓▓▓▓▓▓▓▓▓▓ = 24+ hours (3+ person-days)
```

---

## Team Calendar

### Backend Engineer (@adwit)
```
Week 1 (Aug 11-17):  2 days  (0.4 FTE)
  ├─ Aug 14 (1 day): Task 0.3 - Rollout-safe design
  └─ Aug 15 (0.5 day): Task 0.4 - Stakeholder review

Week 2 (Aug 18-24):  4 days  (0.8 FTE)
  ├─ Aug 18 (1 day): Task 1.1 - Confidence banding
  ├─ Aug 19 (1 day): Task 1.2 - Consulting questions
  ├─ Aug 19 (0.5 day): Task 1.3a - Deploy to prod
  └─ Aug 22 (0.5 day): Task 1.4 - Stakeholder review

Week 3 (Aug 25-31):  2 days  (0.4 FTE)
  ├─ Aug 26 (1 day): Task 2.2 - Enable Channels & WhatsApp
  ├─ Aug 26 (0.5 day): Task 2.3a - Deploy
  └─ Aug 29 (0.5 day): Task 2.3c - Stakeholder review

Week 4 (Sep 1-7):    4 days  (0.8 FTE)
  ├─ Sep 1 (1 day): Task 3.1 - Confidence gating
  ├─ Sep 2 (1 day): Task 3.2 - Enable all 8 modules
  ├─ Sep 2 (0.5 day): Task 3.3a - Deploy
  └─ Sep 7 (0.5 day): Task 3.3c - Phase 4 planning

Week 5+ (Sep 8+):   0.5 days/week (0.1 FTE)
  └─ Ad-hoc: Code reviews, bug fixes, optimization PRs

TOTAL: ~12-13 days over 4 weeks (1.0 FTE for month)
```

### Analytics Agent (@analytics-claude)
```
Week 1 (Aug 11-17):  5 days  (1.0 FTE)
  ├─ Aug 11 (1 day): Task 0.1 - Pipeline archaeology
  ├─ Aug 12-13 (2 days): Task 0.2 - Consulting framework
  └─ Aug 15 (0.5 day): Task 0.4 - Stakeholder review

Week 2 (Aug 18-24):  6 days  (1.2 FTE) *peak
  ├─ Aug 18-19 (0.5 day): Task 1.1 testing
  ├─ Aug 19-20 (1 day): Task 1.2 testing
  ├─ Aug 19-22 (3 days): Task 1.3 - A/B test setup, collect, analyze
  └─ Aug 22 (1 day): Task 1.4 - Results analysis

Week 3 (Aug 25-31):  6 days  (1.2 FTE) *peak
  ├─ Aug 25 (1 day): Task 2.1 - Refine templates
  ├─ Aug 26 (0.5 day): Task 2.2 testing
  ├─ Aug 26-29 (3 days): Task 2.3 - Collect, monitor, analyze
  └─ Aug 29 (0.5 day): Task 2.3 - Present findings

Week 4 (Sep 1-7):    8 days  (1.6 FTE) *peak
  ├─ Sep 1-2 (0.5 day): Task 3.1 testing
  ├─ Sep 2-3 (0.5 day): Task 3.2 testing
  ├─ Sep 2-6 (3 days): Task 3.3 - Regression, monitoring, analysis
  ├─ Sep 3-4 (1 day): Task 3.3b - Detailed QA support
  ├─ Sep 6-7 (1 day): Task 3.3c - Analysis + Phase 4 planning
  └─ Sep 7 (0.5 day): Dashboard creation

Week 5+ (Sep 8+):   2-3 days/week (0.4-0.6 FTE)
  ├─ Week 5 (2 days): Task 4.1 - Threshold calibration
  ├─ Week 6 (2 days): Task 4.2 - Template optimization
  ├─ Week 7-8 (2 days): Task 4.3 - Module-specific tuning
  └─ Ongoing (1-2 hrs/week): Task 4.4 - Monitoring

TOTAL: ~30-35 days over 4 weeks + ongoing (1.5 FTE for month)
```

### QA/Testing (@qa-team or embedded)
```
Week 1 (Aug 11-17):  None (0 FTE)

Week 2 (Aug 18-24):  2 days  (0.4 FTE)
  ├─ Aug 19-20 (1 day): Create & run test_phase1_gradient
  └─ Aug 19-20 (1 day): Monitor production for errors

Week 3 (Aug 25-31):  1 day   (0.2 FTE)
  └─ Aug 27-28 (1 day): Monitor production for errors

Week 4 (Sep 1-7):    3 days  (0.6 FTE)
  ├─ Sep 2-4 (2 days): Regression test suite (phase3_regression_test.py)
  ├─ Sep 3-5 (1 day): Stability monitoring (error rates, latency)
  └─ Sep 7 (0.5 day): QA sign-off

Week 5+ (Sep 8+):   0.5 days/week (0.1 FTE)
  └─ Ad-hoc: Bug verification, test updates

TOTAL: ~6-7 days over 4 weeks (0.35 FTE for month)
```

### Product Lead (@product-lead)
```
Week 1 (Aug 11-17):  1 day   (0.2 FTE)
  └─ Aug 15 (1 day): Phase 0 review & Phase 1 approval

Week 2 (Aug 18-24):  0.5 day (0.1 FTE)
  └─ Aug 22 (0.5 day): Phase 1 results review & Phase 2 approval

Week 3 (Aug 25-31):  0.5 day (0.1 FTE)
  └─ Aug 29 (0.5 day): Phase 2 results review & Phase 3 approval

Week 4 (Sep 1-7):    1 day   (0.2 FTE)
  └─ Sep 7 (1 day): Phase 3 results review & Phase 4 planning

Week 5+ (Sep 8+):    0.5 hrs/week (0.02 FTE)
  └─ Monthly: Review optimization reports

TOTAL: ~3-4 days over 4 weeks (0.2 FTE for month)
```

---

## Dependency Map

```
Phase 0 (All Required)
├─ Task 0.1: Pipeline archaeology
├─ Task 0.2: Consulting framework (depends on 0.1)
├─ Task 0.3: Rollout design (depends on 0.1 + 0.2)
└─ Task 0.4: Stakeholder review (depends on 0.1 + 0.2 + 0.3)

Phase 1 (Sequential: 1.1 → 1.2 → 1.3 → 1.4)
├─ Task 1.1: Confidence banding (depends on Phase 0)
├─ Task 1.2: Consulting questions (depends on 1.1)
├─ Task 1.3: A/B test (depends on 1.1 + 1.2 deployed)
└─ Task 1.4: Analysis & decision (depends on 1.3 data)

Phase 2 (Sequential: 2.1 → 2.2 → 2.3 → decision)
├─ Task 2.1: Refine questions (depends on Phase 1 results)
├─ Task 2.2: Enable modules (depends on 2.1 + Phase 0)
├─ Task 2.3: Measure impact (depends on 2.2 deployed)
└─ Decision: Proceed to Phase 3 (depends on 2.3 data)

Phase 3 (Parallel: 3.1 & 3.2, then 3.3)
├─ Task 3.1: Confidence gating (depends on Phase 0 + Phase 2)
├─ Task 3.2: Enable 8 modules (depends on Phase 2)
├─ Task 3.3: Regression testing (depends on 3.1 + 3.2 deployed)
└─ Decision: Proceed to Phase 4 (depends on 3.3)

Phase 4 (Ongoing, No Dependencies)
├─ Task 4.1: Recalibrate (depends on Phase 3 complete)
├─ Task 4.2: Template optimization (ongoing)
├─ Task 4.3: Module tuning (ongoing)
└─ Task 4.4: Monitoring (ongoing)
```

---

## Budget & Costs

**Personnel Effort:**
| Role | Days | Rate | Total |
|------|------|------|-------|
| Backend Engineer | 12-13 days | $500/day | $6,000-6,500 |
| Analytics Agent | 30-35 days | $400/day | $12,000-14,000 |
| QA/Testing | 6-7 days | $300/day | $1,800-2,100 |
| Product Lead | 3-4 days | $600/day | $1,800-2,400 |
| **Total Personnel** | ~50-60 days | Average $440/day | **$22,000-25,000** |

**Infrastructure:**
- Langfuse API: ~$200 (existing, small increase for 4 weeks)
- Git/GitHub/GitLab: $0 (existing)
- Testing tools: $0 (existing)
- **Total Infrastructure:** $200

**Total 4-Week Cost:** ~$22,200-25,200

---

## Success Metrics & KPIs

### Technical KPIs (Daily Monitoring)
- Accuracy: ≥70% per module (target 73%)
- IDK Rate: <40% (target 33%)
- Engagement: 1.25-1.40x multiplier
- Error Rate: <1 critical error/day
- Latency: <2s p95 (no impact from consulting logic)

### Product KPIs (Weekly Reporting)
- Consulting Question Acceptance: ≥50% per module
- Follow-up Success Rate: ≥70% (answered question led to resolution)
- Consulting Question Quality: ≥85% relevant (manual audit)
- User Satisfaction (inferred): 75%+ (target increase from 62%)

### Rollback Triggers (Immediate Action)
- Accuracy <70% → Disable consulting for affected module
- Engagement <1.15x → Investigate question quality
- IDK Rate ≥45% → Rollback consulting (not working)
- Consulting Acceptance <40% → Refine templates
- Critical Errors >0/day → Debug & fix before proceeding

---

## Stakeholder Communication Plan

### Weekly Status Reports (Every Friday)
**Recipients:** Product Lead, Engineering Lead, Analytics  
**Content:**
- Phase progress (% complete)
- Rollback trigger status (all green/red indicators)
- Key metrics (accuracy, engagement, IDK rate)
- Blockers or issues
- Decision needed? (yes/no)

### Decision Gates (Fri End-of-Week, 1 hour each)
**Phase 0 → 1 (Aug 15):** Framework + rollout design review  
**Phase 1 → 2 (Aug 22):** RCS A/B test results  
**Phase 2 → 3 (Aug 29):** Cross-module impact  
**Phase 3 → 4 (Sep 7):** Full rollout stability + Phase 4 planning

### Post-Launch Optimization (Sep 8+)
**Monthly Reports:** Calibration results, template optimization, module-specific tuning  
**Ad-hoc:** Issues, rollback triggers, major changes

---

## Risk Mitigation Checklist

- [ ] Feature flags enable instant rollback (no code deploy)
- [ ] Accuracy gate ≥70% enforced at each phase
- [ ] A/B testing framework prevents blind rollout
- [ ] Regression test suite (50+) run before Phase 4
- [ ] Consulting question quality audit ≥85%
- [ ] Daily monitoring dashboard (rollback triggers)
- [ ] Stakeholder reviews at each phase gate
- [ ] Rollback procedure documented + tested
- [ ] Post-Phase 3 stability check (48+ hours green)
- [ ] Phase 4 optimization plan ready

---

**Document Version:** 1.0  
**Date Prepared:** August 11, 2026  
**Status:** Ready for Phase 0 Kickoff  
**Next Review:** Friday, August 15, 2026 (Phase 0 completion)

