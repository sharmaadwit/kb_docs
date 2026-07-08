#!/usr/bin/env python3
"""
Fix polluted Langfuse traces: restore correct user_email for traces
incorrectly tagged with adwit.sharma@gupshup.io during the 2026-07-03 bug window.

Usage:
    python3 fix_polluted_traces.py

Email mapping is defined in USER_ID_TO_EMAIL below — update before running.
"""
import json, os, requests
from pathlib import Path
from requests.auth import HTTPBasicAuth

# -----------------------------------------------------------------------
# ✏️  FILL IN CORRECT EMAILS HERE before running
# -----------------------------------------------------------------------
USER_ID_TO_EMAIL = {
    30: None,           # user_name="marketing" — fill in correct email
    # 43: "adwit.sharma@gupshup.io",  # your own test — already correct, skip
}

# Traces from trace_env=LOCAL with userId=None → automated/local tests
# These will be relabelled as "local-test" rather than your email
LOCAL_PLACEHOLDER = "local-test@gupshup.io"
# -----------------------------------------------------------------------

def load_env():
    env_path = Path("/Users/adwit.sharma/kb_docs/.env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())

load_env()

host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")
pub = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
sec = os.environ.get("LANGFUSE_SECRET_KEY", "")
auth = HTTPBasicAuth(pub, sec)
headers = {"Content-Type": "application/json"}

with open("/Users/adwit.sharma/kb_docs/local/reports/polluted_traces_full.json") as f:
    polluted = json.load(f)

print(f"Loaded {len(polluted)} polluted traces\n")

fixed = 0
skipped = 0
errors = 0

for trace in polluted:
    trace_id = trace.get("id")
    meta = trace.get("metadata") or {}
    user_id = meta.get("user_id")
    trace_env = meta.get("trace_env", "")
    current_email = meta.get("user_email", "")

    # Determine correct email
    if user_id == 43:
        # Adwit's own test — correct as-is
        skipped += 1
        print(f"  SKIP  {trace_id} (userId=43, adwit's own test)")
        continue

    elif user_id is not None and user_id in USER_ID_TO_EMAIL:
        correct_email = USER_ID_TO_EMAIL[user_id]
        if correct_email is None:
            print(f"  SKIP  {trace_id} (userId={user_id} — email not set in USER_ID_TO_EMAIL, fill it in)")
            skipped += 1
            continue

    elif trace_env == "LOCAL" and user_id is None:
        correct_email = LOCAL_PLACEHOLDER

    else:
        print(f"  SKIP  {trace_id} (no mapping for userId={user_id}, trace_env={trace_env})")
        skipped += 1
        continue

    # Patch the trace via Langfuse API
    updated_meta = {**meta, "user_email": correct_email}
    payload = {
        "metadata": updated_meta,
        "userId": correct_email,
    }

    try:
        url = f"{host}/api/public/traces/{trace_id}"
        resp = requests.patch(url, auth=auth, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        print(f"  FIXED {trace_id}: {current_email} → {correct_email}")
        fixed += 1
    except Exception as e:
        print(f"  ERROR {trace_id}: {e}")
        errors += 1

print(f"\n{'='*60}")
print(f"Fixed:   {fixed}")
print(f"Skipped: {skipped}")
print(f"Errors:  {errors}")
