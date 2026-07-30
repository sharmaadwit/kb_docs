#!/usr/bin/env python3
"""Regression check: SuperAgent + Agent Assist queries with current KB (meta boost=3.0)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill"))

QUERIES = [
    "How do I use SuperAgent?",
    "What is Agent Assist?",
    "SuperAgent use cases",
    "Human agent support",
]


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
            return None

    for mod in (kb_storage, kba, kbs):
        try:
            mod._load_chunks = _load_chunks_local
            mod._read_json = _read_json_local
        except AttributeError:
            pass
    return FakeCtx()


def main():
    ctx = setup_local_kb()
    import kb_answer as kba

    results = []
    for q in QUERIES:
        res = kba.kb_answer({"query": q}, context=ctx)
        meta = (res.get("langfuse") or {}).get("metadata") or {}
        answer = res.get("answer") or ""
        citations = res.get("citations") or []
        results.append({
            "query": q,
            "answer_preview": answer[:300],
            "answer_length": len(answer),
            "confidence": meta.get("confidence"),
            "top_score": meta.get("top_score"),
            "top_source": meta.get("top_source") or "",
            "modules": meta.get("modules") or [],
            "citations": citations,
            "source_count": meta.get("source_count"),
            "answered": meta.get("answered"),
        })
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
