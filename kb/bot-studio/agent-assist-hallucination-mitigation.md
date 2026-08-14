# Agent Assist: Hallucination Mitigation

## Diagnosis
**The agent is making up facts. What can I do?**

Hallucinations (factually incorrect statements presented with confidence) are the #1 safety risk in AI agents. A confident but wrong answer is more dangerous than an uncertain response. This guide covers root causes, detection methods, and prevention strategies.

---

## Context: Why Hallucinations Happen

### Root Cause 1: No Access to Facts
The model generates plausible-sounding text without checking against real data.

```
Q: "What's your refund policy?"
Agent thinks: "Most companies offer 30-day refunds, 
              so I'll say that" (without checking your KB)
A: "30 days" ← Might be wrong (yours is 14 days)
```

### Root Cause 2: Training Data Mismatch
The model learned general patterns but your specifics are different.

```
Q: "Do you ship to Canada?"
Model trained on: "Most e-commerce sites ship to Canada"
A: "Yes!" ← But you don't (only US)
```

### Root Cause 3: Confidence Without Verification
The model high-confidence answers it hasn't checked.

```
Q: "Is item XYZ in stock?"
A: "Yes, we have 5 in stock" (without querying inventory)
Confidence: 0.95 ← High, but no fact-check
```

### Root Cause 4: Complex Reasoning Chains
Each step in reasoning adds error probability.

```
Step 1: "This item qualifies for returns" (might be wrong)
Step 2: "Return window is 30 days" (might be wrong)
Step 3: "So you qualify for a refund" (wrong conclusion)
Risk: 3 steps × 5% error each = ~14% compound error
```

---

## Detection Methods

### Detection 1: Confidence Scoring
```
Model outputs confidence 0.0-1.0 on each response
Low confidence → Likely hallucination
High confidence → Might still be hallucination (dangerous!)

Example:
Q: "Do you offer returns?"
A: "Yes, 30-day policy"
Confidence: 0.92 ← High, BUT NEEDS FACT-CHECK

Don't rely on confidence alone!
```

### Detection 2: Fact-Checking Against KB
```
Extract factual claims from response:
1. "30-day return policy" → Check KB
2. "Free returns" → Check KB
3. "All items eligible" → Check KB

If KB says:
- "30-day policy: ✓ Correct"
- "Return shipping: Customer pays (not free)"
- "Electronics: 14-day, not eligible for full return"

Verdict: HALLUCINATION DETECTED (2 out of 3 claims wrong)
```

### Detection 3: Cross-Reference Multiple Sources
```
Q: "What's the current exchange rate USD/EUR?"
Source 1 (API): 1 USD = 0.92 EUR ✓
Response claims: 1 USD = 0.95 EUR ✗
Source 2 (API): 1 USD = 0.92 EUR ✓

Verdict: HALLUCINATION (different from real-time data)
```

### Detection 4: User Feedback
```
User reports: "You told me returns are free, but I was charged"
→ Hallucination confirmed
→ Update fact-check KB
→ Audit past 7 days for similar hallucinations
→ Send corrections to affected users
```

---

## Options & Prevention Strategies

### Option 1: Low Temperature (Minimal)
```
Strategy: Lower model creativity (temperature 0.1-0.3)
Effect: More "safe" generic responses
Accuracy: 85-88%
Cost: Same ($0.01/query)

Strengths:
- Reduces hallucinations by ~10%
- Faster inference

Weaknesses:
- Responses become repetitive
- Still hallucinate on factual questions
- Not sufficient alone
```

**When: Not recommended as sole strategy**

---

### Option 2: Confidence Thresholds (Better)
```
Strategy: Only use responses with high confidence
If confidence < 0.80 → Escalate to human
Effect: Blocks uncertain hallucinations
Accuracy: 90-92%
Cost: Same ($0.01/query) + escalation cost

Strengths:
- Catches most uncertain responses
- Reduces hallucinations reaching users

Weaknesses:
- Doesn't catch high-confidence hallucinations (dangerous!)
- High escalation rate (10-30% of traffic)
```

**When: Baseline guardrail, but insufficient**

---

### Option 3: Retrieval-Augmented Generation (RAG) [Recommended]
```
Strategy: Agent only answers from KB documents
Process:
1. User asks question
2. Search KB for relevant documents
3. Agent reads documents
4. Agent generates response from documents
5. No generation without source material

Effect: Dramatically reduces hallucinations
Accuracy: 94-97%
Cost: $0.01-0.02/query (search overhead)

Strengths:
- Eliminates "making up facts" (no sources = escalate)
- Sources traceable (audit trail)
- Most effective single technique

Weaknesses:
- Requires good KB (incomplete KB → missing answers)
- Latency increase (search adds 200-500ms)
```

**Recommended for factual questions**

---

### Option 4: Fact-Checking Backend (Recommended)
```
Strategy: All factual claims checked before sending
Process:
1. Agent generates response
2. Extract factual claims (regex + NLP)
3. Look up each claim in API/DB
4. Compare response vs. real data
5. Block/flag mismatches

Effect: Catches hallucinations post-generation
Accuracy: 97-99%
Cost: $0.01-0.03/query (lookup overhead)

Strengths:
- Catches high-confidence hallucinations
- Works with any model
- Can be tightened over time

Weaknesses:
- Requires live data sources (APIs, databases)
- Latency increase (lookups add 200-1000ms)
- False positives (agent correct, system wrong)
```

**Recommended for dynamic data (inventory, rates, pricing)**

---

## Recommended Approach: RAG + Fact-Checking (Tier 1)

### Implementation Pattern
```
USER QUESTION
    ↓
[1] SEARCH KB for relevant documents
    ↓ (Found docs?)
    YES → [2] AGENT reads docs + generates response
        ↓
        [3] EXTRACT factual claims
        ↓
        [4] FACT-CHECK each claim against API/DB
        ↓ (All correct?)
        YES → SEND to user ✓
        NO → ESCALATE to human (hallucination detected)
    
    NO → [Escalate] No relevant docs found
        (Ask human or refine question)
```

### Example: Product Return Question

#### WITHOUT RAG (Hallucination Risk)
```
Q: "Can I return this electronics item?"
Agent thinks: "Most electronics have 30-day returns"
A: "Yes, we have a 30-day return window"
Response sent to user ✓

Reality: Your policy = "Electronics: 14-day, inspection required"
User receives WRONG information ✗
```

#### WITH RAG + FACT-CHECKING (Safe)
```
Q: "Can I return this electronics item?"

Step 1: Search KB for "return policy + electronics"
Result: "Electronics Return Policy: 14-day from purchase, 
         item must be unopened, no physical damage"

Step 2: Agent reads KB document
A: "Electronics can be returned within 14 days if unopened 
   and in original condition."

Step 3: Fact-check
Claim 1: "14-day return window" → KB match ✓
Claim 2: "Must be unopened" → KB match ✓
Claim 3: "Original condition" → KB match ✓

Step 4: All facts verified
Response sent to user ✓
```

---

## RAG Implementation Checklist

### Step 1: Build Knowledge Base
```
□ Collect all factual content:
  - Product specifications
  - Return/refund policies
  - Shipping information
  - Warranty terms
  - Eligibility rules
  - Pricing (if shareable)

□ Structure as documents:
  - One policy per document (not mega-docs)
  - Clear titles ("Electronics Return Policy", not "Returns")
  - Explicit rules ("14 days", not "typically short period")
  - Version dates ("Updated Jan 2024")

□ Example document:
  Title: "Electronics Return Policy"
  Content: "Customers may return unopened electronics within 
           14 days of purchase for a full refund. Opened or 
           damaged items cannot be returned. Expedited shipping 
           (2-day) is not available on returns."
```

### Step 2: Set Up Document Search
```
□ Choose embedding model:
  - OpenAI Embeddings (recommended)
  - Open-source: all-MiniLM-L6-v2 (smaller, faster)
  
□ Index KB documents:
  - Embed each document
  - Store in vector database (Pinecone, Milvus, etc.)
  - Set up semantic search

□ Configure search:
  - Return top-3 most relevant documents
  - Relevance threshold: 0.75+ (0.0-1.0 scale)
  - Default: If no docs match, escalate
```

### Step 3: Provide Context to Agent
```
System Prompt Update:

You are a support agent. Answer questions ONLY based on 
the provided knowledge base documents.

CRITICAL: If the knowledge base does not mention something, 
you MUST NOT guess. Instead, say:
"I don't have information about that. Let me escalate 
to a specialist."

Here are the relevant policies:
[Document 1 inserted here]
[Document 2 inserted here]
[Document 3 inserted here]

Now answer the customer's question based only on these 
documents.
```

### Step 4: Extract & Fact-Check Claims
```
Python pseudocode:

response = agent_generate(kb_docs, question)
claims = extract_claims(response)
  # Returns: ["14-day return", "unopened only", "full refund"]

for claim in claims:
  kb_match = search_kb(claim)
  if not kb_match:
    # Hallucination detected
    escalate_to_human(response, claim)
    break
  else:
    log(f"Verified: {claim}")

if all_verified:
  send_to_user(response)
```

---

## Fact-Checking API Example

### Dynamic Data (Inventory, Pricing, Rates)
```
Response: "This item is in stock and costs $49.99"

Fact-check:
1. Call inventory API: 
   GET /api/inventory/item-123
   → Returns: {in_stock: true, quantity: 5}
   ✓ Claim verified

2. Call pricing API:
   GET /api/price/item-123
   → Returns: {price: 49.99, currency: USD}
   ✓ Claim verified

3. Both match? Send response.
   4. Mismatch? Escalate + log hallucination.
```

### Policy Data (Knowledge Base)
```
Response: "Returns accepted within 30 days"

Fact-check:
1. Query KB database:
   SELECT policy FROM return_policies 
   WHERE category = 'General'
   → Returns: "Returns accepted within 14 days"
   ✗ Mismatch (response says 30, KB says 14)

2. Hallucination detected
   Escalate + mark response as incorrect
   Send correction: "Sorry, I misspoke. Returns are 14 days."
```

---

## Common Hallucinations & Prevention

### Hallucination 1: Pricing (High Risk)
```
Response: "Your shipping is free over $50"
Reality: Free over $75 (or not free at all)

Prevention:
- NEVER let agent discuss pricing without API lookup
- Price queries must call pricing backend
- Confidence thresholds: >0.95 still fact-check

Implementation:
If "price" or "cost" in response:
  → Fact-check against pricing API
  → If mismatch, block + escalate
```

### Hallucination 2: Eligibility (High Risk)
```
Response: "You're eligible for this discount"
Reality: Only for new customers, you're existing

Prevention:
- Check customer status (new vs. existing)
- Check purchase history
- Verify eligibility rules in KB

Implementation:
If "eligible" or "qualify" in response:
  → Look up customer profile
  → Cross-reference KB eligibility rules
  → If mismatch, escalate
```

### Hallucination 3: Feature Claims (Medium Risk)
```
Response: "Our app has dark mode"
Reality: Dark mode not yet released

Prevention:
- Query feature availability API
- Check feature flags
- Use version date in KB (update regularly)

Implementation:
If "feature" mentioned:
  → Check feature_flags table
  → Verify against released version
  → If uncertain, escalate
```

### Hallucination 4: Timelines (Medium Risk)
```
Response: "You'll get a response within 24 hours"
Reality: SLA is 48 hours

Prevention:
- Keep timelines in KB with explicit dates
- Use facts, not estimates
- Add "(typical)" for variations

Implementation:
If "hour" or "day" or "week" mentioned:
  → Cross-check against KB SLA table
  → If mismatch, block
```

---

## Monitoring for Hallucinations

### Real-Time Detection
```
□ Confidence scores: Track distribution
  - If average drops, model may be hallucinating more
  - Alert if >15% of responses <0.70 confidence

□ Fact-check failures: Track rate
  - Alert if >3% of responses fail fact-checks
  - Investigate causes (bad KB? bad prompt? drift?)

□ Escalation rate: Track trending
  - Alert if escalation rate jumps >10%
  - May indicate increased hallucinations
```

### User Feedback Loop
```
□ Enable "Was this helpful?" thumbs up/down
□ Enable "Incorrect information" flag
□ When flagged:
  - Log response + claim
  - Review for hallucination
  - Update KB if information was wrong
  - Send correction to user

□ Weekly review:
  - Analyze flagged responses
  - Categorize hallucination types
  - Update guardrails (tighten thresholds)
  - Update KB (fill gaps)
```

### Audit Trail
```
For every response sent to user, log:
- User ID
- Question
- Agent response
- Confidence score
- Fact-check results (pass/fail)
- Final output sent
- User feedback (if any)

This enables:
- Root cause analysis
- Trend detection
- Compliance audits
- Quality improvements
```

---

## Follow-Up Questions

### Required to Implement
1. **Do you have a knowledge base of facts?** (policies, specs, FAQs)
2. **What data changes frequently?** (inventory, pricing, dates)
3. **What's your acceptable hallucination rate?** (0%, 2%, 5%?)
4. **Do you have APIs for dynamic data?** (inventory, pricing, customer status)
5. **Can you enable user feedback?** (flag incorrect responses)

### Secondary Clarifications
- How often is your KB updated? (daily, weekly, monthly)
- What's the max acceptable latency? (500ms, 2s, 5s?)
- Should the agent cite sources? ("According to our policy...")
- How escalation SLA? (immediate, 30min, 2hr?)
- Do you need audit logs of all fact-checks?

---

## See Also
- [Agent Assist: Readiness Diagnosis](agent-assist-readiness-diagnosis.md) — Should you use AI agents?
- [Agent Assist: Prompt Design](agent-assist-prompt-design.md) — Writing effective system prompts
- [Agent Assist: Guardrails Checklist](agent-assist-guardrails-checklist.md) — Preventing bad outputs
- [Agent Assist: Fallback to Rules](agent-assist-fallback-to-rules.md) — Escalation patterns
