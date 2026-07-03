#!/usr/bin/env python3
"""
Debug _kb_read_text to see what's actually being fetched
"""

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

# Import the internal functions
from kb_answer import _kb_read_text, _kb_cfg
import json

context = _Context(env_vars)

# Get config
cfg = _kb_cfg(context)
print(f"KB Config: {cfg}")

# Read raw chunks
raw = _kb_read_text("kb/kb_chunks.jsonl", context)

# Parse
lines = raw.splitlines()
print(f"\nTotal lines fetched: {len(lines)}")

# Count unique sources
sources = {}
for i, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue
    try:
        obj = json.loads(line)
        source = obj.get("source", "")
        if source not in sources:
            sources[source] = 0
        sources[source] += 1
    except:
        pass

print(f"Unique sources: {len(sources)}")

# Show what folders are present
folders = {}
for source in sources:
    if "/" in source:
        folder = source.split("/")[1]
        if folder not in folders:
            folders[folder] = 0
        folders[folder] += sources[source]

print("\nChunks by folder in fetched data:")
for folder in sorted(folders.keys()):
    print(f"  {folder}: {folders[folder]}")

# Check specifically for whatsapp
whatsapp_raw = [line for line in lines if "whatsapp" in line and "kb/whatsapp/" in line]
print(f"\nLines containing 'kb/whatsapp/': {len(whatsapp_raw)}")
EOF
