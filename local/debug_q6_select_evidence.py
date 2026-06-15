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

query = "How do I sync customer data from Salesforce to Gupshup through webhooks?"

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

# Now see what _select_evidence returns
evidence = kb._select_evidence(query, scored, intent, explicit_module)

print(f"\n_select_evidence returned {len(evidence)} chunks:")
for i, e in enumerate(evidence, 1):
    print(f"  {i}. {e['source']}: {e['score']:.2f}")

# Debug the logic
scoped = kb._filter_by_explicit_module(scored, explicit_module)
print(f"\nAfter _filter_by_explicit_module: {len(scoped)} chunks")

action_rows = []
for row in scoped[:6]:
    text_lines = str(row.get("text") or "").splitlines()
    is_action = any(kb._is_action_oriented(x) for x in text_lines)
    print(f"  Checking {row['source'][:40]}: action={is_action}")
    if is_action:
        action_rows.append(row)

print(f"\naction_rows: {len(action_rows)} chunks")
for i, r in enumerate(action_rows[:4], 1):
    print(f"  {i}. {r['source']}: {r['score']:.2f}")

result = action_rows[:4] if action_rows else scoped[:3]
print(f"\nFinal result: {len(result)} chunks")
for i, r in enumerate(result, 1):
    print(f"  {i}. {r['source']}: {r['score']:.2f}")
