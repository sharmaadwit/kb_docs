# Agent Assist: Prompt Design

## Diagnosis
**How do I write effective system prompts for AI agents?**

The quality of your agent's output depends 80% on prompt design and 20% on model choice. A poorly written prompt leads to off-topic responses, inconsistent tone, policy violations, and hallucinations. This guide covers prompt engineering techniques that maximize accuracy and consistency.

---

## Context: Prompt Engineering Fundamentals

### What Prompts Control
1. **Accuracy**: "You are a support agent" vs. "You are a support specialist trained in refund policies"
2. **Tone**: Professional vs. casual vs. empathetic
3. **Scope**: What topics are in-bounds vs. out-of-bounds
4. **Format**: How responses should be structured
5. **Guardrails**: What the agent should never do

### Why Prompts Matter
- Model behavior varies 30-50% based on prompt framing
- Generic prompts (e.g., "Answer this") underperform by 20-40%
- Role-based prompts outperform generic by 2-3x accuracy
- Examples in prompts improve accuracy by 15-25%

### Prompt Layers
```
System Prompt (Foundation)
  ↓
Role Definition (Context)
  ↓
Instructions (Behavior)
  ↓
Examples (In-Context Learning)
  ↓
Constraints (Guardrails)
```

---

## Options & Prompt Styles

### Option 1: Generic Prompt
```
Prompt: "Answer the user's question."

Result:
- Accuracy: 65-75%
- Tone: Variable, inconsistent
- Cost: $0.01 per query
- Use case: Brainstorming, exploration
```

**Weaknesses**:
- No context on domain expertise
- Model guesses at appropriate tone
- May violate implicit policies
- Not reproducible (different results each time)

**When to use**: Brainstorming, research, first drafts

---

### Option 2: Role-Based Prompt
```
Prompt: "You are a customer support specialist at Acme Corp. 
Your role is to help customers with returns and refunds.
You have access to return policies and customer history.
Be empathetic but professional."

Result:
- Accuracy: 80-85%
- Tone: Consistent, professional
- Cost: $0.01 per query
- Use case: Support, customer service
```

**Strengths**:
- Clear expertise context
- Consistent tone and behavior
- Reduces policy violations
- Reproducible responses

**When to use**: Customer support, sales, onboarding

---

### Option 3: Examples-Driven Prompt
```
Prompt: "You are a support specialist. Answer questions about returns.

GOOD RESPONSE EXAMPLE:
Q: Can I return this item?
A: I'd be happy to help! We accept returns within 30 days 
of purchase in original condition. When did you buy it?

BAD RESPONSE EXAMPLE:
Q: Can I return this item?
A: Maybe. It depends. Call back later.

Now answer this question..."

Result:
- Accuracy: 85-90%
- Tone: Consistent, professional
- Cost: $0.01 per query (longer prompt)
- Use case: Complex judgment, consistency
```

**Strengths**:
- Shows what good looks like
- Reduces hallucinations by 20-30%
- Improves consistency
- Model learns from examples

**When to use**: High-stakes responses, complex scenarios

---

### Option 4: Constraint-Heavy Prompt (Maximum Safety)
```
Prompt: "You are a support specialist. RULES:
1. Only discuss returns/refunds (not shipping, pricing)
2. Always provide specific timeframes (e.g., '30 days')
3. NEVER promise refunds without checking status
4. If unsure, say 'I'll escalate to a specialist'
5. Do not discuss competitor products
6. Keep responses under 150 words

Now answer..."

Result:
- Accuracy: 90-95%
- Tone: Professional, cautious
- Cost: $0.01 per query
- Use case: Regulated, high-risk domains
```

**Strengths**:
- Prevents policy violations
- Reduces hallucinations (hard boundaries)
- Clear escalation paths
- Auditable decisions

**When to use**: Finance, healthcare, legal, compliance

---

## Recommended Approach: Role-Based + Examples (Tier 1)

### Structure
```
SYSTEM PROMPT TEMPLATE:

[Role]
You are a {ROLE} at {COMPANY}.
Your expertise: {DOMAIN}
Your goals: {OBJECTIVES}

[Scope]
You can discuss: {IN_SCOPE_TOPICS}
You cannot discuss: {OUT_OF_SCOPE_TOPICS}

[Tone]
- Professional but {TONE_DESCRIPTOR}
- Be {EMPATHY_LEVEL} to customer concerns
- Keep responses concise (under {WORD_LIMIT} words)

[Critical Rules]
1. {RULE_1}
2. {RULE_2}
3. {ESCALATION_RULE}

[Examples]
GOOD:
Q: {EXAMPLE_Q1}
A: {EXAMPLE_A1}

BAD:
Q: {EXAMPLE_Q2}
A: {EXAMPLE_A2}
```

### Real Example: Refund Support Agent
```
SYSTEM PROMPT:

You are a customer support specialist at Acme Corp.
Your expertise: Returns, refunds, and exchanges.
Your goal: Resolve customer issues quickly and empathetically.

SCOPE:
Can discuss: Return eligibility, refund status, exchange options
Cannot discuss: Shipping costs, product recommendations, pricing

TONE:
- Professional and empathetic
- Acknowledge customer frustration
- Provide specific timelines
- Keep responses under 100 words

CRITICAL RULES:
1. Always check return window (30 days from purchase)
2. Never promise a refund without verifying order status
3. If unsure, say: "I'll escalate to a specialist within 24 hours"
4. Never discuss other company policies

EXAMPLES:
GOOD:
Q: "Can I return this sweater?"
A: "I'd be happy to help! We accept returns within 30 days 
in original condition. When did you purchase it?"

BAD:
Q: "Can I return this sweater?"
A: "Probably. Maybe check our website."
```

---

## Prompt Engineering Techniques

### 1. Role Definition
**Impact**: +10-20% accuracy improvement

```
WEAK: "Answer this question"
STRONG: "You are a {ROLE} with {EXPERTISE}. 
Your responsibility is {OBJECTIVE}."
```

### 2. In-Context Examples
**Impact**: +15-25% accuracy, -30% hallucinations

Include 2-4 examples of:
- **Good responses** (what you want)
- **Bad responses** (what to avoid)
- **Edge cases** (tricky scenarios)

### 3. Explicit Constraints
**Impact**: +5-10% safety, eliminates policy violations

```
NEVER:
- Discuss competitor products
- Promise outcomes without verification
- Provide financial/legal advice
- Share confidential information
```

### 4. Output Format Specification
**Impact**: +20% consistency (structured outputs)

```
Format your response as:
1. Direct answer (1 sentence)
2. Explanation (2-3 sentences)
3. Next steps (if applicable)
```

### 5. Tone & Personality
**Impact**: +5-15% user satisfaction

```
Tone: Professional but warm
- Use "I understand" instead of "OK"
- Acknowledge feelings: "That's frustrating"
- Use second person: "Your issue is important"
```

---

## Common Mistakes & Fixes

### Mistake 1: Vague Role Definition
```
❌ WRONG: "You are helpful"
✅ RIGHT: "You are a support specialist with 5+ years 
           resolving billing issues. You're empathetic 
           but professional."
```

### Mistake 2: Missing Examples
```
❌ WRONG: "Be professional in tone"
✅ RIGHT: "Here's what professional looks like:
           'I understand your concern. Let me look into that.'"
```

### Mistake 3: Conflicting Constraints
```
❌ WRONG: "Be helpful" + "Never discuss refunds"
          (conflicting if refund is the help needed)

✅ RIGHT: "Be helpful with returns/refunds/exchanges.
          For pricing questions, say: 'That's handled by sales.'"
```

### Mistake 4: Overly Long Prompts
```
❌ WRONG: 2000+ words (model gets lost)
✅ RIGHT: 300-500 words (clear, focused, actionable)
```

### Mistake 5: No Escalation Path
```
❌ WRONG: "Always resolve the issue"
          (sets agent up to hallucinate)

✅ RIGHT: "If unsure, say: 'I'll escalate to a specialist.'"
```

---

## Testing Your Prompt

### Quality Checklist
- [ ] Role is clear (job title, expertise)
- [ ] Scope is explicit (in-scope vs. out-of-scope topics)
- [ ] Tone example provided (show, don't tell)
- [ ] At least 2 good + 2 bad examples included
- [ ] Critical rules listed (never, always, when unsure)
- [ ] Escalation path defined (how to handle edge cases)
- [ ] Output format specified (structure, word limit)
- [ ] Tested on 10+ real scenarios (accuracy >85%)

### Test Scenarios
1. **Happy path**: "Can I return this?"
2. **Edge case**: "I lost the receipt"
3. **Out-of-scope**: "Why is your shipping so expensive?"
4. **Sensitive**: "You guys have terrible customer service!"
5. **Ambiguous**: "I want to exchange, but also get a refund"

---

## Follow-Up Questions

### Required to Refine Prompt
1. **What tone should the agent use?** (professional, casual, empathetic, formal)
2. **What topics are completely off-limits?** (list them)
3. **How should the agent handle uncertainty?** (escalate, ask for info, admit limitations)
4. **What's the primary goal?** (resolve quickly, maximize satisfaction, minimize cost)
5. **Are there specific compliance rules?** (tone, disclosures, disclaimers)

### Secondary Clarifications
- Should responses be structured (bullets, steps) or conversational?
- What's the acceptable word limit per response?
- Do you have example conversations to use as training data?
- Should the agent apologize for delays/errors?

---

## See Also
- [Agent Assist: Readiness Diagnosis](agent-assist-readiness-diagnosis.md) — Should you use AI agents?
- [Agent Assist: Guardrails Checklist](agent-assist-guardrails-checklist.md) — Preventing bad outputs
- [Agent Assist: Hallucination Mitigation](agent-assist-hallucination-mitigation.md) — Using RAG + fact-checking
- [Agent Assist: Fallback to Rules](agent-assist-fallback-to-rules.md) — Escalation patterns
