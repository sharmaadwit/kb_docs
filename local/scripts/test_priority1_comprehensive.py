#!/usr/bin/env python3
"""
Re-run the two failing queries with Priority 1 fixes applied.
Confirms end-to-end routing improvement.
"""

import sys
sys.path.insert(0, "skill")

from kb_answer import kb_answer

test_queries = [
    ("What third-party integrations does SuperAgent support?", "SuperAgent"),
    ("How do I access agent analytics and insights?", "Agent Assist"),
]

print("Testing Priority 1 fixes with full kb_answer skill...\n")

passed = 0
for query, expected_module in test_queries:
    try:
        response = kb_answer({"query": query, "trace_env": "LOCAL"})
        langfuse_meta = response.get("langfuse", {})
        detected_module = langfuse_meta.get("module_label", "Unknown")
        status = "✓" if detected_module == expected_module else "✗"
        
        if detected_module == expected_module:
            passed += 1
        
        print(f"{status} '{query}'")
        print(f"  Expected module: {expected_module}")
        print(f"  Detected module: {detected_module}")
        top_source = langfuse_meta.get("metadata", {}).get("top_source", "None")
        print(f"  Top source: {top_source[:80] if top_source else 'None'}")
        print()
    except Exception as e:
        print(f"✗ '{query}'")
        print(f"  Error: {str(e)[:100]}")
        print()

print(f"Results: {passed}/{len(test_queries)} queries routed correctly")
sys.exit(0 if passed == len(test_queries) else 1)
