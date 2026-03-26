#!/usr/bin/env python3
"""Local asserts for kb_answer output policy (no separate policy module)."""
import json
import os
import sys

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_SCRIPT_DIR = os.path.dirname(__file__)
sys.path.insert(0, _ROOT)
sys.path.insert(0, _SCRIPT_DIR)

import kb_answer as kba  # noqa: E402
from cursor_test_context import CursorKBTestContext  # noqa: E402


def assert_true(cond, msg):
    if not cond:
        raise AssertionError(msg)


def test_policy_functions():
    long = "Intro line\n" + "\n".join(f"- bullet {i}" for i in range(12))
    capped = kba._apply_faq_summary_cap(long)
    bullet_lines = [L for L in capped.split("\n") if kba._FAQ_BULLET_LINE_RE.match(L)]
    assert_true(len(bullet_lines) <= kba.FAQ_SUMMARY_MAX_BULLETS, f"bullets {len(bullet_lines)}")

    out, meta = kba._apply_answer_policy("Short ok.", "What is X?", {})
    assert_true("Need more detail" in out, "followup on substantive short answer")
    assert_true(meta.get("applied") is True, meta)

    out2, meta2 = kba._apply_answer_policy(
        "I can help only with documented Gupshup Console.", "hi", {}
    )
    assert_true("Need more detail" not in out2, "no followup on refusal")
    assert_true(meta2.get("mode") == "skipped_guardrail_or_idk", meta2)

    out3, meta3 = kba._apply_answer_policy(long, "Tell me more detail about api node", {})
    assert_true(meta3.get("mode") == "full_query_phrase", meta3)
    assert_true("Need more detail" not in out3, "phrase bypass")

    out4, meta4 = kba._apply_answer_policy(long, "x", {"answer_depth": "full"})
    assert_true(meta4.get("mode") == "full_param", meta4)


def test_kb_answer_integration():
    import importlib.util
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    spec = importlib.util.spec_from_file_location("kba_t", root / "kb_answer.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    chunks_path = root / "kb" / "kb_chunks.jsonl"
    if not chunks_path.is_file():
        print("SKIP integration: no kb_chunks.jsonl")
        return

    chunks = []
    with open(chunks_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    mod._load_chunks = lambda ctx: chunks

    ctx = CursorKBTestContext()

    r = mod.kb_answer({"query": "What is api node in Bot Studio?"}, context=ctx)
    assert_true(r.get("answer_policy", {}).get("version") == mod.ANSWER_POLICY_VERSION, r)
    assert_true("Need more detail" in (r.get("answer") or ""), "kb_answer applies policy")

    r2 = mod.kb_answer(
        {"query": "What is api node in Bot Studio?", "answer_depth": "full"},
        context=ctx,
    )
    assert_true(
        "Need more detail" not in (r2.get("answer") or ""),
        "full depth skips followup",
    )


if __name__ == "__main__":
    test_policy_functions()
    print("ok: kb_answer policy unit checks")
    test_kb_answer_integration()
    print("ok: kb_answer integration (if chunks present)")
    print("ALL OK")
