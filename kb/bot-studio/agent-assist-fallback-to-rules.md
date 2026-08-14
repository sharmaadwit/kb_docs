# Agent Assist: Fallback to Rules

## Diagnosis
**When should the AI agent hand off to rules or escalate to humans?**

The best agent is not "AI all the way" but rather a **hybrid system that knows its limits**. Confidence thresholds, topic boundaries, and escalation paths prevent the agent from making catastrophic mistakes on edge cases. This guide covers when and how to fall back to safer systems.

---

## Context: Why Fallback Matters

### Rule-Based Decisions vs. AI Decisions
```
RULES (100% correct, but brittle):
- IF item_value < $50 AND days_since_purchase < 14 THEN approve

AI AGENTS (Flexible, but ~5% error):
- "Let me assess this situation and recommend..."
```

### The Fallback Philosophy
1. **High confidence + safe topic** → Use AI (efficiency)
2. **Low confidence OR risky topic** → Use rules (safety)
3. **Completely uncertain** → Escalate to human (accuracy)

### Fallback Paths
```
USER REQUEST
    ↓
Does AI have high confidence (>0.85)?
├─ YES: Is this a low-risk topic?
│       ├─ YES → Use AI response ✓
│       └─ NO → Escalate to rules / human
└─ NO → Fallback to rules or escalate
```

---

## Options & Fallback Strategies

### Option 1: Confidence-Based Fallback (Simple)
```
Fallback rule: Confidence < 0.70 → Use rules

Effect:
- Low confidence questions go to rules
- High confidence questions use AI
- Escalation rate: ~15-25% of traffic

Accuracy:
- Confidence >0.85: 95% accuracy
- Confidence <0.70: 70% accuracy

Strengths:
- Simple to implement
- Catches most uncertain cases
- Maintains UX (most use AI)

Weaknesses:
- High-confidence hallucinations still reach users
- Rules may not handle all edge cases
- No escalation path (just picks rules)
```

**When to use**: Initial implementation, add more sophistication later

---

### Option 2: Topic-Based Fallback (Structured)
```
Fallback rule: 
- Returns/refunds questions → AI ok (confidence >0.80)
- Pricing questions → ALWAYS rules (never AI)
- Eligibility questions → Rules if confidence <0.85
- Complaints → ALWAYS escalate to human

Effect:
- Different confidence thresholds per topic
- High-risk topics never use AI
- Escalation rate: ~20-30% of traffic

Strengths:
- Tailored to risk profile of each topic
- Prevents hallucinations on critical topics
- Clear rules about what AI can discuss

Weaknesses:
- Requires topic classification (adds complexity)
- May be overly conservative
- Requires manual topic mapping
```

**When to use**: Medium-risk systems, some topics more important than others

---

### Option 3: Hybrid (Confidence + Topic + Fact-Check) [Recommended]
```
Fallback rule:
1. Classify user question by topic
2. If topic is high-risk (pricing, eligibility) → Use rules
3. Else if confidence <0.65 → Escalate to human
4. Else → Run fact-check
   - Pass → Send AI response
   - Fail → Escalate to human
5. If escalation needed → Route to appropriate queue

Effect:
- Confidence thresholds per topic
- Fact-checking before sending
- Smart escalation routing
- Escalation rate: ~25-35% of traffic

Accuracy:
- AI responses only if confidence >0.65 + facts verified
- Rules handle high-confidence edge cases
- Humans resolve true edge cases

Strengths:
- Maximum safety without total coverage loss
- Flexible per topic
- Catches hallucinations + uncertainty
- Clear escalation paths

Weaknesses:
- Implementation complexity
- Requires fact-check backend
- Higher latency (fact-checking adds time)
```

**Recommended for production systems**

---

## Recommended Approach: Hybrid (Confidence + Topic + Fact-Check)

### Implementation Architecture
```
[User Question]
    ↓
[Topic Classification]
(Returns, Pricing, Eligibility, Complaint, Other)
    ↓
[Confidence Check]
(Classify high-risk topics)
    ├─ Topic = "Pricing" → [RULES ONLY]
    ├─ Topic = "Eligibility" + Low confidence → [ESCALATE]
    └─ Other → [Check Confidence]
    ↓
[Confidence Threshold by Topic]
Topic          Threshold   Action if Below
─────────────────────────────────────────────
Pricing        N/A         Always rules
Eligibility    >0.85       Escalate
Returns        >0.75       Escalate
Complaints     N/A         Always escalate
Order status   >0.70       Escalate
Other          >0.65       Escalate
    ↓
[Fact-Check (if confidence passes)]
    ├─ Pass → [Send AI response]
    └─ Fail → [Escalate]
    ↓
[Escalation Routing]
    ├─ Low confidence + billing → Billing specialist
    ├─ Policy violation → Compliance team
    ├─ Angry customer → Senior specialist
    └─ General edge case → Support queue
```

### Topic Classification

#### High-Risk Topics (Use Rules Only)
```
Topic: PRICING
Examples: "How much is this?", "What's your shipping cost?"
Why: Hallucinations cost money (revenue impact)
Fallback: Rules only, never AI
Config:
  threshold: N/A (disabled)
  fallback_type: RULES
  escalate_if: Unsure (confidence <0.95)

Topic: COMPLIANCE / POLICY
Examples: "GDPR compliance?", "Do you collect data?"
Why: Legal liability, regulatory risk
Fallback: Rules only, never AI
Config:
  threshold: N/A (disabled)
  fallback_type: RULES
  escalate_if: Any non-standard question

Topic: FINANCIAL COMMITMENT
Examples: "Do I get a refund?", "Will you pay me back?"
Why: Money commitment, disputes expensive
Fallback: Rules if clear-cut, else escalate
Config:
  threshold: 0.90 (very high)
  fallback_type: ESCALATE (if <0.90)
  escalate_queue: Financial specialist
```

#### Medium-Risk Topics (Use AI with Confidence Thresholds)
```
Topic: ELIGIBILITY / QUALIFICATION
Examples: "Can I return this?", "Am I eligible for discount?"
Why: Complex logic, but important to get right
Fallback: AI if confidence >0.85, else escalate
Config:
  threshold: 0.85
  fallback_type: ESCALATE
  escalate_queue: Support specialist

Topic: CUSTOMER STATUS / HISTORY
Examples: "How many returns have I had?", "What's my status?"
Why: Requires data lookup, some risk
Fallback: AI if confidence >0.80, else escalate
Config:
  threshold: 0.80
  fallback_type: ESCALATE
  escalate_queue: Support team

Topic: ORDER STATUS / LOGISTICS
Examples: "Where's my order?", "When will it arrive?"
Why: Time-sensitive, but can be looked up
Fallback: AI if confidence >0.75, else escalate
Config:
  threshold: 0.75
  fallback_type: ESCALATE
  escalate_queue: Logistics team
```

#### Low-Risk Topics (AI Acceptable)
```
Topic: GENERAL INFO / FAQ
Examples: "Do you have a store?", "What's your mission?"
Why: Low stakes, mistakes recoverable
Fallback: AI if confidence >0.65
Config:
  threshold: 0.65
  fallback_type: ESCALATE_IF_VERY_LOW
  escalate_queue: Support queue

Topic: PRODUCT SPECS / FEATURES
Examples: "What colors does this come in?", "Does it have Bluetooth?"
Why: Factual, but can be fact-checked
Fallback: AI if confidence >0.70 (with fact-check)
Config:
  threshold: 0.70
  fallback_type: FACT_CHECK_REQUIRED
  fact_check_db: Product specs API
```

### Confidence Thresholds

#### Thresholds by Risk Level
```
Risk Level    Threshold   Reasoning
──────────────────────────────────────────────────
CRITICAL      > 0.95      (Pricing, finance, compliance)
HIGH          > 0.85      (Eligibility, refunds)
MEDIUM        > 0.75      (Returns, order status)
LOW           > 0.65      (FAQ, general info)
```

#### Confidence Interpretation
```
Confidence 0.95-1.00: "I'm very sure"
  → Send to user (after fact-check if factual)
  
Confidence 0.85-0.95: "I'm fairly sure"
  → Check topic, fact-check if needed
  → Medium-risk: send if facts verify
  → High-risk: escalate

Confidence 0.70-0.85: "I think so"
  → Medium-risk: escalate
  → Low-risk: send if facts verify

Confidence 0.50-0.70: "I'm guessing"
  → Always escalate (don't send)

Confidence < 0.50: "No idea"
  → Definitely escalate (don't send)
```

### Escalation Routing Matrix

```
Condition                     Escalation Queue    SLA
─────────────────────────────────────────────────────
Confidence < 0.65            Support Queue       2 hours
+ Pricing question           (any)               

Confidence 0.65-0.80         Specialist Queue    2 hours
+ Eligibility question       (billing/returns)   

Confidence 0.80-0.90         Specialist Queue    1 hour
+ Policy/compliance          (compliance team)   

Confidence < 0.85            Manager Queue       30 min
+ Customer angry/frustrated  (senior specialist) 

Fact-check FAILED            Compliance Team     Immediate
+ PII/hallucination          (P0 priority)       

Out-of-scope topic           Specialist Queue    2 hours
(agent uncertain)            (relevant domain)   
```

---

## Implementation Checklist

### Step 1: Define Topic Categories
```
□ Map all possible user questions to topics:
  - Returns & Refunds
  - Pricing & Billing
  - Shipping & Logistics
  - Product Info
  - Account & Status
  - Compliance & Policies
  - Complaints & Escalations
  - Other

□ For each topic, define:
  - Risk level (Critical/High/Medium/Low)
  - Confidence threshold
  - Fallback strategy (Rules/Escalate/Both)
  - Escalation destination
  - SLA for response
```

### Step 2: Implement Topic Classifier
```
□ Train classifier (or use prompt-based classification):
  - Input: User question
  - Output: Topic + confidence

□ Example implementation:
  prompt = f"""
  Classify this question:
  "{user_question}"
  
  Categories:
  1. Returns & Refunds
  2. Pricing & Billing
  ...
  
  Return JSON: {{"topic": "Returns & Refunds", 
                 "confidence": 0.95}}
  """

□ Test classifier on 100+ real questions
  - Target accuracy: >90%
  - Misclassifications escalate (safer)
```

### Step 3: Set Confidence Thresholds
```
□ Define per-topic thresholds:
  Returns: 0.75
  Pricing: N/A (rules only)
  Eligibility: 0.85
  etc.

□ Implement threshold check:
  if agent_confidence < topic_threshold:
    escalate_to_queue(topic)
  else:
    send_response()

□ Monitor escalation rates:
  - If >40% escalating → thresholds too high
  - If <10% escalating → thresholds too low
  - Adjust based on error rates
```

### Step 4: Build Escalation Queues
```
□ Define queues:
  - Support Queue (general, 2-hour SLA)
  - Billing Specialist (pricing, refunds)
  - Compliance Team (policies, P0 urgent)
  - Manager Queue (complaints, frustration)
  - Logistics Team (shipping questions)

□ Route escalations:
  if topic == "Pricing":
    queue = "Billing Specialist"
  elif topic == "Compliance":
    queue = "Compliance Team"
    priority = "P0"
  else:
    queue = "Support Queue"
    priority = "P2"

□ Track SLA compliance:
  - Log escalation time
  - Log resolution time
  - Alert if SLA breach
```

### Step 5: Monitor & Adjust
```
□ Weekly metrics:
  - Escalation rate per topic (target: 20-30%)
  - Confidence distribution (should be bimodal)
  - User satisfaction on escalated issues
  - Error rate on AI responses (target: <3%)

□ Monthly adjustment:
  - Review escalations for false positives
  - Adjust thresholds if needed
  - Update topic classifier if drift detected
  - Retrain on recent data

□ Quarterly review:
  - Compare AI accuracy vs. rules
  - Identify topics ready for AI
  - Identify topics requiring more guardrails
  - Update strategy doc
```

---

## Example Scenarios

### Scenario 1: Returns Question (Medium Risk)
```
User: "Can I return this item?"
Topic Classification: Returns & Refunds (confidence 0.98)
AI Agent Response: "Yes, within 30 days for most items" 
                   (confidence 0.82)

Decision Tree:
1. Topic = "Returns" → threshold = 0.75
2. AI confidence = 0.82 > 0.75 ✓
3. Fact-check: "30 days" → KB says "30 days" ✓
4. All checks pass

Action: Send AI response to user ✓
```

### Scenario 2: Pricing Question (High Risk)
```
User: "How much is free shipping?"
Topic Classification: Pricing & Billing (confidence 0.99)
AI Agent Response: "Free over $50" (confidence 0.88)

Decision Tree:
1. Topic = "Pricing" → Use RULES ONLY (no AI)

Action: Query pricing rules database
        Rules say: "Free over $75"
        Send rules response: "Free shipping on orders over $75" ✓
```

### Scenario 3: Low Confidence (Uncertain)
```
User: "Will you waive my restocking fee?"
Topic Classification: Eligibility (confidence 0.92)
AI Agent Response: "That depends on the situation" 
                   (confidence 0.42)

Decision Tree:
1. Topic = "Eligibility" → threshold = 0.85
2. AI confidence = 0.42 < 0.85 ✗
3. Confidence too low

Action: Escalate to Support Specialist
        Response: "I'll connect you with a specialist 
                  who can review your specific situation" ✓
```

### Scenario 4: Angry Customer (Escalate)
```
User: "Your product is garbage! I want a refund NOW!"
Topic Classification: Complaint (confidence 0.95)
AI Agent Response: (acknowledges frustration, explains policy)
Emotion Detection: Customer frustrated (sentiment score: -0.8)

Decision Tree:
1. Topic = "Complaint" → Always escalate
2. Emotion = Frustrated/Angry → High priority

Action: Escalate to Manager Queue (30-min SLA, P1 priority)
        Response: "I understand your frustration. 
                  A manager will call you within 30 minutes" ✓
```

---

## Follow-Up Questions

### Required to Configure
1. **What's your acceptable error rate?** (2%, 5%, 10%?)
2. **Which topics are highest risk?** (pricing, compliance, finance)
3. **How much escalation can you handle?** (10%, 20%, 50% of traffic?)
4. **What escalation capacity do you have?** (# of specialists available)
5. **What's your SLA for escalations?** (immediate, 30min, 2hr?)

### Secondary Clarifications
- Do you have topic classification capability?
- Can you measure AI confidence on your model?
- Do you have specialized teams for different topics?
- Should escalations be sync (live chat) or async (callback)?
- Do you need audit logs of all fallback decisions?

---

## See Also
- [Agent Assist: Readiness Diagnosis](agent-assist-readiness-diagnosis.md) — Should you use AI agents?
- [Agent Assist: Prompt Design](agent-assist-prompt-design.md) — Writing effective system prompts
- [Agent Assist: Guardrails Checklist](agent-assist-guardrails-checklist.md) — Preventing bad outputs
- [Agent Assist: Hallucination Mitigation](agent-assist-hallucination-mitigation.md) — RAG + fact-checking
