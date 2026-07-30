#!/usr/bin/env python3
"""Test 2 queries and capture trace IDs after separate event removal."""
import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from skill import kb_answer as kb_answer_module

class MockContext:
    def __init__(self):
        self.secrets = {}
        self.user_email = "test@example.com"

    def get_secret(self, key):
        return os.getenv(key)

def test_query(query: str, test_name: str):
    """Run a single query and capture trace."""
    print(f"\n{'='*60}")
    print(f"Test: {test_name}")
    print(f"Query: {query}")
    print('='*60)

    ctx = MockContext()
    corr_id = f"test_{test_name.replace(' ', '_')}_{int(datetime.now().timestamp() * 1000)}"

    try:
        result = kb_answer_module.kb_answer(
            parameters={"query": query},
            context=ctx,
            correlation_id=corr_id
        )

        print(f"\n✓ Query completed")
        print(f"  Correlation ID: {corr_id}")

        # Check if video was attached
        if isinstance(result, dict) and result.get("video_meta"):
            vm = result['video_meta']
            print(f"  Video Attached: {vm.get('video_attached')}")
            print(f"  Video Platform: {vm.get('video_platform')}")
            if vm.get('demoforge_demo_id'):
                print(f"  DemoForge Demo ID: {vm.get('demoforge_demo_id')}")
                print(f"  DemoForge API Latency: {vm.get('demoforge_api_latency_ms')}ms")
            if vm.get('demoforge_fallback_reason'):
                print(f"  Fallback Reason: {vm.get('demoforge_fallback_reason')}")
            # Check for old separate event fields
            if vm.get('video_channel'):
                print(f"  Video Channel: {vm.get('video_channel')}")
        else:
            print(f"  No video metadata in result")

        return corr_id
    except Exception as e:
        import traceback
        print(f"✗ Query failed: {e}")
        traceback.print_exc()
        return None

def main():
    """Run 2 test queries."""
    print("\n" + "="*60)
    print("TESTING 2 QUERIES - SEPARATE EVENT REMOVAL")
    print("="*60)

    # Test 1: Campaign Manager (should get DemoForge)
    corr_id_1 = test_query(
        "How do I create a campaign in Gupshup?",
        "Campaign Manager how-to"
    )

    # Test 2: Bot Studio (should get DemoForge)
    corr_id_2 = test_query(
        "What is Bot Studio?",
        "Bot Studio overview"
    )

    print(f"\n{'='*60}")
    print("TRACE IDs FOR LANGFUSE LOOKUP")
    print('='*60)
    if corr_id_1:
        print(f"\n1. Campaign Manager:")
        print(f"   Correlation ID: {corr_id_1}")

    if corr_id_2:
        print(f"\n2. Bot Studio:")
        print(f"   Correlation ID: {corr_id_2}")

    print(f"\n\nTo fetch traces via Langfuse CLI:")
    if corr_id_1:
        print(f"  langfuse traces --filter 'correlation_id={corr_id_1}'")
    if corr_id_2:
        print(f"  langfuse traces --filter 'correlation_id={corr_id_2}'")

if __name__ == "__main__":
    main()
