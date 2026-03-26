#!/usr/bin/env python3
"""
Replay Langfuse-exported kb_answer queries against local kb_answer.py; compare to trace answers.
Usage:
  python3 langfuse_replay_compare.py [path/to/export.json] [--max N]
"""
import argparse
import importlib.util
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
from cursor_test_context import CursorKBTestContext

ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def norm(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9\s]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def is_refusal(t: str) -> bool:
    n = norm(t)
    return any(
        x in n
        for x in [
            "i can help only with documented",
            "i don t know based on the current docs",
            "i don't know based on the current docs",
            "unsupported",
            "sensitive",
            "cannot help with that",
        ]
    )


def is_idk(t: str) -> bool:
    n = norm(t)
    return "don t know" in n or "don't know" in n or "i can t help" in n


def similarity(a: str, b: str) -> float:
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def extract_langfuse_qa(events):
    """First occurrence per query wins (langfuse answer)."""
    seen = {}
    order = []
    for e in events:
        if e.get("name") != "kb_answer" or e.get("type") != "SPAN":
            continue
        inp = e.get("input")
        if not inp:
            continue
        try:
            d = json.loads(inp) if isinstance(inp, str) else inp
        except Exception:
            continue
        q = (d.get("query") or "").strip() if isinstance(d, dict) else ""
        if not q:
            continue
        if q in seen:
            continue
        ans = ""
        out = e.get("output")
        if out:
            try:
                o = json.loads(out) if isinstance(out, str) else out
                if isinstance(o, dict):
                    ans = str(o.get("answer") or "")
            except Exception:
                ans = str(out)
        seen[q] = ans
        order.append(q)
    return [(q, seen[q]) for q in order]


def classify(lf: str, loc: str) -> str:
    if is_refusal(lf) and is_refusal(loc):
        return "both_refusal"
    if is_refusal(lf) != is_refusal(loc):
        return "refusal_mismatch"
    if is_idk(lf) and is_idk(loc):
        return "both_idk"
    if is_idk(lf) != is_idk(loc):
        return "idk_mismatch"
    r = similarity(lf, loc)
    if r >= 0.55:
        return "similar"
    if r >= 0.35:
        return "partial"
    return "divergent"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "export",
        nargs="?",
        default=str(ROOT / "1773852770451-lf-events-export-cmmn9l5gq019kad07u4o41lxz.json"),
    )
    ap.add_argument("--max", type=int, default=0, help="Max unique queries (0=all)")
    args = ap.parse_args()

    path = Path(args.export)
    if not path.is_file():
        print("Missing:", path, file=sys.stderr)
        sys.exit(1)

    events = json.loads(path.read_text(encoding="utf-8"))
    pairs = extract_langfuse_qa(events)
    if args.max and args.max > 0:
        pairs = pairs[: args.max]

    kb_answer = load_module("kba_replay", ROOT / "kb_answer.py")
    chunks_path = ROOT / "kb" / "kb_chunks.jsonl"
    chunks = []
    with open(chunks_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    kb_answer._load_chunks = lambda ctx: chunks

    ctx = CursorKBTestContext()
    rows = []
    for i, (query, lf_ans) in enumerate(pairs):
        if (i + 1) % 50 == 0:
            print(f"... {i+1}/{len(pairs)}", file=sys.stderr)
        try:
            out = kb_answer.kb_answer({"query": query}, context=ctx)
            loc = str((out or {}).get("answer") or "")
        except Exception as ex:
            loc = f"__ERROR__ {ex}"
        cat = classify(lf_ans, loc) if not loc.startswith("__ERROR__") else "error"
        sim = similarity(lf_ans, loc) if loc and not loc.startswith("__ERROR__") else 0.0
        rows.append(
            {
                "query": query,
                "langfuse_answer_preview": (lf_ans[:400] + "…") if len(lf_ans) > 400 else lf_ans,
                "local_answer_preview": (loc[:400] + "…") if len(loc) > 400 else loc,
                "similarity": round(sim, 3),
                "bucket": cat,
            }
        )

    from collections import Counter

    buckets = Counter(r["bucket"] for r in rows)
    sims = [r["similarity"] for r in rows if r["bucket"] not in ("error",)]
    avg_sim = sum(sims) / len(sims) if sims else 0.0

    summary = {
        "export_file": str(path.name),
        "unique_queries_tested": len(rows),
        "buckets": dict(buckets),
        "mean_similarity_all_pairs": round(avg_sim, 3),
        "note": "similarity is token/char overlap; 'similar' bucket uses 0.55 threshold on full text.",
    }

    out_path = ARTIFACTS / f"langfuse_replay_{path.stem[:20]}.json"
    ARTIFACTS.mkdir(exist_ok=True)
    out_path.write_text(
        json.dumps({"summary": summary, "results": rows}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    print("Wrote:", out_path)


if __name__ == "__main__":
    main()
