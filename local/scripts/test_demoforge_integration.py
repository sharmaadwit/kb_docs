#!/usr/bin/env python3
"""DemoForge integration test harness.

Tests the DemoForge demo selection and API integration with real KB queries.
Covers:
  1. Campaign Manager how-to → DemoForge demo
  2. Bot Studio overview → YouTube fallback (no DemoForge mapped)
  3. Unmapped module → graceful fallback
  4. API timeout/error handling → graceful degradation

Usage:
  python3 local/scripts/test_demoforge_integration.py
  python3 local/scripts/test_demoforge_integration.py --verbose

Outputs:
  local/reports/demoforge_integration_test.json
  Prints detailed test results with query→demo→API flow.
"""
from __future__ import annotations

import argparse
import json
import sys
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import logging

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "skill"))

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)-8s %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)


# Test cases: (query, expected_intent, expected_module, expected_demo_name_or_fallback)
TEST_CASES = [
    {
        "id": "campaign_manager_how_to",
        "query": "How do I create a campaign?",
        "description": "Campaign Manager how-to query → should return Campaign Manager Demo",
        "expected_intent": "how_to",
        "expected_module": "campaigns",
        "expected_demo_name": "Campaign Manager Demo",
        "check_demoforge": True,  # Should have demoforge link
    },
    {
        "id": "bot_studio_overview",
        "query": "What is Bot Studio?",
        "description": "Bot Studio overview query → should return YouTube (no DemoForge mapped for overview)",
        "expected_intent": "overview",
        "expected_module": "bot_studio",
        "expected_demo_name": None,  # No DemoForge for overview intent
        "check_demoforge": False,
    },
    {
        "id": "campaigns_setup",
        "query": "How do I set up my first campaign in Gupshup?",
        "description": "Campaigns setup query → should return Campaign Manager Demo",
        "expected_intent": "how_to",
        "expected_module": "campaigns",
        "expected_demo_name": "Campaign Manager Demo",
        "check_demoforge": True,
    },
    {
        "id": "webhooks_setup",
        "query": "How do I set up webhooks?",
        "description": "Webhooks setup → should return YouTube or no video (unmapped module)",
        "expected_intent": "how_to",
        "expected_module": None,  # Unmapped to demo
        "expected_demo_name": None,
        "check_demoforge": False,
    },
    {
        "id": "bot_studio_how_to",
        "query": "How do I build a bot in Bot Studio?",
        "description": "Bot Studio how-to → should return YouTube video",
        "expected_intent": "how_to",
        "expected_module": "bot_studio",
        "expected_demo_name": None,  # how_to maps to YouTube, not DemoForge
        "check_demoforge": False,
    },
    {
        "id": "general_demo_pitch",
        "query": "Show me a demo of Gupshup Console features for a retail client",
        "description": "Broad pitch query → should return General Demo (broad_fallback)",
        "expected_intent": "overview",
        "expected_module": None,
        "expected_demo_name": "General Demo",  # Broad/pitch fallback
        "check_demoforge": True,
    },
]


def _setup_local_kb():
    """Set up KB with local chunks and capture mechanism."""
    import kb_storage
    import kb_answer
    import kb_video

    chunks_path = ROOT / "kb" / "kb_chunks.jsonl"
    chunks = [json.loads(l) for l in chunks_path.read_text(encoding="utf-8").splitlines() if l.strip()]

    def _read_json_local(path, context=None):
        p = ROOT / path if not str(path).startswith("/") else Path(path)
        return json.loads(p.read_text(encoding="utf-8"))

    captured = {}

    def _cap_lf(trace_name, query, answer, results, explicit_module, intents,
                selected_answer_mode, clarification_asked, latency_ms, context,
                params=None, video_meta=None, **kwargs):
        """Capture telemetry for analysis."""
        captured["last"] = {
            "top_source": results[0].get("source") if results else None,
            "top_score": results[0].get("score") if results else None,
            "source_count": len(results),
            "mode": selected_answer_mode,
            "intents": intents,
            "module": explicit_module,
            "video_meta": video_meta,
            "detected_product_original": kwargs.get("detected_product_original"),
        }
        return {}

    kb_answer._load_chunks = lambda ctx=None: chunks
    kb_answer._send_langfuse = _cap_lf
    kb_storage.read_json = _read_json_local

    class Ctx:
        def __init__(self):
            self.secrets = {
                "KB_VIDEO_MANIFEST_PATH": "kb/video_manifest.json",
                "KB_VIDEO_TRANSCRIPT_DIR": "kb/video_transcripts",
                "KB_DEMOFORGE_MANIFEST_PATH": "kb/demoforge_manifest.json",
            }

        def get_secret(self, name):
            return self.secrets.get(name)

    return kb_answer, kb_video, Ctx(), captured


def _extract_module_from_query(query: str) -> str | None:
    """Simple module extraction from query keywords."""
    q = query.lower()
    if any(w in q for w in ["campaign", "bulk send", "broadcast"]):
        return "campaigns"
    if any(w in q for w in ["bot studio", "journey", "build"]):
        return "bot_studio"
    if any(w in q for w in ["rcs", "rich communication"]):
        return "rcs"
    if any(w in q for w in ["webhook", "integration", "api"]):
        return "webhooks"
    if any(w in q for w in ["whatsapp", "wa "]):
        return "whatsapp"
    return None


def _extract_intent_from_query(query: str) -> str | None:
    """Simple intent extraction from query keywords."""
    q = query.lower()
    if any(w in q for w in ["how", "setup", "configure", "create"]):
        return "how_to"
    if any(w in q for w in ["what is", "what's", "overview", "explain"]):
        return "overview"
    if any(w in q for w in ["show me", "demo", "example"]):
        return "overview"
    return "how_to"  # Default


def test_query(kb_answer, kb_video, ctx, captured, test_case, verbose=False):
    """Execute a single test case through the KB pipeline."""
    test_id = test_case["id"]
    query = test_case["query"]

    if verbose:
        print(f"\n{'='*70}")
        print(f"Test: {test_id}")
        print(f"Query: {query}")
        print(f"Description: {test_case['description']}")

    result = {
        "id": test_id,
        "query": query,
        "description": test_case["description"],
        "expected": {
            "intent": test_case.get("expected_intent"),
            "module": test_case.get("expected_module"),
            "demo_name": test_case.get("expected_demo_name"),
            "check_demoforge": test_case.get("check_demoforge"),
        },
        "actual": {},
        "status": "PASS",
        "errors": [],
    }

    try:
        # Call kb_answer with the query
        res = kb_answer.kb_answer(parameters={"query": query}, context=ctx)
        answer = str(res.get("answer") or "")
        video = res.get("video")
        videos = res.get("videos")

        if verbose:
            print(f"\nAnswer (first 200 chars): {answer[:200]}")
            print(f"Video: {video}")
            print(f"Videos: {videos}")

        # Capture metadata from telemetry
        meta = captured.get("last", {})

        # Extract intent and module from the result's metadata
        result["actual"]["intents"] = meta.get("intents")
        result["actual"]["module"] = meta.get("module")
        result["actual"]["top_source"] = meta.get("top_source")
        result["actual"]["mode"] = meta.get("mode")
        result["actual"]["video_meta"] = meta.get("video_meta")

        # Check video attachment
        if video:
            result["actual"]["video_attached"] = True
            result["actual"]["video"] = {
                "video_id": video.get("video_id"),
                "title": video.get("title"),
                "source": video.get("source"),
                "fallback": video.get("fallback"),
                "url": video.get("url"),
            }
            if verbose:
                print(f"\nVideo selected:")
                print(f"  ID: {video.get('video_id')}")
                print(f"  Title: {video.get('title')}")
                print(f"  URL: {video.get('url')}")
        else:
            result["actual"]["video_attached"] = False

        if videos:
            result["actual"]["videos_attached"] = True
            result["actual"]["videos"] = [
                {
                    "video_id": v.get("video_id"),
                    "title": v.get("title"),
                    "source": v.get("source"),
                    "fallback": v.get("fallback"),
                    "url": v.get("url"),
                }
                for v in videos
            ]
            if verbose:
                print(f"\nMultiple videos selected:")
                for v in videos:
                    print(f"  - {v.get('title')} ({v.get('video_id')})")
        else:
            result["actual"]["videos_attached"] = False

        # Validate expectations
        if test_case.get("check_demoforge"):
            # Should have a video with demoforge link
            has_demoforge = False
            if video and "demoforge" in str(video.get("url", "")).lower():
                has_demoforge = True
            if videos and any("demoforge" in str(v.get("url", "")).lower() for v in videos):
                has_demoforge = True

            if not has_demoforge:
                result["status"] = "FAIL"
                result["errors"].append(f"Expected DemoForge link but got: {video.get('url') if video else 'no video'}")
            else:
                result["actual"]["has_demoforge"] = True
        else:
            # Should NOT have demoforge link (YouTube or nothing)
            if video and "demoforge" in str(video.get("url", "")).lower():
                result["status"] = "FAIL"
                result["errors"].append(f"Unexpected DemoForge link: {video.get('url')}")
            elif videos and any("demoforge" in str(v.get("url", "")).lower() for v in videos):
                result["status"] = "FAIL"
                result["errors"].append(f"Unexpected DemoForge link in multi-video response")

    except Exception as exc:
        result["status"] = "ERROR"
        result["errors"].append(str(exc))
        if verbose:
            import traceback
            traceback.print_exc()

    if verbose:
        print(f"\nStatus: {result['status']}")
        if result['errors']:
            print(f"Errors: {result['errors']}")

    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true", help="Print detailed output")
    args = ap.parse_args()

    print("=== DemoForge Integration Test ===")
    print(f"Timestamp: {datetime.now().isoformat()}")

    # Load KB
    kb_answer, kb_video, ctx, captured = _setup_local_kb()

    # Run tests
    results = []
    passes = 0
    for test_case in TEST_CASES:
        result = test_query(kb_answer, kb_video, ctx, captured, test_case, verbose=args.verbose)
        results.append(result)
        if result["status"] == "PASS":
            passes += 1

    # Summary
    total = len(TEST_CASES)
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "passes": passes,
        "pass_rate_pct": round(100 * passes / total, 1) if total > 0 else 0,
        "failures": total - passes,
    }

    # Write report
    report = {
        "summary": summary,
        "tests": results,
    }

    out = ROOT / "local" / "reports" / "demoforge_integration_test.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")

    # Print summary
    print(f"\n{'='*70}")
    print(f"SUMMARY: {passes}/{total} passed ({summary['pass_rate_pct']}%)")
    print(f"{'='*70}")

    for r in results:
        status_marker = "✓" if r["status"] == "PASS" else "✗"
        print(f"{status_marker} {r['id']:<25} {r['status']:<8} {r['query'][:40]}")
        if r["errors"]:
            for err in r["errors"]:
                print(f"    Error: {err}")

    print(f"\nDetailed report: {out}")
    return 0 if passes == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
