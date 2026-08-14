# Agent Assist: Fallback to Rules

## Diagnosis

**When should an AI agent hand off to rule-based automation—and how do I design a safe fallback strategy?**

Even the best AI agents sometimes fail. Confidence drops, hallucinations slip through, or the request is outside the agent's expertise. A well-designed fallback strategy ensures that when the agent is uncertain, the system gracefully steps down to deterministic rules or escalates to humans—rather than proceeding with low confidence.

---

## Context

### When AI Agents Fail

**Scenario 1: Confidence Crisis**
- Customer asks complex question
- Agent isn't sure of the answer (confidence 0.45)
- Without fallback: Agent guesses → Customer gets wrong info
- With fallback: Escalate to rules or human

**Scenario 2: Out-of-Scope Request**
- Customer asks about topic agent doesn't handle
- Agent tries to answer anyway (hallucination)
- Without fallback: Customer gets made-up info
- With fallback: Politely decline, offer alternatives

**Scenario 3: Policy Violation**
- Agent generates response that violates policy
- Guardrails catch it (good!)
- Without fallback: Error message, no help
- With fallback: Offer safe alternative or escalate

**Scenario 4: Skill-Based Boundary**
- Request needs domain expertise (legal, medical advice)
- Agent is general-purpose, not qualified
- Without fallback: Agent attempts anyway → harm
- With fallback: Decline, escalate to expert

---

### Fallback Options

**Rule-Based Fallback:** If Agent Fails → Apply Rules
- Deterministic, predictable outcome
- Fast (no LLM calls)
- Limited to structured decisions
- Best for: Routing, validation, simple decisions

**Human Escalation:** If Agent Fails → Contact Human
- Highest accuracy
- Most expensive
- Slowest response
- Best for: Complex/sensitive decisions, edge cases

**Cached Response:** If Agent Fails → Return Safe Default
- Instant response
- Covers common cases
- Limited flexibility
- Best for: Known failure modes (e.g., "I don't know, please contact support")

**Graceful Degradation:** If Agent Fails → Offer Limited Help
- Provide partial answer (if low confidence on details only)
- Acknowledge uncertainty ("I'm not 100% sure...")
- Suggest alternatives
- Best for: Balancing helpfulness + safety

---

## Options

### Option 1: No Fallback (Risky)
**Approach:** Agent always responds, even if unsure

**Pros:**
- Always gives an answer
- Fast

**Cons:**
- High hallucination rate (5–10%)
- Policy violations slip through
- Customer gets wrong information
- Compliance risk

**Risk Level:** 🔴 CRITICAL

---

### Option 2: Confidence-Based Fallback
**Approach:** If agent confidence <0.65, escalate to human

**Metrics:**
- Agent confidence ≥ 0.85 → Accept response
- Agent confidence 0.65–0.84 → Flag for review
- Agent confidence <0.65 → Escalate to human

**Pros:**
- Catches most uncertain responses
- Clear decision boundary
- Measurable (track confidence scores)

**Cons:**
- Escalation rate may be high (30–50%)
- Human review is expensive
- Some low-confidence answers are still correct

**Risk Level:** 🟡 MEDIUM

**Escalation Rate:** ~30% (depending on task)

---

### Option 3: Topic-Based Fallback
**Approach:** Certain topics must fall back to rules or humans

**Example Topics:**
- Pricing (too critical; use rules only)
- Medical advice (escalate to doctor)
- Legal advice (escalate to lawyer)
- Refund decisions (use rules for policy-compliant answers)
- Payment processing (use rules/API calls, not agent guessing)

**Pros:**
- Prevents hallucinations on high-risk topics
- Fast for safe topics
- Compliant by design (rules already checked)

**Cons:**
- Requires clear topic boundaries
- Some edge cases may be mislabeled
- Needs frequent updates as topics change

**Risk Level:** 🟢 LOW (for defined topics)

**Escalation Rate:** ~5–10% (only high-risk topics)

---

### Option 4: Hybrid Fallback (Recommended)
**Approach:** Use all three:
1. Confidence threshold (escalate if <0.65)
2. Topic boundaries (high-risk topics use rules)
3. Output validation (catch policy violations)

**Pros:**
- Multiple layers of defense
- Low false-positive rate
- Handles both known and unknown failures
- Compliant + safe

**Cons:**
- More complex to implement
- Requires clear policy definitions
- Escalation rate varies by task

**Risk Level:** 🟢 LOW

**Escalation Rate:** ~10–15%

---

## Recommended Approach

### Recommended: Hybrid Fallback with Confidence Threshold

**Decision Tree:**

```
User Request
    ↓
1. INPUT VALIDATION (Rules)
   ├─ Is user authenticated? NO → Reject (rule)
   ├─ Is request spam/injection? YES → Reject (rule)
   └─ Is user authorized? NO → Reject (rule)
    ↓
2. TOPIC ROUTING (Rules)
   ├─ High-risk topic (pricing, refund)? YES → Use rules only
   ├─ General support topic? → Use AI agent
   └─ Edge case? → Depends on confidence
    ↓
3. AI AGENT (Probabilistic)
   ├─ Generate response
   ├─ Compute confidence
   └─ Output validation
    ↓
4. CONFIDENCE CHECK
   ├─ Confidence ≥ 0.85? → Send to customer ✅
   ├─ Confidence 0.65–0.84? → Flag for human review ⚠️
   └─ Confidence <0.65? → Escalate to human ❌
    ↓
5. FALLBACK ACTIONS
   ├─ Human review: Approve or modify response
   ├─ Escalation: Route to tier-2 support
   └─ Safe default: "I'm not sure; a specialist will help"
```

---

## Implementation Patterns

### Pattern 1: Confidence-Triggered Fallback

```python
# Pseudocode
def handle_request(user_request):
    response, confidence = agent.generate(user_request)
    
    if confidence >= 0.85:
        return response  # Send to customer
    elif confidence >= 0.65:
        return queue_for_human_review(response)  # Flag
    else:
        return fallback_to_human(user_request)  # Escalate
```

**Metrics:**
- Track: % sent directly (high conf)
- Track: % queued for review (medium conf)
- Track: % escalated to human (low conf)
- Goal: 70% direct, 20% review, 10% escalate

---

### Pattern 2: Topic-Based Fallback

```python
# Pseudocode
HIGH_RISK_TOPICS = ["pricing", "refund", "payment", "legal"]

def handle_request(user_request):
    topic = classify_topic(user_request)
    
    if topic in HIGH_RISK_TOPICS:
        return rules_engine.process(user_request)  # Use rules
    else:
        response, confidence = agent.generate(user_request)
        if confidence >= 0.65:
            return response
        else:
            return fallback_to_human(user_request)
```

**Metrics:**
- Track: % routed to rules by topic
- Track: Agent accuracy on non-high-risk topics
- Monitor: Are rules handling high-risk accurately?

---

### Pattern 3: Safe Default Fallback

```python
# Pseudocode
SAFE_DEFAULT = """
I'm not entirely certain about this. A specialist from our team 
will review your request and get back to you within 2 hours. 
In the meantime, here's what I do know: [partial answer if available]
"""

def handle_request(user_request):
    response, confidence = agent.generate(user_request)
    
    if confidence >= 0.70:
        return response  # High confidence
    elif confidence >= 0.50:
        return response + "\n\n[Note: Check with support for exact details]"
    else:
        return SAFE_DEFAULT  # Low confidence → escalate
```

---

## Fallback Decision Matrix

Use this to decide fallback strategy by use case:

| Use Case | Accuracy Requirement | Escalation Tolerance | Recommended Fallback |
|----------|---------------------|---------------------|----------------------|
| **Customer Support** | 90%+ | High | Confidence threshold |
| **Pricing/Billing** | 99%+ | None | Rules only |
| **Product Recommendations** | 85% | Medium | Confidence + topic-based |
| **Healthcare/Medical** | 99.9%+ | None | Human escalation (rules for simple) |
| **Internal FAQ** | 80%+ | Medium-high | Confidence + safe default |
| **Complaint Triage** | 95%+ | Low | Confidence + human review |

---

## Monitoring & Optimization

### Metrics to Track

**1. Escalation Rate by Topic**
```
Pricing questions: 2% escalated
Refund requests: 8% escalated
General support: 15% escalated
Target: <15% overall
```

**2. Accuracy of Escalations**
- Of escalated requests, how many were the right call?
- If 80%+ were correctly escalated → Threshold is good
- If <80% → Threshold is too strict (false positives)

**3. False Negative Rate**
- Of accepted responses, how many contained errors?
- Sample 1% of accepted responses for human review
- Track: % that should have been escalated
- Target: <1% (i.e., <1 in 100 responses should have escalated)

**4. Human Review Backlog**
- How many requests are queued for human review?
- If queue is empty → Threshold may be too strict
- If queue is large → Threshold may be too loose
- Aim for: Review queue completed within 2 hours

### Quarterly Review

- [ ] Plot escalation rate trend (should be stable)
- [ ] Review false positives (were we too cautious?)
- [ ] Review false negatives (did bad responses slip through?)
- [ ] Adjust confidence threshold if needed
- [ ] Update topic-based rules if policies changed

---

## Common Fallback Mistakes

### ❌ Mistake 1: No Fallback at All
**Problem:** Agent always responds, no escalation
**Result:** Hallucinations reach customers
**Fix:** Implement confidence threshold + escalation path

### ❌ Mistake 2: Fallback Is Slower Than Agent
**Problem:** Escalation to human takes 24+ hours
**Result:** Customers prefer agent's wrong answer than waiting for human
**Fix:** Implement SLA for human review (2–4 hours)

### ❌ Mistake 3: Fallback Is Generic
**Problem:** "Please contact support" with no details
**Result:** Customer frustration
**Fix:** Fallback includes what you DO know + escalation path

### ❌ Mistake 4: Rules Engine Has Gaps
**Problem:** High-risk topic escalates to rules, but rules are incomplete
**Result:** Rules engine also fails
**Fix:** Audit rules before relying on them for fallback

### ❌ Mistake 5: No Metrics
**Problem:** You don't know if fallback is working
**Result:** Bad responses slip through undetected
**Fix:** Track escalation rate, false positive rate, false negative rate

---

## Implementation Checklist

### Phase 1: Define Fallback Strategy (Week 1)
- [ ] List high-risk topics (pricing, refund, medical, legal, etc.)
- [ ] Define confidence threshold (default: 0.65)
- [ ] Design fallback messages (safe defaults)
- [ ] Plan escalation path (who gets escalated requests?)

### Phase 2: Implement Confidence Scoring (Week 2)
- [ ] Add confidence score to agent output
- [ ] Implement threshold check
- [ ] Route low-confidence to escalation
- [ ] Log all escalations

### Phase 3: Implement Topic-Based Routing (Week 2–3)
- [ ] Classify requests by topic (rules-based or ML classifier)
- [ ] Route high-risk topics to rules engine
- [ ] Test rules engine accuracy on high-risk topics
- [ ] Audit: Do rules produce correct answers?

### Phase 4: Monitoring & Optimization (Week 4 onwards)
- [ ] Set up dashboards to track escalation rate
- [ ] Weekly review of false positives
- [ ] Monthly review of false negatives
- [ ] Adjust confidence threshold based on data

---

## Follow-up Questions

### 1. **What's your acceptable error rate?**
- Can you tolerate 2% hallucinations? → Confidence threshold 0.70
- Must be <0.5%? → Rules for high-risk, escalate for medium-risk
- Must be <0.1%? → Human review mandatory for all uncertain requests

### 2. **How fast must escalations be resolved?**
- <1 hour? → Dedicate team to escalation queue
- <4 hours? → Batch review (reasonable cost)
- <24 hours? → Not urgent (customer satisfaction may suffer)

### 3. **Do you have a rules engine for high-risk topics?**
- Yes? → Route high-risk to rules (fast fallback)
- No? → Must escalate to humans (slower but safer)

### 4. **How many topics are "high-risk"?**
- 1–2? → Topic-based routing is simple
- 5+? → Might be simpler to use confidence threshold only

---

## See Also

- **Agent Assist: Readiness Diagnosis** — Should you use AI agent?
- **Agent Assist: Guardrails Checklist** — Output validation catches errors
- **Agent Assist: Hallucination Mitigation** — Prevention is better than fallback
- **Agent Assist: Prompt Design** — Better prompts reduce fallback frequency
