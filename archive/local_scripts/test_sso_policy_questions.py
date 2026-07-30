#!/usr/bin/env python3
"""
Test SSO document with high-level policy questions using kb_answer.

Tests 5 specific policy questions:
1. Does Gupshup Console support Single Sign-On?
2. What identity providers does Console SSO support?
3. Can my organization use SAML 2.0 with Console?
4. Do I need admin access to set up Console SSO?
5. What certificate formats are accepted for SSO?
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


def score_answer_quality(answer: str, question: str) -> int:
    """
    Score answer quality 0-10 for policy questions.

    Quality levels:
    10 = Directly and completely answers the policy/yes-no question with specific details
    8-9 = Directly answers the question with substantive details
    6-7 = Answers the question but with limited detail or some tangential content
    4-5 = Partially addresses the question or mostly relevant
    1-3 = Tangentially related but doesn't directly answer
    0 = Not relevant or no answer
    """
    if not answer or len(answer.strip()) < 20:
        return 0

    answer_lower = answer.lower()
    question_lower = question.lower()

    # Question 1: Does Gupshup Console support Single Sign-On?
    if "support" in question_lower and "single sign-on" in question_lower:
        if "sso" in answer_lower and "console" in answer_lower:
            if "yes" in answer_lower or "support" in answer_lower or "enable" in answer_lower:
                if any(x in answer_lower for x in ["saml", "identity provider", "idp", "authenticat"]):
                    return 10
            if "sso" in answer_lower and len(answer) > 100:
                return 8
        return 0

    # Question 2: What identity providers does Console SSO support?
    if "identity provider" in question_lower or "idp" in question_lower:
        if "active directory" in answer_lower or "azure" in answer_lower:
            if "saml" in answer_lower:
                if len(answer) > 150:
                    return 10
                return 8
        if any(x in answer_lower for x in ["identity provider", "idp", "active directory"]):
            return 6
        return 1

    # Question 3: Can my organization use SAML 2.0 with Console?
    if "saml" in question_lower and "console" in question_lower:
        if "saml" in answer_lower and "yes" in answer_lower:
            if "saml 2.0" in answer_lower or "saml2" in answer_lower.replace(" ", ""):
                return 10
        if "saml" in answer_lower and "console" in answer_lower:
            if len(answer) > 100:
                return 9
            return 7
        return 0

    # Question 4: Do I need admin access to set up Console SSO?
    if "admin access" in question_lower or "admin" in question_lower and "setup" in question_lower:
        if "admin" in answer_lower and ("prerequisite" in answer_lower or "required" in answer_lower or "need" in answer_lower):
            return 10
        if "admin" in answer_lower and "sso" in answer_lower:
            if len(answer) > 80:
                return 8
            return 6
        return 1

    # Question 5: What certificate formats are accepted for SSO?
    if "certificate" in question_lower and ("format" in question_lower or "accepted" in question_lower):
        if ("pem" in answer_lower or "cer" in answer_lower) and "certificate" in answer_lower:
            if "format" in answer_lower:
                return 10
            if len(answer) > 80:
                return 9
        if "certificate" in answer_lower and len(answer) > 100:
            return 7
        if "certificate" in answer_lower:
            return 5
        return 0

    # Generic scoring for SSO-related content
    if any(kw in answer_lower for kw in ["sso", "saml", "identity", "authentication", "certificate"]):
        if len(answer) > 200:
            return 5
        elif len(answer) > 100:
            return 3
        else:
            return 1
    return 0


def main() -> int:
    print("=" * 80)
    print("SSO POLICY QUESTIONS TEST - KB ANSWER VERIFICATION")
    print("=" * 80)

    # Load env and import kb_answer
    env_vars = load_env()
    os.environ.update(env_vars)

    try:
        from kb_answer import kb_answer
        print("\nkb_answer imported successfully")
    except Exception as e:
        print(f"\nERROR importing kb_answer: {e}")
        return 1

    context = _Context(env_vars)

    # The 5 policy test questions
    test_cases = [
        {
            "id": "q1_sso_support",
            "question": "Does Gupshup Console support Single Sign-On?",
            "expected_keywords": ["sso", "console", "support", "saml"],
        },
        {
            "id": "q2_identity_providers",
            "question": "What identity providers does Console SSO support?",
            "expected_keywords": ["identity provider", "idp", "active directory", "azure"],
        },
        {
            "id": "q3_saml_support",
            "question": "Can my organization use SAML 2.0 with Console?",
            "expected_keywords": ["saml", "console", "yes", "support"],
        },
        {
            "id": "q4_admin_access",
            "question": "Do I need admin access to set up Console SSO?",
            "expected_keywords": ["admin", "access", "prerequisite", "required"],
        },
        {
            "id": "q5_certificate_format",
            "question": "What certificate formats are accepted for SSO?",
            "expected_keywords": ["certificate", "format", "pem", "cer"],
        },
    ]

    results = []
    passed = 0
    failed = 0

    for test in test_cases:
        question = test["question"]
        print(f"\nQuestion {test['id']}: {question}")

        try:
            result = kb_answer({"query": question}, context=context)
            answer = result.get("answer", "")
            metadata = (result.get("langfuse") or {}).get("metadata", {})

            answered = metadata.get("answered", False)
            top_source = metadata.get("top_source", "N/A")
            confidence = metadata.get("confidence", 0.0)

            # Quality score
            quality_score = score_answer_quality(answer, question)

            # Did it answer with good quality?
            answered_well = (quality_score >= 7 and answered) or quality_score >= 8

            status = "PASS" if answered_well else "FAIL"

            print(f"  [{status}]")
            print(f"  Quality: {quality_score}/10 | Confidence: {confidence:.3f} | Source: {top_source}")

            if answer:
                # Show snippet
                snippet = answer[:300] if len(answer) > 300 else answer
                snippet = snippet.replace("\n", " ")
                print(f"  Snippet: {snippet}")
            else:
                print(f"  Snippet: (no answer)")

            results.append({
                "question": question,
                "answered": answered,
                "quality": quality_score,
                "snippet": answer[:200] if answer else "",
                "top_source": top_source,
                "confidence": float(confidence),
            })

            if answered_well:
                passed += 1
            else:
                failed += 1

        except Exception as e:
            print(f"  [ERROR] {e}")
            results.append({
                "question": question,
                "error": str(e),
                "answered": False,
                "quality": 0,
            })
            failed += 1

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")

    # Calculate average quality
    quality_scores = [r.get("quality", 0) for r in results if "quality" in r]
    avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
    print(f"Average Quality Score: {avg_quality:.2f}/10")

    # Final output
    test_results = []
    for i, result in enumerate(results, 1):
        test_results.append({
            "question": result["question"],
            "answered": result.get("answered", False),
            "quality": result.get("quality", 0),
            "snippet": result.get("snippet", ""),
        })

    output = {
        "test_results": test_results,
        "summary": {
            "passed": passed,
            "failed": failed,
            "avg_quality": round(avg_quality, 2),
        }
    }

    print("\n" + "=" * 80)
    print("JSON OUTPUT")
    print("=" * 80)
    print(json.dumps(output, indent=2))

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
