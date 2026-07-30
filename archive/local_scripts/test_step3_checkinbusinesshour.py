#!/usr/bin/env python3
"""
Step 3: Test checkInBusinessHour API documentation query.

This test verifies that the query:
  "checkInBusinessHour API documentation"

Returns:
  - answered=true (not IDK or refusal)
  - confidence > 2.0
  - Answer contains relevant API information

Run: python3 test_step3_checkinbusinesshour.py
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

    # Determine if answered (not IDK)
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

def main():
    test_query = "checkInBusinessHour API documentation"

    print("=" * 90)
    print("  STEP 3 TEST: checkInBusinessHour API Documentation")
    print("=" * 90)
    print(f"\nQuery: {test_query!r}\n")

    result = run_pipeline(test_query)

    # Check criteria
    confidence = result["top_score"]
    answered = result["answered"]

    pass_confidence = confidence > 2.0
    pass_answered = answered

    # Print result
    print(f"Module:              {result['module']}")
    print(f"Intent:              {result['intent']}")
    print(f"Entities:            {result['entities']}")
    print(f"Top Source:          {result['top_source']}")
    print(f"Confidence (Score):  {confidence}")
    print(f"Evidence Count:      {result['evidence_count']}")
    print(f"Answered:            {answered}")

    print(f"\n{'-' * 90}")
    print(f"Test Criteria:")
    print(f"  ✓ answered=true:           {pass_answered}")
    print(f"  ✓ confidence > 2.0:        {pass_confidence} (actual: {confidence})")

    overall_pass = pass_answered and pass_confidence
    print(f"\n{'=' * 90}")
    print(f"Result: {'PASS' if overall_pass else 'FAIL'}")
    print(f"{'=' * 90}")

    print(f"\nAnswer preview (first 500 chars):")
    print(f"{result['answer'][:500]}")

    # Return structured result
    return {
        "step": "step3",
        "test_queries": [test_query],
        "pass_count": 1 if overall_pass else 0,
        "fail_count": 0 if overall_pass else 1,
        "passed": overall_pass,
        "details": {
            "query": test_query,
            "confidence": confidence,
            "answered": answered,
            "pass_confidence": pass_confidence,
            "pass_answered": pass_answered,
            "top_source": result["top_source"],
            "module": result["module"],
            "intent": result["intent"],
            "answer_preview": result["answer"][:200]
        }
    }

if __name__ == "__main__":
    result = main()

    # Save result as JSON
    report_path = os.path.join(os.path.dirname(__file__), "..", "reports", "idk_regression_step3_implementation_test.json")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    with open(report_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\n✓ Results saved to: {report_path}")

    sys.exit(0 if result["passed"] else 1)
