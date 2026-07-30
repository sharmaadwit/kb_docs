#!/usr/bin/env python3
"""
Test SSO document by querying kb_answer with SSO-related questions.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

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


def check_sso_content(answer: str) -> tuple[bool, bool]:
    """
    Check if answer contains SSO/SAML/IAM setup keywords.
    Returns (found_sso_content, mentioned_sso_saml_iam)
    """
    answer_lower = answer.lower()

    # Check if it mentions SSO, SAML, or IAM
    has_sso_saml_iam = any(keyword in answer_lower for keyword in ["sso", "saml", "iam", "single sign-on", "identity provider", "idp", "azure ad"])

    # Check if it's actually about the SSO document (has substantive content)
    sso_keywords = ["sso", "single sign-on", "saml", "identity provider", "idp", "console", "authentication"]
    found_sso_content = sum(1 for kw in sso_keywords if kw in answer_lower) >= 2

    return found_sso_content, has_sso_saml_iam


def score_answer_quality(answer: str, question: str) -> int:
    """
    Score answer quality 0-10.
    10 = directly answers the question with specific details
    7-9 = answers the question with some details
    4-6 = partially addresses the question
    1-3 = mentions relevant topic but doesn't directly answer
    0 = not relevant or no answer
    """
    if not answer or len(answer.strip()) < 20:
        return 0

    answer_lower = answer.lower()
    question_lower = question.lower()

    # Check for specific relevant keywords based on question
    if "single sign-on" in question_lower or "support" in question_lower:
        if "console" in answer_lower and ("saml" in answer_lower or "sso" in answer_lower):
            if len(answer) > 100:
                return 9
            return 6

    if "set up" in question_lower:
        if "setup" in answer_lower or "configure" in answer_lower or "settings" in answer_lower:
            if len(answer) > 150:
                return 9
            return 7

    if "parameters" in question_lower:
        if "url" in answer_lower and "certificate" in answer_lower:
            if "acs" in answer_lower or "entity id" in answer_lower:
                return 10
            return 8
        if any(param in answer_lower for param in ["parameter", "configure", "setting"]):
            return 6

    if "azure" in question_lower:
        if "azure" in answer_lower and "ad" in answer_lower:
            if len(answer) > 150:
                return 9
            return 7
        if "idp" in answer_lower or "identity provider" in answer_lower:
            return 6

    if "certificate" in question_lower:
        if "certificate" in answer_lower or "cert" in answer_lower:
            if "pem" in answer_lower or "cer" in answer_lower or "format" in answer_lower:
                return 10
            return 8
        return 3

    # Generic SSO-related answer
    if any(kw in answer_lower for kw in ["sso", "saml", "identity", "authentication"]):
        if len(answer) > 200:
            return 7
        elif len(answer) > 100:
            return 5
        else:
            return 3

    return 0


def main() -> int:
    print("=" * 80)
    print("SSO DOCUMENT TEST - KB ANSWER VERIFICATION")
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
            "id": "sso_support",
            "query": "Does Gupshup Console support Single Sign-On via SAML 2.0?",
        },
        {
            "id": "sso_setup",
            "query": "How do I set up SSO for Console?",
        },
        {
            "id": "sso_parameters",
            "query": "What parameters are needed for SSO integration?",
        },
        {
            "id": "azure_integration",
            "query": "How do I integrate Azure AD with Console?",
        },
        {
            "id": "certificate_format",
            "query": "What certificate format is needed for SSO?",
        },
    ]

    results = []
    passed = 0
    failed = 0

    for test in test_cases:
        print(f"\nTesting: {test['id']}")
        print(f"  Query: {test['query']}")

        try:
            result = kb_answer({"query": test["query"]}, context=context)
            answer = result.get("answer", "")
            metadata = (result.get("langfuse") or {}).get("metadata", {})

            answered = metadata.get("answered", False)
            top_source = metadata.get("top_source", "N/A")
            confidence = metadata.get("confidence", 0.0)

            # Check if SSO content found and quality
            found_sso_content, has_sso_keywords = check_sso_content(answer)
            quality_score = score_answer_quality(answer, test["query"])

            # Pass criteria: found SSO content AND quality > 5 OR answered flag is true
            passed_test = (found_sso_content and quality_score >= 6) or answered

            status = "✓ PASS" if passed_test else "✗ FAIL"

            print(f"  {status}")
            print(f"    Found SSO Content: {found_sso_content}")
            print(f"    Has SSO/SAML/IAM Keywords: {has_sso_keywords}")
            print(f"    Quality Score: {quality_score}/10")
            print(f"    Top source: {top_source}")
            print(f"    Confidence: {confidence:.3f}")
            print(f"    Answered: {answered}")
            if answer:
                print(f"    Answer preview: {answer[:150]}...")

            results.append({
                "question": test["query"],
                "found_sso_content": found_sso_content,
                "has_sso_keywords": has_sso_keywords,
                "quality_score": quality_score,
                "answer_snippet": answer[:200] if answer else "",
                "top_source": top_source,
                "confidence": confidence,
                "answered": answered,
                "passed": passed_test,
            })

            if passed_test:
                passed += 1
            else:
                failed += 1

        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            import traceback
            traceback.print_exc()
            results.append({
                "question": test["query"],
                "error": str(e),
                "passed": False,
            })
            failed += 1

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")

    # Calculate average quality
    quality_scores = [r.get("quality_score", 0) for r in results if "quality_score" in r]
    avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
    print(f"Average Quality Score: {avg_quality:.2f}/10")

    # Save results
    report = {
        "test_results": results,
        "summary": {
            "passed": passed,
            "failed": failed,
            "total": len(test_cases),
            "avg_quality": avg_quality,
        }
    }

    report_path = REPO_ROOT / "local" / "reports" / "sso_test_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\nReport saved to {report_path}")

    # Also output JSON to stdout for structured response
    print("\n" + "=" * 80)
    print("STRUCTURED RESULTS (JSON)")
    print("=" * 80)
    print(json.dumps(report, indent=2))

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
