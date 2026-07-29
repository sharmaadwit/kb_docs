#!/usr/bin/env python3
"""Retro-backfill: for historical traces with null metadata.user_email but a
populated user_id, mirror the same acct:{uid}:{name} identity that
_langfuse_user_context() now synthesizes going forward (skill/kb_answer.py).

Re-sends a trace-create ingestion event with the SAME trace id (Langfuse
upserts on id) carrying the full original body plus the patched
metadata.user_email / metadata.identity_source / userId fields, so no other
trace data is touched or lost.

Usage:
    python3 local/scripts/backfill_anonymous_identity.py --days 365 --dry-run
    python3 local/scripts/backfill_anonymous_identity.py --days 365 --apply
"""
import sys, os, json, time, argparse
sys.path.insert(0, os.path.dirname(__file__))
from datetime import datetime, timedelta


def fetch_all_traces(days, page_timeout=90, max_retries=4):
    from generate_analytics_dashboard import _load_env
    import urllib.request, urllib.parse, base64, ssl
    _load_env()
    host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")
    pub = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
    sec = os.environ.get("LANGFUSE_SECRET_KEY", "")
    try:
        import certifi
        ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

    creds = base64.b64encode(f"{pub}:{sec}".encode()).decode()
    headers = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
    from_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")

    all_traces = []
    page = 1
    while True:
        params = urllib.parse.urlencode({"page": page, "limit": 100, "fromTimestamp": from_date})
        url = f"{host}/api/public/traces?{params}"
        req = urllib.request.Request(url, headers=headers)
        body = None
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req, timeout=page_timeout, context=ssl_ctx) as resp:
                    body = json.loads(resp.read())
                break
            except Exception as e:
                print(f"  page {page} attempt {attempt+1} failed: {e}")
                time.sleep(3)
        if body is None:
            print(f"  giving up on page {page} after {max_retries} attempts")
            break
        batch = body.get("data", [])
        all_traces.extend(batch)
        meta = body.get("meta", {})
        total = meta.get("totalItems", meta.get("total", len(all_traces)))
        print(f"  fetched page {page}: {len(batch)} traces ({len(all_traces)}/{total})")
        if not batch or len(all_traces) >= total:
            break
        page += 1
    return all_traces, host, pub, sec


def build_patch_event(trace, host):
    import uuid
    meta = dict(trace.get("metadata") or {})
    user_id = meta.get("user_id")
    if user_id is None or meta.get("user_email"):
        return None  # nothing to backfill
    name = (meta.get("user_name") or "unknown")
    acct_identity = f"acct:{str(user_id).strip()}:{str(name).strip() or 'unknown'}"
    meta["user_email"] = acct_identity
    meta["identity_source"] = "account_id_backfill"

    event_id = f"evt-{uuid.uuid4().hex[:24]}"
    now_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    body = {
        "id": trace["id"],
        "timestamp": trace.get("timestamp") or now_iso,
        "name": trace.get("name"),
        "input": trace.get("input"),
        "output": trace.get("output"),
        "metadata": meta,
        "userId": acct_identity,
    }
    return {
        "batch": [{"id": event_id, "timestamp": now_iso, "type": "trace-create", "body": body}]
    }, acct_identity


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=365)
    ap.add_argument("--env-filter", default="PROD_EXT")
    ap.add_argument("--apply", action="store_true", help="actually send patch events")
    ap.add_argument("--dry-run", action="store_true", help="report only (default)")
    args = ap.parse_args()

    traces, host, pub, sec = fetch_all_traces(days=args.days)
    print(f"\n✅ Fetched {len(traces)} traces total")

    candidates = []
    for t in traces:
        meta = t.get("metadata") or {}
        if args.env_filter and meta.get("trace_env") != args.env_filter:
            continue
        if meta.get("user_email"):
            continue
        if meta.get("user_id") is None:
            continue
        candidates.append(t)

    print(f"Candidates for backfill (trace_env={args.env_filter}, null user_email, has user_id): {len(candidates)}")

    if not candidates:
        print("Nothing to backfill.")
        return

    if not args.apply:
        print("\n--dry-run (default): no writes performed. Sample:")
        for t in candidates[:10]:
            meta = t.get("metadata") or {}
            print(f"  trace_id={t['id']}  user_id={meta.get('user_id')}  ts={t.get('timestamp')}")
        print(f"\nRe-run with --apply to patch all {len(candidates)} traces.")
        return

    import urllib.request, base64, ssl
    try:
        import certifi
        ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    except Exception:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
    creds = base64.b64encode(f"{pub}:{sec}".encode()).decode()
    headers = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
    endpoint = f"{host}/api/public/ingestion"

    ok, failed = 0, 0
    for t in candidates:
        result = build_patch_event(t, host)
        if result is None:
            continue
        event, identity = result
        req = urllib.request.Request(endpoint, data=json.dumps(event).encode(), headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
                if resp.status < 400:
                    ok += 1
                else:
                    failed += 1
                    print(f"  FAILED trace_id={t['id']} status={resp.status}")
        except Exception as e:
            failed += 1
            print(f"  FAILED trace_id={t['id']} error={e}")
        time.sleep(0.05)

    print(f"\nBackfill complete: {ok} patched, {failed} failed, {len(candidates)} candidates")


if __name__ == "__main__":
    main()
