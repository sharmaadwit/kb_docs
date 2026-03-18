# Regression Hotfix — Scoring Logic + Alias Expansion + Version Stamp (kb_answer.py + kb_search.py)

**Files:** `kb_answer.py` and `kb_search.py`  
**Risk:** Low — fixes a scoring bug, expands aliases, hardens patterns, stamps logic version  
**Depends on:** All 9 patches + all previous hotfixes applied  

> **IMPORTANT — DO NOT touch telemetry code structure.** All Langfuse integration, tracing, span logging, and telemetry-related functions/imports must remain exactly as they are. The only telemetry-adjacent change in this hotfix is setting the `logic_version` metadata value (A4, B7) so traces can be filtered by runtime version.

---

## Part A — kb_answer.py (4 changes)

### A1 — Remove "dashboard" self-penalty from live_monitoring

The live_monitoring entry in `CONCEPT_REGISTRY` has a `source_penalties` entry for `"dashboard"` that accidentally matches the live-monitoring-dashboard source slug itself, canceling its own boost.

**Find** in `CONCEPT_REGISTRY` under the `"id": "live_monitoring"` entry:

```python
        "source_penalties": {"dashboard": -3.0, "agent-timesheet": -3.0},
```

**Replace with:**

```python
        "source_penalties": {"agent-timesheet": -3.0},
```

### A2 — Fix scoring: skip global penalty when entity boost matches

The current `_score_chunk` applies `GLOBAL_PENALTY_SOURCES` before entity boosts. This means a page like `live-monitoring-dashboard-...` gets penalized for containing `"dashboard"` even though an entity explicitly boosts it. The fix applies entity boosts first, then only applies the global penalty if NO entity boost matched.

**Find** in the `_score_chunk` function (the one that takes `entities` as a parameter):

```python
    if any(bad in source for bad in GLOBAL_PENALTY_SOURCES):
        score -= 3.0

    for entity in entities:
        for slug, boost in entity.get("source_boosts", {}).items():
            if slug in source:
                score += boost
        for slug, penalty in entity.get("source_penalties", {}).items():
            if slug in source:
                score += penalty

    return score
```

**Replace with:**

```python
    has_entity_boost = False
    for entity in entities:
        for slug, boost in entity.get("source_boosts", {}).items():
            if slug in source:
                score += boost
                has_entity_boost = True
        for slug, penalty in entity.get("source_penalties", {}).items():
            if slug in source:
                score += penalty

    if not has_entity_boost and any(bad in source for bad in GLOBAL_PENALTY_SOURCES):
        score -= 3.0

    return score
```

### A3 — Verify _compose_from_evidence page_lookup indentation

Open the `_compose_from_evidence` function. Locate this block:

```python
    if intent == "page_lookup" and evidence:
        c = evidence[0]
        page = _canonical_page_name(
            str(c.get("source") or ""),
            c.get("heading_path") or [],
            str(c.get("heading") or ""),
        )
        out = ["Exact page"]
        if page:
            out.append(f"- {page}")
        for line in lines[:2]:
            out.append(f"- {line}")
        return "\n".join(out)
```

Verify that `out = ["Exact page"]`, `if page:`, `for line in lines[:2]:`, `out.append(f"- {line}")`, and `return "\n".join(out)` are ALL indented inside the `if intent == "page_lookup"` block (8 spaces). If any of them are at 4-space indentation (outside the if), fix the indentation. This is a verification step only — if the indentation is already correct, make no changes.

### A4 — Stamp logic_version in metadata

The `logic_version` field in telemetry metadata is currently `None`. Set it to a meaningful version string so Langfuse traces can be filtered by runtime version.

**Find** in the `metadata` dict inside `kb_answer()` (near the bottom of the function):

```python
        "logic_version": None,
```

**Replace with:**

```python
        "logic_version": "kb-answer-v2.0-concept-registry",
```

---

## Part B — kb_search.py (7 changes)

### B1 — Expand live_monitoring aliases

**Find** in `CONCEPT_REGISTRY` under the `"id": "live_monitoring"` entry:

```python
        "id": "live_monitoring",
        "aliases": [
            "waiting for assignment", "ongoing chats", "no rule matched",
            "active busy offline", "first response time",
            "average first response time", "average response time",
            "average resolution time", "wait time related metrics",
            "monitor active agents", "live monitoring",
        ],
```

**Replace with:**

```python
        "id": "live_monitoring",
        "aliases": [
            "waiting for assignment", "ongoing chats", "no rule matched",
            "active busy offline", "first response time",
            "average first response time", "average response time",
            "average resolution time", "wait time related metrics",
            "monitor active agents", "live monitoring",
            "agent availability", "live agent",
            "live assignment queues", "agent state counts",
            "queue pressure", "piling up before assignment",
            "live monitoring dashboard", "wait time metrics",
            "agent state metrics", "real time monitoring",
        ],
```

### B2 — Remove "dashboard" self-penalty from live_monitoring

Same bug as kb_answer.py. **Find** in the same live_monitoring entry:

```python
        "source_penalties": {"dashboard": -3.0, "agent-timesheet": -3.0},
```

**Replace with:**

```python
        "source_penalties": {"agent-timesheet": -3.0},
```

### B3 — Expand test_your_bot aliases

**Find** in `CONCEPT_REGISTRY` under `"id": "test_your_bot"`:

```python
        "id": "test_your_bot",
        "aliases": [
            "test your bot", "message log", "backend json",
            "starting node inputs", "variables updated",
            "before going live", "wrong path after a user message",
        ],
```

**Replace with:**

```python
        "id": "test_your_bot",
        "aliases": [
            "test your bot", "test my bot", "message log", "backend json",
            "starting node inputs", "variables updated",
            "before going live", "wrong path after a user message",
            "test a journey", "test the journey", "payload debugging",
            "inspect payloads", "debugging before go live",
            "validate triggers", "debug in test your bot",
        ],
```

### B4 — Expand save_deploy aliases

**Find** in `CONCEPT_REGISTRY` under `"id": "save_deploy"`:

```python
        "id": "save_deploy",
        "aliases": [
            "save vs save & deploy", "save vs deploy",
            "save and deploy", "save & deploy",
            "live bot is still behaving like the old version",
        ],
```

**Replace with:**

```python
        "id": "save_deploy",
        "aliases": [
            "save vs save & deploy", "save vs deploy",
            "save and deploy", "save & deploy",
            "live bot is still behaving like the old version",
            "update the live bot", "deploy journey",
            "live rollout", "publish changes",
            "before release and then update",
        ],
```

### B5 — Harden SENSITIVE_PATTERNS

**Find** in `SENSITIVE_PATTERNS`:

```python
    "answer from memory",
]
```

**Replace with:**

```python
    "answer from memory", "hack into", "hack the", "exploit",
]
```

### B6 — Fix scoring: skip global penalty when entity boost matches

Same logic fix as kb_answer.py. **Find** in the `_score_chunk` function (the one that takes `entities` as a parameter):

```python
    if any(bad in source for bad in GLOBAL_PENALTY_SOURCES):
        score -= 4.0

    for entity in entities:
        for slug, boost in entity.get("source_boosts", {}).items():
            if slug in source:
                score += boost
        for slug, penalty in entity.get("source_penalties", {}).items():
            if slug in source:
                score += penalty
```

**Replace with:**

```python
    has_entity_boost = False
    for entity in entities:
        for slug, boost in entity.get("source_boosts", {}).items():
            if slug in source:
                score += boost
                has_entity_boost = True
        for slug, penalty in entity.get("source_penalties", {}).items():
            if slug in source:
                score += penalty

    if not has_entity_boost and any(bad in source for bad in GLOBAL_PENALTY_SOURCES):
        score -= 4.0
```

### B7 — Stamp logic_version in metadata

The `logic_version` field currently reads from `context.get_secret("KB_LOGIC_VERSION")` which returns `null` because the secret isn't configured. Replace with a hardcoded version string.

**Find** in the `metadata` dict inside `kb_search()`:

```python
            "logic_version": context.get_secret("KB_LOGIC_VERSION") if context else "search-telemetry-v1",
```

**Replace with:**

```python
            "logic_version": "kb-search-v2.0-concept-registry",
```

---

## Smoke Tests — Run after applying ALL changes

### kb_answer tests

| # | Query | Action | Expected |
|---|-------|--------|----------|
| A-S1 | `"What is live monitoring dashboard?"` | kb_answer | Answer mentions "Live Monitoring Dashboard" |
| A-S2 | `"Where do I configure business hours?"` | kb_answer | Answer mentions "Business Hours" |
| A-S3 | `"What does Goal Achieved mean in goal analytics?"` | kb_answer | Answer mentions "Goal Analytics" |
| A-N1 | `"How do I make pizza?"` | kb_answer | Refused (off-topic) |
| A-N2 | `"How do I hack into the admin panel?"` | kb_answer | Refused (sensitive) |

### kb_search tests

| # | Query | Action | Expected |
|---|-------|--------|----------|
| B-S1 | `"live monitoring dashboard"` | kb_search | Top source contains `live-monitoring-dashboard` |
| B-S2 | `"test my bot before going live"` | kb_search | Top source contains `test-your-bot` |
| B-S3 | `"update the live bot after save & deploy"` | kb_search | Top source contains `save-save-and-deploy` or `save-vs-save-deploy` |
| B-M1 | `"business hours vs auto replies"` | kb_search | Top 5 includes BOTH `business-hours` and `auto-replies` sources |
| B-M2 | `"campaign click metrics vs goal conversions"` | kb_search | Top 5 includes BOTH `campaign-analytics` and `goal-analytics` sources |
| B-N1 | `"Tell me a joke"` | kb_search | Empty results (guardrail) |
| B-N2 | `"How do I hack into the admin panel?"` | kb_search | Empty results (guardrail) |

---

**Report all smoke test results back. If all pass, the regression hotfix is complete.**
