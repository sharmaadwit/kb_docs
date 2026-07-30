#!/usr/bin/env python3
"""
Debug SSO document retrieval by checking chunk scores directly.
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


def load_env():
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
    print("=" * 80)
    print("DEBUG: SSO DOCUMENT SCORING")
    print("=" * 80)

    env_vars = load_env()
    os.environ.update(env_vars)

    try:
        from kb_answer import _load_chunks, _score_chunk, _normalize_query_for_match, _detect_module, _extract_entities, _classify_intent
        print("\nFunctions imported successfully")
    except Exception as e:
        print(f"\nERROR importing: {e}")
        import traceback
        traceback.print_exc()
        return 1

    context = _Context(env_vars)

    try:
        chunks = _load_chunks(context)
        print(f"Loaded {len(chunks)} chunks")
    except Exception as e:
        print(f"ERROR loading chunks: {e}")
        return 1

    # Find SSO chunks
    sso_chunks = [c for c in chunks if "sso" in c.get("source", "").lower()]
    print(f"Found {len(sso_chunks)} SSO-related chunks")

    test_queries = [
        "Does Gupshup Console support Single Sign-On?",
        "What identity providers does Console SSO support?",
        "Can my organization use SAML 2.0 with Console?",
        "Do I need admin access to set up Console SSO?",
        "What certificate formats are accepted for SSO?",
    ]

    for query in test_queries:
        print(f"\n{'='*80}")
        print(f"Query: {query}")
        print('='*80)

        normalized_q = _normalize_query_for_match(query)
        print(f"Normalized: {normalized_q}")

        module = _detect_module(query)
        print(f"Detected module: {module}")

        entities = _extract_entities(query)
        print(f"Entities: {entities}")

        intent = _classify_intent(query, entities)
        print(f"Intent: {intent}")

        # Score all chunks
        scored = []
        for c in chunks:
            score = _score_chunk(query, c, entities, module)
            if c.get("source", "").lower() in ["gupshup_console_sso support.md", "gupshup_console_sso_support.md"] or "sso" in c.get("source", "").lower():
                scored.append({
                    "score": score,
                    "source": c.get("source", "N/A"),
                    "heading": c.get("heading", "N/A"),
                    "text": c.get("text", "")[:80] if c.get("text") else "",
                })

        # Sort by score descending
        scored.sort(key=lambda x: x["score"], reverse=True)

        print(f"\nTop SSO Chunks (sorted by score):")
        for i, item in enumerate(scored[:10], 1):
            print(f"  {i}. Score: {item['score']:.2f}")
            print(f"     Source: {item['source']}")
            print(f"     Heading: {item['heading']}")
            print(f"     Text: {item['text']}")

        # Now score ALL chunks and show top 5 overall
        all_scored = []
        for c in chunks:
            score = _score_chunk(query, c, entities, module)
            if score > 0:  # Only include scored chunks
                all_scored.append({
                    "score": score,
                    "source": c.get("source", "N/A"),
                    "heading": c.get("heading", "N/A"),
                })

        all_scored.sort(key=lambda x: x["score"], reverse=True)
        print(f"\nTop 5 Overall Chunks:")
        for i, item in enumerate(all_scored[:5], 1):
            print(f"  {i}. Score: {item['score']:.2f} | {item['source']} | {item['heading']}")


if __name__ == "__main__":
    sys.exit(main())
