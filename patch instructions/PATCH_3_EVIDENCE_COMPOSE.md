# Patch 3 of 3 — Evidence Fallback + Compose Improvements (kb_answer.py only)

**File**: `product_introduction_kb/kb_answer.py`
**Risk**: Medium (behavior change in answer composition)
**Telemetry**: Do NOT touch any Langfuse/telemetry code.

---

## Overview

This patch improves the answer composition fallback path so queries that don't match any CONCEPT_REGISTRY entity can still get useful answers when the retrieved evidence is strong. Changes:
1. `_has_explicit_support` — trust high-overlap evidence even without entity match
2. `_compose_from_evidence` — generate compare answers from evidence headings, anchor answers with chunk headings

---

## Step 1 — Update `_has_explicit_support` function

Find the `_has_explicit_support` function. Replace the ENTIRE function with:

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
        return True

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
                "configure", "create", "manage", "set up", "export",
                "what is", "defined as", "refers to",
            ]
        )

    if intent == "behavior":
        return top1_overlap >= 0.2 and any(
            term in joined for term in [
                "when", "if", "after", "before", "enabled", "disabled",
                "active", "inactive", "triggers", "happens",
            ]
        )

    if intent == "setup":
        return any(_is_action_oriented(line) for line in lines[:6]) or top1_overlap >= 0.3

    if intent == "troubleshooting":
        return any(
            term in joined for term in [
                "verify", "inspect", "check", "validate", "payload", "mapping",
                "ensure", "confirm", "review", "debug",
            ]
        )

    if intent == "compare":
        return top1_overlap >= 0.2 and len(evidence) >= 1

    return bool(lines)
```

Key changes vs. original:
- New signature adds optional `entities` parameter
- New early-return: if `top1_overlap >= 0.35` and `top1.get("score", 0) >= 2.0`, return `True` immediately
- Expanded term lists for definition (added `"configure"`, `"create"`, `"manage"`, `"set up"`, `"export"`, `"what is"`, `"defined as"`, `"refers to"`)
- Expanded term lists for behavior (added `"triggers"`, `"happens"`)
- Setup intent now also passes if `top1_overlap >= 0.3`
- Expanded troubleshooting terms (added `"ensure"`, `"confirm"`, `"review"`, `"debug"`)

---

## Step 2 — Update `_compose_from_evidence` function

Find the `_compose_from_evidence` function. Replace the ENTIRE function with:

```python
def _compose_from_evidence(
    query: str, intent: str, evidence: List[Dict], lines: List[str],
    entities: List[Dict] = None,
) -> str:
    """Fallback: compose answer purely from retrieved evidence."""
    if not evidence or not lines:
        return "I don't know based on the current docs."

    if not _has_explicit_support(query, intent, evidence, lines, entities):
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
        heading = str(evidence[0].get("heading") or "").strip()
        prefix = f"**{heading}**\n" if heading else ""
        return prefix + "Definition\n- " + "\n- ".join(lines[:4]) if lines else "I don't know the exact definition from the current docs."

    if intent == "behavior":
        return "What happens\n- " + "\n- ".join(lines[:4]) if lines else "I don't know the exact behavior from the current docs."

    if intent == "schema":
        return "Key fields to store\n- " + "\n- ".join(lines[:5]) if lines else "I don't know the exact details from the current docs."

    if intent == "troubleshooting":
        return "Likely cause\n- " + lines[0] if lines else "I don't know based on the documentation provided."

    if intent == "compare" and evidence and len(evidence) >= 2:
        h1 = str(evidence[0].get("heading") or "").strip()
        h2 = str(evidence[1].get("heading") or "").strip()
        if h1 and h2:
            l1 = [l for l in str(evidence[0].get("text") or "").splitlines() if _clean_line(l)][:2]
            l2 = [l for l in str(evidence[1].get("text") or "").splitlines() if _clean_line(l)][:2]
            parts = [f"Based on the docs:"]
            parts.append(f"- **{h1}**: " + (_clean_line(l1[0]) if l1 else "See documentation."))
            parts.append(f"- **{h2}**: " + (_clean_line(l2[0]) if l2 else "See documentation."))
            return "\n".join(parts)

    if intent == "compare":
        return "I don't know the exact compare details from the current docs."

    heading = str(evidence[0].get("heading") or "").strip()
    if heading and lines:
        return f"**{heading}**\nExact path and steps\n- " + "\n- ".join(lines[:5])

    return "Exact path and steps\n- " + "\n- ".join(lines[:5]) if lines else "I don't know the exact details from the current docs."
```

Key changes vs. original:
- New signature adds optional `entities` parameter
- Calls `_has_explicit_support` with `entities` arg
- Definition intent now anchors answer with evidence heading (`**{heading}**` prefix)
- Compare intent with 2+ evidence chunks composes from headings instead of "I don't know"
- Default fallback anchors with heading when available

---

## Step 3 — Update the caller

Find the line that calls `_compose_from_evidence` inside `_compose_answer`:

```python
    return _compose_from_evidence(query, intent, evidence, lines)
```

Replace with:

```python
    return _compose_from_evidence(query, intent, evidence, lines, entities)
```

---

## Smoke Tests

### kb_answer

| ID | Query | Expected |
|----|-------|----------|
| A-S1 | "What is the Address Node and which WABA regions does it support?" | Answer should mention Address Node (NOT "I don't know") |
| A-S2 | "What is the difference between intents and entities in AI Admin?" | Answer should compare intents vs entities (NOT "I don't know the exact compare details") |
| A-S3 | "What is sticky assignment?" | Answer mentions Sticky Assignment (existing, not regressed) |
| A-S4 | "Where do I configure business hours?" | Answer mentions Business Hours (existing, not regressed) |
| A-N1 | "How do I make pizza?" | Refused (off-topic, existing, not regressed) |

---

## Validation Checklist

- [ ] `kb_answer` action executes successfully
- [ ] All smoke tests pass
- [ ] No telemetry code was modified
