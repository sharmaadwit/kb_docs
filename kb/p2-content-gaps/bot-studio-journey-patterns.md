# Bot Studio Journey Builder: Advanced Patterns & Conditional Logic

## Overview

Bot Studio's Journey Builder lets you create complex, multi-step conversation flows. This guide covers advanced patterns: conditional branching, state management, error handling, and optimization techniques used in production bots.

---

## Core Concept: Journey as State Machine

Every bot is a state machine:
- **States:** Nodes (Start, Message, Decision, API Call, End)
- **Transitions:** Conditions that move between states
- **Memory:** Variables (user inputs, API responses) persist across steps
- **Terminal states:** End nodes (success, fallback, timeout)

```
Start → Ask Name → [Check name length] → Process → End
          ↓ (store)     ↓ (condition)
       Variable     Branch on condition
```

---

## Pattern 1: Conditional Message Routing

### Use Case
Route users to different conversation paths based on their input, profile, or previous responses.

### Implementation

**Single Condition:**
```
Node: "Ask user type"
Message: "Are you a developer or marketer?"

Decision Node: "Route by type"
Condition: message == "developer" → Path A
Condition: message == "marketer" → Path B
Condition: else → Fallback
```

**Multiple Conditions (AND logic):**
```
Node: "Check eligibility"
Conditions:
  - User in India AND
  - Account age > 30 days AND
  - Monthly message volume > 1000
→ Path: "Offer premium tier"

Else → Path: "Standard tier"
```

**Multiple Conditions (OR logic):**
```
Node: "Check urgency"
Conditions:
  - Issue type == "outage" OR
  - Message contains "urgent" OR
  - Time > 22:00 (night)
→ Path: "Escalate to support"

Else → Path: "Standard resolution"
```

### Pro Tip: Order Conditions Logically
More specific conditions first (easier to debug):
```
✅ GOOD:
  if user.is_enterprise AND user.monthly_volume > 100k → escalate
  if user.monthly_volume > 50k → priority queue
  else → standard queue

❌ BAD:
  if user.monthly_volume > 50k → priority queue
  if user.is_enterprise AND monthly_volume > 100k → escalate (never reached!)
```

---

## Pattern 2: Multi-Turn Conversations with State

### Use Case
Collect information across multiple steps, build context, make decisions based on full state.

### Implementation

**Example: Bot collects campaign details over 4 steps**

```
Step 1: Node "Campaign name"
├─ Message: "What's your campaign name?"
├─ Action: Store input → variable:campaign_name
└─ Transition: Next

Step 2: Node "Target audience"
├─ Message: "Who's your target audience?"
├─ Action: Store input → variable:audience
└─ Transition: Next

Step 3: Node "Budget"
├─ Message: "What's your budget? (in ₹)"
├─ Action: Store input → variable:budget
└─ Transition: Decision node

Decision: "Validate campaign"
├─ Condition: budget > 50000 → Path A (enterprise)
├─ Condition: budget > 10000 → Path B (mid-market)
├─ Condition: else → Path C (SMB)
```

**Accessing collected state:**
In any later node, reference variables:
- `{campaign_name}` = user's answer from Step 1
- `{audience}` = user's answer from Step 2
- `{budget}` = user's answer from Step 3

**State in message template:**
```
Node: "Confirmation"
Message: "Great! I'm setting up a {campaign_name} campaign 
targeting {audience} with budget ₹{budget}. Confirm? (yes/no)"

Then route:
Condition: message == "yes" → Create campaign
Condition: message == "no" → Restart
```

---

## Pattern 3: Graceful Error Handling

### Use Case
Manage invalid inputs, API failures, and edge cases without killing the conversation.

### Implementation

**Retry Logic for Invalid Input:**
```
Node: "Ask budget (numeric)"
├─ Message: "Enter budget in ₹ (numbers only)"
├─ Decision: Is input numeric?
│  ├─ YES → Store to variable:budget → Continue
│  └─ NO → Error counter++
│
Retry node: "Invalid input - retry"
├─ If error_count < 3:
│  └─ Message: "Please enter a number, like 50000"
│     → Back to "Ask budget"
├─ If error_count >= 3:
│  └─ Message: "I'll use your plan limit. Continuing..."
│     → Skip budget, use default
```

**API Failure Handling:**
```
Node: "Call API - Verify business"
├─ Action: Call GET /api/business/{business_id}
├─ On success:
│  └─ Store response → variable:business_verified
│     Transition → Next
├─ On failure (timeout/5xx):
│  └─ Retry counter++
│     If retries < 2: Retry after 2 second delay
│     If retries >= 2: Fallback message
│        "Can't verify right now. Try again later."
```

**Timeout Handling:**
```
Node: "Waiting for user response"
├─ Timeout: 5 minutes
├─ On timeout:
│  ├─ Save current state → database
│  ├─ Message: "Session timed out. Reply START to resume."
│  └─ End journey
│
Resume journey (triggered by START):
├─ Load saved state → variables
├─ Message: "Welcome back! You were at step X..."
└─ Resume from where they left off
```

---

## Pattern 4: Dynamic Button Responses

### Use Case
Present options as buttons instead of free text (better UX, easier parsing).

### Implementation

**Simple Buttons:**
```
Node: "Choose channel"
├─ Message: "Which channel do you use?"
├─ Buttons:
│  ├─ Button 1: "WhatsApp"
│  ├─ Button 2: "SMS"
│  ├─ Button 3: "RCS"
│  └─ Button 4: "Email"
├─ On click:
│  └─ Store button value → variable:selected_channel
│     (no parsing needed, exact value known)
└─ Route based on channel
```

**Button with Follow-Up:**
```
Node: "Quick poll"
├─ Message: "How satisfied are you?"
├─ Buttons: [Very Satisfied, Satisfied, Neutral, Unsatisfied, Very Unsatisfied]
├─ Action: Store rating → variable:satisfaction_score
└─ Decision:
   ├─ If Very Satisfied/Satisfied → "Thank you! Anything else?"
   ├─ If Unsatisfied → "Sorry to hear. What went wrong?"
   └─ If Neutral → "Thanks for feedback. Tips to improve?"
```

**Pro Tip: Keep Buttons Concise**
```
✅ GOOD: [Yes, No]
✅ GOOD: [WhatsApp, SMS, RCS, Email]
❌ BAD: [Let me send you more detailed information about our premium tier offerings]
(Button text too long, confusing)
```

---

## Pattern 5: Complex Branching with Variable Context

### Use Case
Make decisions based on user profile + their inputs (combine database + conversation state).

### Implementation

**Example: Personalized support routing**

```
Step 1: "Collect issue type"
├─ Buttons: [Bug, Feature Request, Billing, Other]
└─ Store → variable:issue_type

Step 2: "Check user tier" (from database)
├─ Action: Call API → GET /users/{user_id}/tier
├─ Responses:
│  ├─ Enterprise → variable:tier = "enterprise"
│  ├─ Pro → variable:tier = "pro"
│  └─ Free → variable:tier = "free"

Decision: "Route by issue + tier"
├─ If issue_type == "Bug" AND tier == "enterprise"
│  └─ Route: "Dedicated support" (SLA: 1 hour)
│
├─ If issue_type == "Bug" AND tier == "pro"
│  └─ Route: "Priority queue" (SLA: 4 hours)
│
├─ If issue_type == "Bug" AND tier == "free"
│  └─ Route: "Community forum + FAQ" (SLA: none)
│
├─ If issue_type == "Billing"
│  └─ Route: "Billing support" (all tiers)
│
└─ Else (Feature requests, etc.)
   └─ Route: "Product team email"
```

**Accessing both sources in message:**
```
Node: "Confirmation"
Message: "Hi {user_name}, your {issue_type} issue 
will be handled by {tier} support. 
Reference: {ticket_id}"

(user_name, tier = from API; issue_type, ticket_id = from conversation)
```

---

## Pattern 6: Loop Detection & Prevention

### Use Case
Prevent infinite loops when users repeatedly ask the same question.

### Implementation

**Loop Counter:**
```
Node: "Answer FAQ"
├─ Counter: same_question_count++
├─ If same_question_count > 3:
│  └─ Break pattern
│     Message: "Looks like I'm repeating myself. 
│               Let me escalate to a human."
│     → Handoff to support
│
├─ If same_question_count == 1-3:
│  └─ Show answer normally
│     → Wait for next input
```

**Session Memory Reset:**
```
Node: "Timeout or session end"
├─ After 30 min of inactivity:
│  ├─ Save variables to database (for resume)
│  ├─ Clear loop counter
│  └─ End journey
│
Node: "Resume session"
├─ Load saved variables (but reset counters)
├─ Message: "Welcome back!"
└─ Continue from last step
```

---

## Pattern 7: Fallback Chains

### Use Case
Handle unexpected inputs gracefully (user says something bot doesn't understand).

### Implementation

**Intelligent Fallback:**
```
Node: "Decision: Understand input"
├─ Try to match against known intents
│
├─ Fallback 1 (60% confidence):
│  └─ Message: "Did you mean [intent]? (Yes/No)"
│     If No → Fallback 2
│
├─ Fallback 2 (30% confidence):
│  └─ Message: "Can you rephrase that?"
│     Show buttons: [Issue type 1, Issue type 2, Issue type 3]
│
├─ Fallback 3 (exhausted):
│  └─ Message: "I'm not sure. Let me connect you with support."
│     → Handoff to agent
```

---

## Common Mistakes

### ❌ Mistake 1: Unreachable Branches

```
❌ WRONG:
Decision node:
├─ If user_age > 18 → Path A
├─ If user_age > 21 → Path B (NEVER REACHED! Already caught by first condition)

✅ CORRECT:
Decision node:
├─ If user_age > 21 → Path A
├─ If user_age > 18 AND user_age <= 21 → Path B
├─ If user_age <= 18 → Path C
```

### ❌ Mistake 2: Lost Variables

```
❌ WRONG:
Step 1: Store email → variable:user_email
Step 2: Use {user_email} in message
Step 3: Later... try to use {user_email} (not in scope if journey restarted)

✅ CORRECT:
Step 1: Store to database (not just journey memory)
Step 2: Load from database when needed
Step 3: Persist persists across sessions
```

### ❌ Mistake 3: Too Many Buttons

```
❌ WRONG:
Buttons: [Option 1, Option 2, Option 3, Option 4, Option 5, Option 6]
(User can't read, needs to scroll)

✅ CORRECT:
Step 1: Buttons: [Category A, Category B]
Step 2 (based on choice): Buttons: [Sub-option 1, Sub-option 2, Sub-option 3]
(Progressive disclosure)
```

---

## Performance Tips

### Optimize Decision Nodes

**Move specific checks first:**
```
✅ FASTER:
├─ If user_type == "test_user" → Fallback (eliminates 99% of traffic)
├─ If status == "premium" AND volume > 100k → Premium flow
├─ Else → Standard flow

❌ SLOWER:
├─ If status == "premium" → Check volume (every user)
├─ If user_type == "test_user" → Fallback (redundant check)
```

### Batch API Calls

```
❌ INEFFICIENT:
Step 1: Call API → Get user tier (1 call)
Step 2: Call API → Get user quota (2 calls)
Step 3: Call API → Get support tier (3 calls)

✅ EFFICIENT:
Step 1: Call API → Get user profile (includes tier, quota, support_tier in 1 call)
Step 2-3: Use fields from Step 1 (no additional calls)
```

---

## Testing Checklist

Before deploying a journey to production:

- [ ] Test happy path (best case scenario)
- [ ] Test each error branch separately
- [ ] Test with empty/null inputs
- [ ] Test timeout conditions
- [ ] Test with invalid data (symbols, very long strings)
- [ ] Test API failures (mock API down)
- [ ] Test button clicks (all options)
- [ ] Test state persistence (close/reopen app)
- [ ] Test with different user tiers/profiles
- [ ] Monitor loop counter for infinite loops

---

## FAQ

**Q: Can variables persist across multiple journeys?**
A: Yes, store in database, not just journey memory. Use user_id as key for durability.

**Q: What's the max number of steps in a journey?**
A: No hard limit, but >50 steps = likely needs refactoring. Consider breaking into sub-journeys.

**Q: How do I test conditional logic before going live?**
A: Use Bot Studio's Debug mode. Set variable values manually, trace through each branch.

**Q: Can I A/B test two different message flows?**
A: Yes. Use Decision node at start: `if random(0,1) < 0.5 → Flow A, else → Flow B`. Track outcomes separately.

---

**Last Updated:** 2026-08-11  
**Platform:** Gupshup Bot Studio Journey Builder
