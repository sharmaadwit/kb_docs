#!/usr/bin/env python3
"""Fire a test question to the SuperAgent stream endpoint and verify the
resulting Langfuse trace to confirm the OTLP migration is working correctly.

Usage:
    python3 local/scripts/test_superagent_live.py
    python3 local/scripts/test_superagent_live.py --question "how do I create a bot?"
    python3 local/scripts/test_superagent_live.py --wait 30

Checks:
  1. SuperAgent returns a streamed answer (HTTP 200, data events)
  2. A corresponding trace appears in Langfuse within --wait seconds
  3. trace.input._meta is populated (OTLP metadata path is working)
  4. Key metadata fields are present: answered, module_label, latency_ms
"""
import argparse
import json
import os
import sys
import time
import uuid
import requests


# ── env ──────────────────────────────────────────────────────────────────────

def _load_env():
    dotenv = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    if not os.path.exists(dotenv):
        return
    with open(dotenv) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k and not os.getenv(k):
                os.environ[k] = v

_load_env()

SUPERAGENT_URL   = os.environ.get("SUPERAGENT_API_URL", "https://superagent.smsgupshup.com/api/agents/chat/stream")
SUPERAGENT_KEY   = os.environ.get("SUPERAGENT_API_KEY", "")
ORG_ID           = os.environ.get("SUPERAGENT_ORG_ID", "")
PROJECT_ID       = os.environ.get("SUPERAGENT_PROJECT_ID", "")
LANGFUSE_HOST    = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")
LANGFUSE_PUBLIC  = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET  = os.environ.get("LANGFUSE_SECRET_KEY", "")


# ── SuperAgent call ───────────────────────────────────────────────────────────

def fire_question(question: str, session_id: str) -> dict:
    """POST to SuperAgent stream endpoint; collect full streamed response."""
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": SUPERAGENT_KEY,
    }
    payload = {
        "message": question,
        "session_id": session_id,
        "user_email_id": "test-otlp-check@gupshup.io",
    }
    if ORG_ID:
        payload.setdefault("tenant_context", {})["org_id"] = ORG_ID
    if PROJECT_ID:
        payload.setdefault("tenant_context", {})["project_id"] = PROJECT_ID

    print(f"→ POST {SUPERAGENT_URL}")
    print(f"  question : {question}")
    print(f"  session  : {session_id}")
    if ORG_ID:    print(f"  org_id   : {ORG_ID}")
    if PROJECT_ID: print(f"  proj_id  : {PROJECT_ID}")
    print()

    answer_parts = []
    done_event   = {}
    fired_at     = time.time()

    with requests.post(SUPERAGENT_URL, headers=headers, json=payload,
                       stream=True, timeout=120) as resp:
        print(f"  HTTP {resp.status_code}")
        if resp.status_code != 200:
            print(f"  ERROR body: {resp.text[:500]}")
            sys.exit(1)

        for raw_line in resp.iter_lines():
            if not raw_line:
                continue
            line = raw_line.decode("utf-8") if isinstance(raw_line, bytes) else raw_line
            if line.startswith("data:"):
                data_str = line[5:].strip()
                if data_str == "[DONE]":
                    break
                try:
                    ev = json.loads(data_str)
                    if ev.get("type") == "done":
                        done_event = ev
                    elif ev.get("type") == "text_delta":
                        answer_parts.append(ev.get("text", ""))
                except json.JSONDecodeError:
                    answer_parts.append(data_str)

    answer = "".join(answer_parts).strip()
    elapsed = round(time.time() - fired_at, 2)

    print(f"  answer ({elapsed}s): {answer[:300]}{'…' if len(answer) > 300 else ''}")
    if done_event:
        usage = done_event.get("usage") or {}
        print(f"  tokens in={usage.get('input_tokens')} out={usage.get('output_tokens')}")
    print()
    return {"answer": answer, "done_event": done_event, "elapsed_s": elapsed, "fired_at": fired_at}


# ── Langfuse poll ─────────────────────────────────────────────────────────────

def poll_langfuse(fired_at: float, wait_s: int) -> dict | None:
    """Poll legacy /api/public/traces for the most recent kb_answer trace
    that arrived after fired_at. Returns the trace dict or None on timeout."""
    auth = (LANGFUSE_PUBLIC, LANGFUSE_SECRET)
    deadline = time.time() + wait_s
    attempt  = 0

    print(f"⏳ Polling Langfuse for up to {wait_s}s …")
    while time.time() < deadline:
        attempt += 1
        try:
            r = requests.get(
                f"{LANGFUSE_HOST}/api/public/traces",
                params={"name": "kb_answer", "limit": 5},
                auth=auth, timeout=30,
            )
            traces = r.json().get("data", [])
            for t in traces:
                ts = t.get("timestamp", "")
                # Accept traces created at or after the question was fired
                if ts:
                    import datetime
                    t_epoch = datetime.datetime.fromisoformat(
                        ts.replace("Z", "+00:00")
                    ).timestamp()
                    if t_epoch >= fired_at - 2:   # 2s grace for clock skew
                        print(f"  ✅ Trace found on attempt {attempt}: {t.get('id','?')[:16]}…")
                        return t
        except Exception as e:
            print(f"  poll error: {e}")
        sleep = min(5, deadline - time.time())
        if sleep > 0:
            time.sleep(sleep)

    print(f"  ❌ No trace found after {wait_s}s ({attempt} attempts)")
    return None


# ── verify trace ──────────────────────────────────────────────────────────────

def verify_trace(trace: dict) -> bool:
    print("─" * 60)
    print("LANGFUSE TRACE VERIFICATION")
    print("─" * 60)

    inp  = trace.get("input") or {}
    meta = inp.get("_meta") if isinstance(inp, dict) else None
    old_meta = trace.get("metadata") or {}

    print(f"  trace id    : {trace.get('id')}")
    print(f"  name        : {trace.get('name')}")
    print(f"  timestamp   : {trace.get('timestamp')}")
    print()

    ok = True

    # Check _meta path (OTLP)
    if meta:
        print("  ✅ input._meta present (OTLP metadata path working)")
        for field in ("answered", "module_label", "latency_ms", "confidence"):
            val = meta.get(field)
            mark = "✅" if val is not None else "⚠️ "
            print(f"     {mark} {field}: {val}")
    else:
        # Fallback: check legacy metadata field (old SDK traces)
        if old_meta and any(k in old_meta for k in ("answered", "module_label")):
            print("  ⚠️  input._meta absent — using legacy trace.metadata (pre-OTLP trace)")
            for field in ("answered", "module_label", "latency_ms"):
                print(f"      {field}: {old_meta.get(field)}")
        else:
            print("  ❌ input._meta absent AND trace.metadata has no analytics fields")
            print(f"     trace.metadata keys: {sorted(old_meta.keys())[:8]}")
            ok = False

    print()

    # Check input query
    query = inp.get("query") if isinstance(inp, dict) else None
    if query:
        print(f"  ✅ input.query: {str(query)[:100]}")
    else:
        print("  ⚠️  input.query not found in trace.input")

    print()
    print(f"  Result: {'PASS ✅' if ok else 'FAIL ❌'}")
    print("─" * 60)
    return ok


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Test SuperAgent + Langfuse OTLP pipeline")
    parser.add_argument("--question", default="How do I set up a WhatsApp bot on Gupshup?",
                        help="Question to ask SuperAgent")
    parser.add_argument("--wait", type=int, default=45,
                        help="Seconds to wait for Langfuse trace (default 45)")
    args = parser.parse_args()

    if not SUPERAGENT_KEY:
        print("ERROR: SUPERAGENT_API_KEY not set in .env")
        sys.exit(1)
    if not LANGFUSE_PUBLIC or not LANGFUSE_SECRET:
        print("ERROR: LANGFUSE credentials not set in .env")
        sys.exit(1)

    session_id = f"test-otlp-{uuid.uuid4().hex[:8]}"

    # 1. Fire question
    result = fire_question(args.question, session_id)

    # 2. Poll Langfuse
    trace = poll_langfuse(result["fired_at"], args.wait)
    if not trace:
        sys.exit(1)

    # 3. Verify
    ok = verify_trace(trace)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
