#!/usr/bin/env python3
"""
Test both ACCURACY and CONSULTING-TONE quality.

Consulting-tone only makes sense when accuracy is high.
Avoid confident false positives.

Metrics:
  1. ACCURACY: Is the answer correct for the question?
  2. CONSULTING-QUALITY: Does consulting-tone add value (or just dress up wrong answers)?
  3. WASTED-TOKENS: Does consulting-tone increase length without improving accuracy?

Run: python3 local/scripts/test_accuracy_and_consulting.py
"""

import os
import json
import ssl
import urllib.request
import uuid
from datetime import datetime

def load_env():
    """Load .env file."""
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        os.environ.setdefault(parts[0], parts[1])

def test_query(query, expected_answer_keywords, expected_structure=None):
    """
    Test a query for accuracy and consulting-tone quality.

    Args:
        query: User question
        expected_answer_keywords: List of keywords that MUST appear in correct answer
        expected_structure: Optional. If "consulting", verify consulting-tone format

    Returns: Dict with accuracy, structure, token_count, assessment
    """
    load_env()

    api_url = os.environ.get('SUPERAGENT_API_URL', '')
    api_key = os.environ.get('SUPERAGENT_API_KEY', '')
    user_email = os.environ.get('USER_EMAIL', 'test@example.com')

    if not api_url or not api_key:
        return {
            'query': query,
            'error': 'Missing SUPERAGENT_API_URL or SUPERAGENT_API_KEY',
        }

    session_id = f"test-{uuid.uuid4().hex[:12]}"

    payload = {
        "message": query,
        "session_id": session_id,
        "user_email_id": user_email,
    }

    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': api_key,
    }

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode(),
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
            response_text = response.read().decode()
            answer = ''

            for line in response_text.strip().split('\n'):
                if line.startswith('data: '):
                    try:
                        chunk = json.loads(line[6:])
                        if 'content' in chunk:
                            answer += chunk['content']
                    except json.JSONDecodeError:
                        continue

            # ============================================================
            # ACCURACY CHECK: Do expected keywords appear?
            # ============================================================
            answer_lower = answer.lower()
            matched_keywords = [kw for kw in expected_answer_keywords
                              if kw.lower() in answer_lower]
            accuracy_score = len(matched_keywords) / len(expected_answer_keywords) * 100 \
                           if expected_answer_keywords else 0

            if accuracy_score >= 80:
                accuracy_status = '✅ HIGH'
            elif accuracy_score >= 50:
                accuracy_status = '⚠️  MEDIUM'
            else:
                accuracy_status = '❌ LOW'

            # ============================================================
            # CONSULTING-TONE STRUCTURE CHECK
            # ============================================================
            consulting_markers = {
                'diagnosis': any(p in answer_lower for p in
                               ['let', 'here', 'to set', 'to prevent', 'figure out']),
                'context': any(p in answer_lower for p in
                             ['depend', 'vary', 'setup', 'scenario', 'context']),
                'options': '-' in answer or '•' in answer,
                'recommended': 'most common' in answer_lower or 'recommended' in answer_lower,
                'followup': 'tell me' in answer_lower or 'more detail' in answer_lower or 'clarif' in answer_lower,
            }

            consulting_score = sum(1 for v in consulting_markers.values() if v) / len(consulting_markers) * 100
            paragraphs = len([p for p in answer.split('\n\n') if p.strip()])

            # ============================================================
            # ASSESSMENT: Consulting-tone appropriate for accuracy level?
            # ============================================================
            if accuracy_score >= 80:
                if consulting_score >= 60:
                    assessment = '✅ GOOD: Accurate answer with proper consulting structure'
                else:
                    assessment = '⚠️  UNDERUTILIZED: Accurate but could use consulting structure'
            else:
                if consulting_score >= 60:
                    assessment = '❌ RISKY: Consulting-tone dresses up inaccurate answer (false confidence)'
                else:
                    assessment = '❌ POOR: Inaccurate answer without consulting structure'

            return {
                'query': query,
                'answer_preview': answer[:150],
                'answer_length': len(answer),
                'accuracy_score': round(accuracy_score, 1),
                'accuracy_status': accuracy_status,
                'matched_keywords': matched_keywords,
                'missed_keywords': [kw for kw in expected_answer_keywords if kw.lower() not in answer_lower],
                'consulting_markers': consulting_markers,
                'consulting_score': round(consulting_score, 1),
                'paragraphs': paragraphs,
                'assessment': assessment,
            }

    except Exception as e:
        return {
            'query': query,
            'error': str(e),
        }

def main():
    print("=" * 120)
    print("ACCURACY + CONSULTING-TONE QUALITY TEST")
    print("=" * 120)
    print()
    print("Philosophy: Consulting-tone only adds value when accuracy is high.")
    print("Confident false positives waste tokens and mislead users.")
    print()

    test_cases = [
        {
            'query': 'How do I prevent infinite loops in Bot Studio journeys?',
            'keywords': ['infinite', 'loop', 'prevention', 'journey', 'condition', 'node'],
            'description': 'Loop prevention (should be accurate)',
        },
        {
            'query': 'How do I use conditional branching to route users in Bot Studio?',
            'keywords': ['conditional', 'branching', 'route', 'decision', 'node', 'logic'],
            'description': 'Conditional routing (retrieval issue identified)',
        },
        {
            'query': 'What are the best practices for multi-turn Bot Studio journeys?',
            'keywords': ['multi-turn', 'state', 'context', 'session', 'memory', 'conversation'],
            'description': 'Multi-turn patterns (retrieval issue identified)',
        },
        {
            'query': 'How do I handle errors in Bot Studio API nodes?',
            'keywords': ['error', 'handling', 'api', 'retry', 'fallback', 'recovery'],
            'description': 'Error handling (may have content)',
        },
        {
            'query': 'How do I use webhooks to integrate external services?',
            'keywords': ['webhook', 'integration', 'external', 'api', 'callback', 'event'],
            'description': 'Webhook integration (general coverage)',
        },
    ]

    results = []

    for i, test in enumerate(test_cases):
        print(f"\n{i+1}. {test['description']}")
        print(f"   Query: {test['query'][:80]}")
        print("-" * 120)

        result = test_query(test['query'], test['keywords'])

        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            results.append(result)
            continue

        print(f"\n📊 ACCURACY:")
        print(f"  Status: {result['accuracy_status']} ({result['accuracy_score']}%)")
        print(f"  Matched: {len(result['matched_keywords'])}/{len(test['keywords'])} keywords")
        if result['matched_keywords']:
            print(f"    ✓ {', '.join(result['matched_keywords'][:3])}")
        if result['missed_keywords']:
            print(f"    ✗ {', '.join(result['missed_keywords'][:2])}")

        print(f"\n📝 CONSULTING-TONE STRUCTURE:")
        print(f"  Score: {result['consulting_score']}%")
        for marker, found in result['consulting_markers'].items():
            status = '✅' if found else '❌'
            print(f"    {status} {marker.capitalize()}")
        print(f"  Paragraphs: {result['paragraphs']}")

        print(f"\n🎯 ASSESSMENT:")
        print(f"  {result['assessment']}")
        print(f"  Tokens used: {result['answer_length']} chars ≈ {result['answer_length']//4} tokens")
        print(f"\n  Answer preview:")
        print(f"  \"{result['answer_preview']}...\"")

        results.append(result)

    # ============================================================
    # SUMMARY
    # ============================================================
    print("\n")
    print("=" * 120)
    print("SUMMARY")
    print("=" * 120)
    print()

    high_accuracy = sum(1 for r in results if r.get('accuracy_score', 0) >= 80)
    medium_accuracy = sum(1 for r in results if 50 <= r.get('accuracy_score', 0) < 80)
    low_accuracy = sum(1 for r in results if r.get('accuracy_score', 0) < 50)

    high_consulting = sum(1 for r in results if r.get('consulting_score', 0) >= 60)
    low_consulting = sum(1 for r in results if r.get('consulting_score', 0) < 60)

    print(f"Accuracy breakdown:")
    print(f"  ✅ High (≥80%): {high_accuracy}")
    print(f"  ⚠️  Medium (50-80%): {medium_accuracy}")
    print(f"  ❌ Low (<50%): {low_accuracy}")
    print()

    print(f"Consulting-tone usage:")
    print(f"  ✅ Strong (≥60% markers): {high_consulting}")
    print(f"  ❌ Weak (<60% markers): {low_consulting}")
    print()

    # Risk assessment
    false_confidence = sum(1 for r in results
                          if r.get('accuracy_score', 0) < 50 and r.get('consulting_score', 0) >= 60)
    if false_confidence > 0:
        print(f"⚠️  WARNING: {false_confidence} query/queries have consulting-tone but low accuracy")
        print(f"   This creates false confidence. Disable consulting-tone or fix retrieval first.")
        print()

    well_used = sum(1 for r in results
                   if r.get('accuracy_score', 0) >= 80 and r.get('consulting_score', 0) >= 60)
    print(f"✅ Well-used consulting-tone: {well_used}/{len(results)}")
    print()

    # Recommendations
    print("RECOMMENDATIONS:")
    print()
    if low_accuracy > 0:
        print(f"1. FIX RETRIEVAL FIRST: {low_accuracy} queries have low accuracy")
        print("   - Don't enable consulting-tone on low-accuracy queries")
        print("   - Focus on KB content and ranking improvements")
        print()

    if false_confidence > 0:
        print(f"2. DISABLE FOR LOW-ACCURACY: Turn off consulting-tone for {false_confidence} queries")
        print("   - Consulting structure shouldn't dress up wrong answers")
        print()

    if well_used > 0:
        print(f"3. CONSULTING-TONE WORKING: {well_used} queries benefit from structure")
        print("   - Use on high-accuracy, complex queries")
        print("   - Especially for setup/patterns with multiple options")
        print()

    print("NEXT STEPS:")
    if low_accuracy > 0:
        print("- Run KB retrieval optimization (see KB_RETRIEVAL_OPTIMIZATION_PLAN.md)")
        print("- Re-run this test after KB fixes")
        print("- Only enable consulting-tone once accuracy reaches ≥75%")

    # Save results
    output_file = 'local/reports/accuracy_consulting_test_results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.utcnow().isoformat(),
            'results': results,
            'summary': {
                'total': len(results),
                'high_accuracy': high_accuracy,
                'medium_accuracy': medium_accuracy,
                'low_accuracy': low_accuracy,
                'high_consulting': high_consulting,
                'false_confidence': false_confidence,
                'well_used_consulting': well_used,
            }
        }, f, indent=2)

    print(f"\n📁 Results saved to: {output_file}")

if __name__ == '__main__':
    main()
