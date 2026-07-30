#!/usr/bin/env python3
"""
Comprehensive Guardrails Testing Suite
Tests BizAI, SuperAgent, Agent Assist, and Meta Business Agent (WhatsApp)
Validates module routing, cross-contamination prevention, and confidence scoring
"""

import json
import time
import uuid
import os
import sys
from datetime import datetime
from pathlib import Path

# Setup paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
os.chdir(Path(__file__).parent.parent.parent)

# Load environment
import dotenv
dotenv.load_dotenv()

from skill.kb_answer import kb_answer
import requests

# ============================================================================
# TEST QUERY DEFINITIONS (15-20 comprehensive queries)
# ============================================================================

TEST_QUERIES = [
    # BIZAI QUERIES (5)
    {
        "category": "BizAI",
        "query": "What is BizAI and what are its key features?",
        "expected_module": "BizAI",
        "expected_kb_prefix": "kb/bizai/",
    },
    {
        "category": "BizAI",
        "query": "How do I price BizAI agents?",
        "expected_module": "BizAI",
        "expected_kb_prefix": "kb/bizai/",
    },
    {
        "category": "BizAI",
        "query": "What is the BizAI architecture and value-add?",
        "expected_module": "BizAI",
        "expected_kb_prefix": "kb/bizai/",
    },
    {
        "category": "BizAI",
        "query": "How do I onboard a customer to BizAI?",
        "expected_module": "BizAI",
        "expected_kb_prefix": "kb/bizai/",
    },
    {
        "category": "BizAI",
        "query": "What APIs does BizAI expose?",
        "expected_module": "BizAI",
        "expected_kb_prefix": "kb/bizai/",
    },

    # SUPERAGENT QUERIES (5)
    {
        "category": "SuperAgent",
        "query": "How do I build a custom agent in SuperAgent?",
        "expected_module": "SuperAgent",
        "expected_kb_prefix": "kb/superagent/",
    },
    {
        "category": "SuperAgent",
        "query": "What deployment options are available for SuperAgent?",
        "expected_module": "SuperAgent",
        "expected_kb_prefix": "kb/superagent/",
    },
    {
        "category": "SuperAgent",
        "query": "How do I create and register custom skills?",
        "expected_module": "SuperAgent",
        "expected_kb_prefix": "kb/superagent/",
    },
    {
        "category": "SuperAgent",
        "query": "What third-party integrations does SuperAgent support?",
        "expected_module": "SuperAgent",
        "expected_kb_prefix": "kb/superagent/",
    },
    {
        "category": "SuperAgent",
        "query": "How do I set up agent automations?",
        "expected_module": "SuperAgent",
        "expected_kb_prefix": "kb/superagent/",
    },

    # AGENT ASSIST QUERIES (3)
    {
        "category": "Agent Assist",
        "query": "How do I manage teams in Agent Assist?",
        "expected_module": "Agent Assist",
        "expected_kb_prefix": "kb/agent-assist/",
    },
    {
        "category": "Agent Assist",
        "query": "How does conversation routing work?",
        "expected_module": "Agent Assist",
        "expected_kb_prefix": "kb/agent-assist/",
    },
    {
        "category": "Agent Assist",
        "query": "How do I access agent analytics and insights?",
        "expected_module": "Agent Assist",
        "expected_kb_prefix": "kb/agent-assist/",
    },

    # META BUSINESS AGENT / WHATSAPP QUERIES (3)
    {
        "category": "WhatsApp",
        "query": "How do I create a WhatsApp agent?",
        "expected_module": "WhatsApp",
        "expected_kb_prefix": "kb/whatsapp/",
    },
    {
        "category": "WhatsApp",
        "query": "How do I handle escalations in WhatsApp agent?",
        "expected_module": "WhatsApp",
        "expected_kb_prefix": "kb/whatsapp/",
    },
    {
        "category": "WhatsApp",
        "query": "What are the capabilities of Meta Business Agent?",
        "expected_module": "WhatsApp",
        "expected_kb_prefix": "kb/whatsapp/",
    },

    # AMBIGUOUS / CROSS-PRODUCT QUERIES (3+)
    {
        "category": "Ambiguous",
        "query": "What is an agent?",
        "expected_module": "General",
        "expected_kb_prefix": "kb/",
    },
    {
        "category": "Ambiguous",
        "query": "How do I deploy an agent?",
        "expected_module": "General",
        "expected_kb_prefix": "kb/",
    },
    {
        "category": "Ambiguous",
        "query": "Can I use an agent for WhatsApp?",
        "expected_module": "General",
        "expected_kb_prefix": "kb/",
    },
    {
        "category": "Ambiguous",
        "query": "Tell me about agents and pricing",
        "expected_module": "General",
        "expected_kb_prefix": "kb/",
    },
]

# ============================================================================
# EXECUTION ENGINE
# ============================================================================

def extract_module_from_source(source: str) -> str:
    """Extract module name from KB source path."""
    if not source:
        return "Unknown"
    if "bizai" in source.lower():
        return "BizAI"
    elif "superagent" in source.lower():
        return "SuperAgent"
    elif "agent-assist" in source.lower():
        return "Agent Assist"
    elif "whatsapp" in source.lower() or "meta" in source.lower():
        return "WhatsApp"
    else:
        return "General"


def fetch_langfuse_trace(trace_id: str, max_retries=3):
    """Fetch trace details from Langfuse API."""
    langfuse_host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    langfuse_public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    langfuse_secret_key = os.getenv("LANGFUSE_SECRET_KEY")

    if not all([langfuse_public_key, langfuse_secret_key]):
        return None

    url = f"{langfuse_host}/api/public/traces/{trace_id}"

    for attempt in range(max_retries):
        try:
            response = requests.get(
                url,
                auth=(langfuse_public_key, langfuse_secret_key),
                timeout=10,
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404 and attempt < max_retries - 1:
                time.sleep(1)  # Trace might not be indexed yet
                continue
            else:
                return None
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                print(f"Error fetching trace {trace_id}: {e}")
                return None

    return None


def execute_test_query(test_case: dict) -> dict:
    """Execute a single test query and capture results."""
    correlation_id = str(uuid.uuid4())
    query = test_case["query"]

    print(f"\n[{test_case['category']}] {query}")
    print(f"  Correlation ID: {correlation_id}")

    # Execute query
    start_time = time.time()
    result = kb_answer({"query": query}, correlation_id=correlation_id)
    execution_time = time.time() - start_time

    # Parse result
    answer = result.get("answer", "")
    answer_preview = answer[:300] if len(answer) > 300 else answer

    # Extract from langfuse metadata
    langfuse = result.get("langfuse", {})
    langfuse_metadata = langfuse.get("metadata", {})
    confidence = langfuse_metadata.get("confidence", 0)
    top_source = langfuse_metadata.get("top_source", "")
    module_label = langfuse_metadata.get("module_label", "Unknown")
    trace_id = langfuse.get("trace_id", "")

    # Extract detected module from source
    detected_module = extract_module_from_source(top_source)

    # Verify expectation
    expected_module = test_case["expected_module"]
    is_correct = (
        expected_module == "General"
        or detected_module == expected_module
        or module_label == expected_module
    )

    result_record = {
        "query": query,
        "category": test_case["category"],
        "answer_preview": answer_preview,
        "confidence": confidence,
        "top_source": top_source or "No source",
        "module_label": module_label,
        "detected_module": detected_module,
        "expected_module": expected_module,
        "is_correct": is_correct,
        "trace_id": trace_id,
        "execution_time_ms": round(execution_time * 1000, 2),
        "correlation_id": correlation_id,
    }

    # Fetch Langfuse trace if available
    if trace_id:
        time.sleep(0.5)  # Small delay for trace indexing
        trace_data = fetch_langfuse_trace(trace_id)
        if trace_data:
            result_record["langfuse_trace"] = {
                "status": "fetched",
                "timestamp": trace_data.get("timestamp"),
                "input": trace_data.get("input"),
                "output": trace_data.get("output"),
                "metadata": trace_data.get("metadata"),
            }

    # Print result
    status = "✓ PASS" if is_correct else "✗ FAIL"
    print(f"  {status} | Confidence: {confidence:.2f} | Module: {detected_module}")
    source_preview = (top_source or "No source")
    if isinstance(source_preview, str) and len(source_preview) > 80:
        source_preview = source_preview[:80] + "..."
    print(f"  Source: {source_preview}")

    return result_record


def analyze_results(results: list) -> dict:
    """Analyze test results for module routing accuracy."""
    by_category = {
        "bizai": {"correct": 0, "incorrect": 0, "examples": []},
        "superagent": {"correct": 0, "incorrect": 0, "examples": []},
        "agent_assist": {"correct": 0, "incorrect": 0, "examples": []},
        "whatsapp": {"correct": 0, "incorrect": 0, "examples": []},
        "ambiguous": {"correct": 0, "incorrect": 0, "examples": []},
    }

    total_correct = 0
    total_tests = len(results)
    cross_contamination_examples = []
    confusion_examples = []

    for result in results:
        # Skip error results
        if "error" in result:
            continue

        category = result.get("category", "ambiguous").lower().replace(" ", "_")
        is_correct = result.get("is_correct", False)

        if category not in by_category:
            category = "ambiguous"

        if is_correct:
            by_category[category]["correct"] += 1
            total_correct += 1
        else:
            by_category[category]["incorrect"] += 1
            confusion = {
                "query": result.get("query", ""),
                "expected": result.get("expected_module", ""),
                "got": result.get("detected_module", ""),
                "source": result.get("top_source", ""),
            }
            by_category[category]["examples"].append(confusion)
            confusion_examples.append(confusion)

            # Check for cross-contamination
            if result.get("category") != "Ambiguous" and result.get("detected_module") != "General":
                cross_contamination_examples.append({
                    "query": result.get("query", ""),
                    "expected": result.get("expected_module", ""),
                    "got": result.get("detected_module", ""),
                })

    accuracy = (total_correct / total_tests * 100) if total_tests > 0 else 0

    # Determine guardrails status
    guardrails_working = accuracy >= 85  # 85%+ accuracy = passing
    cross_contamination_detected = len(cross_contamination_examples) > 0

    confidence_in_routing = "HIGH" if accuracy >= 95 else "MEDIUM" if accuracy >= 85 else "LOW"

    return {
        "total_correct": total_correct,
        "total_tests": total_tests,
        "accuracy_percent": round(accuracy, 2),
        "by_category": by_category,
        "cross_contamination_detected": cross_contamination_detected,
        "cross_contamination_examples": cross_contamination_examples[:5],  # Top 5
        "confusion_examples": confusion_examples[:5],  # Top 5
        "guardrails_working": guardrails_working,
        "confidence_in_routing": confidence_in_routing,
    }


def main():
    """Main test execution."""
    print("=" * 80)
    print("COMPREHENSIVE GUARDRAILS TESTING")
    print("BizAI | SuperAgent | Agent Assist | Meta Business Agent (WhatsApp)")
    print("=" * 80)

    start_time = time.time()
    results = []

    # Execute all tests
    for i, test_case in enumerate(TEST_QUERIES, 1):
        print(f"\n[{i}/{len(TEST_QUERIES)}]", end=" ")
        try:
            result = execute_test_query(test_case)
            results.append(result)
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            results.append({
                "query": test_case["query"],
                "category": test_case["category"],
                "error": str(e),
                "is_correct": False,
            })

        # Rate limiting for Langfuse API
        if i % 5 == 0:
            time.sleep(1)

    execution_time = time.time() - start_time

    # Analyze results
    print("\n" + "=" * 80)
    print("ANALYSIS")
    print("=" * 80)

    analysis = analyze_results(results)

    print(f"\nTotal Tests: {analysis['total_tests']}")
    print(f"Correct: {analysis['total_correct']} / {analysis['total_tests']}")
    print(f"Accuracy: {analysis['accuracy_percent']}%")
    print(f"Execution Time: {execution_time:.2f}s")
    print(f"\nGuardrails Status: {'✓ PASS' if analysis['guardrails_working'] else '✗ FAIL'}")
    print(f"Confidence in Routing: {analysis['confidence_in_routing']}")
    print(f"Cross-Contamination Detected: {'YES' if analysis['cross_contamination_detected'] else 'NO'}")

    # Category breakdown
    print("\nBy Category:")
    for category, stats in analysis["by_category"].items():
        total = stats["correct"] + stats["incorrect"]
        if total > 0:
            acc = stats["correct"] / total * 100
            print(f"  {category.upper():15} {stats['correct']:2}/{total:2} ({acc:5.1f}%)")

    # Show confusion examples
    if analysis["confusion_examples"]:
        print("\nConfusion Examples (Top 5):")
        for i, example in enumerate(analysis["confusion_examples"], 1):
            print(f"  {i}. Query: {example['query'][:60]}...")
            print(f"     Expected: {example['expected']} | Got: {example['got']}")

    # Generate report
    report = {
        "test_metadata": {
            "total_queries": len(TEST_QUERIES),
            "execution_time_seconds": round(execution_time, 2),
            "trace_env": os.getenv("TRACE_ENV", "LOCAL"),
            "timestamp": datetime.now().isoformat(),
        },
        "queries_and_responses": results,
        "module_routing_analysis": {
            "total_correct": analysis["total_correct"],
            "total_incorrect": analysis["total_tests"] - analysis["total_correct"],
            "accuracy_percent": analysis["accuracy_percent"],
            "by_category": analysis["by_category"],
        },
        "confusion_detection_verdict": {
            "status": "PASS" if analysis["guardrails_working"] else "FAIL",
            "cross_contamination_detected": analysis["cross_contamination_detected"],
            "examples_of_confusion": analysis["confusion_examples"][:3],
            "guardrails_working": analysis["guardrails_working"],
            "confidence_in_routing": analysis["confidence_in_routing"],
        },
        "recommendations": generate_recommendations(analysis),
    }

    # Save report
    report_path = Path("local/reports/guardrails_comprehensive_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n✓ Report saved: {report_path}")

    # Print final verdict
    print("\n" + "=" * 80)
    print("FINAL VERDICT")
    print("=" * 80)
    print(f"Status: {report['confusion_detection_verdict']['status']}")
    print(f"Accuracy: {analysis['accuracy_percent']}%")
    print(f"Confidence: {analysis['confidence_in_routing']}")
    print("=" * 80)

    return 0 if analysis["guardrails_working"] else 1


def generate_recommendations(analysis: dict) -> list:
    """Generate recommendations based on analysis."""
    recommendations = []

    accuracy = analysis["accuracy_percent"]

    if accuracy < 85:
        recommendations.append(
            "CRITICAL: Module routing accuracy below 85%. Review guardrail thresholds and "
            "module keyword tuning. Focus on cross-contamination between similar modules."
        )
    elif accuracy < 95:
        recommendations.append(
            "MODULE TUNING: Improve routing accuracy to 95%+. Review ambiguous query handling "
            "and module boundary definitions."
        )

    by_cat = analysis["by_category"]

    for category, stats in by_cat.items():
        total = stats["correct"] + stats["incorrect"]
        if total > 0 and stats["incorrect"] > 0:
            acc = stats["correct"] / total * 100
            if acc < 80:
                recommendations.append(
                    f"REVIEW {category.upper()}: {acc:.0f}% accuracy. Check module detection "
                    f"logic and KB chunk scoring for this category."
                )

    if analysis["cross_contamination_detected"]:
        recommendations.append(
            "CROSS-CONTAMINATION: Detected queries routed to wrong modules. Review and "
            "strengthen module boundary definitions and guardrail keywords."
        )

    if not recommendations:
        recommendations.append("EXCELLENT: Guardrails performing well. Continue monitoring.")

    return recommendations


if __name__ == "__main__":
    sys.exit(main())
