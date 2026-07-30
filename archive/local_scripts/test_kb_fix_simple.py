#!/usr/bin/env python3
"""
Simple test of BizAI and WhatsApp KB retrieval after fix.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional

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


def load_env() -> Dict[str, str]:
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


def main() -> int:
    print("=" * 80)
    print("KB FIX VERIFICATION TEST")
    print("=" * 80)

    # Load env and import kb_answer
    env_vars = load_env()
    os.environ.update(env_vars)

    try:
        from kb_answer import kb_answer
        print("\n✓ kb_answer imported successfully")
    except Exception as e:
        print(f"\n✗ ERROR importing kb_answer: {e}")
        return 1

    context = _Context(env_vars)

    # Test queries
    test_cases = [
        {
            "id": "bizai_overview",
            "query": "What is BizAI and what does it do?",
            "expect_confidence_gt": 0.2,
            "expect_sources_gt": 0,
        },
        {
            "id": "whatsapp_pricing",
            "query": "What is WhatsApp API pricing?",
            "expect_confidence_gt": 0.2,
            "expect_sources_gt": 0,
        },
        {
            "id": "bizai_architecture",
            "query": "Explain BizAI architecture",
            "expect_confidence_gt": 0.2,
            "expect_sources_gt": 0,
        },
        {
            "id": "whatsapp_api",
            "query": "How do I use WhatsApp API?",
            "expect_confidence_gt": 0.2,
            "expect_sources_gt": 0,
        },
    ]

    results = []
    passed = 0
    failed = 0

    for test in test_cases:
        print(f"\nTesting: {test['id']}")
        print(f"  Query: {test['query'][:60]}...")

        try:
            result = kb_answer({"query": test["query"]}, context=context)
            answer = result.get("answer", "")
            metadata = (result.get("langfuse") or {}).get("metadata", {})

            confidence = metadata.get("confidence", 0.0)
            source_count = metadata.get("source_count", 0)
            top_source = metadata.get("top_source", "N/A")
            answered = metadata.get("answered", False)

            # Check expectations
            conf_ok = confidence > test["expect_confidence_gt"]
            sources_ok = source_count > test["expect_sources_gt"]

            status = "✓ PASS" if (conf_ok and sources_ok) else "✗ FAIL"

            print(f"  {status}")
            print(f"    Confidence: {confidence:.3f} (expect > {test['expect_confidence_gt']})")
            print(f"    Sources: {source_count} (expect > {test['expect_sources_gt']})")
            print(f"    Top source: {top_source}")
            print(f"    Answered: {answered}")
            print(f"    Answer preview: {answer[:100]}...")

            results.append({
                "id": test["id"],
                "query": test["query"],
                "confidence": confidence,
                "source_count": source_count,
                "top_source": top_source,
                "answered": answered,
                "passed": conf_ok and sources_ok,
            })

            if conf_ok and sources_ok:
                passed += 1
            else:
                failed += 1

        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            import traceback
            traceback.print_exc()
            results.append({"id": test["id"], "query": test["query"], "error": str(e), "passed": False})
            failed += 1

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")

    # Save results
    report = {
        "timestamp": datetime.now().isoformat() if "datetime" not in dir() else "N/A",
        "passed": passed,
        "failed": failed,
        "results": results,
    }

    report_path = REPO_ROOT / "local" / "reports" / "kb_fix_test_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nReport saved to {report_path}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    from datetime import datetime
    sys.exit(main())
