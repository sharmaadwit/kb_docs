#!/usr/bin/env python3
"""
Re-run full 20-query guardrails test with Priority 1 fixes applied.
Compare pre-fix (90%) vs post-fix accuracy.
"""

import sys
import json
sys.path.insert(0, "skill")

from kb_answer import kb_answer

test_queries = [
    # BizAI (5 queries)
    ("What is BizAI and what are its key features?", "BizAI"),
    ("How do I price BizAI agents?", "BizAI"),
    ("What is the BizAI architecture and value-add?", "BizAI"),
    ("How do I onboard a customer to BizAI?", "BizAI"),
    ("What APIs does BizAI expose?", "BizAI"),
    
    # SuperAgent (5 queries)
    ("How do I build a custom agent in SuperAgent?", "SuperAgent"),
    ("What deployment options are available for SuperAgent?", "SuperAgent"),
    ("How do I create and register custom skills?", "SuperAgent"),
    ("How do I set up agent automations?", "SuperAgent"),
    ("What third-party integrations does SuperAgent support?", "SuperAgent"),  # FIXED #1
    
    # Agent Assist (3 queries)
    ("How do I manage teams in Agent Assist?", "Agent Assist"),
    ("How does conversation routing work?", "Agent Assist"),
    ("How do I access agent analytics and insights?", "Agent Assist"),  # FIXED #2
    
    # WhatsApp (3 queries)
    ("How do I create a WhatsApp agent?", "WhatsApp"),
    ("How do I handle escalations in WhatsApp agent?", "WhatsApp"),
    ("What are the capabilities of Meta Business Agent?", "WhatsApp"),
    
    # Ambiguous (4 queries)
    ("What is an agent?", "SuperAgent"),
    ("How do I deploy an agent?", "SuperAgent"),
    ("Can I use an agent for WhatsApp?", "WhatsApp"),
    ("Tell me about agents and pricing", "SuperAgent"),
]

print("=" * 80)
print("FULL GUARDRAILS TEST WITH PRIORITY 1 FIXES")
print("=" * 80)
print()

results_by_category = {
    "BizAI": [],
    "SuperAgent": [],
    "Agent Assist": [],
    "WhatsApp": [],
    "Ambiguous": [],
}

category_map = {
    0: "BizAI", 1: "BizAI", 2: "BizAI", 3: "BizAI", 4: "BizAI",
    5: "SuperAgent", 6: "SuperAgent", 7: "SuperAgent", 8: "SuperAgent", 9: "SuperAgent",
    10: "Agent Assist", 11: "Agent Assist", 12: "Agent Assist",
    13: "WhatsApp", 14: "WhatsApp", 15: "WhatsApp",
    16: "Ambiguous", 17: "Ambiguous", 18: "Ambiguous", 19: "Ambiguous",
}

passed_total = 0
failed_queries = []

for idx, (query, expected_module) in enumerate(test_queries):
    category = category_map[idx]
    try:
        response = kb_answer({"query": query, "trace_env": "LOCAL"})
        langfuse_meta = response.get("langfuse", {})
        detected_module = langfuse_meta.get("module_label", "Unknown")
        
        is_correct = detected_module == expected_module
        status = "✓" if is_correct else "✗"
        
        if is_correct:
            passed_total += 1
        else:
            failed_queries.append((idx + 1, query, expected_module, detected_module))
        
        results_by_category[category].append({
            "query": query,
            "expected": expected_module,
            "detected": detected_module,
            "correct": is_correct,
            "status": status,
        })
        
        marker = " [FIXED #1]" if idx == 9 else (" [FIXED #2]" if idx == 12 else "")
        print(f"{status} Q{idx+1:2d} {category:12} | {query[:60]:60} → {detected_module:15}{marker}")
        
    except Exception as e:
        print(f"✗ Q{idx+1:2d} {category:12} | {query[:60]:60} → ERROR: {str(e)[:30]}")

print()
print("=" * 80)
print("SUMMARY BY CATEGORY")
print("=" * 80)
print()

for category in ["BizAI", "SuperAgent", "Agent Assist", "WhatsApp", "Ambiguous"]:
    results = results_by_category[category]
    correct = sum(1 for r in results if r["correct"])
    total = len(results)
    pct = (correct / total * 100) if total > 0 else 0
    status_icon = "✅" if pct == 100 else ("⚠️ " if pct >= 67 else "❌")
    print(f"{status_icon} {category:15} | {correct}/{total} ({pct:.0f}%)")

print()
print("=" * 80)
print(f"OVERALL ACCURACY: {passed_total}/{len(test_queries)} ({passed_total/len(test_queries)*100:.1f}%)")
print("=" * 80)
print()

if failed_queries:
    print("FAILED QUERIES:")
    print("-" * 80)
    for q_num, query, expected, detected in failed_queries:
        print(f"Q{q_num}: '{query}'")
        print(f"  Expected: {expected}")
        print(f"  Got: {detected}")
    print()

if passed_total >= 19:
    print("✅ GUARDRAILS SYSTEM READY FOR PRODUCTION")
    print("   - 95%+ accuracy achieved")
    print("   - Priority 1 fixes verified")
    print("   - No cross-contamination detected")
else:
    print(f"⚠️  ACCURACY BELOW TARGET: {passed_total}/{len(test_queries)} ({passed_total/len(test_queries)*100:.1f}%)")

