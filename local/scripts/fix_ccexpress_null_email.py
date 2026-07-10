#!/usr/bin/env python3
"""
Retroactive fix: Langfuse traces with user_id=2 (CC Express visitor) but null/missing user_email.

Symptom: trace.userId == 'acct:2:unknown' (fallback) while trace.user_id == 2
but metadata.user_email is null or missing.

Fix: Set userId + metadata.user_email to the CC Express visitor email:
  visitor-8cbe2c97-d8dd-4d5f-a9aa-ea01f087314e@ccexpress.gupshup.io

This retroactively fixes traces created before the UID-to-email mapping was
added to _langfuse_user_context() (commit 1e396c29).

Usage:
    python3 fix_ccexpress_null_email.py --dry-run   # analyze only
    python3 fix_ccexpress_null_email.py             # apply fixes
    python3 fix_ccexpress_null_email.py --verify    # re-check fixed traces
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth

FROM_TS = "2026-07-01T00:00:00Z"
TO_TS = "2026-07-10T08:00:00Z"  # before UID mapping deployed
OUT_JSON = Path("/Users/adwit.sharma/kb_docs/local/reports/ccexpress_fix_results.json")

# CC Express visitor mapping
CCEXPRESS_VISITOR_EMAIL = "visitor-8cbe2c97-d8dd-4d5f-a9aa-ea01f087314e@ccexpress.gupshup.io"


def load_env():
    env_path = Path("/Users/adwit.sharma/kb_docs/.env")
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
HEADERS = {"Content-Type": "application/json"}


def fetch_all_traces():
    traces, page = [], 1
    while True:
        r = requests.get(
            f"{HOST}/api/public/traces",
            auth=AUTH,
            params={
                "page": page,
                "limit": 100,
                "fromTimestamp": FROM_TS,
                "toTimestamp": TO_TS,
            },
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        batch = data.get("data", [])
        traces.extend(batch)
        total_pages = data.get("meta", {}).get("totalPages", page)
        if page >= total_pages or not batch:
            break
        page += 1
    return traces


def is_kb_answer(trace):
    name = trace.get("name") or ""
    return "kb_answer" in name


def classify(traces):
    """Identify CC Express visitor traces with null/missing email."""
    cats = {
        "ccexpress_null_email": [],  # userId=acct:2:unknown, no metadata.user_email
        "ccexpress_with_email": [],  # userId=acct:2:unknown, metadata.user_email present
        "other": [],
    }
    for t in traces:
        uid = t.get("userId") or ""
        meta = t.get("metadata") or {}
        user_id = meta.get("user_id")
        meta_email = (meta.get("user_email") or "").strip()

        # Check if this is a CC Express visitor trace
        if uid == "acct:2:unknown" or (user_id == 2 and uid and uid.startswith("acct:")):
            if not meta_email or not ("@" in meta_email):
                cats["ccexpress_null_email"].append(t)
            else:
                cats["ccexpress_with_email"].append(t)
        else:
            cats["other"].append(t)

    return cats


def patch_trace(trace_id, new_user_id, new_email, old_trace):
    """Apply fix via ingestion API upsert."""
    event = {
        "batch": [{
            "id": f"fix-ccexpress-{trace_id[-8:]}-{int(time.time()*1000)}",
            "type": "trace-create",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
            "body": {
                "id": trace_id,
                "timestamp": old_trace.get("timestamp"),
                "userId": new_user_id,
                "metadata": {
                    **old_trace.get("metadata", {}),
                    "user_email": new_email,
                }
            },
        }]
    }
    r = requests.post(
        f"{HOST}/api/public/ingestion",
        auth=AUTH,
        headers=HEADERS,
        json=event,
        timeout=15,
    )
    if r.status_code in (200, 201, 207):
        body = r.json()
        if body.get("errors"):
            return None, f"ingestion errors: {body['errors']}"
        return "ingestion", None
    return None, f"HTTP {r.status_code}: {r.text[:200]}"


def get_trace(trace_id):
    r = requests.get(f"{HOST}/api/public/traces/{trace_id}", auth=AUTH, timeout=15)
    r.raise_for_status()
    return r.json()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    if args.verify:
        if not OUT_JSON.exists():
            print(f"No results file found: {OUT_JSON}")
            return
        results = json.loads(OUT_JSON.read_text())
        ok, bad = 0, []
        for item in results.get("fixed", []):
            t = get_trace(item["trace_id"])
            meta_email = (t.get("metadata") or {}).get("user_email", "").strip()
            if t.get("userId") == CCEXPRESS_VISITOR_EMAIL and meta_email == CCEXPRESS_VISITOR_EMAIL:
                ok += 1
            else:
                bad.append({
                    "trace_id": item["trace_id"],
                    "expected_userId": CCEXPRESS_VISITOR_EMAIL,
                    "actual_userId": t.get("userId"),
                    "actual_email": meta_email,
                })
            time.sleep(0.1)
        print(f"Verified OK: {ok}/{len(results.get('fixed', []))}")
        if bad:
            print("MISMATCHES AFTER FIX:")
            for b in bad:
                print(f"  {b['trace_id']}: userId={b['actual_userId']} email={b['actual_email']}")
        results["verification"] = {"ok": ok, "mismatches": bad}
        OUT_JSON.write_text(json.dumps(results, indent=2))
        return

    print(f"Fetching traces {FROM_TS} .. {TO_TS} ...")
    all_traces = fetch_all_traces()
    kb_traces = [t for t in all_traces if is_kb_answer(t)]
    print(f"Total traces: {len(all_traces)}, kb_answer traces: {len(kb_traces)}")

    cats = classify(kb_traces)
    for k, v in cats.items():
        print(f"  {k}: {len(v)}")

    to_fix = cats["ccexpress_null_email"]
    print(f"\nCC Express visitor traces with null/missing email: {len(to_fix)}")
    for t in to_fix:
        meta = t.get("metadata") or {}
        print(
            f"  {t['id']:20s} userId={t.get('userId'):30s} "
            f"user_id={meta.get('user_id'):4} user_email={meta.get('user_email')}"
        )

    results = {
        "range": [FROM_TS, TO_TS],
        "target_email": CCEXPRESS_VISITOR_EMAIL,
        "counts": {k: len(v) for k, v in cats.items()},
        "fixed": [],
        "failed": [],
        "already_complete": [t["id"] for t in cats["ccexpress_with_email"]],
    }

    if args.dry_run:
        print("\nDRY RUN — no changes made.")
        OUT_JSON.write_text(json.dumps(results, indent=2))
        return

    if not to_fix:
        print("\nNo traces to fix.")
        OUT_JSON.write_text(json.dumps(results, indent=2))
        return

    print("\nApplying fixes...")
    for t in to_fix:
        tid = t["id"]
        method, err = patch_trace(tid, CCEXPRESS_VISITOR_EMAIL, CCEXPRESS_VISITOR_EMAIL, t)
        if method:
            results["fixed"].append({
                "trace_id": tid,
                "name": t.get("name"),
                "old_userId": t.get("userId"),
                "new_userId": CCEXPRESS_VISITOR_EMAIL,
                "method": method,
            })
            print(f"  FIXED ({method}) {tid}")
        else:
            results["failed"].append({
                "trace_id": tid,
                "old_userId": t.get("userId"),
                "error": err,
            })
            print(f"  FAILED {tid}: {err}")
        time.sleep(0.15)

    OUT_JSON.write_text(json.dumps(results, indent=2))
    print(f"\nFixed: {len(results['fixed'])}  Failed: {len(results['failed'])}")
    print(f"Results written to {OUT_JSON}")


if __name__ == "__main__":
    main()
