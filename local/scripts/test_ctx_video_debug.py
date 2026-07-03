#!/usr/bin/env python3
"""
Test script to debug CTX video selection with local logging.

Runs 5 CTX queries and captures debug output from kb_answer.
"""

import json
import logging
import os
import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Configure logging to see DEBUG level
logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s - %(levelname)s - %(message)s'
)

from skill.kb_answer import kb_answer

class MockContext:
    def __init__(self):
        self.env = {
            "KB_DEMOFORGE_MANIFEST_PATH": "kb/demoforge_manifest.json",
            "KB_CHUNKS_PATH": "kb/kb_chunks.jsonl",
            "KB_INDEX_PATH": "kb/kb_index.json",
        }

    def get_secret(self, name):
        return self.env.get(name)

# CTX test queries
ctx_queries = [
    "How do I set up CTX?",
    "Tell me about CTX overview",
    "What is CTX used for?",
    "How do I configure context window?",
    "CTX best practices",
]

context = MockContext()

print("=" * 80)
print("CTX VIDEO SELECTION DEBUG TEST")
print("=" * 80)

for i, query in enumerate(ctx_queries, 1):
    print(f"\n[Test {i}] Query: {query}")
    print("-" * 80)

    result = kb_answer(
        query=query,
        context=context,
        params={"language": "en"},
    )

    if result.get("ok"):
        answer = result.get("answer", "")[:100]
        print(f"Answer (first 100 chars): {answer}...")

        # Check video metadata
        if "video" in result:
            video = result["video"]
            print(f"Video Type: {video.get('type')}")
            print(f"Video ID/Demo ID: {video.get('demo_id') or video.get('video_id')}")
            print(f"Video Title: {video.get('title') or video.get('name')}")
        else:
            print("No video attached")
    else:
        print(f"Error: {result.get('error')}")

print("\n" + "=" * 80)
print("DEBUG OUTPUT ABOVE CONTAINS [DemoForge] and [VideoSelection] LOGS")
print("=" * 80)
