# Choosing When to Build a Bot: Use Case Assessment & Design Patterns

## Diagnosis: What Problem Does Your Bot Solve?

Before investing in bot development, identify your core use case. Are you trying to:

1. **Automate support** (FAQ deflection, ticket routing, common questions)
2. **Qualify leads** (pre-screen prospects, collect requirements, route to sales)
3. **Guide onboarding** (step-by-step setup, product tours, education)
4. **Personalize engagement** (dynamic messaging, offers based on user behavior, loyalty programs)

Each use case has different success metrics:
- **Support bots** are measured by deflection rate (tickets avoided)
- **Lead bots** by qualification accuracy (quality of leads)
- **Onboarding bots** by completion rate (users finishing setup)
- **Engagement bots** by conversion lift (purchase increase)

Choosing the wrong use case leads to wasted effort (bot built but never used, or bot deployed but users prefer human agents).

## Context: When Bots Work vs Don't Work

**When bots work:**
- Structured conversations (clear decision trees, predefined questions)
- High volume (100+ conversations/day justifies automation investment)
- Repetitive questions (same FAQ asked 50+ times/day)
- Clear success metrics (can measure deflection, qualification, completion)

**When bots don't work:**
- Highly variable needs (no two conversations follow the same flow—requires AI)
- Creative problem-solving required (user needs novel advice, not script)
- Complex human judgment (e.g., negotiation, empathy, trust-building)
- Low volume (10-20 conversations/day—not worth the dev time)

**Platform fit:** Bot Studio's Condition Nodes work best for structured, rule-based routing. If your use case requires NLP, entity extraction, or open-ended conversations, you'll need AI nodes (if available) or a handoff to human agents.

**Cost-benefit:** Assume 40-80 hours to build + 5 hours/week to maintain. ROI emerges when:
- (Support bot) deflecting 30+ tickets/week saves $500/month
- (Lead bot) qualifying 10 leads/week increases sales pipeline by 20%
- (Onboarding bot) completing 70% of signups without support reach-out saves 200 hours/month

## Options: Three Bot Design Approaches

### Option 1: Decision Tree Bot (Narrow Scope, High Accuracy)
**How it works:** Solve ONE specific problem (e.g., 'FAQ for billing questions only' or 'Lead qualification for enterprise sales'). Create a Decision Node tree with 3-5 branches, validate with real users, then scale.

- **Pros:** Easy to build (5-10 nodes), easy to maintain, 90%+ accuracy
- **Cons:** Only solves one problem, requires human handoff for out-of-scope questions
- **Best for:** First-time bot builders
- **Example:** Bot that answers 'How do I change my password?' (5 common answers) → escalates if user asks about billing

### Option 2: Handoff Bot (Bot + Human Collaboration)
**How it works:** Bot handles first layer (triage, FAQ, simple questions), then escalates unresolved cases to human.

- **Reduces support load by 40-60%** (bots handle easy cases, humans handle hard ones)
- **Pros:** Solves more problems than decision tree, scales easily
- **Cons:** Requires ticketing/handoff infrastructure, humans must be on standby
- **Best for:** Support teams (avoid 100% bot-only, users want human fallback)
- **Example:** Bot asks 'What's your issue?' → routes to FAQ or escalates to support queue based on issue type

### Option 3: Co-Pilot (Bot + AI Assistance)
**How it works:** Combine Bot Studio's structured nodes with AI capabilities (AI Node for intent detection, API Node for data enrichment, Function Node for custom logic). Handles 70-80% of conversations, escalates edge cases to human.

- **Pros:** Handles variable queries, learns from interactions, higher user satisfaction
- **Cons:** Requires AI/ML expertise, higher maintenance (model retraining), latency (AI calls add 2-5 sec delay)
- **Best for:** High-volume channels (1000+ conversations/day), teams with technical depth
- **Example:** Bot uses AI to detect user intent ('refund', 'track order', 'upgrade') → calls API to fetch order data → provides personalized response

## Recommended Approach

**For your first bot, choose Option 1 (Decision Tree Bot with narrow scope).** Focus on ONE specific problem that:
- (a) Happens 50+ times per week
- (b) Has a clear answer or routing path
- (c) You can test with 20-30 users

Once you validate success (measure deflection rate or qualification accuracy), expand to **Option 2 (add human handoff)** or **Option 3 (add AI if volume grows)**. This incremental approach reduces risk and lets you learn Bot Studio before scaling.

## Follow-Up Questions

Answer these three questions:

1. **What's your specific use case?** (support/lead gen/onboarding/engagement?)
2. **How many similar conversations happen per week?** (volume drives ROI)
3. **Who's your user?** (internal support team, customers, prospects?)

Once you answer, we can recommend the right bot design and estimate timeline.

## See Also

- **About Bot Studio:** Overview of JB V2 vs JB Pro; choose based on complexity (V2 for simple bots, Pro for enterprise workflows)
- **Pattern: Conditional Message Routing:** Examples of decision trees routing users to different paths
- **Pattern: Complex Branching with Variable Context:** Combining user profile + conversation state for personalization
- **Pattern: Fallback Chains:** Gracefully handling out-of-scope questions and escalation flows
- **Bot Studio Analytics:** Track bot performance (deflection rate, user satisfaction, conversation length) to validate ROI
- **Agent Transfer Node:** Handoff from bot to human support (required for Option 2)
- **AI Node (if available):** Intent detection, entity extraction, open-ended responses (enables Option 3)
