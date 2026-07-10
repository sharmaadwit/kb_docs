#!/usr/bin/env python3
"""
Find and fix production traces (trace_env=PROD) from last 15 days with null/missing user_email.

For traces with trace_env="PROD" and null/missing user_email in metadata,
attribute the CC Express visitor email to ensure all production traces are properly attributed.

Usage:
    python3 fix_prod_null_email.py --dry-run   # analyze only
    python3 fix_prod_null_email.py             # apply fixes
    python3 fix_prod_null_email.py --verify    # re-check fixed traces
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth

# CC Express visitor mapping
CCEXPRESS_VISITOR_EMAIL = "visitor-8cbe2c97-d8dd-4d5f-a9aa-ea01f087314e@ccexpress.gupshup.io"

# Last 15 days
TO_TS = datetime.utcnow().isoformat() + "Z"
FROM_TS = (datetime.utcnow() - timedelta(days=15)).isoformat() + "Z"
OUT_JSON = Path("/Users/adwit.sharma/kb_docs/local/reports/prod_null_email_fix_results.json")


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


def fetch_all_traces(trace_env=None):
    """Fetch kb_answer traces from last 15 days, optionally filtered by trace_env."""
    traces, page = [], 1
    while True:
        try:
            params = {
                "page": page,
                "limit": 100,
                "fromTimestamp": FROM_TS,
                "toTimestamp": TO_TS,
            }
            r = requests.get(
                f"{HOST}/api/public/traces",
                auth=AUTH,
                params=params,
                timeout=60,
            )
            r.raise_for_status()
            data = r.json()
            batch = data.get("data", [])

            for t in batch:
                if "kb_answer" not in (t.get("name") or ""):
                    continue
                # Filter by trace_env if specified
                if trace_env:
                    meta = t.get("metadata") or {}
                    if meta.get("trace_env") != trace_env:
                        continue
                traces.append(t)

            total_pages = data.get("meta", {}).get("totalPages", page)
            if page >= total_pages or not batch:
                break
            page += 1
            print(f"  Fetched page {page}/{total_pages} ({len(traces)} matching traces)")
            time.sleep(0.5)  # Rate limit

        except requests.exceptions.Timeout:
            print(f"  Page {page}: Timeout, skipping")
            continue
        except Exception as e:
            print(f"  Page {page}: Error - {e}")
            break

    return traces


def classify(traces):
    """Identify traces with null/missing user_email."""
    cats = {
        "null_email": [],           # trace_env=PROD, no user_email
        "has_email": [],            # trace_env=PROD, has user_email
    }
    for t in traces:
        meta = t.get("metadata") or {}
        email = (meta.get("user_email") or "").strip()

        if not email or not ("@" in email):
            cats["null_email"].append(t)
        else:
            cats["has_email"].append(t)

    return cats


def patch_trace(trace_id, new_email, old_trace):
    """Apply fix via ingestion API upsert."""
    event = {
        "batch": [{
            "id": f"fix-prod-{trace_id[-8:]}-{int(time.time()*1000)}",
            "type": "trace-create",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
            "body": {
                "id": trace_id,
                "timestamp": old_trace.get("timestamp"),
                "userId": new_email,
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
            meta_email = (t.get("metadata") or {}).get("user_email") or ""
            meta_email = meta_email.strip() if isinstance(meta_email, str) else ""
            if t.get("userId") == CCEXPRESS_VISITOR_EMAIL and meta_email == CCEXPRESS_VISITOR_EMAIL:
                ok += 1
            else:
                bad.append({
                    "trace_id": item["trace_id"],
                    "expected_email": CCEXPRESS_VISITOR_EMAIL,
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

    print(f"Fetching PROD traces from {FROM_TS[:10]} to {TO_TS[:10]}...")
    prod_traces = fetch_all_traces(trace_env="PROD")
    print(f"Total PROD kb_answer traces: {len(prod_traces)}")

    cats = classify(prod_traces)
    print(f"\n  With email: {len(cats['has_email'])}")
    print(f"  Null/missing email: {len(cats['null_email'])}")

    to_fix = cats["null_email"]
    if to_fix:
        print(f"\nProduction traces with null user_email ({len(to_fix)}):")
        for t in to_fix[:10]:  # Show first 10
            meta = t.get("metadata") or {}
            print(
                f"  {t['id']:25s} userId={str(t.get('userId'))[:40]:40s} "
                f"user_id={str(meta.get('user_id')):5s} ts={t.get('timestamp')[:10]}"
            )
        if len(to_fix) > 10:
            print(f"  ... and {len(to_fix)-10} more")

    results = {
        "time_range": [FROM_TS[:10], TO_TS[:10]],
        "target_email": CCEXPRESS_VISITOR_EMAIL,
        "counts": {k: len(v) for k, v in cats.items()},
        "fixed": [],
        "failed": [],
    }

    if args.dry_run:
        print(f"\nDRY RUN — no changes made.")
        OUT_JSON.write_text(json.dumps(results, indent=2))
        return

    if not to_fix:
        print("\nNo traces to fix.")
        OUT_JSON.write_text(json.dumps(results, indent=2))
        return

    print("\nApplying fixes...")
    for i, t in enumerate(to_fix, 1):
        tid = t["id"]
        method, err = patch_trace(tid, CCEXPRESS_VISITOR_EMAIL, t)
        if method:
            results["fixed"].append({
                "trace_id": tid,
                "name": t.get("name"),
                "old_userId": t.get("userId"),
                "new_email": CCEXPRESS_VISITOR_EMAIL,
                "method": method,
            })
            print(f"  [{i}/{len(to_fix)}] FIXED ({method}) {tid}")
        else:
            results["failed"].append({
                "trace_id": tid,
                "old_userId": t.get("userId"),
                "error": err,
            })
            print(f"  [{i}/{len(to_fix)}] FAILED {tid}: {err}")
        time.sleep(0.15)

    OUT_JSON.write_text(json.dumps(results, indent=2))
    print(f"\nFixed: {len(results['fixed'])}  Failed: {len(results['failed'])}")
    print(f"Results written to {OUT_JSON}")


if __name__ == "__main__":
    main()
