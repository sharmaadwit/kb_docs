# Agent Assist Hotfix — Expand call_return + agent_transfer aliases (kb_answer.py + kb_search.py)

**Files:** `kb_answer.py` and `kb_search.py`  
**Risk:** Zero — alias expansion only, no logic changes  
**Impact:** `call_return_node` 52% → 100% answer, 80% → 100% search. `agent_transfer_node` 64% → 100% answer, 20% → 100% search.

> **IMPORTANT — DO NOT touch telemetry code.** All Langfuse integration, tracing, span logging, and telemetry-related functions/imports must remain exactly as they are.

---

## Fix 1 — Expand call_return aliases in kb_answer.py

**Find** in `CONCEPT_REGISTRY` under `"id": "call_return"`:

```python
        "id": "call_return",
        "aliases": [
            "call and return node", "call return node",
            "call another journey",
            "return back to the same journey", "sub journey",
        ],
```

**Replace with:**

```python
        "id": "call_return",
        "aliases": [
            "call and return node", "call return node",
            "call another journey",
            "return back to the same journey", "sub journey",
            "parent journey invoke another journey",
            "child journey execution", "child journey",
            "resume the original flow", "return to the parent",
            "invoke another journey and then resume",
            "hand control to another journey",
            "reuse a sub journey", "temporarily hand control",
            "parent journey", "invoke sub journey",
        ],
```

## Fix 2 — Expand agent_transfer aliases in kb_answer.py

**Find** in `CONCEPT_REGISTRY` under `"id": "agent_transfer"`:

```python
        "id": "agent_transfer",
        "aliases": [
            "agent transfer node", "connect with a human agent",
            "handover to agent", "transfer to human agent",
            "not be transferred to an agent",
            "customer might not be transferred to an agent",
            "same conversation continues", "conversation reopening",
            "reopened chat", "bot to agent transfer flow",
            "live agent", "same thread", "resume later",
            "no agent picks up", "handoff fail",
            "agent transfer does not happen",
            "earlier flow or agent",
        ],
```

**Replace with:**

```python
        "id": "agent_transfer",
        "aliases": [
            "agent transfer node", "connect with a human agent",
            "handover to agent", "transfer to human agent",
            "not be transferred to an agent",
            "customer might not be transferred to an agent",
            "same conversation continues", "conversation reopening",
            "reopened chat", "bot to agent transfer flow",
            "live agent", "same thread", "resume later",
            "no agent picks up", "handoff fail",
            "agent transfer does not happen",
            "earlier flow or agent",
            "human handoff", "bot to agent",
            "bot should stop and a human should take over",
            "move a conversation from bot flow to a live human",
            "hand over from journey builder to a support agent",
            "bot to agent escalation", "escalation to agent",
            "human agent take over", "human take over",
            "bot flow to a live human agent",
        ],
```

## Fix 3 — Expand call_return aliases in kb_search.py

**Find** in `CONCEPT_REGISTRY` under `"id": "call_return"`:

```python
        "id": "call_return",
        "aliases": [
            "call and return node", "call return node",
            "call another journey", "return back to the same journey",
            "sub journey",
        ],
```

**Replace with:**

```python
        "id": "call_return",
        "aliases": [
            "call and return node", "call return node",
            "call another journey", "return back to the same journey",
            "sub journey",
            "parent journey invoke another journey",
            "child journey execution", "child journey",
            "resume the original flow", "return to the parent",
            "invoke another journey and then resume",
            "hand control to another journey",
            "reuse a sub journey", "temporarily hand control",
            "parent journey", "invoke sub journey",
        ],
```

## Fix 4 — Expand agent_transfer aliases in kb_search.py

**Find** in `CONCEPT_REGISTRY` under `"id": "agent_transfer"`:

```python
        "id": "agent_transfer",
        "aliases": [
            "agent transfer node", "connect with a human agent",
            "handover to agent", "transfer to human agent",
            "not be transferred to an agent",
            "customer might not be transferred to an agent",
            "same conversation continues", "conversation reopening",
            "reopened chat", "bot to agent transfer flow",
            "live agent", "same thread", "resume later",
            "no agent picks up", "handoff fail",
        ],
```

**Replace with:**

```python
        "id": "agent_transfer",
        "aliases": [
            "agent transfer node", "connect with a human agent",
            "handover to agent", "transfer to human agent",
            "not be transferred to an agent",
            "customer might not be transferred to an agent",
            "same conversation continues", "conversation reopening",
            "reopened chat", "bot to agent transfer flow",
            "live agent", "same thread", "resume later",
            "no agent picks up", "handoff fail",
            "human handoff", "bot to agent",
            "bot should stop and a human should take over",
            "move a conversation from bot flow to a live human",
            "hand over from journey builder to a support agent",
            "bot to agent escalation", "escalation to agent",
            "human agent take over", "human take over",
            "bot flow to a live human agent",
        ],
```

---

## Smoke Tests

| # | Query | Action | Expected |
|---|-------|--------|----------|
| S1 | `"Which node lets a parent journey invoke another journey and then resume the original flow?"` | kb_answer | Answer mentions "Call & Return Node" |
| S2 | `"What Bot Studio node is used for human handoff during a journey?"` | kb_answer | Answer mentions "Agent Transfer Node" |
| S3 | `"How do I hand over from Journey Builder to a support agent?"` | kb_answer | Answer mentions "Agent Transfer Node" |
| S4 | `"Which node supports child-journey execution with return to the parent path?"` | kb_search | Top source contains `call-and-return` |
| S5 | `"If the bot should stop and a human should take over, which node should I configure?"` | kb_search | Top source contains `agent-transfer-node` |

**Report all smoke test results back.**
