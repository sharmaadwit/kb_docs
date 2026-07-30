#!/usr/bin/env python3
"""Fetch CC Express traces from Langfuse and compare against equivalent Console
traces to verify the silent-alias change produces identical answers.

Analytics-only. This script NEVER edits skill code. It reads live Langfuse data
and (optionally) re-runs the local kb_answer pipeline to compare CC Express vs
Console phrasings of the same question.

Modes
-----
1. --mode live   (default): pull the last N CC Express traces from Langfuse,
   strip the "CC Express" product mention, find/synthesize an equivalent Console
   query, and re-run BOTH through the local kb_answer pipeline. Compare answer
   body, confidence, intent, module. This is the authoritative "are they
   identical now?" check because it exercises the *current* code.

2. --mode langfuse-only: pull CC Express traces AND Console traces from Langfuse
   and pair them by normalized query (no local pipeline run). Useful to inspect
   what production has historically returned.

Usage
-----
  python3 local/scripts/fetch_and_compare_cc_express_traces.py
  python3 local/scripts/fetch_and_compare_cc_express_traces.py --limit 100
  python3 local/scripts/fetch_and_compare_cc_express_traces.py --mode langfuse-only
  python3 local/scripts/fetch_and_compare_cc_express_traces.py --tolerance 0.0

Output
------
  local/reports/cc_express_compare_<mode>.json
  prints a summary table + side-by-side diff for any mismatch.

Pass criteria (default): zero answer-body mismatches and confidence delta within
--tolerance (default 0.0, i.e. exact). Intent + module must match exactly.
"""
from __future__ import annotations

import argparse
import base64
import difflib
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill"))

# Case-insensitive removal of the CC Express product mention so we can derive
# the "neutral" / Console-equivalent question from a CC Express trace.
_CC_EXPRESS_RE = re.compile(r"\b(in\s+|on\s+|using\s+)?cc\s*express\b[,:]?", re.IGNORECASE)
_MULTISPACE_RE = re.compile(r"\s{2,}")


# ---------------------------------------------------------------------------
# Env + Langfuse fetch
# ---------------------------------------------------------------------------
def _load_env() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())


def _lf_headers() -> dict | None:
    _load_env()
    pub = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
    sec = os.environ.get("LANGFUSE_SECRET_KEY", "")
    if not pub or not sec:
        print("ERROR: LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY not set in .env")
        return None
    creds = base64.b64encode(f"{pub}:{sec}".encode()).decode()
    return {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}


def _lf_host() -> str:
    return os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")


def fetch_traces(days: int = 90, max_items: int = 5000) -> list[dict]:
    headers = _lf_headers()
    if headers is None:
        return []
    host = _lf_host()
    from_ts = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")
    out: list[dict] = []
    page = 1
    while True:
        params = urllib.parse.urlencode({"page": page, "limit": 100, "fromTimestamp": from_ts})
        url = f"{host}/api/public/traces?{params}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read())
        except Exception as e:
            print(f"ERROR fetching page {page}: {e}")
            break
        batch = body.get("data", [])
        out.extend(batch)
        meta = body.get("meta", {})
        total = meta.get("totalItems", meta.get("total", len(out)))
        print(f"  page {page}: {len(batch)} traces (seen {len(out)} / {total})")
        if not batch or len(out) >= total or len(out) >= max_items:
            break
        page += 1
    return out


# ---------------------------------------------------------------------------
# Trace field extraction
# ---------------------------------------------------------------------------
def _trace_query(trace: dict) -> str | None:
    """Prefer the original user query from metadata, fall back to input/name."""
    meta = trace.get("metadata") or {}
    if isinstance(meta, dict):
        q = meta.get("query")
        if isinstance(q, str) and len(q) > 2:
            return q
    val = trace.get("input")
    if isinstance(val, str) and len(val) > 2:
        return val
    if isinstance(val, dict):
        for sub in ("query", "question", "message", "text", "content"):
            v = val.get(sub)
            if isinstance(v, str) and len(v) > 2:
                return v
    name = trace.get("name")
    if isinstance(name, str) and len(name) > 2:
        return name
    return None


def _trace_meta(trace: dict) -> dict:
    m = trace.get("metadata")
    return m if isinstance(m, dict) else {}


def _is_cc_express_trace(trace: dict) -> bool:
    q = (_trace_query(trace) or "").lower()
    meta = _trace_meta(trace)
    detected = str(meta.get("detected_product_original") or "").lower()
    intents = meta.get("intent_labels") or []
    if "cc express" in q or "ccexpress" in q or "cc_express" in q:
        return True
    if "cc_express" in detected or "cc express" in detected:
        return True
    if any("cc_express" in str(i).lower() for i in intents):
        return True
    return False


def strip_cc_express(query: str) -> str:
    """Remove the CC Express product mention to derive the neutral question."""
    q = _CC_EXPRESS_RE.sub(" ", query or "")
    q = _MULTISPACE_RE.sub(" ", q).strip(" ,:")
    return q.strip()


def _normalize_for_pairing(query: str) -> str:
    q = (query or "").lower()
    q = _CC_EXPRESS_RE.sub(" ", q)
    q = re.sub(r"\bconsole\b", " ", q)
    q = re.sub(r"\bconversation cloud\b", " ", q)
    q = re.sub(r"[^a-z0-9]+", " ", q)
    return _MULTISPACE_RE.sub(" ", q).strip()


# ---------------------------------------------------------------------------
# Local pipeline (authoritative re-run of CURRENT code)
# ---------------------------------------------------------------------------
def _setup_local_kb():
    import kb_storage
    import kb_answer

    chunks_path = ROOT / "kb" / "kb_chunks.jsonl"
    chunks = [json.loads(l) for l in chunks_path.read_text(encoding="utf-8").splitlines() if l.strip()]

    def _read_json_local(path, context=None):
        p = ROOT / path if not str(path).startswith("/") else Path(path)
        return json.loads(p.read_text(encoding="utf-8"))

    captured = {"last": {}}

    def _cap_lf(trace_name, query, answer, results, explicit_module, intents,
                selected_answer_mode, clarification_asked, latency_ms, context,
                params=None, video_meta=None, **kwargs):
        captured["last"] = {
            "top_source": results[0].get("source") if results else None,
            "top_score": results[0].get("score") if results else None,
            "source_count": len(results),
            "mode": selected_answer_mode,
            "intents": list(intents or []),
            "module": explicit_module,
            # surface the new alias-tracking fields if the skill change is live
            "detected_product_original": kwargs.get("detected_product_original"),
            "original_query": kwargs.get("original_query"),
        }
        return {}

    kb_answer._load_chunks = lambda ctx=None: chunks
    kb_answer._send_langfuse = _cap_lf
    kb_storage.read_json = _read_json_local
    try:
        import kb_video
        kb_video.record_video_delivery = lambda *a, **k: None
    except Exception:
        pass

    class Ctx:
        def get_secret(self, name):
            return None

    return kb_answer, Ctx(), captured


def _run_local(kb_answer, ctx, captured, query: str) -> dict:
    try:
        res = kb_answer.kb_answer(parameters={"query": query}, context=ctx)
        ans = str(res.get("answer") or "")
    except Exception as exc:
        ans = ""
        captured["last"] = {"error": str(exc)}
    meta = dict(captured.get("last", {}))
    return {
        "query": query,
        "answer": ans,
        "confidence": meta.get("top_score"),
        "intent_mode": meta.get("mode"),
        "intents": meta.get("intents"),
        "module": meta.get("module"),
        "top_source": meta.get("top_source"),
        "detected_product_original": meta.get("detected_product_original"),
    }


def _answers_match(a: str, b: str) -> bool:
    return (a or "").strip() == (b or "").strip()


def _conf_delta(a, b) -> float | None:
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(float(a) - float(b))
    if a is None and b is None:
        return 0.0
    return None


def _diff_snippet(a: str, b: str, n: int = 20) -> list[str]:
    a_lines = (a or "").splitlines()
    b_lines = (b or "").splitlines()
    diff = list(difflib.unified_diff(a_lines, b_lines, "cc_express", "console", lineterm=""))
    return diff[:n]


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------
def run_live(limit: int, days: int, tolerance: float) -> dict:
    print(f"Fetching last {days}d of Langfuse traces to find CC Express queries...")
    traces = fetch_traces(days=days)
    cc_traces = [t for t in traces if _is_cc_express_trace(t)]
    # de-dup by original query, keep newest first ordering from API
    seen: set[str] = set()
    cc_queries: list[str] = []
    for t in cc_traces:
        q = _trace_query(t)
        if not q:
            continue
        key = q.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        cc_queries.append(q)
        if len(cc_queries) >= limit:
            break

    print(f"CC Express traces: {len(cc_traces)}  unique queries: {len(cc_queries)}")
    if not cc_queries:
        print("No CC Express traces found. Nothing to compare.")
        return {"mode": "live", "pairs": [], "summary": {"total": 0}}

    kb_answer, ctx, captured = _setup_local_kb()
    rows = []
    mismatches = 0
    for cc_q in cc_queries:
        neutral = strip_cc_express(cc_q)
        console_q = f"In Console, {neutral}" if neutral else "Console"
        cc_res = _run_local(kb_answer, ctx, captured, cc_q)
        con_res = _run_local(kb_answer, ctx, captured, console_q)

        same_answer = _answers_match(cc_res["answer"], con_res["answer"])
        cd = _conf_delta(cc_res["confidence"], con_res["confidence"])
        conf_ok = cd is not None and cd <= tolerance
        intent_ok = cc_res["intents"] == con_res["intents"]
        module_ok = cc_res["module"] == con_res["module"]
        ok = same_answer and conf_ok and intent_ok and module_ok
        if not ok:
            mismatches += 1
        rows.append({
            "cc_query": cc_q,
            "console_query": console_q,
            "identical_answer": same_answer,
            "confidence_delta": cd,
            "intent_match": intent_ok,
            "module_match": module_ok,
            "pass": ok,
            "cc_product_tag": cc_res["detected_product_original"],
            "console_product_tag": con_res["detected_product_original"],
            "cc_confidence": cc_res["confidence"],
            "console_confidence": con_res["confidence"],
            "cc_intents": cc_res["intents"],
            "console_intents": con_res["intents"],
            "cc_module": cc_res["module"],
            "console_module": con_res["module"],
            "diff": [] if same_answer else _diff_snippet(cc_res["answer"], con_res["answer"]),
            "cc_answer_preview": cc_res["answer"][:200],
            "console_answer_preview": con_res["answer"][:200],
        })

    summary = {
        "total": len(rows),
        "mismatches": mismatches,
        "pass": mismatches == 0,
        "tolerance": tolerance,
        "tag_distribution_cc": dict(Counter(r["cc_product_tag"] for r in rows)),
        "tag_distribution_console": dict(Counter(r["console_product_tag"] for r in rows)),
    }
    return {"mode": "live", "rows": rows, "summary": summary}


def run_langfuse_only(limit: int, days: int) -> dict:
    print(f"Fetching last {days}d of Langfuse traces (langfuse-only pairing)...")
    traces = fetch_traces(days=days)
    cc, console = {}, {}
    for t in traces:
        q = _trace_query(t)
        if not q:
            continue
        meta = _trace_meta(t)
        rec = {
            "query": q,
            "answer": meta.get("answer_preview") or "",
            "confidence": meta.get("confidence"),
            "intents": meta.get("intent_labels"),
            "module": meta.get("module_label"),
            "trace_id": t.get("id"),
        }
        key = _normalize_for_pairing(q)
        if _is_cc_express_trace(t):
            cc.setdefault(key, rec)
        elif "console" in q.lower() or "conversation cloud" in q.lower():
            console.setdefault(key, rec)

    rows = []
    for key, cc_rec in list(cc.items())[:limit]:
        con_rec = console.get(key)
        if not con_rec:
            rows.append({"normalized_key": key, "cc": cc_rec, "console": None, "paired": False})
            continue
        same = _answers_match(cc_rec["answer"], con_rec["answer"])
        rows.append({
            "normalized_key": key,
            "cc": cc_rec,
            "console": con_rec,
            "paired": True,
            "identical_answer_preview": same,
            "diff": [] if same else _diff_snippet(cc_rec["answer"], con_rec["answer"]),
        })
    paired = [r for r in rows if r["paired"]]
    summary = {
        "cc_unique": len(cc),
        "console_unique": len(console),
        "paired": len(paired),
        "unpaired_cc": len(cc) - len(paired),
        "identical_among_paired": sum(1 for r in paired if r.get("identical_answer_preview")),
    }
    return {"mode": "langfuse-only", "rows": rows, "summary": summary}


# ---------------------------------------------------------------------------
def _print_live(report: dict) -> None:
    s = report["summary"]
    print(f"\n=== CC Express vs Console (live local re-run) ===")
    print(f"pairs={s['total']}  mismatches={s['mismatches']}  PASS={s['pass']}  tolerance={s['tolerance']}")
    print(f"cc tags: {s['tag_distribution_cc']}")
    print(f"console tags: {s['tag_distribution_console']}")
    print(f"\n{'identical':<11}{'conf_d':<8}{'intent':<8}{'module':<8}{'pass':<6}query")
    for r in report["rows"]:
        cd = r["confidence_delta"]
        cd = f"{cd:.3f}" if isinstance(cd, (int, float)) else "-"
        print(f"{str(r['identical_answer']):<11}{cd:<8}{str(r['intent_match']):<8}"
              f"{str(r['module_match']):<8}{str(r['pass']):<6}{r['cc_query'][:60]}")
    for r in report["rows"]:
        if not r["pass"]:
            print(f"\n--- MISMATCH ---\n  CC:      {r['cc_query']}\n  Console: {r['console_query']}")
            for line in r["diff"]:
                print(f"    {line}")


def _print_langfuse_only(report: dict) -> None:
    s = report["summary"]
    print(f"\n=== CC Express vs Console (langfuse-only pairing) ===")
    print(json.dumps(s, indent=2))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["live", "langfuse-only"], default="live")
    ap.add_argument("--limit", type=int, default=100, help="max CC Express queries to compare")
    ap.add_argument("--days", type=int, default=90, help="Langfuse lookback window")
    ap.add_argument("--tolerance", type=float, default=0.0,
                    help="max allowed confidence delta for a pair to pass (live mode)")
    args = ap.parse_args()

    if args.mode == "live":
        report = run_live(args.limit, args.days, args.tolerance)
        _print_live(report)
    else:
        report = run_langfuse_only(args.limit, args.days)
        _print_langfuse_only(report)

    out = ROOT / "local" / "reports" / f"cc_express_compare_{args.mode}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, default=str, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out}")

    # Non-zero exit on failure so CI / shell can gate on it.
    if args.mode == "live" and not report["summary"].get("pass", False):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
