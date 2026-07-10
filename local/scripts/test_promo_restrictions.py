#!/usr/bin/env python3
"""
Test harness for WhatsApp promotional restrictions document.
Tests kb_answer with queries about promotional restrictions, consent, and bulk messaging.
"""

import json
import os
import sys
from pathlib import Path

# Add skill directory to path so we can import kb_answer
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "skill"))

# Mock context since we're testing locally
class MockContext:
    def get_secret(self, name):
        return None

# Test questions
TEST_QUESTIONS = [
    "Can I send promotional messages for dietary supplements on WhatsApp Business?",
    "Are there restrictions on promotional messages for multivitamins?",
    "What are WhatsApp guidelines for promotional content?",
    "Is bulk messaging allowed for supplement promotion?",
    "Do I need user consent to send promotional messages on WhatsApp?",
]

# Keywords that indicate promotional/restriction coverage
PROMO_KEYWORDS = {
    "promotional", "bulk", "consent", "spam", "unwanted", "automated",
    "user consent", "opt-in", "deceptive", "compliance", "restrict"
}

RESTRICT_KEYWORDS = {
    "restrict", "prohibited", "not allowed", "violation", "not permitted",
    "must", "required", "compliance", "guidelines", "bulk", "spam",
    "unwanted contact", "consent required", "not", "no"
}


def check_for_promo_content(answer_text):
    """Check if answer contains promotional restriction content."""
    if not answer_text:
        return False
    text_lower = answer_text.lower()
    return any(kw in text_lower for kw in PROMO_KEYWORDS)


def check_for_restrictions(answer_text):
    """Check if answer mentions promotional restrictions, consent, or bulk messaging rules."""
    if not answer_text:
        return False
    text_lower = answer_text.lower()
    return any(kw in text_lower for kw in RESTRICT_KEYWORDS)


def score_answer_quality(question, answer_text):
    """Score answer quality from 0-10 based on relevance to promotional restrictions."""
    if not answer_text:
        return 0

    text_lower = answer_text.lower()
    score = 0

    # Check for direct mentions of promotional restrictions
    if "promotional" in text_lower and "restrict" in text_lower:
        score += 3

    # Check for consent/user opt-in mentions
    if "consent" in text_lower or "opt-in" in text_lower or "opted" in text_lower:
        score += 2

    # Check for bulk messaging/automation mentions
    if "bulk" in text_lower or "automated" in text_lower or "automation" in text_lower:
        score += 2

    # Check for compliance/guidelines mentions
    if "compliance" in text_lower or "guidelines" in text_lower or "regulations" in text_lower:
        score += 2

    # Check for dietary supplements/multivitamins specific content
    if "dietary" in text_lower or "supplement" in text_lower or "multivitamin" in text_lower:
        score += 1

    # Normalize to 0-10 scale
    return min(10, score)


def test_kb_answer():
    """Test kb_answer with promotional restriction queries."""

    # Import kb_answer after path setup
    try:
        from kb_answer import kb_answer
    except ImportError as e:
        print(f"Error importing kb_answer: {e}")
        return None

    results = []
    context = MockContext()

    for question in TEST_QUESTIONS:
        print(f"\nTesting: {question}")
        print("-" * 80)

        try:
            # Call kb_answer with the question
            response = kb_answer(
                parameters={"query": question},
                context=context
            )

            answer_text = response.get("answer", "")
            citations = response.get("citations", [])
            ok = response.get("ok", False)

            print(f"Response OK: {ok}")
            print(f"Answer length: {len(answer_text)} chars")
            print(f"Citations: {len(citations)}")

            # Check content
            has_promo = check_for_promo_content(answer_text)
            has_restrictions = check_for_restrictions(answer_text)
            quality_score = score_answer_quality(question, answer_text)

            print(f"Found promo content: {has_promo}")
            print(f"Found restrictions/consent: {has_restrictions}")
            print(f"Quality score: {quality_score}/10")

            # Get snippet of answer
            snippet = answer_text[:200] + "..." if len(answer_text) > 200 else answer_text

            result = {
                "question": question,
                "found_promo_content": has_promo,
                "found_restrictions": has_restrictions,
                "quality_score": quality_score,
                "answer_snippet": snippet,
                "response_ok": ok,
                "full_answer": answer_text[:1000],  # Store first 1000 chars for inspection
                "citations_count": len(citations)
            }
            results.append(result)

        except Exception as e:
            print(f"Error: {e}")
            result = {
                "question": question,
                "found_promo_content": False,
                "found_restrictions": False,
                "quality_score": 0,
                "answer_snippet": f"Error: {str(e)}",
                "response_ok": False,
                "error": str(e),
                "citations_count": 0
            }
            results.append(result)

    return results


def main():
    """Run tests and output results."""
    print("=" * 80)
    print("WhatsApp Promotional Restrictions Document - Test Harness")
    print("=" * 80)

    results = test_kb_answer()

    if not results:
        print("Failed to run tests")
        sys.exit(1)

    # Calculate summary
    passed = sum(1 for r in results if r.get("quality_score", 0) >= 6)
    failed = sum(1 for r in results if r.get("quality_score", 0) < 6)
    avg_quality = sum(r.get("quality_score", 0) for r in results) / len(results) if results else 0

    # Build output JSON
    output = {
        "test_results": [
            {
                "question": r["question"],
                "found_promo_content": r.get("found_promo_content", False),
                "found_restrictions": r.get("found_restrictions", False),
                "quality_score": r.get("quality_score", 0),
                "answer_snippet": r.get("answer_snippet", "")
            }
            for r in results
        ],
        "summary": {
            "passed": passed,
            "failed": failed,
            "avg_quality": round(avg_quality, 2)
        }
    }

    # Print JSON output
    print("\n" + "=" * 80)
    print("Test Results JSON:")
    print("=" * 80)
    print(json.dumps(output, indent=2))

    # Print detailed results
    print("\n" + "=" * 80)
    print("Detailed Results:")
    print("=" * 80)
    for i, r in enumerate(results, 1):
        print(f"\n{i}. {r['question']}")
        print(f"   Promo Content Found: {r.get('found_promo_content', False)}")
        print(f"   Restrictions Found: {r.get('found_restrictions', False)}")
        print(f"   Quality Score: {r.get('quality_score', 0)}/10")
        print(f"   Response OK: {r.get('response_ok', False)}")
        if 'error' in r:
            print(f"   Error: {r['error']}")
        else:
            print(f"   Answer Preview: {r.get('answer_snippet', '')}")

    print("\n" + "=" * 80)
    print(f"Summary: {passed} passed, {failed} failed")
    print(f"Average Quality Score: {avg_quality:.2f}/10")
    print("=" * 80)

    return output


if __name__ == "__main__":
    result = main()
    # Exit with appropriate code
    sys.exit(0 if result and result["summary"]["avg_quality"] >= 6 else 1)
