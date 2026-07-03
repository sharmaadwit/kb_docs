#!/usr/bin/env python3
"""
Analyze DemoForge video matching against module labels in kb_answer traces.

Fetches recent kb_answer traces from Langfuse (PROD_EXT environment),
extracts video metadata, and analyzes module-to-video matching accuracy.

Outputs structured JSON report to stdout.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
from collections import Counter, defaultdict
import base64
import urllib.request
import urllib.parse
import ssl

# Module-to-keywords mapping for validation
MODULE_KEYWORDS = {
    "Bot Studio": {"keywords": ["bot", "studio", "automation", "conversation", "workflow"], "video_markers": ["bot", "studio"]},
    "CTX": {"keywords": ["ctx", "context", "customer", "context exchange"], "video_markers": ["context", "ctx"]},
    "AI Admin": {"keywords": ["ai", "admin", "administration", "settings", "configuration"], "video_markers": ["ai", "admin"]},
    "Campaign Manager": {"keywords": ["campaign", "manager", "marketing", "email", "message"], "video_markers": ["campaign"]},
    "Personalize": {"keywords": ["personalize", "personalization", "segment", "dynamic"], "video_markers": ["personalize"]},
}

# Expected module platforms (normalization)
PLATFORM_MAPPING = {
    "Bot Studio": "demo_videos",
    "CTX": "demo_videos",
    "AI Admin": "demo_videos",
    "Campaign Manager": "demo_videos",
    "Personalize": "demo_videos",
}

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "local" / "reports" / "video_matching_analysis.json"


def _load_env():
    """Load .env file into os.environ."""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and not os.getenv(key):
                os.environ[key] = val


def fetch_kb_answer_traces(limit: int = 20, timeout: int = 60) -> List[Dict[str, Any]]:
    """
    Fetch recent kb_answer traces from Langfuse API.

    Returns:
        List of trace dictionaries with input, output, metadata, and metadata.
    """
    _load_env()

    host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")
    pub = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
    sec = os.environ.get("LANGFUSE_SECRET_KEY", "")

    if not pub or not sec:
        print("ERROR: LANGFUSE_PUBLIC_KEY or LANGFUSE_SECRET_KEY not set", file=sys.stderr)
        return []

    # Build SSL context
    try:
        import certifi
        ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

    try:
        creds = base64.b64encode(f"{pub}:{sec}".encode()).decode()
        headers = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

        # Fetch traces filtered by name="kb_answer"
        params = urllib.parse.urlencode({
            "name": "kb_answer",
            "limit": limit,
        })
        url = f"{host}/api/public/traces?{params}"

        print(f"Fetching {limit} kb_answer traces from {host}...", file=sys.stderr)
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            body = json.loads(resp.read())

        traces = body.get("data", [])
        print(f"Fetched {len(traces)} kb_answer traces", file=sys.stderr)
        return traces

    except Exception as e:
        print(f"ERROR fetching traces: {e}", file=sys.stderr)
        return []


def extract_trace_data(trace: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract relevant fields from a trace.

    Returns dict with:
      - trace_id
      - timestamp
      - query
      - module_label
      - top_source
      - video_title
      - video_platform
      - demoforge_demo_id
      - confidence_score
      - answer_text
    """
    metadata = trace.get("metadata") or {}
    output = trace.get("output") or {}

    # Extract nested metadata (may be in top-level or under "metadata" key)
    if isinstance(output, dict):
        output_metadata = output.get("metadata") or {}
    else:
        output_metadata = {}

    # Merge metadata sources
    merged_meta = {**metadata, **output_metadata}

    # Extract video data from metadata
    video_data = merged_meta.get("video_data") or {}
    if isinstance(video_data, str):
        try:
            video_data = json.loads(video_data)
        except:
            video_data = {}

    # Extract video platform from either video_data or direct metadata
    video_platform = video_data.get("platform") or merged_meta.get("video_platform")

    return {
        "trace_id": trace.get("id") or "",
        "timestamp": trace.get("timestamp") or "",
        "query": (trace.get("input") or {}).get("query") or merged_meta.get("query") or "",
        "module_label": merged_meta.get("module_label") or "",
        "top_source": merged_meta.get("top_source") or "",
        "video_title": video_data.get("title") or merged_meta.get("video_title") or "",
        "video_platform": video_platform or "",
        "demoforge_demo_id": video_data.get("demo_id") or merged_meta.get("demoforge_demo_id") or "",
        "confidence_score": merged_meta.get("top_score") or None,
        "answer_text": (output.get("answer") if isinstance(output, dict) else "") or "",
    }


def infer_module_from_query(query: str) -> Optional[str]:
    """Infer module from query text if not explicitly labeled."""
    if not query:
        return None

    query_lower = query.lower()

    for module, config in MODULE_KEYWORDS.items():
        for keyword in config["keywords"]:
            if keyword.lower() in query_lower:
                return module

    return None


def check_video_module_match(module: str, video_title: str, video_platform: str) -> Dict[str, Any]:
    """
    Check if video matches the module.

    Returns dict with:
      - matches: bool
      - module_platform_expected: str
      - platform_match: bool
      - title_contains_module_marker: bool
      - confidence: float (0-1)
    """
    if not module or not video_title:
        return {
            "matches": False,
            "reason": "missing_module_or_video",
            "module_platform_expected": PLATFORM_MAPPING.get(module, ""),
            "platform_match": False,
            "title_contains_module_marker": False,
            "confidence": 0.0,
        }

    config = MODULE_KEYWORDS.get(module, {})
    expected_platform = PLATFORM_MAPPING.get(module, "demo_videos")
    video_title_lower = video_title.lower()

    # Check platform match
    platform_match = (video_platform or "").lower() == expected_platform.lower() if video_platform else False

    # Check if video title contains module markers
    markers = config.get("video_markers", [])
    title_contains_marker = any(m.lower() in video_title_lower for m in markers)

    # Confidence scoring
    confidence = 0.0
    reasons = []

    if platform_match:
        confidence += 0.5
        reasons.append("platform_match")

    if title_contains_marker:
        confidence += 0.5
        reasons.append("title_marker_found")

    matches = confidence >= 1.0

    return {
        "matches": matches,
        "reason": " + ".join(reasons) if reasons else "no_match",
        "module_platform_expected": expected_platform,
        "platform_match": platform_match,
        "title_contains_module_marker": title_contains_marker,
        "confidence": confidence,
    }


def analyze_video_matching(traces: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze video matching for all traces.

    Returns comprehensive analysis with summary, per-trace details, and recommendations.
    """
    extracted = []
    video_matching_results = []

    # Extract data from all traces
    for trace in traces:
        data = extract_trace_data(trace)
        extracted.append(data)

        # Infer module if not present
        module = data["module_label"] or infer_module_from_query(data["query"])

        # Check video match
        if data["video_title"]:
            match_result = check_video_module_match(
                module or "",
                data["video_title"],
                data["video_platform"]
            )
            video_matching_results.append({
                **data,
                "inferred_module": module,
                "match_result": match_result,
            })

    # Build summary statistics
    total_traces = len(extracted)
    traces_with_video = sum(1 for t in extracted if t["video_title"])
    traces_with_module = sum(1 for t in extracted if t["module_label"])
    traces_with_matches = sum(1 for r in video_matching_results if r["match_result"]["matches"])

    video_attachment_rate = (traces_with_video / total_traces * 100) if total_traces > 0 else 0.0

    # Module-video matching accuracy (only for traces with both)
    matching_accuracy = (traces_with_matches / len(video_matching_results) * 100) if video_matching_results else 0.0

    # Analyze by module
    by_module = defaultdict(lambda: {"total": 0, "with_video": 0, "matching": 0, "confidence_sum": 0})
    for result in video_matching_results:
        module = result.get("inferred_module") or "unknown"
        by_module[module]["total"] += 1

        if result["video_title"]:
            by_module[module]["with_video"] += 1

        if result["match_result"]["matches"]:
            by_module[module]["matching"] += 1

        by_module[module]["confidence_sum"] += result["match_result"]["confidence"]

    # Calculate module-level stats
    module_stats = {}
    for module, stats in by_module.items():
        total = stats["total"]
        matching = stats["matching"]
        confidence_sum = stats["confidence_sum"]

        module_stats[module] = {
            "total_traces": total,
            "with_video": stats["with_video"],
            "matching_count": matching,
            "accuracy": (matching / total * 100) if total > 0 else 0.0,
            "avg_confidence": (confidence_sum / total) if total > 0 else 0.0,
        }

    # Find mismatches for recommendation
    mismatches = [
        r for r in video_matching_results
        if r["video_title"] and not r["match_result"]["matches"]
    ]

    mismatches = sorted(
        mismatches,
        key=lambda x: x["match_result"]["confidence"],
        reverse=True
    )[:10]  # Top 10 mismatches

    # Generate recommendations
    recommendations = []

    for mismatch in mismatches:
        module = mismatch.get("inferred_module") or "unknown"
        video = mismatch["video_title"]
        reason = mismatch["match_result"]["reason"]

        recommendations.append({
            "query": mismatch["query"][:100],
            "module": module,
            "current_video": video,
            "issue": reason,
            "expected_platform": mismatch["match_result"]["module_platform_expected"],
            "current_platform": mismatch["video_platform"],
        })

    # Overall recommendations
    overall_recommendations = []

    if video_attachment_rate < 50:
        overall_recommendations.append(
            "Less than 50% of traces have video attachments. "
            "Consider increasing video attachment coverage in kb_answer logic."
        )

    if matching_accuracy < 80:
        overall_recommendations.append(
            "Module-video matching accuracy is below 80%. "
            "Review video selection logic to better align with module context."
        )

    if any(m["match_result"]["reason"] == "missing_module_or_video" for m in video_matching_results):
        overall_recommendations.append(
            "Some traces have missing module labels or video titles. "
            "Ensure metadata is properly populated in kb_answer output."
        )

    if not overall_recommendations:
        overall_recommendations.append(
            "Video matching is performing well. Continue monitoring for edge cases."
        )

    return {
        "summary": {
            "analysis_timestamp": datetime.utcnow().isoformat() + "Z",
            "total_traces_analyzed": total_traces,
            "traces_with_video": traces_with_video,
            "traces_with_module": traces_with_module,
            "video_attachment_rate_percent": round(video_attachment_rate, 2),
            "traces_with_video_module_match": traces_with_matches,
            "module_video_matching_accuracy_percent": round(matching_accuracy, 2),
        },
        "module_stats": dict(module_stats),
        "traces": [
            {
                "trace_id": r["trace_id"],
                "timestamp": r["timestamp"],
                "query": r["query"][:150],
                "module": r.get("inferred_module") or "unknown",
                "video_title": r["video_title"],
                "video_platform": r["video_platform"],
                "demoforge_demo_id": r["demoforge_demo_id"],
                "confidence_score": r["confidence_score"],
                "match_result": r["match_result"],
            }
            for r in video_matching_results
        ],
        "top_mismatches": recommendations,
        "recommendations": overall_recommendations,
    }


def main() -> int:
    """Main entry point."""
    try:
        # Fetch traces
        traces = fetch_kb_answer_traces(limit=20)

        if not traces:
            print("ERROR: No traces fetched from Langfuse", file=sys.stderr)
            return 1

        # Analyze video matching
        analysis = analyze_video_matching(traces)

        # Output to stdout
        print(json.dumps(analysis, indent=2, default=str))

        # Also save to file
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(analysis, indent=2, default=str), encoding="utf-8")
        print(f"\n# Report saved to {OUT}", file=sys.stderr)

        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
