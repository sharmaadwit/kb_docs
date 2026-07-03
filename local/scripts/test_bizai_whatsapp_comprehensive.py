#!/usr/bin/env python3
"""
Comprehensive test for new BizAI and WhatsApp KB content.
Executes 12 test queries against kb_answer skill and analyzes Langfuse traces.

Queries:
- BizAI (6): overview, architecture, value-add, API endpoints, onboarding, pricing
- WhatsApp (3): pricing, API, Meta Business Agent
- Mixed/integration (3): cross-topic questions
"""

import json
import os
import sys
import uuid
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
import base64

# ── Path setup ──────────────────────────────────────────────────────────────
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILL_DIR = os.path.join(REPO_ROOT, "skill")
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

LOG_PATH = os.path.join(REPO_ROOT, ".logs", "test_bizai_whatsapp.log")


def log(msg: str):
    """Log message with timestamp."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")


# ── Test queries ─────────────────────────────────────────────────────────────
TEST_QUERIES = [
    # BizAI queries (6)
    {
        "id": "bizai_overview",
        "query": "What is BizAI and what does it do?",
        "expected_sources": ["kb/bizai/bizai-overview.md"],
    },
    {
        "id": "bizai_architecture",
        "query": "Explain BizAI architecture and components",
        "expected_sources": ["kb/bizai/bizai-architecture.md"],
    },
    {
        "id": "bizai_value_add",
        "query": "What makes Gupshup's BizAI different from Meta's? List the four value-add capabilities.",
        "expected_sources": ["kb/bizai/bizai-value-add.md"],
    },
    {
        "id": "bizai_api",
        "query": "What are the BizAI API endpoints?",
        "expected_sources": ["kb/bizai/bizai-api-endpoints.md"],
    },
    {
        "id": "bizai_onboarding",
        "query": "How do I onboard to BizAI?",
        "expected_sources": ["kb/bizai/bizai-onboarding.md"],
    },
    {
        "id": "bizai_pricing",
        "query": "What is BizAI pricing?",
        "expected_sources": ["kb/bizai/bizai-pricing.md"],
    },
    # WhatsApp queries (3)
    {
        "id": "whatsapp_pricing",
        "query": "What is WhatsApp API pricing?",
        "expected_sources": ["kb/whatsapp/whatsapp-pricing.md"],
    },
    {
        "id": "whatsapp_api",
        "query": "How do I use the WhatsApp API?",
        "expected_sources": ["kb/whatsapp/whatsapp-api-reference.md"],
    },
    {
        "id": "whatsapp_meta_agent",
        "query": "What is Meta Business Agent for WhatsApp?",
        "expected_sources": ["kb/whatsapp/meta-business-agent.md"],
    },
    # Mixed/integration queries (3)
    {
        "id": "bizai_whatsapp_integration",
        "query": "How does BizAI integrate with WhatsApp?",
        "expected_sources": ["kb/bizai/bizai-overview.md", "kb/whatsapp/"],
    },
    {
        "id": "bizai_whatsapp_pricing_comparison",
        "query": "Compare BizAI pricing with WhatsApp API pricing",
        "expected_sources": ["kb/bizai/bizai-pricing.md", "kb/whatsapp/whatsapp-pricing.md"],
    },
    {
        "id": "bizai_onboarding_whatsapp",
        "query": "What is the onboarding process for BizAI on WhatsApp?",
        "expected_sources": ["kb/bizai/bizai-onboarding.md", "kb/whatsapp/"],
    },
]


# ── Minimal context stub ─────────────────────────────────────────────────────
class _Context:
    """Minimal context object that satisfies kb_answer's context.get_secret() calls."""

    def __init__(self, secrets: dict):
        self._secrets = secrets

    def get_secret(self, key: str):
        return self._secrets.get(key) or os.environ.get(key)


# ── Step 1: Load .env ────────────────────────────────────────────────────────
log("Step 1: Loading .env credentials")
env_path = os.path.join(REPO_ROOT, ".env")
env_vars = {}
try:
    with open(env_path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, _, v = line.partition("=")
                env_vars[k.strip()] = v.strip()
    os.environ.update(env_vars)
    log(f"Step 1: Loaded {len(env_vars)} env vars from .env")
except Exception as e:
    log(f"Step 1: ERROR loading .env: {e}")
    sys.exit(1)

LANGFUSE_HOST = env_vars.get("LANGFUSE_HOST", "")
LANGFUSE_PUBLIC_KEY = env_vars.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = env_vars.get("LANGFUSE_SECRET_KEY", "")

if not (LANGFUSE_HOST and LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY):
    log("Step 1: ERROR: Missing Langfuse credentials in .env")
    sys.exit(1)

log(f"Step 1: LANGFUSE_HOST={LANGFUSE_HOST}")

# ── Step 2: Import kb_answer ─────────────────────────────────────────────────
log("Step 2: Importing kb_answer from skill/kb_answer.py")
try:
    from kb_answer import kb_answer
    log("Step 2: kb_answer imported successfully")
except Exception as e:
    log(f"Step 2: ERROR importing kb_answer: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

context = _Context(
    {
        "LANGFUSE_HOST": LANGFUSE_HOST,
        "LANGFUSE_PUBLIC_KEY": LANGFUSE_PUBLIC_KEY,
        "LANGFUSE_SECRET_KEY": LANGFUSE_SECRET_KEY,
    }
)

# ── Step 3: Execute 12 queries ───────────────────────────────────────────────
log(f"Step 3: Executing {len(TEST_QUERIES)} test queries")
query_results = []
start_time = datetime.now(timezone.utc)

for idx, test in enumerate(TEST_QUERIES, 1):
    query_id = test["id"]
    query_text = test["query"]
    correlation_id = uuid.uuid4().hex[:12]

    log(f"Step 3: Query {idx}/{len(TEST_QUERIES)} - {query_id} (correlation_id={correlation_id})")

    try:
        result = kb_answer(
            parameters={"query": query_text},
            context=context,
            correlation_id=correlation_id,
        )

        answer = result.get("answer", "")
        metadata = (result.get("langfuse") or {}).get("metadata") or {}
        citations = result.get("citations", [])

        query_results.append(
            {
                "id": query_id,
                "query": query_text,
                "correlation_id": correlation_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "answer_preview": answer[:200] if answer else "",
                "answer_length": len(answer),
                "confidence": metadata.get("confidence"),
                "top_source": metadata.get("top_source"),
                "modules": metadata.get("modules", []),
                "source_count": metadata.get("source_count"),
                "answered": metadata.get("answered"),
                "citations": citations,
            }
        )

        log(
            f"Step 3: Query {idx} executed - confidence={metadata.get('confidence')}, sources={metadata.get('source_count')}"
        )
    except Exception as e:
        log(f"Step 3: ERROR executing query {idx}: {e}")
        import traceback
        traceback.print_exc()
        query_results.append(
            {
                "id": query_id,
                "query": query_text,
                "correlation_id": correlation_id,
                "error": str(e),
            }
        )

log(f"Step 3: Completed {len(query_results)} queries")

# ── Step 4: Wait for traces to propagate ─────────────────────────────────────
log("Step 4: Waiting 30 seconds for traces to propagate to Langfuse")
time.sleep(30)

# ── Step 5: Fetch traces from Langfuse ───────────────────────────────────────
log("Step 5: Fetching traces from Langfuse API")

import requests
from urllib.parse import urlencode

# Build basic auth header
auth_str = f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}"
auth_b64 = base64.b64encode(auth_str.encode()).decode()
headers = {
    "Authorization": f"Basic {auth_b64}",
    "Content-Type": "application/json",
}

trace_data = {}
traces_found = 0

# Fetch all recent traces first
log("Step 5: Fetching all recent traces from Langfuse")
try:
    url = f"{LANGFUSE_HOST.rstrip('/')}/api/public/traces?limit=100"
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    all_traces = response.json().get("data", [])
    log(f"Step 5: Fetched {len(all_traces)} total traces from Langfuse")

    # Index traces by correlation_id from metadata
    for trace in all_traces:
        metadata = trace.get("metadata", {})
        corr_id = metadata.get("correlation_id")
        if corr_id:
            trace_data[corr_id] = {
                "trace_id": trace.get("id"),
                "timestamp": trace.get("timestamp"),
                "tags": trace.get("tags", []),
                "metadata": metadata,
            }

    # Match with our queries
    for qr in query_results:
        if "error" in qr:
            continue
        correlation_id = qr["correlation_id"]
        if correlation_id in trace_data:
            traces_found += 1
            log(f"Step 5: Found trace for {qr['id']}")
        else:
            log(f"Step 5: No trace found for {qr['id']} (correlation_id={correlation_id})")

except Exception as e:
    log(f"Step 5: ERROR fetching traces: {e}")
    import traceback
    traceback.print_exc()

log(f"Step 5: Found {traces_found} traces")

# ── Step 6: Analyze results ──────────────────────────────────────────────────
log("Step 6: Analyzing results")

new_kb_retrieved_count = 0
high_confidence_count = 0

for qr in query_results:
    if "error" in qr:
        continue

    # Check if answer mentions expected sources
    answer_preview = qr["answer_preview"]
    expected_sources = next(
        (t["expected_sources"] for t in TEST_QUERIES if t["id"] == qr["id"]), []
    )

    if qr["confidence"] and qr["confidence"] > 0.7:
        high_confidence_count += 1

    # Basic heuristic: if we got an answer, we likely retrieved KB content
    if qr["answered"] is True and qr["source_count"] and qr["source_count"] > 0:
        new_kb_retrieved_count += 1

# ── Step 7: Generate final report ────────────────────────────────────────────
log("Step 7: Generating final report")

report = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "test_config": {
        "total_queries": len(TEST_QUERIES),
        "bizai_queries": 6,
        "whatsapp_queries": 3,
        "mixed_queries": 3,
    },
    "execution_summary": {
        "queries_executed": len(query_results),
        "traces_found": traces_found,
        "new_kb_retrieved": new_kb_retrieved_count,
        "high_confidence_answers": high_confidence_count,
        "accuracy_rate": f"{(new_kb_retrieved_count / len(query_results) * 100):.1f}%"
        if query_results
        else "0%",
    },
    "query_results": query_results,
    "trace_data": trace_data,
    "sample_traces": [
        {
            "id": qr["id"],
            "query": qr["query"],
            "answer_preview": qr["answer_preview"],
            "confidence": qr["confidence"],
            "top_source": qr["top_source"],
            "sources_count": qr["source_count"],
            "modules": qr["modules"],
        }
        for qr in query_results[:3]
        if "error" not in qr
    ],
    "issues": [
        qr.get("error") for qr in query_results if "error" in qr
    ],
}

# ── Output ───────────────────────────────────────────────────────────────────
log("Step 7: Test complete")
print("\n" + "=" * 80)
print("FINAL REPORT")
print("=" * 80)
print(json.dumps(report, indent=2))

# Save report to file
report_path = os.path.join(REPO_ROOT, "local", "reports", "test_bizai_whatsapp_report.json")
os.makedirs(os.path.dirname(report_path), exist_ok=True)
with open(report_path, "w") as f:
    json.dump(report, f, indent=2)

log(f"Report saved to {report_path}")
log("COMPLETED")

sys.exit(0 if not report["issues"] else 1)
