# Patch 9 — `kb_answer.py` (spot-check after Patch 8)

Apply **after** Patches **1–8**. Addresses remaining issues where answers were **technically grounded** but **wrong or generic** because:

1. **`_has_explicit_support`** accepted almost any chunk via the **high overlap shortcut** (`top1_overlap >= 0.35` and score ≥ 2.0) before intent/topic checks.
2. **Setup** intent still passed on **action verbs alone** (“Open Console…”) for **dynamic link** and **SMTP** questions without topic terms in evidence.
3. **Campaign in queue** was still classified as **setup** for some phrasings.
4. **Overview** lists showed **weak section titles** (“Details”, “Overview”) when the slug map did not apply.
5. **Ranking** still favored a few high-scoring but irrelevant paths (extra penalties).

**Target file:** `kb_answer.py` only.

---

## 9a — Intent: campaign + queue → troubleshooting

In **`_classify_intent`**, immediately after the `if is_troubleshoot: return "troubleshooting"` block, add:

```python
    if ("queue" in q or "queued" in q) and "campaign" in q:
        return "troubleshooting"
```

(Before the `is_overview` block.)

---

## 9b — Helpers: setup term checks + loose-overlap guard

**Add** `_setup_evidence_missing_required_terms` and replace **`_blocks_loose_explicit_support`** with versions that:

- For **queue + campaign** queries: block the overlap shortcut unless `joined` mentions queue/delivery/pending/etc.
- For **setup** intent: delegate dynamic-link and SMTP checks to **`_setup_evidence_missing_required_terms`**.

**In `_has_explicit_support`:**

1. After computing `joined`, only allow  
   `if top1_overlap >= 0.35 and top1.get("score", 0) >= 2.0: return True`  
   when **`not _blocks_loose_explicit_support(query, intent, joined)`**.

2. In the **`setup`** branch, **before** action-verb / overlap logic:

```python
        if _setup_evidence_missing_required_terms(query, joined):
            return False
```

3. In the **`troubleshooting`** branch, if the query has **queue + campaign**, require queue-related terms in `joined` **before** the generic verify/check list (see implementation in repo).

---

## 9c — Overview list labels

**Add** `_WEAK_OVERVIEW_PAGE_LABELS`, **`_fallback_page_title_from_source`**, **`_overview_list_page_label`**.

In **`_compose_from_evidence`** (overview branch), build each bullet with **`_overview_list_page_label(c)`** instead of raw **`_canonical_page_name`**.

---

## 9d — Extra source penalties (`_query_source_penalty_adjustment`)

Extend with (when conditions match):

| Condition | Penalized source hints | Adj |
|-----------|------------------------|-----|
| queue + campaign | `about-campaign-manager` | -7 |
| dynamic-link phrase block | `how-to-measure-click-through`, `measure-click-through` | -8 |
| SMTP + Agent Assist | `user-management-users`, `user-management-teams` | -9 |
| Agent Assist orientation (`give me an overview` / `overview of` / `key areas` / `where to start`) | `chat-management-assignment-rules`, `assignment-rules` | -7 |

---

## Verify

```bash
python3 -m py_compile kb_answer.py
python3 test_patches.py && python3 test_regression.py
```

---

## Summary

| Issue | Mechanism |
|-------|-----------|
| Queue question → generic setup | Troubleshooting intent + queue terms in evidence + penalties |
| Dynamic link / SMTP → generic setup | Setup branch requires topic tokens in evidence; overlap shortcut blocked |
| Overview list noisy headings | Weak heading labels replaced by slug-based titles |
| Assignment Rules still tops broad overview | Extra penalty when query looks like Agent Assist onboarding |

The authoritative implementation is the current **`kb_answer.py`** in this repo; this file is a **change summary** for agents that apply patches manually.

---

## Patch 9e — Entity template fallback vs troubleshooting (critical)

**Symptom:** Queue + campaign questions still answered as **“Exact page → Campaign Analytics”** even when intent was **`troubleshooting`**, because **`campaign_analytics`** has no `troubleshooting` template and the code **fell through to `page_lookup`** via `for fallback_intent in ["setup", "page_lookup", ...]`.

**Fix:** In **`_compose_answer`**, **do not run** that fallback loop when **`intent in ("troubleshooting", "schema")`** — use evidence / IDK instead.

**Optional:** Add **`"what can i do if"`** / **`"what can we do if"`** to **`_TROUBLESHOOT_SIGNALS`** so phrasing is classified as troubleshooting even without the queue heuristic.
