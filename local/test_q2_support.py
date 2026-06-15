#!/usr/bin/env python3
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

query = "How do I structure JSON for WhatsApp quick reply buttons?"

chunks = CACHED_CHUNKS
explicit_module = kb._detect_module(query)
entities = kb._extract_entities(query)
intent = kb._classify_intent(query, entities)

scored = []
for c in chunks:
    s = kb._score_chunk(query, c, entities, explicit_module)
    if s > 0:
        row = dict(c)
        row["score"] = s
        scored.append(row)
scored.sort(key=lambda x: x.get("score", 0.0), reverse=True)

evidence = kb._select_evidence(query, scored, intent, explicit_module)
lines = kb._evidence_lines(evidence)

print(f"Evidence: {len(evidence)} chunks")
for e in evidence:
    print(f"  - {e['source']}: {e['score']:.2f}")

has_support = kb._has_explicit_support(query, intent, evidence, lines, entities, explicit_module)
print(f"\n_has_explicit_support: {has_support}")

# Also check what the answer is
answer = kb._compose_answer(query, intent, entities, evidence, explicit_module)
print(f"\nAnswer (first 200 chars):\n{answer[:200]}")
