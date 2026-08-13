#!/usr/bin/env python3
"""
Comprehensive Phase 1 deployment verification.
Run this INSIDE the SuperAgent environment to verify code and telemetry.
"""

import os
import sys
import json

# Add skill path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

print("=" * 100)
print("PHASE 1 DEPLOYMENT VERIFICATION")
print("=" * 100)
print()

# ============================================================================
# 1. CHECK CODE IS PRESENT
# ============================================================================
print("1. CODE PRESENCE CHECK")
print("-" * 100)

try:
    from skill.kb_answer import (
        CONSULTING_TONE_CONFIG,
        _compose_consulting_answer,
        _gate_module_for_consulting,
        _resolve_answer_mode,
        _route_answer_composer,
    )
    print("✅ All Phase 1 functions imported successfully")
    print()
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# ============================================================================
# 2. CHECK CONFIG
# ============================================================================
print("2. CONFIGURATION CHECK")
print("-" * 100)

print(f"CONSULTING_TONE_CONFIG = {json.dumps(CONSULTING_TONE_CONFIG, default=str, indent=2)}")
print()

if not CONSULTING_TONE_CONFIG.get("enabled"):
    print("⚠️  WARNING: 'enabled' is False!")
    print("   Phase 1 pilot is DISABLED")
    print("   To enable: change CONSULTING_TONE_CONFIG['enabled'] = True")
    print()
else:
    print("✅ Config enabled: True")
    print(f"   Modules: {CONSULTING_TONE_CONFIG.get('modules', set())}")
    print(f"   Traffic %: {CONSULTING_TONE_CONFIG.get('traffic_pct', 50)}%")
    print()

# ============================================================================
# 3. TEST ROUTER FUNCTION
# ============================================================================
print("3. ROUTER FUNCTION TEST")
print("-" * 100)

try:
    # Mock evidence
    test_evidence = [
        {'heading': 'Test Step', 'text': 'Do this step first to enable feature.', 'score': 0.8, 'source': 'test.json'},
    ]

    # Test 1: Bot Studio (should hit consulting if enabled)
    answer1, mode1 = _route_answer_composer(
        query='how do I build a Bot Studio journey',
        intent='setup',
        entities=[],
        evidence=test_evidence,
        explicit_module='Bot Studio',
        params={},
    )

    print(f"Test 1 (Bot Studio):")
    print(f"  Mode: {mode1}")
    print(f"  Answer type: {'Consulting-tone' if mode1 == 'consulting' else 'Standard'}")
    print()

    # Test 2: WhatsApp (excluded from Phase 1)
    answer2, mode2 = _route_answer_composer(
        query='how do I send a WhatsApp template',
        intent='setup',
        entities=[],
        evidence=test_evidence,
        explicit_module='WhatsApp',
        params={},
    )

    print(f"Test 2 (WhatsApp - excluded):")
    print(f"  Mode: {mode2}")
    print(f"  Expected: 'standard' (WhatsApp not in Phase 1 modules)")
    print()

    # Test 3: Forced override
    answer3, mode3 = _route_answer_composer(
        query='test query',
        intent='setup',
        entities=[],
        evidence=test_evidence,
        explicit_module='General',
        params={'answer_mode': 'consulting'},  # Force override
    )

    print(f"Test 3 (Forced override):")
    print(f"  Mode: {mode3}")
    print(f"  Expected: 'consulting' (param override)")
    print()

    if mode1 in ('consulting', 'standard') and mode2 == 'standard' and mode3 == 'consulting':
        print("✅ All router tests passed")
    else:
        print("⚠️  Some router tests have unexpected results")
        print(f"   Bot Studio: {mode1} (expected consulting if enabled)")
        print(f"   WhatsApp: {mode2} (expected standard)")
        print(f"   Override: {mode3} (expected consulting)")

except Exception as e:
    print(f"❌ Router test error: {e}")
    import traceback
    traceback.print_exc()

print()

# ============================================================================
# 4. LANGFUSE INTEGRATION CHECK
# ============================================================================
print("4. LANGFUSE INTEGRATION CHECK")
print("-" * 100)

try:
    from skill.kb_answer import kb_answer

    print("✅ kb_answer function imported")
    print()
    print("When kb_answer() is called:")
    print("  1. Calls _route_answer_composer() → gets (answer, answer_mode)")
    print("  2. Tags policy_meta['answer_mode'] = answer_mode")
    print("  3. Langfuse receives metadata with answer_mode field")
    print()
    print("Expected in Langfuse traces:")
    print("  metadata.answer_mode = 'consulting' OR 'standard'")
    print()

except Exception as e:
    print(f"❌ kb_answer import error: {e}")

# ============================================================================
# 5. DEPLOYMENT STATUS
# ============================================================================
print("=" * 100)
print("DEPLOYMENT STATUS SUMMARY")
print("=" * 100)
print()

status_ok = True

if CONSULTING_TONE_CONFIG.get("enabled"):
    print("✅ Code deployed and ENABLED")
else:
    print("❌ Code deployed but DISABLED")
    status_ok = False

print()
print("NEXT STEPS:")
print()

if not status_ok:
    print("1. In skill/kb_answer.py, change:")
    print("   CONSULTING_TONE_CONFIG = {")
    print("       'enabled': False,  ← Change to True")
    print("       ...")
    print()

print("2. Restart the SuperAgent skill service")
print("   (The service must reload skill/kb_answer.py with enabled=True)")
print()

print("3. Send test queries:")
print("   - Bot Studio: 'how do I build a journey with conditional branching'")
print("   - RCS (via Campaign): 'should I use RCS or WhatsApp for my campaign'")
print()

print("4. Check Langfuse dashboard:")
print("   - Filter: metadata.answer_mode = 'consulting'")
print("   - Should see new traces with answer_mode field")
print()

print("5. Run this script again to re-verify:")
print("   python3 local/scripts/verify_phase1_deployment.py")
print()

print("=" * 100)
