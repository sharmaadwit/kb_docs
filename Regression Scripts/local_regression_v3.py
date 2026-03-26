#!/usr/bin/env python3
"""
Run regression_v3 dataset: kb_search + kb_answer against kb/kb_chunks.jsonl.
Negatives: answer-only (search not scored).
"""
import importlib.util
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
from cursor_test_context import CursorKBTestContext

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"
QUESTIONS_PATH = ARTIFACTS / "regression_v3_questions.json"
OUT_RESULTS = ARTIFACTS / "regression_v3_results.json"
OUT_SUMMARY = ARTIFACTS / "regression_v3_summary.json"
OUT_LOG = ARTIFACTS / "regression_v3_run.log"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def norm(s):
    s = (s or "").lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def score_answer(text, kind, required_any, required_all):
    t = norm(text)
    if kind == "negative":
        refusal = [
            "i can t help",
            "i can help only with documented gupshup console and kb topics",
            "i don t know based on the current documentation",
            "i don t know based on the current docs",
            "i don t know based on the docs",
            "unsupported",
            "sensitive",
            "cannot help",
        ]
        return 1.0 if any(x in t for x in refusal) else 0.15
    if "i don t know" in t and kind == "supported":
        return 0.2
    score = 0.0
    req_any = required_any or []
    req_all = required_all or []
    if req_any:
        hits = sum(1 for term in req_any if norm(term) in t)
        score += min(0.85, 0.85 * hits / max(1, len(req_any)))
    else:
        score += 0.35
    if req_all:
        hits = sum(1 for term in req_all if norm(term) in t)
        score += 0.15 * hits / max(1, len(req_all))
    return round(max(0.0, min(1.0, score)), 2)


def score_search(search_blob, required_any):
    blob = (search_blob or "").lower()
    req = required_any or []
    if not req:
        return 0.5
    hits = sum(1 for slug in req if slug.lower().replace(" ", "-") in blob or slug.lower() in blob)
    return round(min(1.0, 0.25 + 0.75 * hits / len(req)), 2)


def serialize_search_results(results):
    if not results:
        return ""
    parts = []
    for row in results[:5]:
        parts.append(str(row.get("source") or ""))
        parts.extend(str(x) for x in (row.get("heading_path") or []))
        parts.append(str(row.get("heading") or ""))
    return "\n".join(parts)


def main():
    kb_search = load_module("kb_search_v3", ROOT / "kb_search.py")
    kb_answer = load_module("kb_answer_v3", ROOT / "kb_answer.py")

    chunks = []
    chunks_path = ROOT / "kb" / "kb_chunks.jsonl"
    if not chunks_path.is_file():
        print(f"Missing {chunks_path}", file=sys.stderr)
        sys.exit(1)
    with open(chunks_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))

    kb_search._load_chunks = lambda context: chunks
    kb_answer._load_chunks = lambda context: chunks

    context = CursorKBTestContext()

    data = json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))
    questions = data["questions"]

    log_lines = [f"started {datetime.now(timezone.utc).isoformat()}", f"questions={len(questions)}"]

    results = []
    for spec in questions:
        q = spec["query"]
        kind = spec.get("kind", "supported")
        search_out = kb_search.kb_search({"query": q, "top_k": 5}, context=context)
        answer_out = kb_answer.kb_answer({"query": q}, context=context)
        search_blob = serialize_search_results(search_out.get("results", []))
        answer_text = answer_out.get("answer", "")

        ans_score = score_answer(
            answer_text,
            kind,
            spec.get("answer_required_any") or [],
            spec.get("answer_required_all") or [],
        )
        if kind == "negative":
            search_score = None
            search_ok = None
        else:
            search_score = score_search(search_blob, spec.get("search_required_any") or [])
            search_ok = search_score >= 0.75

        ans_ok = ans_score >= 0.75
        results.append(
            {
                "idx": spec["idx"],
                "query": q,
                "category": spec["category"],
                "kind": kind,
                "kb_search": {
                    "score": search_score,
                    "correct": search_ok,
                    "top_source": (search_out.get("results") or [{}])[0].get("source"),
                },
                "kb_answer": {
                    "score": ans_score,
                    "correct": ans_ok,
                    "answer_preview": (answer_text[:280] + "…") if len(answer_text) > 280 else answer_text,
                },
            }
        )

    supported = [r for r in results if r["kind"] != "negative"]
    negative = [r for r in results if r["kind"] == "negative"]

    s_search = sum(1 for r in supported if r["kb_search"]["correct"])
    s_ans = sum(1 for r in supported if r["kb_answer"]["correct"])
    n_ans = sum(1 for r in negative if r["kb_answer"]["correct"])

    cat = defaultdict(lambda: {"n": 0, "s_n": 0, "s_ok": 0, "a_ok": 0})
    for r in results:
        c = r["category"]
        cat[c]["n"] += 1
        if r["kind"] != "negative":
            cat[c]["s_n"] += 1
            if r["kb_search"]["correct"]:
                cat[c]["s_ok"] += 1
        if r["kb_answer"]["correct"]:
            cat[c]["a_ok"] += 1

    summary = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "dataset": data.get("dataset_name"),
        "totals": {
            "questions": len(results),
            "supported": len(supported),
            "negative": len(negative),
        },
        "kb_search_supported": {
            "correct": s_search,
            "total": len(supported),
            "pct": round(100.0 * s_search / max(1, len(supported)), 1),
        },
        "kb_answer_supported": {
            "correct": s_ans,
            "total": len(supported),
            "pct": round(100.0 * s_ans / max(1, len(supported)), 1),
        },
        "kb_answer_negative": {
            "correct": n_ans,
            "total": len(negative),
            "pct": round(100.0 * n_ans / max(1, len(negative)), 1),
        },
        "kb_answer_overall": {
            "correct": s_ans + n_ans,
            "total": len(results),
            "pct": round(100.0 * (s_ans + n_ans) / max(1, len(results)), 1),
        },
        "category_breakdown": {
            k: {
                "count": v["n"],
                "search_pct": round(100.0 * v["s_ok"] / max(1, v["s_n"]), 1) if v["s_n"] else None,
                "answer_pct": round(100.0 * v["a_ok"] / v["n"], 1),
            }
            for k, v in sorted(cat.items())
        },
        "failures_answer": [r["query"] for r in results if not r["kb_answer"]["correct"]],
        "failures_search": [r["query"] for r in supported if not r["kb_search"]["correct"]],
    }

    OUT_RESULTS.write_text(json.dumps({"results": results}, indent=2), encoding="utf-8")
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    log_lines.append(
        f"search_supported {s_search}/{len(supported)} answer_supported {s_ans}/{len(supported)} answer_negative {n_ans}/{len(negative)}"
    )
    log_lines.append(f"done {datetime.now(timezone.utc).isoformat()}")
    OUT_LOG.write_text("\n".join(log_lines), encoding="utf-8")
    print(json.dumps(summary["totals"], indent=2))
    print("search_supported", summary["kb_search_supported"])
    print("answer_supported", summary["kb_answer_supported"])
    print("answer_negative", summary["kb_answer_negative"])


if __name__ == "__main__":
    main()
