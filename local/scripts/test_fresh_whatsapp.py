#!/usr/bin/env python3
"""
Test WhatsApp after fresh import
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

from kb_answer import kb_answer

context = _Context(env_vars)

result = kb_answer({"query": "What is WhatsApp API pricing?"}, context=context)
metadata = (result.get("langfuse") or {}).get("metadata", {})

print(f"Confidence: {metadata.get('confidence')}")
print(f"Sources: {metadata.get('source_count')}")
print(f"Top source: {metadata.get('top_source')}")
print(f"Answer: {result.get('answer', '')[:200]}")
"""

result = subprocess.run([sys.executable, "-c", test_script], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)
print("Return code:", result.returncode)
