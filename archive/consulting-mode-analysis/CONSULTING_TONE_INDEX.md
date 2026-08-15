# Consulting-Tone Answer Generation Framework — Complete Index

**Date:** 2026-08-11  
**Status:** Framework specification complete (3 documents, 15K+ words)  
**Deliverables:** Strategic framework + technical implementation + real examples

---

## Document Overview

This package contains everything needed to design and implement a consulting-tone answer generation system for KB answers. It shifts from "Here's the solution" to "Here's what I see, why it matters, and how successful teams approach this."

### Three Core Documents

| Document | Purpose | Audience | Length |
|----------|---------|----------|--------|
| **CONSULTING_TONE_FRAMEWORK.md** | Strategic framework, answer anatomy, conditional logic patterns | Product, leadership, designers | ~8,000 words |
| **CONSULTING_ANSWER_IMPLEMENTATION.md** | Technical specs, Python data structures, code examples, rollout plan | Engineers, architects | ~5,000 words |
| **CONSULTING_ANSWER_EXAMPLES.md** | Real-world Q&A transformations (3 queries, Current → Minimal → Radical) | Product managers, copywriters | ~6,000 words |

---

## Quick Navigation

### Strategic Questions Answered

**Part 1: Core Differences**
- What changes in answer structure, tone, phrasing?
- How does context shift from feature-focused to customer-situation-focused?
- When should you admit uncertainty vs. give confident guidance?
- **Read:** `CONSULTING_TONE_FRAMEWORK.md` → Part 1

**Part 2: Answer Anatomy**
- Should answers include diagnosis, strategic context, multiple approaches, recommendations, and open questions?
- What does each section accomplish?
- How long should consulting answers be?
- **Read:** `CONSULTING_TONE_FRAMEWORK.md` → Part 2

**Part 3: Conditional Logic**
- When should you say "If you are X → path A; if you are Y → path B"?
- How do you detect which condition applies?
- When is branching helpful vs. confusing?
- **Read:** `CONSULTING_TONE_FRAMEWORK.md` → Part 3

**Part 4: Follow-Up Prompts**
- How to inject follow-up suggestions naturally (not as buttons)?
- Where should follow-ups appear in the narrative?
- What makes a follow-up feel like dialogue vs. a menu?
- **Read:** `CONSULTING_TONE_FRAMEWORK.md` → Part 4

**Part 5: Accuracy While Less Definitive**
- How do you maintain accuracy while using conditional language?
- How to tag confidence levels without sounding uncertain?
- When to admit limitations?
- **Read:** `CONSULTING_TONE_FRAMEWORK.md` → Part 5

**Part 6: Mock Answers**
- See 3 real examples: Current (problem-solution) → Minimal (structured) → Radical (full consulting)
- **Read:** `CONSULTING_TONE_FRAMEWORK.md` → Part 6

### Implementation Questions Answered

**Architecture**
- How does consulting mode integrate with existing `kb_answer.py`?
- Is it opt-in or automatic?
- What's the rollout strategy?
- **Read:** `CONSULTING_ANSWER_IMPLEMENTATION.md` → Part 1

**Data Structures**
- What does a consulting answer contain (internally)?
- How are approaches structured?
- How are open questions organized?
- **Read:** `CONSULTING_ANSWER_IMPLEMENTATION.md` → Part 2

**Core Functions**
- How does `_compose_consulting_answer()` work?
- What helper functions power it?
- How do you diagnose customer scenarios?
- **Read:** `CONSULTING_ANSWER_IMPLEMENTATION.md` → Part 3-4

**Testing & Rollout**
- What success metrics matter?
- How do you phase adoption?
- What could go wrong?
- **Read:** `CONSULTING_TONE_FRAMEWORK.md` → Part 7 + `CONSULTING_ANSWER_IMPLEMENTATION.md` → Part 6-7

### Real-World Examples

**Three Detailed Examples** (each with Current → Minimal → Radical transformations):

1. **API Integration Setup**
   - Current: Step-by-step, assumes one right way
   - Minimal: Surfaces 2 paths, mentions sync vs. async
   - Radical: 4 approaches (sync, async, cache, hybrid) with ROI impact, complexity, and evolution path
   - **Read:** `CONSULTING_ANSWER_EXAMPLES.md` → Example 1

2. **Channel Selection (SMS vs. WhatsApp vs. RCS)**
   - Current: Feature comparison, generic "choose based on audience"
   - Minimal: Adds cost/conversion metrics, conditional logic
   - Radical: 4 approaches (SMS-dominant, RCS-first, multi-channel, hybrid) with cost at scale, geography variance, and business ROI
   - **Read:** `CONSULTING_ANSWER_EXAMPLES.md` → Example 2

3. **Simple Definition (Prompt Node)**
   - Current: Definition + use case
   - Minimal: (skipped)
   - Radical: Even simple answers benefit from "when to use", trade-offs, and open question
   - **Read:** `CONSULTING_ANSWER_EXAMPLES.md` → Example 3

**Tone Markers Reference**
- Collection of phrases for diagnosis, strategy, conditions, uncertainty, recommendations, follow-ups
- Copy-paste ready for training consultants and engineers
- **Read:** `CONSULTING_ANSWER_EXAMPLES.md` → Tone Markers Reference

---

## Quick-Start Checklist

### For Product Managers / Decision Makers
- [ ] Read: `CONSULTING_TONE_FRAMEWORK.md` Part 1 (Core Differences) — 10 min
- [ ] Skim: `CONSULTING_ANSWER_EXAMPLES.md` → Example 1 or 2 — 5 min
- [ ] Decide: Does this tone shift align with your brand? (Yes → proceed)

### For Designers / UX
- [ ] Read: `CONSULTING_TONE_FRAMEWORK.md` Part 2 (Answer Anatomy) — 10 min
- [ ] Read: `CONSULTING_TONE_FRAMEWORK.md` Part 4 (Follow-Up Prompts) — 10 min
- [ ] Study: All 3 examples in `CONSULTING_ANSWER_EXAMPLES.md` — 15 min
- [ ] Task: Sketch 2-3 layout options for consulting answer (headers, trade-off formatting, open questions)

### For Engineers
- [ ] Read: `CONSULTING_ANSWER_IMPLEMENTATION.md` Part 1 (Architecture) — 5 min
- [ ] Read: `CONSULTING_ANSWER_IMPLEMENTATION.md` Part 2 (Data Structures) — 10 min
- [ ] Read: `CONSULTING_ANSWER_IMPLEMENTATION.md` Part 3-4 (Core Functions) — 20 min
- [ ] Code review: Check Python patterns against your codebase standards
- [ ] Estimate: How long to build? (Likely: 2 weeks)

### For Content/QA
- [ ] Read: `CONSULTING_ANSWER_EXAMPLES.md` completely — 20 min
- [ ] Task: Pick 5 current KB answers; rewrite in consulting tone (practice)
- [ ] Task: Review tone markers; create house style guide

### For Executives / Leadership
- [ ] Read: `CONSULTING_TONE_FRAMEWORK.md` Part 6 (Mock Answers) — 10 min
- [ ] Skim: `CONSULTING_TONE_FRAMEWORK.md` Part 8 (Success Metrics) — 5 min
- [ ] Decide: Is this worth the build effort? ROI?

---

## Key Insights Summary

### 1. Answer Anatomy (5 Sections)

Every consulting answer should include:

1. **Diagnosis** (1-3 sentences)
   - What scenario am I seeing?
   - Signals: "Based on your question, I'm seeing..."

2. **Strategic Context** (2-4 sentences)
   - Why does this matter to your business?
   - Metrics: Cost, speed, revenue, retention impact

3. **Multiple Approaches** (3-8 bullets per path)
   - 2-3 viable options with explicit trade-offs
   - Preconditions, strengths, risks for each
   - Complexity rating (Low/Medium/High)

4. **Recommended Path** (2-4 sentences)
   - Suggested starting point (not prescriptive)
   - Evolution path if context changes
   - Language: "I'd typically start with…"

5. **Open Questions** (3-5 grouped questions)
   - What unknowns refine the recommendation?
   - Grouped by category (audience, goals, ops, risks)
   - Invites dialogue: "Does this match your situation?"

### 2. Tonal Shifts

| Dimension | Old (Prescriptive) | New (Advisory) |
|-----------|-------------------|----------------|
| **Opening** | "Here's how to..." | "Let me first understand..." |
| **Options** | One right way | Multiple paths with trade-offs |
| **Risk** | Not mentioned | Explicit for each path |
| **Certainty** | "You must" | "I'd typically..." |
| **Uncertainty** | "I don't know" | "I'm less certain about X" |
| **Closing** | Answer ends | Dialogue invite |

### 3. Conditional Logic Patterns

Use "If you are X → path A" when:
- ✅ Each path has materially different outcomes (cost, complexity, time)
- ✅ You can detect which condition applies from query language or explicitly ask
- ✅ The choice is reversible (can switch paths later if needed)
- ✅ There's a default/recommended path

Don't use if:
- ❌ All paths are equally valid (just list them)
- ❌ Conditions are too vague ("if you care about quality")
- ❌ You're guessing the customer's situation (ask first)

### 4. Accuracy Maintenance

Maintain accuracy while being less definitive by:
1. **Confidence tagging:** Mark HIGH/MEDIUM/LOW based on KB evidence count
2. **Source transparency:** "Documented in 10+ case studies" vs. "One customer reported"
3. **Preconditions:** "Works best for [specific profile]" vs. universal claim
4. **Uncertainty admission:** "Less certain here, so I'd test first"
5. **Conditional language:** "One approach is…" vs. "You must…"
6. **Data anchoring:** Cite specific metrics ("92% open rates") not vague ("high")

### 5. Success Metrics

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| **Comprehension** | 4+ sections in each answer | Consulting answers are complete |
| **Engagement** | 40%+ follow-up questions | Users are dialoguing, not just implementing |
| **Accuracy** | Zero regressions vs. current | Safety first; no worse than before |
| **Satisfaction** | 80%+ "trusted advisor" rating | Tone should feel advisory, not pushy |
| **Performance** | <500ms additional latency | Speed doesn't suffer |

### 6. Rollout Phases

- **Phase 1 (Week 1):** Build + test on 5-10 queries
- **Phase 2 (Weeks 2-3):** Enable for compare intent (highest value) + gather feedback
- **Phase 3 (Week 4):** Expand to setup + overview; measure engagement
- **Phase 4 (Week 5+):** Full rollout or opt-in toggle based on Phase 3 results

### 7. Real-World Impact

Example from `CONSULTING_ANSWER_EXAMPLES.md` (Holiday Channel Strategy):

- **Current answer:** "Choose based on your audience and goals" (vague)
- **Consulting answer:** 4 approaches with $50K-$200K+ budget scenarios, ROI math, cost breakdowns
- **Impact:** Customer can now decide if SMS ($150K for 1M messages = 3% → 30K conversions) vs. RCS ($162K for 1.4M = 10% → 132K conversions) is worth the extra cost

This is the difference between advice and strategy.

---

## File Locations

```
/Users/adwit.sharma/kb_docs/local/reports/
├── CONSULTING_TONE_FRAMEWORK.md           (Strategic, ~8K words)
├── CONSULTING_ANSWER_IMPLEMENTATION.md    (Technical, ~5K words)
├── CONSULTING_ANSWER_EXAMPLES.md          (Practical, ~6K words)
└── CONSULTING_TONE_INDEX.md               (This file)
```

---

## Next Steps by Role

### Product Lead
1. Review Mock Answer 1 and 2 (CONSULTING_ANSWER_EXAMPLES.md)
2. Decide: Launch as experiment (50% of users) or full rollout?
3. Define success metrics (beyond the defaults)
4. Timeline: Plan Phase 1 sprint (2 weeks)

### Design Lead
1. Study Part 4 (Follow-Up Prompts) — how to display questions naturally
2. Design 2-3 layout options for consulting answers
3. Test with users: Does format help or overwhelm?

### Engineering Lead
1. Review CONSULTING_ANSWER_IMPLEMENTATION.md Part 1-4
2. Estimate effort (likely 3-4 weeks of dev + testing)
3. Decide: Build custom or use existing LLM patterns?
4. Plan: Gradual rollout vs. big bang?

### QA / Content
1. Create tone style guide using Tone Markers reference
2. Rewrite 10 current answers in consulting style (practice)
3. Build test cases for confidence levels, branching logic
4. Plan: Accuracy audits post-launch

### Data / Analytics
1. Add Langfuse tracking for new metrics (approaches offered, questions asked, follow-up rate)
2. Build dashboard for consulting vs. solution mode comparison
3. Define guardrails (if consulting answers perform worse, trigger alert)

---

## Common Questions

### Q: Will consulting answers be too long?
**A:** Yes, they're longer. But they're scannable (headers, bullets) and can be summarized. Consider offering both: 1-2 sentence summary + "Want to explore this?" option for full answer.

### Q: What if the customer doesn't have enough context for conditional logic?
**A:** Ask in the Open Questions section. The framework includes "doesn't know" as a valid state—invite exploration rather than forcing a decision.

### Q: How does this affect latency?
**A:** Composition adds ~200-500ms (retrieval + formatting). Total answer time goes from ~2s to ~2.5s. Acceptable for advisory content.

### Q: Should every answer be consulting-tone?
**A:** No. Transactional questions ("What's a Prompt Node?") can be brief. Use consulting-tone for high-value decisions (setup, troubleshooting, compare, overview). Use problem-solution for definitions and simple how-tos.

### Q: What about accuracy risks?
**A:** Lower than you'd think. Confidence tagging + evidence counts + uncertainty admission actually build more trust. Users prefer "I'm 80% confident, test it" over "I don't know."

### Q: How do we train the system to write consulting-tone answers?
**A:** (1) Use the Tone Markers reference as few-shot examples. (2) Fine-tune on consulting-style answers. (3) Or: Use rule-based composition (this framework) instead of LLM generation for safety.

---

## References & Related Work

- Current system: `/Users/adwit.sharma/kb_docs/skill/kb_answer.py` (lines 6482-6700, answer composition)
- Real examples tested: `/Users/adwit.sharma/kb_docs/local/reports/RCS_CONSULTING_QUESTIONS_TEST.md`
- Case studies in KB: holiday marketing, multi-channel strategy, API integration patterns

---

## Version History

| Version | Date | Sections | Status |
|---------|------|----------|--------|
| 1.0 | 2026-08-11 | Framework (Part 1-9) + Implementation (Part 1-7) + Examples (3 queries) + Index | Complete, ready for review |

---

**Questions?** Refer back to the 3 main documents. If something is unclear, check the examples first—they're often more illustrative than the theory.

**Ready to build?** Start with CONSULTING_ANSWER_IMPLEMENTATION.md Part 1 (Architecture). It's a simple modification to kb_answer() that doesn't break existing functionality.

