#!/usr/bin/env python3
"""P0 regression suite for skill/kb_answer.py guardrails fixes."""
import json
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
# Disable telemetry side effects if possible
os.environ.setdefault("KB_DISABLE_LANGFUSE", "1")

from kb_answer import (  # noqa: E402
    _load_chunks,
    _score_chunk,
    _extract_entities,
    _detect_module,
    MIN_CHUNK_SCORE,
)

context = _Context(env_vars)

results = []


def add(name, expected, actual):
    passed = (expected == actual)
    results.append({
        "test": name,
        "expected": expected,
        "actual": actual,
        "pass": passed,
    })


# ---------------- _detect_module tests ----------------
add("1. _detect_module('Meta Business Agent overview')",
    "WhatsApp", _detect_module("Meta Business Agent overview"))
add("2. _detect_module('Deploy my agent to WhatsApp')",
    "SuperAgent", _detect_module("Deploy my agent to WhatsApp"))
add("3. _detect_module('What is SuperAgent?')",
    "SuperAgent", _detect_module("What is SuperAgent?"))
add("4. _detect_module('Agent Assist for support')",
    "Agent Assist", _detect_module("Agent Assist for support"))
add("5. _detect_module('Agent for WhatsApp')",
    "WhatsApp", _detect_module("Agent for WhatsApp"))
add("6. _detect_module('How do I build an agent?')",
    "SuperAgent", _detect_module("How do I build an agent?"))


# ---------------- integration helpers ----------------
CHUNKS = _load_chunks(context)


def search(query, top_n=5):
    module = _detect_module(query)
    entities = _extract_entities(query)
    scored = []
    for c in CHUNKS:
        s = _score_chunk(query, c, entities, module)
        if s >= MIN_CHUNK_SCORE:
            row = dict(c)
            row["score"] = s
            scored.append(row)
    scored.sort(key=lambda x: x.get("score", 0.0), reverse=True)
    top = scored[:top_n]
    top_source = str(top[0].get("source") or "") if top else ""
    top_score = top[0].get("score", 0.0) if top else 0.0
    confidence = min(1.0, max(0.0, top_score / 8.0))
    return top_source, confidence, top


# 7. BizAI pricing -> top_source in kb/bizai/
src7, conf7, _ = search("What is BizAI pricing?")
add("7. kb_answer('What is BizAI pricing?') top_source in kb/bizai/",
    True, "/bizai/" in ("/" + src7.replace("\\", "/").lower()))

# 8. WhatsApp API reference -> top_source in kb/whatsapp/
src8, conf8, _ = search("WhatsApp API reference")
add("8. kb_answer('WhatsApp API reference') top_source in kb/whatsapp/",
    True, "/whatsapp/" in ("/" + src8.replace("\\", "/").lower()))

# 9. SuperAgent usage -> confidence >= 0.7
src9, conf9, _ = search("How do I use SuperAgent?")
add("9. kb_answer('How do I use SuperAgent?') confidence >= 0.7",
    True, conf9 >= 0.7)

# 10. Agent Assist -> confidence >= 0.8
src10, conf10, _ = search("What is Agent Assist?")
add("10. kb_answer('What is Agent Assist?') confidence >= 0.8",
    True, conf10 >= 0.8)

# Extra detail for integration tests
extra = {
    "test7_top_source": src7, "test7_confidence": round(conf7, 4),
    "test8_top_source": src8, "test8_confidence": round(conf8, 4),
    "test9_top_source": src9, "test9_confidence": round(conf9, 4),
    "test10_top_source": src10, "test10_confidence": round(conf10, 4),
}

failed = [r["test"] for r in results if not r["pass"]]
summary = {
    "results": results,
    "extra": extra,
    "total": len(results),
    "passed": sum(1 for r in results if r["pass"]),
    "failed_count": len(failed),
    "failed_tests": failed,
    "all_passed": len(failed) == 0,
}
print(json.dumps(summary, indent=2))
