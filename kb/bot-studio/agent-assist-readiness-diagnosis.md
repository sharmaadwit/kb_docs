# Agent Assist: Readiness Diagnosis

## Diagnosis
**Should I use an AI agent or stick with rules-based automation?**

This is the foundational question before implementing any AI-powered agent. The answer depends on your accuracy requirements, latency constraints, cost tolerance, and hallucination risk profile. Choosing the wrong architecture leads to either excessive rule maintenance (rules-only) or unacceptable error rates (pure AI).

---

## Context: Architecture Options by Use Case

### Rule-Based Systems
**Strengths**: Predictable, zero hallucination, fast, explainable, audit-friendly
**Weaknesses**: High maintenance cost, brittle at scale, requires manual edge cases
**Best for**: High-stakes decisions, strict accuracy (>99%), regulatory compliance

**Industry profiles**:
- **Finance/Payments**: Rules mandatory (regulatory requirement)
- **Healthcare**: Rules recommended (liability, FDA oversight)
- **Legal**: Rules preferred (discovery, precedent-based)

### Pure AI Agents
**Strengths**: Flexible, learns nuance, handles variations, lower maintenance
**Weaknesses**: Hallucinations, variable latency, cost per query, hard to debug
**Best for**: Customer service, content, low-stakes exploration

**Industry profiles**:
- **E-commerce**: AI acceptable (returns, recommendations)
- **SaaS support**: AI promising (FAQ routing, ticket classification)
- **Content**: AI strong (summarization, drafting)

### Hybrid (Rules + AI Fallback)
**Strengths**: Best accuracy, controlled cost, clear escalation paths
**Weaknesses**: Implementation complexity, requires fallback design
**Best for**: Mixed-risk workflows (high-value rules, AI for long tail)

---

## Options & Trade-Offs

### Option 1: Rules-Only
```
Accuracy:     ★★★★★ (99%+)
Latency:      ★★★★★ (<100ms)
Cost:         ★★☆☆☆ (maintenance heavy)
Scalability:  ★★☆☆☆ (new rules per variant)
Hallucination: ★★★★★ (zero)
```
**When to choose**: Regulated industries, payment processing, identity verification

### Option 2: Pure AI Agent
```
Accuracy:     ★★★☆☆ (85-92%)
Latency:      ★★★☆☆ (500ms-2s)
Cost:         ★★★☆☆ (per-query pricing)
Scalability:  ★★★★★ (flexible)
Hallucination: ★★☆☆☆ (3-8% rate)
```
**When to choose**: Customer support, content generation, exploration use cases

### Option 3: Hybrid (Recommended)
```
Accuracy:     ★★★★★ (95%+)
Latency:      ★★★★☆ (200-500ms)
Cost:         ★★★☆☆ (balanced)
Scalability:  ★★★★☆ (rules + AI)
Hallucination: ★★★★☆ (rules block edge cases)
```
**When to choose**: Most production systems (start here)

---

## Recommended Approach: Hybrid (Rules → AI → Fallback)

### Implementation Pattern
1. **Tier 1 (Rules)**: High-confidence patterns (70-80% of traffic)
   - Confidence: >0.95
   - Latency: <100ms
   - Cost: <$0.001/query
   - Example: "Return policy → check item condition" → deterministic rules

2. **Tier 2 (AI Agent)**: Complex judgment calls (15-25% of traffic)
   - Confidence: 0.70-0.95
   - Latency: 500ms-2s
   - Cost: $0.001-0.01/query
   - Example: "Assess customer sentiment → recommend retention offer"

3. **Tier 3 (Human Review)**: Low confidence (<0.70)
   - Confidence: <0.70
   - Latency: Async (human-in-loop)
   - Cost: $5-50/query (human time)
   - Example: "Complex dispute → escalate to specialist"

### Hybrid Benefits
- **Accuracy**: Rules eliminate easy mistakes; AI handles nuance
- **Cost**: Rules for high-volume, AI for exceptions
- **Trust**: Rules provide audit trail; AI adds judgment
- **Safety**: Confidence thresholds prevent bad outputs

### Example: Customer Refund Request
```
IF item_value < $50 AND days_since_purchase < 14 THEN
  → AUTO APPROVE (Rule)
ELSE IF item_category in [Electronics, Furniture] THEN
  → ASK AI AGENT (Sentiment, return reason, customer history)
ELSE
  → ESCALATE TO HUMAN (Edge case)
```

---

## Accuracy Requirements by Industry

### High-Accuracy Threshold (>98%)
- **Finance/Banking**: AI not recommended; hybrid with rules-first
- **Healthcare**: AI assistance only; human verification required
- **Legal/Contracts**: Rules recommended; AI for research only

### Medium-Accuracy Threshold (93-98%)
- **E-commerce**: Hybrid acceptable (returns, refunds)
- **SaaS/B2B**: Hybrid recommended (ticket routing, onboarding)
- **Insurance**: Hybrid acceptable (claims triage)

### Lower-Accuracy Threshold (85-93%)
- **Customer Support**: Pure AI acceptable (FAQs, initial response)
- **Content**: Pure AI acceptable (summaries, drafts)
- **Recommendations**: Pure AI acceptable (suggestions require confirmation)

---

## Hallucination Risk by Use Case

### High Risk (AI Needs Guardrails)
- **Factual claims**: "Your policy covers X" → requires KB validation
- **Personal recommendations**: "Based on your history..." → verify data sources
- **Compliance statements**: "Under GDPR..." → fact-check against legal docs

### Medium Risk (AI Acceptable with Confidence Thresholds)
- **Tone/sentiment assessment**: "Customer is frustrated" → OK, human can override
- **Categorization**: "This is a billing issue" → OK, can be corrected
- **Explanation**: "Because your subscription ended" → OK, user can dispute

### Low Risk (AI Can Operate Freely)
- **Brainstorming**: "Suggest 5 email subject lines"
- **Summarization**: "Condense feedback into 2 sentences"
- **Formatting**: "Convert this to JSON"

---

## Decision Tree

```
START: Should I use an AI agent?

1. Are accuracy requirements > 98%?
   YES → Use Rules-Only (add AI for research only)
   NO → Continue

2. Is this a regulated industry (finance, healthcare, legal)?
   YES → Use Hybrid (rules-first, AI for research)
   NO → Continue

3. Is hallucination cost acceptable (<2% error)?
   YES → Can use Pure AI (with confidence thresholds)
   NO → Use Hybrid (rules for high-stakes, AI for rest)

4. Is this high-volume traffic (>1000 queries/day)?
   YES → Recommend Hybrid (rules for 80%, AI for long tail)
   NO → Can use Pure AI (cost per query acceptable)

OUTPUT:
- Pure AI: Customer support, content, chat
- Hybrid: E-commerce, SaaS, marketing, recommendations
- Rules: Finance, healthcare, legal, compliance
```

---

## Follow-Up Questions

### Required to Proceed
1. **Accuracy requirement**: What's your acceptable error rate? (e.g., 95%, 99%)
2. **Industry**: Are you in a regulated sector (finance, healthcare, legal)?
3. **Hallucination tolerance**: Is factual accuracy critical or can AI "close enough"?
4. **Volume**: How many requests per day? (affects cost trade-offs)
5. **Latency**: Do you need <100ms response, or is 2-5s acceptable?

### Secondary Clarifications
- Do you have a fact source (KB, API, database)?
- What topics are absolutely off-limits (compliance violations)?
- Do you have confidence scoring infrastructure?
- Is human review available for escalations?

---

## See Also
- [Agent Assist: Prompt Design](agent-assist-prompt-design.md) — Writing effective system prompts
- [Agent Assist: Guardrails Checklist](agent-assist-guardrails-checklist.md) — Preventing hallucinations
- [Agent Assist: Hallucination Mitigation](agent-assist-hallucination-mitigation.md) — RAG + fact-checking
- [Agent Assist: Fallback to Rules](agent-assist-fallback-to-rules.md) — Confidence-based escalation
