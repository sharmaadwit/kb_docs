#!/usr/bin/env python3
"""
Integrate new KB chunks into kb/kb_chunks.jsonl

Usage:
  python local/scripts/integrate_new_chunks.py
"""

import json
from pathlib import Path

KB_CHUNKS = Path(__file__).parent.parent.parent / "kb" / "kb_chunks.jsonl"
NEW_CHUNKS = Path(__file__).parent.parent / "reports" / "new_kb_chunks.json"

def integrate():
    """Read new chunks and append to kb_chunks.jsonl"""

    # Load new chunks
    with open(NEW_CHUNKS) as f:
        data = json.load(f)

    new_chunks = data.get("chunks", [])
    if not new_chunks:
        print("No chunks to integrate")
        return 1

    # Count existing chunks
    existing_count = 0
    with open(KB_CHUNKS) as f:
        for line in f:
            if line.strip():
                existing_count += 1

    print(f"Existing chunks: {existing_count}")
    print(f"New chunks: {len(new_chunks)}")

    # Append new chunks as JSONL
    with open(KB_CHUNKS, "a") as f:
        for chunk in new_chunks:
            # Convert to JSONL format (minimal metadata per chunk)
            jsonl_entry = {
                "id": chunk.get("id"),
                "content": chunk.get("content"),
                "source": chunk.get("source"),
                "module": chunk.get("module"),
                "intent_keywords": chunk.get("intent_keywords", []),
                "topic": chunk.get("topic"),
            }
            f.write(json.dumps(jsonl_entry) + "\n")

    final_count = existing_count + len(new_chunks)
    print(f"Final chunk count: {final_count}")
    print(f"✓ Integrated {len(new_chunks)} new chunks")
    print(f"✓ Saved to kb/kb_chunks.jsonl")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(integrate())
