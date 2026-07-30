#!/usr/bin/env python3
"""
Verify telemetry preserves the ORIGINAL (pre-translation) query.

Asserts:
  - Non-English query  -> metadata.query == original text; metadata.query_translated present (English).
  - English query      -> metadata.query == original text; NO query_translated key.
Covers both kb_answer._send_langfuse and kb_search._compact_langfuse.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill"))


def _extract_meta(result: dict) -> dict:
    """Pull the langfuse metadata dict out of a kb_answer/kb_search result."""
    lf = result.get("langfuse") or {}
    return lf.get("metadata") or {}


def setup_local_kb():
    import kb_storage
    import kb_answer as kba
    import kb_search as kbs

    chunks_path = ROOT / "kb" / "kb_chunks.jsonl"

    def _load_chunks_local(context=None):
        items = []
        with chunks_path.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    items.append(json.loads(line))
        return items

    def _read_json_local(path, context=None):
        p = ROOT / path if not str(path).startswith("/") else Path(path)
        return json.loads(p.read_text(encoding="utf-8"))

    class FakeCtx:
        def get_secret(self, name):
            return None  # no Langfuse host -> no network call, dict still returned

    for mod in (kb_storage, kba, kbs):
        try:
            mod._load_chunks = _load_chunks_local
            mod._read_json = _read_json_local
        except AttributeError:
            pass
    return FakeCtx()


PT_QUERY = "Que tipo de demonstração posso apresentar para uma marca automotiva?"
EN_QUERY = "What kind of demo can I present for an automotive brand?"

passed = []
failed = []


def check(name, cond, detail=""):
    (passed if cond else failed).append(name)
    icon = "✓" if cond else "✗"
    print(f"  {icon} {name}" + (f"  — {detail}" if detail and not cond else ""))


def main():
    ctx = setup_local_kb()
    import kb_answer as kba
    import kb_search as kbs

    print("=" * 70)
    print("kb_answer telemetry")
    print("=" * 70)
    res_pt = kba.kb_answer({"query": PT_QUERY}, context=ctx)
    m_pt = _extract_meta(res_pt)
    print(f"  PT metadata.query           = {m_pt.get('query')!r}")
    print(f"  PT metadata.query_translated= {m_pt.get('query_translated')!r}")
    check("kb_answer PT: query is original (non-ascii preserved)",
          "demonstração" in (m_pt.get("query") or ""), m_pt.get("query"))
    check("kb_answer PT: query_translated present",
          bool(m_pt.get("query_translated")))
    check("kb_answer PT: query_translated is English (demo)",
          "demo" in (m_pt.get("query_translated") or "").lower())

    res_en = kba.kb_answer({"query": EN_QUERY}, context=ctx)
    m_en = _extract_meta(res_en)
    print(f"  EN metadata.query           = {m_en.get('query')!r}")
    print(f"  EN metadata.query_translated= {m_en.get('query_translated')!r}")
    check("kb_answer EN: query present", bool(m_en.get("query")))
    check("kb_answer EN: NO query_translated key",
          "query_translated" not in m_en, str(list(m_en.keys())))

    print("=" * 70)
    print("kb_search telemetry")
    print("=" * 70)
    sres_pt = kbs.kb_search({"query": PT_QUERY}, context=ctx)
    sm_pt = _extract_meta(sres_pt)
    print(f"  PT metadata.query           = {sm_pt.get('query')!r}")
    print(f"  PT metadata.query_translated= {sm_pt.get('query_translated')!r}")
    check("kb_search PT: query is original (non-ascii preserved)",
          "demonstração" in (sm_pt.get("query") or ""), sm_pt.get("query"))
    check("kb_search PT: query_translated present",
          bool(sm_pt.get("query_translated")))

    sres_en = kbs.kb_search({"query": EN_QUERY}, context=ctx)
    sm_en = _extract_meta(sres_en)
    print(f"  EN metadata.query           = {sm_en.get('query')!r}")
    print(f"  EN metadata.query_translated= {sm_en.get('query_translated')!r}")
    check("kb_search EN: query present", bool(sm_en.get("query")))
    check("kb_search EN: NO query_translated key",
          "query_translated" not in sm_en, str(list(sm_en.keys())))

    print("=" * 70)
    print(f"PASSED {len(passed)}  FAILED {len(failed)}")
    if failed:
        print("FAILURES:", failed)
        sys.exit(1)
    print("ALL TELEMETRY ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
