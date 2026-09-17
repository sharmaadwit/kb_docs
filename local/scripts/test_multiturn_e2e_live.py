#!/usr/bin/env python3
"""
End-to-end multi-turn test against the LIVE SuperAgent endpoint, now that
the Phase 2 module expansion (Campaign Manager, Agent Assist, Channels @
50%) and Phase 1 traffic increase (RCS, Bot Studio @ 75%) are deployed.

5 sequential turns in ONE session, spanning:
  1. Campaign Manager (new, 50%)
  2. Agent Assist (new, 50%)
  3. Channels (new, 50%)
  4. WhatsApp (deliberately NOT gated - should always be standard mode,
     even mid-conversation after prior turns hit consulting mode)
  5. Bot Studio (Phase 1, 75%)

Verifies via SuperAgent's own session continuity (reused session_id) +
Langfuse traces afterward: module/mode routing correctness, answer
accuracy, turn-tracking field shape, and engagement content presence
where consulting mode fired.
"""
import os
import json
import ssl
import uuid
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT_FILE = ROOT / "local" / "reports" / "multiturn_e2e_live_test.jsonl"


def load_env():
    env_path = ROOT / ".env"
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k, v)


def send_query(query: str, session_id: str) -> dict:
    api_url = os.environ.get("SUPERAGENT_API_URL", "")
    api_key = os.environ.get("SUPERAGENT_API_KEY", "")
    user_email = os.environ.get("USER_EMAIL", "adwit.sharma@gupshup.io")

    payload = {"message": query, "session_id": session_id, "user_email_id": user_email}
    headers = {"Content-Type": "application/json", "X-API-Key": api_key}

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(api_url, data=json.dumps(payload).encode(), headers=headers, method="POST")

    result = {"query": query, "session_id": session_id, "timestamp": datetime.now(timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(req, timeout=45, context=ssl_context) as response:
            body = response.read().decode(errors="replace")
            result["status"] = response.status
            result["raw_response"] = body
            # Pull conversation_id if the server echoes one (seen in earlier tests)
            for line in body.splitlines():
                if '"conversation_id"' in line:
                    result["conversation_id_seen"] = line.strip()
                    break
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
    return result


def main():
    load_env()
    session_id = f"e2e-multiturn-{uuid.uuid4().hex[:12]}"

    turns = [
        ("Campaign Manager", "How do I create a segmented campaign in Campaign Manager?"),
        ("Agent Assist", "What guardrails should I add to Agent Assist to prevent hallucinations?"),
        ("Channels", "How do I set up the Instagram channel?"),
        ("WhatsApp (must stay standard)", "How does that compare to setting up the WhatsApp channel?"),
        ("Bot Studio", "Switching topics - how do I use the API node in Bot Studio to call an external API?"),
    ]

    results = []
    for label, query in turns:
        print(f"\n{'='*80}\n[{label}] {query}\n{'='*80}")
        r = send_query(query, session_id)
        results.append({**r, "label": label})
        print(f"status={r['status']}", f"conv_id={r.get('conversation_id_seen','n/a')}")

    with open(REPORT_FILE, "a") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")
    print(f"\nSession ID used: {session_id}")
    print(f"Saved: {REPORT_FILE}")


if __name__ == "__main__":
    main()
