# Hotfix — `_compose_from_evidence` page_lookup indentation (`kb_answer.py`)

**Risk:** Low  
**Files:** `kb_answer.py` only (do **not** change `kb_search.py`)  
**Telemetry:** Do not modify any Langfuse/telemetry code.

## Why this patch

A bad indent breaks Python at **line ~2474**: `IndentationError: expected an indented block` (Pylance/basedpyright shows the file in red). The `for line in lines[:2]:` loop had no body, and the `page_lookup` logic was partially outside its `if`, which would also cause **`NameError: page is not defined`** on non–`page_lookup` intents at runtime.

## Location

Function: **`_compose_from_evidence`**  
Search for the first occurrence of:

```python
    if intent == "page_lookup" and evidence:
        c = evidence[0]
        page = _canonical_page_name(
```

## Replace (broken) — DELETE this entire block

If your file matches the **broken** pattern below, replace it with the **fixed** block in the next section.

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

    if intent == "definition":
```

**Signs you are broken:** `out = ["Exact page"]` starts at the **same** indent as `if intent == "page_lookup"` (not indented one more level), and `out.append(f"- {line}")` is **not** indented under `for line in lines[:2]:`.

## Replace (fixed) — USE this block

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

    if intent == "definition":
```

## Verification

1. **Syntax:** `python3 -m py_compile kb_answer.py` — must exit **0**.
2. **Smoke — `kb_answer`**

| ID | Query | Expected |
|----|--------|----------|
| P-S1 | Where do I configure business hours? | Answer mentions Business Hours / exact page style (not crash). |
| P-S2 | What is sticky assignment? | Normal behavior-style answer. |
| P-S3 | How do I make pizza? | Off-topic refusal (unchanged). |

3. **IDE:** No red error on `kb_answer.py` from the Python language server.

## Summary

| Item | Value |
|------|--------|
| Root cause | `page_lookup` block dedented; `for` loop body missing indent |
| Fix | Indent `out` / `if page` / `for` / `return` under `if intent == "page_lookup" and evidence:` |
