# Agent Assist: Guardrails Checklist

## Diagnosis

**How do I prevent bad outputs—hallucinations, policy violations, harmful content—from reaching customers?**

Guardrails are your safety net. A well-designed system has multiple layers: input validation (what comes in), output validation (what goes out), and policy enforcement (what should never be said). Without guardrails, even a good prompt will occasionally produce harmful outputs.

---

## Context

### Three Layers of Defense

**Input Validation** (Prevent bad requests)
- Detect spam, injection attacks, off-topic requests
- Filter before they reach the AI agent
- Block at the protocol level
- Cost: Very low (runs before LLM)

**Output Validation** (Catch bad responses)
- Check agent output against policy
- Flag hallucinations, prohibited topics, unsafe language
- Allow high-confidence outputs, block/escalate low-confidence
- Cost: Varies (can be lightweight heuristics or LLM-based)

**Policy Enforcement** (Business rules)
- Explicit rules that the agent must follow
- Examples: "Never offer >20% discount," "Always cite source," "Refuse requests from unverified users"
- Implemented as constraints in prompt or post-processing rules
- Cost: Medium (requires domain expertise to define)

### Soft vs. Hard Guardrails

**Soft Guardrails** (Warning, advice)
- Agent sees guidance but can override
- Example: "I recommend asking for more details, but you may proceed if confident"
- Use: When false positives are costly (e.g., blocking valid requests)
- Risk: Agent may ignore warnings

**Hard Guardrails** (Blocking, mandatory)
- Agent cannot bypass them
- Example: "Never output PII (name, email, SSN)"
- Use: When false negatives are costly (e.g., compliance risk)
- Risk: May block valid use cases

---

## Options

### Option 1: Minimal Guardrails (Soft Only)
**Approach:** Add guidance to prompt, but rely on model behavior

**Guardrails:**
- Prompt includes: "Try to be accurate and avoid making up facts"
- No explicit output validation
- No hard rules

**Pros:**
- Simple to implement
- Low cost
- Maximum flexibility

**Cons:**
- High hallucination rate (5–10% of outputs)
- No policy enforcement
- Compliance risk
- Customer harm possible

**Risk Level:** 🔴 HIGH

---

### Option 2: Soft Guardrails (Warnings + Escalation)
**Approach:** Validation layer that flags suspicious outputs; human reviews before delivery

**Guardrails:**
- Input validation: Block common attacks/spam
- Output validation: Flag low-confidence answers, off-topic responses
- Confidence threshold: <0.65 confidence → escalate to human
- Policy hints in prompt: "Never offer >20% discount"

**Pros:**
- Catches many hallucinations
- Human-in-the-loop provides final check
- Better than nothing

**Cons:**
- Escalation rate may be high (30–50%)
- Slower response times
- Human review is expensive
- Some bad outputs still slip through

**Risk Level:** 🟡 MEDIUM

---

### Option 3: Hard Guardrails (Blocking + Validation)
**Approach:** Strict output validation; block harmful outputs before delivery

**Guardrails:**
- Input validation: Reject spam, injection attacks, unauthorized users
- Hard constraints in prompt: "You MUST follow these rules: [list]"
- Output validation:
  - Reject responses with PII (name, email, SSN)
  - Reject offers outside policy (discount >20%)
  - Reject if confidence <0.65
  - Reject if hallucination detected (claim not in KB)
- Policy rules: "If user is not verified, never offer refunds"

**Pros:**
- Prevents most bad outputs
- Compliant by design
- Fast (hard rules block before human review)
- Clear audit trail

**Cons:**
- May block valid requests (false positives)
- Requires clear policy definition
- Not suitable for creative/open-ended tasks

**Risk Level:** 🟢 LOW

---

## Recommended Approach

### Recommended: Hard Guardrails + Spot-Check Sampling

**Implementation:**

```
1. INPUT VALIDATION (Block before AI agent)
   ├─ Check user is authenticated
   ├─ Check request is within scope (not spam/injection)
   └─ Check rate limits (no abuse)

2. AI AGENT (With hard constraints in prompt)
   ├─ Prompt includes explicit rules: "Never X, Always Y"
   ├─ System prompt includes policy examples
   └─ Temperature set to 0.5 (deterministic)

3. OUTPUT VALIDATION (Block harmful outputs)
   ├─ Reject if: Hallucination detected (claim not in KB)
   ├─ Reject if: Policy violation (e.g., discount >20%)
   ├─ Reject if: Confidence <0.65
   ├─ Reject if: Contains PII (name, email, SSN)
   ├─ Reject if: Off-topic (not about supported domain)
   └─ Reject if: Unsafe language (slurs, hate speech)

4. AUDIT & MONITORING (Spot-check)
   ├─ Log all rejected outputs (why rejected?)
   ├─ Sample 1% of accepted outputs for human review
   ├─ Track: Rejection rate, false positive rate, escalation rate
   └─ Monthly review of policies (are they working?)

5. ESCALATION PATH (Fallback)
   ├─ If validation fails: Return predefined safe response
   ├─ If confidence <0.65: Offer to escalate to human
   └─ Log for human review + policy refinement
```

---

## Guardrails Checklist

Use this checklist to implement hard guardrails:

### Input Validation
- [ ] **Authentication**: Verify user is logged in and authorized
- [ ] **Authorization**: Check user has permission for this action
- [ ] **Rate Limiting**: Detect and block abuse (>10 requests/min)
- [ ] **Injection Protection**: Sanitize input (no prompt injection attacks)
- [ ] **Format Validation**: Ensure input is valid (not too long, correct schema)
- [ ] **Scope Check**: Request is about supported topic (not random questions)

### Output Validation
- [ ] **Hallucination Detection**: Claim should be verifiable from KB or documented facts
- [ ] **Policy Compliance**: Offer doesn't violate policy (discount <20%, refund <policy window, etc.)
- [ ] **Confidence Threshold**: Reject if model confidence <0.65
- [ ] **PII Screening**: Output contains no names, emails, SSNs, phone numbers
- [ ] **Tone Check**: Output matches expected tone (professional/casual/empathetic)
- [ ] **Citation Check**: Claims reference sources (if required by policy)
- [ ] **Length Check**: Output isn't too long/short (reasonable for task)
- [ ] **Off-Topic Detection**: Response is about supported domain

### Policy Enforcement
- [ ] **Forbidden Topics**: Agent won't discuss X, Y, Z (list specific topics)
- [ ] **Escalation Rules**: When to hand off to human (e.g., "Complex disputes go to tier-2")
- [ ] **Boundary Conditions**: Clear limits on what agent can/can't do (offer discounts, process refunds, etc.)
- [ ] **Exception Handling**: What happens if none of the above catch an issue?

### Monitoring & Improvement
- [ ] **Rejection Logging**: Log all rejected outputs (what was rejected, why?)
- [ ] **Spot-Check Sampling**: 1% of accepted outputs reviewed by human
- [ ] **Escalation Analysis**: Review escalations monthly (are guardrails too strict?)
- [ ] **False Positive Tracking**: Are we blocking too many valid requests?
- [ ] **Hallucination Rate**: Track % of outputs containing hallucinations
- [ ] **Policy Violation Rate**: Track % of outputs violating business policy

---

## Common Guardrail Mistakes

### ❌ Mistake 1: Only Soft Guardrails (No Enforcement)
**Problem:** Prompt says "avoid hallucinations" but doesn't block them
**Consequence:** 5–10% of outputs still contain made-up facts
**Fix:** Add hard output validation (fact-check against KB)

### ❌ Mistake 2: Too Strict (False Positives)
**Problem:** Guardrails block all ambiguous outputs
**Consequence:** Valid requests rejected, customers frustrated
**Fix:** Use confidence threshold (only reject <0.65), not blanket bans

### ❌ Mistake 3: No Monitoring
**Problem:** You don't know if guardrails are working
**Consequence:** Bad outputs reach customers undetected
**Fix:** Log rejections, sample accepted outputs, measure metrics

### ❌ Mistake 4: Guardrails Don't Match Policy
**Problem:** Guardrails enforce old policy, business changed rules
**Consequence:** System rejects valid newer requests
**Fix:** Quarterly policy review + guardrail update

### ❌ Mistake 5: No Escalation Path
**Problem:** Rejected outputs have no safe fallback
**Consequence:** User gets error message with no help
**Fix:** Define escalation: offer human support, suggest alternatives, etc.

---

## Implementation Timeline

### Week 1: Input Validation
- [ ] Add authentication check
- [ ] Add authorization check
- [ ] Add rate limiting
- [ ] Test with 50 requests

### Week 2: Output Validation
- [ ] Add hallucination detection (fact-check against KB)
- [ ] Add policy compliance check
- [ ] Add confidence threshold (reject <0.65)
- [ ] Add PII screening
- [ ] Test with 100 requests

### Week 3: Monitoring
- [ ] Set up rejection logging
- [ ] Start spot-check sampling (1% of outputs)
- [ ] Create dashboard to track metrics
- [ ] Test with 500 requests

### Week 4: Refinement
- [ ] Review false positives (is threshold too strict?)
- [ ] Review false negatives (any bad outputs slipped through?)
- [ ] Adjust policies based on 1 week of data
- [ ] Document guardrails for team

---

## Follow-up Questions

### 1. **What topics are off-limits?**
- List 5 topics the agent should never discuss
- Example: "Never discuss pricing of competitor products"
- Add to guardrails as hard rules

### 2. **What policy violations are most critical?**
- Risk ranking: Legal > Financial > Reputational > Efficiency
- High-risk violations? Use hard guardrails (block immediately)
- Low-risk violations? Use soft guardrails (flag and escalate)

### 3. **How much false positive rate can you tolerate?**
- Can you block 10% of valid requests? → Strict guardrails
- Can you block 1% of valid requests? → Lenient guardrails
- This determines confidence threshold

### 4. **Do you have a KB or source of truth for fact-checking?**
- Yes? → Implement hallucination detection against KB
- No? → Hard to prevent hallucinations; consider RAG setup

---

## See Also

- **Agent Assist: Readiness Diagnosis** — Whether to use AI agent at all
- **Agent Assist: Prompt Design** — Guardrails start in the system prompt
- **Agent Assist: Hallucination Mitigation** — Complementary technique to output validation
- **Agent Assist: Fallback to Rules** — When guardrails catch issues, fallback strategy
