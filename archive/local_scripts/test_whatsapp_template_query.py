#!/usr/bin/env python3
"""Verify the WhatsApp template variable-parameters query (primary fix target).

Query: "maximum number of variable parameters for WhatsApp message template"
Expected post-fix: confidence > 2.0, top_source contains 'whatsapp',
answer references WhatsApp (not RCS).

Analytics-only harness: loads local KB chunks, runs the current kb_answer
pipeline, prints the result. Does NOT modify skill code.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill"))

QUERY = "maximum number of variable parameters for WhatsApp message template"


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

    res = kba.kb_answer({"query": QUERY}, context=ctx)
    meta = (res.get("langfuse") or {}).get("metadata") or {}
    answer = res.get("answer") or ""

    confidence = meta.get("confidence")
    top_source = meta.get("top_source") or ""

    out = {
        "query": QUERY,
        "confidence": confidence,
        "top_source": top_source,
        "top_score": meta.get("top_score"),
        "source_count": meta.get("source_count"),
        "answered": meta.get("answered"),
        "answer_excerpt": answer[:600],
        "mentions_whatsapp": "whatsapp" in answer.lower(),
        "mentions_rcs": "rcs" in answer.lower(),
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
