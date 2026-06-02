"""
Test harness for the 6 misroute cases.
Loads chunks locally and runs each query through the internal pipeline.
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

MISROUTE_CASES = [
    {
        "label": "Case 1: Agent Assist feature usage -> WhatsApp Flow Node",
        "query": "How do I use the Agent Assist feature in Gupshup Console? Provide practical step-by-step guidance for getting started, key setup flow, and common usage patterns.",
        "bad_signals": ["whatsapp flow node", "whatsapp flow"],
    },
    {
        "label": "Case 2: Agent Assist APIs -> Sending Marketing Templates",
        "query": "List Gupshup Agent Assist APIs. Include API names/endpoints if documented, what each API is used for, and mention if the docs do not expose public endpoint details.",
        "bad_signals": ["sending marketing templates"],
    },
    {
        "label": "Case 3: SR panels -> AI Agents framework",
        "query": "How do SR panels work in Gupshup? What are SR panels and how are they used?",
        "bad_signals": ["agentic framework", "ai agents", "elevating customer"],
    },
    {
        "label": "Case 4: Dynamic link tracking -> Campaign Analytics",
        "query": "In Gupshup Console Campaign Manager documentation, how do users send campaigns using dynamic link tracking or tracked dynamic links? Please answer specifically for Campaign Manager, including setup steps, prerequisites, how dynamic links are inserted into campaign messages, what gets tracked, reporting/analytics behavior, and any documented limitations.",
        "bad_signals": ["campaign analytics"],
    },
    {
        "label": "Case 5: Template dynamic link -> Modify Variable Node",
        "query": "In Gupshup Console documentation, when creating a template, how do users use a dynamic link? Please explain the documented setup flow, where dynamic links are configured during template creation, prerequisites, variable usage, and any limitations. If the docs do not clearly document it, say what is supported and what remains unclear.",
        "bad_signals": ["modify variable node"],
    },
    {
        "label": "Case 6: Postback JSON array parsing -> Clear Context Node",
        "query": 'In Gupshup Console Journey Builder, how do I handle postback text that arrives like ["CUSTFEED", "81bc9d2a4dd1ceaee1c8dd3aed7f0fc5ac705a6df5"] inside a JSON Handler node? I want to parse the array, access the first and second values, and branch based on them.',
        "bad_signals": ["clear context node"],
    },
]


def run_pipeline(query):
    chunks = CACHED_CHUNKS
    explicit_module = kb._detect_module(query)
    entities = kb._extract_entities(query)
    intent = kb._classify_intent(query, entities)

    scored = []
    for c in chunks:
        s = kb._score_chunk(query, c, entities, explicit_module)
        threshold = getattr(kb, 'MIN_CHUNK_SCORE', 0.0)
        if s <= threshold and threshold == 0.0:
            continue
        if threshold > 0.0 and s < threshold:
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


def check_misroute(answer, bad_signals):
    low = answer.lower()
    for sig in bad_signals:
        if sig.lower() in low:
            return True
    return False


def main():
    print("=" * 80)
    print("MISROUTE TEST HARNESS")
    print("=" * 80)

    passed = 0
    failed = 0

    for case in MISROUTE_CASES:
        result = run_pipeline(case["query"])
        is_misrouted = check_misroute(result["answer"], case["bad_signals"])

        status = "FAIL (misrouted)" if is_misrouted else "PASS (not misrouted)"
        if not is_misrouted:
            passed += 1
        else:
            failed += 1

        print(f"\n{'~' * 80}")
        print(f"  {case['label']}")
        print(f"  STATUS: {status}")
        print(f"  module={result['module']}  entities={result['entities']}  intent={result['intent']}")
        print(f"  top_source={result['top_source']}")
        print(f"  top_score={result['top_score']}  evidence_count={result['evidence_count']}")
        print(f"  answer_preview: {result['answer'][:250]}")

    print(f"\n{'=' * 80}")
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(MISROUTE_CASES)}")
    print(f"{'=' * 80}")
    return failed == 0


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
