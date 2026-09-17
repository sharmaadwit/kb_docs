#!/usr/bin/env python3
"""
Direct kb_answer simulation (not through SuperAgent).

Since kb_answer is exposed as a skill in the Gupshup platform,
we'll simulate calling it with the consulting mode configuration active
and capture the structured response that includes:
- Answer text
- Consulting mode indicators (best practices, resources, follow-ups)
- Confidence score
- Decomposition metadata
"""

import json
import sys
from pathlib import Path

# Add skill directory to path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill"))

# Import kb_answer directly
from kb_answer import kb_answer

REPORT_FILE = ROOT / "local" / "reports" / "consulting_mode_direct_kb_answer.jsonl"


class MockContext:
    """Mock context for local testing."""
    def __init__(self, user_email="gabriel.lucena@gupshup.io"):
        self.user_email = user_email
        self.user_id = "user-consulting-test-001"

    def get_secret(self, name):
        """Mock secret retrieval."""
        secrets = {
            "KB_GIT_PROVIDER": "github",
            "KB_REPO": "gupshup/kb-docs",
            "KB_BRANCH": "main",
            "KB_VIDEO_MANIFEST_PATH": "kb/video_manifest.json",
            "KB_DEMOFORGE_MANIFEST_PATH": "kb/demoforge_manifest.json",
        }
        return secrets.get(name)


def call_kb_answer(query: str, user_email: str = "gabriel.lucena@gupshup.io") -> dict:
    """Call kb_answer directly with mock context."""
    context = MockContext(user_email)

    try:
        result = kb_answer(
            parameters={
                "query": query,
                "user_email": user_email,
                "module": "Bot Studio",
            },
            context=context
        )
        return {
            "status": "success",
            "response": result,
            "query": query,
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "query": query,
        }


def extract_consulting_indicators(response: dict) -> dict:
    """Extract consulting mode characteristics from response."""
    answer = response.get("response", {}).get("answer", "")

    return {
        "has_structure": any(x in answer for x in ["###", "##", "**", "→", "✅"]),
        "has_best_practices": any(x in answer for x in ["Best Practice", "best practice", "✅"]),
        "has_resources": any(x in answer for x in ["video", "template", "demo", "case study", "Video"]),
        "has_follow_ups": any(x in answer for x in ["What's next", "Next step", "Reply with", "need more"]),
        "has_confidence": "confidence" in answer.lower(),
        "answer_length": len(answer),
        "decomposition": response.get("response", {}).get("decomposition"),
        "confidence_score": response.get("response", {}).get("confidence"),
    }


def main():
    print("=" * 80)
    print("CONSULTING MODE DIRECT KB_ANSWER SIMULATION")
    print("=" * 80)
    print()

    user_email = "gabriel.lucena@gupshup.io"

    turns = [
        (
            1,
            "How do I set up a WhatsApp bot in Bot Studio that asks for customer feedback after an order confirmation?",
            "Bot Studio - Setup Feedback Bot"
        ),
        (
            2,
            "Can I personalize the feedback prompt based on the product category? Like, ask about shipping speed for electronics but product quality for clothing?",
            "Bot Studio - Personalization by Category"
        ),
        (
            3,
            "This is great. But how do I handle the API call to my order system if it's slow? The feedback prompt is delaying.",
            "Bot Studio - Performance Optimization"
        ),
    ]

    results = []
    analyses = []

    for turn_num, query, label in turns:
        print(f"\n{'='*80}")
        print(f"TURN {turn_num}: {label}")
        print(f"{'='*80}")
        print(f"\nQuery: {query[:80]}...\n" if len(query) > 80 else f"\nQuery: {query}\n")

        # Call kb_answer
        response = call_kb_answer(query, user_email)

        # Analyze
        analysis = extract_consulting_indicators(response)

        # Report
        if response["status"] == "success":
            answer = response.get("response", {}).get("answer", "")
            print(f"✓ Answer received ({len(answer)} chars)")
            print(f"  Confidence: {analysis.get('confidence_score', 'N/A')}")
            print(f"  Has structure: {analysis['has_structure']}")
            print(f"  Has best practices: {analysis['has_best_practices']}")
            print(f"  Has resources: {analysis['has_resources']}")
            print(f"  Has follow-ups: {analysis['has_follow_ups']}")

            # Print first 500 chars
            preview = answer[:500] if len(answer) > 500 else answer
            print(f"\nAnswer preview:\n{preview}...\n")
        else:
            print(f"✗ Error: {response.get('error')}")

        # Store results
        results.append({
            "turn": turn_num,
            "label": label,
            "status": response["status"],
            "response": response,
            "analysis": analysis,
        })
        analyses.append(analysis)

    # Write results to JSONL
    print(f"\n{'='*80}")
    print("SAVING RESULTS")
    print(f"{'='*80}\n")

    with open(REPORT_FILE, "a") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")

    print(f"✓ Full results saved to: {REPORT_FILE}")

    # Summary
    print(f"\n{'='*80}")
    print("CONSULTING MODE ANALYSIS")
    print(f"{'='*80}\n")

    for analysis in analyses:
        turn = analyses.index(analysis) + 1
        print(f"Turn {turn}:")
        print(f"  Answer length: {analysis['answer_length']} chars")
        print(f"  Has structure: {analysis['has_structure']}")
        print(f"  Has best practices: {analysis['has_best_practices']}")
        print(f"  Has resources: {analysis['has_resources']}")
        print(f"  Has follow-ups: {analysis['has_follow_ups']}")
        print(f"  Decomposition: {analysis.get('decomposition')}")
        print()

    # Overall metrics
    print(f"{'='*80}")
    print("MULTI-TURN METRICS")
    print(f"{'='*80}\n")

    total_length = sum(a['answer_length'] for a in analyses)
    avg_length = total_length / len(analyses)

    print(f"Total answer length: {total_length} chars")
    print(f"Average per turn: {avg_length:.0f} chars")
    print(f"Consulting mode characteristics:")
    print(f"  Structure in {sum(a['has_structure'] for a in analyses)}/3 turns")
    print(f"  Best practices in {sum(a['has_best_practices'] for a in analyses)}/3 turns")
    print(f"  Resources in {sum(a['has_resources'] for a in analyses)}/3 turns")
    print(f"  Follow-ups in {sum(a['has_follow_ups'] for a in analyses)}/3 turns")

    if avg_length > 1000:
        print(f"\n✅ Answers average {avg_length:.0f} chars (>1000) → consulting mode characteristic")

    if sum(a['has_structure'] for a in analyses) == 3:
        print(f"✅ All turns structured → formatted for readability")

    if sum(a['has_follow_ups'] for a in analyses) >= 2:
        print(f"✅ Follow-ups in 2+ turns → drives multi-turn adoption")


if __name__ == "__main__":
    main()
