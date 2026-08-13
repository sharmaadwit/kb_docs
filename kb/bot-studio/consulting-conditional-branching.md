# Conditional Branching in Bot Studio: Choosing Your Routing Strategy

## Diagnosis: What's Your Routing Scenario?

When building conversational journeys, bot designers face three common routing needs:

1. **Response-based routing** — Users select from predefined options (e.g., buttons for 'WhatsApp' vs 'SMS' vs 'Email')
2. **API-based routing** — External data drives the decision (e.g., fetch user tier from database, then route to premium vs standard support flow)
3. **Multi-condition logic** — Complex rules combine user inputs, profile data, and business rules (e.g., 'if budget > 50k AND location == India AND account_age > 30 days, offer enterprise tier')

Each scenario demands a different decision node implementation. Choosing the wrong path leads to confused users or maintenance headaches.

## Context: How Decision Nodes Work

Conditional branching in Bot Studio uses the **Condition Node** as the primary if/else control:

- A **Message or Prompt Node** collects user input or references an existing variable (from API calls, database lookups, or previous steps)
- The **Condition Node** evaluates that input against one or more rules using operators like equals, contains, greater than, or custom expressions
- Each matching condition routes to a different node; unmatched input follows the fallback path

**Prerequisites:** You need at least one Message Node (to collect input), one Condition Node (to branch), and variables to evaluate (from user input or API responses).

**When to use:** Response-based branching (buttons make parsing reliable), API-driven decisions (external data + variables), multi-tier user segmentation (enterprise vs SMB flows).

**When to avoid:** Avoid Condition Nodes for simple pass-through logic (where every input maps to the same next step); use direct connectors instead. Also avoid deeply nested conditions (>5 levels) as they become hard to debug—instead, break into sub-journeys.

## Options: Three Implementation Approaches

### Option 1: Simple Response Branching
**How it works:** User selects from buttons → Condition Node evaluates button text → Routes to one of N paths

- **Best for:** Lead qualification (Choose: Sales / Support / Account Management)
- **Accuracy:** 99% (buttons have fixed values)
- **Setup time:** 5 minutes
- **Example:** Message 'Which channel do you prefer?' with buttons [WhatsApp, SMS, Email] → Condition node routes each to channel-specific workflow

### Option 2: API-Based Routing
**How it works:** Fetch external data (API Node call) → store response in variables → Condition Node evaluates those variables → routes based on API response

- **Best for:** Personalization by user tier, dynamic pricing, inventory checks
- **Accuracy:** 95-99% (if API is stable)
- **Setup time:** 10-15 minutes (requires API configuration)
- **Example:** Call `GET /users/{id}/tier` → get 'enterprise'/'pro'/'free' → Condition routes enterprise users to dedicated support, others to standard queue

### Option 3: Multi-Condition Logic (AND/OR chaining)
**How it works:** Combine multiple rules using AND (all must match) or OR (any match triggers branch)

- **Best for:** Complex eligibility rules, SLA routing, fraud detection
- **Accuracy:** 98%+ (rules-based, deterministic)
- **Setup time:** 15-20 minutes (requires careful rule ordering)
- **Example:** If `(issue_type == 'Bug' AND user_tier == 'enterprise' AND time > 18:00)` route to 24/7 support, else if `(issue_type == 'Bug' AND user_tier in [pro, free])` route to standard queue

## Recommended Approach

**Start with Option 1 (Simple Response Branching)** for your first bot. It's fastest to implement, easiest to test, and has zero dependencies. Once you validate the flow, add **Option 2 (API-based routing)** if you need personalization or external data. Avoid **Option 3** initially—multi-condition logic makes debugging harder and is better tackled after you're comfortable with Decision Nodes.

## Follow-Up Questions

Which routing scenario fits your use case?
- Are you starting with buttons (user selection)?
- Do you have external data to fetch (API)?
- Do you need to combine multiple rules (complex logic)?

Once you clarify, the specific Condition Node setup becomes straightforward.

## See Also

- **Condition Node (reference):** Bot Studio's if/else control, supports message evaluation and variable-based decisions
- **API Node: HTTP Status Code Branching:** Route based on API response codes (200/400/500), useful for error handling
- **Pattern: Complex Branching with Variable Context:** Examples combining user profile data with conversation state
- **Pattern: Fallback Chains:** Gracefully handle unmatched conditions across multiple fallback levels
- **Test your Bot:** Validation interface where you can trigger each branch and confirm routing works end-to-end
