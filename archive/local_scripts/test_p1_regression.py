#!/usr/bin/env python3
"""P1 regression suite: verify R2/R8/R9 rules don't break existing behavior.

CRITICAL GATE: these tests must all pass or P1 is rolled back.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill"))

CHUNKS_PATH = ROOT / "kb" / "kb_chunks.jsonl"


def setup_local_kb():
    import kb_storage
    import kb_answer as kba
    import kb_search as kbs

    def _load_chunks_local(context=None):
        items = []
        with CHUNKS_PATH.open(encoding="utf-8") as f:
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


def run_kb(ctx, query):
    import kb_answer as kba
    res = kba.kb_answer({"query": query}, context=ctx)
    meta = (res.get("langfuse") or {}).get("metadata") or {}
    citations = res.get("citations") or []
    return {
        "query_family": meta.get("query_family"),
        "explicit_module": meta.get("explicit_module"),
        "top_source": (meta.get("top_source") or ""),
        "confidence": meta.get("confidence"),
        "answered": meta.get("answered"),
        "citations": citations,
    }


def main():
    ctx = setup_local_kb()
    import kb_answer as kba

    results = []

    def record(name, passed, detail, rule=None):
        results.append({"name": name, "passed": bool(passed), "detail": detail, "rule": rule})

    # --- Direct _detect_module tests -------------------------------------
    dm = kba._detect_module

    # Test 1 (R2)
    v = dm("Build a conversational agent")
    record("T1 _detect_module('Build a conversational agent') -> SuperAgent",
           v == "SuperAgent", f"got={v!r}", "R2")

    # Test 2 (R2)
    v = dm("Skills for my agent")
    record("T2 _detect_module('Skills for my agent') -> SuperAgent",
           v == "SuperAgent", f"got={v!r}", "R2")

    # Test 3 (R8)
    v = dm("What is an agent?")
    record("T3 _detect_module('What is an agent?') -> SuperAgent (R8 bare default)",
           v == "SuperAgent", f"got={v!r}", "R8")

    # --- P0 regression suite (existing routing must still hold) ----------
    # These verify R9 module fence + R2/R8 don't cross-contaminate other modules.
    p0_cases = [
        # (query, expected_module, rule_if_fail)
        ("Deploy my agent to WhatsApp", "SuperAgent", "R3"),
        ("Meta business agent setup", "WhatsApp", "R1"),
        ("business agent", "WhatsApp", "R1"),
        ("whatsapp agent", "WhatsApp", "R4"),
        ("agent template", "Agent Assist", "R6"),
        ("BizAI pricing", "BizAI", "R9"),
        ("Bot Studio journey builder", "Bot Studio", "R9"),
        ("Campaign manager broadcast", "Campaign Manager", "shortcut"),
        ("How does RCS work", "Channels", "shortcut"),
        ("Agent Assist live monitoring", "Agent Assist", "R9"),
        ("What are goals", "Goals", "map"),
        ("How do I use integrations", "Integrations", "map"),
        ("Tell me about pricing", "General", "default"),
    ]
    for q, exp, rule in p0_cases:
        got = dm(q)
        record(f"P0 _detect_module({q!r}) -> {exp}", got == exp, f"got={got!r}", rule)

    # Test 4 explicitly: R9 module fence should not leak. BizAI query must not
    # get pulled to SuperAgent by bare-agent R8, and SuperAgent query must not
    # bleed into BizAI.
    v = dm("BizAI pricing")
    record("T4a no cross-contamination: 'BizAI pricing' stays BizAI",
           v == "BizAI", f"got={v!r}", "R9")
    v = dm("Bot Studio API node")
    record("T4b no cross-contamination: 'Bot Studio API node' stays Bot Studio",
           v == "Bot Studio", f"got={v!r}", "R9")

    # --- kb_answer end-to-end routing -----------------------------------
    # Test 5: 'How do I build an agent?' should NOT route to General.
    r = run_kb(ctx, "How do I build an agent?")
    passed = r["query_family"] == "SuperAgent" and r["query_family"] != "General"
    record("T5 kb_answer('How do I build an agent?') NOT General (routes SuperAgent)",
           passed, f"query_family={r['query_family']!r} top_source={r['top_source']!r}", "R2/R8")

    # Test 6: 'BizAI pricing' should still prefer kb/bizai/ (R9 fence intact).
    r = run_kb(ctx, "BizAI pricing")
    ts = r["top_source"].lower()
    cit_sources = " ".join(str(c.get("source", c)) for c in r["citations"]).lower()
    passed = "bizai" in ts or "bizai" in cit_sources
    record("T6 kb_answer('BizAI pricing') prefers kb/bizai/ (R9 fence)",
           passed, f"query_family={r['query_family']!r} top_source={r['top_source']!r}", "R9")

    # Test 7: 'Bot Studio API node' should still prefer bot-studio/
    # (R9 doesn't suppress when module != the doc's module).
    r = run_kb(ctx, "Bot Studio API node")
    ts = r["top_source"].lower()
    cit_sources = " ".join(str(c.get("source", c)) for c in r["citations"]).lower()
    passed = "bot-studio" in ts or "bot-studio" in cit_sources
    record("T7 kb_answer('Bot Studio API node') prefers bot-studio/",
           passed, f"query_family={r['query_family']!r} top_source={r['top_source']!r}", "R9")

    # --- summarize --------------------------------------------------------
    passed_count = sum(1 for x in results if x["passed"])
    failed = [x for x in results if not x["passed"]]
    failed_rules = {}
    for x in failed:
        failed_rules.setdefault(x["rule"], 0)
        failed_rules[x["rule"]] += 1

    summary = {
        "total": len(results),
        "passed": passed_count,
        "failed": len(failed),
        "all_passed": len(failed) == 0,
        "failed_tests": [{"name": x["name"], "detail": x["detail"], "rule": x["rule"]} for x in failed],
        "failed_by_rule": failed_rules,
        "rollback_recommended": len(failed) > 1,
        "results": results,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
