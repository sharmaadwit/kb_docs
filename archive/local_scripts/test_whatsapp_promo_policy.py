#!/usr/bin/env python3
"""
Test WhatsApp promotional restrictions document with high-level policy questions.
Tests kb_answer with the specific questions from the test requirements.
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

# The exact test questions as specified
TEST_QUESTIONS = [
    "Can I send promotional messages on WhatsApp Business?",
    "Are there restrictions on dietary supplement promotion via WhatsApp?",
    "Do I need user consent before sending promotional messages?",
    "What types of content violate WhatsApp promotional guidelines?",
    "Can I promote multivitamins on WhatsApp?"
]


def extract_quality_indicators(answer_text, question):
    """Extract quality indicators from answer text."""
    if not answer_text:
        return {"has_policy_info": False, "is_yes_no": False, "is_direct": False}

    text_lower = answer_text.lower()

    # Check for policy/guidance information
    has_policy_info = any(word in text_lower for word in [
        "consent", "bulk", "promotional", "spam", "unwanted", "automated",
        "guidelines", "compliance", "restrictions", "prohibited", "allowed",
        "supplement", "multivitamin", "dietary", "user consent"
    ])

    # Check for direct yes/no answer (for yes/no questions)
    is_yes_no = any(phrase in text_lower for phrase in [
        "yes ", "no ", "allowed", "not allowed", "permitted", "prohibited",
        "can ", "cannot", "must", "required", "necessary"
    ])

    # Check if answer is directly about the question topic
    is_direct = any(word in text_lower for word in [
        "whatsapp", "promotional", "consent", "supplement", "multivitamin"
    ])

    return {
        "has_policy_info": has_policy_info,
        "is_yes_no": is_yes_no,
        "is_direct": is_direct
    }


def score_answer_quality(question, answer_text):
    """Score answer quality from 0-10.

    Criteria:
    - Is it relevant to WhatsApp policy? (base 0-5)
    - Does it directly answer yes/no or policy question? (0-3)
    - Does it provide specific guidance? (0-2)
    """
    if not answer_text or len(answer_text.strip()) < 50:
        return 0

    text_lower = answer_text.lower()
    score = 0

    # Relevance to WhatsApp policy (0-5)
    policy_indicators = [
        ("consent", 1),
        ("promotional", 1),
        ("bulk", 1),
        ("guidelines", 1),
        ("restrictions", 1),
    ]

    for indicator, points in policy_indicators:
        if indicator in text_lower:
            score += points

    # Direct answer to question (0-3)
    question_lower = question.lower()

    if "can i send" in question_lower:
        if any(x in text_lower for x in ["allowed", "yes", "permitted", "can", "before sending"]):
            score += 2
        elif any(x in text_lower for x in ["promotional"]):
            score += 1
    if "restrictions" in question_lower and any(x in text_lower for x in ["restrict", "prohibited", "not", "cannot", "must comply", "not allowed"]):
        score += 2
    if "consent" in question_lower:
        if "consent" in text_lower or "opted in" in text_lower:
            score += 2
        elif "promotional" in text_lower:
            score += 1
    if "types of content" in question_lower and any(x in text_lower for x in ["prohibited", "violate", "not", "cannot", "red flags"]):
        score += 2
    if "multivitamin" in question_lower and "multivitamin" in text_lower:
        score += 2

    # Specific guidance/details (0-2)
    if "user consent" in text_lower or "opted in" in text_lower:
        score += 1
    if any(x in text_lower for x in ["bulk messaging", "automated", "spam", "deceptive"]):
        score += 1

    # Cap at 10
    return min(10, score)


def test_kb_answer():
    """Test kb_answer with the specified policy questions."""

    # Import kb_answer after path setup
    try:
        from kb_answer import kb_answer
    except ImportError as e:
        print(f"Error importing kb_answer: {e}", file=sys.stderr)
        return None

    results = []
    context = MockContext()

    for i, question in enumerate(TEST_QUESTIONS, 1):
        print(f"\n[{i}/5] Testing: {question}")
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
            print(f"Citations found: {len(citations)}")

            # Determine if question was answered
            quality_score = score_answer_quality(question, answer_text)
            indicators = extract_quality_indicators(answer_text, question)

            # Consider answered if score >= 4 (moderate quality)
            answered = quality_score >= 4

            print(f"Quality Score: {quality_score}/10")
            print(f"Answered: {answered}")
            print(f"Has policy info: {indicators['has_policy_info']}")
            print(f"Direct answer: {indicators['is_direct']}")

            # Get snippet of answer
            if len(answer_text) > 250:
                snippet = answer_text[:250] + "..."
            else:
                snippet = answer_text

            result = {
                "question": question,
                "answered": answered,
                "quality": quality_score,
                "snippet": snippet,
                "response_ok": ok,
                "citations_count": len(citations)
            }
            results.append(result)

            if answer_text:
                print(f"Answer preview: {snippet}")

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            result = {
                "question": question,
                "answered": False,
                "quality": 0,
                "snippet": f"Error: {str(e)}",
                "response_ok": False,
                "citations_count": 0
            }
            results.append(result)

    return results


def main():
    """Run tests and output results in the required JSON format."""

    print("=" * 80)
    print("WhatsApp Promotional Restrictions - Policy Question Test")
    print("=" * 80)
    print(f"Testing document: kb/whatsapp-promotional-restrictions.md")
    print(f"Questions: 5 high-level policy questions")
    print()

    results = test_kb_answer()

    if not results:
        print("Failed to run tests", file=sys.stderr)
        sys.exit(1)

    # Calculate summary
    passed = sum(1 for r in results if r.get("answered", False))
    failed = sum(1 for r in results if not r.get("answered", False))
    avg_quality = sum(r.get("quality", 0) for r in results) / len(results) if results else 0

    # Build output JSON in required format
    output = {
        "test_results": [
            {
                "question": r["question"],
                "answered": r.get("answered", False),
                "quality": r.get("quality", 0),
                "snippet": r.get("snippet", "")
            }
            for r in results
        ],
        "summary": {
            "passed": passed,
            "failed": failed,
            "avg_quality": round(avg_quality, 2)
        }
    }

    # Print detailed results to console
    print("\n" + "=" * 80)
    print("Test Results:")
    print("=" * 80)
    for i, r in enumerate(results, 1):
        status = "PASS" if r.get("answered") else "FAIL"
        quality = r.get("quality", 0)
        print(f"\n[{status}] Q{i}: {r['question']}")
        print(f"      Quality: {quality}/10")
        if r.get("snippet"):
            print(f"      Snippet: {r['snippet']}")

    print("\n" + "=" * 80)
    print("Summary:")
    print("=" * 80)
    print(f"Passed: {passed}/5")
    print(f"Failed: {failed}/5")
    print(f"Average Quality: {avg_quality:.2f}/10")
    print("=" * 80)

    # Output JSON to stdout
    print("\nJSON Output:")
    print(json.dumps(output, indent=2))

    return output


if __name__ == "__main__":
    result = main()
    sys.exit(0)
