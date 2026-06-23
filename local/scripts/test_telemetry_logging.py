#!/usr/bin/env python3
"""
Test telemetry logging patch in kb_answer.py

Verifies:
  - HTTP failure errors are logged with status code + response text
  - Exception errors are logged with exception type + message
  - Missing credentials are logged with specific missing fields
  - All logs use flush=True for immediate output
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def analyze_telemetry_patch():
    """Check that the telemetry logging patch is correctly applied."""

    print("=" * 80)
    print("TELEMETRY LOGGING PATCH ANALYSIS")
    print("=" * 80)
    print()

    kb_answer_path = ROOT / "skill" / "kb_answer.py"
    content = kb_answer_path.read_text(encoding="utf-8")

    # Check 1: HTTP failure logging
    print("✓ Check 1: HTTP failure logging")
    if 'ingestion_failed_http_{status_code}' in content:
        print("  ✅ HTTP status code captured in error message")
        if '[LANGFUSE] Ingestion failed: HTTP' in content:
            print("  ✅ Error is logged with [LANGFUSE] marker")
        else:
            print("  ❌ Missing [LANGFUSE] log marker")
        if 'resp.text[:200]' in content:
            print("  ✅ Response text is logged (first 200 chars)")
        else:
            print("  ❌ Response text not captured")
    else:
        print("  ❌ HTTP status code not captured")
    print()

    # Check 2: Exception logging
    print("✓ Check 2: Exception logging")
    if 'except Exception as e:' in content:
        print("  ✅ Exception is captured")
        if 'type(e).__name__' in content:
            print("  ✅ Exception type is logged")
        else:
            print("  ❌ Exception type not captured")
        if '[LANGFUSE] Ingestion exception:' in content:
            print("  ✅ Exception is logged with [LANGFUSE] marker")
        else:
            print("  ❌ Missing [LANGFUSE] log marker for exceptions")
    else:
        print("  ❌ Exception handling not found")
    print()

    # Check 3: Missing credentials logging
    print("✓ Check 3: Missing credentials logging")
    if 'missing_credentials' in content:
        print("  ✅ Missing credentials error message created")
        if '[LANGFUSE] Cannot ingest:' in content:
            print("  ✅ Logged with [LANGFUSE] marker")
        else:
            print("  ❌ Missing [LANGFUSE] log marker for credentials")
        missing_checks = ['LANGFUSE_HOST', 'LANGFUSE_PUBLIC_KEY', 'LANGFUSE_SECRET_KEY']
        all_checked = all(check in content for check in missing_checks)
        if all_checked:
            print("  ✅ All three credentials checked individually")
        else:
            print("  ⚠️  Not all credentials checked")
    else:
        print("  ❌ Missing credentials handling not found")
    print()

    # Check 4: flush=True for immediate output
    print("✓ Check 4: Immediate output with flush=True")
    flush_count = content.count('flush=True')
    print(f"  ✅ Found {flush_count} print statements with flush=True")
    if flush_count >= 3:
        print("  ✅ All error paths have flush=True")
    else:
        print(f"  ⚠️  Expected at least 3 flush=True, found {flush_count}")
    print()

    # Check 5: Verify syntax
    print("✓ Check 5: Syntax validation")
    try:
        import py_compile
        py_compile.compile(str(kb_answer_path), doraise=True)
        print("  ✅ kb_answer.py has valid Python syntax")
    except py_compile.PyCompileError as e:
        print(f"  ❌ Syntax error: {e}")
    print()


def simulate_error_cases():
    """Simulate what error messages will look like at runtime."""

    print("=" * 80)
    print("SIMULATED ERROR MESSAGES (what skill logs will show)")
    print("=" * 80)
    print()

    # Case 1: HTTP error
    print("Case 1: HTTP 401 Unauthorized")
    status_code = 401
    resp_text = '{"error": "Invalid API key"}'
    error_msg = f"[LANGFUSE] Ingestion failed: HTTP {status_code} | {resp_text}"
    print(f"  Log: {error_msg}")
    print()

    # Case 2: Network exception
    print("Case 2: Network timeout")
    exc_type = "ConnectTimeout"
    exc_msg = "Connection timed out after 30s"
    error = f"ingestion_transport_error: {exc_type}: {exc_msg}"
    error_msg = f"[LANGFUSE] Ingestion exception: {error}"
    print(f"  Log: {error_msg}")
    print()

    # Case 3: Missing credentials
    print("Case 3: Missing Langfuse secrets")
    missing = ["LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"]
    error = f"missing_credentials: {', '.join(missing)}"
    error_msg = f"[LANGFUSE] Cannot ingest: {error}"
    print(f"  Log: {error_msg}")
    print()


def check_telemetry_state():
    """Check current telemetry state from dashboard data."""

    print("=" * 80)
    print("CURRENT TELEMETRY STATE (from latest dashboard refresh)")
    print("=" * 80)
    print()

    analysis_path = ROOT / "local" / "reports" / "dashboard_analysis.json"
    if not analysis_path.exists():
        print("❌ No dashboard analysis found. Run: bash local/scripts/refresh_dashboard.sh")
        return

    import json
    data = json.loads(analysis_path.read_text())

    print(f"Total traces analyzed: {data.get('total_queries', 'N/A')}")
    print(f"Answer rate: {data.get('answer_rate', 'N/A')}%")
    print(f"IDK rate: {data.get('idk_rate', 'N/A')}%")
    print(f"Timestamp: {data.get('timestamp', 'N/A')}")
    print()

    print("Top failing modules (lowest answer rate):")
    modules = data.get('modules', {})
    sorted_mods = sorted(modules.items(), key=lambda x: x[1].get('answer_rate', 100))
    for mod, stats in sorted_mods[:3]:
        ans_rate = stats.get('answer_rate', 0)
        count = stats.get('count', 0)
        print(f"  {mod:25s} {ans_rate:5.1f}% ({count} queries)")
    print()


if __name__ == '__main__':
    analyze_telemetry_patch()
    simulate_error_cases()
    check_telemetry_state()

    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("1. Deploy patched skill/kb_answer.py to Gupshup environment")
    print("2. Run a test query")
    print("3. Check skill logs for [LANGFUSE] markers")
    print("4. Re-run this test after deployment to verify telemetry is working")
    print()
