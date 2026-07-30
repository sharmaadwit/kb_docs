#!/usr/bin/env python3
"""
Final test after pushing changes to GitHub
"""

import subprocess
import sys

test_script = """
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

from kb_answer import kb_answer, _load_chunks

context = _Context(env_vars)

# Check chunks loaded
chunks = _load_chunks(context)
print(f"Total chunks loaded: {len(chunks)}")

bizai_chunks = [c for c in chunks if "bizai" in c.get("source", "").lower()]
whatsapp_chunks = [c for c in chunks if "whatsapp" in c.get("source", "").lower()]

print(f"BizAI chunks: {len(bizai_chunks)}")
print(f"WhatsApp chunks: {len(whatsapp_chunks)}")

# Test queries
tests = [
    ("What is BizAI and what does it do?", 0.3),
    ("What is WhatsApp API pricing?", 0.2),
    ("Explain BizAI architecture", 0.3),
]

print("\\nTest Results:")
for query, min_confidence in tests:
    result = kb_answer({"query": query}, context=context)
    metadata = (result.get("langfuse") or {}).get("metadata", {})
    confidence = metadata.get("confidence", 0.0)
    sources = metadata.get("source_count", 0)
    top_source = metadata.get("top_source", "N/A")

    status = "PASS" if confidence >= min_confidence else "FAIL"
    print(f"\\n{status}: {query}")
    print(f"  Confidence: {confidence:.3f} (need {min_confidence})")
    print(f"  Sources: {sources}")
    print(f"  Top: {top_source}")
"""

result = subprocess.run([sys.executable, "-c", test_script], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
