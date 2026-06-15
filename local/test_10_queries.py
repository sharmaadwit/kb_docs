#!/usr/bin/env python3
"""
Test runner for 10 test queries through kb_search and kb_answer.

Shows baseline behavior before and after fixes are applied.
"""
import json
import sys
import os
from typing import Dict, List, Any

# Add skill modules to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skill"))
import kb_answer as kb

CHUNKS_PATH = os.path.join(os.path.dirname(__file__), "..", "kb", "kb_chunks.jsonl")

def _load_chunks():
    """Load chunks from JSONL."""
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

CACHED_CHUNKS = _load_chunks()

# Test queries
TEST_QUERIES = [
    "Where do I find my API keys in the Gupshup Console?",
    "How do I structure JSON for WhatsApp quick reply buttons?",
    "What's the pattern for collecting user input, validating it, then sending a response in a journey?",
    "How do I set up a WhatsApp Business Account WABA and connect it to Gupshup?",
    "What are the steps to onboard an RCS agent through Dotgo RBM Hub?",
    "How do I sync customer data from Salesforce to Gupshup through webhooks?",
    "How do I configure a WABA in the Gupshup Console and register webhook endpoints?",
    "What are the API rate limits for sending messages, and how do I handle 429 responses?",
    "What are the steps to create and send my first campaign to 1000 contacts?",
    "What's the recommended message design best practice for RCS rich cards to maximize engagement?",
]

def search_and_answer_query(query: str) -> Dict[str, Any]:
    """Run kb_answer pipeline on a query using local chunks."""
    # Run guardrail check
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
            "confidence": 0,
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

    # Store search results for analysis
    top_search_source = scored[0].get("source") if scored else None
    top_search_score = scored[0].get("score", 0) if scored else 0

    evidence = kb._select_evidence(query, scored, intent, explicit_module)
    answer = kb._compose_answer(query, intent, entities, evidence, explicit_module)

    # Check if answer is "I don't know"
    is_idk = "i don't know" in answer.lower() or "i don t know" in answer.lower()

    return {
        "module": explicit_module,
        "entities": [e["id"] for e in entities],
        "intent": intent,
        "top_source": evidence[0].get("source") if evidence else None,
        "top_score": round(evidence[0].get("score", 0), 2) if evidence else 0,
        "evidence_count": len(evidence),
        "answer": answer,
        "answered": not is_idk,
        "confidence": round(evidence[0].get("score", 0), 2) if evidence else 0,
        "search_source": top_search_source,
        "search_score": round(top_search_score, 2),
    }

def format_source(source: str) -> str:
    """Extract filename from source slug."""
    if not source:
        return "—"
    return source.split("/")[-1] if "/" in source else source

def run_tests():
    """Run all 10 test queries."""
    results = []

    print("\n" + "="*120)
    print("KB SYSTEM TEST: 10 QUERIES".center(120))
    print("="*120)
    print()

    for idx, query in enumerate(TEST_QUERIES, 1):
        print(f"\n{'─'*120}")
        print(f"Q{idx}: {query[:80]}{'...' if len(query) > 80 else ''}")
        print(f"{'─'*120}")

        # Run answer pipeline (includes search)
        result = search_and_answer_query(query)

        search_source = format_source(result.get("search_source", ""))
        search_score = result.get("search_score", 0)

        print(f"  kb_search:")
        print(f"    Top source: {search_source}")
        print(f"    Score:      {search_score:.2f}")

        answered = result.get("answered", False)
        answer_source = format_source(result.get("top_source", ""))
        confidence = result.get("confidence", 0)
        intent = result.get("intent", "unknown")
        answer_text = result.get("answer", "")

        print(f"  kb_answer:")
        print(f"    Answered:   {answer_text[:80] if answer_text else 'IDK'}")
        print(f"    Source:     {answer_source if answered else '—'}")
        print(f"    Confidence: {confidence:.2f}")
        print(f"    Intent:     {intent}")

        # Improvement check
        status = "PASS ✅" if answered else "FAIL ❌"

        if search_score > 5.0 and not answered:
            improvement = "BROKEN (search found, answer IDK)"
        elif search_score <= 5.0 and not answered:
            improvement = "EXPECTED (no good search result)"
        elif answered:
            improvement = "WORKS ✅"
        else:
            improvement = "—"

        print(f"  Status: {status} | {improvement}")

        results.append({
            "q_num": idx,
            "query": query,
            "search_source": search_source,
            "search_score": search_score,
            "answered": answered,
            "answer_source": answer_source,
            "confidence": confidence,
            "intent": intent,
        })

    # Summary table
    print(f"\n\n{'='*120}")
    print("SUMMARY TABLE".center(120))
    print(f"{'='*120}\n")

    print(f"{'Q':<3} {'Query':<50} {'Search Score':<15} {'Answered':<10} {'Confidence':<12} {'Status':<15}")
    print(f"{'-'*3} {'-'*50} {'-'*15} {'-'*10} {'-'*12} {'-'*15}")

    for r in results:
        status = "PASS ✅" if r["answered"] else "FAIL ❌"
        query_short = r["query"][:47] + "..." if len(r["query"]) > 50 else r["query"]
        print(f"{r['q_num']:<3} {query_short:<50} {r['search_score']:<15.2f} {str(r['answered']):<10} {r['confidence']:<12.2f} {status:<15}")

    # Analysis by query range
    print(f"\n{'='*120}")
    print("ANALYSIS BY QUERY RANGE".center(120))
    print(f"{'='*120}\n")

    q1_5 = sum(1 for r in results[:5] if r["answered"])
    q6_9 = sum(1 for r in results[5:9] if r["answered"])
    q10 = 1 if results[9]["answered"] else 0

    print(f"Q1-Q5 (baseline):           {q1_5}/5 answered ({q1_5*20}%)")
    print(f"Q6-Q9 (focus area):         {q6_9}/4 answered ({q6_9*25}%)")
    print(f"Q10 (RCS rich cards):       {q10}/1 answered ({q10*100}%)")

    total_answered = sum(1 for r in results if r["answered"])
    print(f"\nOVERALL: {total_answered}/10 answered ({total_answered*10}%)")

    # Detailed issue analysis for Q6-Q9
    print(f"\n{'='*120}")
    print("DETAILED ANALYSIS: Q6-Q9 (Previously Failing)".center(120))
    print(f"{'='*120}\n")

    focus_queries = [
        (6, "Salesforce Webhook"),
        (7, "WABA + Webhook Config"),
        (8, "API Rate Limits"),
        (9, "First Campaign"),
    ]

    for q_num, label in focus_queries:
        r = results[q_num - 1]
        gap = r["search_score"] - r["confidence"]

        print(f"\nQ{q_num} — {label}")
        print(f"  Search score:      {r['search_score']:.2f}")
        print(f"  Answer confidence: {r['confidence']:.2f}")
        print(f"  Gap:               {gap:.2f}")
        print(f"  kb_search result:  ✅ (score {r['search_score']:.2f})" if r["search_score"] > 3.0 else "  kb_search result:  ❌")
        print(f"  kb_answer result:  {'✅ (answered)' if r['answered'] else '❌ (IDK)'}")

        if r["search_score"] > 5.0 and not r["answered"]:
            print(f"  ⚠️  ISSUE: Search found valid result but answer returned IDK")
            print(f"      Threshold likely: {r['confidence']:.1f} < 2.0")
            print(f"      FIX: Lower threshold to ~1.0 or use search as fallback")

if __name__ == "__main__":
    run_tests()
