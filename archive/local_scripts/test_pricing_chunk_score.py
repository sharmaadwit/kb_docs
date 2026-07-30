#!/usr/bin/env python3
"""
Test scoring for whatsapp-pricing chunk
"""

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path("/Users/adwit.sharma/kb_docs")
SKILL_DIR = REPO_ROOT / "skill"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

class _Context:
    def __init__(self, secrets: dict):
        self._secrets = secrets
    def get_secret(self, key: str):
        return self._secrets.get(key) or os.environ.get(key)

env_path = REPO_ROOT / ".env"
env_vars = {}
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env_vars[k.strip()] = v.strip().strip('"').strip("'")

os.environ.update(env_vars)

from kb_answer import (
    _load_chunks,
    _score_chunk,
    _extract_entities,
    _classify_intent,
    _detect_module,
)

context = _Context(env_vars)

query = "What is WhatsApp API pricing?"
print(f"Query: {query}\n")

chunks = _load_chunks(context)
entities = _extract_entities(query)
module = _detect_module(query)
intent = _classify_intent(query, entities)

print(f"Detected module: {module}")
print(f"Entities: {entities}")
print(f"Intent: {intent}\n")

# Find and score whatsapp-pricing chunks
pricing_chunks = [c for c in chunks if "whatsapp-pricing" in c.get("source", "")]
print(f"Found {len(pricing_chunks)} whatsapp-pricing chunks\n")

# Score each
scored = []
for chunk in pricing_chunks:
    score = _score_chunk(query, chunk, entities, module)
    scored.append((score, chunk))

scored.sort(key=lambda x: x[0], reverse=True)

print("Top 5 whatsapp-pricing chunks:")
for i, (score, chunk) in enumerate(scored[:5], 1):
    heading = chunk.get("heading", "")
    confidence = min(1.0, max(0.0, score / 8.0))
    text_preview = chunk.get("text", "")[:100]

    print(f"\n{i}. Raw Score: {score:.3f} (Confidence: {confidence:.3f})")
    print(f"   Heading: {heading}")
    print(f"   Text: {text_preview}...")
