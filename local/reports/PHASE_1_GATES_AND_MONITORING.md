# Phase 1: Consulting-Tone Pilot — Gates & Monitoring Dashboard

**Date:** 2026-08-11 (Pre-pilot planning)  
**Phase Duration:** 1 week  
**Deployment:** RCS module only (A/B test 50/50 traffic)  
**Status:** Ready to launch (awaiting code design completion)

---

## Success Criteria & Gates

### Hard Gates (Must Pass to Proceed to Phase 2)

**Gate 1: Engagement Lift**
- **Target:** Multi-turn conversation % ≥ 9.6% (20% lift from 8% baseline)
- **Measure:** % of conversations with 2+ turns
- **Current baseline:** ~8% (from dashboard)
- **Success:** Consulting reduces single-turn conversations
- **Trigger rollback if:** Multi-turn % stays ≤ 8.5% after 3 days

**Gate 2: Accuracy Hold**
- **Target:** RCS module accuracy ≥ 65% (acceptable 5pp regression from ~70% baseline)
- **Measure:** % of answers user marked as helpful / total answers
- **Current baseline:** ~70% (RCS module)
- **Success:** Consulting doesn't degrade accuracy below 65%
- **Trigger rollback if:** Accuracy drops below 62% or continues declining after 2 days

**Gate 3: Consulting Question Effectiveness**
- **Target:** Consulting questions → resolution ≥ 50%
- **Measure:** % of consulting question conversations that resolve without escalation
- **Definition:** "Resolution" = user marks final answer as helpful, or stops asking within 2 turns
- **Success:** Diagnostic questions actually help users
- **Trigger rollback if:** Resolution rate < 35% (questions are friction, not value)

**Gate 4: Module Routing Stability**
- **Target:** Module detection accuracy ≥ 90%
- **Measure:** % of queries correctly routed to intended module
- **Current baseline:** ~95%
- **Success:** Consulting tone doesn't confuse module detection
- **Trigger rollback if:** Routing accuracy drops below 88%

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

```
RCS Module (Consulting Tone - 50% traffic)
├─ Queries processed: [count]
├─ Answer rate: [%] (target ≥60%)
├─ IDK rate: [%] (target ≤30%, expect slight increase initially)
├─ Multi-turn %: [%] (target ≥9.6%)
├─ Avg confidence: [score] (monitor for major shifts)
├─ Response time: [ms] (target <2000ms)
└─ Errors/timeouts: [count] (should be 0 or minimal)

RCS Module (Control - Problem-Solution - 50% traffic)
├─ Queries processed: [count]
├─ Answer rate: [%]
├─ IDK rate: [%]
├─ Multi-turn %: [%]
├─ Avg confidence: [score]
├─ Response time: [ms]
└─ Errors/timeouts: [count]

Comparison
├─ Engagement lift: (Consulting multi-turn % - Control multi-turn %)
├─ Accuracy delta: (Consulting answer rate - Control answer rate)
├─ Routing accuracy: Module detection success %
└─ Alert: Any metric crosses threshold?
```

### Daily Summary (EOD)

| Metric | Consulting | Control | Difference | Status |
|--------|-----------|---------|-----------|--------|
| Multi-turn % | X% | Y% | +Z% | ✅/⚠️/❌ |
| Answer rate | X% | Y% | ±Z% | ✅/⚠️/❌ |
| IDK rate | X% | Y% | ±Z% | ✅/⚠️/❌ |
| Routing accuracy | X% | Y% | N/A | ✅/⚠️/❌ |
| Avg satisfaction | X% | Y% | ±Z% | ℹ️ (monitor) |
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
- If all gates passing: expand sample to 100% of RCS traffic (move from 50/50 to 100% consulting)
- If accuracy trending down: plan rollback; don't expand

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
