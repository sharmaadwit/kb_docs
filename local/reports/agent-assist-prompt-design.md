# Agent Assist: Prompt Design

## Diagnosis

**How do I write effective system prompts that improve agent accuracy?**

A well-designed prompt is the difference between a 65% accurate agent and a 95% accurate one. Yet many teams spend weeks optimizing guardrails while neglecting prompt engineering. Prompt quality directly impacts hallucination risk, tone consistency, and decision accuracy.

---

## Context

### Prompt Engineering Fundamentals

**The System Prompt** is the agent's "job description"
- Defines role and expertise
- Sets tone and style
- Establishes decision criteria
- Influences accuracy by 20–30%

**Few-Shot Examples** (in-context learning)
- Provide 2–5 examples of correct behavior
- Show edge cases and how to handle them
- Influence accuracy by 10–20%
- Most cost-effective accuracy boost

**Constraints and Rules**
- Explicit boundaries (what NOT to do)
- Policy enforcement
- Reduce hallucinations by 5–15%
- Required for compliance-sensitive tasks

**Temperature and Sampling**
- Low temperature (0.3–0.5) → More deterministic, factual
- High temperature (0.8–1.0) → More creative, varied
- For agents: Prefer 0.3–0.7 (balance creativity and consistency)

---

## Options

### Option 1: Generic Prompt
**Prompt:** "You are a helpful assistant. Answer questions accurately."

**Pros:**
- Simple to write
- Works for basic tasks

**Cons:**
- Low accuracy (65–75%)
- High hallucination risk
- No tone consistency
- No constraint enforcement

**Accuracy:** ~70%

---

### Option 2: Role-Based Prompt
**Prompt:** "You are an expert customer support agent for SaaS billing. You specialize in subscription issues and payment disputes. Your tone is empathetic but professional. Always acknowledge customer frustration before explaining policy."

**Pros:**
- Clearer role definition
- Improves tone consistency
- Better accuracy (75–85%)
- Easier to iterate

**Cons:**
- Still needs examples
- Doesn't cover edge cases

**Accuracy:** ~80%

---

### Option 3: Examples-Driven Prompt
**Prompt:** [Role-based prompt] + 3–5 correct/incorrect examples showing:
- How to handle ambiguous requests
- Edge cases (e.g., "What if customer refunded via credit card?")
- Forbidden outputs (e.g., "Never offer discounts beyond 20%")

**Pros:**
- High accuracy (85–95%)
- In-context learning is powerful
- Shows exact decision criteria
- Reduces hallucinations

**Cons:**
- Longer prompt (higher cost)
- Requires curating good examples
- May overfit to examples

**Accuracy:** ~90%

---

### Option 4: Constraint-Heavy Prompt
**Prompt:** [Role + examples] + explicit rules:
```
REQUIRED BEHAVIORS:
1. Always cite the policy you're referencing
2. Never promise refunds; say "I'll escalate to billing"
3. If uncertain, escalate to tier-2 support

FORBIDDEN OUTPUTS:
1. Offering discounts without manager approval
2. Making up refund timelines
3. Accepting payment outside approved systems
```

**Pros:**
- Enforces compliance
- Reduces hallucination (guardrails are explicit)
- Measurable accuracy (can verify against rules)

**Cons:**
- Very long prompts
- Can feel rigid/robotic
- May miss nuanced cases

**Accuracy:** ~92%

---

## Recommended Approach

### Best Practice: Role-Based + Examples + Soft Constraints

**Template:**

```markdown
# System Prompt

## Role & Expertise
You are a [TITLE] with expertise in [DOMAIN].
Your goal is to [PRIMARY OBJECTIVE].
Your tone should be [TONE: professional/empathetic/casual].

## Decision Criteria
When evaluating requests, prioritize:
1. [Priority 1: e.g., "Customer safety"]
2. [Priority 2: e.g., "Company policy compliance"]
3. [Priority 3: e.g., "Efficiency"]

## Examples

### Correct: [Scenario]
**Input:** [Example input]
**Output:** [Example output]
**Why:** [Reasoning]

### Incorrect: [Scenario]
**Input:** [Bad example input]
**Output:** [What NOT to do]
**Why:** [Explain the error]

## Guardrails
- Always [Required behavior 1]
- Never [Forbidden behavior 1]
- If uncertain about [X], escalate to [Y]
```

**Why This Works:**
- Role is clear (80% accuracy baseline)
- Examples show nuance (+10% accuracy)
- Soft constraints guide behavior without being rigid (+2–5%)
- Total: 92–95% accuracy

---

## Implementation Tips

### 1. Start Generic, Then Iterate
**Version 1:** Role + 1 example
**Version 2:** Add 2 more examples (show edge cases)
**Version 3:** Add explicit guardrails

### 2. Use Real Examples from Production
- Pull 5 correct decisions from logs
- Pull 5 incorrect decisions (from fallback/human review)
- Use these as examples in the prompt

### 3. Test Prompt Variations
- Baseline: Generic prompt
- Variant A: Add role-based context
- Variant B: Add examples
- Variant C: Add constraints
- Measure accuracy improvement at each step

### 4. A/B Test on Sample Data
- 50 representative requests
- Run baseline vs. improved prompt
- Track: Accuracy, hallucination rate, tone consistency
- Roll out only if improvement is statistically significant

### 5. Monitor Over Time
- Track: Accuracy by request type, tone consistency, escalation rate
- If accuracy drops, prompt may need refresh
- Re-test with updated examples from recent data

---

## Common Mistakes

### ❌ Mistake 1: Overly Long Prompts
**Bad:** 1000+ words of instruction
**Why:** Token cost increases, model loses focus on key guidance
**Fix:** 300–500 words (role, 3 examples, 5 guardrails)

### ❌ Mistake 2: Vague Role Definition
**Bad:** "You are helpful and accurate"
**Why:** No specificity; model guesses at tone and expertise
**Fix:** "You are a SaaS billing expert who handles refund requests with empathy"

### ❌ Mistake 3: Missing Edge Cases in Examples
**Bad:** Only show "happy path" examples
**Why:** Agent fails when it encounters unusual requests
**Fix:** Include 1 edge case example (e.g., "What if refund window is expired?")

### ❌ Mistake 4: Tone Mismatch
**Bad:** Professional prompt but casual outputs
**Why:** Tone wasn't explicit in the prompt
**Fix:** Add: "Always respond in professional, formal language."

---

## Follow-up Questions

### 1. **What tone should the agent use?**
- Professional/formal? → Use "expert" language in prompt
- Friendly/casual? → Add "conversational, empathetic" guidance
- Varies by scenario? → Add conditional guidance in examples

### 2. **What are your most common edge cases?**
- List top 3 decision points where humans disagree
- Add as explicit examples in the prompt
- This often provides +5–10% accuracy boost

### 3. **Do you have production logs to extract examples from?**
- Yes? → Use real examples (most effective)
- No? → Craft synthetic examples with domain experts

### 4. **How much should the agent explain its reasoning?**
- Brief (1 sentence)? → Add: "Be concise"
- Detailed? → Add: "Explain your decision-making process"
- Policy citations? → Add: "Always reference the relevant policy"

---

## See Also

- **Agent Assist: Readiness Diagnosis** — Should you use AI agent or rules?
- **Agent Assist: Guardrails Checklist** — Hard and soft constraints
- **Agent Assist: Hallucination Mitigation** — RAG and fact-checking with good prompts
- **Agent Assist: Fallback to Rules** — When prompt quality isn't enough
