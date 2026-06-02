# Patch 10 — `kb_answer.py` (eval batch: Agent Assist exploration, APIs, SR panels, campaign flow)

Apply after Patches **1–9**. **Target file:** `kb_answer.py` only.

## What it fixes

| Failure mode | Mechanism |
|--------------|-----------|
| A2 / getting-started → Assignment Rules | **`_is_broad_overview_query`**: treat “how do I use + Agent Assist”, “common usage”, “practical + getting started”, and high-level **campaign flow** phrasing as **overview** (same path as Patch 8: skip narrow entity templates). |
| A3 / C3 / APIs → Assignment Rules | **`_query_source_penalty_adjustment`**: **−12** when query has **Agent Assist** + **api/apis/endpoint** and source is **assignment-rules**. (Do **not** add `list`+`apis` to broad overview — it surfaces unrelated pages like “Sending Marketing Templates” in overview lists.) |
| A4 / SR panels → Agentic LLM | **`_query_topic_not_in_evidence`**: if query mentions **sr panel(s)**, evidence must include **“sr panel”**; **penalties** on **ace-and-agentic-llm** / **ai-agents-developer** sources when **sr panel** in query. |
| C4 / campaign flow → Campaign Analytics blurb | Broad overview for **“creating and publishing” + campaign**, **high level + campaign**, **campaign + publish + flow**; **−10** on **campaign-analytics** for **high level** / **creating and publishing** + **campaign**. |

## Verify

```bash
python3 -m py_compile kb_answer.py
python3 test_patches.py && python3 test_regression.py
```

Reference implementation: current repo **`kb_answer.py`**.

---

## Patch 10b — Agent Assist API list / “documented for APIs” → IDK unless evidence mentions API surface

**Symptom:** A3/C3 still returned generic `**Setup path**` / “Details” from weak chunks.

**Add:**

- **`_is_agent_assist_api_inventory_query(q)`** — `agent assist` + `api`/`endpoint` + inventory phrasing (`list`, `documented`, `public`, `not listed`, `say if`, `what s documented`, …).
- **`_evidence_mentions_agent_assist_api_surface(joined)`** — evidence must mention terms like `endpoint`, `rest api`, `api reference`, `swagger`, etc.
- **`_compose_answer`:** after overview, if `_is_agent_assist_api_inventory_query(q)`, **`return _compose_from_evidence(...)`** (skip entity templates).
- **`_blocks_loose_explicit_support`** and **`_has_explicit_support` (setup):** if API inventory query and evidence lacks API-surface terms → **no explicit support** → standard **IDK** string.

This keeps **`test_patches` case 2** as **IDK** when webhooks chunks lack real API reference language.

---

## Patch 10c — API inventory vs overlap shortcut (order-of-operations bug)

**Symptom:** A3/C3 still returned `**Setup path**` / “Details” with high-scoring chunks.

**Cause:** `_has_explicit_support` applied **`top1_overlap >= 0.35` and score ≥ 2.0** *before* intent-specific rules. That short-circuited to **True**, so API-inventory checks in the **setup** branch never ran. Also, substring **`endpoint`** matched **`endpoints`** in generic UI copy.

**Fix:**

1. Evaluate **`_is_agent_assist_api_inventory_query`** at the **top** of `_has_explicit_support` (right after building `joined`) and return **`_evidence_mentions_agent_assist_api_surface(joined)`** only — **before** the overlap shortcut.
2. Tighten **`_evidence_mentions_agent_assist_api_surface`**: drop bare **`endpoint`**; require phrases like **`rest api`**, **`api reference`**, **`api endpoint`**, **`openapi`**, etc.
3. Remove the duplicate API-inventory block from **`_blocks_loose_explicit_support`** (handled at top).
4. Remove duplicate API check from the **setup** branch (handled at top).

---

## Patch 10d — `_compose_from_evidence` hard gate (full chunk text)

**Symptom:** A3/C3 still showed **Setup path / Details** after 10c in some runtimes.

**Cause:** Any remaining mismatch in `_has_explicit_support` order, or **only** line-deduped text missing tokens that exist elsewhere in the chunk body.

**Fix:**

1. At the **very start** of **`_compose_from_evidence`** (after empty check), if **`_is_agent_assist_api_inventory_query(qn)`**: build **`full_text`** from **`"\n".join(c.get("text") for c in evidence)`** and if **`not _evidence_mentions_agent_assist_api_surface(full_text)`** → return **IDK** immediately — **before** calling **`_has_explicit_support`**.

2. Broaden **`_is_agent_assist_api_inventory_query`** with fallbacks: **`for apis`**, **`apis in`**, **`list`+`apis`**, **`apis`+`gupshup`**, so short phrasings still classify.

This path is **independent** of scoring shortcuts inside **`_has_explicit_support`**.

---

## Patch 10e — Eval follow-up (A7 JSON/postback, E2 nonsense module, A2/C1 onboarding list)

| Case | Change |
|------|--------|
| **A7** | **`_query_source_penalty_adjustment`**: penalize **JB Legacy vs V2 vs Pro** (`legacy-vs-v2-vs-pro`) and **Journey Builder platform upgrade** docs when the query mentions **postback** + **JSON/handler** — those are platform overview chunks, not procedural JSON Handler guidance. **`postback`** added to **`json_handler`** aliases. |
| **E2** | **`_COMMON_LONG_PRODUCT_WORDS`** + **`_long_distinctive_terms_missing_from_evidence`**: any query token **≥11 letters** that is not in the common list must appear in evidence **`joined`** text, else setup answers fail explicit support (**IDK**). Catches nonsense product names like **frobnicator**. |
| **A2 / C1** | **`_overview_onboarding_boost_agent_assist`** + sort in **`_compose_from_evidence`** (overview only): for onboarding-style Agent Assist queries, list **About Agent Assist** first **in the bullet list only** — do **not** reorder **`evidence`** (would put a low-scoring chunk first and break **`MIN_EVIDENCE_SCORE`**). |
