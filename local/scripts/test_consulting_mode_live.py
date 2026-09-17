#!/usr/bin/env python3
"""
Test the consulting-mode engagement build (best practices, related-feature
fitment) via the LIVE SuperAgent endpoint, now that the fix is deployed.

Queries below are pre-verified via hashlib.md5(query) % 100 < 50 to
deterministically route to consulting mode for RCS/Bot Studio (the only
Phase 1 gated modules) — see skill/kb_answer.py:_resolve_answer_mode.
"""
import os
import sys
import json
import ssl
import uuid
import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT_FILE = ROOT / "local" / "reports" / "consulting_mode_live_test.jsonl"


def load_env():
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k, v)


def send_query(query: str) -> dict:
    api_url = os.environ.get("SUPERAGENT_API_URL", "")
    api_key = os.environ.get("SUPERAGENT_API_KEY", "")
    user_email = os.environ.get("USER_EMAIL", "adwit.sharma@gupshup.io")

    session_id = f"consulting-live-test-{uuid.uuid4().hex[:12]}"
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
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
    return result


def main():
    load_env()

    queries = [
        "How do I register as an RCS agent?",
        "How do I set up RCS messaging for my WhatsApp account?",
        "How do I configure API node error handling in Bot Studio?",
        "How can I use the API node to send data to an external system?",
    ]

    # Sanity-check these still hash to consulting per the deployed logic
    for q in queries:
        digest = int(hashlib.md5(q.encode()).hexdigest(), 16)
        mode = "consulting" if (digest % 100) < 50 else "standard"
        assert mode == "consulting", f"Query no longer hashes to consulting: {q}"

    results = []
    for q in queries:
        print(f"\n{'='*80}\nQuery: {q}\n{'='*80}")
        r = send_query(q)
        results.append(r)
        if r["status"] == 200:
            print(r["raw_response"][:3000])
        else:
            print(f"FAILED: {r.get('error', r.get('status'))}")

    with open(REPORT_FILE, "a") as f:
        for r in results:
            f.write(json.dumps(r, default=str) + "\n")
    print(f"\nSaved: {REPORT_FILE}")


if __name__ == "__main__":
    main()
