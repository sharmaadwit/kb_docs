#!/usr/bin/env python3
"""Test 2 queries -> verify consolidated telemetry via Langfuse v4 SDK.

Verifies:
  1. No separate 'demoforge_share_link' traces created (consolidated).
  2. video_meta params present in the kb_answer trace, clearly indicating
     video source (video_platform, demoforge_demo_id, etc.) while preserving
     the original shape (video_source KB path, video_channel).

LOCAL ANALYSIS ONLY — skill code unchanged. Loads .env for real DEMOFORGE_PAT
so a share link actually gets minted and video_meta populates.
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "skill"))
sys.path.insert(0, os.path.dirname(__file__))

from langfuse_client import get_client, list_traces, get_trace, _load_env_from_dotenv

# Load ALL env from .env (DemoForge + Langfuse creds) before importing skill.
def _load_full_dotenv():
    dotenv = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    if not os.path.exists(dotenv):
        return
    with open(dotenv) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip('"').strip("'")
            if key and not os.getenv(key):
                os.environ[key] = val

_load_full_dotenv()

from skill import kb_answer as kb_answer_module


class Ctx:
    """Context that resolves secrets from the loaded environment."""
    def __init__(self):
        self.secrets = {}
        self.user_email = "adwit.sharma@gupshup.io"

    def get_secret(self, key):
        return os.getenv(key)


def run_query(query, label):
    print(f"\n{'='*70}\nRunning: {label}\nQuery: {query}\n{'='*70}")
    corr_id = f"sdktest_{label.replace(' ', '_')}_{int(time.time()*1000)}"
    try:
        # trace_env is NOT hardcoded here — it comes from KB_ENV in .env
        # (loaded into the environment above), which the skill resolves via
        # context.get_secret("KB_ENV") -> trace_env=local. SuperAgent prod sets
        # its own KB_ENV, so this only tags local test traffic.
        kb_answer_module.kb_answer(
            parameters={
                "query": query,
                "user_email": "adwit.sharma@gupshup.io",
            },
            context=Ctx(),
            correlation_id=corr_id,
        )
        print(f"✓ Executed  (correlation_id={corr_id})")
        return corr_id
    except Exception as e:
        import traceback
        print(f"✗ Failed: {e}")
        traceback.print_exc()
        return None


def analyze(client, run_start_ts):
    """Fetch traces created after run_start_ts and report the two checks."""
    print(f"\n\n{'='*70}\nVERIFICATION (traces since test start)\n{'='*70}")

    # Check 1: any demoforge_share_link events after run start?
    df = list_traces(client, name="demoforge_share_link", limit=10)
    new_df = [t for t in df if t.timestamp.timestamp() >= run_start_ts]
    if new_df:
        print(f"\n✗ CHECK 1 FAIL: {len(new_df)} new 'demoforge_share_link' traces:")
        for t in new_df:
            print(f"    - {t.id}  {t.timestamp}")
    else:
        print(f"\n✓ CHECK 1 PASS: No new separate 'demoforge_share_link' traces")

    # Check 2: kb_answer traces since run start carry video_meta params
    ka = list_traces(client, name="kb_answer", limit=10)
    new_ka = [t for t in ka if t.timestamp.timestamp() >= run_start_ts]
    print(f"\nCHECK 2: {len(new_ka)} new kb_answer trace(s) — video params:")
    for t in new_ka:
        full = get_trace(client, t.id)
        md = full.metadata or {}
        q = (full.input or {}).get("query") if isinstance(full.input, dict) else full.input
        print(f"\n  Trace: {full.id}")
        print(f"    query: {q}")
        print(f"    trace_env:                 {md.get('trace_env')}   <- 'local' for local testing")
        print(f"    -- original shape --")
        print(f"    video_attached:            {md.get('video_attached')}")
        print(f"    video_channel:             {md.get('video_channel')}")
        print(f"    video_id:                  {md.get('video_id')}")
        print(f"    video_title:               {md.get('video_title')}")
        print(f"    video_source:              {md.get('video_source')}   <- KB path (None for DemoForge)")
        print(f"    video_fallback:            {md.get('video_fallback')}")
        print(f"    video_appended_to_answer:  {md.get('video_appended_to_answer')}")
        print(f"    -- source indicator + demoforge extras --")
        print(f"    video_platform:            {md.get('video_platform')}")
        print(f"    demoforge_demo_id:         {md.get('demoforge_demo_id')}")
        print(f"    demoforge_share_token:     {md.get('demoforge_share_token')}")
        print(f"    demoforge_api_latency_ms:  {md.get('demoforge_api_latency_ms')}")
        print(f"    demoforge_fallback_reason: {md.get('demoforge_fallback_reason')}")


def main():
    print("="*70)
    print("CONSOLIDATED TELEMETRY TEST (Langfuse v4 SDK)")
    print("="*70)

    run_start = time.time()

    run_query("How do I create a campaign in Gupshup?", "Campaign Manager")
    run_query("How do I set up Agent Assist?", "Agent Assist setup")

    print("\nWaiting 5s for Langfuse ingestion...")
    time.sleep(5)

    client = get_client()
    analyze(client, run_start)


if __name__ == "__main__":
    main()
