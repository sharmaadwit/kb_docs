#!/usr/bin/env python3
"""Debug coverage check."""
import json
import sys
import os
import re

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
    "Q4": "How do I set up a WhatsApp Business Account WABA and connect it to Gupshup?",
    "Q9": "What are the steps to create and send my first campaign to 1000 contacts?",
}

def debug_query(query_label, query):
    print(f"\n{'='*100}")
    print(f"DEBUG COVERAGE: {query_label}")
    print(f"{'='*100}")
    print(f"Query: {query}\n")

    # Run guardrail check
    guardrail = kb._guardrail_answer(query)
    if guardrail:
        print(f"Guardrail triggered")
        return

    chunks = CACHED_CHUNKS
    explicit_module = kb._detect_module(query)
    entities = kb._extract_entities(query)
    intent = kb._classify_intent(query, entities)

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

    # Select evidence
    evidence = kb._select_evidence(query, scored, intent, explicit_module)
    lines = kb._evidence_lines(evidence)

    if not evidence:
        print("No evidence")
        return

    joined = "\n".join(lines).lower()
    source_text = " ".join(str(c.get("source") or "").lower() for c in evidence)
    topic_joined = joined + "\n" + source_text

    # Debug coverage
    distinctive = list(set(kb._query_distinctive_tokens(query)))
    print(f"Distinctive tokens: {distinctive}")

    j = (topic_joined or "").lower()
    hits = {}
    for t in distinctive:
        is_in = t in j
        hits[t] = is_in
        print(f"  '{t}': {is_in}")

    coverage = sum(1 for v in hits.values() if v) / len(distinctive) if distinctive else 1.0
    coverage_threshold = 0.2 if explicit_module != "General" else 0.4

    print(f"\nCoverage: {sum(1 for v in hits.values() if v)} / {len(distinctive)} = {coverage:.2f}")
    print(f"Threshold (module_match={explicit_module != 'General'}): {coverage_threshold}")
    print(f"Passes: {coverage >= coverage_threshold}")

for label, query in queries.items():
    debug_query(label, query)
