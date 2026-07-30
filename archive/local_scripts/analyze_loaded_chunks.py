#!/usr/bin/env python3
"""
Analyze what chunks are actually being loaded by kb_answer
"""

import os
import sys
from pathlib import Path
from collections import defaultdict

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

from kb_answer import _load_chunks

context = _Context(env_vars)
chunks = _load_chunks(context)

# Count by folder
by_folder = defaultdict(int)
for chunk in chunks:
    source = chunk.get("source", "")
    if "/" in source:
        folder = source.split("/")[1]
        by_folder[folder] += 1
    else:
        by_folder["(no folder)"] += 1

print("Chunks by folder:")
for folder in sorted(by_folder.keys()):
    print(f"  {folder}: {by_folder[folder]}")

print(f"\nTotal: {sum(by_folder.values())}")

# Check for kb/whatsapp specifically
whatsapp = [c for c in chunks if "whatsapp" in c.get("source", "")]
print(f"\nChunks containing 'whatsapp' in source: {len(whatsapp)}")

bizai = [c for c in chunks if "bizai" in c.get("source", "")]
print(f"Chunks containing 'bizai' in source: {len(bizai)}")

new_whatsapp = [c for c in chunks if c.get("source", "").startswith("kb/whatsapp/")]
print(f"Chunks from kb/whatsapp/ folder: {len(new_whatsapp)}")

new_bizai = [c for c in chunks if c.get("source", "").startswith("kb/bizai/")]
print(f"Chunks from kb/bizai/ folder: {len(new_bizai)}")
