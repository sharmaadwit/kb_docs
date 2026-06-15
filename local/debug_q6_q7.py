#!/usr/bin/env python3
"""Debug Q6 and Q7 to understand why they're still failing."""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skill"))
import kb_answer as kb

CHUNKS_PATH = os.path.join(os.path.dirname(__file__), "..", "kb", "kb_chunks.jsonl")

def _load_chunks():
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
queries = {
    "Q6": "How do I sync customer data from Salesforce to Gupshup through webhooks?",
    "Q7": "How do I configure a WABA in the Gupshup Console and register webhook endpoints?",
}

def debug_query(query_label, query):
    print(f"\n{'='*100}")
    print(f"DEBUG: {query_label}")
    print(f"{'='*100}")
    print(f"Query: {query}\n")

    # Run guardrail check
    guardrail = kb._guardrail_answer(query)
    if guardrail:
        print(f"Guardrail triggered: {guardrail[:100]}")
        return

    chunks = CACHED_CHUNKS
    explicit_module = kb._detect_module(query)
    entities = kb._extract_entities(query)
    intent = kb._classify_intent(query, entities)

    print(f"Module: {explicit_module}")
    print(f"Entities: {[e['id'] for e in entities]}")
    print(f"Intent: {intent}\n")

    # Score all chunks
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

    print(f"Top 5 scored chunks:")
    for i, chunk in enumerate(scored[:5], 1):
        print(f"  {i}. {chunk['source']}: {chunk['score']:.2f}")

    # Select evidence
    evidence = kb._select_evidence(query, scored, intent, explicit_module)

    print(f"\nEvidence selected: {len(evidence)} chunks")
    for i, e in enumerate(evidence, 1):
        print(f"  {i}. {e['source']}: {e['score']:.2f}")

    if not evidence:
        print("\nNo evidence - returning IDK")
        return

    lines = kb._evidence_lines(evidence)
    print(f"\nEvidence lines: {len(lines)}")
    for line in lines[:5]:
        print(f"  - {line[:80]}")

    # Check _has_explicit_support
    has_support = kb._has_explicit_support(query, intent, evidence, lines, entities, explicit_module)
    print(f"\n_has_explicit_support: {has_support}")

for label, query in queries.items():
    debug_query(label, query)
