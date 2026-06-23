#!/usr/bin/env python3
"""
Test script for correlation_id implementation in kb_answer.
Verifies that both traces share the same correlation_id and that the
second trace correctly links its parentTraceId to the first trace's ID.

Usage: python local/scripts/test_correlation_id.py
"""

import json
import os
import sys
import uuid
import base64
import time
from datetime import datetime, timezone

# ── Path setup ──────────────────────────────────────────────────────────────
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOG_PATH = os.path.join(REPO_ROOT, ".logs", "agents.log")
SKILL_DIR = os.path.join(REPO_ROOT, "skill")
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

# ── Logging helper ───────────────────────────────────────────────────────────
def log(msg: str):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] [AGENT-4] {msg}"
    print(line, flush=True)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")


# ── Step 1: Load .env ────────────────────────────────────────────────────────
log("test: Step 1/7 - Loading .env credentials")
env_path = os.path.join(REPO_ROOT, ".env")
env_vars = {}
try:
    with open(env_path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, _, v = line.partition("=")
                env_vars[k.strip()] = v.strip()
    os.environ.update(env_vars)
    log(f"test: Step 1/7 - Loaded {len(env_vars)} env vars from .env")
except Exception as e:
    log(f"test: Step 1/7 - ERROR loading .env: {e}")
    sys.exit(1)

LANGFUSE_HOST = env_vars.get("LANGFUSE_HOST", "")
LANGFUSE_PUBLIC_KEY = env_vars.get("LANGFUSE_PUBLIC_KEY", "")
LANGFUSE_SECRET_KEY = env_vars.get("LANGFUSE_SECRET_KEY", "")

if not (LANGFUSE_HOST and LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY):
    log("test: Step 1/7 - ERROR: Missing Langfuse credentials in .env")
    sys.exit(1)


# ── Step 2: Import kb_answer ─────────────────────────────────────────────────
log("test: Step 2/7 - Importing kb_answer from skill/kb_answer.py")
try:
    from kb_answer import kb_answer
    log("test: Step 2/7 - kb_answer imported successfully")
except Exception as e:
    log(f"test: Step 2/7 - ERROR importing kb_answer: {e}")
    sys.exit(1)


# ── Minimal context stub ─────────────────────────────────────────────────────
class _Context:
    """Minimal context object that satisfies kb_answer's context.get_secret() calls."""
    def __init__(self, secrets: dict):
        self._secrets = secrets

    def get_secret(self, key: str):
        return self._secrets.get(key) or os.environ.get(key)


context = _Context({
    "LANGFUSE_HOST": LANGFUSE_HOST,
    "LANGFUSE_PUBLIC_KEY": LANGFUSE_PUBLIC_KEY,
    "LANGFUSE_SECRET_KEY": LANGFUSE_SECRET_KEY,
})


# ── Step 3: Generate correlation_id ─────────────────────────────────────────
log("test: Step 3/7 - Generating correlation_id")
correlation_id = uuid.uuid4().hex[:12]
log(f"test: Step 3/7 - correlation_id = {correlation_id}")


# ── Step 4: First kb_answer call ─────────────────────────────────────────────
log("test: Step 4/7 - Calling kb_answer (query 1: 'How do I set up WhatsApp?')")
try:
    result1 = kb_answer(
        parameters={"query": "How do I set up WhatsApp?"},
        context=context,
        correlation_id=correlation_id,
        parent_trace_id=None,
    )
    lf1 = result1.get("langfuse", {})
    trace_id_1 = lf1.get("trace_id")
    lf1_ok = lf1.get("ok", False)
    lf1_ingested = lf1.get("ingestion_live", False)
    meta1 = lf1.get("metadata", {})
    log(f"test: Step 4/7 - trace_id_1 = {trace_id_1}")
    log(f"test: Step 4/7 - ingestion_live = {lf1_ingested} | status_code = {lf1.get('status_code')}")
    log(f"test: Step 4/7 - answer preview: {result1.get('answer', '')[:80]!r}")
except Exception as e:
    log(f"test: Step 4/7 - ERROR in first call: {e}")
    import traceback; traceback.print_exc()
    sys.exit(1)


# Brief pause so Langfuse has a moment to ingest before the second call
time.sleep(1)


# ── Step 5: Second kb_answer call (follow-up, hierarchical) ─────────────────
log("test: Step 5/7 - Calling kb_answer (query 2: 'What about automation?', parent_trace_id=trace_id_1)")
try:
    result2 = kb_answer(
        parameters={"query": "What about automation?"},
        context=context,
        correlation_id=correlation_id,
        parent_trace_id=trace_id_1,
    )
    lf2 = result2.get("langfuse", {})
    trace_id_2 = lf2.get("trace_id")
    lf2_ok = lf2.get("ok", False)
    lf2_ingested = lf2.get("ingestion_live", False)
    meta2 = lf2.get("metadata", {})
    log(f"test: Step 5/7 - trace_id_2 = {trace_id_2}")
    log(f"test: Step 5/7 - ingestion_live = {lf2_ingested} | status_code = {lf2.get('status_code')}")
    log(f"test: Step 5/7 - answer preview: {result2.get('answer', '')[:80]!r}")
except Exception as e:
    log(f"test: Step 5/7 - ERROR in second call: {e}")
    import traceback; traceback.print_exc()
    sys.exit(1)


# ── Step 6: Fetch recent traces from Langfuse API ────────────────────────────
log("test: Step 6/7 - Fetching recent traces from Langfuse API")
import requests

auth_raw = f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}"
auth_value = "Basic " + base64.b64encode(auth_raw.encode()).decode()
headers = {"Authorization": auth_value, "Content-Type": "application/json"}

# Wait a bit for ingestion to settle
time.sleep(3)

fetched_traces = {}
fetch_ok = False
try:
    url = f"{LANGFUSE_HOST.rstrip('/')}/api/public/traces?limit=20"
    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        traces_list = data.get("data", [])
        log(f"test: Step 6/7 - Fetched {len(traces_list)} recent traces from Langfuse")
        for t in traces_list:
            tid = t.get("id", "")
            if tid in (trace_id_1, trace_id_2):
                fetched_traces[tid] = t
        fetch_ok = True
        log(f"test: Step 6/7 - Found {len(fetched_traces)}/2 of our traces in the response")
    else:
        log(f"test: Step 6/7 - Langfuse API returned HTTP {resp.status_code}: {resp.text[:200]}")
except Exception as e:
    log(f"test: Step 6/7 - ERROR fetching traces: {e}")


# ── Step 7: Verification ──────────────────────────────────────────────────────
log("test: Step 7/7 - Verifying correlation_id, parent-child linking, and metadata")

# --- Verification 1: Both traces have same correlation_id ---
corr1 = meta1.get("correlation_id")
corr2 = meta2.get("correlation_id")
correlation_linking_ok = (corr1 == correlation_id) and (corr2 == correlation_id)
corr_check = "✅" if correlation_linking_ok else "❌"
log(f"test: Step 7/7 - Correlation ID check: trace1={corr1!r}, trace2={corr2!r}, expected={correlation_id!r} → {corr_check}")

# --- Verification 2: Second trace has parentTraceId = first trace's ID ---
# Check from the local metadata dict we built
parent_trace_in_meta2 = meta2.get("parent_trace_id")
parent_linking_ok = (parent_trace_in_meta2 == trace_id_1)
parent_check = "✅" if parent_linking_ok else "❌"
log(f"test: Step 7/7 - Parent-child check: meta2.parent_trace_id={parent_trace_in_meta2!r}, trace_id_1={trace_id_1!r} → {parent_check}")

# Also verify from Langfuse API response if we fetched it
if fetched_traces.get(trace_id_2):
    api_parent = fetched_traces[trace_id_2].get("parentTraceId") or fetched_traces[trace_id_2].get("parent_trace_id")
    log(f"test: Step 7/7 - Langfuse API parentTraceId for trace2 = {api_parent!r}")
else:
    log("test: Step 7/7 - Note: trace_id_2 not in fetched batch (may be propagation delay)")

# --- Verification 3: Metadata contains decomposition_level and is_sub_query ---
decom1 = meta1.get("decomposition_level")
decom2 = meta2.get("decomposition_level")
issub1 = meta1.get("is_sub_query")
issub2 = meta2.get("is_sub_query")

meta_fields_ok = (
    decom1 is not None and decom2 is not None
    and issub1 is not None and issub2 is not None
)
meta_check = "✅" if meta_fields_ok else "❌"
log(f"test: Step 7/7 - Metadata fields: trace1(decomposition_level={decom1}, is_sub_query={issub1}), trace2(decomposition_level={decom2}, is_sub_query={issub2}) → {meta_check}")

# Expected behavior: trace1 is_sub_query=False (no parent), trace2 is_sub_query=True (has parent)
is_sub_semantics_ok = (issub1 is False or issub1 == False) and (issub2 is True or issub2 == True)
log(f"test: Step 7/7 - is_sub_query semantics: trace1={issub1} (expect False), trace2={issub2} (expect True) → {'✅' if is_sub_semantics_ok else '❌'}")

# ── Final Report ──────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("CORRELATION ID TEST REPORT")
print("=" * 60)
print(f"Correlation ID generated : {correlation_id}")
print(f"Trace ID 1 (root call)   : {trace_id_1}")
print(f"Trace ID 2 (follow-up)   : {trace_id_2}")
print(f"Trace 1 ingested         : {lf1_ingested}")
print(f"Trace 2 ingested         : {lf2_ingested}")
print()
print(f"Correlation ID linking   : {corr_check}  (both traces share correlation_id={correlation_id!r})")
print(f"Parent-child linking     : {parent_check}  (trace2.parent_trace_id == trace_id_1)")
print(f"Metadata fields present  : {meta_check}  (decomposition_level + is_sub_query in both)")
print(f"  ↳ is_sub_query semantics: {'✅' if is_sub_semantics_ok else '❌'} (trace1=False, trace2=True)")
print()
print("Metadata snapshot (trace1):")
for k in ("correlation_id", "parent_trace_id", "decomposition_level", "is_sub_query"):
    print(f"  {k}: {meta1.get(k)!r}")
print("Metadata snapshot (trace2):")
for k in ("correlation_id", "parent_trace_id", "decomposition_level", "is_sub_query"):
    print(f"  {k}: {meta2.get(k)!r}")
print("=" * 60)

log(f"test: Step 7/7 - Done. correlation={corr_check} parent={parent_check} metadata={meta_check}")
