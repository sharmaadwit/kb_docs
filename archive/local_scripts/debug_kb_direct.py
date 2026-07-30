#!/usr/bin/env python3
"""
Direct debug of kb_answer execution.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path('/Users/adwit.sharma/kb_docs/skill')))

class MockContext:
    def get_secret(self, name):
        return None

from kb_answer import (
    kb_answer, _load_chunks, _score_chunk, _select_evidence,
    _classify_intent, _extract_entities, _detect_module,
    _normalize_query_for_match, _compose_answer, _parse_parameters,
    _extract_query, _sanitize_kb_query, _translate_key_terms, MIN_CHUNK_SCORE
)

def debug_query(query_text):
    print("=" * 80)
    print(f"Query: {query_text}")
    print("=" * 80)

    # Parse and sanitize query
    params = _parse_parameters({"query": query_text})
    query = _sanitize_kb_query(_extract_query(params))
    query = _translate_key_terms(query)

    print(f"Processed query: {query}")

    # Get entities and intent
    entities = _extract_entities(query)
    intent = _classify_intent(query, entities)
    module = _detect_module(query)

    print(f"Entities: {entities}")
    print(f"Intent: {intent}")
    print(f"Module: {module}")

    # Load chunks
    context = MockContext()
    chunks = _load_chunks(context)
    product_chunks = [c for c in chunks if "case-studies" not in str(c.get("source", ""))]

    # Score and filter
    scored = []
    for c in product_chunks:
        s = _score_chunk(query, c, entities, module)
        if s >= MIN_CHUNK_SCORE:
            row = dict(c)
            row["score"] = s
            scored.append(row)
    scored.sort(key=lambda x: x.get("score", 0.0), reverse=True)

    print(f"\nTop 15 scored chunks (MIN_CHUNK_SCORE={MIN_CHUNK_SCORE}):")
    print("-" * 80)
    for i, row in enumerate(scored[:15], 1):
        print(f"{i:2}. Score: {row['score']:6.2f} | Source: {row['source']:50} | Heading: {row['heading'][:40]}")

    # Select evidence
    evidence = _select_evidence(query, scored, intent, module)
    print(f"\nEvidence selected (count={len(evidence)}):")
    print("-" * 80)
    for i, row in enumerate(evidence, 1):
        print(f"{i}. Source: {row['source']}")
        print(f"   Heading: {row['heading']}")
        print(f"   Score: {row['score']}")
        print(f"   Text preview: {row['text'][:100]}")
        print()

    # Compose answer
    answer = _compose_answer(query, intent, entities, evidence, module)
    print(f"\nFinal answer (first 300 chars):")
    print("-" * 80)
    print(answer[:300])

# Test the problematic query
query = "Are there restrictions on dietary supplement promotion via WhatsApp?"
debug_query(query)
