#!/usr/bin/env python3
"""Fetch last-N-day IDK traces and replay locally to diagnose gate failures."""
from __future__ import annotations

import json
import os
import sys
from collections import Counter, defaultdict
from datetime import timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "local" / "scripts"))
sys.path.insert(0, str(ROOT / "skill"))

from analytics_common import (  # noqa: E402
    build_corpus,
    fetch_langfuse_traces,
    is_idk,
    parse_iso,
    utc_now,
)

OUT = ROOT / "local" / "reports" / "idk_analysis_7d.json"


def _setup_local_kb():
    import kb_storage
    import kb_answer
    import kb_search

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

    class FakeContext:
        def get_secret(self, name):
            return None

    kb_answer._load_chunks = _load_chunks_local
    kb_search._load_chunks = _load_chunks_local
    kb_answer._send_langfuse = lambda *a, **k: {}
    kb_search._compact_langfuse = lambda *a, **k: {}
    kb_storage.read_json = _read_json_local
    try:
        import kb_video
        kb_video.record_video_delivery = lambda *a, **k: None
    except Exception:
        pass
    return kb_answer, FakeContext()


def _replay_query(kb_answer, ctx, query: str) -> Dict[str, Any]:
    r = kb_answer.kb_answer(parameters={"query": query}, context=ctx)
    ans = str(r.get("answer") or "")
    lf = r.get("langfuse") or {}
    md = lf.get("metadata") or {}
    return {
        "answer_is_idk": is_idk(ans),
        "answer_preview": ans[:200],
        "module_label": md.get("module_label") or lf.get("module_label"),
        "mode": md.get("selected_answer_mode"),
        "intents": md.get("intent_labels"),
        "top_source": md.get("top_source"),
        "top_score": md.get("top_score"),
        "source_count": md.get("source_count"),
        "video_attached": md.get("video_attached"),
        "video_appended": md.get("video_appended_to_answer"),
        "answered": md.get("answered"),
        "unanswered": md.get("unanswered"),
    }


def _classify_failure(trace: Dict[str, Any], replay: Optional[Dict[str, Any]]) -> str:
    score = trace.get("top_score")
    mode = trace.get("mode") or ""
    intents = trace.get("intents") or []
    src = trace.get("top_source") or ""
    q = (trace.get("query") or "").lower()

    if not src and (score is None or score == 0):
        return "no_retrieval_match"
    if mode == "refusal" or "refusal" in intents:
        return "guardrail_refusal"
    if score is not None and score < 0.5:
        return "very_low_score"
    if score is not None and 0.5 <= score < 1.2:
        return "below_MIN_EVIDENCE_SCORE_1.2"
    if score is not None and 1.2 <= score < 4.0 and mode not in ("overview",):
        return "support_gate_or_topic_coverage"
    if "compare" in intents or mode == "compare":
        return "compare_intent_insufficient_sources"
    if any(t in q for t in ("third party", "external", "integration", "webhook", "api")):
        return "integration_doc_gap"
    if any(t in q for t in ("customer 360", "cc express", "sla", "leadsquared", "catalog message")):
        return "undocumented_or_missing_topic"
    if replay and not replay.get("answer_is_idk"):
        return "would_answer_now_replay"
    return "support_gate_or_topic_coverage"


def main() -> int:
    days = 7
    since = utc_now() - timedelta(days=days)
    traces: List[Dict[str, Any]] = []
    fetch_err = None
    try:
        raw = fetch_langfuse_traces(since, limit=5000)
        for t in raw:
            out = t.get("output") or {}
            ans = (out.get("answer") if isinstance(out, dict) else "") or ""
            meta = t.get("metadata") or {}
            if meta.get("unanswered") or is_idk(ans):
                traces.append({
                    "ts": t.get("timestamp"),
                    "user": t.get("userId") or meta.get("user_email"),
                    "query": (t.get("input") or {}).get("query") or meta.get("query"),
                    "module": meta.get("module_label"),
                    "mode": meta.get("selected_answer_mode"),
                    "intents": meta.get("intent_labels"),
                    "top_source": meta.get("top_source"),
                    "top_score": meta.get("top_score"),
                    "source_count": meta.get("source_count"),
                    "video_attached": meta.get("video_attached"),
                    "module_source": meta.get("module_source"),
                    "answer_preview": (ans or meta.get("answer_preview") or "")[:160],
                })
    except Exception as exc:
        fetch_err = str(exc)
        # Fallback: deduped events from NDJSON only (Langfuse down)
        events, _, meta = build_corpus(since)
        for e in events:
            if e.idk and e.action == "kb_answer":
                traces.append({
                    "ts": e.ts.isoformat(),
                    "user": e.user_email,
                    "query": e.query,
                    "module": e.module,
                    "mode": e.mode,
                    "intents": e.intents,
                    "top_source": e.top_source,
                    "top_score": e.top_score,
                    "source_count": e.source_count,
                    "video_attached": e.video_attached,
                    "source": e.source,
                    "answer_preview": "",
                })

    kb_answer, ctx = _setup_local_kb()
    enriched = []
    failure_modes = Counter()
    for i, tr in enumerate(traces):
        rep = None
        if tr.get("query"):
            try:
                rep = _replay_query(kb_answer, ctx, tr["query"])
            except Exception as exc:
                rep = {"replay_error": str(exc)}
        fm = _classify_failure(tr, rep)
        failure_modes[fm] += 1
        row = {**tr, "failure_mode": fm, "replay": rep}
        enriched.append(row)

    payload = {
        "generated_at": utc_now().isoformat(),
        "window_days": days,
        "fetch_error": fetch_err,
        "idk_count": len(enriched),
        "failure_modes": dict(failure_modes.most_common()),
        "by_module": dict(Counter(t.get("module") or "unknown" for t in enriched).most_common()),
        "by_mode": dict(Counter(t.get("mode") or "unknown" for t in enriched).most_common()),
        "score_buckets": _score_buckets(enriched),
        "video_on_idk": sum(1 for t in enriched if t.get("video_attached")),
        "items": enriched,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    print(json.dumps({
        "idk_count": payload["idk_count"],
        "fetch_error": fetch_err,
        "failure_modes": payload["failure_modes"],
        "wrote": str(OUT),
    }, indent=2))
    return 0


def _score_buckets(items: List[Dict]) -> Dict[str, int]:
    c = Counter()
    for t in items:
        s = t.get("top_score")
        if s is None:
            c["no_score"] += 1
        elif s < 0.5:
            c["<0.5"] += 1
        elif s < 1.2:
            c["0.5-1.2"] += 1
        elif s < 4.0:
            c["1.2-4.0"] += 1
        else:
            c[">=4.0"] += 1
    return dict(c)


if __name__ == "__main__":
    raise SystemExit(main())
