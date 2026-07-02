#!/usr/bin/env python3
"""Local Langfuse analysis helper — v4 SDK (langfuse>=4.x).

LOCAL ANALYSIS ONLY. The skill (skill/kb_answer.py) transmits telemetry via raw
HTTP and is intentionally NOT changed. This module is for local trace inspection,
comparison and cleanup during testing.

v3 -> v4 migration notes (per langfuse.com/docs/observability/sdk/upgrade-path/python-v3-to-v4):
  - Trace fetching moved to the typed `.api` client:
        lf.api.trace.list(...)          # was fetch_traces()
        lf.api.trace.get(trace_id)      # was get_trace()
        lf.api.trace.delete_multiple([ids])
  - High-performance v2 endpoints are now the defaults (api.observations,
    api.scores, api.metrics).
  - Cloud reads can be slow from some networks; pass a generous
    request_options timeout.

Reads credentials from env (LANGFUSE_HOST / LANGFUSE_PUBLIC_KEY /
LANGFUSE_SECRET_KEY) or from ../../.env.
"""
import os
from typing import List, Optional

try:
    from langfuse import Langfuse
except ImportError as e:  # pragma: no cover
    raise SystemExit(
        "langfuse SDK not installed. Run: pip3 install --upgrade langfuse"
    ) from e


def _load_env_from_dotenv():
    """Best-effort load of .env into environment (all keys, not just LANGFUSE_*)."""
    dotenv = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    if not os.path.exists(dotenv):
        return
    with open(dotenv) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip('"').strip("'")
            # Load any non-empty key that's not already set (don't override shell env)
            if key and not os.getenv(key):
                os.environ[key] = val


# Cloud reads from some networks are slow; default generous.
DEFAULT_TIMEOUT = 60


def get_client(timeout: int = DEFAULT_TIMEOUT) -> Langfuse:
    """Return a v4 Langfuse client configured from env / .env."""
    _load_env_from_dotenv()
    return Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
        timeout=timeout,
    )


def _req_opts(timeout: int = DEFAULT_TIMEOUT):
    return {"timeout_in_seconds": timeout}


def list_traces(client: Langfuse, name: Optional[str] = None,
                limit: int = 20, timeout: int = DEFAULT_TIMEOUT):
    """List traces (optionally filtered by name). Returns list of trace objects."""
    res = client.api.trace.list(
        name=name, limit=limit, request_options=_req_opts(timeout)
    )
    return res.data


def get_trace(client: Langfuse, trace_id: str, timeout: int = DEFAULT_TIMEOUT):
    """Fetch a single trace with full observations."""
    return client.api.trace.get(trace_id, request_options=_req_opts(timeout))


def delete_traces(client: Langfuse, trace_ids: List[str],
                  timeout: int = DEFAULT_TIMEOUT):
    """Delete test traces so they don't pollute the CxO dashboard."""
    if not trace_ids:
        return None
    return client.api.trace.delete_multiple(
        trace_ids=trace_ids, request_options=_req_opts(timeout)
    )


if __name__ == "__main__":
    # Smoke test: list recent kb_answer traces.
    lf = get_client()
    print("Recent kb_answer traces:")
    for t in list_traces(lf, name="kb_answer", limit=5):
        print(f"  {t.id}  {t.timestamp}")
