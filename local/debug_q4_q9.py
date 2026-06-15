#!/usr/bin/env python3
"""Debug why Q4 and Q9 are returning IDK despite decent scores."""
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
    "Q4": "How do I set up a WhatsApp Business Account WABA and connect it to Gupshup?",
    "Q9": "What are the steps to create and send my first campaign to 1000 contacts?",
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

    # Debug the checks in _has_explicit_support
    top1 = evidence[0]
    top_source_mod = kb._module_from_source(str(top1.get("source") or ""))
    module_match = (
        explicit_module != "General"
        and top_source_mod.lower() == explicit_module.lower()
    )

    top1_overlap = kb._query_overlap_score(query, top1)
    strong_overlap = top1_overlap >= 0.7 and top1.get("score", 0.0) >= 0.5
    hedged_ok = (
        (top1_overlap >= 0.7 and top1.get("score", 0.0) >= 0.5)
        or (top1_overlap >= 0.5 and top1.get("score", 0.0) >= 0.85)
    )

    effective_min = 0.8 if module_match else kb.MIN_EVIDENCE_SCORE
    initial_check_pass = not (top1.get("score", 0.0) < effective_min and not strong_overlap and not hedged_ok)

    print(f"\nDebug details:")
    print(f"  Top1 score: {top1.get('score', 0.0):.2f}")
    print(f"  Top1 source module: {top_source_mod}")
    print(f"  Module match: {module_match}")
    print(f"  Overlap score: {top1_overlap:.2f}")
    print(f"  Strong overlap (>=0.7 && >=0.5): {strong_overlap}")
    print(f"  Hedged OK (0.7/0.5 or 0.5/0.85): {hedged_ok}")
    print(f"  Effective min: {effective_min}")
    print(f"  Initial check pass: {initial_check_pass}")

    # Check unboosted floor
    has_entity_boost = kb._top_evidence_has_entity_boost(evidence, entities or [])
    print(f"\n  Entity boost: {has_entity_boost}")

    if not module_match and not has_entity_boost:
        unboosted_floor = kb.MIN_EVIDENCE_SCORE_UNBOOSTED
        if len(evidence) >= 2 and top1_overlap >= 0.25:
            unboosted_floor = kb.MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI
        unboosted_check_pass = not (
            intent != "overview"
            and top1.get("score", 0.0) < unboosted_floor
            and not strong_overlap
            and not hedged_ok
        )
        print(f"  Unboosted floor: {unboosted_floor}")
        print(f"  Unboosted check pass: {unboosted_check_pass}")

for label, query in queries.items():
    debug_query(label, query)
