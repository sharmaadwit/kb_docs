# Patch 6 Hotfix M5 — Fix sticky_assignment vs assignment_rules compare

**File:** `kb_answer.py`
**Depends on:** Patch 6 + previous hotfix already applied
**Risk:** Low — adds one data entry, tightens one fallback condition.

> **IMPORTANT — DO NOT touch telemetry code.**

---

## Fix 1 — Add COMPARE_OVERRIDES entry for sticky_assignment + assignment_rules

In `COMPARE_OVERRIDES`, find the entry for `("assignment_rules", "agent_transfer")`. Immediately after that entry's closing `),`, add a new entry:

**Find:**
```python
    ("assignment_rules", "agent_transfer"): (
        "Check these two modules together\n"
        "- `Agent Assist -> Settings -> Chat Management -> Assignment Rules` for tag-based or team-based routing conditions.\n"
        "- `Bot Studio -> Journey Builder -> Agent Transfer Node` for the documented bot-to-agent handover step."
    ),
```

**Replace with:**
```python
    ("assignment_rules", "agent_transfer"): (
        "Check these two modules together\n"
        "- `Agent Assist -> Settings -> Chat Management -> Assignment Rules` for tag-based or team-based routing conditions.\n"
        "- `Bot Studio -> Journey Builder -> Agent Transfer Node` for the documented bot-to-agent handover step."
    ),
    ("sticky_assignment", "assignment_rules"): (
        "Use Sticky Assignment when\n"
        "- You need reopened chats to return to the same agent who previously handled them.\n"
        "Use Assignment Rules when\n"
        "- You need tag-based or team-based chat routing conditions.\n"
        "Both are configured under `Agent Assist -> Settings -> Chat Management -> Assignment Rules`."
    ),
```

## Fix 2 — Tighten the partial-match fallback in _compose_compare

In the `_compose_compare` function, find the second `COMPARE_OVERRIDES` loop (it comes after the first exact-match loop). It currently looks like:

```python
    for key, answer in COMPARE_OVERRIDES.items():
        if any(eid in key for eid in entity_ids):
            return answer
```

**Replace with:**
```python
    for key, answer in COMPARE_OVERRIDES.items():
        overlap = sum(1 for eid in entity_ids if eid in key)
        if overlap >= 2:
            return answer
```

This prevents a single overlapping entity from grabbing the wrong override (which was causing M5 to return the agent_transfer answer instead of sticky_assignment).

## Smoke test

| # | Query | Expected |
|---|-------|----------|
| M5 | `"Where do I configure sticky assignment vs assignment rules?"` | "Use Sticky Assignment when... Use Assignment Rules when... Both are configured under Assignment Rules." |
| M1 | `"Should I check business hours or auto replies for away messages?"` | Still works: mentions both Business Hours and Auto Replies |
| M3 | `"Which page shows campaign click metrics vs goal conversions?"` | Still works: mentions both Campaign Analytics and Goal Analytics |

---
**After M5 passes, continue with Patch 7 (dead code cleanup).**
