# Latest patches — `kb_answer.py` (Patch 7 optional)

This file is a **standalone** copy of the **most recent** optional patch layer. Full incremental history (Patches 1–6) lives in **`PATCH_INSTRUCTIONS.md`**.

**Prerequisite:** Patches **1–6** are already applied to `kb_answer.py`. If not, apply those first from `PATCH_INSTRUCTIONS.md`.

**Target file:** `kb_answer.py` only.

---

## Patch 7 — Eval-driven query/source penalties + overview diversity

**What it fixes:** Recurring **mis-ranked sources** from evals (campaign queue vs Personalize, dynamic link tracking vs generic send/analytics, SMTP vs marketing templates) and **noisy overview** page lists.

**What it does not fix:** Missing KB articles — add real docs for “campaign in queue”, “dynamic link tracking setup”, SMTP, etc., when the product needs definitive answers.

---

### Step 7a — `_query_source_penalty_adjustment` + call in `_score_chunk`

**Insert** the new function **immediately after** `_score_chunk` (after its `return score`, before `# Section 8 — Evidence selection`).

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

**Inside `_score_chunk`,** immediately **before** the final `return score` (after entity boosts/penalties and `GLOBAL_PENALTY_SOURCES`), add:

```python
    score += _query_source_penalty_adjustment(q, source)
```

Use the same `q` and `source` already defined at the start of `_score_chunk`.

**Tuning:** `-8.0`, `-6.0`, `-10.0` can be adjusted if ranking shifts; keep values **negative**.

---

### Step 7b — Overview diversity: helpers + branch in `_select_evidence`

**Insert** **`_overview_source_bucket`** and **`_select_evidence_overview_diverse`** immediately **before** `def _select_evidence(`.

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

**Inside `_select_evidence`,** add **before** the final `return scoped[:4]` (after the `setup` / `troubleshooting` / `chain` block):

```python
    if intent == "overview":
        return _select_evidence_overview_diverse(scoped, limit=4)
```

---

### Step 7c — Verify (no extra test files)

```bash
python3 -m py_compile kb_answer.py
grep -n _query_source_penalty_adjustment kb_answer.py
grep -n _select_evidence_overview_diverse kb_answer.py
```

Expect the penalty call inside `_score_chunk` and the overview branch in `_select_evidence`.

---

## Summary

| Piece | Role |
|-------|------|
| `_query_source_penalty_adjustment` | Down-ranks known bad query↔source pairs |
| `_select_evidence_overview_diverse` | Reduces duplicate themes in overview answers |

---

## `kb_search.py`

Not modified here. If search duplicates scoring, consider mirroring penalty logic separately.
