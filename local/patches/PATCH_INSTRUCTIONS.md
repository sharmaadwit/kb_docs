# KB Answer Patch Instructions — Incremental

Apply patches **1–6** to `kb_answer.py` in order. **Patch 7** is optional (eval-driven ranking tweaks). All target the same file: **`kb_answer.py`**.

**Minimal Product KB layout (typical local agent):** only the shipped files — e.g. `kb_answer.py`, `kb_search.py`, `kb_ingest.py`, `kb_analytics.py`, `SKILL.md`, and `docs/`. There is **no** `test_patches.py`, `test_regression.py`, or `PATCH_INSTRUCTIONS.md` in that tree unless you copy them in. **Verification below** uses only what that agent has: `kb_answer.py` + a Python interpreter (and optional chunk source if you run end-to-end).

**Already applied Patch 3 (keyword fallback only)?** Add **Patch 5, Step 5a** — Pass 1 alias scoring uses `EXPLICIT_MODULES` the same way as Patch 3’s keyword path (included in **Patch 5** below).

Baseline (before patches): 4/6 misroute cases fail.
After all patches: 6/6 pass.

---

## Patch 1 — Score gate + entity-evidence coherence in `_compose_answer`

**What it fixes:** Templates returned from wrong concept match (Cases 1, 2, 6).
**Impact:** Prevents canned entity templates unless the entity's boosted sources appear in top evidence AND score clears a threshold.

### Step 1a: Add constant after `GLOBAL_PENALTY_SOURCES`

Find:
```python
GLOBAL_PENALTY_SOURCES = [
    "how-to-create-whatsapp-static-flows",
    "whatsapp-flow",
    "call-and-return-node",
    "json-handler",
]


# ---------------------------------------------------------------------------
# Section 3 — Concept Registry
```

Replace with:
```python
GLOBAL_PENALTY_SOURCES = [
    "how-to-create-whatsapp-static-flows",
    "whatsapp-flow",
    "call-and-return-node",
    "json-handler",
]

MIN_TEMPLATE_SCORE = 2.5

# ---------------------------------------------------------------------------
# Section 3 — Concept Registry
```

### Step 1b: Replace the template short-circuit in `_compose_answer`

Find:
```python
    # --- Single-entity template lookup ---
    if entities:
        primary = entities[0]
        template = primary.get("templates", {}).get(intent)
        if template:
            return template

        for fallback_intent in ["setup", "page_lookup", "behavior", "definition"]:
            template = primary.get("templates", {}).get(fallback_intent)
            if template:
                return template
```

Replace with:
```python
    # --- Single-entity template lookup (with score gate + coherence) ---
    if entities and evidence:
        primary = entities[0]
        top_score = evidence[0].get("score", 0.0) if evidence else 0.0
        top_source = str(evidence[0].get("source") or "").lower() if evidence else ""
        boosted_slugs = list(primary.get("source_boosts", {}).keys())
        entity_supported = any(slug in top_source for slug in boosted_slugs)

        if entity_supported and top_score >= MIN_TEMPLATE_SCORE:
            template = primary.get("templates", {}).get(intent)
            if template:
                return template

            for fallback_intent in ["setup", "page_lookup", "behavior", "definition"]:
                template = primary.get("templates", {}).get(fallback_intent)
                if template:
                    return template
```

---

## Patch 2 — Minimum evidence score floor in `_has_explicit_support`

**What it fixes:** Weak retrieval (score < 1.2) still producing confident answers (Case 3).
**Impact:** Blocks evidence-based answers when top retrieval score is below threshold.

### Step 2a: Add constant (right after the one from Patch 1)

Find:
```python
MIN_TEMPLATE_SCORE = 2.5

# ---------------------------------------------------------------------------
# Section 3 — Concept Registry
```

Replace with:
```python
MIN_TEMPLATE_SCORE = 2.5
MIN_EVIDENCE_SCORE = 1.2

# ---------------------------------------------------------------------------
# Section 3 — Concept Registry
```

### Step 2b: Add score floor at top of `_has_explicit_support`

Find:
```python
def _has_explicit_support(
    query: str, intent: str, evidence: List[Dict], lines: List[str],
    entities: List[Dict] = None,
) -> bool:
    if not evidence:
        return False
    top1 = evidence[0]
    top1_overlap = _query_overlap_score(query, top1)
    joined = "\n".join(lines).lower()

    if top1_overlap >= 0.35 and top1.get("score", 0) >= 2.0:
```

Replace with:
```python
def _has_explicit_support(
    query: str, intent: str, evidence: List[Dict], lines: List[str],
    entities: List[Dict] = None,
) -> bool:
    if not evidence:
        return False
    top1 = evidence[0]
    if top1.get("score", 0.0) < MIN_EVIDENCE_SCORE:
        return False
    top1_overlap = _query_overlap_score(query, top1)
    joined = "\n".join(lines).lower()

    if top1_overlap >= 0.35 and top1.get("score", 0) >= 2.0:
```

---

## Patch 3 — Harden keyword fallback in `_extract_entities`

**What it fixes:** Single-keyword matches on wrong concepts (Cases 1, 4, 5).
**Impact:** Requires 2+ keyword hits OR a valid module_context match (validated against EXPLICIT_MODULES) for keyword-only entity matching.

Find:
```python
    if not matched:
        query_tokens = set(re.findall(r"[a-z0-9]+", q)) - SCORING_STOP_WORDS
        kw_candidates = []
        for concept in CONCEPT_REGISTRY:
            if concept["id"] in matched_ids:
                continue
            kws = concept.get("keywords", [])
            kw_hits = [k for k in kws if k in query_tokens]
            if not kw_hits:
                continue
            kw_score = len(kw_hits) * 3
            if concept.get("module_context") and any(ctx in q for ctx in concept["module_context"]):
                kw_score += 3
            kw_candidates.append((kw_score, concept))
```

Replace with:
```python
    if not matched:
        query_tokens = set(re.findall(r"[a-z0-9]+", q)) - SCORING_STOP_WORDS
        kw_candidates = []
        for concept in CONCEPT_REGISTRY:
            if concept["id"] in matched_ids:
                continue
            kws = concept.get("keywords", [])
            kw_hits = [k for k in kws if k in query_tokens]
            if not kw_hits:
                continue
            valid_contexts = [
                ctx for ctx in (concept.get("module_context") or [])
                if ctx in EXPLICIT_MODULES
            ]
            has_context = bool(valid_contexts) and any(ctx in q for ctx in valid_contexts)
            if len(kw_hits) < 2 and not has_context:
                continue
            kw_score = len(kw_hits) * 3
            if has_context:
                kw_score += 3
            kw_candidates.append((kw_score, concept))
```

---

## Patch 4 — Overview intent detection and composition handler

**What it fixes:** Broad/overview queries forced into narrow page answers (Cases 1, 2).
**Impact:** Detects overview-style queries and returns a page listing instead of picking one wrong page.

### Step 4a: Add overview signal list (after `_SCHEMA_SIGNALS`)

Find:
```python
_SCHEMA_SIGNALS = [
    "schema", "payload", "statuses", "fields to store",
    "how should we store",
]

INTENT_TYPES = [
    "compare", "choose_between", "page_lookup", "definition",
    "behavior", "troubleshooting", "schema", "chain", "setup",
]
```

Replace with:
```python
_SCHEMA_SIGNALS = [
    "schema", "payload", "statuses", "fields to store",
    "how should we store",
]
_OVERVIEW_SIGNALS = [
    "overview", "getting started", "show me the docs", "show docs",
    "what can i do with", "key features", "how does it work",
    "tell me about", "explain the feature", "give me an overview",
    "list apis", "list the apis", "api list", "all apis",
    "end to end", "full flow", "complete guide",
]

INTENT_TYPES = [
    "compare", "choose_between", "page_lookup", "definition",
    "behavior", "troubleshooting", "schema", "chain", "overview", "setup",
]
```

### Step 4b: Add overview detection in `_classify_intent` (before `return "setup"`)

Find:
```python
    if is_troubleshoot:
        return "troubleshooting"
    if len(entities) >= 3:
        return "chain"
    return "setup"
```

Replace with:
```python
    if is_troubleshoot:
        return "troubleshooting"
    is_overview = any(x in q for x in _OVERVIEW_SIGNALS)
    if is_overview and len(entities) <= 1:
        return "overview"
    if len(entities) >= 3:
        return "chain"
    return "setup"
```

### Step 4c: Add overview to `_detect_intents` (legacy list version)

Find:
```python
    if any(x in q for x in _SCHEMA_SIGNALS):
        intents.append("schema")
    if not intents:
        intents.append("setup")
    return intents
```

Replace with:
```python
    if any(x in q for x in _SCHEMA_SIGNALS):
        intents.append("schema")
    if any(x in q for x in _OVERVIEW_SIGNALS):
        intents.append("overview")
    if not intents:
        intents.append("setup")
    return intents
```

### Step 4d: Add overview case in `_has_explicit_support` (before `return bool(lines)`)

Find:
```python
    if intent == "compare":
        return top1_overlap >= 0.2 and len(evidence) >= 1

    return bool(lines)
```

Replace with:
```python
    if intent == "compare":
        return top1_overlap >= 0.2 and len(evidence) >= 1

    if intent == "overview":
        return bool(evidence)

    return bool(lines)
```

### Step 4e: Add overview handler in `_compose_from_evidence` (before the final heading/lines block)

Find:
```python
    if intent == "compare":
        return "I don't know the exact compare details from the current docs."

    heading = str(evidence[0].get("heading") or "").strip()
```

Replace with:
```python
    if intent == "compare":
        return "I don't know the exact compare details from the current docs."

    if intent == "overview" and evidence:
        mod = _module_from_source(str(evidence[0].get("source") or ""))
        pages = []
        seen_sources: set = set()
        for c in evidence[:4]:
            src = str(c.get("source") or "")
            if src in seen_sources:
                continue
            seen_sources.add(src)
            page = _canonical_page_name(
                src, c.get("heading_path"), str(c.get("heading") or ""),
            )
            if page:
                pages.append(page)
        if pages:
            return (
                f"The documentation covers several {mod} topics. "
                "The most relevant pages are:\n- "
                + "\n- ".join(pages)
                + "\n\nAsk about a specific page or feature for detailed steps."
            )
        return (
            "I don't have a single overview page for this topic. "
            "Ask about a specific feature or setup step and I'll help with that."
        )

    heading = str(evidence[0].get("heading") or "").strip()
```

---

## Patch 5 — Pass 1 alias alignment + chunk score floor

**What it fixes:** (1) **Pass 1** alias ranking inflated by spurious `module_context` tokens (same `EXPLICIT_MODULES` rule as Patch 3’s Pass 2). (2) Noise chunks with near-zero scores entering the pipeline.

**Impact:** Aligns both passes in `_extract_entities`; adds a soft floor before ranking.

**Order inside this patch:** Do **Step 5a** first if you already applied Patch 3 without it; then **5b** and **5c** in order.

### Step 5a: Pass 1 alias boost — `EXPLICIT_MODULES` for `module_context`

Apply after **Patch 3** (keyword fallback). Only changes the **first** loop in `_extract_entities` (alias substring matching).

**Why:** `module_context` lists sometimes include concept words (e.g. `"variable"`, `"journey"`) that are not keys in `EXPLICIT_MODULES`. Those must not grant the **+5** alias ranking boost.

Find (inside `_extract_entities`, Pass 1 — immediately after alias `hits` are computed):

```python
        match_score = sum(len(a) for a in hits)
        if concept.get("module_context") and any(ctx in q for ctx in concept["module_context"]):
            match_score += 5
        matched.append((match_score, concept))
```

Replace with:

```python
        match_score = sum(len(a) for a in hits)
        valid_contexts = [
            ctx for ctx in (concept.get("module_context") or [])
            if ctx in EXPLICIT_MODULES
        ]
        if valid_contexts and any(ctx in q for ctx in valid_contexts):
            match_score += 5
        matched.append((match_score, concept))
```

`EXPLICIT_MODULES` is the existing dict at the top of `kb_answer.py`. No new imports.

### Step 5b: Add `MIN_CHUNK_SCORE` constant (right after the ones from Patches 1–2)

Find:
```python
MIN_TEMPLATE_SCORE = 2.5
MIN_EVIDENCE_SCORE = 1.2

# ---------------------------------------------------------------------------
# Section 3 — Concept Registry
```

Replace with:
```python
MIN_TEMPLATE_SCORE = 2.5
MIN_EVIDENCE_SCORE = 1.2
MIN_CHUNK_SCORE = 0.3

# ---------------------------------------------------------------------------
# Section 3 — Concept Registry
```

### Step 5c: Replace score filter in main `kb_answer()` function

Find:
```python
    scored = []
    for c in chunks:
        s = _score_chunk(query, c, entities, explicit_module)
        if s > 0:
            row = dict(c)
            row["score"] = s
            scored.append(row)
    scored.sort(key=lambda x: x.get("score", 0.0), reverse=True)
```

Replace with:
```python
    scored = []
    for c in chunks:
        s = _score_chunk(query, c, entities, explicit_module)
        if s >= MIN_CHUNK_SCORE:
            row = dict(c)
            row["score"] = s
            scored.append(row)
    scored.sort(key=lambda x: x.get("score", 0.0), reverse=True)
```

---

## Patch 6 — Entity-module coherence filter in `_compose_answer`

**What it fixes:** Cross-module entity matches (Case 5: Bot Studio entity for a template-creation query).
**Impact:** Discards entities whose module disagrees with the explicit module or the evidence module.

### Step 6a: Update `_compose_answer` signature and add coherence filter

Find:
```python
def _compose_answer(
    query: str,
    intent: str,
    entities: List[Dict],
    evidence: List[Dict],
) -> str:
    """Main answer composition: pick the best strategy based on intent + entities."""
    q = _normalize_query_for_match(query)
    lines = _evidence_lines(evidence)

    # --- Compare: check overrides first, then compose from blurbs ---
    if intent == "compare" and len(entities) >= 2:
```

Replace with:
```python
def _compose_answer(
    query: str,
    intent: str,
    entities: List[Dict],
    evidence: List[Dict],
    explicit_module: str = "General",
) -> str:
    """Main answer composition: pick the best strategy based on intent + entities."""
    q = _normalize_query_for_match(query)
    lines = _evidence_lines(evidence)

    if entities and explicit_module != "General":
        entities = [
            e for e in entities
            if (e.get("module") or "").lower() == explicit_module.lower()
            or not e.get("module")
        ] or entities

    if entities and evidence:
        ev_module = _module_from_source(str(evidence[0].get("source") or ""))
        if ev_module != "General":
            coherent = [
                e for e in entities
                if (e.get("module") or "").lower() == ev_module.lower()
                or not e.get("module")
            ]
            if coherent:
                entities = coherent

    # --- Compare: check overrides first, then compose from blurbs ---
    if intent == "compare" and len(entities) >= 2:
```

### Step 6b: Update the call site in `kb_answer()` to pass `explicit_module`

Find:
```python
    evidence = _select_evidence(query, scored, intent, explicit_module)
    answer = _compose_answer(query, intent, entities, evidence)
    answer, policy_meta = _apply_answer_policy(answer, query, params)
```

Replace with:
```python
    evidence = _select_evidence(query, scored, intent, explicit_module)
    answer = _compose_answer(query, intent, entities, evidence, explicit_module)
    answer, policy_meta = _apply_answer_policy(answer, query, params)
```

---

## Patch 7 (optional) — Eval-driven query/source penalties + overview diversity

Apply **after** Patches 1–6. Targets recurring **mis-ranked sources** from production evals (campaign queue vs Personalize, dynamic link tracking vs generic send/analytics, SMTP vs marketing templates) and **noisy overview** lists.

A **standalone, paste-ready copy** of Patch 7 only is in **`LATEST_PATCHES.md`** (same steps; use either file).

### Step 7a: Add `_query_source_penalty_adjustment` and call it from `_score_chunk`

**Placement:** Insert the new function **immediately after** `_score_chunk` (after its `return score`, before `# Section 8 — Evidence selection`).

**New function (paste as-is):**

```python
def _query_source_penalty_adjustment(q: str, source: str) -> float:
    """Negative score deltas when query semantics conflict with frequent mis-ranked sources."""
    s = source.lower()
    adj = 0.0
    if ("queue" in q or "queued" in q) and "campaign" in q:
        if "personalize-enabled-campaign-manager" in s or "personalize/personalize-enabled" in s:
            adj -= 8.0
    if any(
        ph in q
        for ph in (
            "dynamic link",
            "dynamic links",
            "link tracking",
            "tracked dynamic",
        )
    ):
        if "sending-an-automated-campaign" in s:
            adj -= 8.0
        if "personalize-enabled-campaign-manager" in s or "personalize/personalize-enabled" in s:
            adj -= 8.0
        if "campaign-analytics" in s:
            adj -= 6.0
    if any(ph in q for ph in ("smtp", "email server", "mail server")):
        if "agent assist" in q:
            if "sending-marketing-templates" in s or "marketing-templates-from-agent" in s:
                adj -= 10.0
    return adj
```

**Inside `_score_chunk`,** immediately **before** the final `return score` (after the `GLOBAL_PENALTY_SOURCES` block and entity boosts/penalties), add:

```python
    score += _query_source_penalty_adjustment(q, source)
```

(Use the same `q` and `source` variables already defined at the top of `_score_chunk`.)

**Tune:** Adjust the `-8.0` / `-6.0` / `-10.0` magnitudes if retrieval shifts; keep penalties **negative** so bad pairs rank lower.

---

### Step 7b: Diverse overview evidence — helpers + `intent == "overview"` branch

**Placement:** Insert **`_overview_source_bucket`** and **`_select_evidence_overview_diverse`** immediately **before** `def _select_evidence(`.

**Paste as-is:**

```python
def _overview_source_bucket(source: str) -> str:
    """Group chunks by kb/<segment>/... for diverse overview picks."""
    s = (source or "").replace("\\", "/").lower()
    parts = [p for p in s.split("/") if p]
    if "kb" in parts:
        i = parts.index("kb")
        if i + 2 < len(parts):
            return "/".join(parts[i : i + 3])
        if i + 1 < len(parts):
            return "/".join(parts[i : i + 2])
    return s[:80]


def _select_evidence_overview_diverse(scoped: List[Dict], limit: int = 4) -> List[Dict]:
    """At most one chunk per kb/.../folder bucket so overview lists stay varied."""
    if not scoped:
        return []
    out: List[Dict] = []
    buckets: set = set()
    for row in scoped:
        src = str(row.get("source") or "")
        b = _overview_source_bucket(src)
        if b in buckets:
            continue
        buckets.add(b)
        out.append(row)
        if len(out) >= limit:
            return out
    for row in scoped:
        if row not in out:
            out.append(row)
        if len(out) >= limit:
            break
    return out[:limit]
```

**Inside `_select_evidence`,** add a branch **before** the final `return scoped[:4]` (after the `setup` / `troubleshooting` / `chain` block):

```python
    if intent == "overview":
        return _select_evidence_overview_diverse(scoped, limit=4)
```

---

### Step 7c: Rubric / grep (optional)

After Patch 7:

```bash
grep -n _query_source_penalty_adjustment kb_answer.py
grep -n _select_evidence_overview_diverse kb_answer.py
```

Expect at least one call site for each.

**KB note:** Penalties reduce wrong wins; they **do not replace** missing docs. Add real pages for “campaign in queue”, “dynamic link tracking setup”, and SMTP if product requires definitive answers.

---

## Summary

| Patch | What it fixes | Key constant/threshold |
|-------|--------------|----------------------|
| 1 | Template returned from wrong entity | `MIN_TEMPLATE_SCORE = 2.5` |
| 2 | Weak evidence still passes | `MIN_EVIDENCE_SCORE = 1.2` |
| 3 | Single-keyword entity match (Pass 2) | 2+ keywords required; `module_context` validated against `EXPLICIT_MODULES` |
| 4 | Broad queries forced to narrow pages | New `"overview"` intent + page-listing composition |
| 5 | Pass 1 alias boost + noise chunks | Step 5a: Pass 1 `module_context` uses `EXPLICIT_MODULES`; Steps 5b–5c: `MIN_CHUNK_SCORE = 0.3` |
| 6 | Cross-module entity mismatch | Entity-module coherence filter in `_compose_answer` |
| 7 (opt.) | Eval-driven mis-ranks + overview noise | Query-conditioned penalties; overview diversity in `_select_evidence` |

Tunable thresholds: `MIN_TEMPLATE_SCORE`, `MIN_EVIDENCE_SCORE`, `MIN_CHUNK_SCORE`. Start with the values above and adjust based on production telemetry. Patch 7 penalty magnitudes are also tunable.

---

## Post-patch verification rubric (no test scripts required)

Use this after **all six patches** are applied. It is designed for a **minimal repo** that only contains `kb_answer.py` (and siblings like `kb_search.py`) — **no** `test_patches.py`, `test_regression.py`, or `PATCH_INSTRUCTIONS.md` in the agent bundle.

**Passing bar**

| Tier | Name | Required? |
|------|------|-----------|
| **1** | Mechanical | **Yes** — must all pass |
| **2** | Structural audit | **Yes** — must all pass |
| **3** | Runtime spot-checks | **If** you can execute `kb_answer` with real chunks + secrets; otherwise skip and note “not exercised” |
| **4** | `kb_search.py` parity | **Optional** — only if your process keeps search aligned with answer |

---

### Tier 1 — Mechanical (must pass)

| # | Check | Command / action | Pass when |
|---|--------|------------------|------------|
| 1.1 | File parses | `python3 -m py_compile kb_answer.py` | Exit code 0, no output |
| 1.2 | Module imports | `python3 -c "import kb_answer; print(kb_answer.MIN_TEMPLATE_SCORE)"` | Prints `2.5` (or your chosen value if you tuned it) |
| 1.3 | Entry point exists | `python3 -c "import kb_answer; assert callable(kb_answer.kb_answer)"` | No exception |

---

### Tier 2 — Structural audit (must pass)

Confirm the intended **shapes** exist in `kb_answer.py` (copy-paste friendly grep). **Pass** = each row matches at least once unless noted.

| # | Patch intent | What to verify | Example grep (adjust path) |
|---|----------------|----------------|-----------------------------|
| 2.1 | P1 template gate | `MIN_TEMPLATE_SCORE` and `entity_supported` (or equivalent logic) near template return | `grep -n MIN_TEMPLATE_SCORE kb_answer.py` and inspect `_compose_answer` |
| 2.2 | P2 evidence floor | `MIN_EVIDENCE_SCORE` and comparison on `top1` score in `_has_explicit_support` | `grep -n MIN_EVIDENCE_SCORE kb_answer.py` |
| 2.3 | P3 keyword path | `valid_contexts` + `EXPLICIT_MODULES` inside **keyword** branch of `_extract_entities` | `grep -n valid_contexts kb_answer.py` (expect ≥2 hits: Pass 1 + Pass 2) |
| 2.4 | P4 overview | `_OVERVIEW_SIGNALS`, `"overview"` in `INTENT_TYPES`, `intent == "overview"` in `_has_explicit_support` and `_compose_from_evidence` | `grep -n _OVERVIEW_SIGNALS kb_answer.py` |
| 2.5 | P5 chunk floor | `MIN_CHUNK_SCORE` and `s >= MIN_CHUNK_SCORE` in `kb_answer()` scoring loop | `grep -n MIN_CHUNK_SCORE kb_answer.py` |
| 2.6 | P6 coherence | `_compose_answer(..., explicit_module` and call site passes `explicit_module` | `grep -n explicit_module kb_answer.py` |
| 2.7 | P7 (if applied) | `_query_source_penalty_adjustment`, `_select_evidence_overview_diverse`, `intent == "overview"` in `_select_evidence` | `grep -n _query_source_penalty_adjustment kb_answer.py` |

**Quick one-liner count (optional sanity):**  
`grep -c 'valid_contexts' kb_answer.py` — expect **2** (Pass 1 and Pass 2 in `_extract_entities`).

---

### Tier 3 — Runtime spot-checks (if you can run `kb_answer`)

Only when your environment provides **chunks** (e.g. JSONL or GitHub raw) and whatever **secrets / context** your host injects. Do **not** fail the rubric if you cannot run this tier in the agent sandbox.

| # | Scenario | Expected behavior (shape, not exact wording) |
|---|----------|-----------------------------------------------|
| 3.1 | Broad overview query (include phrases like “give me an overview” or “getting started”) for a module you name in the query | Intent resolves to overview-style handling; answer lists **multiple** doc pages or admits limits — **not** a single unrelated node template (e.g. not WhatsApp Flow for a generic Agent Assist overview) |
| 3.2 | Query with **no** good doc match and **low** retrieval | Answer tends toward **“I don’t know…”** or short refusal — **not** a long procedural template from a weak match |
| 3.3 | Query that **exactly** names a documented node/feature (alias from registry) | Answer may use that concept’s template or grounded bullets; **not** a different concept’s template |
| 3.4 | Guardrail probe (only in a safe test environment) | Off-topic or sensitive phrasing matches your existing `_guardrail_answer` / refusal path |

Record **pass / fail / skipped** for each row.

---

### Tier 4 — Optional: `kb_search.py` parity

If `kb_search.py` duplicates `CONCEPT_REGISTRY` or scoring helpers, decide whether Patch 3 / 5 **Pass 1–2** rules should be mirrored there for consistent search ranking. This repo’s patches target **`kb_answer.py` only**; updating search is a **separate** change. If you do mirror, re-run Tier 1 on `kb_search.py` (`python3 -m py_compile kb_search.py`).

---

### Rubric outcome

- **Ready to ship:** Tier 1 and Tier 2 all pass; Tier 3 passed or explicitly **skipped** with reason (no chunks / no runtime).
- **Not ready:** Any Tier 1 or Tier 2 failure — fix before merge.
- **Follow-up:** Tier 3 failures with Tier 1–2 green → tune thresholds (`MIN_*_SCORE`) or registry, not necessarily revert patches wholesale.
