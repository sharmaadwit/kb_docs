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

query = "How do I configure a WABA in the Gupshup Console and register webhook endpoints?"

guardrail = kb._guardrail_answer(query)
if guardrail:
    print(f"Guardrail: {guardrail}")
    sys.exit(1)

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

print(f"Answer:\n{answer[:200]}")
is_idk = "i don t know" in answer.lower() or "i don't know" in answer.lower()
print(f"\nIs IDK: {is_idk}")
