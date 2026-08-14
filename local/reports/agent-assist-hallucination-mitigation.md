# Agent Assist: Hallucination Mitigation

## Diagnosis

**The agent is making up facts. It confidently cites policies that don't exist, invents product features, and fabricates statistics. What can I do?**

Hallucinations are the #1 risk in deployed AI agents. A model can't distinguish between real information and plausible-sounding made-up facts. The solution isn't better prompts—it's architecture: grounding the agent in reality through retrieval-augmented generation (RAG) and fact-checking.

---

## Context

### Root Causes of Hallucination

**1. Knowledge Cutoff**
- Model was trained on data up to Feb 2025
- Product has changed since training
- Agent confidently gives outdated information
- Example: "Our refund window is 30 days" (but it's now 60)

**2. Model Uncertainty**
- Model doesn't know the answer
- Instead of saying "I don't know," it guesses
- Guess sounds confident because it's trained on plausible language
- Example: "I'm not sure, but I think the API rate limit is..." [makes up number]

**3. Conflicting Information in Training Data**
- Training data had contradictory examples
- Model learns to pick the most "likely" answer
- Likelihood ≠ correctness
- Example: Two versions of policy in training data; model picks one randomly

**4. Domain-Specific Gaps**
- Model is general-purpose, not domain-expert
- Missing context about your business
- Fills gaps with plausible-sounding guesses
- Example: "For your SaaS product, the churn rate is usually 3%" [made up; should consult your data]

---

## Detection Methods

### Method 1: Manual Testing
**Approach:** Ask agent questions you know the answers to

**Test Questions:**
- "What is our refund policy?" (should cite exact policy)
- "What are the API rate limits?" (should cite exact numbers)
- "What features does the Premium tier include?" (should list exact features)

**Scoring:**
- Correct answer + exact source: ✅ No hallucination
- Correct gist but wrong details: ⚠️ Partial hallucination
- Made-up information: ❌ Hallucination

---

### Method 2: Fact-Checking Layer
**Approach:** Automated check that agent claims are verifiable

**Process:**
1. Extract claims from agent output
2. Search KB/documentation for evidence
3. If no evidence found: Flag as potential hallucination
4. Human review of flagged claims

**Tool Example:**
```
Agent output: "Our refund policy allows 60 days for refunds."
Fact-check: Search KB for "refund" + "60 days"
Result: Found in /docs/refund-policy.md → Valid
Output: ✅ Fact-checked
```

---

### Method 3: Confidence Scoring
**Approach:** Measure model confidence; low confidence = hallucination risk

**How it Works:**
- Ask agent: "Rate your confidence in this answer (0-100)"
- Low score (<50%) = likely hallucination or uncertainty
- High score (>80%) = likely accurate (but not guaranteed)

**Example:**
- "What's our API rate limit?" Agent responds with confidence 92% → Likely accurate
- "What's our churn rate?" Agent responds with confidence 45% → Likely hallucination

---

## Mitigation Strategies

### Strategy 1: Retrieval-Augmented Generation (RAG)
**How It Works:**
1. Agent receives user question
2. Search your KB for relevant documents
3. Agent writes response based on retrieved docs only
4. Agent cannot reference facts outside KB

**Pros:**
- Grounds agent in reality
- 90%+ hallucination reduction
- Simple to implement

**Cons:**
- Requires KB setup
- Slower (needs search step)
- Fails if KB is incomplete

**Hallucination Reduction:** 🔴 90%+

**Implementation:** 2 weeks (if KB exists)

**Example:**
```
User: "What's the refund policy?"
System:
  1. Search KB: docs/refund-policy.md retrieved
  2. Agent reads: "Refunds allowed within 60 days..."
  3. Agent responds: "Based on our policy, refunds are allowed within 60 days."
  4. Output includes: [Source: refund-policy.md]
```

---

### Strategy 2: Prompt-Level Constraints
**How It Works:**
- System prompt includes: "Only answer using the provided facts"
- Examples show: "If you don't know, say 'I don't know' rather than guessing"
- Temperature set to 0.3 (low = less creative/more factual)

**Pros:**
- No new infrastructure needed
- Low cost

**Cons:**
- Not fully effective (model still hallucinates 3–5%)
- Requires good prompt engineering
- No enforcement mechanism

**Hallucination Reduction:** 30–50%

**Implementation:** 1 day

---

### Strategy 3: Output Fact-Checking
**How It Works:**
1. Agent generates response
2. Extract all factual claims
3. Search KB for evidence
4. Flag claims without evidence
5. Human reviews flagged claims before sending

**Pros:**
- Catches hallucinations before customer sees them
- Works with any prompt/setup
- Confidence scoring tells you risk level

**Cons:**
- Adds latency (fact-check step)
- Requires human review time
- False positives (valid claims marked as dubious)

**Hallucination Reduction:** 80–95%

**Implementation:** 2 weeks

---

### Strategy 4: Low-Temperature Sampling
**How It Works:**
- Set model temperature to 0.3 (vs. default 0.7)
- Low temperature = deterministic, factual responses
- High temperature = creative, varied responses

**Pros:**
- Simple one-line change
- Immediate effect

**Cons:**
- May reduce response quality for creative tasks
- Moderate hallucination reduction only
- Not suitable for empathetic/tonal tasks

**Hallucination Reduction:** 20–40%

**Implementation:** 1 minute

---

### Strategy 5: Hybrid (RAG + Fact-Check + Low Temp)
**How It Works:**
1. Set temperature to 0.3 (deterministic)
2. Use RAG (ground in KB)
3. Add fact-checking layer (catch edge cases)
4. Prompt includes: "Only use provided facts"

**Pros:**
- Multiple layers of defense
- 95%+ hallucination prevention
- Highest accuracy

**Cons:**
- More complex to implement
- Higher latency
- Requires KB investment

**Hallucination Reduction:** 🟢 95%+

**Implementation:** 4 weeks

---

## Recommended Approach

### Start with RAG + Low Temperature + Prompt Constraints

**Week 1–2: Setup RAG**
- Inventory your KB (docs, policies, product info)
- Set up vector search (Pinecone, Weaviate, or built-in)
- Implement retrieval step in agent pipeline

**Week 3: Low Temperature + Prompt Constraints**
- Set temperature to 0.3
- Update system prompt: "Only answer using retrieved documents"
- Add examples: "If you don't know → say 'I don't know'"

**Week 4: Fact-Checking Layer**
- Extract claims from responses
- Search KB for evidence
- Flag unverified claims (human review)

**Measure:**
- Baseline: 5–8% hallucination rate
- After Week 2: 2–3% (RAG helps)
- After Week 3: 1–2% (temperature + prompt)
- After Week 4: <0.5% (fact-checking catches rest)

---

## Hallucination Detection Checklist

Use this checklist to verify your mitigation is working:

### Pre-Deployment Testing
- [ ] Test 20 questions you know the answers to
- [ ] Score: % of answers with correct facts
- [ ] Goal: >95% of facts correct
- [ ] Document any hallucinations

### Post-Deployment Monitoring
- [ ] Log all agent responses
- [ ] Weekly sample: Review 20 random responses
- [ ] Track: % containing hallucinations
- [ ] Goal: <1% hallucination rate
- [ ] Alert if rate exceeds threshold (e.g., >2%)

### Fact-Checking Automation
- [ ] Extract claims from responses
- [ ] Check against KB (automated)
- [ ] Flag unverified claims
- [ ] Track: % of claims verified, % flagged

### Customer Feedback
- [ ] Monitor customer complaints: "That's not right"
- [ ] Analyze: Which topics have highest hallucination rate?
- [ ] Update KB to cover gaps
- [ ] Re-test agent on those topics

---

## Common Hallucination Patterns

### Pattern 1: Made-Up Statistics
**Example:** "Most customers report 40% productivity improvement with our tool"
**Root Cause:** Training data had many marketing claims
**Fix:** Add to prompt: "Never cite statistics without a source" + RAG retrieval

### Pattern 2: Outdated Information
**Example:** "Our pricing is $29/month" (but it's now $39)
**Root Cause:** Training data includes old pricing, not updated docs
**Fix:** RAG retrieval ensures agent uses current docs

### Pattern 3: Product Features That Don't Exist
**Example:** "You can integrate with Salesforce" (feature doesn't exist)
**Root Cause:** Similar products have this feature; model assumes yours does
**Fix:** KB entry: "Supported integrations: [list only real ones]"

### Pattern 4: Confident Wrong Answers
**Example:** "Our API response time is <100ms guaranteed" (actually SLA is <500ms)
**Root Cause:** Model saw "response time" + "100" in training; combined them
**Fix:** Add to prompt + RAG: Exact SLA numbers only from docs

---

## Implementation by Use Case

### Customer Support Agent
- **Highest Risk:** Outdated policy information
- **Recommended:** RAG (KB of policies) + Prompt constraints
- **Timeline:** 2 weeks
- **Hallucination Target:** <0.5%

### Product Recommendation Agent
- **Highest Risk:** Inventing features, wrong pricing
- **Recommended:** RAG (product KB) + Fact-checking layer
- **Timeline:** 3 weeks
- **Hallucination Target:** <1%

### Internal Knowledge Bot
- **Highest Risk:** Confidently wrong answers
- **Recommended:** RAG (internal docs) + Low temperature
- **Timeline:** 2 weeks
- **Hallucination Target:** <2%

### Healthcare/Compliance Agent
- **Highest Risk:** Medical/legal misinformation (high stakes)
- **Recommended:** RAG + Fact-check + Human review (mandatory)
- **Timeline:** 6 weeks
- **Hallucination Target:** <0.1%

---

## Follow-up Questions

### 1. **Do you have a fact source (KB, API, database)?**
- Yes? → Implement RAG (2 weeks, huge impact)
- No? → You can't prevent hallucinations effectively; build KB first
- Partial? → RAG + prompt constraints for gaps

### 2. **How bad would a hallucination be for you?**
- Customer inconvenience (support agent wrong)? → 1–2% acceptable
- Financial impact (wrong pricing)? → <0.5% required
- Legal/safety impact (medical/legal advice)? → <0.1% required, human review mandatory

### 3. **What topics hallucinate most?**
- Pricing? → Add exact pricing table to KB
- Product features? → Add feature matrix to KB
- Policies? → Add policy doc to KB
- Fix: Update KB, then test agent again

### 4. **How much latency can you tolerate?**
- <100ms? → Low-temp + prompt only (no RAG)
- <500ms? → RAG + fact-check (realistic)
- No limit? → Full hybrid (RAG + fact-check + human review)

---

## See Also

- **Agent Assist: Readiness Diagnosis** — Whether AI agent is right for you
- **Agent Assist: Prompt Design** — Constraints that reduce hallucinations
- **Agent Assist: Guardrails Checklist** — Output validation catches hallucinations
- **Agent Assist: Fallback to Rules** — When RAG/fact-check fails, fallback to rules
