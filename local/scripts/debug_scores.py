#!/usr/bin/env python3
"""
Debug score calculation for BizAI/WhatsApp queries
"""

import json
import os
import sys
from pathlib import Path

# Setup paths
REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / "skill"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

# Minimal context stub
class _Context:
    def __init__(self, secrets: dict):
        self._secrets = secrets

    def get_secret(self, key: str):
        return self._secrets.get(key) or os.environ.get(key)


def load_env() -> dict:
    """Load .env into dict."""
    env_path = REPO_ROOT / ".env"
    env_vars = {}
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    env_vars[k.strip()] = v.strip().strip('"').strip("'")
    return env_vars


def main():
    env_vars = load_env()
    os.environ.update(env_vars)

    # Import internal functions
    from kb_answer import (
        _load_chunks,
        _score_chunk,
        _extract_entities,
        _classify_intent,
        _normalize_query_for_match,
        _detect_module,
        MIN_CHUNK_SCORE,
    )

    context = _Context(env_vars)

    test_query = "What is BizAI and what does it do?"

    print(f"Query: {test_query}")
    print(f"MIN_CHUNK_SCORE threshold: {MIN_CHUNK_SCORE}")
    print()

    chunks = _load_chunks(context)
    print(f"Total chunks: {len(chunks)}")

    # Score chunks
    entities = _extract_entities(test_query)
    module = _detect_module(test_query)
    intent = _classify_intent(test_query, entities)

    print(f"Detected module: {module}")
    print(f"Detected intent: {intent}")
    print()

    scored = []
    for c in chunks:
        s = _score_chunk(test_query, c, entities, module)
        if s >= MIN_CHUNK_SCORE:
            scored.append((s, c))

    # Sort and show top 10
    scored.sort(key=lambda x: x[0], reverse=True)

    print("Top 10 scored chunks:")
    print("-" * 80)
    for rank, (score, chunk) in enumerate(scored[:10], 1):
        source = chunk.get("source", "")
        heading = chunk.get("heading", "")
        text_preview = (chunk.get("text") or "")[:60]

        # Calculate confidence the way kb_answer does
        confidence = min(1.0, max(0.0, score / 8.0))

        print(f"{rank}. Score: {score:.3f} (confidence: {confidence:.3f})")
        print(f"   Source: {source}")
        print(f"   Heading: {heading}")
        print(f"   Text: {text_preview}...")
        print()


if __name__ == "__main__":
    main()
