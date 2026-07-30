#!/usr/bin/env python3
"""
Quick test of Priority 1 fixes for SuperAgent integrations and Agent Assist analytics.
"""

import sys
sys.path.insert(0, "skill")

from kb_answer import _detect_module

test_cases = [
    # Issue #1: SuperAgent integrations
    ("What third-party integrations does SuperAgent support?", "SuperAgent"),
    ("SuperAgent integrations", "SuperAgent"),
    ("integrations in super agent", "SuperAgent"),
    
    # Issue #2: Agent Assist analytics
    ("How do I access agent analytics and insights?", "Agent Assist"),
    ("Agent Assist analytics", "Agent Assist"),
    ("analytics for teams", "Agent Assist"),
    ("team routing analytics", "Agent Assist"),
    
    # Regression: ensure we don't break existing routing
    ("What is BizAI?", "BizAI"),
    ("How do I deploy my agent to WhatsApp?", "SuperAgent"),
    ("Meta Business Agent overview", "WhatsApp"),
]

print("Testing Priority 1 fixes...\n")

passed = 0
failed = 0

for query, expected in test_cases:
    detected = _detect_module(query)
    status = "✓" if detected == expected else "✗"
    if detected == expected:
        passed += 1
    else:
        failed += 1
    print(f"{status} '{query}'")
    print(f"  Expected: {expected}, Got: {detected}")

print(f"\nResults: {passed}/{len(test_cases)} passed")
sys.exit(0 if failed == 0 else 1)
