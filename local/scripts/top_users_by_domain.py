#!/usr/bin/env python3
"""One-off: top 50 gupshup.io and knowlarity.com users of the skill, all-time."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(__file__))
from collections import Counter
from datetime import datetime, timedelta

DOMAINS = ("gupshup.io", "knowlarity.com")


def fetch_all_traces(days=365, page_timeout=90, max_retries=4):
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

    def _trace_to_shape(trace):
        inp = trace.get("input") or {}
        meta = (inp.get("_meta") if isinstance(inp, dict) else None) or trace.get("metadata") or {}
        return {
            "id": trace.get("id"),
            "timestamp": trace.get("timestamp"),
            "name": trace.get("name"),
            "userId": trace.get("userId"),
            "metadata": meta,
            "input": inp,
            "output": trace.get("output"),
        }

    all_traces = []
    page = 1
    while True:
        p: dict = {"name": "kb_answer", "limit": 100, "fromTimestamp": from_date}
        p["page"] = page
        params = urllib.parse.urlencode(p)
        url = f"{host}/api/public/traces?{params}"
        req = urllib.request.Request(url, headers=headers)
        body = None
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req, timeout=page_timeout, context=ssl_ctx) as resp:
                    body = json.loads(resp.read())
                break
            except Exception as e:
                print(f"  page={page} attempt {attempt+1} failed: {e}")
                time.sleep(3)
        if body is None:
            print(f"  giving up after {max_retries} attempts")
            break
        batch = body.get("data", [])
        all_traces.extend(_trace_to_shape(t) for t in batch)
        print(f"  fetched page {page}: {len(batch)} traces (total so far: {len(all_traces)})")
        if len(batch) < 100:
            break
        page += 1
    return all_traces


traces = fetch_all_traces(days=365)
if not traces:
    print("No traces fetched")
    sys.exit(1)

print(f"\n✅ Total traces fetched: {len(traces)}")

counters = {d: Counter() for d in DOMAINS}
for t in traces:
    meta = (t.get("metadata") or {})
    email = (meta.get("user_email") or "").strip().lower()
    if not email or "@" not in email:
        continue
    domain = email.split("@", 1)[1]
    for d in DOMAINS:
        if domain == d:
            counters[d][email] += 1

for d in DOMAINS:
    print(f"\n=== Top 50 {d} users (all-time, {sum(counters[d].values())} total queries, {len(counters[d])} unique users) ===")
    for i, (email, count) in enumerate(counters[d].most_common(50), 1):
        print(f"{i:>3}. {email:<45} {count}")
