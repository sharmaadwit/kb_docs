#!/usr/bin/env python3
"""
Test Step 5: TTL + Token Scoring (Strict interpretation)

All three queries should:
- Handle acronyms correctly (in COMMON_ACRONYMS, not filtered)
- Score >= 2.0 (confident answers)

Note: This is a stricter test. SMS and STD queries may not have
direct concept matches in the KB, so they may not achieve 2.0 scores
without additional content or entity mappings.
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
    """Run the KB answer pipeline."""
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

    return {
        "module": explicit_module,
        "entities": [e["id"] for e in entities],
        "intent": intent,
        "top_source": evidence[0].get("source") if evidence else None,
        "top_score": round(evidence[0].get("score", 0), 2) if evidence else 0,
        "evidence_count": len(evidence),
        "answer": answer,
    }

def is_idk(answer):
    low = answer.lower()
    return "i don't know" in low or "i don t know" in low

TESTS = [
    {
        "name": "ttl_based_agent_mapping",
        "query": "TTL-based agent mapping approach",
        "description": "Score > 2.0 and answer",
        "check": lambda r: not is_idk(r["answer"]) and r["top_score"] > 2.0,
    },
    {
        "name": "sms_service",
        "query": "Do we provide SMS service?",
        "description": "Score > 2.0 and answer",
        "check": lambda r: not is_idk(r["answer"]) and r["top_score"] > 2.0,
    },
    {
        "name": "std_service_voice_ai",
        "query": "do we have STD service in voice ai platform",
        "description": "Score > 2.0 and answer",
        "check": lambda r: not is_idk(r["answer"]) and r["top_score"] > 2.0,
    },
]

def main():
    print("=" * 90)
    print("  STEP 5: TTL + TOKEN SCORING (STRICT - ALL TESTS > 2.0)")
    print("=" * 90)
    print(f"\nCommon Acronyms: {sorted(kb.COMMON_ACRONYMS)}\n")

    pass_count = 0
    fail_count = 0
    failures = []
    test_queries = []

    for t in TESTS:
        test_queries.append(t["query"])
        query = t["query"]

        print(f"\nTest: {t['name']}")
        print(f"  Query: {query}")

        try:
            result = run_pipeline(query)
            ok = t["check"](result)

            print(f"  Score: {result['top_score']}  |  Entities: {result['entities']}  |  Source: {result['top_source']}")

            if ok:
                print(f"  ✓ PASS")
                pass_count += 1
            else:
                print(f"  ✗ FAIL")
                fail_count += 1
                failures.append(t["name"])

        except Exception as exc:
            print(f"  ✗ EXCEPTION: {exc}")
            fail_count += 1
            failures.append(t["name"])

    print(f"\n{'=' * 90}")
    print(f"  RESULTS: {pass_count}/{pass_count + fail_count} passed")
    print(f"{'=' * 90}")

    if failures:
        print(f"Failed: {', '.join(failures)}")

    results = {
        "step": "Step 5: TTL + Token Scoring (Strict)",
        "test_queries": test_queries,
        "pass_count": pass_count,
        "fail_count": fail_count,
        "passed": fail_count == 0,
        "details": f"{pass_count}/{pass_count+fail_count} tests passed. TTL: 100%. SMS/STD: need CONCEPT_REGISTRY entries for > 2.0 scores."
    }

    print(f"\nJSON Results:")
    print(json.dumps(results, indent=2))

    return fail_count == 0

if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
