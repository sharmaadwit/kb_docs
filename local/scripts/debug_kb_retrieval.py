#!/usr/bin/env python3
"""
Debug script to see what chunks kb_answer is retrieving for promotional restriction queries.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "skill"))

class MockContext:
    def get_secret(self, name):
        return None

def debug_retrieval():
    from kb_answer import kb_answer, _load_chunks, _score_chunk, _normalize_query_for_match
    import re

    # Test question
    query = "Are there restrictions on promotional messages for dietary supplements on WhatsApp?"

    context = MockContext()
    chunks = _load_chunks(context)

    # Search for promotional restriction chunks
    promo_chunks = [c for c in chunks if "promotional" in str(c.get("text", "")).lower()]

    print("=" * 80)
    print(f"Query: {query}")
    print("=" * 80)
    print(f"\nTotal chunks: {len(chunks)}")
    print(f"Chunks mentioning 'promotional': {len(promo_chunks)}")

    # Score all chunks
    scored = []
    for c in chunks:
        score = _score_chunk(query, c, [], "General")
        if score >= 0.5:  # Lower threshold to see what's being ranked
            scored.append({
                "source": c.get("source"),
                "heading": c.get("heading"),
                "score": score,
                "text_preview": c.get("text", "")[:100]
            })

    scored.sort(key=lambda x: x["score"], reverse=True)

    print("\n" + "=" * 80)
    print("Top 20 scored chunks:")
    print("=" * 80)
    for i, item in enumerate(scored[:20], 1):
        print(f"\n{i}. Score: {item['score']:.2f}")
        print(f"   Source: {item['source']}")
        print(f"   Heading: {item['heading']}")
        print(f"   Preview: {item['text_preview']}")

    # Specifically look for WhatsApp promo restriction chunks
    print("\n" + "=" * 80)
    print("Chunks from whatsapp-promotional-restrictions.md:")
    print("=" * 80)
    promo_restrict_chunks = [c for c in chunks if "whatsapp-promotional" in str(c.get("source", "")).lower()]

    for c in promo_restrict_chunks[:10]:
        score = _score_chunk(query, c, [], "General")
        print(f"\nHeading: {c.get('heading')}")
        print(f"Score: {score:.2f}")
        print(f"Text preview: {c.get('text', '')[:150]}")

if __name__ == "__main__":
    debug_retrieval()
