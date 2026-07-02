#!/usr/bin/env python3
"""Cross-channel isolation test: WhatsApp vs RCS template queries."""
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
        except AttributeError:
            pass
        try:
            mod._read_json = _read_json_local
        except AttributeError:
            pass
    return FakeCtx()


def run_query(kbs, ctx, query):
    res = kbs.kb_search({"query": query, "top_k": 5}, context=ctx)
    results = res.get("results") or []
    top = results[0] if results else {}
    return {
        "query": query,
        "top_source": top.get("source") or "",
        "confidence": top.get("score") or 0.0,
        "top5": [{"score": round(r.get("score") or 0.0, 4), "source": r.get("source")} for r in results[:5]],
    }


def main():
    ctx = setup_local_kb()
    import kb_search as kbs

    out = {}
    for label, q in (("q1_whatsapp", "whatsapp template"), ("q2_rcs", "rcs template")):
        out[label] = run_query(kbs, ctx, q)

    print("JSON_RESULT_START")
    print(json.dumps(out, indent=2))
    print("JSON_RESULT_END")


if __name__ == "__main__":
    main()
