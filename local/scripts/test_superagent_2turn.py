#!/usr/bin/env python3
"""Test 2-turn conversation with SuperAgent.
Sends Turn 1 and Turn 2 queries, capturing trace_ids, correlation_ids, and session linking.

Usage:
    export LANGFUSE_HOST=https://cloud.langfuse.com
    export LANGFUSE_PUBLIC_KEY=pk-lf-...
    export LANGFUSE_SECRET_KEY=sk-lf-...
    python3 local/scripts/test_superagent_2turn.py
"""
import os
import sys
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Import langfuse to capture trace metadata
try:
    from langfuse import Langfuse
except ImportError:
    print("ERROR: langfuse not installed. Install: pip install langfuse")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "local" / "reports"
REPORT_FILE = REPORT_DIR / "superagent_2turn_conversation.jsonl"

# Setup Langfuse client
lf_host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")
lf_pk = os.environ.get("LANGFUSE_PUBLIC_KEY")
lf_sk = os.environ.get("LANGFUSE_SECRET_KEY")

if not (lf_pk and lf_sk):
    print("ERROR: LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY required in environment")
    sys.exit(1)

langfuse = Langfuse(
    public_key=lf_pk,
    secret_key=lf_sk,
    host=lf_host,
    debug=False,
)

def query_kb_answer(query: str, session_id: str = None, parent_trace_id: str = None) -> dict:
    """Query kb_answer skill locally (simulating SuperAgent call).

    Returns: {
        "query": str,
        "response": str,
        "trace_id": str,
        "correlation_id": str,
        "session_id": str,
        "parent_trace_id": str (if provided),
        "timestamp": ISO8601
    }
    """
    sys.path.insert(0, str(ROOT / "skill"))
    import kb_answer as kba

    # Generate IDs
    if session_id is None:
        session_id = str(uuid.uuid4())

    trace_id = str(uuid.uuid4())
    correlation_id = str(uuid.uuid4())

    # Setup context mock for KB fetch
    class MockContext:
        def get_secret(self, name):
            return os.environ.get(name)

    params = {
        "query": query,
        "trace_id": trace_id,
        "correlation_id": correlation_id,
        "session_id": session_id,
    }
    if parent_trace_id:
        params["parent_trace_id"] = parent_trace_id

    try:
        result = kba.kb_answer(parameters=params, context=MockContext())
        response = result.get("answer", "")

        # Try to extract langfuse trace metadata
        lf_meta = result.get("langfuse", {})
        lf_trace_id = lf_meta.get("trace_id") if isinstance(lf_meta, dict) else None

        return {
            "query": query,
            "response": response[:500],  # First 500 chars for reporting
            "response_full": response,
            "trace_id": trace_id,
            "correlation_id": correlation_id,
            "session_id": session_id,
            "parent_trace_id": parent_trace_id,
            "langfuse_trace_id": lf_trace_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "success": True,
        }
    except Exception as e:
        return {
            "query": query,
            "error": str(e),
            "trace_id": trace_id,
            "correlation_id": correlation_id,
            "session_id": session_id,
            "parent_trace_id": parent_trace_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "success": False,
        }

def main():
    print("=" * 80)
    print("SuperAgent 2-Turn Conversation Test")
    print("=" * 80)
    print()

    # Create report directory
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Session ID for both turns
    session_id = str(uuid.uuid4())
    print(f"Session ID: {session_id}")
    print()

    results = []

    # Turn 1
    print("TURN 1: 'How do I configure agent assist for my bot?'")
    print("-" * 80)
    turn1 = query_kb_answer(
        query="How do I configure agent assist for my bot?",
        session_id=session_id,
    )
    results.append(turn1)

    print(f"  Query: {turn1['query']}")
    print(f"  Trace ID: {turn1['trace_id']}")
    print(f"  Correlation ID: {turn1['correlation_id']}")
    print(f"  Session ID: {turn1['session_id']}")
    print(f"  Status: {'SUCCESS' if turn1['success'] else 'FAILED'}")
    if turn1['success']:
        print(f"  Response preview: {turn1['response'][:200]}...")
    else:
        print(f"  Error: {turn1.get('error')}")
    print()

    # Turn 2 - using parent_trace_id from Turn 1
    print("TURN 2: 'What's the best way to prevent hallucinations?'")
    print("-" * 80)
    turn2 = query_kb_answer(
        query="What's the best way to prevent hallucinations?",
        session_id=session_id,
        parent_trace_id=turn1["trace_id"],  # Chain to Turn 1
    )
    results.append(turn2)

    print(f"  Query: {turn2['query']}")
    print(f"  Trace ID: {turn2['trace_id']}")
    print(f"  Correlation ID: {turn2['correlation_id']}")
    print(f"  Session ID: {turn2['session_id']}")
    print(f"  Parent Trace ID: {turn2['parent_trace_id']}")
    print(f"  Status: {'SUCCESS' if turn2['success'] else 'FAILED'}")
    if turn2['success']:
        print(f"  Response preview: {turn2['response'][:200]}...")
    else:
        print(f"  Error: {turn2.get('error')}")
    print()

    # Write results to JSONL
    print("=" * 80)
    print(f"Writing results to: {REPORT_FILE}")
    print("=" * 80)
    print()

    with open(REPORT_FILE, "w") as f:
        for result in results:
            f.write(json.dumps(result, default=str) + "\n")

    # Summary
    summary = {
        "test_timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "turns": len(results),
        "turn1_trace_id": turn1["trace_id"],
        "turn1_correlation_id": turn1["correlation_id"],
        "turn2_trace_id": turn2["trace_id"],
        "turn2_correlation_id": turn2["correlation_id"],
        "turn2_parent_trace_id": turn2["parent_trace_id"],
        "turn1_success": turn1["success"],
        "turn2_success": turn2["success"],
        "chain_linked": turn2["parent_trace_id"] == turn1["trace_id"],
    }

    print("SUMMARY:")
    print("-" * 80)
    print(json.dumps(summary, indent=2, default=str))
    print()
    print("REPORT:")
    print(f"  File: {REPORT_FILE}")
    print(f"  Session ID: {session_id}")
    print(f"  Both queries sent: {len([r for r in results if r['success']]) == 2}")
    print(f"  Chain-linked (Turn 2 parent = Turn 1 trace_id): {summary['chain_linked']}")
    print()


if __name__ == "__main__":
    main()
