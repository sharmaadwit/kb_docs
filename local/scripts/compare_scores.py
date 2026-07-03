#!/usr/bin/env python3
"""
Compare scoring behavior between BizAI and existing modules
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

class _Context:
    def __init__(self, secrets: dict):
        self._secrets = secrets

    def get_secret(self, key: str):
        return self._secrets.get(key) or os.environ.get(key)


def load_env() -> dict:
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

    from kb_answer import (
        _load_chunks,
        _score_chunk,
        _extract_entities,
        _classify_intent,
        _detect_module,
        MIN_CHUNK_SCORE,
    )

    context = _Context(env_vars)

    # Test queries for comparison
    test_queries = [
        ("What is Agent Assist?", "agent assist"),
        ("What is BizAI and what does it do?", "bizai"),
        ("What is Campaign Manager?", "campaign manager"),
    ]

    chunks = _load_chunks(context)

    print("Score Comparison Across Modules")
    print("=" * 80)

    for query, module_keyword in test_queries:
        print(f"\nQuery: {query}")
        print(f"Module keyword: {module_keyword}")

        entities = _extract_entities(query)
        module = _detect_module(query)
        intent = _classify_intent(query, entities)

        print(f"Detected module: {module}")

        scored = []
        for c in chunks:
            s = _score_chunk(query, c, entities, module)
            if s >= MIN_CHUNK_SCORE:
                scored.append((s, c))

        scored.sort(key=lambda x: x[0], reverse=True)

        # Show top 3
        print("Top 3 scores:")
        for rank, (score, chunk) in enumerate(scored[:3], 1):
            source = chunk.get("source", "")
            heading = chunk.get("heading", "")
            confidence = min(1.0, max(0.0, score / 8.0))
            print(f"  {rank}. Raw: {score:.3f} → Confidence: {confidence:.3f} ({source})")

        if scored:
            avg_score = sum(s for s, _ in scored[:5]) / min(5, len(scored))
            print(f"Average score (top 5): {avg_score:.3f}")


if __name__ == "__main__":
    main()
