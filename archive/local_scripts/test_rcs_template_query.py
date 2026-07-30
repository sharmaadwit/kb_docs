#!/usr/bin/env python3
"""Ad-hoc test: RCS template variables query should resolve to RCS, not WhatsApp."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill"))


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
    import kb_search as kbs

    query = "rcs message template variables"
    res = kbs.kb_search({"query": query, "top_k": 5}, context=ctx)

    results = res.get("results") or []
    top = results[0] if results else {}
    top_source = top.get("source") or ""
    confidence = top.get("score") or 0.0

    print(f"Query: {query}")
    print(f"Top source: {top_source}")
    print(f"Confidence (top score): {confidence}")
    print("Top 5 sources:")
    for r in results[:5]:
        print(f"  {r.get('score'):.4f}  {r.get('source')}")

    lf = res.get("langfuse") or {}
    meta = lf.get("metadata") or {}
    print(f"langfuse top_source: {meta.get('top_source')}")
    print(f"langfuse confidence: {meta.get('confidence')}")
    print(f"langfuse module: {meta.get('module')}")

    out = {
        "query": query,
        "top_source": top_source,
        "confidence": confidence,
        "results": [{"score": r.get("score"), "source": r.get("source")} for r in results[:5]],
        "module": meta.get("module"),
    }
    print("JSON_RESULT_START")
    print(json.dumps(out))
    print("JSON_RESULT_END")


if __name__ == "__main__":
    main()
