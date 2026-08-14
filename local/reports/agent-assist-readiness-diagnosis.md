# Agent Assist: Readiness Diagnosis

## Diagnosis

**Should I use an AI agent or stick with rules-based automation?**

This is the foundational decision. Many teams default to AI agents without considering whether their use case actually requires them. The wrong choice leads to either unnecessary complexity (over-engineered rules) or uncontrolled hallucinations (under-engineered agents).

---

## Context

### The Three Deployment Models

**Rules-Based Systems** (Deterministic)
- Decisions follow if/then/else logic
- 100% predictable output
- Suitable for: Routing, validation, simple classification
- Cost: Lowest
- Latency: Fastest
- Accuracy: Depends on rule coverage (0% or 100%)

**AI Agents** (Probabilistic)
- Decisions driven by language models
- Non-deterministic output (can vary per run)
- Suitable for: Open-ended reasoning, nuanced understanding, synthesis
- Cost: Per-token (scales with complexity)
- Latency: Slower (API call required)
- Accuracy: 85–98% depending on prompt design and guardrails

**Hybrid** (Rules + AI Fallback)
- Rules handle high-confidence paths
- AI agent handles edge cases
- Suitable for: Balancing safety and capability
- Cost: Lower than full AI
- Latency: Faster for common cases
- Accuracy: 95%+ (rules + AI double-check)

### Industry-Specific Hallucination Risk

| Industry | Hallucination Risk | Recommended Model | Why |
|----------|-------------------|-------------------|-----|
| **Healthcare** | **CRITICAL** | Hybrid (rules first) | Wrong facts can harm patients |
| **Financial** | **HIGH** | Hybrid or rules only | Compliance, regulatory exposure |
| **Legal** | **HIGH** | Rules first, AI audit | Citation requirements, case law |
| **E-commerce** | **MEDIUM** | Hybrid with guardrails | Wrong product info is recoverable |
| **Customer Support** | **MEDIUM-LOW** | Full AI (with RAG) | Tone & empathy matter more than precision |
| **Internal Tools** | **LOW** | Full AI | Human-in-the-loop available |

---

## Options

### Option 1: Rules-Based (Deterministic)
**Best for:** High-accuracy, low-ambiguity tasks

**Pros:**
- 100% predictable
- Compliant by design
- Fast (no LLM calls)
- Low cost

**Cons:**
- Brittle (breaks on new patterns)
- Difficult to scale (rule explosion)
- No reasoning capability
- Maintenance-heavy

**Example:** "If email ends with @company.com AND request type = 'internal', approve automatically. Else, escalate."

---

### Option 2: Full AI Agent (Probabilistic)
**Best for:** Complex reasoning, open-ended tasks

**Pros:**
- Handles nuance and edge cases
- Scales to new scenarios
- Natural language reasoning
- Powerful and flexible

**Cons:**
- Non-deterministic (can fail unexpectedly)
- Hallucination risk
- Higher cost
- Requires strong guardrails

**Example:** "Analyze this customer complaint and suggest a resolution that balances customer satisfaction with company policy."

---

### Option 3: Hybrid (Rules + AI Fallback)
**Best for:** Balancing safety and capability

**Pros:**
- Rules handle common, high-confidence cases
- AI handles edge cases safely
- Lower cost than full AI
- Faster than full AI (rules bypass LLM)
- Compliant by default (rules first)

**Cons:**
- More complex to implement
- Requires fallback logic
- Testing is more involved

**Example:** "If request is clearly 'bug report' (rules), auto-assign to eng. Else, use AI to classify, then route accordingly."

---

## Recommended Approach

### Start with Hybrid (Rules + AI Fallback)

1. **Identify high-confidence, high-frequency paths** → Cover with rules
   - Example: "Request format is invalid" → Reject immediately
   - Example: "User is not authenticated" → Block immediately

2. **Use AI for low-frequency, complex reasoning paths**
   - Example: "Request is valid but ambiguous" → AI decides intent
   - Example: "User complaint needs resolution strategy" → AI drafts response

3. **Implement confidence thresholds**
   - AI score >= 0.85 → Accept AI decision
   - AI score < 0.65 → Fall back to rules or escalate to human

4. **Monitor and iterate**
   - Track: Rule coverage, AI accuracy, fallback rate
   - Goal: 80%+ covered by rules (safe), <1% escalations

---

## Follow-up Questions

### 1. **What's your accuracy requirement?**
- Must be 99%+ accurate? → Hybrid or rules only
- Can tolerate 95% accuracy? → Full AI is viable
- Accuracy varies by severity? → Hybrid with risk-based routing

### 2. **What happens if you're wrong?**
- Customer is merely inconvenienced? → Full AI is acceptable
- Legal/compliance consequences? → Rules first, AI guardrails only
- Safety impact (healthcare/aviation)? → Rules only, or extremely high guardrails

### 3. **How much variation in inputs?**
- Inputs are highly structured (forms)? → Rules are enough
- Inputs are unstructured (free text)? → AI agent is needed
- Mix of both? → Hybrid is ideal

### 4. **What's your cost/latency tolerance?**
- Must be <100ms? → Rules or lightweight routing AI
- Can tolerate 500ms–1s? → Full AI is fine
- Batch processing (not real-time)? → Cost is less critical

### 5. **Do you have domain experts to review decisions?**
- Yes, humans review everything? → Start with rules, add AI confidently
- No human review? → Need extremely strong guardrails

---

## See Also

- **Agent Assist: Prompt Design** — How to write effective prompts for AI agents
- **Agent Assist: Guardrails Checklist** — Preventing hallucinations and policy violations
- **Agent Assist: Hallucination Mitigation** — RAG and fact-checking strategies
- **Agent Assist: Fallback to Rules** — When to hand off AI to rule-based fallback
