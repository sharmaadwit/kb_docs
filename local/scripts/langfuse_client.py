#!/usr/bin/env python3
"""Local Langfuse analysis helper — v4 SDK (langfuse>=4.7.0).

LOCAL ANALYSIS ONLY. The skill (skill/kb_answer.py) transmits telemetry via
raw OTLP/HTTP and is separate from this module.

Ingestion path (skill):
  POST /api/public/otel/v1/traces (OTLP/JSON, non-deprecated)
  Metadata is embedded in trace.input._meta because OTLP traces are NOT
  surfaced by v2/observations — they only appear in the legacy /traces API.

Fetch path (analytics):
  list_traces() → GET /api/public/traces (legacy list, page-based)
  OTLP-ingested traces only appear here, not in v2/observations.
  Metadata extracted from trace.input._meta (OTLP) or trace.metadata (SDK).
  get_trace()   → GET /api/public/traces/{id} (legacy single-fetch)

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
            if key and not os.getenv(key):
                os.environ[key] = val


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


def _trace_to_shape(trace: dict) -> dict:
    """Normalise a legacy /traces object into the standard analytics shape.

    OTLP-ingested traces: metadata lives in trace.input._meta (embedded by
    _build_otlp_request in skill/kb_answer.py — v2/observations does not
    surface OTLP traces so the legacy list endpoint is the only fetch path).
    SDK-ingested traces: metadata lives directly in trace.metadata.
    """
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


def _obs_to_trace_shape(obs: dict) -> dict:
    """Remap ObservationV2 model_dump() fields to the standard analytics shape.

    Only used for SDK-ingested observations fetched via v2/observations.
    OTLP-ingested traces do NOT appear in v2/observations — use list_traces()
    which goes through the legacy /traces endpoint instead.
    """
    inp = obs.get("input") or {}
    meta = (inp.get("_meta") if isinstance(inp, dict) else None) or obs.get("metadata") or {}
    return {
        "id": obs.get("traceId") or obs.get("trace_id"),
        "timestamp": obs.get("startTime") or obs.get("start_time"),
        "name": obs.get("name"),
        "userId": obs.get("userId") or obs.get("user_id"),
        "metadata": meta,
        "input": inp,
        "output": obs.get("output"),
        "_obs_id": obs.get("id"),
    }


def list_traces(
    client: Langfuse,
    name: Optional[str] = None,
    limit: int = 20,
    from_timestamp=None,
    cursor: Optional[str] = None,
    page: int = 1,
    timeout: int = DEFAULT_TIMEOUT,
):
    """List traces via legacy GET /api/public/traces (page-based pagination).

    Returns (list_of_trace_shaped_dicts, next_page_or_None).
    Uses the legacy endpoint because OTLP-ingested traces (all production
    traces since the v4 ingestion migration) are NOT surfaced by v2/observations.

    The cursor param is accepted for API compatibility but ignored — the legacy
    endpoint uses page numbers. Pass page= to fetch successive pages.
    """
    kwargs: dict = {"limit": limit, "page": page, "request_options": _req_opts(timeout)}
    if name:
        kwargs["name"] = name
    if from_timestamp is not None:
        kwargs["from_timestamp"] = from_timestamp
    res = client.api.trace.list(**kwargs)
    data = [_trace_to_shape(t.model_dump(mode="json", by_alias=True)) for t in res.data]
    # Legacy endpoint has no cursor; signal no-more-pages when result is smaller than limit
    has_more = len(res.data) >= limit
    return data, None if not has_more else "page"


def get_trace(client: Langfuse, trace_id: str, timeout: int = DEFAULT_TIMEOUT):
    """Fetch a single trace by ID from GET /api/public/traces/{id}.

    Returns a trace-shaped dict (same shape as list_traces() items).
    """
    t = client.api.trace.get(trace_id, request_options=_req_opts(timeout))
    return _trace_to_shape(t.model_dump(mode="json", by_alias=True))


def delete_traces(client: Langfuse, trace_ids: List[str],
                  timeout: int = DEFAULT_TIMEOUT):
    """Delete test traces so they don't pollute the CxO dashboard."""
    if not trace_ids:
        return None
    return client.api.trace.delete_multiple(
        trace_ids=trace_ids, request_options=_req_opts(timeout)
    )


if __name__ == "__main__":
    lf = get_client()
    print("Recent kb_answer traces (via legacy /traces list):")
    traces, _ = list_traces(lf, name="kb_answer", limit=5)
    for t in traces:
        meta = t.get("metadata") or {}
        print(f"  {t['id']}  answered={meta.get('answered')}  module={meta.get('module_label')}")
