#!/usr/bin/env python3
"""
One-time historical cleanup: fix Langfuse trace userIds that were overwritten
by the USER_EMAIL env override bug (traces from 2026-07-01 to 2026-07-09).

Symptom: trace.userId == env override (e.g. adwit.sharma@gupshup.io) while
trace.metadata.user_email holds the real user (e.g. harishmanek...@gmail.com).

Fix: set userId = metadata.user_email for every mismatched kb_answer trace.

Usage:
    python3 fix_userid_env_override.py --dry-run   # analyze only
    python3 fix_userid_env_override.py             # apply fixes
    python3 fix_userid_env_override.py --verify    # re-check fixed traces
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth

FROM_TS = "2026-07-01T00:00:00Z"
TO_TS   = "2026-07-10T08:00:00Z"   # fix deployed ~07-10 08:00 UTC
OUT_JSON = Path("/Users/adwit.sharma/kb_docs/local/reports/userid_fix_results.json")

ACCT_FALLBACK_RE = re.compile(r"^acct:\d+:unknown$")


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
    """Return dict of categorized trace lists."""
    cats = {
        "mismatch_fixable": [],     # userId != metadata.user_email, email present
        "acct_fallback": [],        # userId like acct:N:unknown
        "acct_fallback_fixable": [],# acct fallback AND metadata.user_email present
        "no_metadata_email": [],    # mismatch suspected but no user_email to restore
        "already_correct": [],      # userId == metadata.user_email
        "no_userid": [],            # userId missing entirely
    }
    for t in traces:
        uid = t.get("userId")
        meta = t.get("metadata") or {}
        meta_email = (meta.get("user_email") or "").strip()

        if not uid:
            cats["no_userid"].append(t)
        elif ACCT_FALLBACK_RE.match(uid):
            if meta_email and "@" in meta_email:
                cats["acct_fallback_fixable"].append(t)
            else:
                cats["acct_fallback"].append(t)
        elif meta_email and "@" in meta_email:
            if uid == meta_email:
                cats["already_correct"].append(t)
            else:
                cats["mismatch_fixable"].append(t)
        else:
            cats["no_metadata_email"].append(t)
    return cats


def patch_trace(trace_id, new_user_id, old_trace):
    """Try PATCH endpoint first; fall back to ingestion upsert."""
    # Attempt 1: PATCH /api/public/traces/{id}
    r = requests.patch(
        f"{HOST}/api/public/traces/{trace_id}",
        auth=AUTH, headers=HEADERS,
        json={"userId": new_user_id},
        timeout=15,
    )
    if r.status_code in (200, 201):
        return "patch", None
    # Attempt 2: ingestion API upsert (trace-create with same id merges fields)
    event = {
        "batch": [{
            "id": f"fix-{trace_id}-{int(time.time()*1000)}",
            "type": "trace-create",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
            "body": {
                "id": trace_id,
                "timestamp": old_trace.get("timestamp"),
                "userId": new_user_id,
            },
        }]
    }
    r2 = requests.post(f"{HOST}/api/public/ingestion", auth=AUTH, headers=HEADERS,
                       json=event, timeout=15)
    if r2.status_code in (200, 201, 207):
        body = r2.json()
        if body.get("errors"):
            return None, f"ingestion errors: {body['errors']}"
        return "ingestion", None
    return None, f"PATCH {r.status_code}: {r.text[:200]} | INGEST {r2.status_code}: {r2.text[:200]}"


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
        results = json.loads(OUT_JSON.read_text())
        ok, bad = 0, []
        for item in results.get("fixed", []):
            t = get_trace(item["trace_id"])
            if t.get("userId") == item["new_userId"]:
                ok += 1
            else:
                bad.append({"trace_id": item["trace_id"],
                            "expected": item["new_userId"],
                            "actual": t.get("userId")})
            time.sleep(0.1)
        print(f"Verified OK: {ok}/{len(results.get('fixed', []))}")
        if bad:
            print("MISMATCHES AFTER FIX:")
            for b in bad:
                print(f"  {b['trace_id']}: expected={b['expected']} actual={b['actual']}")
        results["verification"] = {"ok": ok, "bad": bad}
        OUT_JSON.write_text(json.dumps(results, indent=2))
        return

    print(f"Fetching traces {FROM_TS} .. {TO_TS} ...")
    all_traces = fetch_all_traces()
    kb_traces = [t for t in all_traces if is_kb_answer(t)]
    print(f"Total traces: {len(all_traces)}, kb_answer traces: {len(kb_traces)}")

    cats = classify(kb_traces)
    for k, v in cats.items():
        print(f"  {k}: {len(v)}")

    # Which env-override emails appear as wrong userIds?
    from collections import Counter
    wrong_uid_counts = Counter(t["userId"] for t in cats["mismatch_fixable"])
    print("\nMismatched userId values (env overrides):")
    for uid, n in wrong_uid_counts.most_common():
        print(f"  {uid}: {n}")

    to_fix = cats["mismatch_fixable"] + cats["acct_fallback_fixable"]
    print(f"\nTraces to fix: {len(to_fix)}")
    for t in to_fix:
        meta_email = (t.get("metadata") or {}).get("user_email")
        print(f"  {t['id']}  {t.get('name','')[:48]:48s} {t.get('userId')} -> {meta_email}")

    results = {
        "range": [FROM_TS, TO_TS],
        "counts": {k: len(v) for k, v in cats.items()},
        "wrong_userid_values": dict(wrong_uid_counts),
        "fixed": [], "failed": [],
        "already_correct": [t["id"] for t in cats["already_correct"]],
        "unfixable_no_email": [
            {"trace_id": t["id"], "userId": t.get("userId"), "name": t.get("name")}
            for t in cats["acct_fallback"] + cats["no_metadata_email"]
            if t.get("userId")  # only flag ones with a userId set
        ],
    }

    if args.dry_run:
        print("\nDRY RUN — no changes made.")
        OUT_JSON.write_text(json.dumps(results, indent=2))
        return

    print("\nApplying fixes...")
    for t in to_fix:
        tid = t["id"]
        new_uid = (t.get("metadata") or {}).get("user_email").strip()
        method, err = patch_trace(tid, new_uid, t)
        if method:
            results["fixed"].append({
                "trace_id": tid, "name": t.get("name"),
                "old_userId": t.get("userId"), "new_userId": new_uid,
                "method": method,
            })
            print(f"  FIXED ({method}) {tid}: {t.get('userId')} -> {new_uid}")
        else:
            results["failed"].append({"trace_id": tid, "old_userId": t.get("userId"),
                                      "new_userId": new_uid, "error": err})
            print(f"  FAILED {tid}: {err}")
        time.sleep(0.15)

    OUT_JSON.write_text(json.dumps(results, indent=2))
    print(f"\nFixed: {len(results['fixed'])}  Failed: {len(results['failed'])}")
    print(f"Results written to {OUT_JSON}")


if __name__ == "__main__":
    main()
