# Skill-level patch prompt (full file)

**Use this file for the agent.** It contains only patches for skill files. No local/temp file patches (e.g. tmp_regression_500.py) are included; those are applied locally.

**Instructions for the agent:** Apply only the following search-and-replace edits. Use exact string match. Do not change any other code. Do not touch telemetry-related code. If a "Find" block is not found, skip that patch and continue. Files in scope: `kb_answer.py`, `kb_search.py`.

---

## 1. `kb_answer.py` — OFFTOPIC_TERMS

**Find (exact):**
```python
OFFTOPIC_TERMS = ["cricket", "ipl", "football", "weather", "biryani", "pizza", "burger", "dinner", "japan", "iphone", "birthday", "bored", "joke", "movie"]
```

**Replace with:**
```python
OFFTOPIC_TERMS = [
    "cricket", "ipl", "football", "weather", "biryani", "pizza", "burger", "dinner",
    "japan", "iphone", "birthday", "bored", "joke", "movie",
    "tv show", "phone to buy", "workout routine", "travel plan", "cricket score",
]
```

---

## 2. `kb_answer.py` — UNSUPPORTED_PATTERNS

**Find (exact):**
```python
UNSUPPORTED_PATTERNS = [
    "two different callback urls",
    "two callback urls",
    "a b test",
    "ab test",
    "preview campaign analytics before",
    "sync across different browsers",
    "sync across browsers",
    "recycle bin",
    "pin reopened chats permanently",
    "dark mode",
    "download raw bot execution traces",
    "multi region webhook failover",
    "voice call escalation",
    "send campaign analytics automatically to s3",
]
```

**Replace with:**
```python
UNSUPPORTED_PATTERNS = [
    "two different callback urls",
    "two callback urls",
    "different callback urls",
    "callback urls for delivered and read",
    "a b test",
    "ab test",
    "preview campaign analytics before",
    "campaign analytics be previewed",
    "sync across different browsers",
    "sync across browsers",
    "sync retained anonymous chat history across devices",
    "sync automatically across browsers",
    "recycle bin",
    "restore deleted goal analytics exports",
    "schedule goal analytics exports",
    "two parallel backend requests",
    "one api node send two parallel",
    "per event webhook retry",
    "pin reopened chats permanently",
    "dark mode",
    "download raw bot execution traces",
    "multi region webhook failover",
    "voice call escalation",
    "send campaign analytics automatically to s3",
]
```

---

## 3. `kb_answer.py` — Save vs Deploy exact-case block

**Find (exact):**
```python
    if any(x in q for x in [
        "saved changes are not yet live on the channel",
        "draft is updated but production behavior is still old",
        "saved versus actually live",
        "pushing live behavior",
        "customers still see the old bot",
        "production bot still behaves old",
        "changes are merely saved versus actually live"
    ]):
        return "\n".join([
            "Use Save when",
            "- `Save` stores progress in Bot Studio.",
            "Use Save & Deploy when",
            "- `Save & Deploy` pushes the latest saved changes live to the channel.",
        ])
```

**Replace with:**
```python
    if any(x in q for x in [
        "saved changes are not yet live on the channel",
        "concept explains why saved",
        "not yet live on the channel",
        "draft is updated but production behavior is still old",
        "production behavior is still old",
        "saved versus actually live",
        "merely saved versus actually live",
        "pushing live behavior",
        "gap between saving progress and pushing live",
        "customers still see the old bot",
        "production bot still behaves old",
        "changes are merely saved versus actually live",
        "testing looks right but customers still see the old bot",
    ]) or ("save" in q and "deploy" in q and ("live" in q or "concept" in q or "difference" in q or "draft" in q)):
        return "\n".join([
            "Use Save when",
            "- `Save` stores progress in Bot Studio.",
            "Use Save & Deploy when",
            "- `Save & Deploy` pushes the latest saved changes live to the channel.",
        ])
```

---

## 4. `kb_answer.py` — Condition Node exact-case

**Find (exact):**
```python
    if (
        ("journey builder" in q or "bot studio" in q)
        and any(term in q for term in [
            "condition node",
            "branch based on variable",
            "branch based on a variable value",
            "branching based on a variable value",
            "if else branching",
            "if else",
            "fallback branch logic",
            "branch logic",
            "fallback path",
        ])
    ):
        return "\n".join([
            "The documentation indicates you should use `Condition Node` for this pattern.",
            "",
            "Recommended setup",
            "- Open the target journey in `Journey Builder` and add or open `Condition Node`.",
            "- Select whether the condition should evaluate the current user message or another variable.",
            "- Configure the condition/operator and comparison value.",
            "- Connect each branch to the correct next node and configure the fallback path.",
            "",
            "Validation",
            "- Use `Test your Bot` to trigger each expected branch value and confirm unmatched input follows the fallback path.",
        ])
```

**Replace with:**
```python
    if (
        ("journey builder" in q or "bot studio" in q or "journey" in q)
        and any(term in q for term in [
            "condition node",
            "branch based on variable",
            "branch based on a variable value",
            "branching based on a variable value",
            "if else branching",
            "if else",
            "fallback branch logic",
            "branch logic",
            "fallback path",
            "else path when none of the condition checks match",
            "configure an else path",
            "fallback handling when branch conditions fail",
            "conditional routing from parsed response values",
        ])
    ):
        return "\n".join([
            "The documentation indicates you should use `Condition Node` for this pattern.",
            "",
            "Recommended setup",
            "- Open the target journey in `Journey Builder` and add or open `Condition Node`.",
            "- Select whether the condition should evaluate the current user message or another variable.",
            "- Configure the condition/operator and comparison value.",
            "- Connect each branch to the correct next node and configure the fallback path.",
            "",
            "Validation",
            "- Use `Test your Bot` to trigger each expected branch value and confirm unmatched input follows the fallback path.",
        ])
```

---

## 5. `kb_answer.py` — Manage Variables exact-case

**Find (exact):**
```python
    if (
        ("journey builder" in q or "bot studio" in q)
        and ("save user input into a variable" in q or "store user input" in q or "reuse it later" in q)
    ):
        return "\n".join([
            "The documentation indicates you should use `Manage Variables` for this pattern.",
            "",
            "Recommended setup",
            "- Create or select the required variable in `Bot Studio -> Manage Variables`.",
            "- Store the user input into that variable so it can be reused later in the journey.",
            "- If you need to transform or update the value after capture, use `Modify Variable Node`.",
            "",
            "Useful related components",
            "- `Manage Variables` defines and manages the variable.",
            "- `Modify Variable Node` is used when you need to update or transform the stored value.",
        ])
```

**Replace with:**
```python
    if (
        ("journey builder" in q or "bot studio" in q or "journey" in q)
        and any(term in q for term in [
            "save user input into a variable",
            "store user input",
            "reuse it later",
            "define reusable journey variables",
            "reusable journey variables",
            "create a variable so multiple nodes can reference",
            "manages variables used across a journey",
            "set up variables before capturing user input",
            "prepare journey variables ahead of",
            "manage variables",
        ])
    ):
        return "\n".join([
            "The documentation indicates you should use `Manage Variables` for this pattern.",
            "",
            "Recommended setup",
            "- Create or select the required variable in `Bot Studio -> Manage Variables`.",
            "- Store the user input into that variable so it can be reused later in the journey.",
            "- If you need to transform or update the value after capture, use `Modify Variable Node`.",
            "",
            "Useful related components",
            "- `Manage Variables` defines and manages the variable.",
            "- `Modify Variable Node` is used when you need to update or transform the stored value.",
        ])
```

---

## 6. `kb_answer.py` — Add Modify Variable Node exact-case (insert after Manage Variables block)

**Find (exact):** This is the line that immediately follows the Manage Variables `])` and the closing `])` of the return, i.e. the start of the Trigger Event Node block:

```python
        ])
    if ("trigger event node" in q or "send custom event" in q or "event manager" in q) and ("journey builder" in q or "bot studio" in q):
```

**Replace with:**
```python
        ])
    if any(term in q for term in [
        "modify variable node",
        "transform a variable value",
        "updates an existing variable after it has already been stored",
        "variable transformation rather than initial creation",
        "saved variable needs to be updated",
        "change stored values",
    ]) and ("journey builder" in q or "bot studio" in q or "journey" in q or "variable" in q):
        return "\n".join([
            "The documentation indicates you should use `Modify Variable Node` for this pattern.",
            "",
            "Recommended setup",
            "- Ensure the variable already exists (create it in `Manage Variables` if needed).",
            "- Add `Modify Variable Node` at the point where the stored value should be updated or transformed.",
            "- Select the variable and the operation (e.g. set, append, increment).",
            "- Use the modified value in later steps or in `Condition Node` for branching.",
            "",
            "Useful related components",
            "- `Manage Variables` defines the variable; `Modify Variable Node` updates it inside the journey.",
        ])
    if ("trigger event node" in q or "send custom event" in q or "event manager" in q) and ("journey builder" in q or "bot studio" in q):
```

---

## 7. `kb_answer.py` — Goal Node exact-case

**Find (exact):**
```python
    if ("goal node" in q or "track milestones" in q or "track purchase milestone" in q) and ("journey builder" in q or "bot studio" in q):
        return "\n".join([
            "The documentation indicates you should use `Goal Node` for this pattern.",
            "",
            "Recommended setup",
            "- Add `Goal Node` at the milestone you want to track in the journey.",
            "- Use it to track milestone attainment for users interacting with the bot.",
            "- If useful, enable the analytics toggle to see traversal and drop-outs for that goal.",
        ])
```

**Replace with:**
```python
    if (
        ("goal node" in q or "track milestones" in q or "track purchase milestone" in q
         or "conversion milestone" in q or "milestone tracking" in q or "count toward goal analytics" in q
         or "goal achievement inside the flow" in q or "mark a purchase or signup milestone" in q
         or "records that a user reached a conversion milestone" in q)
        and ("journey builder" in q or "bot studio" in q or "journey" in q or "flow" in q)
    ):
        return "\n".join([
            "The documentation indicates you should use `Goal Node` for this pattern.",
            "",
            "Recommended setup",
            "- Add `Goal Node` at the milestone you want to track in the journey.",
            "- Use it to track milestone attainment for users interacting with the bot.",
            "- If useful, enable the analytics toggle to see traversal and drop-outs for that goal.",
        ])
```

---

## 8. `kb_answer.py` — Add API + JSON Handler + Condition Node chain exact-case (insert after Goal Node block, before WhatsApp Flow block)

**Find (exact):**
```python
        ])
    if ("flow trigger" in q or "launch a whatsapp flow" in q) and ("journey builder" in q or "whatsapp flow" in q):
```

**Replace with:**
```python
        ])
    if (
        ("journey builder" in q or "bot studio" in q or "journey" in q)
        and (
            ("call an api" in q or "call api" in q) and ("parse" in q or "response" in q) and ("branch" in q or "conditional" in q)
            or ("api node" in q and "json handler" in q and "condition node" in q)
            or ("api node" in q and "parse the response" in q and "branch" in q)
        )
    ):
        return "\n".join([
            "The documentation indicates you should use **API Node**, **JSON Handler**, and **Condition Node** together for this pattern.",
            "",
            "Recommended setup",
            "- Use **API Node** to call the backend and store the response in a variable.",
            "- Use **JSON Handler** after the API Node to parse fields from the response into variables.",
            "- Use **Condition Node** to branch the journey based on the parsed value (e.g. success/error flag).",
            "",
            "Useful related",
            "- API Node: HTTP Status Code Branching if you also want to route by response code.",
        ])
    if ("flow trigger" in q or "launch a whatsapp flow" in q) and ("journey builder" in q or "whatsapp flow" in q):
```

---

## 9. `kb_answer.py` — BS_GOAL_NODE triggers in FEATURE_RULES

**Find (exact):**
```python
    {
        "id": "BS_GOAL_NODE",
        "triggers": [
            "goal node",
            "track milestones",
            "goal analytics toggle",
            "track purchase milestone",
        ],
        "preferred_sources": ["goal-node"],
        "penalty_sources": ["goal-analytics", "goals/"],
        "preferred_mode": "setup",
    },
]
```

**Replace with:**
```python
    {
        "id": "BS_GOAL_NODE",
        "triggers": [
            "goal node",
            "track milestones",
            "goal analytics toggle",
            "track purchase milestone",
            "conversion milestone",
            "milestone tracking",
            "count toward goal analytics",
            "goal achievement inside the flow",
        ],
        "preferred_sources": ["goal-node"],
        "penalty_sources": ["goal-analytics", "goals/"],
        "preferred_mode": "setup",
    },
]
```

---

## 10. `kb_answer.py` — _score_chunk goal-node boost

**Find (exact):**
```python
    if ("goal node" in q or "track milestones" in q or "track purchase milestone" in q) and "goal-node" in source:
        score += 5.0
```

**Replace with:**
```python
    if (
        any(term in q for term in [
            "goal node", "track milestones", "track purchase milestone",
            "conversion milestone", "milestone tracking", "count toward goal analytics",
            "goal achievement inside the flow", "mark a purchase or signup milestone",
        ])
        and "goal-node" in source
    ):
        score += 5.0
```

---

## 11. `kb_search.py` — UNSUPPORTED_PATTERNS

**Find (exact):**
```python
UNSUPPORTED_PATTERNS = [
    "two different callback urls",
    "two callback urls",
    "a b test",
    "ab test",
    "preview campaign analytics before",
    "sync across different browsers",
    "sync across browsers",
    "recycle bin",
    "pin reopened chats permanently",
    "dark mode",
    "download raw bot execution traces",
    "multi region webhook failover",
    "voice call escalation",
    "send campaign analytics automatically to s3",
]
```

**Replace with:**
```python
UNSUPPORTED_PATTERNS = [
    "two different callback urls",
    "two callback urls",
    "different callback urls",
    "callback urls for delivered and read",
    "a b test",
    "ab test",
    "preview campaign analytics before",
    "campaign analytics be previewed",
    "sync across different browsers",
    "sync across browsers",
    "sync retained anonymous chat history across devices",
    "sync automatically across browsers",
    "recycle bin",
    "restore deleted goal analytics exports",
    "schedule goal analytics exports",
    "two parallel backend requests",
    "one api node send two parallel",
    "per event webhook retry",
    "pin reopened chats permanently",
    "dark mode",
    "download raw bot execution traces",
    "multi region webhook failover",
    "voice call escalation",
    "send campaign analytics automatically to s3",
]
```

---

## 12. `kb_search.py` — BS_GOAL_NODE triggers in FEATURE_RULES

**Find (exact):**
```python
    {
        "id": "BS_GOAL_NODE",
        "triggers": ["goal node", "track milestones", "goal analytics toggle", "track purchase milestone"],
        "preferred_sources": ["goal-node"],
        "penalty_sources": ["goal-analytics", "goals/"],
        "preferred_mode": "setup",
    },
]
```

**Replace with:**
```python
    {
        "id": "BS_GOAL_NODE",
        "triggers": [
            "goal node", "track milestones", "goal analytics toggle", "track purchase milestone",
            "conversion milestone", "milestone tracking", "count toward goal analytics",
            "goal achievement inside the flow",
        ],
        "preferred_sources": ["goal-node"],
        "penalty_sources": ["goal-analytics", "goals/"],
        "preferred_mode": "setup",
    },
]
```

---

**End of skill patches.** Apply only these edits; do not change anything else and do not touch telemetry code.
