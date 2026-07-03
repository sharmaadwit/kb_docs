#!/usr/bin/env python3
"""Test video matching across modules with DemoForge integration.

Generates fresh traces for testing if DemoForge video selection now matches
module intent correctly. Tests 5 key modules with various query types.

Usage:
  python3 local/scripts/test_video_matching.py
  python3 local/scripts/test_video_matching.py --verbose
  python3 local/scripts/test_video_matching.py --output-file /path/to/results.json

Outputs:
  - Prints structured results to stdout
  - Optionally writes results to JSON file
  - Trace IDs available for Langfuse CLI lookup
  - Video matching metadata for each query
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid

# Add skill module to path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill"))

# Import kb_answer skill
try:
    from skill import kb_answer as kb_answer_module
except ImportError:
    print("ERROR: Could not import kb_answer skill. Ensure PYTHONPATH is set correctly.")
    sys.exit(1)


class MockContext:
    """Mock context object for skill execution."""

    def __init__(self):
        self.secrets = {}
        self.user_email = "test@video_matching.example.com"

    def get_secret(self, key: str) -> Optional[str]:
        """Get secret from environment."""
        return os.getenv(key)


# Test queries covering 5 modules with different intents
TEST_QUERIES = [
    # ========== Module 1: Bot Studio (journey/workflow) ==========
    {
        "module": "Bot Studio",
        "intent": "overview",
        "query": "What is Bot Studio and how do I use it?",
        "description": "Bot Studio overview - should demonstrate flow builder interface",
    },
    {
        "module": "Bot Studio",
        "intent": "how_to",
        "query": "How do I create a bot using Bot Studio?",
        "description": "Bot Studio creation workflow",
    },
    {
        "module": "Bot Studio",
        "intent": "how_to",
        "query": "How do I set up bot flows and integrate them?",
        "description": "Bot Studio advanced flows",
    },

    # ========== Module 2: CTX (Click-To-Chat, conversions) ==========
    {
        "module": "CTX",
        "intent": "overview",
        "query": "What is Click-to-Chat and how does it work?",
        "description": "CTX/Click-to-Chat overview for conversions",
    },
    {
        "module": "CTX",
        "intent": "how_to",
        "query": "How do I implement Click-to-Chat on my website?",
        "description": "CTX implementation guide",
    },
    {
        "module": "CTX",
        "intent": "setup",
        "query": "How do I set up Click-to-Chat for lead generation?",
        "description": "CTX setup and configuration",
    },

    # ========== Module 3: AI Admin (management, configuration) ==========
    {
        "module": "AI Admin",
        "intent": "overview",
        "query": "What is AI Admin and what can I do with it?",
        "description": "AI Admin overview",
    },
    {
        "module": "AI Admin",
        "intent": "how_to",
        "query": "How do I configure AI models in AI Admin?",
        "description": "AI Admin configuration",
    },
    {
        "module": "AI Admin",
        "intent": "setup",
        "query": "How do I set up admin controls and permissions?",
        "description": "AI Admin security and permissions",
    },

    # ========== Module 4: Campaign Manager (campaigns, execution) ==========
    {
        "module": "Campaign Manager",
        "intent": "overview",
        "query": "What is Campaign Manager and how does it work?",
        "description": "Campaign Manager overview",
    },
    {
        "module": "Campaign Manager",
        "intent": "how_to",
        "query": "How do I create and execute a campaign in Gupshup?",
        "description": "Campaign Manager creation and execution",
    },
    {
        "module": "Campaign Manager",
        "intent": "setup",
        "query": "How do I set up campaign scheduling and targeting?",
        "description": "Campaign Manager advanced setup",
    },

    # ========== Module 5: Personalize (personalization engine) ==========
    {
        "module": "Personalize",
        "intent": "overview",
        "query": "What is the Personalize module and how does personalization work?",
        "description": "Personalize overview",
    },
    {
        "module": "Personalize",
        "intent": "how_to",
        "query": "How do I personalize messages for different user segments?",
        "description": "Personalize user segmentation",
    },
    {
        "module": "Personalize",
        "intent": "setup",
        "query": "How do I set up dynamic content personalization rules?",
        "description": "Personalize dynamic rules setup",
    },
]


def format_timestamp() -> str:
    """Get ISO format timestamp."""
    return datetime.utcnow().isoformat() + "Z"


def generate_correlation_id(module: str, intent: str, index: int) -> str:
    """Generate unique correlation ID for trace."""
    safe_module = module.lower().replace(" ", "_")
    safe_intent = intent.lower().replace(" ", "_")
    timestamp = int(datetime.now().timestamp() * 1000)
    unique_suffix = str(uuid.uuid4())[:8]
    return f"video_match_{safe_module}_{safe_intent}_{index}_{timestamp}_{unique_suffix}"


def run_test_query(
    query: str,
    module: str,
    intent: str,
    description: str,
    index: int,
    verbose: bool = False
) -> Dict[str, Any]:
    """Run a single test query and capture results.

    Args:
        query: Test query string
        module: Module name (e.g., "Bot Studio")
        intent: Intent type (e.g., "how_to", "overview")
        description: Human-readable description
        index: Query index for logging
        verbose: Print detailed output

    Returns:
        Dict with query results, video metadata, and trace info
    """

    correlation_id = generate_correlation_id(module, intent, index)
    started = datetime.now()

    if verbose:
        print(f"\n{'='*70}")
        print(f"[{index}] {module.upper()} - {intent.upper()}")
        print(f"{'='*70}")
        print(f"Query: {query}")
        print(f"Description: {description}")
        print(f"Correlation ID: {correlation_id}")
        print(f"Started: {format_timestamp()}")

    result = {
        "index": index,
        "module": module,
        "intent": intent,
        "description": description,
        "query": query,
        "correlation_id": correlation_id,
        "timestamp": format_timestamp(),
        "status": "unknown",
        "error": None,
        "video_title": None,
        "video_platform": None,
        "demoforge_demo_id": None,
        "demoforge_demo_name": None,
        "demoforge_api_latency_ms": None,
        "fallback_reason": None,
        "video_attached": False,
        "langfuse_trace_id": None,
        "latency_ms": None,
    }

    try:
        # Create mock context
        ctx = MockContext()

        # Execute kb_answer skill
        response = kb_answer_module.kb_answer(
            parameters={"query": query},
            context=ctx,
            correlation_id=correlation_id
        )

        result["status"] = "success"

        # Extract video metadata from response
        if isinstance(response, dict):
            # Check for langfuse trace ID
            if response.get("langfuse"):
                result["langfuse_trace_id"] = response.get("langfuse", {}).get("trace_id")

            # Extract video metadata
            if response.get("video_meta"):
                vm = response["video_meta"]
                result["video_attached"] = vm.get("video_attached", False)
                result["video_title"] = vm.get("video_title")
                result["video_platform"] = vm.get("video_platform")
                result["demoforge_demo_id"] = vm.get("demoforge_demo_id")
                result["demoforge_demo_name"] = vm.get("demoforge_demo_name")
                result["demoforge_api_latency_ms"] = vm.get("demoforge_api_latency_ms")
                result["fallback_reason"] = vm.get("demoforge_fallback_reason")

        # Calculate latency
        elapsed = (datetime.now() - started).total_seconds() * 1000
        result["latency_ms"] = round(elapsed, 1)

        if verbose:
            print(f"\n✓ Query executed successfully")
            print(f"  Status: {result['status']}")
            print(f"  Latency: {result['latency_ms']}ms")
            if result["video_attached"]:
                print(f"  Video: {result['video_title']} ({result['video_platform']})")
                if result["demoforge_demo_id"]:
                    print(f"  DemoForge Demo: {result['demoforge_demo_name']} (ID: {result['demoforge_demo_id']})")
                    print(f"  DemoForge API Latency: {result['demoforge_api_latency_ms']}ms")
                if result["fallback_reason"]:
                    print(f"  Fallback Reason: {result['fallback_reason']}")
            else:
                print(f"  No video attached")
            if result["langfuse_trace_id"]:
                print(f"  Langfuse Trace: {result['langfuse_trace_id']}")

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        elapsed = (datetime.now() - started).total_seconds() * 1000
        result["latency_ms"] = round(elapsed, 1)
        if verbose:
            print(f"\n✗ Query failed: {e}")
            import traceback
            traceback.print_exc()

    return result


def main():
    """Run all test queries and generate report."""

    parser = argparse.ArgumentParser(
        description="Test video matching across modules with DemoForge integration"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print detailed output for each query"
    )
    parser.add_argument(
        "--output-file", "-o",
        type=str,
        default=None,
        help="Write results to JSON file"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=None,
        help="Limit number of queries to run"
    )

    args = parser.parse_args()

    print("\n" + "="*70)
    print("VIDEO MATCHING TEST HARNESS - DemoForge Integration")
    print("="*70)
    print(f"Started: {format_timestamp()}")
    print(f"Total queries: {len(TEST_QUERIES)}")
    print(f"Verbose mode: {args.verbose}")
    print()

    # Run all test queries
    results = []
    queries_to_run = TEST_QUERIES[:args.limit] if args.limit else TEST_QUERIES

    for index, test_case in enumerate(queries_to_run, 1):
        result = run_test_query(
            query=test_case["query"],
            module=test_case["module"],
            intent=test_case["intent"],
            description=test_case["description"],
            index=index,
            verbose=args.verbose
        )
        results.append(result)

    # Print summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    successful = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "error")
    with_video = sum(1 for r in results if r["video_attached"])
    with_demoforge = sum(1 for r in results if r["demoforge_demo_id"])

    print(f"\nQueries executed: {len(results)}")
    print(f"  ✓ Successful: {successful}")
    print(f"  ✗ Failed: {failed}")
    print(f"\nVideo selection:")
    print(f"  Queries with video attached: {with_video}/{len(results)}")
    print(f"  Queries with DemoForge demo: {with_demoforge}/{len(results)}")

    # Module breakdown
    print(f"\nResults by module:")
    modules_data = {}
    for result in results:
        module = result["module"]
        if module not in modules_data:
            modules_data[module] = {"total": 0, "with_video": 0, "with_demoforge": 0}
        modules_data[module]["total"] += 1
        if result["video_attached"]:
            modules_data[module]["with_video"] += 1
        if result["demoforge_demo_id"]:
            modules_data[module]["with_demoforge"] += 1

    for module in sorted(modules_data.keys()):
        data = modules_data[module]
        print(f"  {module}: {data['total']} queries, {data['with_video']} with video, {data['with_demoforge']} with DemoForge")

    # Print correlation IDs for Langfuse lookup
    print(f"\n" + "="*70)
    print("CORRELATION IDs FOR LANGFUSE LOOKUP")
    print("="*70)
    print("\nTo fetch traces in Langfuse, use:")
    print("  lf traces --filter 'correlation_id=<ID>'")
    print("\nCorrelation IDs:")

    for result in results:
        status_icon = "✓" if result["status"] == "success" else "✗"
        video_icon = "📹" if result["video_attached"] else " "
        demoforge_icon = "🎯" if result["demoforge_demo_id"] else " "

        print(f"\n{status_icon} [{result['index']}] {result['module']} / {result['intent']}")
        print(f"   {video_icon} Video: {result['video_platform'] or 'None'}")
        print(f"   {demoforge_icon} DemoForge: {result['demoforge_demo_name'] or 'None'}")
        print(f"   Correlation ID: {result['correlation_id']}")

    # Write to file if requested
    if args.output_file:
        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Prepare output data
        output_data = {
            "timestamp": format_timestamp(),
            "test_run_summary": {
                "total_queries": len(results),
                "successful": successful,
                "failed": failed,
                "with_video": with_video,
                "with_demoforge": with_demoforge,
            },
            "results": results,
            "modules": modules_data,
        }

        with open(output_path, "w") as f:
            json.dump(output_data, f, indent=2)

        print(f"\n✓ Results written to: {output_path}")

    print(f"\n" + "="*70)
    print("TEST COMPLETE")
    print("="*70)
    print("\nNext steps:")
    print("  1. Check Langfuse dashboard for correlation IDs")
    print("  2. Verify video selection matches module intent")
    print("  3. Review DemoForge demo URLs and latency metrics")
    if args.output_file:
        print(f"  4. Review detailed results in {args.output_file}")


if __name__ == "__main__":
    main()
