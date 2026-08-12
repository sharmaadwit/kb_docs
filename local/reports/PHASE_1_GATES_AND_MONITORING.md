# Phase 1: Consulting-Tone Pilot — Gates & Monitoring Dashboard

**Date:** 2026-08-11 (Pre-pilot planning, revised same day)  
**Phase Duration:** 1 week  
**Deployment:** **Two modules, tracked as independent signals — RCS + Bot Studio** (A/B test 50/50 traffic within each)  
**Status:** Ready to launch (awaiting code design completion)

---

## Why Two Modules, Tracked Separately

RCS alone was the original plan, but RCS traffic is campaign-driven: marketing sends generate bursts of near-identical templated queries. That pollutes the engagement/accuracy signal — you'd be measuring campaign response, not consulting-tone effectiveness. Bot Studio (Journey Builder) was added as the primary clean signal:

| Module | Volume (30d) | Answer Rate | IDK Rate | Role in Phase 1 |
|---|---|---|---|---|
| **Bot Studio** | 60 | 81.7% | 18.3% | **Primary gate signal** — organic traffic, real baseline, top-3 by volume |
| **RCS** | Low, bursty | — (no stable baseline) | — | Secondary/directional signal — monitored, not used alone for go/no-go |

**Gate decisions in this document are made per-module, using Bot Studio's baseline as the primary go/no-go signal.** RCS metrics are still logged and reviewed, but a good or bad RCS week alone does not trigger expansion or rollback — its traffic is too templated to trust in isolation. If RCS and Bot Studio disagree, investigate before deciding; don't average them together.

---

## Success Criteria & Gates

Gates below are stated in terms of Bot Studio's real baseline (the trustworthy signal). Apply the same gate logic to RCS directionally, but weight Bot Studio's result more heavily in the go/no-go call.

### Hard Gates (Must Pass to Proceed to Phase 2)

**Gate 1: Engagement Lift**
- **Target:** Multi-turn conversation % ≥ 20% relative lift over each module's own baseline
- **Measure:** % of conversations with 2+ turns, computed separately for Bot Studio and RCS
- **Current baseline:** ~8% platform-wide (Bot Studio-specific baseline to be confirmed from Day 1 control-arm data, since it wasn't previously broken out)
- **Success:** Consulting reduces single-turn conversations in Bot Studio (primary), directionally similar in RCS
- **Trigger rollback (Bot Studio) if:** Multi-turn % shows no lift over its own baseline after 3 days
- **RCS:** Log only; do not gate off RCS engagement alone (campaign bursts can fake a lift or mask one)

**Gate 2: Accuracy Hold**
- **Target (Bot Studio):** Accuracy ≥ 76% (acceptable ~5.7pp regression from 81.7% baseline)
- **Target (RCS):** Directional only — no reliable baseline to gate against; watch for gross regression (e.g., answer rate cut in half)
- **Measure:** % of answers user marked as helpful / total answers
- **Success:** Consulting doesn't degrade Bot Studio accuracy below 76%
- **Trigger rollback (Bot Studio) if:** Accuracy drops below 72% or continues declining after 2 days
- **Trigger investigation (RCS) if:** Answer rate drops >15pp vs its own control arm that week

**Gate 3: Consulting Question Effectiveness**
- **Target:** Consulting questions → resolution ≥ 50%, evaluated per-module
- **Measure:** % of consulting question conversations that resolve without escalation
- **Definition:** "Resolution" = user marks final answer as helpful, or stops asking within 2 turns
- **Success:** Diagnostic questions actually help users — this should be clearest in Bot Studio, where questions are genuinely conditional ("which trigger type?", "webhook or native integration?")
- **Trigger rollback (Bot Studio) if:** Resolution rate < 35% (questions are friction, not value)
- **RCS:** Log resolution rate; low RCS resolution may just reflect templated queries that don't need clarification — don't rollback off this alone

**Gate 4: Module Routing Stability**
- **Target:** Module detection accuracy ≥ 90%, for both RCS and Bot Studio queries
- **Measure:** % of queries correctly routed to intended module
- **Current baseline:** ~95%
- **Success:** Consulting tone doesn't confuse module detection for either module
- **Trigger rollback if:** Routing accuracy drops below 88% for either module (this one DOES apply symmetrically — routing errors are a code-correctness signal, not a traffic-quality signal)

### Soft Gates (Monitor, but won't trigger rollback alone)

**Gate 5: User Satisfaction**
- **Target:** Thumbs up/down ratio ≥ 70%
- **Measure:** % of answers user thumbed up (of those with feedback)
- **Current baseline:** ~68%
- **Insight:** Consulting might improve satisfaction but may take longer to measure

**Gate 6: Response Time**
- **Target:** Response time <2 seconds (consulting shouldn't add latency)
- **Measure:** API response time from query to answer
- **Current baseline:** ~1.5 seconds
- **Success:** Consulting composition doesn't add overhead
- **Note:** If >2.5s consistently, investigate code efficiency

---

## Daily Monitoring Dashboard

### Hourly Metrics (Real-time)

Track each module's consulting vs. control arm independently — do not merge RCS and Bot Studio numbers.

```
Bot Studio (Consulting Tone - 50% traffic)  [PRIMARY SIGNAL]
├─ Queries processed: [count]
├─ Answer rate: [%] (target ≥76%, vs 81.7% baseline)
├─ IDK rate: [%] (target ≤24%, vs 18.3% baseline)
├─ Multi-turn %: [%] (target: +20% relative vs control arm)
├─ Avg confidence: [score] (monitor for major shifts)
├─ Response time: [ms] (target <2000ms)
└─ Errors/timeouts: [count] (should be 0 or minimal)

Bot Studio (Control - Problem-Solution - 50% traffic)
├─ Queries processed: [count]
├─ Answer rate: [%] (should track ~81.7% baseline)
├─ IDK rate: [%]
├─ Multi-turn %: [%] (this establishes the true baseline — not previously broken out per-module)
├─ Avg confidence: [score]
├─ Response time: [ms]
└─ Errors/timeouts: [count]

RCS (Consulting Tone - 50% traffic)  [SECONDARY / DIRECTIONAL]
├─ Queries processed: [count] (expect low, bursty)
├─ Answer rate: [%] (no reliable baseline — compare to its own control arm only)
├─ IDK rate: [%]
├─ Multi-turn %: [%]
├─ Avg confidence: [score]
├─ Response time: [ms]
└─ Errors/timeouts: [count]

RCS (Control - Problem-Solution - 50% traffic)
├─ Queries processed: [count]
├─ Answer rate: [%]
├─ IDK rate: [%]
├─ Multi-turn %: [%]
├─ Avg confidence: [score]
├─ Response time: [ms]
└─ Errors/timeouts: [count]

Comparison (per module, not blended)
├─ Bot Studio engagement lift: (Consulting multi-turn % - Control multi-turn %)
├─ Bot Studio accuracy delta: (Consulting answer rate - Control answer rate)
├─ RCS engagement lift: (directional only)
├─ RCS accuracy delta: (directional only)
├─ Routing accuracy: Module detection success %, both modules
└─ Alert: Any Bot Studio metric crosses threshold? (RCS crossing alone = investigate, not auto-rollback)
```

### Daily Summary (EOD)

**Bot Studio (primary gate signal)**

| Metric | Consulting | Control | Difference | Status |
|--------|-----------|---------|-----------|--------|
| Multi-turn % | X% | Y% | +Z% | ✅/⚠️/❌ |
| Answer rate | X% | Y% | ±Z% | ✅/⚠️/❌ |
| IDK rate | X% | Y% | ±Z% | ✅/⚠️/❌ |
| Routing accuracy | X% | Y% | N/A | ✅/⚠️/❌ |
| Avg satisfaction | X% | Y% | ±Z% | ℹ️ (monitor) |
| Response time | Xms | Yms | ±Zms | ✅/⚠️ |

**RCS (secondary / directional signal)**

| Metric | Consulting | Control | Difference | Status |
|--------|-----------|---------|-----------|--------|
| Multi-turn % | X% | Y% | +Z% | ℹ️ (log, don't gate) |
| Answer rate | X% | Y% | ±Z% | ℹ️ (log, don't gate) |
| IDK rate | X% | Y% | ±Z% | ℹ️ (log, don't gate) |
| Routing accuracy | X% | Y% | N/A | ✅/⚠️/❌ (this one gates) |
| Response time | Xms | Yms | ±Zms | ✅/⚠️ |

---

## Rollback Triggers & Recovery

### Automatic Rollback (Immediate)

| Trigger | Threshold | Action | Recovery |
|---------|-----------|--------|----------|
| **Accuracy drops** | <62% (>8pp regression) | Stop A/B test, revert to 100% control | Investigate code, fix, retry |
| **Consulting questions fail** | <35% resolution rate | Stop question-based routing, keep full answers only | Redesign question prompts, retry |
| **Routing breaks** | <88% module accuracy | Disable consulting for that module | Debug routing logic |
| **Errors spike** | >5% error/timeout rate | Immediate pause, investigate | Check logs, fix bugs |
| **Latency increases** | >2.5s avg response time | Revert, optimize consulting code | Profile code, improve efficiency |

### Manual Intervention Points

**Day 1 EOD:**
- If multi-turn % shows no improvement: investigate whether consulting questions are appearing or if users skipping them
- If accuracy drops >3pp: might be normal variance; monitor 24h more before rollback

**Day 2-3:**
- If still no engagement lift: consult-tone might not be engaging enough; consider redesigning prompts
- If accuracy stabilizes at 65-67%: acceptable for consulting trade-off; continue

**Day 4-5:**
- If Bot Studio gates passing: expand sample to 100% of Bot Studio traffic (move from 50/50 to 100% consulting); use RCS data directionally to corroborate, not to drive the decision alone
- If Bot Studio accuracy trending down: plan rollback for Bot Studio; don't expand. RCS accuracy trending down without a Bot Studio signal is not sufficient grounds for rollback on its own — investigate whether it's a campaign artifact first

---

## Test Queries (Pre-Deployment)

Before launching Phase 1, test these queries against both old and new answer generation:

### RCS-Specific Queries (Should benefit from consulting tone)

```
1. "How do I set up my first RCS campaign?"
   Expected old: Problem-solution (steps 1-2-3)
   Expected new: Diagnostic (what's your goal?) → tailored path

2. "What's the ROI I should expect from RCS?"
   Expected old: Facts (92% open rate, 3.2x conversion)
   Expected new: Context-aware (depends on industry, segment...)

3. "RCS vs WhatsApp — which should I use?"
   Expected old: Comparison table
   Expected new: Diagnostic path (depend on your use case: A, B, or C?)

4. "How do I handle RCS delivery failures?"
   Expected old: Troubleshooting steps
   Expected new: Error diagnosis (what error?) → specific fix

5. "Can I use RCS for customer support?"
   Expected old: Yes/No answer
   Expected new: Context check (depends on volume, support model...)
```

### Bot Studio-Specific Queries (Primary gate signal — should benefit most)

```
1. "How do I build a journey that sends different messages based on user response?"
   Expected old: Generic conditional-routing steps
   Expected new: Diagnostic (single condition or multiple? AND/OR logic?) → tailored pattern

2. "What's the best way to collect a user's info across multiple steps?"
   Expected old: Generic multi-step form steps
   Expected new: Context-aware (depends whether you need to persist across sessions)

3. "How do I handle API failures inside a journey?"
   Expected old: Generic retry-logic steps
   Expected new: Diagnostic (timeout vs 5xx vs invalid response?) → specific handling

4. "Should I use buttons or free text for user responses?"
   Expected old: Pros/cons list
   Expected new: Diagnostic path (how many options? need exact parsing?) → recommendation

5. "How do I prevent my bot from looping on the same question?"
   Expected old: Generic loop-counter steps
   Expected new: Context check (is this FAQ-repeat or a stuck decision node?) → targeted fix
```

### Quality Checks

For each query above:
- [ ] Consulting version still answers the core question (accuracy)
- [ ] Consulting version is longer but not overwhelming (readability)
- [ ] Consulting version has follow-up prompt (engagement)
- [ ] Old version still works (control group baseline)
- [ ] Confidence scores don't drop dramatically (consistency)

---

## Engagement Metrics Definition

### Multi-Turn Conversation

**Definition:** Conversation where user asks 2+ related questions or the bot asks 2+ clarifying questions.

**Examples:**
```
✅ Multi-turn:
  User: "How do I set up RCS?"
  Bot: "It depends on your platform. Are you using our API or dashboard?"
  User: "Dashboard"
  Bot: [specific dashboard steps]
  
✅ Multi-turn:
  User: "What's the difference between RCS and SMS?"
  Bot: [Answer with follow-up] "Tell me more about your use case..."
  User: "We send promotions"
  Bot: [tailored recommendation]

❌ Single-turn:
  User: "What's the open rate for RCS?"
  Bot: "92%"
  
❌ Single-turn:
  User: "How do I fix error 131000?"
  Bot: [Complete error guide]
  (No follow-up question = user got answer and left)
```

**Measurement:** Log `conversation_turns` field in Langfuse telemetry. Multi-turn % = conversations with turns ≥ 2 / total.

---

## Confidence Score Analysis

### Expected Changes Post-Consulting

| Scenario | Old Confidence | New Confidence | Reason |
|----------|---|---|---|
| **Very confident match** (query match 0.85+) | 3.5+ | 3.5+ (unchanged) | High confidence answers don't change |
| **Medium confident** (query match 0.60-0.79) | 2.8 | 2.9 (slight increase) | Consulting adds context → user perceives more completeness |
| **Low confident** (query match <0.60) | 1.8 | 2.2+ (if diagnostic helps) | Diagnostic question → user can clarify → higher perceived confidence |

**Monitor for:** If consulting answers show confidence scores 0.3-0.5 lower than control, investigation needed (consulting might be under-confident).

---

## Success Milestones

### Day 1 (Launch Day)

✅ **Goals:**
- A/B split deployed (50/50 traffic on RCS)
- Consulting questions appearing in 50% of RCS conversations
- No errors/crashes
- Baseline metrics established

⚠️ **Checkpoints:**
- Are consulting questions actually reaching users?
- Is the toggle working (50/50 split validated)?
- Are Langfuse logs capturing consulting decisions?

### Day 2-3 (Early Results)

✅ **Goals:**
- Multi-turn % trending up (even if not yet at target)
- Accuracy holding (no >3pp drops yet)
- Response time stable

⚠️ **Checkpoints:**
- If multi-turn flat: consulting questions might not be reaching users; check logs
- If accuracy drops >3pp: investigate whether new content from P2 is interfering
- Are user satisfaction scores staying stable?

### Day 4-5 (Mid-Pilot)

✅ **Goals:**
- Multi-turn ≥ 9.6% (gate 1 passing)
- Accuracy ≥ 65% (gate 2 passing)
- Consulting question resolution ≥ 50% (gate 3 passing)

⚠️ **Decision point:**
- If gates passing: expand to 100% consulting on RCS
- If gates failing: investigate root cause before rollback decision

### Day 6-7 (Final Check)

✅ **Goals:**
- All gates consistently passing over full week
- No regressions in other modules (spillover effect check)
- Ready to proceed to Phase 2 scale plan

⚠️ **Decision:**
- Proceed to Phase 2: expand to Channels, WhatsApp, Bot Studio
- OR: pause, refine consulting prompts, retry Phase 1
- OR: rollback, investigate, retry from scratch

---

## Escalation Path

**If consulting accuracy drops to 62-64%:**
- Option A: Keep but slow expansion (monitor daily)
- Option B: Revert to problem-solution, investigate
- Recommendation: Option B (accuracy floor is 70%, acceptable pilot regression is down to 65%, below that needs investigation)

**If multi-turn doesn't improve:**
- Possible cause: consulting questions not compelling enough
- Action: Review prompt engineering, rewrite questions to be more specific
- Retry: Try new prompts for 2 days, re-measure

**If routing breaks:**
- Immediate action: Disable consulting for that module
- Investigate: Does consulting composition confuse entity detection?
- Fix: Add routing pre-check before composition

---

## Artifacts & Logging

### What to Log in Langfuse

For each consulting-tone answer, log:
```
{
  "conversation_id": "...",
  "turn_number": 2,
  "query": "...",
  "answer_type": "problem_solution" | "consulting",
  "consulting_diagnostic_question": "...", # if consulting
  "consulting_options": ["A", "B", "C"],    # if consulting
  "consulting_recommended": "A",            # if consulting
  "confidence": 2.8,
  "module": "rcs",
  "query_overlap": 0.68,
  "is_follow_up": true,
  "user_thumbed": "up" | "down" | null,
  "response_time_ms": 1243,
  "routing_accuracy": true
}
```

### Daily Report Template

```markdown
# RCS Consulting-Tone Pilot — Day X Report

**Date:** 2026-08-12

## Metrics Summary
- Consulting queries: [N]
- Control queries: [N]
- Engagement lift: [multi-turn % delta]
- Accuracy delta: [answer rate delta]

## Gate Status
- ✅ Engagement: [X%] (target 9.6%)
- ✅ Accuracy: [X%] (target ≥65%)
- ✅ Consulting resolution: [X%] (target ≥50%)
- ✅ Routing: [X%] (target ≥90%)

## Alerts
- [List any metrics crossing thresholds]

## Next Steps
- [Continue monitoring / Expand / Investigate / Rollback]
```

---

## Conclusion

Phase 1 pilot is designed to test consulting-tone engagement hypothesis with strict accuracy gates. If gates pass, proceed to Phase 2 (scale to other modules). If gates fail, rollback and investigate before retry.

**Ready to launch** when code design is complete and consulting-tone answer generation is implemented.

---

**Prepared by:** Phase 1 Planning  
**Date:** 2026-08-11  
**Next:** Await code design completion, then deploy A/B test
