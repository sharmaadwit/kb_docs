# Consulting-Tone Implementation: Decision Tree & Strategic Gates

**Quick Reference:** Use this to navigate Phase 0 → Phase 1 → Phase 2/3 decisions  
**Document:** CONSULTING_TONE_OPTIMAL_IMPLEMENTATION_SEQUENCE.md (full details)

---

## DECISION TREE (Visual)

```
┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 0: RCS-Only MVP (Week 1)                                      │
│ - Implement consulting-tone answers for RCS module ONLY            │
│ - Keep WhatsApp, Campaigns, Bot Studio unchanged                   │
│ - Measure: Engagement lift + Accuracy hold                          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│ DECISION GATE 1 (End of Week 1): Should Phase 1 proceed?           │
│                                                                      │
│ Success Criteria:                                                   │
│  ✓ Engagement lift ≥ 20% (follow-up rate: 8% → ≥9.6%)            │
│  ✓ Accuracy hold (IDK rate ≤ baseline + 5pp)                      │
│  ✓ Application accuracy ≥ 70% (maintained)                         │
│                                                                      │
│ Paths:                                                              │
│  → YES: All criteria met → PROCEED to Phase 1                       │
│  → MAYBE: Engagement 15-20% + accuracy held → PROCEED with monitoring │
│  → NO: Engagement < 15% OR accuracy regressed → STOP + Investigate │
└────────────┬───────────────────────────────────────────────┬────────┘
             │                                               │
      YES/MAYBE                                            NO
             │                                               │
             ↓                                               ↓
    ┌──────────────────┐                          ┌─────────────────┐
    │ PROCEED          │                          │ STOP + DEBUG    │
    │ PHASE 1 (Wk 2)   │                          │                 │
    │                  │                          │ - Investigate   │
    │                  │                          │   why not working
    │                  │                          │ - Revert RCS    │
    │                  │                          │ - Consider P0.v2│
    │                  │                          └─────────────────┘
    └────────┬─────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────────────────┐
│ PHASE 1: Soft Gradient Confidence Tiers (Week 2)                    │
│ - Replace binary 0.5 threshold with 4 tiers (0.80/0.60/0.40/0.0)   │
│ - Apply system-wide: RCS + Campaigns + others                       │
│ - Measure: IDK rate, follow-up rate, calibration error              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────────┐
│ DECISION GATE 2 (End of Week 2): What's next?                      │
│                                                                      │
│ Success Criteria:                                                   │
│  ✓ IDK rate ≤ 30% (45.7% → 30%)                                   │
│  ✓ Follow-up rate ≥ 25% (8% → 25%+)                               │
│  ✓ Accuracy maintained ≥ 70% (NO regression)                       │
│  ✓ Calibration error ≤ ±0.08 (was ±0.18)                          │
│                                                                      │
│ Next Decision: Phase 2 vs Phase 3 vs Consolidate?                  │
│                                                                      │
│  ┌─ YES (all targets met)                                          │
│  │  → Choose: Phase 2 (consulting Qs) OR Phase 3 (context-gating)  │
│  │  → Logic: Look at engagement_lift ≥30% or accuracy_improve ≥15%│
│  │                                                                  │
│  ├─ PARTIAL (some targets met, e.g., follow-up 20% not 25%)       │
│  │  → Continue Phase 1 with monitoring                             │
│  │  → Investigate: Why not hitting all targets?                    │
│  │  → Decide Phase 2/3 after investigation                         │
│  │                                                                  │
│  └─ CRITICAL (accuracy regressed >5pp)                             │
│     → ROLLBACK Phase 1 immediately                                  │
│     → Debug root cause                                              │
│     → Do NOT proceed to Phase 2/3                                   │
└────────────┬──────────────────────────────────────────────┬────────┘
             │                                              │
      YES/PARTIAL                                      CRITICAL
             │                                              │
             ↓                                              ↓
    ┌──────────────────────────┐                ┌──────────────────┐
    │ CHOOSE: Phase 2 or 3?    │                │ ROLLBACK         │
    │                          │                │                  │
    │ IF engagement_lift ≥30%  │                │ - Revert Phase 1 │
    │  → Phase 2 (consulting Qs)                │ - Debug issue    │
    │                          │                │ - Stay at Phase 0│
    │ IF accuracy_improve ≥15% │                │ - Iterate later  │
    │  → Phase 3 (context-gate)│                │                  │
    │                          │                └──────────────────┘
    │ IF both positive         │
    │  → Do BOTH (sequenced)   │
    │                          │
    │ IF neither high          │
    │  → Consolidate Phase 1   │
    │    Archive 2 & 3         │
    └────────┬─────────────────┘
             │
             ↓
    ┌──────────────────────────┐
    │ PHASE 2 or 3 (Wk 3-4)    │
    │ (Conditional on decision)│
    │                          │
    │ P2: Diagnostic questions │
    │ P3: Context-gating       │
    │ P2+P3: Both (sequenced)  │
    └────────┬─────────────────┘
             │
             ↓
    ┌──────────────────────────┐
    │ FINAL DECISION (Wk 4)    │
    │                          │
    │ Consolidate into        │
    │ standard implementation │
    │         OR              │
    │ Archive for future      │
    └──────────────────────────┘
```

---

## QUICK DECISION REFERENCE

### Decision Gate 1: "Should we do Phase 1?"

| Metric | Success Threshold | Your Data | ✓ or ✗ |
|--------|-------------------|-----------|--------|
| **Engagement Lift** | ≥20% relative (8% → ≥9.6% follow-up) | ? | |
| **Accuracy Hold** | IDK ≤ baseline + 5pp | ? | |
| **Application Accuracy** | ≥70% (maintained) | ? | |

**Decision:** 
- ✓ All three → **PROCEED to Phase 1**
- ✓ Two + engagement ≥15% → **PROCEED with monitoring**
- ✗ Any failed → **STOP, investigate**

---

### Decision Gate 2: "What comes after Phase 1?"

| Scenario | What It Means | Action |
|----------|---------------|--------|
| **All Phase 1 targets met** | Soft gradient working well system-wide | Choose Phase 2 (engagement) or Phase 3 (accuracy) |
| **IDK ↓, follow-up ↑, but not all targets** | Partial success; investigate why | Keep Phase 1; delay Phase 2/3; reanalyze |
| **Accuracy regressed >5pp** | CRITICAL: Consulting tone made answers worse | **ROLLBACK Phase 1** immediately; debug |

---

### Decision Gate 3: "Phase 2 vs Phase 3?"

| Choice | When to Pick | What It Does | Expected Lift |
|--------|--------------|--------------|--------|
| **Phase 2: Consulting Questions** | Engagement_lift ≥30% | Ask diagnostic Qs instead of IDK | Follow-up rate 40-50%+ |
| **Phase 3: Context-Gating** | Accuracy_improve ≥15% | Track user context; adjust confidence | Calibration error ±0.04 |
| **Both (Sequenced)** | Both metrics positive | Phase 2 week 3, Phase 3 week 4 | Multiplicative impact |
| **Neither (Consolidate)** | Both metrics weak | Keep Phase 1; archive 2 & 3 | Baseline Phase 1 gains |

---

## KEY METRICS CHEAT SHEET

### Engagement Metrics (Measure Real-Time)

```
IDK Rate = % of queries returning "I don't know"
  Current: 45.7%
  Phase 0 Target: 35-40%
  Phase 1 Target: 25-30%

Follow-Up Rate = % of responses followed by user turn within 5min
  Current: 8%
  Phase 0 Target: 15-25%
  Phase 1 Target: 30-50%

Avg Conversation Depth = turns per session
  Current: 1.2 turns
  Phase 0 Target: 1.5-2.0
  Phase 1 Target: 2.5-3.5+
```

### Accuracy Metrics (Measure Weekly)

```
Calibration Error = |Reported Confidence - Actual User Satisfaction|
  Current: ±0.18 (overconfident)
  Phase 1 Target: ±0.04 (well-calibrated)

False Negative Rate = % IDK when search score > 5
  Current: ~15-20% (estimated)
  Phase 1 Target: <5%

Application Accuracy = % users confirm "yes, that worked"
  Current: ~70%
  Phase 1 Target: ≥70% (hold steady, no regression)
```

### Business Metrics (Measure Monthly)

```
Repeat User Rate = % with 2+ conversations in 30 days
  Current: 12%
  Phase 1+ Target: 20%+
```

---

## WHEN TO ROLLBACK

🚨 **IMMEDIATE ROLLBACK IF:**

1. **Accuracy regression > 5pp** (application accuracy drops below 65%)
   - Consulting tone is making wrong answers, not better ones
   - Revert to baseline immediately

2. **Confidence calibration error gets WORSE** (±0.25+)
   - Means confidence scores now less trustworthy
   - May need to revisit how confidence is computed

3. **Abandonment rate increases** (users stop mid-session)
   - Consulting questions may be backfiring
   - Revert and investigate

4. **Critical errors in Langfuse** (>5% of responses missing data)
   - Can't measure properly; can't continue
   - Fix data pipeline before proceeding

---

## PHASE 0 SUCCESS CRITERIA (RCS Only, Week 1)

| Criterion | Target | Pass? | Action If Fail |
|-----------|--------|-------|--------|
| Engagement lift (follow-up) | ≥20% relative | ? | Extend P0 1 week |
| Accuracy hold (IDK) | ≤baseline + 5pp | ? | Investigate + stop |
| Application accuracy | ≥70% maintained | ? | Rollback immediately |
| No critical errors | 0 errors | ? | Fix + retest |
| RCS module stability | <0.1% error rate | ? | Revert feature flag |

**Go/No-Go Decision:** ✓✓✓ on all five → **PROCEED to Phase 1**

---

## PHASE 1 SUCCESS CRITERIA (System-Wide, Week 2)

| Criterion | Target | Why It Matters | Pass? | Action If Fail |
|-----------|--------|--------|-------|--------|
| IDK rate | 25-30% (from 45.7%) | Reduces false dismissal | ? | Keep monitoring |
| Follow-up rate | ≥25% (from 8%) | Shows engagement lift | ? | Investigate Q quality |
| Calibration error | ≤±0.08 (from ±0.18) | Confidence more honest | ? | Review confidence calc |
| Accuracy maintained | ≥70% (no regression) | CRITICAL: no harm | ? | **ROLLBACK** |
| Repeat users | Trend up (was 12%) | Long-term stickiness | ? | Monitor next month |

**Go/No-Go Decision:** ✓✓✓ on top 4 (accuracy is critical) → **PROCEED to Phase 2/3**

---

## WHO DECIDES WHAT

| Decision | Who | Timeline | Criteria |
|----------|-----|----------|----------|
| Phase 0 implementation | Engineer | Mon-Fri Wk 1 | Code review pass |
| Phase 0 rollout | DevOps | Thu Wk 1 | Staging tests pass |
| Phase 0 go/no-go | PM + Tech Lead | Fri Wk 1 | Metrics from Gate 1 |
| Phase 1 implementation | Engineer | Mon-Tue Wk 2 | Gate 1 passed |
| Phase 1 go/no-go | PM + Tech Lead | Fri Wk 2 | Metrics from Gate 2 |
| Phase 2 vs 3 choice | Product + Analytics | Fri Wk 2 | Gate 2 + engagement data |
| Phase 2/3 implementation | Engineer | Wk 3-4 | Decision from above |
| Final consolidation | PM + Tech Lead | Fri Wk 4 | Phase 2/3 results |

---

## TEMPLATE: DECISION GATE REPORT

Use this at each gate (End of Week 1, End of Week 2, End of Week 4):

```
═══════════════════════════════════════════════════════════════
DECISION GATE [N] REPORT: [Phase Name] Impact
Date: [Date]
Period: [Start] to [End]
═══════════════════════════════════════════════════════════════

ENGAGEMENT METRICS
──────────────────
IDK Rate:           [Before] → [After]  (Target: [Target])  [✓/✗]
Follow-Up Rate:     [Before] → [After]  (Target: [Target])  [✓/✗]
Avg Turns/Session:  [Before] → [After]  (Target: [Target])  [✓/✗]

ACCURACY METRICS
────────────────
Calibration Error:  [Before] → [After]  (Target: [Target])  [✓/✗]
False Negative Rate:[Before] → [After]  (Target: [Target])  [✓/✗]
Application Acc:    [Before] → [After]  (Target: [Target])  [✓/✗]

RECOMMENDATION
──────────────
Gate Passed: [YES / NO / MAYBE]
Recommendation: [PROCEED to Phase X / EXTEND Phase X / STOP + DEBUG]
Confidence Level: [HIGH / MEDIUM / LOW]

NOTES
─────
[Key findings, anomalies, follow-ups]

DECISION
────────
Authorized By: [Name]
Date Approved: [Date]
Next Phase: [Phase X / On Hold / Canceled]
═══════════════════════════════════════════════════════════════
```

---

## DOCUMENT MAPPING

For more details, see:

| Topic | Document |
|-------|----------|
| Full implementation sequence | CONSULTING_TONE_OPTIMAL_IMPLEMENTATION_SEQUENCE.md |
| Impact analysis (theory) | consulting_tone_impact_analysis.md |
| Technical implementation | CONSULTING_TONE_IMPLEMENTATION_TECHNICAL.md |
| RCS testing framework | RCS_CONSULTING_QUESTIONS_TEST.md |
| Stability/risk analysis | CONSULTING_TONE_STABILITY_RISK_ANALYSIS.md |

---

**Status:** Ready for implementation  
**Next Step:** Approval from stakeholders → Execute Phase 0
