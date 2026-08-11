# Consulting-Tone Answer Generation Framework

**Date:** 2026-08-11  
**Purpose:** Design system for transforming problem-solution answers into strategic consulting guidance  
**Status:** Framework specification with 3 mock implementations

---

## Executive Summary

This document outlines how to shift from **"Here's the solution"** to **"Here's what I see, why it matters, and how you might approach it"** — the hallmark of consulting-grade advisory. The framework provides architectural patterns, conditional logic gates, and three increasingly sophisticated answer templates suitable for adoption.

---

## Part 1: Core Differences — Problem-Solution vs. Consulting Tone

### Current System (Problem-Solution)
| Dimension | Current Pattern |
|-----------|-----------------|
| **Answer structure** | Problem → Single authoritative solution → Close |
| **Tone** | Definitive, prescriptive ("Use X because…") |
| **Phrasing** | Imperative commands ("Add a prompt node", "Configure X") |
| **Context** | Feature-focused; assumes technical capability |
| **Accuracy** | High confidence assertions; "I don't know" if uncertain |
| **Follow-up** | FAQ button; user must click to get variants |
| **Audience assumption** | Homogeneous (all users have same constraints) |
| **Branching** | Path A or Path B determined by intent classification |
| **Closure** | Answer ends; follow-up requires new query |
| **Risk acknowledgment** | Minimal; focuses on happy path |

### Consulting-Tone System (This Framework)
| Dimension | Consulting Pattern |
|-----------|-------------------|
| **Answer structure** | Diagnosis → Strategic context → Multiple paths (with trade-offs) → Recommended path (not prescriptive) → Open questions |
| **Tone** | Exploratory, advisory ("Based on what I'm seeing, here's how successful teams…") |
| **Phrasing** | Conditional language ("If you're X, then A; if you're Y, then B"; "One approach is…") |
| **Context** | Customer-situation focused; builds context before jumping to solution |
| **Accuracy** | Confidence levels explicit ("High confidence on X, less certain on Y") |
| **Follow-up** | Woven into narrative as natural next steps ("We should explore whether…") |
| **Audience assumption** | Heterogeneous; builds personas into the answer |
| **Branching** | Conditional logic based on customer profile, constraints, and goals |
| **Closure** | Answer ends with open questions that invite dialogue |
| **Risk acknowledgment** | Explicit trade-offs and edge cases for each path |

### Key Tonal Shifts

**Old (Definitive):**
> "Add a Prompt Node for Age with numeric validation. Use Free Text Node for Gender. Configure validation rules for each prompt. Save and deploy."

**New (Consulting):**
> "For demographic capture, I typically see two approaches: (1) **Native journey inputs**—use Prompt and Number Nodes with validation, which gives you tight control and offline capability. The trade-off: users see separate inputs rather than a cohesive form. (2) **WhatsApp Flow forms**—single interactive form in WhatsApp, seamless UX, but requires Meta approval and adds latency. Which direction fits your user experience priority? Also, are you exporting these demographics to a CRM, or using them in-journey? That changes whether we validate here or downstream."

---

## Part 2: Answer Anatomy — Core Sections

### Section 1: Diagnosis (What I See)
**Purpose:** Establish credibility by showing you understand the customer's implied situation  
**Length:** 1-3 sentences  
**Pattern:**
```
"Based on your question about [topic], I'm seeing a few common scenarios:
- If you're [situation A], then [implication A]
- If you're [situation B], then [implication B]
- If this is for [context C], then [context implication]"
```

**Example:**
```
"Holiday campaign RCS questions usually come from two places: either you're 
planning audience segmentation and messaging strategy (budget/content phase), 
or you're troubleshooting delivery and performance at scale (live campaign). 
Which stage are you in?"
```

**Tone markers:** "I'm seeing", "Common patterns", "Usually", "It depends on", "First signal"

---

### Section 2: Strategic Context (Why It Matters)
**Purpose:** Explain why the answer matters to their business, not just technical implementation  
**Length:** 2-4 sentences  
**Pattern:**
```
"Why this matters:
- For [goal A], the constraint is [X], which affects [outcome A]
- For [goal B], the critical metric is [Y], which determines [outcome B]
- Timing/dependencies: [relevant context]"
```

**Example:**
```
"Why this matters: Holiday peak is when message load spikes 5-10x, so delivery reliability 
becomes your bottleneck. Performance targets shift from 'nice to have' to 'business critical'
—a 2% delivery failure during Black Friday could mean 10K lost conversions. Channel choice 
isn't about features, it's about reliability and audience reach during the peak."
```

**Tone markers:** "Why this matters", "Business impact", "Critical constraint", "The risk is", "This becomes important when"

---

### Section 3: Multiple Approaches (Trade-Offs)
**Purpose:** Surface 2-3 realistic paths, each with explicit trade-offs  
**Length:** 3-8 bullet points per path  
**Structure per path:**
```
**Approach [N]: [Name]**
- What it is: [1-2 sentence description]
- When it works best: [customer profile or scenario]
- Strengths: [2-3 benefits specific to this path]
- Trade-offs: [2-3 explicit costs or constraints]
- Implementation complexity: [Low/Medium/High]
- Example: [Real scenario or use case]
```

**Example:**
```
**Approach 1: RCS-First + SMS Safety Net**
- What it is: Primary messaging on RCS (92% open rate), fallback to SMS for non-RCS devices
- When it works best: High-value campaigns (conversions > alerts); audiences with 60%+ RCS reach
- Strengths: 
  * Maximizes conversion lift (3.2x vs SMS)
  * Rich media (buttons, carousels) drive engagement
  * Verified branding builds trust at scale
- Trade-offs:
  * SMS fallback adds cost per message
  * Split analytics (need to track both channels)
  * Requires dual message templates
- Implementation complexity: Medium
- Example: Fashion retailer, 45% revenue lift using countdown + carousels for holiday flash sales

**Approach 2: Multi-Channel Wave (RCS → SMS → WhatsApp)**
- What it is: Sequence messaging: high-intent → SMS transactional → WhatsApp support
- When it works best: Customer lifecycle (acquisition → conversion → retention)
- Strengths:
  * Each channel optimized for its job (RCS captures intent, SMS confirms, WhatsApp retains)
  * Audience segmentation is clear (reach each user once per stage)
  * Better ROI per message (no wasted impressions)
- Trade-offs:
  * Complex orchestration (need message sequencing logic)
  * Longer campaign lifecycle (not good for 24-hour flash sales)
  * Requires rich customer data (know where each user is in journey)
- Implementation complexity: High
- Example: E-commerce platform, 50% sales lift + 30% retention improvement across channels

**Approach 3: SMS-Dominant (RCS as Upside)**
- What it is: SMS as primary channel; RCS replaces SMS only for accounts with proven RCS capability
- When it works best: Budget-constrained, transactional-heavy, or low-engagement audiences
- Strengths:
  * Lower cost per message
  * Simple (one template, one channel logic)
  * Reliable (SMS has 99%+ delivery)
- Trade-offs:
  * 45% open rate (vs 92% RCS)
  * No rich media (text limits engagement)
  * Harder to stand out during holiday peak
- Implementation complexity: Low
- Example: SaaS alerts, telco usage notifications (not revenue-driving)
```

---

### Section 4: Recommended Path (Not Prescriptive)
**Purpose:** Suggest a starting point based on pattern matching, but leave room for customer judgment  
**Length:** 2-4 sentences  
**Pattern:**
```
"I'd typically recommend [Path X] first, because [reason 1] and [reason 2]. 
You can evolve from there if [condition A] or [condition B] happens."
```

**Example:**
```
"I'd typically start with **RCS-First + SMS Safety Net** for holidays, especially if your 
audience is 60%+ smartphone users in developed markets. It maximizes conversion lift without 
overcomplicating orchestration. Once you see RCS performance, you can layer in WhatsApp for 
post-purchase support. The main risk: if your RCS reach is below 40%, SMS-Dominant might be 
smarter to start."
```

**Tone markers:** "I'd typically", "A common starting point", "Usually works well", "Starting here lets you", "Plan to iterate"

---

### Section 5: Open Questions (For Next Turn)
**Purpose:** Invite dialogue by highlighting unknowns that should shape the recommendation  
**Length:** 3-5 questions, grouped by category  
**Structure:**
```
**To refine this recommendation, it helps to know:**

1. **Audience & Scale**
   - What's your current RCS reach? (% of audience with RCS-capable devices)
   - How many messages during peak day? (helps determine delivery risk)

2. **Business Priority**
   - Is this campaign about conversion (revenue focus) or retention (loyalty focus)?
   - What's the acceptable cost per message? (constrains multi-channel strategy)

3. **Ops & Integration**
   - Do you have journey orchestration set up? (Multi-channel requires scheduling logic)
   - Is customer segmentation data available? (Needed for audience-specific paths)

4. **Risks You Haven't Mentioned**
   - Regulatory: Are there SMS/RCS restrictions in your regions? (GDPR, TCPA)
   - Technical: Do you have APIs ready? (Multi-channel needs real-time sync)
```

**Tone markers:** "To refine this", "Would help to know", "One thing I'd explore", "Key unknowns", "Before committing"

---

## Part 3: Conditional Logic — When to Branch

### Decision Tree: When to Use Conditional Answers

```
START: User asks [question]
  ↓
1. DETECT SCENARIO TYPE (Diagnosis)
   - Can I infer customer situation from query language?
     YES → Extract signals (scale, urgency, industry, goal)
     NO → Ask in Section 5 open questions
   ↓
2. MATCH TO ARCHETYPE (Strategic Context)
   - Is this [high-value/time-sensitive/ops-heavy/uncertain]?
   - Map to business outcome (revenue/retention/cost/risk)
   ↓
3. GENERATE PATHS (Multiple Approaches)
   - For each viable path:
     a) Define preconditions (who should use this)
     b) Identify 3-4 trade-offs
     c) Rate implementation complexity
   ↓
4. RECOMMEND STARTING POINT (Recommended Path)
   - Which path aligns with [detected scenario + business outcome]?
   - What's the lowest-risk entry point?
   ↓
5. SURFACE UNKNOWNS (Open Questions)
   - What assumptions did I make?
   - What data would change the recommendation?
   ↓
END: User reads answer + chooses next step or asks clarifying question
```

### When to Use "If You Are X → Path A; If You Are Y → Path B"

**Use this conditional logic when:**
1. ✅ Customer situation materially changes the recommendation (not just preference)
2. ✅ Each path has explicit preconditions (audience size, budget, tech maturity)
3. ✅ Trade-offs are real and quantifiable (cost, complexity, risk)
4. ✅ You have enough signal to detect which condition applies

**Don't use if:**
- ❌ All paths are equally valid (just list all with equal weight)
- ❌ Preconditions are too vague ("if you care about quality" — subjective)
- ❌ You're guessing the customer's situation (ask instead, in Section 5)

### Pattern: Confidence Levels

**Attach explicit confidence markers:**

```
HIGH CONFIDENCE: "Based on the KB, RCS reaches 92% open rates (documented across 10+ case studies)."
MEDIUM CONFIDENCE: "For audience segmentation, successful teams typically use 3-5 segments (seen in 6 cases, but not exhaustively tested)."
LOW CONFIDENCE: "Regulatory timelines vary by country—I'd check your specific region."
```

---

## Part 4: Injecting Follow-Up Prompts Naturally

### Anti-Pattern: Buttons (❌ What NOT to do)
```
Answer text...

[MORE DETAIL]  [TRY PATH 1]  [TRY PATH 2]
```
**Why it fails:** Breaks conversational flow; feels like a menu, not advisory.

### Pattern: Narrative Threads (✅ What TO do)

**Option 1: Open Question Phrasing**
```
"…the main risk: if your RCS reach is below 40%, SMS-Dominant might be smarter to start.
**That's worth exploring—what does your reach look like right now?**"
```

**Option 2: Conditional Suggestion**
```
"Once you see RCS performance, you can layer in WhatsApp for post-purchase support. 
**If engagement rates drop after 24 hours, post-purchase support becomes critical—we should talk about that flow next.**"
```

**Option 3: Practical Next Step**
```
"To refine this recommendation, it helps to know your current RCS reach…
**A quick way to check: pull your last 7 days of RCS delivery data and note what % of messages landed on RCS vs SMS fallback. That single metric will tell us which path to prioritize.**"
```

**Option 4: Risk Signal**
```
"The main edge case: if you're launching in Vietnam, Thailand, or Mexico, check RCS availability first—it's spotty there. 
**Does your holiday campaign target regions with known RCS gaps?**"
```

**Option 5: Stakeholder Alignment**
```
"Approach 1 works great for conversion focus, but Approach 2 requires your ops team to set up message sequencing.
**Is your team built for orchestration, or do you need something simpler this year?**"
```

### Mechanics: Where to Place Follow-Ups

| Section | Prompt Type | Example |
|---------|------------|---------|
| **Diagnosis** | Clarifying | "Which stage are you in?" |
| **Strategic Context** | Risk-flag | "Does your situation include [edge case]?" |
| **Paths** | Option-focused | "Which priority resonates more—conversion or retention?" |
| **Recommended Path** | Reality-check | "Does this match your team's current capability?" |
| **Open Questions** | Exploratory | "Before committing, would help to know…" |

---

## Part 5: Maintaining Accuracy While Being Less Definitive

### Accuracy Levers

| Lever | Implementation |
|-------|-----------------|
| **Confidence tagging** | Mark each claim as HIGH/MEDIUM/LOW based on KB evidence count |
| **Source transparency** | "This is documented in 10+ case studies" vs. "One customer reported" |
| **Preconditions** | "This works best for [specific profile]" vs. universal claim |
| **Uncertainty admission** | "This varies by region—I'm less certain here" (builds trust) |
| **Conditional language** | "One approach is…" / "Many teams…" vs. "You must…" |
| **Data anchoring** | Cite specific metrics from KB ("92% open rates" not "high open rates") |
| **Timeframe context** | "As of 2026" / "In high-volume campaigns" / "During holiday peaks" |
| **Scope qualification** | "For WhatsApp, this applies to Business Accounts" not all WhatsApp |

### Examples: Phrasing Accuracy as Nuance

**Low Confidence:**
```
"I'm not certain from the docs, but one approach teams try is..."
"This isn't fully documented, so I'd recommend testing first..."
"In limited cases, teams have seen... but this isn't a reliable pattern yet."
```

**Medium Confidence + Conditions:**
```
"For most high-volume campaigns, X works well. The exception: if Y or Z applies, consider A instead."
"Typically, [metric]. In outlier cases (bottom 10%), [different metric]."
"Works reliably for [profile], less predictable for [profile], untested for [profile]."
```

**High Confidence:**
```
"This is well-documented across [N] case studies: RCS achieves 92% open rates."
"Consistently, top-performing teams implement [X] first, because [reason from KB]."
```

---

## Part 6: Mock Answer Structures

---

## MOCK 1: Current System (Problem-Solution)

**Query:** "How should we set up demographic capture in our WhatsApp bot?"

**Current Answer:**

```
Recommended step-by-step setup (documented pattern)

1. In Journey Builder, add prompt-based input nodes for each field you need.
2. Use a Number Node for Age so numeric validation is applied.
3. Use Prompt Node / Free Text Node for Gender and Current City.
4. Configure validation rules and fallback behavior for each prompt.
5. Define variables via Manage Variables and map each captured response to a variable.
6. If you need to transform/update values later, use Modify Variable Node.
7. Save and run the journey in Test your Bot; use Save & Deploy for live traffic.

What I could not verify from the current docs
- An explicit CTX profile-attribute mapping screen/flow for these exact fields is not clearly specified on the retrieved pages.
```

**Characteristics:**
- ✅ Clear, step-by-step
- ✅ Specific node names (actionable)
- ✅ Honest about uncertainty
- ❌ Assumes one right way
- ❌ No context about why this approach
- ❌ No mention of alternatives
- ❌ No follow-up signals
- ❌ Doesn't explore customer's actual goal

---

## MOCK 2: Minimal Change (Structured, But Still Consulting)

**Query:** "How should we set up demographic capture in our WhatsApp bot?"

**Minimal-Change Answer:**

```
For demographic capture, let me first understand your setup goal—are you collecting data 
for immediate bot logic (e.g., branching messages by age), or exporting to a CRM later?

**If it's for in-journey logic**, here's the documented pattern:

1. In Journey Builder, add prompt-based input nodes for each field.
2. Use Number Node for Age (numeric validation), Prompt/Free Text for Gender & City.
3. Configure validation rules and fallback for each prompt.
4. Map responses to variables via Manage Variables.
5. Use Modify Variable Node if you need transformations later.
6. Test in Test your Bot, then Save & Deploy.

This approach gives you tight control and works offline. Trade-off: Users see separate 
inputs, not a cohesive form—that's OK for most flows but feels clunky on mobile.

**If it's for CRM export**, you might want to:
- Capture minimally in-journey (just the fields you'll act on)
- Export to CRM after, letting CRM handle extended profiling
- This avoids friction and keeps the bot flow fast

Key unknown: What's your target profile—are these new users (less patient for multi-step 
inputs) or returning customers (comfortable with the journey)? Also, which fields actually 
affect your journey logic—that determines how many capture steps feel reasonable.
```

**Characteristics:**
- ✅ Starts with diagnosis ("Let me first understand")
- ✅ Surfaces 2 approaches (in-journey vs CRM export)
- ✅ Mentions trade-offs (separate inputs vs cohesive form)
- ✅ Asks open question at end (profile, fields)
- ✅ Explains why each path matters (bot logic vs export)
- ❌ Still fairly prescriptive (gives one "documented" path)
- ❌ Doesn't mention risk or edge cases deeply
- ❌ Doesn't quantify confidence levels

---

## MOCK 3: Radical Redesign (Full Consulting Framework)

**Query:** "How should we set up demographic capture in our WhatsApp bot?"

**Radical-Redesign Answer:**

```
Demographic Capture Strategy — Your Goals Matter Here

**What I'm sensing:** Demographic capture questions usually come from two places:
1. **Bot logic focus** — You need to branch conversations (age determines product recs, city determines shipping)
2. **Audience intelligence focus** — You're building a customer profile for CRM/analytics, separate from bot flow

These are actually different problems with different solutions. Let me walk through both.

---

**THE CORE CONSTRAINT:** WhatsApp is mobile-first, with low patience for multi-step forms. 
Every input field you add increases dropout risk. So the question isn't "capture everything," 
it's "capture only what actually changes the conversation or requires immediate action."

---

**APPROACH 1: Minimal In-Journey Capture (Bot Logic Only)**

What it is: Ask only the questions that branch your bot logic; export extended profile to CRM.

When it works best:
- You have clear bot branches (age-based product recs, city-based shipping, etc.)
- Your CRM can be the "source of truth" for extended profiling
- Audience is mobile-first; friction matters

How to implement:
1. In Journey Builder, add Number Node for Age (numeric validation) → maps to variable
2. Add Prompt/Free Text Node for City (validation: length/format) → maps to variable
3. Skip Gender if you don't branch on it (most bots don't)
4. Use Modify Variable Node downstream if you need transformations (e.g., "age_group = 25-35")
5. Optional: After capturing, immediately route to SMS or CRM sync to export the profile
6. Test in Test your Bot, deploy via Save & Deploy

Strengths:
- Fast (3-4 inputs, 30-45 seconds)
- Clear intent (bot logic drives the ask)
- Mobile-friendly (fewer steps = lower dropout)

Trade-offs:
- Users see separate sequential inputs, not a form (feels less native)
- If you ask for 5+ fields, dropout jumps 25-40% (documented pattern)
- You lose interactivity (buttons/carousels can't capture; text inputs only)

Risk: If fields don't actually affect bot logic, users resent the friction—verify first.

Complexity: Low (existing Journey Builder patterns; simple flows)

Example: E-commerce bot—captures age (age-gated products) + city (shipping cost calc), 
then routes to product carousel. Results: 65% completion rate, fast flows.

---

**APPROACH 2: WhatsApp Flow (Native Form, Better UX)**

What it is: Use WhatsApp's Flows feature (Meta's native form builder) instead of Journey Builder prompts.
Forms appear as native, single-screen interactions rather than sequential bot inputs.

When it works best:
- You need 4-6 demographic fields at once
- User experience (form-like interface) is a priority over speed
- Your audience expects mobile app–quality forms
- You can handle Meta approval timelines (5-10 days for Flow submission)

How to implement:
1. Design Flow in WhatsApp Business Manager (not Journey Builder)—native form builder
2. Configure fields (Age, Gender, City as single form)
3. Submit for Meta approval (new Flows undergo review; can take 5-10 days)
4. Once approved, embed Flow into your journey via Flow Node
5. Map Flow output variables to Journey variables
6. Test in Test your Bot, deploy

Strengths:
- Single native form (feels like a real app, not bot inputs)
- Higher completion rate (50-75% vs 40-55% for sequential inputs)
- Mobile-optimized UX
- Users see all fields at once (lower cognitive load)

Trade-offs:
- Meta approval required (not immediate; 5-10 day delay)
- Flow creation is new skill for your team (different from Journey Builder)
- Slightly more latency (Flow Form rendering)
- Once deployed, updates also need re-approval

Risk: If you frequently update demographics, approval delays become painful—plan in advance.

Complexity: Medium (new tool, approval dependency)

Example: Banking bot—captures KYC fields via Flow (name, age, address, PAN). Results: 
72% completion rate, smoother UX, but 8-day approval delay on first launch.

---

**APPROACH 3: Phased Capture (Progressive Profiling)**

What it is: Capture 1-2 demographic fields now, add more fields later in the conversation 
or on repeat interactions.

When it works best:
- First-time users (low patience; capture minimal)
- Repeat engagement (you can ask more questions over time)
- Long customer lifetime (CRM will fill in gaps over multiple interactions)
- High volume (30K+ users; need predictable flows with low dropout)

How to implement:
1. Launch with just Age (binary branch: adult/minor products)
2. Store in variable; don't ask more on first interaction
3. On repeat chats (2nd-3rd message), add City (for future order targeting)
4. Let CRM/tags build the rest over time (email, purchase history, etc.)
5. Use analytics to find the inflection point: "When do users expect to share more data?"

Strengths:
- Lowest friction on first touch (1 input = 90%+ completion)
- Progressive relationship building (trust grows over time)
- Reduces "why are you asking?" drop-off
- Works great for high-volume campaigns

Trade-offs:
- Longer time to complete profile (might be 5+ interactions)
- Requires tracking conversation count/sequence
- More complex flow (conditional branching based on "is this repeat user?")
- Lower data completeness on day 1 (OK if CRM fills gaps)

Risk: If you later realize you need fields you skipped, you have to re-ask—rebuilding trust costs.

Complexity: High (requires conversation-state tracking, conditional logic)

Example: E-commerce—first message captures Age (product recommendations), third message 
captures City (shipping). Profile completes over 3-4 interactions. Results: 92% first-message 
completion, 75% three-message completion, high retention due to low friction.

---

**RECOMMENDED STARTING POINT:**

I'd recommend **Approach 1 (Minimal In-Journey Capture)** for your first implementation, because:
1. You get results immediately (no Meta approval wait)
2. Fits existing Journey Builder workflows
3. Lowest risk (test with real users fast)

Once you're live and see dropout rates, you can evolve:
- If completion is 60%+, you're fine; might try Flow later for nicer UX
- If completion drops below 40%, Approach 3 (phased capture) likely works better
- If you're building a fintech/banking app, Flow is worth the approval wait

---

**TO REFINE THIS RECOMMENDATION, HELPS TO KNOW:**

1. **Bot Logic**: Which demographic fields actually branch your conversation?
   - "We branch on age (18+), but not gender or city" → Approach 1 is cleanest
   - "We need age, gender, city, income, interests" → Approach 2 or 3 is necessary

2. **Scale & Volume**: How many users are you capturing daily?
   - "500-1000/day" → Approach 1 is fine (any approach works)
   - "10K+/day" → Approach 3 (phased) reduces server load and bot state complexity

3. **First-Time vs. Repeat**: Is most traffic first-time or returning users?
   - "Mostly first-time" → Approach 1 (minimal capture) to reduce friction
   - "Mostly repeat" → Approach 2 (Flow) or Approach 3 (phased) OK; users expect more engagement

4. **Timeline**: When do you need this live?
   - "This week" → Approach 1 only (Flow approval takes 5-10 days)
   - "Next month" → Can invest in Approach 2 (Flow)

5. **Data Destination**: Where does this demographic data go next?
   - "Stays in bot (branches logic)" → Approach 1 sufficient
   - "Exports to CRM/CDP" → Approach 2 or 3 (you can be more aggressive capturing)
   - "Used for analytics/lookalike audiences" → Approach 3 (phased) builds trust gradually

---

**WHAT I CAN'T VERIFY FROM THE KB (Your Unknowns):**

- Exact dropout curves by input count (the KB says "friction increases" but doesn't quantify)
- WhatsApp Flow approval times (dependent on Meta review bandwidth)
- Whether your specific demographic fields are "branching-worthy" (only you know your logic)

I'd recommend A/B testing Approach 1 first (low risk, immediate), then upgrading if needed.

---

**NEXT STEPS:**

1. Identify your core branching logic (age? city? income?)—those are your must-ask fields
2. Implement Approach 1 with those fields only
3. Monitor: Completion rate, dropout rate by field, time-to-complete
4. If completion <50%, try Approach 3 (phased capture) on your next cohort
5. If UX feedback is negative, plan Approach 2 (Flow) for a future release

Does this help clarify? Which approach resonates most with your setup?
```

**Characteristics:**
- ✅ Opens with diagnosis (what this question typically means)
- ✅ Explains core constraint first (mobile friction)
- ✅ 3 full paths with preconditions, strengths, trade-offs, complexity, examples
- ✅ Recommended starting point (with evolution path)
- ✅ 5 open questions with categories
- ✅ Acknowledges unknowns (dropout curves, approval times)
- ✅ Explicit next steps (not just "ask me later")
- ✅ Tone is advisory, not prescriptive
- ✅ Confidence levels woven throughout
- ✅ Ends with dialogue invite ("Does this help clarify? Which resonates?")
- ❌ Much longer (tradeoff for depth; could be summarized for quick consumers)

---

## Part 7: Implementation Roadmap

### Phase 1: Framework Adoption (Weeks 1-2)
- [ ] Update `kb_answer.py` → Add `_compose_consulting_answer()` function
- [ ] Create consulting templates in `templates/` folder
- [ ] Add `answer_mode` parameter to `kb_answer()` → "solution" (current) vs "consulting" (new)
- [ ] Test on 5 representative queries
- [ ] Metrics: Track clicks, follow-up engagement, user satisfaction vs. baseline

### Phase 2: Conditional Logic (Weeks 3-4)
- [ ] Implement decision tree (Scenario Type → Archetype → Paths → Recommendation)
- [ ] Add confidence tagging to KB evidence retrieval
- [ ] Create persona detection from query language ("we're a startup" → small team, budget-constrained)
- [ ] Test on compare, setup, troubleshooting intents first (highest complexity)

### Phase 3: Refinement (Weeks 5-6)
- [ ] Collect user feedback (which paths are chosen most?)
- [ ] Iterate on open questions (are they actually useful?)
- [ ] Add follow-up prompts to top 20 queries
- [ ] Measure: Do users ask follow-ups, or do they implement immediately?

### Phase 4: Scale (Week 7+)
- [ ] Roll out to 100% of queries (if Phase 1-3 show engagement lift)
- [ ] Or: Keep "solution" mode as default, offer "consulting" mode as opt-in
- [ ] Monitor for accuracy (are recommendations still correct as KB evolves?)

---

## Part 8: Success Metrics

| Metric | Baseline | Target | Notes |
|--------|----------|--------|-------|
| **Answer comprehension** | FAQ clicks (20-30%) | User asks follow-up naturally (40-50%) | Higher is better; shows they're engaged |
| **Implementation time** | Direct-to-action (80%) | Deliberation + questions (60% explore first) | OK if more deliberation = better decisions |
| **User satisfaction** | "Helpful" (70%) | "Trusted advisor" (80%+) | Measured via survey or NPS |
| **Accuracy complaints** | 5-10 per month | <5 per month | Consulting tone can reduce edge-case surprise |
| **Retry rate** | Users asking 3+ variants (30%) | Users asking 1 clarifying follow-up (20%) | Fewer retries = better answer first time |
| **Adoption** | N/A | 50%+ of queries opt-in to consulting mode | If voluntary feature |

---

## Part 9: Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Answers become too long** | High | Users overwhelmed; skip to action | Offer summary + depth (1-2 sentences vs. full) |
| **Open questions feel preachy** | Medium | Users ignore and implement wrong path | A/B test question phrasing; keep to 3-5 only |
| **Confidence tagging is wrong** | Medium | User trusts LOW-confidence path; fails | Cite KB evidence counts; update as KB grows |
| **Consulting answers don't match KB** | Low | Accuracy drops | Add verification step before deployment |
| **Hidden edge cases emerge** | Low | Recommended path fails for 5% of users | Include risk signals ("Exception: if X happens") |

---

## Appendix: Quick Reference — Tone Shift Checklist

When writing a consulting-tone answer, use this checklist:

```
[ ] DIAGNOSIS: Start with "I'm sensing…" or "This usually comes from…"
[ ] STRATEGIC CONTEXT: Explain "Why it matters" tied to business outcome
[ ] PATHS: At least 2 approaches; each with preconditions + trade-offs
[ ] COMPLEXITY: Rate Low/Medium/High; cite tech maturity needed
[ ] CONFIDENCE: Mark HIGH/MEDIUM/LOW based on KB evidence
[ ] RECOMMENDED: "I'd typically start with…" not "You must…"
[ ] OPEN QUESTIONS: Ask 3-5 grouped by category (audience, goals, ops, risks)
[ ] FOLLOW-UP: End with dialogue invite ("Does this help? What's your priority?")
[ ] TONE: Conditional language ("If you're X…", "One approach is…") throughout
[ ] EXAMPLES: 1-2 real scenarios; cite results when possible
```

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-08-11 | Initial framework with 3 mock answer structures |

---

**End of Framework Document**

**For questions or implementation details, refer to:**
- `kb_answer.py` → `_compose_consulting_answer()` (to be built)
- `local/reports/RCS_CONSULTING_QUESTIONS_TEST.md` → Real examples of consulting-tone answers
- `skill/consulting_templates.py` (to be created) → Reusable answer blocks

