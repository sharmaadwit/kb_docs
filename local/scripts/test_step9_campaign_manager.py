#!/usr/bin/env python3
"""
Step 9: Test Campaign Manager prompts coverage.

Verifies these queries each:
  1. "Campaign Manager prompts available in Gupshup Console" (original IDK case)
  2. "What prompts are available in Campaign Manager?"
  3. "Campaign Manager features and templates"
  4. "Can I create custom campaign prompts?"

Pass criteria per query:
  - answered=true (not IDK or refusal)
  - confidence (top evidence score) > 2.0
  - top_source contains "campaign-manager"

Run: python3 local/scripts/test_step9_campaign_manager.py

Analytics-only harness: drives the existing kb_answer pipeline with local
chunks. Never modifies skill code.
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "skill"))
import kb_answer as kb

CHUNKS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "kb", "kb_chunks.jsonl")


def _local_chunks():
    items = []
    with open(CHUNKS_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    items.append(json.loads(line))
                except Exception:
                    pass
    return items


CACHED_CHUNKS = _local_chunks()


def run_pipeline(query):
    guardrail = kb._guardrail_answer(query)
    if guardrail:
        return {
            "module": "General",
            "entities": [],
            "intent": "refusal",
            "top_source": None,
            "top_score": 0,
            "evidence_count": 0,
            "answer": guardrail,
            "answered": False,
        }

    chunks = CACHED_CHUNKS
    explicit_module = kb._detect_module(query)
    entities = kb._extract_entities(query)
    intent = kb._classify_intent(query, entities)

    scored = []
    threshold = getattr(kb, 'MIN_CHUNK_SCORE', 0.0)
    for c in chunks:
        s = kb._score_chunk(query, c, entities, explicit_module)
        if threshold > 0 and s < threshold:
            continue
        elif threshold == 0 and s <= 0:
            continue
        row = dict(c)
        row["score"] = s
        scored.append(row)
    scored.sort(key=lambda x: x.get("score", 0.0), reverse=True)

    evidence = kb._select_evidence(query, scored, intent, explicit_module)
    answer = kb._compose_answer(query, intent, entities, evidence, explicit_module)

    is_idk = "i don't know" in answer.lower() or "i don t know" in answer.lower()
    is_refusal = any(s in answer.lower() for s in [
        "i can help only", "sensitive", "cannot help", "i can t help", "i can't help"
    ])
    answered = not (is_idk or is_refusal)

    return {
        "module": explicit_module,
        "entities": [e["id"] for e in entities],
        "intent": intent,
        "top_source": evidence[0].get("source") if evidence else None,
        "top_score": round(evidence[0].get("score", 0), 2) if evidence else 0,
        "evidence_count": len(evidence),
        "answer": answer,
        "answered": answered,
    }


TEST_QUERIES = [
    "Campaign Manager prompts available in Gupshup Console",
    "What prompts are available in Campaign Manager?",
    "Campaign Manager features and templates",
    "Can I create custom campaign prompts?",
]


def evaluate(query):
    result = run_pipeline(query)
    confidence = result["top_score"]
    answered = result["answered"]
    top_source = result["top_source"] or ""

    pass_confidence = confidence > 2.0
    pass_answered = answered
    pass_source = "campaign-manager" in top_source

    overall = pass_confidence and pass_answered and pass_source

    return {
        "query": query,
        "confidence": confidence,
        "answered": answered,
        "pass_confidence": pass_confidence,
        "pass_answered": pass_answered,
        "pass_source": pass_source,
        "passed": overall,
        "top_source": top_source or None,
        "module": result["module"],
        "intent": result["intent"],
        "evidence_count": result["evidence_count"],
        "answer_preview": result["answer"][:200],
    }


def main():
    print("=" * 90)
    print("  STEP 9 TEST: Campaign Manager prompts")
    print("=" * 90)

    details = []
    pass_count = 0
    for q in TEST_QUERIES:
        r = evaluate(q)
        details.append(r)
        if r["passed"]:
            pass_count += 1
        print(f"\nQuery: {q!r}")
        print(f"  module           : {r['module']}")
        print(f"  intent           : {r['intent']}")
        print(f"  top_source       : {r['top_source']}")
        print(f"  confidence       : {r['confidence']} (>2.0 -> {r['pass_confidence']})")
        print(f"  answered         : {r['answered']} (-> {r['pass_answered']})")
        print(f"  source campaign-manager? {r['pass_source']}")
        print(f"  PASS             : {r['passed']}")

    fail_count = len(TEST_QUERIES) - pass_count
    passed = fail_count == 0

    print(f"\n{'=' * 90}")
    print(f"Result: {pass_count}/{len(TEST_QUERIES)} passed -> {'PASS' if passed else 'FAIL'}")
    print(f"{'=' * 90}")

    return {
        "step": "step9",
        "test_queries": TEST_QUERIES,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "passed": passed,
        "details": details,
    }


if __name__ == "__main__":
    result = main()

    report_path = os.path.join(
        os.path.dirname(__file__), "..", "reports", "idk_regression_step9_test.json"
    )
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nResults saved to: {report_path}")
    sys.exit(0 if result["passed"] else 1)
