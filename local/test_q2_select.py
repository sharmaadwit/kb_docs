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

print("Top 6 scored chunks:")
for i, chunk in enumerate(scored[:6], 1):
    text_lines = str(chunk.get("text") or "").splitlines()
    is_action = any(kb._is_action_oriented(x) for x in text_lines)
    print(f"  {i}. {chunk['source'][:50]}: {chunk['score']:.2f} (action={is_action})")

# Debug the logic
scoped = kb._filter_by_explicit_module(scored, explicit_module)

action_rows = []
for row in scoped[:6]:
    text_lines = str(row.get("text") or "").splitlines()
    is_action = any(kb._is_action_oriented(x) for x in text_lines)
    if is_action:
        action_rows.append(row)

print(f"\naction_rows: {len(action_rows)}")
if action_rows:
    top_action_score = action_rows[0].get("score", 0.0)
    top_score = scoped[0].get("score", 0.0)
    ratio = top_action_score / top_score if top_score > 0 else 0
    print(f"  top_action_score: {top_action_score:.2f}")
    print(f"  top_score: {top_score:.2f}")
    print(f"  ratio: {ratio:.4f}")
    print(f"  ratio < 0.95: {ratio < 0.95}")
    if ratio < 0.95:
        print(f"  -> return scoped[:3]")
        for r in scoped[:3]:
            print(f"    - {r['source']}: {r['score']:.2f}")
    else:
        print(f"  -> return action_rows[:4]")
        for r in action_rows[:4]:
            print(f"    - {r['source']}: {r['score']:.2f}")
