#!/usr/bin/env python3
"""Debug why Q4 and Q9 are returning IDK - deeper dive into setup logic."""
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
    print(f"DEBUG SETUP CHECKS: {query_label}")
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

    # Now debug setup logic
    joined = "\n".join(lines).lower()
    top1 = evidence[0]
    top1_overlap = kb._query_overlap_score(query, top1)

    print(f"Setup intent checks:")
    print(f"  1. long_distinctive_terms_missing: {kb._long_distinctive_terms_missing_from_evidence(query, joined)}")
    print(f"  2. setup_evidence_missing_required_terms: {kb._setup_evidence_missing_required_terms(query, joined)}")
    print(f"  3. query_topic_not_in_evidence: {kb._query_topic_not_in_evidence(query, joined)}")

    # Check has_action and has_steps_block
    has_action = any(kb._is_action_oriented(line) for line in lines[:6])
    has_steps_block = any(
        ("steps" in (c.get("heading") or "").lower()
         or "procedure" in (c.get("heading") or "").lower())
        for c in evidence
    )

    print(f"\n  has_action (first 6 lines): {has_action}")
    for i, line in enumerate(lines[:6], 1):
        is_action = kb._is_action_oriented(line)
        print(f"    Line {i} ({is_action}): {line[:70]}")

    print(f"\n  has_steps_block: {has_steps_block}")
    for c in evidence:
        print(f"    Heading: {c.get('heading') or '(none)'}")

    # Check core tokens
    core_tokens = [
        t for t in re.findall(r"[a-z0-9&+-]+", kb._normalize_query_for_match(query))
        if len(t) >= 5
        and t not in kb.SCORING_STOP_WORDS
        and t not in {
            "journey", "builder", "studio", "console", "gupshup",
            "steps", "step", "setup", "node", "nodes",
        }
    ]
    core_hits = sum(1 for t in set(core_tokens) if t in joined)

    print(f"\n  core_tokens (>=5 chars): {core_tokens}")
    print(f"  core_hits: {core_hits}")
    print(f"  core_tokens && core_hits==0 && overlap<0.45: {bool(core_tokens and core_hits == 0 and top1_overlap < 0.45)}")

    # Final check
    final_result = ((has_action or has_steps_block) and top1_overlap >= 0.2) or top1_overlap >= 0.45
    print(f"\n  Final: ((has_action={has_action} or has_steps_block={has_steps_block}) and overlap={top1_overlap:.2f}>=0.2) or overlap={top1_overlap:.2f}>=0.45")
    print(f"  Result: {final_result}")

for label, query in queries.items():
    debug_query(label, query)
