#!/usr/bin/env python3
"""
Send a natural 3-turn conversation to the LIVE SuperAgent /api/agents/chat/stream
endpoint, reusing the same session_id across turns (the only continuity
mechanism the client-facing API exposes) WITHOUT manually injecting any
parent_trace_id. This mirrors what a real client would do.

Turns:
  1. "How do I configure Agent Assist for my bot?"
  2. "What about hallucination guardrails?"
  3. "How does that compare to Bot Studio's approach?"

Reports each turn's trace_id/correlation_id/session identifiers (as surfaced
by the response, if at all) and whether the API gives any explicit mechanism
to link turn 2/3 back to turn 1.

Run: python3 local/scripts/test_superagent_3turn_live.py
"""
import os
import sys
import json
import ssl
import uuid
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "local" / "reports"
REPORT_FILE = REPORT_DIR / "superagent_3turn_live_conversation.jsonl"


def load_env():
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split("=", 1)
                if len(parts) == 2:
                    os.environ.setdefault(parts[0], parts[1])


def send_turn(query: str, session_id: str, turn_num: int) -> dict:
    api_url = os.environ.get("SUPERAGENT_API_URL", "")
    api_key = os.environ.get("SUPERAGENT_API_KEY", "")
    org_id = os.environ.get("SUPERAGENT_ORG_ID", "")
    project_id = os.environ.get("SUPERAGENT_PROJECT_ID", "")
    user_email = os.environ.get("USER_EMAIL", "test@example.com")

    if not api_url or not api_key:
        return {"turn": turn_num, "query": query, "success": False,
                "error": "Missing SUPERAGENT_API_URL or SUPERAGENT_API_KEY in .env"}

    # NOTE: session_id is the ONLY continuity field a real client controls.
    # No parent_trace_id / thread_id is injected here.
    payload = {
        "message": query,
        "session_id": session_id,
        "user_email_id": user_email,
    }
    if org_id or project_id:
        payload["tenant_context"] = {}
        if org_id:
            payload["tenant_context"]["org_id"] = org_id
        if project_id:
            payload["tenant_context"]["project_id"] = project_id

    headers = {"Content-Type": "application/json", "X-API-Key": api_key}

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(
        api_url, data=json.dumps(payload).encode(), headers=headers, method="POST"
    )

    result = {
        "turn": turn_num,
        "query": query,
        "session_id": session_id,
        "request_payload": payload,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    try:
        with urllib.request.urlopen(req, timeout=45, context=ssl_context) as response:
            raw_headers = dict(response.headers.items())
            response_text = response.read().decode()

        result["response_headers"] = raw_headers

        answers = []
        chunks_meta = []
        raw_lines = []
        for line in response_text.strip().split("\n"):
            if line.startswith("data: "):
                raw_lines.append(line)
                try:
                    chunk = json.loads(line[6:])
                    if "content" in chunk:
                        answers.append(chunk["content"])
                    chunks_meta.append(chunk)
                except json.JSONDecodeError:
                    continue

        # Scan every chunk + response headers for anything resembling
        # trace_id / correlation_id / thread/session linkage fields.
        linkage_keys_found = {}
        for chunk in chunks_meta:
            for k, v in _flatten(chunk).items():
                lk = k.lower()
                if any(tok in lk for tok in
                       ("trace_id", "trace-id", "correlation_id", "correlation-id",
                        "session_id", "session-id", "parent", "thread_id", "conversation_id")):
                    linkage_keys_found[k] = v
        for k, v in raw_headers.items():
            lk = k.lower()
            if any(tok in lk for tok in
                   ("trace", "correlation", "session", "thread", "conversation")):
                linkage_keys_found[f"header:{k}"] = v

        result["answer"] = "".join(answers)
        result["raw_chunk_count"] = len(chunks_meta)
        result["raw_chunks_sample"] = chunks_meta[:3]
        result["linkage_fields_found"] = linkage_keys_found
        result["success"] = True

    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode()
        except Exception:
            pass
        result["success"] = False
        result["error"] = f"HTTP {e.code}: {e.reason}"
        result["error_body"] = body[:1000]
    except Exception as e:
        result["success"] = False
        result["error"] = f"{type(e).__name__}: {e}"

    return result


def _flatten(d, prefix=""):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            key = f"{prefix}.{k}" if prefix else k
            if isinstance(v, (dict, list)):
                out.update(_flatten(v, key))
            else:
                out[key] = v
    elif isinstance(d, list):
        for i, v in enumerate(d):
            key = f"{prefix}[{i}]"
            if isinstance(v, (dict, list)):
                out.update(_flatten(v, key))
            else:
                out[key] = v
    return out


def main():
    load_env()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Real-client continuity: one session_id reused across the whole conversation.
    session_id = f"kb-3turn-{uuid.uuid4().hex[:12]}"

    turns = [
        "How do I configure Agent Assist for my bot?",
        "What about hallucination guardrails?",
        "How does that compare to Bot Studio's approach?",
    ]

    print("=" * 100)
    print("SuperAgent LIVE 3-Turn Conversation Test (natural session continuity)")
    print(f"Session ID: {session_id}")
    print("=" * 100)

    results = []
    with REPORT_FILE.open("a") as f:
        for i, q in enumerate(turns, start=1):
            print(f"\n--- TURN {i}: {q} ---")
            res = send_turn(q, session_id, i)
            results.append(res)
            f.write(json.dumps(res, default=str) + "\n")

            if res.get("success"):
                print(f"  Answer preview: {res['answer'][:200]}")
                print(f"  Linkage fields found in response: {json.dumps(res['linkage_fields_found'], default=str)}")
            else:
                print(f"  FAILED: {res.get('error')}")
                if res.get("error_body"):
                    print(f"  Body: {res['error_body']}")

    print(f"\nFull results written to {REPORT_FILE}")
    return results


if __name__ == "__main__":
    main()
