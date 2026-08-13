# Preventing Infinite Loops in Bot Studio: Detection & Exit Strategies

## Diagnosis: What's Causing Your Loop?

Infinite loops in Bot Studio manifest in three ways:

1. **User keeps returning to the same node** (e.g., Message A → Decision → Message A, creating a cycle)
2. **Bot asks the same question repeatedly** because a condition always evaluates true (logic error)
3. **Journey never reaches an end state** because there's no exit condition

**Identifying the root:** Check your journey canvas for cyclic arrows (node pointing back to itself or earlier node). In analytics, look for users stuck on one node for >10 turns. In traces, observe the same message being sent repeatedly.

## Context: Common Loop Patterns

**Message-to-message looping** (Node A → Decision → Node A): User input doesn't match any condition, so fallback routes back to the same question.

**Condition always true** (logic error): A rule like 'if message contains X' matches every user input, trapping users in one branch.

**No exit node/timeout**: Journey lacks an explicit End Node or timeout mechanism, so it continues indefinitely waiting for user input.

**Prevention requires three layers:**
1. Exit conditions at decision points (every branch must eventually reach an End Node)
2. Conversation depth limits (max 30-50 turns per session)
3. Timeout-based exits (close conversation after 5-30 minutes of inactivity)

## Options: Four Prevention Strategies

### Option 1: Add Exit Conditions to Loops
**Action:** Every decision node must have a fallback that either routes elsewhere or ends the journey. Do NOT route fallback back to the same node.

**Pattern:** Fallback → 'I didn't understand, try again' (counter++) → if counter > 3, end or escalate

**Setup time:** 5 minutes per decision node

### Option 2: Limit Conversation Depth (Max Turns)
**Action:** Use a variable `conversation_turn_count`, increment it each step, and if `conversation_turn_count > 30`, force end with message 'Session limit reached. Reply HELP for options.'

**Setup:** Add turn counter to every node transition. Prevents accidental infinite loops even if logic is flawed.

### Option 3: Fallback to Human (Escalation Path)
**Action:** When loop is detected (same node visited 3+ times, or `conversation_turn_count > 20`), route to human agent or support team via handoff node.

**Ensures:** User doesn't get stuck; they reach a human instead.

**Best for:** Critical workflows (support, billing) where you can't afford loops.

### Option 4: Timeout-Based Exit (Max 30 Sec per Loop)
**Action:** Set node-level timeout (e.g., 'Wait for user response, timeout after 30 sec'). On timeout, either ask a different question or escalate.

**Prevents:** Long waits if bot logic is stuck.

## Recommended Approach

**Combine Options 1 + 3:** Always add exit conditions to decision nodes (prevents root cause), AND add escalation to human if user is looping (catches any bugs you missed). This dual approach is the industry standard for production bots.

## Follow-Up Questions

How do you want to exit the loop?
- (a) Re-route to a different question?
- (b) Offer user a menu of alternatives?
- (c) Escalate to human support?
- (d) End session and ask user to start over?

Your answer determines which option to implement.

## See Also

- **Pattern: Loop Detection & Prevention:** Detailed examples with loop counters and session memory reset
- **Prompt Nodes: Number of Retries setting:** Built-in retry logic for failed validations (default 3 retries, configurable up to infinite)
- **Exit Nodes:** Terminal states in bot journeys; every flow should lead to an explicit end
- **Bot Studio Analytics: Conversational Path view:** Shows cyclic nodes (nodes that loop back); use to identify problematic flows
- **Test your Bot:** Trace through your journey manually to find loops before going live
