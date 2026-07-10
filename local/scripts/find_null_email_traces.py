#!/usr/bin/env python3
"""
Find all Langfuse KB_answer traces with null/missing user_email in metadata.

This identifies ALL traces (not time-bounded) that lack proper email attribution,
to enable comprehensive retroactive fixing across the full history.

Usage:
    python3 find_null_email_traces.py  # scan and report
"""
import json
import os
from pathlib import Path
from collections import Counter

import requests
from requests.auth import HTTPBasicAuth

def load_env():
    env_path = Path(".env")
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

load_env()
HOST = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")
AUTH = HTTPBasicAuth(os.environ["LANGFUSE_PUBLIC_KEY"], os.environ["LANGFUSE_SECRET_KEY"])

def fetch_all_traces_paginated():
    """Fetch all kb_answer traces without time bounds."""
    traces, page = [], 1
    while True:
        r = requests.get(
            f"{HOST}/api/public/traces",
            auth=AUTH,
            params={"page": page, "limit": 100},
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        batch = data.get("data", [])
        for t in batch:
            if "kb_answer" in (t.get("name") or ""):
                traces.append(t)
        total_pages = data.get("meta", {}).get("totalPages", page)
        if page >= total_pages or not batch:
            break
        page += 1
        print(f"  Fetched page {page}/{total_pages} ({len(traces)} kb_answer traces so far)")
    return traces

print("Scanning all kb_answer traces for null/missing user_email...")
all_traces = fetch_all_traces_paginated()
print(f"Total kb_answer traces: {len(all_traces)}\n")

# Categorize
null_email = []
with_email = []
for t in all_traces:
    meta = t.get("metadata") or {}
    email = (meta.get("user_email") or "").strip()
    if not email or not ("@" in email):
        null_email.append(t)
    else:
        with_email.append(t)

print(f"Traces WITH email: {len(with_email)}")
print(f"Traces WITHOUT email: {len(null_email)}")

if null_email:
    print(f"\n=== {len(null_email)} Traces with null/missing user_email ===\n")

    # Group by userId pattern
    by_userid = {}
    for t in null_email:
        uid = t.get("userId") or "NULL"
        if uid not in by_userid:
            by_userid[uid] = []
        by_userid[uid].append(t)

    for uid in sorted(by_userid.keys()):
        traces = by_userid[uid]
        print(f"{uid}: {len(traces)} traces")
        for t in traces[:3]:  # Show first 3 examples
            meta = t.get("metadata") or {}
            print(f"    {t['id']:25s} user_id={meta.get('user_id')} ts={t.get('timestamp')[:10]}")
        if len(traces) > 3:
            print(f"    ... and {len(traces)-3} more")

    # Save to file for reference
    output = {
        "total_traces": len(all_traces),
        "null_email_count": len(null_email),
        "by_userId": {uid: len(traces) for uid, traces in by_userid.items()},
        "sample_traces": [
            {
                "id": t["id"],
                "name": t.get("name"),
                "userId": t.get("userId"),
                "user_id": (t.get("metadata") or {}).get("user_id"),
                "timestamp": t.get("timestamp"),
            }
            for t in null_email[:20]
        ],
    }
    Path("local/reports/null_email_traces.json").write_text(json.dumps(output, indent=2))
    print(f"\nDetailed report saved to local/reports/null_email_traces.json")
else:
    print("✅ All traces have user_email!")
