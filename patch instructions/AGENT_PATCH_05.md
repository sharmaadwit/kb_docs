# Patch 5 of 9 — Add new scoring, evidence, and composition functions (ADDITIVE ONLY)

**File:** `kb_answer.py`
**Depends on:** Patch 4
**Risk:** Zero — adds new functions only. Old code is untouched and still runs.
**What it does:** Adds `_score_chunk_v2`, evidence selection helpers, and answer composition functions alongside the existing code. Nothing is replaced or deleted.

> **IMPORTANT — DO NOT touch telemetry code.** All Langfuse integration, tracing, span logging, and telemetry-related functions/imports must remain exactly as they are. This patch does not modify telemetry and neither should you.

## Step 1 — Add _score_chunk_v2

This is the new data-driven scoring function. It is named `_v2` so the existing `_score_chunk` keeps working unchanged. Find the end of the existing `_score_chunk` function. After it, add:

```python


def _score_chunk_v2(
    query: str, chunk: Dict, entities: List[Dict], explicit_module: str,
) -> float:
    q = _normalize_query_for_match(query)
    source = str(chunk.get("source") or chunk.get("path") or "").lower()
    heading = str(chunk.get("heading") or "").lower()
    text = str(chunk.get("text") or "").lower()
    score = 0.0

    for token in re.findall(r"[a-z0-9&+-]+", q):
        if len(token) < 3:
            continue
        if token in heading:
            score += 0.25
        if token in source:
            score += 0.25
        if token in text:
            score += 0.05

    if explicit_module != "General" and explicit_module.lower() in _module_from_source(source).lower():
        score += 0.35

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

## Step 2 — Add evidence selection helpers

After `_score_chunk_v2`, add:

```python


# ---------------------------------------------------------------------------
# Section 8 — Evidence selection
# ---------------------------------------------------------------------------

def _clean_line(line: str) -> str:
    line = re.sub(r"^[#\-\*\s]+", "", line or "").strip()
    line = re.sub(r"\*\*", "", line)
    return line


def _query_overlap_score(query: str, chunk: Dict) -> float:
    q = _normalize_query_for_match(query)
    hay = " ".join([
        str(chunk.get("heading") or "").lower(),
        str(chunk.get("source") or chunk.get("path") or "").lower(),
        str(chunk.get("text") or "").lower(),
    ])
    tokens = [t for t in re.findall(r"[a-z0-9&+-]+", q) if len(t) >= 4]
    if not tokens:
        return 0.0
    hits = sum(1 for t in set(tokens) if t in hay)
    return hits / max(len(set(tokens)), 1)


def _filter_by_explicit_module(scored: List[Dict], explicit_module: str) -> List[Dict]:
    if explicit_module == "General":
        return scored
    same_module = [
        row for row in scored
        if _module_from_source(str(row.get("source") or "")) == explicit_module
    ]
    if len(same_module) >= 2:
        return same_module
    if same_module and same_module[0].get("score", 0.0) >= 3.5:
        return same_module + [row for row in scored if row not in same_module][:2]
    return scored


def _is_action_oriented(line: str) -> bool:
    low = (line or "").lower()
    return any(term in low for term in [
        "click", "open", "go to", "navigate", "select", "choose", "publish",
        "confirm", "enable", "disable", "configure", "download",
    ])


def _select_evidence(
    query: str, scored: List[Dict], intent: str, explicit_module: str,
) -> List[Dict]:
    scoped = _filter_by_explicit_module(scored, explicit_module)
    if not scoped:
        return []
    top1 = scoped[0]
    top1_overlap = _query_overlap_score(query, top1)
    top1_source = str(top1.get("source") or "")

    if intent in {"page_lookup", "definition", "behavior"}:
        same_source = [row for row in scoped if str(row.get("source") or "") == top1_source]
        if top1.get("score", 0.0) >= 3.5 and top1_overlap >= 0.25:
            return same_source[:3] or [top1]
        return scoped[:4]

    if intent == "compare":
        return scoped[:4]

    if intent in {"setup", "troubleshooting", "chain"}:
        action_rows = []
        for row in scoped[:6]:
            text_lines = str(row.get("text") or "").splitlines()
            if any(_is_action_oriented(x) for x in text_lines):
                action_rows.append(row)
        return action_rows[:4] if action_rows else scoped[:3]

    return scoped[:4]
```

## Step 3 — Add answer composition functions

After `_select_evidence`, add:

```python


# ---------------------------------------------------------------------------
# Section 9 — Answer composition
# ---------------------------------------------------------------------------

def _evidence_lines(evidence: List[Dict]) -> List[str]:
    """Extract and deduplicate text lines from evidence chunks."""
    lines = []
    seen = set()
    for c in evidence:
        for raw in str(c.get("text") or "").splitlines():
            line = _clean_line(raw)
            if not line:
                continue
            low = line.lower()
            if low in seen:
                continue
            seen.add(low)
            lines.append(line)
    return lines


def _has_explicit_support(
    query: str, intent: str, evidence: List[Dict], lines: List[str],
) -> bool:
    if not evidence:
        return False
    top1 = evidence[0]
    top1_overlap = _query_overlap_score(query, top1)
    joined = "\n".join(lines).lower()

    if intent == "page_lookup":
        page = _canonical_page_name(
            str(top1.get("source") or ""),
            top1.get("heading_path") or [],
            str(top1.get("heading") or ""),
        )
        return bool(page) and top1_overlap >= 0.2

    if intent == "definition":
        return top1_overlap >= 0.2 and any(
            term in joined for term in [
                "means", "represents", "is the number of", "includes",
                "shows", "contains", "report", "response file", "link tracking report",
            ]
        )

    if intent == "behavior":
        return top1_overlap >= 0.2 and any(
            term in joined for term in [
                "when", "if", "after", "before", "enabled", "disabled",
                "active", "inactive",
            ]
        )

    if intent == "setup":
        return any(_is_action_oriented(line) for line in lines[:6])

    if intent == "troubleshooting":
        return any(
            term in joined for term in [
                "verify", "inspect", "check", "validate", "payload", "mapping",
            ]
        )

    if intent == "compare":
        return top1_overlap >= 0.2 and len(evidence) >= 1

    return bool(lines)


def _compose_answer(
    query: str,
    intent: str,
    entities: List[Dict],
    evidence: List[Dict],
) -> str:
    """Main answer composition: pick the best strategy based on intent + entities."""
    q = _normalize_query_for_match(query)
    lines = _evidence_lines(evidence)

    if intent == "compare" and len(entities) >= 2:
        answer = _compose_compare(entities, evidence, lines)
        if answer:
            return answer

    if entities:
        primary = entities[0]
        template = primary.get("templates", {}).get(intent)
        if template:
            return template

        for fallback_intent in ["setup", "page_lookup", "behavior", "definition"]:
            template = primary.get("templates", {}).get(fallback_intent)
            if template:
                return template

    if intent == "chain" and len(entities) >= 2:
        answer = _compose_chain(entities)
        if answer:
            return answer

    return _compose_from_evidence(query, intent, evidence, lines)


def _compose_compare(
    entities: List[Dict], evidence: List[Dict], lines: List[str],
) -> str:
    entity_ids = tuple(sorted(e["id"] for e in entities))

    for key, answer in COMPARE_OVERRIDES.items():
        if set(key) == set(entity_ids) or set(key).issubset(set(entity_ids)):
            return answer

    for key, answer in COMPARE_OVERRIDES.items():
        if any(eid in key for eid in entity_ids):
            return answer

    if len(entities) >= 2:
        parts = []
        for ent in entities[:3]:
            blurb = ent.get("compare_blurb", "")
            if blurb:
                parts.append(f"Use {ent['display']} when\n- {blurb}")
        if parts:
            return "\n".join(parts)

    return ""


def _compose_chain(entities: List[Dict]) -> str:
    steps = []
    for i, ent in enumerate(entities[:4], 1):
        template = ent.get("templates", {}).get("setup", "")
        if template:
            first_line = template.split("\n")[0]
            steps.append(f"{i}. **{ent['display']}** — {first_line}")
    if steps:
        return (
            "The documentation indicates you should use these components together for this pattern.\n\n"
            + "\n".join(steps)
        )
    return ""


def _compose_from_evidence(
    query: str, intent: str, evidence: List[Dict], lines: List[str],
) -> str:
    """Fallback: compose answer purely from retrieved evidence."""
    if not evidence or not lines:
        return "I don't know based on the current docs."

    if not _has_explicit_support(query, intent, evidence, lines):
        if intent == "page_lookup" and evidence:
            nearest_page = _canonical_page_name(
                str(evidence[0].get("source") or ""),
                evidence[0].get("heading_path") or [],
                str(evidence[0].get("heading") or ""),
            )
            if nearest_page:
                return f"I don't know based on the current docs. The nearest relevant page is `{nearest_page}`."
        return "I don't know based on the current docs."

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

    if intent == "definition":
        return "Definition\n- " + "\n- ".join(lines[:4]) if lines else "I don't know the exact definition from the current docs."

    if intent == "behavior":
        return "What happens\n- " + "\n- ".join(lines[:4]) if lines else "I don't know the exact behavior from the current docs."

    if intent == "schema":
        return "Key fields to store\n- " + "\n- ".join(lines[:5]) if lines else "I don't know the exact details from the current docs."

    if intent == "troubleshooting":
        return "Likely cause\n- " + lines[0] if lines else "I don't know based on the documentation provided."

    if intent == "compare":
        return "I don't know the exact compare details from the current docs."

    return "Exact path and steps\n- " + "\n- ".join(lines[:5]) if lines else "I don't know the exact details from the current docs."
```

## Test — Gate A (no behavior change)

Run `kb_answer({"query": "test your bot"})`. It should return **exactly the same answer as before this patch** because nothing calls the new functions yet. The old `_score_chunk` and old `kb_answer()` are still in use.

Confirm no syntax error by running any query.

### Quick function existence check

Verify these functions exist in the file (no errors on import):
- `_score_chunk_v2`
- `_select_evidence`
- `_evidence_lines`
- `_compose_answer`
- `_compose_compare`
- `_compose_from_evidence`

---
**Next:** Patch 6 swaps `kb_answer()` to use the new pipeline. That is the first behavior change.
