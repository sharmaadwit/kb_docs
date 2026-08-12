#!/usr/bin/env python3
"""
Pre-deployment comprehensive baseline export.

Captures all key metrics by module, segment, confidence, and intent
BEFORE Phase 1 feature flag is enabled. Used as control baseline to
measure Phase 1 consulting-tone impact.

Metrics exported:
  - By module (RCS, Bot Studio, WhatsApp, etc.)
  - By segment (Standalone, CC Express)
  - By intent (setup, behavior, troubleshooting, etc.)
  - By confidence band (0-0.3, 0.3-0.6, 0.6-0.9, 0.9-1.0)
  - Aggregate (all traffic)

Run: python3 local/scripts/baseline_data_export.py
Output: local/reports/baseline_metrics_pre_phase1.json
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
import base64
import ssl
from collections import defaultdict
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

def load_env():
    """Load .env file if it exists."""
    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split("=", 1)
                    if len(parts) == 2:
                        os.environ.setdefault(parts[0], parts[1])

def segment_by_email(email):
    """Segment user by email domain."""
    if not email:
        return "unknown"
    if "@ccexpress.gupshup.io" in email:
        return "cc_express"
    return "standalone"

def get_intent_from_trace(trace):
    """Extract intent from trace metadata or KB answer policy."""
    try:
        if isinstance(trace, dict):
            metadata = trace.get("metadata") or {}
            if "intent" in metadata:
                return metadata["intent"]
            # Try tags as fallback
            if "tags" in trace and isinstance(trace["tags"], list):
                for tag in trace["tags"]:
                    if tag.startswith("intent:"):
                        return tag.split(":", 1)[1]
    except:
        pass
    return "unknown"

def get_module_from_trace(trace):
    """Extract module from trace metadata."""
    try:
        if isinstance(trace, dict):
            metadata = trace.get("metadata") or {}
            if "module" in metadata:
                return metadata["module"]
            # Try tags as fallback
            if "tags" in trace and isinstance(trace["tags"], list):
                for tag in trace["tags"]:
                    if tag.startswith("module:"):
                        return tag.split(":", 1)[1]
    except:
        pass
    return "unknown"

def get_confidence_from_trace(trace):
    """Extract confidence score from trace metadata."""
    try:
        if isinstance(trace, dict):
            metadata = trace.get("metadata") or {}
            if "confidence" in metadata:
                conf = metadata["confidence"]
                if isinstance(conf, (int, float)):
                    return float(conf)
    except:
        pass
    return None

def confidence_band(conf):
    """Bucket confidence into bands."""
    if conf is None:
        return "unknown"
    if conf < 0.3:
        return "low_0_0.3"
    elif conf < 0.6:
        return "medium_0.3_0.6"
    elif conf < 0.9:
        return "high_0.6_0.9"
    else:
        return "very_high_0.9_1.0"

def is_idk_answer(trace):
    """Check if answer was IDK."""
    try:
        if isinstance(trace, dict):
            metadata = trace.get("metadata") or {}
            if "is_idk" in metadata:
                return bool(metadata["is_idk"])
            if "answer" in metadata:
                answer = str(metadata["answer"]).lower()
                return "don't know" in answer or "i don't know" in answer
    except:
        pass
    return False

def fetch_traces_from_langfuse(days=30):
    """Fetch traces from Langfuse REST API."""
    load_env()

    host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")
    pub = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
    sec = os.environ.get("LANGFUSE_SECRET_KEY", "")

    if not pub or not sec:
        print("❌ Langfuse credentials missing from env")
        return []

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    # Format timestamps as ISO 8601
    from_ts = start_time.isoformat() + "Z"
    to_ts = end_time.isoformat() + "Z"

    all_traces = []
    page = 1

    while True:
        url = f"{host}/api/public/traces?fromTimestamp={urllib.parse.quote(from_ts)}&toTimestamp={urllib.parse.quote(to_ts)}&limit=100&page={page}"

        auth_string = base64.b64encode(f"{pub}:{sec}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth_string}",
            "Content-Type": "application/json"
        }

        try:
            req = urllib.request.Request(url, headers=headers)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
                data = json.loads(response.read().decode())

                if "data" in data:
                    traces = data["data"]
                    if not traces:
                        break
                    all_traces.extend(traces)
                    page += 1
                else:
                    break
        except Exception as e:
            print(f"❌ Error fetching traces: {e}")
            break

    return all_traces

def main():
    print("=" * 80)
    print("PRE-DEPLOYMENT BASELINE DATA EXPORT")
    print("=" * 80)
    print()

    # Fetch last 30 days of traces
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=30)

    print(f"📊 Fetching traces from {start_time.date()} to {end_time.date()}...")
    print()

    trace_list = fetch_traces_from_langfuse(days=30)
    print(f"✅ Fetched {len(trace_list)} traces")
    print()

    # Initialize aggregation buckets
    metrics = {
        "export_timestamp": datetime.utcnow().isoformat(),
        "data_range": f"{start_time.date()} to {end_time.date()}",
        "total_traces": len(trace_list),
        "by_module": defaultdict(lambda: {
            "count": 0,
            "idk_count": 0,
            "answer_count": 0,
            "avg_confidence": 0.0,
            "confidence_counts": defaultdict(int),
        }),
        "by_segment": defaultdict(lambda: {
            "count": 0,
            "idk_count": 0,
            "answer_count": 0,
            "avg_confidence": 0.0,
        }),
        "by_intent": defaultdict(lambda: {
            "count": 0,
            "idk_count": 0,
            "answer_count": 0,
            "avg_confidence": 0.0,
        }),
        "by_confidence_band": defaultdict(lambda: {
            "count": 0,
            "idk_count": 0,
            "answer_count": 0,
        }),
        "module_by_segment": defaultdict(lambda: defaultdict(lambda: {
            "count": 0,
            "idk_count": 0,
            "answer_count": 0,
        })),
        "aggregate": {
            "count": 0,
            "idk_count": 0,
            "answer_count": 0,
            "avg_confidence": 0.0,
            "answer_rate": 0.0,
            "idk_rate": 0.0,
        }
    }

    confidence_sum = 0.0
    confidence_count = 0

    # Process each trace
    for trace in trace_list:
        module = get_module_from_trace(trace)
        intent = get_intent_from_trace(trace)
        email = (trace.get("userId") if isinstance(trace, dict) else trace.user_id) or "unknown"
        segment = segment_by_email(email)
        confidence = get_confidence_from_trace(trace)
        is_idk = is_idk_answer(trace)

        conf_band = confidence_band(confidence)

        # Update aggregations
        metrics["by_module"][module]["count"] += 1
        metrics["by_segment"][segment]["count"] += 1
        metrics["by_intent"][intent]["count"] += 1
        metrics["by_confidence_band"][conf_band]["count"] += 1
        metrics["module_by_segment"][module][segment]["count"] += 1

        metrics["aggregate"]["count"] += 1

        if is_idk:
            metrics["by_module"][module]["idk_count"] += 1
            metrics["by_segment"][segment]["idk_count"] += 1
            metrics["by_intent"][intent]["idk_count"] += 1
            metrics["by_confidence_band"][conf_band]["idk_count"] += 1
            metrics["module_by_segment"][module][segment]["idk_count"] += 1
            metrics["aggregate"]["idk_count"] += 1
        else:
            metrics["by_module"][module]["answer_count"] += 1
            metrics["by_segment"][segment]["answer_count"] += 1
            metrics["by_intent"][intent]["answer_count"] += 1
            metrics["by_confidence_band"][conf_band]["answer_count"] += 1
            metrics["module_by_segment"][module][segment]["answer_count"] += 1
            metrics["aggregate"]["answer_count"] += 1

        if confidence is not None:
            confidence_sum += confidence
            confidence_count += 1
            metrics["by_module"][module]["confidence_counts"][conf_band] += 1

    # Calculate rates and averages
    if confidence_count > 0:
        avg_conf = confidence_sum / confidence_count
        metrics["aggregate"]["avg_confidence"] = round(avg_conf, 4)

    if metrics["aggregate"]["count"] > 0:
        metrics["aggregate"]["answer_rate"] = round(
            metrics["aggregate"]["answer_count"] / metrics["aggregate"]["count"] * 100, 2
        )
        metrics["aggregate"]["idk_rate"] = round(
            metrics["aggregate"]["idk_count"] / metrics["aggregate"]["count"] * 100, 2
        )

    # Calculate per-module averages and rates
    for module, data in metrics["by_module"].items():
        if data["count"] > 0:
            answer_rate = data["answer_count"] / data["count"] * 100
            idk_rate = data["idk_count"] / data["count"] * 100
            data["answer_rate"] = round(answer_rate, 2)
            data["idk_rate"] = round(idk_rate, 2)

            # Calculate avg confidence for this module
            conf_sum = 0
            conf_count = 0
            for band, count in data["confidence_counts"].items():
                conf_sum += count
                conf_count += count
            if conf_count > 0:
                data["avg_confidence"] = round(conf_sum / conf_count, 4)

    # Calculate per-segment averages and rates
    for segment, data in metrics["by_segment"].items():
        if data["count"] > 0:
            answer_rate = data["answer_count"] / data["count"] * 100
            idk_rate = data["idk_count"] / data["count"] * 100
            data["answer_rate"] = round(answer_rate, 2)
            data["idk_rate"] = round(idk_rate, 2)

    # Calculate per-intent averages and rates
    for intent, data in metrics["by_intent"].items():
        if data["count"] > 0:
            answer_rate = data["answer_count"] / data["count"] * 100
            idk_rate = data["idk_count"] / data["count"] * 100
            data["answer_rate"] = round(answer_rate, 2)
            data["idk_rate"] = round(idk_rate, 2)

    # Calculate per-confidence-band rates
    for band, data in metrics["by_confidence_band"].items():
        if data["count"] > 0:
            answer_rate = data["answer_count"] / data["count"] * 100
            idk_rate = data["idk_count"] / data["count"] * 100
            data["answer_rate"] = round(answer_rate, 2)
            data["idk_rate"] = round(idk_rate, 2)

    # Calculate per-module-segment rates
    for module, segments in metrics["module_by_segment"].items():
        for segment, data in segments.items():
            if data["count"] > 0:
                answer_rate = data["answer_count"] / data["count"] * 100
                idk_rate = data["idk_count"] / data["count"] * 100
                data["answer_rate"] = round(answer_rate, 2)
                data["idk_rate"] = round(idk_rate, 2)

    # Convert defaultdicts to regular dicts for JSON serialization
    metrics["by_module"] = {k: dict(v) for k, v in metrics["by_module"].items()}
    metrics["by_segment"] = {k: dict(v) for k, v in metrics["by_segment"].items()}
    metrics["by_intent"] = {k: dict(v) for k, v in metrics["by_intent"].items()}
    metrics["by_confidence_band"] = {k: dict(v) for k, v in metrics["by_confidence_band"].items()}
    metrics["module_by_segment"] = {
        k: {sk: dict(sv) for sk, sv in v.items()}
        for k, v in metrics["module_by_segment"].items()
    }

    # Save to file
    output_path = "local/reports/baseline_metrics_pre_phase1.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=2)

    print("=" * 80)
    print("✅ BASELINE EXPORT COMPLETE")
    print("=" * 80)
    print()
    print(f"📁 Saved to: {output_path}")
    print()
    print("📊 SUMMARY METRICS")
    print("-" * 80)
    print(f"Total traces:      {metrics['aggregate']['count']}")
    print(f"Answer rate:       {metrics['aggregate']['answer_rate']}%")
    print(f"IDK rate:          {metrics['aggregate']['idk_rate']}%")
    print(f"Avg confidence:    {metrics['aggregate']['avg_confidence']}")
    print()
    print("BY MODULE (top 5)")
    print("-" * 80)
    top_modules = sorted(
        metrics["by_module"].items(),
        key=lambda x: x[1]["count"],
        reverse=True
    )[:5]
    for module, data in top_modules:
        print(f"{module:20} | count: {data['count']:5} | answer: {data['answer_rate']:5.1f}% | idk: {data['idk_rate']:5.1f}%")
    print()
    print("BY SEGMENT")
    print("-" * 80)
    for segment, data in metrics["by_segment"].items():
        print(f"{segment:20} | count: {data['count']:5} | answer: {data['answer_rate']:5.1f}% | idk: {data['idk_rate']:5.1f}%")
    print()
    print("BY INTENT (top 5)")
    print("-" * 80)
    top_intents = sorted(
        metrics["by_intent"].items(),
        key=lambda x: x[1]["count"],
        reverse=True
    )[:5]
    for intent, data in top_intents:
        print(f"{intent:20} | count: {data['count']:5} | answer: {data['answer_rate']:5.1f}% | idk: {data['idk_rate']:5.1f}%")
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
