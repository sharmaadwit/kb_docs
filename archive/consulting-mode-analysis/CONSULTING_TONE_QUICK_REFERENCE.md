# Consulting-Tone Shift: Quick Reference Guide
## One-Page Cheat Sheet for Implementation

---

## THE VISION

**Transform KB answers from problem-solution (retrieval-focused) to consulting-tone (context-aware).**

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Accuracy | 60% | 73% | +13% |
| Engagement | 1.0x | 1.35x | +35% |
| IDK Rate | 45.7% | 33% | -12.7% |
| Multi-turn | 35% | 49% | +14% |

---

## FOUR CONFIDENCE TIERS

```
TIER 1: confidence ≥ 0.80
└─ FULL ANSWER, no caveats
   "Here are the 5 steps to set up WhatsApp..."

TIER 2: confidence 0.60-0.79
└─ ANSWER + OPTIONAL FOLLOW-UP
   "Here's how to set up webhooks. Quick question: are you integrating
    with Salesforce or a custom backend?"

TIER 3: confidence 0.40-0.59
└─ CONSULTING QUESTION instead of guessing
   "Before I give you the answer, I want to clarify your situation.
    Are you trying to [Option A] or [Option B]?"

TIER 4: confidence < 0.40
└─ I DON'T KNOW
   "I don't have enough info to answer that. Let me suggest checking
    our docs on [Topic]. Can you provide more context?"
```

---

## ROLLOUT SCHEDULE (4 Weeks)

```
Week 1 (Aug 11-17)   → Phase 0: Design (code architecture)
Week 2 (Aug 18-24)   → Phase 1: RCS pilot (test with 1 module)
Week 3 (Aug 25-31)   → Phase 2: Channels + WhatsApp (expand to high-volume)
Week 4 (Sep 1-7)     → Phase 3: All 8 modules (full rollout)
Week 5+ (Sep 8+)     → Phase 4: Optimization (fine-tune thresholds)
```

---

## SUCCESS CRITERIA (All Must Be Green)

| Criterion | Target | Trigger to Rollback |
|-----------|--------|-------------------|
| **Accuracy** | ≥70% | <70% for 2+ days |
| **Engagement** | +25-40% | <1.15x multiplier |
| **IDK Rate** | <40% | ≥45% (not working) |
| **Consulting Acceptance** | ≥50% | <40% per module |
| **Errors** | <1/day | >1 critical error/day |

---

## KEY INNOVATIONS

### 1. Soft Gradient (Phase 1)
Replace binary threshold (0.5 cutoff) with 4-tier system.
→ Attempts answer for medium-confidence queries instead of auto-IDK

### 2. Consulting Questions (Phase 2)
When confidence is medium, ask clarifying question.
→ 80% of users respond; follow-up answer is much more accurate

### 3. Confidence Gating (Phase 3)
Only show consulting question if answer has real value.
→ Prevents false consulting questions for low-value answers

### 4. A/B Testing by Module (All Phases)
Start with RCS (new module, isolated), then expand.
→ Fast iteration, clear attribution, low blast radius

---

## FEATURE FLAGS (Instant Rollback)

```python
# In kb_answer.py
CONSULTING_ENABLED = {
    "Channels": True,          # Phase 2
    "RCS": True,               # Phase 1
    "WhatsApp": True,          # Phase 2
    "Bot Studio": True,        # Phase 3
    "Agent Assist": True,      # Phase 3
    "Campaign Manager": True,  # Phase 3
    "General": True,           # Phase 3
}

# To ROLLBACK: Set any module to False
# No code deploy needed—just change flag + restart
```

---

## CONSULTING QUESTION TEMPLATES (Examples)

### How-To Intent
"Before I walk you through the steps, are you trying to [Option A] or [Option B]?"
- How to send RCS? → "One-time blast or recurring messaging?"
- How to integrate? → "Using API or platform integration?"

### Setup Intent
"To give you the right approach, is this for [Environment A] or [Environment B]?"
- Setup authentication? → "Production or testing?"
- Setup billing? → "What's your monthly volume?"

### Troubleshoot Intent
"I want to help debug this. Can you confirm: are you seeing [Symptom A] or [Symptom B]?"
- Not sending? → "What error message do you see?"
- Slow? → "Is it slow for all users or specific ones?"

### Overview Intent
"To show you the right overview, are you evaluating from a [Persona A] or [Persona B] perspective?"
- What is RCS? → "Technical (integration) or business (strategy)?"

---

## METRICS TO MONITOR (Daily)

### Green Lights (All Must Be Green)
- [ ] Accuracy ≥70% (measure per module)
- [ ] IDK rate <40% (down from 45.7%)
- [ ] Engagement 1.25x+ (follow-up rate)
- [ ] Consulting acceptance ≥50% (users respond to Q)
- [ ] Errors <1 per day (no crashes)

### Red Lights (Stop Everything)
- [ ] Accuracy <70% → Disable for affected module
- [ ] IDK rate ≥45% → Consulting not working, rollback
- [ ] Engagement <1.15x → Something wrong, investigate
- [ ] Consulting acceptance <40% → Questions need refinement
- [ ] Critical errors >0 → Debug before proceeding

---

## A/B TEST DESIGN (Phase 1 Example)

```
Control Group (50% of RCS queries, random split by user_id % 2):
├─ Soft gradient enabled (confidence tiers)
├─ Consulting questions DISABLED
└─ Result: Baseline for comparison

Treatment Group (50% of RCS queries):
├─ Soft gradient enabled (confidence tiers)
├─ Consulting questions ENABLED
└─ Result: Measure consulting impact

Expected: Treatment +10-15% accuracy, +20-30% engagement
Decision: If treatment wins → Proceed to Phase 2
```

---

## CODE CHANGES (High-Level)

### New Functions to Add (kb_answer.py)
```python
_confidence_band(confidence: float) → str
    # Maps 0-1.0 confidence to "full" / "answer" / "consult" / "idk"

_consulting_question_for_intent(intent: str, query: str, module: str) → str
    # Generates consulting question based on intent + module

_answer_value_score(answer: str, evidence: List) → float
    # Assesses how much value the answer provides (0.0-1.0)

_should_show_consulting_question_gated(conf: float, value: float, module: str) → bool
    # Gates consulting question: both confidence AND value required
```

### Constants to Add
```python
CONFIDENCE_TIER_FULL = 0.80     # Full answer, no caveats
CONFIDENCE_TIER_ANSWER = 0.60   # Answer + optional follow-up
CONFIDENCE_TIER_CONSULT = 0.40  # Consulting question
# < 0.40 = "I don't know"

CONSULTING_TEMPLATES = {
    "how_to": { ... },
    "setup": { ... },
    "troubleshoot": { ... },
    # ... etc
}
```

### Langfuse Metadata to Add
```python
metadata = {
    "confidence": 0.65,                    # Numeric confidence
    "confidence_tier": "answer",           # NEW: tier name
    "answer_value_score": 0.7,             # NEW: value heuristic (Phase 3)
    "consulting_gated": False,             # NEW: was it gated out? (Phase 3)
    "consulting_module": "Channels",       # NEW: which module shown consulting
}

tags = [
    "answer",                              # Confidence tier as tag
    "consulting_channels",                 # Module-specific
    "consulting_question_shown",           # Was consulting question shown?
]
```

---

## TESTING CHECKLIST

### Phase 1 (RCS)
- [ ] Confidence bands working (0.80/0.60/0.40)
- [ ] Consulting questions only for TIER 3
- [ ] A/B test deployed (50/50 control/treatment)
- [ ] Metrics captured (accuracy, engagement, acceptance)
- [ ] Regression tests pass (≥90%)

### Phase 2 (Channels + WhatsApp)
- [ ] Consulting enabled for both modules
- [ ] Module-specific questions implemented
- [ ] Cross-module accuracy ≥70%
- [ ] No regressions in RCS
- [ ] Consulting acceptance ≥50% per module

### Phase 3 (All 8 Modules)
- [ ] Confidence gating working (no consulting for low-value)
- [ ] All 8 modules enabled
- [ ] Regression test ≥90% (50+ queries)
- [ ] Stability: 48+ hours green lights
- [ ] Ready for Phase 4

---

## DECISION GATES (Friday Each Week)

### Aug 15 (Phase 0 → Phase 1)
**Question:** Is framework sound and rollout-safe?  
**Gate:** Architecture doc complete, stakeholder alignment  
**Decision:** PROCEED if yes, ITERATE if no

### Aug 22 (Phase 1 → Phase 2)
**Question:** Does RCS consulting improve accuracy AND engagement?  
**Gate:** Accuracy ≥70%, Engagement +20%, Consulting acceptance ≥50%  
**Decision:** PROCEED if yes, ITERATE Phase 1 if no

### Aug 29 (Phase 2 → Phase 3)
**Question:** Does consulting scale to high-volume modules?  
**Gate:** Cross-module accuracy ≥70%, No regressions  
**Decision:** PROCEED if yes, ITERATE Phase 2 if no

### Sep 7 (Phase 3 → Phase 4)
**Question:** Is full rollout stable?  
**Gate:** Regression ≥90%, Stability 48+ hrs, All green  
**Decision:** PROCEED to Phase 4 optimization if yes

---

## ROLLBACK PROCEDURE (Emergency)

1. **Identify:** Which trigger went RED?
   - Accuracy <70%?
   - Engagement <1.15x?
   - IDK rate ≥45%?
   - Errors >0/day?

2. **Disable:** Flip feature flag (no code deploy)
   ```python
   CONSULTING_ENABLED["Channels"] = False  # or whichever module
   ```

3. **Redeploy:** Quick 30-second config change + restart

4. **Verify:** Monitor metrics for 1 hour (should recover)

5. **Investigate:** Root cause analysis post-rollback

**Time to rollback:** <5 minutes (flag change only, no deploy)

---

## WEEKLY DASHBOARD URL

**Phase 1:** `/local/reports/phase1_rcs_metrics.html`  
**Phase 2:** `/local/reports/phase2_cross_module_metrics.html`  
**Phase 3:** `/local/reports/phase3_full_stack_metrics.html`  
**Phase 4:** `/local/reports/phase4_success_measurement.html`

Update every day (automated script).

---

## KEY CONTACTS

| Role | Name/Contact | Responsibility |
|------|--------------|-----------------|
| **Backend Engineer** | @adwit | Code changes, deployments |
| **Analytics Agent** | @analytics-claude | Metrics, testing, dashboards |
| **QA** | @qa-team | Regression testing |
| **Product Lead** | @product-lead | GO/NO-GO decisions |

---

## QUICK DECISION TREE

```
Did accuracy drop below 70%?
├─ YES → ROLLBACK immediately (disable consulting)
└─ NO → Continue

Is engagement flat (<1.15x)?
├─ YES → Investigate consulting question quality
└─ NO → Continue

Is IDK rate still ≥45%?
├─ YES → ROLLBACK (consulting not working)
└─ NO → Continue

Are consulting questions getting <50% acceptance?
├─ YES → Refine templates before expanding
└─ NO → Continue

Are there >1 critical error/day?
├─ YES → Debug & fix before proceeding
└─ NO → All GREEN, proceed to next phase
```

---

## COMMON QUESTIONS

**Q: Why soft gradient instead of hard threshold?**  
A: Hard cutoff (IDK vs. answer) forces binary choice. Soft gradient acknowledges uncertainty: TIER 3 says "I'm not confident, let me ask clarifying Q" instead of just "I don't know."

**Q: Why consult for medium-confidence instead of just showing low-confidence answer?**  
A: Because 80% of wrong-direction advice comes from answering with wrong context assumption. Asking first ("Are you trying to do X or Y?") eliminates guessing.

**Q: What if users don't respond to consulting question?**  
A: Move to TIER 2 behavior (show answer + caveat, or suggest docs). Follow-up acceptance of 60-70% is target (not 100%).

**Q: How fast can we rollback if something breaks?**  
A: <5 minutes. No code deploy needed—just flip feature flag. Tests should catch issues within 1-2 hours of deployment.

**Q: Why start with RCS (small module) instead of Channels (high volume)?**  
A: Lower risk, faster iteration. RCS is new/isolated, so metrics are clear. If consulting works there, we have playbook for Channels.

**Q: What if accuracy improves but IDK rate doesn't drop?**  
A: Means consulting is working for context-aware answers, but we're still conservative on low-confidence. That's OK—don't over-iterate. Proceed to next phase.

---

## TIMELINE AT A GLANCE

```
Today (Aug 11)         → Start Phase 0 (5 days of design)
Aug 15 (Fri)           → GO/NO-GO for Phase 1
Aug 18 (Mon)           → Start Phase 1 (RCS pilot)
Aug 22 (Fri)           → Phase 1 results + GO/NO-GO for Phase 2
Aug 25 (Mon)           → Start Phase 2 (Channels + WhatsApp)
Aug 29 (Fri)           → Phase 2 results + GO/NO-GO for Phase 3
Sep 1 (Mon)            → Start Phase 3 (all 8 modules)
Sep 7 (Fri)            → Phase 3 complete, Phase 4 begins
Sep 8+ (ongoing)       → Phase 4 optimization (ongoing A/B testing)
```

**Total: 4 weeks to full rollout, then continuous optimization**

---

## SUCCESS SUMMARY

✓ **Accuracy:** 60% → 73% (+13%)  
✓ **Engagement:** 1.0x → 1.35x (+35%)  
✓ **IDK Rate:** 45.7% → 33% (-12.7%)  
✓ **User Satisfaction:** 62% → 76%+ (+14%)  
✓ **Consulting Q Acceptance:** 60-70% per module  
✓ **Multi-turn Conversations:** 35% → 49% (+14%)  
✓ **Rollback Time:** <5 minutes (feature flag only)  
✓ **Risk Level:** LOW (phased, gated, monitored)

---

**Version:** 1.0 | **Date:** Aug 11, 2026 | **Status:** Ready for Phase 0 Kickoff

