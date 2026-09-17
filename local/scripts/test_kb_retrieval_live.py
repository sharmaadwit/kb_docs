#!/usr/bin/env python3
"""
Test KB retrieval quality against live SuperAgent runtime using microagent endpoint.

Uses SuperAgent's /api/agents/chat/stream endpoint to test how the KB retriever
is selecting and ranking evidence for specific queries, then analyzes the results
to identify retrieval gaps and ranking issues.

Queries: "prevent infinite loops", "conditional branching", etc.
Output: Retrieved evidence analysis + recommendations for KB setting adjustments

Run: python3 local/scripts/test_kb_retrieval_live.py
"""

import os
import sys
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

def test_kb_retrieval(query, module="Bot Studio"):
    """
    Test KB retrieval for a query via SuperAgent microagent endpoint.

    Returns: (answer, evidence, metadata) or (None, None, error_msg) on failure
    """
    load_env()

    api_url = os.environ.get('SUPERAGENT_API_URL', '')
    api_key = os.environ.get('SUPERAGENT_API_KEY', '')
    org_id = os.environ.get('SUPERAGENT_ORG_ID', '')
    project_id = os.environ.get('SUPERAGENT_PROJECT_ID', '')
    user_email = os.environ.get('USER_EMAIL', 'test@example.com')

    if not api_url or not api_key:
        return None, None, "Missing SUPERAGENT_API_URL or SUPERAGENT_API_KEY in .env"

    # Generate unique session/conversation ID for tracing
    session_id = f"kb-test-{uuid.uuid4().hex[:12]}"

    # Build request payload (tenant_context is optional)
    payload = {
        "message": query,
        "session_id": session_id,
        "user_email_id": user_email,
    }

    # Add tenant context if org_id and project_id are available
    if org_id or project_id:
        payload["tenant_context"] = {}
        if org_id:
            payload["tenant_context"]["org_id"] = org_id
        if project_id:
            payload["tenant_context"]["project_id"] = project_id

    # Prepare request
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': api_key,
    }

    # SSL context (ignore cert for internal testing)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        print(f"🔍 Testing query: {query}")
        print(f"   Module: {module}")
        print(f"   Session: {session_id}")
        print()

        req = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode(),
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
            # Stream response (may contain multiple events/chunks)
            response_text = response.read().decode()

            # Parse streaming JSON responses (one per line)
            answers = []
            evidence_list = []

            for line in response_text.strip().split('\n'):
                if line.startswith('data: '):
                    try:
                        chunk = json.loads(line[6:])

                        # Extract answer content
                        if 'content' in chunk:
                            answers.append(chunk['content'])

                        # Extract evidence/metadata if present
                        if 'metadata' in chunk:
                            evidence_list.append(chunk['metadata'])
                    except json.JSONDecodeError:
                        continue

            answer = ''.join(answers) if answers else ''
            return answer, evidence_list, None

    except urllib.error.HTTPError as e:
        return None, None, f"HTTP {e.code}: {e.reason}"
    except Exception as e:
        return None, None, f"Error: {str(e)}"

def main():
    print("=" * 100)
    print("KB RETRIEVAL QUALITY TEST (Live SuperAgent Runtime)")
    print("=" * 100)
    print()

    # Test queries that have shown retrieval issues
    test_queries = [
        {
            "query": "How do I prevent infinite loops in Bot Studio journeys?",
            "module": "Bot Studio",
            "expected_topic": "loop prevention, infinite loops, journey logic",
        },
        {
            "query": "How do I use conditional branching to route users in Bot Studio?",
            "module": "Bot Studio",
            "expected_topic": "conditional routing, decision nodes, branching",
        },
        {
            "query": "What is the best way to handle complex multi-turn conversations?",
            "module": "Bot Studio",
            "expected_topic": "state management, multi-turn logic",
        },
    ]

    results = []

    for i, test in enumerate(test_queries):
        print(f"\n{i+1}. Testing: {test['query'][:70]}...")
        print("-" * 100)

        answer, evidence, error = test_kb_retrieval(test['query'], test['module'])

        if error:
            print(f"❌ Error: {error}")
            print()
            results.append({
                'query': test['query'],
                'status': 'ERROR',
                'error': error,
            })
            continue

        # Analyze retrieval quality
        if not answer:
            print("⚠️  No answer returned")
            status = 'NO_ANSWER'
        else:
            print(f"Answer length: {len(answer)} chars")

            # Check if answer addresses the expected topic
            answer_lower = answer.lower()
            expected_lower = test['expected_topic'].lower()

            # Simple relevance check
            expected_keywords = expected_lower.split(',')
            matched_keywords = [kw for kw in expected_keywords if kw.strip() in answer_lower]

            relevance = len(matched_keywords) / len(expected_keywords) * 100 if expected_keywords else 0

            if relevance >= 60:
                print(f"✅ Relevant (matched {len(matched_keywords)}/{len(expected_keywords)} expected topics)")
                status = 'GOOD'
            elif relevance >= 30:
                print(f"⚠️  Partially relevant (matched {len(matched_keywords)}/{len(expected_keywords)} expected topics)")
                status = 'PARTIAL'
            else:
                print(f"❌ Poor relevance (matched {len(matched_keywords)}/{len(expected_keywords)} expected topics)")
                status = 'POOR'

            # Show evidence breakdown if available
            if evidence:
                print(f"\nEvidence pieces: {len(evidence)}")
                for j, ev in enumerate(evidence[:3]):
                    print(f"  {j+1}. {str(ev)[:100]}...")

        print(f"Answer preview: {answer[:200]}...")
        print()

        results.append({
            'query': test['query'],
            'module': test['module'],
            'status': status,
            'answer_length': len(answer) if answer else 0,
            'answer_preview': answer[:100] if answer else '',
        })

    # Summary
    print()
    print("=" * 100)
    print("SUMMARY")
    print("=" * 100)
    print()

    good = sum(1 for r in results if r.get('status') == 'GOOD')
    partial = sum(1 for r in results if r.get('status') == 'PARTIAL')
    poor = sum(1 for r in results if r.get('status') == 'POOR')
    errors = sum(1 for r in results if r.get('status') == 'ERROR')

    print(f"Total tests: {len(results)}")
    print(f"  ✅ Good (relevant): {good}")
    print(f"  ⚠️  Partial: {partial}")
    print(f"  ❌ Poor (irrelevant): {poor}")
    print(f"  ❌ Errors: {errors}")
    print()

    if poor > 0:
        print("⚠️  RETRIEVAL ISSUES DETECTED")
        print()
        print("Poor-relevance queries:")
        for r in results:
            if r.get('status') == 'POOR':
                print(f"  • {r['query'][:70]}...")
        print()
        print("Next steps:")
        print("  1. Review KB content for missing/incorrect chunks")
        print("  2. Check retrieval ranking (BM25, embedding similarity)")
        print("  3. Adjust chunking strategy if needed")
        print("  4. Re-test after changes")
    else:
        print("✅ All retrieval tests passed")

    # Save results
    output_file = 'local/reports/kb_retrieval_test_results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.utcnow().isoformat(),
            'results': results,
            'summary': {
                'total': len(results),
                'good': good,
                'partial': partial,
                'poor': poor,
                'errors': errors,
            }
        }, f, indent=2)

    print(f"\n📁 Results saved to: {output_file}")

if __name__ == '__main__':
    main()
