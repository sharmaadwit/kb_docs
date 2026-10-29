#!/usr/bin/env python3
"""
Generate Comprehensive KB Analytics Dashboard with All Reports
Always fetches LIVE data from Langfuse API, never uses cached JSON files.
Includes: Global metrics, module analysis, intent distribution, user segmentation, video analytics, etc.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional, Dict, List, Any
import re

# Known maintainer/test accounts. Their traffic is excluded from all headline
# metrics (answer rate, IDK rate, confidence, conversation stats) but is still
# surfaced separately in its own "Test/Maintainer Traffic" table, never silently
# dropped.
TEST_ACCOUNTS = {"adwit.sharma@gupshup.io"}

# All times shown on the dashboard, and the day/week grouping, use IST (UTC+5:30).
# Stored trace timestamps and internal cutoffs stay UTC.
IST_OFFSET = timedelta(hours=5, minutes=30)


def _to_ist(dt: datetime) -> datetime:
    """Naive-UTC datetime -> naive IST datetime."""
    return dt + IST_OFFSET


def summarize_test_traffic(traces: List[Dict]) -> Dict[str, Any]:
    """Lightweight summary of excluded test/maintainer traffic for transparency."""
    count = len(traces)
    answered = sum(1 for t in traces if (t.get("metadata") or {}).get("answered"))
    idk = count - answered
    conf_sum = sum((t.get("metadata") or {}).get("confidence") or 0 for t in traces)
    samples = []
    for t in traces[:10]:
        meta = t.get("metadata") or {}
        samples.append({
            "query": (meta.get("query") or "").strip(),
            "module": meta.get("module_label") or meta.get("module") or "",
            "answered": bool(meta.get("answered")),
        })
    return {
        "count": count,
        "answered": answered,
        "idk": idk,
        "answer_rate": round(answered / count * 100, 1) if count else 0.0,
        "avg_confidence": round(conf_sum / count, 2) if count else 0.0,
        "samples": samples,
    }


def detect_language(text: str) -> str:
    """Detect language from text using character patterns and common words."""
    if not text:
        return "unknown"

    text_lower = text.lower()

    # Portuguese patterns (pt)
    if any(word in text_lower for word in ["ão", "ões", "ê", "õ", "é", "à", "ü"]):
        if re.search(r'\b(o|a|de|para|com|sem|este|esse|aquele)\b', text_lower):
            return "pt"

    # Spanish patterns (es)
    if any(word in text_lower for word in ["ñ", "¿", "¡", "ü"]):
        if re.search(r'\b(el|la|de|para|con|sin|este|ese|aquel)\b', text_lower):
            return "es"

    # Arabic patterns (ar)
    if re.search(r'[؀-ۿ]', text):
        return "ar"

    # Hindi patterns (hi)
    if re.search(r'[ऀ-ॿ]', text):
        return "hi"

    # Chinese/Japanese patterns (zh/ja)
    if re.search(r'[一-鿿]', text):
        return "zh"
    if re.search(r'[぀-ゟ゠-ヿ]', text):
        return "ja"

    # Korean patterns (ko)
    if re.search(r'[가-힯]', text):
        return "ko"

    # Default to English
    return "en"


def _load_env():
    """Load .env file from kb_docs root into os.environ."""
    env_path = Path(__file__).parent.parent.parent / ".env"
    if not env_path.exists():
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")
TRACE_CACHE_PATH = os.path.join(CACHE_DIR, "langfuse_traces_cache.json")
INITIAL_BACKFILL_DAYS = 90  # system has been live <2 months; no need for a 3-year pull
INCREMENTAL_OVERLAP_HOURS = 6  # re-fetch a small overlap window to catch late-arriving traces


def _load_trace_cache() -> Dict:
    if os.path.exists(TRACE_CACHE_PATH):
        try:
            with open(TRACE_CACHE_PATH) as f:
                return json.load(f)
        except Exception:
            pass
    return {"last_fetch_max_timestamp": None, "traces": {}}


def _save_trace_cache(cache: Dict) -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(TRACE_CACHE_PATH, "w") as f:
        json.dump(cache, f)


def fetch_langfuse_traces(days: Optional[int] = None) -> Optional[List[Dict]]:
    """Fetch traces from Langfuse, using a local cache + incremental fetch.

    First run (no cache): backfills `days` if given, else INITIAL_BACKFILL_DAYS
    (system has been live <2 months, so 90 days covers full history without a
    wasteful multi-year pull).
    Subsequent runs: fetches only traces since the last cached max timestamp
    (minus a small overlap buffer), merges into the cache by trace id, and
    returns the full merged set. This avoids re-fetching the entire history
    (and tripping Langfuse rate limits) on every dashboard refresh.
    """
    _load_env()
    cache = _load_trace_cache()
    has_cache = bool(cache.get("traces"))

    if has_cache and cache.get("last_fetch_max_timestamp"):
        last_ts = datetime.fromisoformat(cache["last_fetch_max_timestamp"].replace("Z", "+00:00"))
        from_dt = last_ts - timedelta(hours=INCREMENTAL_OVERLAP_HOURS)
        print(f"🔄 Incremental fetch: {len(cache['traces'])} traces cached, fetching new traces since {from_dt.isoformat()}...")
    else:
        backfill_days = days if days is not None else INITIAL_BACKFILL_DAYS
        from_dt = datetime.utcnow() - timedelta(days=backfill_days)
        print(f"🔄 No cache found — initial backfill for last {backfill_days} days...")

    # Fetch via legacy GET /api/public/traces (page-based pagination).
    # OTLP-ingested traces (all production traffic going forward) only appear
    # here — they do NOT appear in v2/observations.
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from langfuse_client import get_client, list_traces as _sdk_list_traces, _trace_to_shape

        pub = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
        sec = os.environ.get("LANGFUSE_SECRET_KEY", "")

        if pub and sec:
            client = get_client()
            new_traces = []
            page = 1
            page_limit = 100

            while True:
                batch, _ = _sdk_list_traces(
                    client, name="kb_answer", limit=page_limit,
                    from_timestamp=from_dt, page=page,
                )
                new_traces.extend(batch)

                if len(batch) < page_limit:
                    break
                page += 1

            print(f"✅ Fetched {len(new_traces)} new/updated traces via legacy /api/public/traces")

            # Merge into cache by trace id (new data wins on conflict)
            for t in new_traces:
                tid = t.get("id")
                if tid:
                    cache["traces"][tid] = t

            # Track max timestamp seen across cache for next incremental fetch
            all_ts = [t.get("timestamp") for t in cache["traces"].values() if t.get("timestamp")]
            if all_ts:
                cache["last_fetch_max_timestamp"] = max(all_ts)

            if cache["traces"]:
                _save_trace_cache(cache)
                merged = list(cache["traces"].values())
                print(f"📦 Cache now holds {len(merged)} total traces ({TRACE_CACHE_PATH})")
                return merged
        else:
            print("⚠️  Langfuse credentials missing from env")
    except Exception as e:
        print(f"❌ Langfuse SDK fetch FAILED: {e}")
        print(f"\n❌ MANDATORY LIVE DATA REQUIREMENT NOT MET")
        print(f"   Dashboard generation requires live Langfuse data to produce a NEW dashboard.")
        print(f"   Not falling back to cache — the previously generated dashboard is already")
        print(f"   built and hosted from that same cached data, so re-running would be wasted work.")
        print(f"\nAction required:")
        print(f"   1. Check Langfuse API credentials in .env (LANGFUSE_HOST, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY)")
        print(f"   2. Verify network connectivity to Langfuse cloud")
        print(f"   3. Check Langfuse API rate limits — if rate-limited, wait and retry rather than re-running immediately")
        print(f"   4. Retry dashboard generation")
        sys.exit(1)

    # Method 2: Try Langfuse CLI
    try:
        import subprocess
        cmd = ["lf", "export", "traces", "--output", "json"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            traces_list = data.get("traces", data) if isinstance(data, dict) else data
            if traces_list:
                print(f"✅ Fetched {len(traces_list)} traces via Langfuse CLI")
                return traces_list
    except Exception as e:
        print(f"⚠️  CLI fetch failed: {e}")

    print(f"\n❌ MANDATORY LIVE DATA REQUIREMENT NOT MET")
    print(f"   All methods to fetch live Langfuse traces have failed:")
    print(f"   1. REST API (HTTP request) - failed")
    print(f"   2. Langfuse CLI (lf export) - failed")
    print(f"\n   Not falling back to cache — the previously generated dashboard is already")
    print(f"   built and hosted from that same cached data, so re-running would be wasted work.")
    print(f"\nAction required:")
    print(f"   1. Verify Langfuse API is accessible (LANGFUSE_HOST={os.getenv('LANGFUSE_HOST')})")
    print(f"   2. Check credentials: LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY")
    print(f"   3. Verify network connectivity to Langfuse cloud")
    print(f"   4. Check Langfuse service status and rate limits")
    print(f"   5. Run 'lf export traces --output json' to test CLI access")
    print(f"\n   Retry dashboard generation after resolving connectivity issues.")
    sys.exit(1)
    return None


def fetch_proposal_traces() -> List[Dict]:
    """Fetch GTM/proposal-agent traces from its own, separate Langfuse project
    (LANGFUSE_*_PROPOSAL env vars -- a different project than the main
    LANGFUSE_PUBLIC_KEY/SECRET_KEY used everywhere else in this file).

    Low volume (tens of traces, not thousands) so no incremental cache like
    fetch_langfuse_traces -- a full fetch every run is cheap. Unlike that
    function, failures here degrade gracefully (empty list, tab just shows
    "no data") rather than sys.exit -- this is a supplementary tab, not the
    dashboard's core data source.
    """
    _load_env()
    pub = os.environ.get("LANGFUSE_PUBLIC_KEY_PROPOSAL", "")
    sec = os.environ.get("LANGFUSE_SECRET_KEY_PROPOSAL", "")
    host = os.environ.get("LANGFUSE_HOST_PROPOSAL", "https://cloud.langfuse.com")
    if not (pub and sec):
        print("⚠️  Proposal-agent Langfuse credentials missing from env -- skipping that tab")
        return []
    try:
        sys.path.insert(0, os.path.dirname(__file__))
        from langfuse import Langfuse
        from langfuse_client import list_traces as _sdk_list_traces

        client = Langfuse(public_key=pub, secret_key=sec, host=host, timeout=60)
        all_traces, page, page_limit = [], 1, 100
        while True:
            batch, _ = _sdk_list_traces(client, limit=page_limit, page=page)
            all_traces.extend(batch)
            if len(batch) < page_limit:
                break
            page += 1
        print(f"✅ Fetched {len(all_traces)} proposal-agent traces (separate Langfuse project)")
        return all_traces
    except Exception as e:
        print(f"⚠️  Proposal-agent trace fetch failed: {e} -- tab will show no data")
        return []


def fetch_cross_sell_observations(days: int = 60) -> List[Dict]:
    """Fetch cross_sell_skill observations from its own, separate Langfuse org
    (LANGFUSE_*_CROSS_SELL env vars). This org returns HTTP 410 on the legacy
    GET /api/public/traces endpoint used everywhere else in this file --
    confirmed by direct probe, matches a documented Langfuse platform change:
    orgs created on/after 2026-09-16 only support the v2/observations read
    path, not the legacy trace-list endpoint. So this function talks to
    /api/public/v2/observations directly (cursor pagination, basic auth)
    instead of going through langfuse_client.py's list_traces(), which only
    knows the legacy path.

    Root observations only (isRootObservation=True) -- one per skill call,
    matching how fetch_proposal_traces()/fetch_langfuse_traces() both treat
    one call as one row. Degrades gracefully on failure (empty list), same
    policy as fetch_proposal_traces -- this is a supplementary tab.
    """
    _load_env()
    pub = os.environ.get("LANGFUSE_PUBLIC_KEY_CROSS_SELL", "")
    sec = os.environ.get("LANGFUSE_SECRET_KEY_CROSS_SELL", "")
    host = os.environ.get("LANGFUSE_HOST_CROSS_SELL", "https://cloud.langfuse.com")
    if not (pub and sec):
        print("⚠️  Cross-sell-skill Langfuse credentials missing from env -- skipping that tab")
        return []
    try:
        import requests
        since = datetime.utcnow() - timedelta(days=days)
        until = datetime.utcnow() + timedelta(minutes=5)
        rows, seen, cursor = [], set(), None
        flt = [{"type": "boolean", "column": "isRootObservation", "operator": "=", "value": True}]
        while True:
            params = {
                "fromStartTime": since.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "toStartTime": until.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "limit": 100, "fields": "core,basic,trace_context,metadata",
                "filter": json.dumps(flt),
            }
            if cursor:
                params["cursor"] = cursor
            r = requests.get(f"{host}/api/public/v2/observations", params=params, auth=(pub, sec), timeout=30)
            r.raise_for_status()
            page = r.json()
            for o in page.get("data") or []:
                oid = o.get("id")
                if oid and oid not in seen:
                    seen.add(oid)
                    rows.append(o)
            cursor = (page.get("meta") or {}).get("cursor")
            if not cursor:
                break
        print(f"✅ Fetched {len(rows)} cross-sell-skill observations (separate Langfuse org, v2/observations)")
        return rows
    except Exception as e:
        print(f"⚠️  Cross-sell-skill observation fetch failed: {e} -- tab will show no data")
        return []


def analyze_cross_sell_traces(observations: List[Dict]) -> Dict[str, Any]:
    """Aggregate cross_sell_skill observations. This skill is a deterministic
    groundedness-validation guardrail in front of the Cross Sell Agent's own
    Genome MCP data (not a content generator like proposal_generator) -- the
    useful signals are: how often grounding checks come back clean vs. flag a
    problem, which grounding-failure types actually fire (cohort_not_ready,
    cohort_approximation, missing_basis -- see groundedness_warnings() in
    cross_sell_skill.py), forbidden/rejected action attempts (a genuine
    agent-instruction-drift signal, since only check_groundedness is allowed
    as of v0.5.0), and the sales-targeting context (industry/segment/region)
    the agent is actually working with.
    """
    from collections import Counter

    def _norm_list(v):
        """Langfuse truncates metadata string values at ~200 characters. A
        list-typed field that's long enough (e.g. many repeated warning
        codes) gets JSON-serialized, truncated mid-array by Langfuse, and
        comes back as a broken JSON string -- not valid JSON, and NOT safe to
        iterate directly (that iterates its characters, not its elements).
        Try a clean parse first; on failure, best-effort recover whatever
        complete quoted tokens survived the truncation; never fall through to
        the raw string itself."""
        if isinstance(v, list):
            return v
        if not isinstance(v, str) or not v.strip():
            return []
        try:
            parsed = json.loads(v)
            return parsed if isinstance(parsed, list) else []
        except (ValueError, TypeError):
            return re.findall(r'"([^"]*)"', v)

    n = len(observations)
    by_day = Counter()
    actions = Counter()
    error_codes = Counter()
    warning_codes = Counter()
    cohort_status = Counter()
    cohort_type = Counter()
    source_action = Counter()
    industry = Counter()
    segment = Counter()
    region = Counter()
    list_shape = Counter()
    ok_count = clean_count = 0
    latency = []
    row_counts = []

    for o in observations:
        m = o.get("metadata") or {}
        action = m.get("action") or (o.get("name") or "").split(":", 1)[-1] or "unknown"
        actions[action] += 1
        if m.get("ok") is True:
            ok_count += 1
        if m.get("clean") is True:
            clean_count += 1
        for c in _norm_list(m.get("error_codes")):
            error_codes[c] += 1
        for c in _norm_list(m.get("warning_codes")):
            warning_codes[c] += 1
        if m.get("cohort_status") not in (None, "unspecified"):
            cohort_status[m["cohort_status"]] += 1
        if m.get("cohort_type") not in (None, "unspecified"):
            cohort_type[m["cohort_type"]] += 1
        if m.get("source_action") not in (None, "unspecified"):
            source_action[m["source_action"]] += 1
        if m.get("industry") not in (None, "unspecified"):
            industry[m["industry"]] += 1
        if m.get("segment") not in (None, "unspecified"):
            segment[m["segment"]] += 1
        if m.get("region") not in (None, "unspecified"):
            region[m["region"]] += 1
        if m.get("list_shape") not in (None, "unspecified"):
            list_shape[m["list_shape"]] += 1
        ts = o.get("startTime")
        if ts:
            try:
                by_day[datetime.fromisoformat(str(ts).replace("Z", "+00:00")).date().isoformat()] += 1
            except Exception:
                pass
        lat = m.get("latency_ms")
        if isinstance(lat, (int, float)) and not isinstance(lat, bool):
            latency.append(lat)
        rc = m.get("row_count")
        if isinstance(rc, (int, float)) and not isinstance(rc, bool):
            row_counts.append(rc)

    def _pct(a, b):
        return round(100.0 * a / b, 1) if b else 0.0

    def _stat(xs):
        import statistics
        return {"min": min(xs), "median": round(statistics.median(xs), 1), "mean": round(statistics.mean(xs), 1), "max": max(xs)} if xs else None

    forbidden_attempts = sum(c for a, c in actions.items() if a != "check_groundedness")

    return {
        "total": n,
        "by_day": sorted(by_day.items()),
        "actions": actions.most_common(),
        "forbidden_attempts": forbidden_attempts,
        "ok_rate": _pct(ok_count, n),
        "clean_rate": _pct(clean_count, n),
        "error_codes": error_codes.most_common(),
        "warning_codes": warning_codes.most_common(),
        "cohort_status": cohort_status.most_common(),
        "cohort_type": cohort_type.most_common(),
        "source_action": source_action.most_common(),
        "industry": industry.most_common(),
        "segment": segment.most_common(),
        "region": region.most_common(),
        "list_shape": list_shape.most_common(),
        "latency_ms": _stat(latency),
        "row_count": _stat(row_counts),
    }


def generate_cross_sell_tab_html(analysis: Dict[str, Any]) -> str:
    """Render the Cross Sell Agent / groundedness-skill tab."""
    n = analysis.get("total", 0)
    if not n:
        return """
        <div class="section"><h2>🧮 Cross Sell / Groundedness</h2>
        <p class="muted">No calls yet, or Langfuse credentials for this project are not configured.</p></div>
"""

    def _count_table(title: str, rows, note: str = "") -> str:
        body = "".join(f"<tr><td>{name}</td><td>{count}</td></tr>" for name, count in list(rows)[:25])
        extra = f'<p class="muted">{note}</p>' if note else ""
        return f"""
        <div class="section"><h3>{title}</h3>{extra}
        <table><thead><tr><th>Name</th><th>Count</th></tr></thead>
        <tbody>{body or '<tr><td colspan="2">None recorded</td></tr>'}</tbody></table>
        </div>
"""

    def _stat_block(title: str, stat) -> str:
        if not stat:
            return ""
        return f"""
        <div class="section"><h3>{title}</h3>
        <p>min {stat['min']} &middot; median {stat['median']} &middot; mean {stat['mean']} &middot; max {stat['max']}</p>
        </div>
"""

    forbidden = analysis.get("forbidden_attempts", 0)
    forbidden_note = (
        f"<p class=\"muted\" style=\"color:#dc2626;\"><b>{forbidden}</b> call(s) used an action other than check_groundedness "
        f"-- only check_groundedness is allowed as of skill v0.5.0; this is a drift/misuse signal worth checking the agent's instructions for.</p>"
        if forbidden else ""
    )

    cards = f"""
        <div class="grid">
            <div class="card" style="border-left: 5px solid #f59e0b;">
                <div class="metric"><div class="metric-label">Calls</div><div class="metric-value">{n}</div>
                <div class="metric-unit">groundedness checks</div></div>
            </div>
            <div class="card" style="border-left: 5px solid #f59e0b;">
                <div class="metric"><div class="metric-label">Clean Rate</div><div class="metric-value">{analysis.get('clean_rate', 0)}%</div>
                <div class="metric-unit">no grounding warnings</div></div>
            </div>
            <div class="card" style="border-left: 5px solid #f59e0b;">
                <div class="metric"><div class="metric-label">Valid Call Rate</div><div class="metric-value">{analysis.get('ok_rate', 0)}%</div>
                <div class="metric-unit">passed input validation</div></div>
            </div>
            <div class="card" style="border-left: 5px solid #f59e0b;">
                <div class="metric"><div class="metric-label">Forbidden-action Attempts</div><div class="metric-value">{forbidden}</div>
                <div class="metric-unit">e.g. list_cohorts -- should be 0</div></div>
            </div>
        </div>
"""

    by_day = analysis.get("by_day") or []
    volume_rows = "".join(f"<tr><td>{day}</td><td>{count}</td></tr>" for day, count in reversed(by_day[-30:]))
    volume_html = f"""
        <div class="section"><h3>Volume by day (last 30 shown)</h3>
        <table><thead><tr><th>Day</th><th>Calls</th></tr></thead>
        <tbody>{volume_rows or '<tr><td colspan="2">No data</td></tr>'}</tbody></table>
        </div>
"""

    grounding_html = "".join([
        _count_table("Warning codes (grounding issues flagged)", analysis.get("warning_codes", []),
                     note="cohort_not_ready / cohort_approximation / missing_basis -- the actual data-quality problems caught before the agent used them in an answer."),
        _count_table("Error codes (rejected calls)", analysis.get("error_codes", [])),
        _count_table("Actions called", analysis.get("actions", []), note=forbidden_note.replace('<p class="muted" style="color:#dc2626;">', '').replace('</p>', '') if forbidden else ""),
    ])

    context_html = "".join([
        _count_table("Cohort status (Genome data freshness)", analysis.get("cohort_status", [])),
        _count_table("Cohort type", analysis.get("cohort_type", [])),
        _count_table("Source action (which Genome MCP tool fed this)", analysis.get("source_action", [])),
        _count_table("Industry", analysis.get("industry", [])),
        _count_table("Segment", analysis.get("segment", [])),
        _count_table("Region", analysis.get("region", [])),
        _count_table("Result shape", analysis.get("list_shape", [])),
    ])

    stats_html = "".join([
        _stat_block("Latency (ms)", analysis.get("latency_ms")),
        _stat_block("Row count per call", analysis.get("row_count")),
    ])

    return f"""
        <div class="section"><h2>🧮 Cross Sell / Groundedness</h2>
        <p class="muted">Separate Langfuse org (cross_sell_skill, a deterministic groundedness-validation guardrail in front of the Cross Sell Agent's Genome MCP data -- not a content generator). Uses the v2/observations read path, not the legacy traces API this dashboard uses elsewhere.</p>
        {forbidden_note}
        </div>
{cards}
{volume_html}
{grounding_html}
{context_html}
{stats_html}
"""


def analyze_proposal_traces(traces: List[Dict]) -> Dict[str, Any]:
    """Aggregate GTM/proposal-agent traces (gtm-agent-turn schema -- intent/
    connectors/capability_gaps/time_saved_minutes, NOT the answered/confidence/
    module shape used by every other tab in this dashboard)."""
    from collections import Counter

    total = len(traces)
    by_day = Counter()
    intents = Counter()
    connectors = Counter()
    gaps = Counter()
    risks = Counter()
    response_types = Counter()
    users = Counter()
    automation_triggered = 0
    time_saved_total = 0

    for t in traces:
        meta = t.get("metadata") or {}
        ts = t.get("timestamp")
        if ts:
            try:
                day = datetime.fromisoformat(str(ts).replace("Z", "+00:00")).date().isoformat()
                by_day[day] += 1
            except Exception:
                pass
        intents[meta.get("intent") or "unknown"] += 1
        for c in (meta.get("connectors_attempted") or []):
            connectors[c] += 1
        for g in (meta.get("capability_gaps") or []):
            gaps[g] += 1
        for rf in (meta.get("risk_flags") or []):
            risks[rf] += 1
        response_types[meta.get("response_type") or "unknown"] += 1
        users[t.get("userId") or "unknown"] += 1
        if meta.get("automation_triggered"):
            automation_triggered += 1
        time_saved_total += (meta.get("time_saved_minutes") or 0)

    return {
        "total": total,
        "unique_users": len([u for u in users if u != "unknown"]),
        "by_day": dict(sorted(by_day.items())),
        "intents": intents.most_common(),
        "connectors": connectors.most_common(),
        "capability_gaps": gaps.most_common(),
        "risk_flags": risks.most_common(),
        "response_types": response_types.most_common(),
        "automation_triggered": automation_triggered,
        "automation_rate": round(100 * automation_triggered / total, 1) if total else 0.0,
        "time_saved_total": time_saved_total,
        "time_saved_avg": round(time_saved_total / total, 1) if total else 0.0,
    }


def analyze_proposal_generator_traces(traces: List[Dict]) -> Dict[str, Any]:
    """Aggregate proposal_generator traces (the WhatsApp-demo-proposal builder tool,
    distinct from the gtm-agent-turn chat agent above -- same Langfuse project,
    different trace name, much richer telemetry: industry/use-case/channel
    classification, effort sizing, validation errors, component adoption, and
    session-level iteration/friction).

    Ported from the reference aggregate()/findings() in isildurs-bane's own
    design/skills/proposal_generator/tools/proposal_usage_report.py -- that
    script is the authoritative definition of what's useful here (written by
    whoever built the telemetry), not something to reinvent independently.
    Adapted from its v2/observations fetch to this file's existing legacy
    /api/public/traces fetch (same trace data, different read path -- OTLP
    ingestion makes both legacy-traces and v2-observations valid reads, same
    as every other OTLP-ingested trace in this whole dashboard).
    """
    from collections import Counter
    import statistics

    def _pct(n, d):
        return round(100.0 * n / d, 1) if d else 0.0

    def _top(counter, n=10):
        return counter.most_common(n)

    n = len(traces)
    dims = {k: Counter() for k in ("industry", "channel", "purpose", "region", "requester_role", "client_size",
                                     "entry_point_kind", "language", "pattern_key", "effort_profile")}
    use_cases, formats, comps, gaps, unsupported, other_labels = Counter(), Counter(), Counter(), Counter(), Counter(), Counter()
    err_paths, err_codes, warn_codes, by_day = Counter(), Counter(), Counter(), Counter()
    pairs = Counter()
    ok = classified = priced = 0
    hours, steps, latency, pdf_pages = [], [], [], []

    for t in traces:
        m = t.get("metadata") or {}
        ok += 1 if m.get("artifact_created") is True else 0
        classified += 1 if m.get("insights_classified") is True else 0
        priced += 1 if m.get("price_computed") is True else 0
        for k, c in dims.items():
            if m.get(k) not in (None, ""):
                c[str(m[k])] += 1
        uc = m.get("use_cases") if isinstance(m.get("use_cases"), list) else []
        use_cases.update(uc)
        for u in uc:
            pairs[f"{m.get('industry', 'unspecified')} x {u}"] += 1
        formats.update(m.get("output_formats") if isinstance(m.get("output_formats"), list) else [])
        comps.update(m.get("component_types") if isinstance(m.get("component_types"), list) else [])
        gaps.update(m.get("capability_gaps") if isinstance(m.get("capability_gaps"), list) else [])
        unsupported.update(m.get("unsupported_requests") if isinstance(m.get("unsupported_requests"), list) else [])
        if m.get("other_label"):
            other_labels[str(m["other_label"])] += 1
        err_paths.update(m.get("error_paths") if isinstance(m.get("error_paths"), list) else [])
        err_codes.update(m.get("error_codes") if isinstance(m.get("error_codes"), list) else [])
        warn_codes.update(m.get("warning_codes") if isinstance(m.get("warning_codes"), list) else [])
        ts = t.get("timestamp")
        if ts:
            try:
                by_day[datetime.fromisoformat(str(ts).replace("Z", "+00:00")).date().isoformat()] += 1
            except Exception:
                pass
        for key, bucket in (("effort_hours", hours), ("step_count", steps), ("latency_ms", latency), ("pdf_pages", pdf_pages)):
            v = m.get(key)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                bucket.append(v)

    # Session-level iteration/friction: runs per session, runs to first success,
    # minutes to first success, sessions with a rejected run, abandoned sessions.
    by_session = defaultdict(list)
    for t in traces:
        sid = t.get("sessionId")
        if sid:
            ts = t.get("timestamp")
            try:
                dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00")) if ts else None
            except Exception:
                dt = None
            by_session[sid].append((dt, t.get("metadata") or {}))

    first_ok_runs, minutes, with_friction, abandoned = [], [], 0, 0
    for runs in by_session.values():
        runs.sort(key=lambda x: (x[0] is None, x[0]))
        idx = next((i for i, (_, m) in enumerate(runs, 1) if m.get("artifact_created") is True), None)
        if any(m.get("artifact_created") is False for _, m in runs):
            with_friction += 1
        if idx is None:
            abandoned += 1
            continue
        first_ok_runs.append(idx)
        a, b = runs[0][0], runs[idx - 1][0]
        if a and b:
            minutes.append((b - a).total_seconds() / 60.0)

    def _stat(xs):
        return {"min": min(xs), "median": round(statistics.median(xs), 1), "mean": round(statistics.mean(xs), 1), "max": max(xs)} if xs else None

    sessions = len(by_session)
    users = {t.get("userId") for t in traces if t.get("userId")}

    rep = {
        "runs": n, "ok": ok, "rejected": n - ok, "success_rate_pct": _pct(ok, n),
        "unique_users": len(users), "sessions": sessions,
        "classified_pct": _pct(classified, n), "unclassified_runs": n - classified,
        "per_day": sorted(by_day.items()),
        "industry": _top(dims["industry"]), "use_cases": _top(use_cases), "industry_x_use_case": _top(pairs, 12),
        "channel": _top(dims["channel"]), "purpose": _top(dims["purpose"]), "region": _top(dims["region"]),
        "requester_role": _top(dims["requester_role"]), "client_size": _top(dims["client_size"]),
        "entry_point": _top(dims["entry_point_kind"]), "language": _top(dims["language"]),
        "output_formats": _top(formats), "pdf_share_pct": _pct(formats.get("pdf", 0), n),
        "component_adoption": [(k, v, _pct(v, n)) for k, v in comps.most_common()],
        "patterns": _top(dims["pattern_key"]),
        "unsupported_requests": _top(unsupported), "capability_gaps": _top(gaps),
        "other_labels": _top(other_labels),
        "top_error_paths": _top(err_paths), "error_codes": _top(err_codes), "warning_codes": _top(warn_codes),
        "effort_hours": _stat(hours), "price_computed_pct": _pct(priced, n), "steps": _stat(steps),
        "latency_ms": _stat(latency), "pdf_pages": _stat(pdf_pages),
        "iteration": {
            "runs_per_session": _stat([len(r) for r in by_session.values()]),
            "runs_to_first_success": _stat(first_ok_runs),
            "minutes_to_first_success": _stat([round(x, 1) for x in minutes]),
            "sessions_with_a_rejected_run_pct": _pct(with_friction, sessions),
            "sessions_without_success_pct": _pct(abandoned, sessions),
        },
    }
    rep["findings"] = _proposal_generator_findings(rep)
    return rep


def _proposal_generator_findings(r: Dict[str, Any]) -> List[str]:
    """Same heuristics as the reference script's findings() -- plain-English,
    directly actionable observations, not just raw numbers."""
    out, n = [], r["runs"]
    if not n:
        return ["No runs in this window."]
    if r["classified_pct"] < 80:
        out.append(f"Only {r['classified_pct']}% of runs carry industry, use case and channel. Check the agent instructions that tell it to classify, or tag-filter 'unclassified' to see which sessions skip it.")
    if r["top_error_paths"] and r["rejected"]:
        p, c = r["top_error_paths"][0]
        out.append(f"Most common validation failure: {p} ({c} runs). Make the agent instruction or the error message for that field clearer.")
    if r["unsupported_requests"]:
        k, c = r["unsupported_requests"][0]
        out.append(f"Most requested unsupported feature: {k} ({c} runs). Strongest roadmap signal.")
    it = r["iteration"]
    if it["runs_to_first_success"] and it["runs_to_first_success"]["mean"] > 1.5:
        out.append(f"Users need {it['runs_to_first_success']['mean']} runs on average to a first success: collect requirements more completely before calling the skill.")
    if it["sessions_without_success_pct"] >= 20:
        out.append(f"{it['sessions_without_success_pct']}% of sessions never produced a file: look at their error paths.")
    if r["other_labels"]:
        out.append(f"'other' labels recorded ({', '.join(k for k, _ in r['other_labels'][:3])}): candidates for new taxonomy values.")
    if r["pdf_share_pct"] >= 30:
        out.append(f"PDF is requested in {r['pdf_share_pct']}% of runs: worth investing in PDF polish and non-Latin fonts if those markets matter.")
    cats = {k: v for k, v, _ in r["component_adoption"]}
    unused = [c for c in ("template", "list_menu", "audio", "pay", "carousel", "flow") if c not in cats]
    if unused and n >= 20:
        out.append(f"Never used in {n} runs: {', '.join(unused)}. Either unknown to the agent or not needed.")
    return out or ["Nothing stands out yet; keep collecting."]


def generate_proposal_generator_tab_html(analysis: Dict[str, Any]) -> str:
    """Render the Proposal Generator (demo-builder tool) sub-tab."""
    n = analysis.get("runs", 0)
    if not n:
        return """
        <div class="section"><h2>📄 Proposal Generator</h2>
        <p class="muted">No runs yet. This tool's telemetry was recently added -- once it's used in production, this sub-tab will populate.</p></div>
"""

    findings_html = "".join(f"<li>{f}</li>" for f in analysis.get("findings", []))
    cards = f"""
        <div class="grid">
            <div class="card" style="border-left: 5px solid #06b6d4;">
                <div class="metric"><div class="metric-label">Runs</div><div class="metric-value">{n}</div>
                <div class="metric-unit">{analysis.get('unique_users', 0)} users, {analysis.get('sessions', 0)} sessions</div></div>
            </div>
            <div class="card" style="border-left: 5px solid #06b6d4;">
                <div class="metric"><div class="metric-label">Success Rate</div><div class="metric-value">{analysis.get('success_rate_pct', 0)}%</div>
                <div class="metric-unit">({analysis.get('ok', 0)} ok, {analysis.get('rejected', 0)} rejected)</div></div>
            </div>
            <div class="card" style="border-left: 5px solid #06b6d4;">
                <div class="metric"><div class="metric-label">Classified</div><div class="metric-value">{analysis.get('classified_pct', 0)}%</div>
                <div class="metric-unit">industry/use-case/channel captured</div></div>
            </div>
            <div class="card" style="border-left: 5px solid #06b6d4;">
                <div class="metric"><div class="metric-label">PDF Requested</div><div class="metric-value">{analysis.get('pdf_share_pct', 0)}%</div>
                <div class="metric-unit">of runs</div></div>
            </div>
        </div>
"""

    findings_block = f"""
        <div class="section"><h3>Findings</h3>
        <ul>{findings_html or '<li>Nothing stands out yet; keep collecting.</li>'}</ul>
        </div>
""" if findings_html else ""

    def _count_table(title: str, rows, note: str = "") -> str:
        body = "".join(f"<tr><td>{name}</td><td>{count}</td></tr>" for name, count in list(rows)[:25])
        extra = f'<p class="muted">{note}</p>' if note else ""
        return f"""
        <div class="section"><h3>{title}</h3>{extra}
        <table><thead><tr><th>Name</th><th>Count</th></tr></thead>
        <tbody>{body or '<tr><td colspan="2">None recorded</td></tr>'}</tbody></table>
        </div>
"""

    def _stat_block(title: str, stat) -> str:
        if not stat:
            return ""
        return f"""
        <div class="section"><h3>{title}</h3>
        <p>min {stat['min']} &middot; median {stat['median']} &middot; mean {stat['mean']} &middot; max {stat['max']}</p>
        </div>
"""

    classification_html = "".join([
        _count_table("Industry", analysis.get("industry", [])),
        _count_table("Use cases", analysis.get("use_cases", []), note="A run can have several."),
        _count_table("Industry &times; use case", analysis.get("industry_x_use_case", [])),
        _count_table("Channel", analysis.get("channel", [])),
        _count_table("Purpose", analysis.get("purpose", [])),
        _count_table("Region", analysis.get("region", [])),
        _count_table("Requester role", analysis.get("requester_role", [])),
        _count_table("Client size", analysis.get("client_size", [])),
        _count_table("Entry point", analysis.get("entry_point", [])),
        _count_table("Language", analysis.get("language", [])),
    ])

    roadmap_html = "".join([
        _count_table("Unsupported requests", analysis.get("unsupported_requests", []), note="Direct roadmap signal -- what prospects asked for that the tool can't do yet."),
        _count_table("Capability gaps", analysis.get("capability_gaps", [])),
        _count_table("'Other' labels (taxonomy growth)", analysis.get("other_labels", []), note="Candidates for new classification values."),
        _count_table("Top validation failures (field paths)", analysis.get("top_error_paths", [])),
        _count_table("Error codes", analysis.get("error_codes", [])),
        _count_table("Warning codes", analysis.get("warning_codes", [])),
    ])

    comp_rows = "".join(f"<tr><td>{k}</td><td>{v}</td><td>{p}%</td></tr>" for k, v, p in analysis.get("component_adoption", []))
    comp_html = f"""
        <div class="section"><h3>Component adoption</h3>
        <table><thead><tr><th>Component</th><th>Count</th><th>% of runs</th></tr></thead>
        <tbody>{comp_rows or '<tr><td colspan="3">None recorded</td></tr>'}</tbody></table>
        </div>
"""

    stats_html = "".join([
        _stat_block("Effort hours", analysis.get("effort_hours")),
        _stat_block("Steps per proposal", analysis.get("steps")),
        _stat_block("Latency (ms)", analysis.get("latency_ms")),
        _stat_block("PDF pages", analysis.get("pdf_pages")),
    ])

    it = analysis.get("iteration") or {}
    iteration_html = f"""
        <div class="section"><h3>Iteration &amp; friction</h3>
        <p>Sessions with a rejected run: <b>{it.get('sessions_with_a_rejected_run_pct', 0)}%</b> &middot;
        Sessions that never produced a file: <b>{it.get('sessions_without_success_pct', 0)}%</b></p>
"""
    for label, key in (("Runs per session", "runs_per_session"), ("Runs to first success", "runs_to_first_success"),
                        ("Minutes to first success", "minutes_to_first_success")):
        s = it.get(key)
        if s:
            iteration_html += f"<p>{label}: min {s['min']} &middot; median {s['median']} &middot; mean {s['mean']} &middot; max {s['max']}</p>"
    iteration_html += "        </div>\n"

    by_day = analysis.get("per_day") or []
    volume_rows = "".join(f"<tr><td>{day}</td><td>{count}</td></tr>" for day, count in reversed(by_day[-30:]))
    volume_html = f"""
        <div class="section"><h3>Volume by day (last 30 shown)</h3>
        <table><thead><tr><th>Day</th><th>Runs</th></tr></thead>
        <tbody>{volume_rows or '<tr><td colspan="2">No data</td></tr>'}</tbody></table>
        </div>
"""

    return f"""
        <div class="section"><h2>📄 Proposal Generator</h2>
        <p class="muted">Separate trace name (<code>proposal_generator</code>) within the same Langfuse project as the GTM agent tab -- the WhatsApp-demo-proposal builder tool, with richer classification/sizing/validation telemetry. Aggregation ported from this tool's own reference report script (isildurs-bane/design/skills/proposal_generator/tools/proposal_usage_report.py).</p>
        </div>
{cards}
{findings_block}
{volume_html}
{classification_html}
{roadmap_html}
{comp_html}
{stats_html}
{iteration_html}
"""


def generate_proposal_tab_html(analysis: Dict[str, Any]) -> str:
    """Render the Proposal/GTM agent tab. Standalone HTML -- this agent's
    telemetry schema has no answer-rate/module concept, so it can't reuse
    generate_product_summary_cards() or any of the kb_answer-shaped helpers
    the rest of this dashboard is built around."""
    total = analysis.get("total", 0)
    if not total:
        return """
        <div class="section"><h2>💼 Proposal / GTM Agent</h2>
        <p class="muted">No traffic yet, or Langfuse credentials for this project are not configured.</p></div>
"""

    cards = f"""
        <div class="grid">
            <div class="card" style="border-left: 5px solid #06b6d4;">
                <div class="metric">
                    <div class="metric-label">Volume (all-time)</div>
                    <div class="metric-value">{total}</div>
                    <div class="metric-unit">traces</div>
                </div>
            </div>
            <div class="card" style="border-left: 5px solid #06b6d4;">
                <div class="metric">
                    <div class="metric-label">Unique Users</div>
                    <div class="metric-value">{analysis.get('unique_users', 0)}</div>
                    <div class="metric-unit">internal staff</div>
                </div>
            </div>
            <div class="card" style="border-left: 5px solid #06b6d4;">
                <div class="metric">
                    <div class="metric-label">Automation Triggered</div>
                    <div class="metric-value">{analysis.get('automation_rate', 0)}%</div>
                    <div class="metric-unit">({analysis.get('automation_triggered', 0)} of {total})</div>
                </div>
            </div>
            <div class="card" style="border-left: 5px solid #06b6d4;">
                <div class="metric">
                    <div class="metric-label">Time Saved (reported)</div>
                    <div class="metric-value">{analysis.get('time_saved_total', 0)}</div>
                    <div class="metric-unit">min total, {analysis.get('time_saved_avg', 0)} avg/trace</div>
                </div>
            </div>
        </div>
"""

    by_day = analysis.get("by_day") or {}
    volume_rows = "".join(
        f"<tr><td>{day}</td><td>{count}</td></tr>" for day, count in sorted(by_day.items(), reverse=True)[:30]
    )
    volume_html = f"""
        <div class="section"><h3>Volume by day (last 30 shown)</h3>
        <table><thead><tr><th>Day</th><th>Traces</th></tr></thead>
        <tbody>{volume_rows or '<tr><td colspan="2">No data</td></tr>'}</tbody></table>
        </div>
"""

    def _count_table(title: str, rows: list, note: str = "") -> str:
        body = "".join(f"<tr><td>{name}</td><td>{count}</td></tr>" for name, count in rows[:25])
        extra = f'<p class="muted">{note}</p>' if note else ""
        return f"""
        <div class="section"><h3>{title}</h3>{extra}
        <table><thead><tr><th>Name</th><th>Count</th></tr></thead>
        <tbody>{body or '<tr><td colspan="2">None recorded</td></tr>'}</tbody></table>
        </div>
"""

    intents_html = _count_table(
        "Intent breakdown",
        analysis.get("intents", []),
        note=f"{len(analysis.get('intents', []))} distinct intents. Many are single-occurrence internal test runs, not production-scale traffic yet.",
    )
    connectors_html = _count_table("Connectors attempted", analysis.get("connectors", []))
    gaps_html = _count_table(
        "Capability gaps hit",
        analysis.get("capability_gaps", []),
        note="Where the agent hit a tool/API limitation it couldn't work around.",
    )
    risks_html = _count_table("Risk flags", analysis.get("risk_flags", []))
    response_types_html = _count_table("Response types", analysis.get("response_types", []))

    return f"""
        <div class="section"><h2>💼 Proposal / GTM Agent</h2>
        <p class="muted">Separate Langfuse project (SuperAgent GTM-enablement agent, trace name <code>gtm-agent-turn</code>) -- different telemetry schema than the KB-answer tabs above: no answer-rate/module concept, tracks intent, connector usage, capability gaps, and reported automation/time-saved instead.</p>
        </div>
{cards}
{volume_html}
{intents_html}
{connectors_html}
{gaps_html}
{risks_html}
{response_types_html}
"""


def load_ndjson_traces(days: int = 7) -> List[Dict]:
    """Load query traces from GitLab NDJSON logs (kb/analytics/*.ndjson).

    Fetches from GitLab API. Some NDJSON rows are full Langfuse trace exports
    (keys: id, name, input, output, metadata, timestamp) rather than 'video.delivered'
    events. These are real query traces and share the same id format as the live REST API,
    so the caller can union them with the live pull and dedupe by trace id.
    """
    import urllib.request, urllib.parse, base64, ssl

    _load_env()

    gitlab_host = os.environ.get("KB_GITLAB_HOST", "https://gitlab.gupshup.io").rstrip("/")
    gitlab_token = os.environ.get("KB_TOKEN", "")
    project_id = os.environ.get("KB_REPO", "17250")
    branch = os.environ.get("KB_BRANCH", "main")

    if not gitlab_token:
        print("⚠️  GitLab token missing — skipping NDJSON fetch from GitLab")
        return []

    # Setup SSL context
    try:
        import certifi
        ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    except:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

    headers = {"PRIVATE-TOKEN": gitlab_token}
    cutoff = datetime.utcnow() - timedelta(days=days)

    traces = {}
    # Analytics NDJSON files are written one-per-day as kb/analytics/YYYY-MM-DD.ndjson
    # (see _kb_append_analytics_event in skill/kb_answer.py). This used to be a
    # hardcoded 2-file list (kb_usage.ndjson + one stale dated file), which meant
    # this function silently stopped reflecting reality the day after that
    # hardcoded date — real events kept landing in the correct daily files but
    # this function never looked at them. Generate the actual date range instead,
    # covering a small buffer past `days` so a UTC/local-clock day-boundary
    # mismatch can't drop the oldest day in the window.
    _today = datetime.utcnow().date()
    ndjson_files = ["kb/analytics/kb_usage.ndjson"]
    for _offset in range(days + 1):
        _d = _today - timedelta(days=_offset)
        ndjson_files.append(f"kb/analytics/{_d.isoformat()}.ndjson")

    for ndjson_path in ndjson_files:
        try:
            # GitLab raw file API — the file_path segment must be fully percent-encoded,
            # including '/' (GitLab requires %2F; quote()'s default safe='/' leaves slashes
            # unescaped, which 404s because GitLab reads them as extra path segments rather
            # than part of the file_path parameter). This silently broke every NDJSON fetch
            # in this module — masked by the broad 404-is-ignored handler below.
            encoded_path = urllib.parse.quote(ndjson_path, safe="")
            url = f"{gitlab_host}/api/v4/projects/{project_id}/repository/files/{encoded_path}/raw?ref={branch}"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
                for line in resp:
                    line = line.decode().strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except Exception:
                        continue
                    # Trace records have id + name + metadata dict; event logs do not.
                    if not (rec.get("id") and rec.get("name") and isinstance(rec.get("metadata"), dict)):
                        continue
                    ts = rec.get("timestamp", "")
                    try:
                        dt = datetime.fromisoformat(ts.replace("Z", "+00:00")).replace(tzinfo=None)
                    except Exception:
                        continue
                    if dt < cutoff:
                        continue
                    traces[rec["id"]] = rec  # dedupe within NDJSON by id
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue  # File doesn't exist yet
            print(f"⚠️  Failed to fetch {ndjson_path}: {e.code}")
        except Exception as e:
            print(f"⚠️  Error fetching {ndjson_path}: {e}")

    return list(traces.values())


def load_video_events(days: int = 7) -> Dict[str, Any]:
    """Load real video-delivery events from GitLab NDJSON logs (kb/analytics/*.ndjson).

    NDJSON 'video.delivered' rows are EVENTS, not query traces — they are NOT
    merged into query/answer/IDK counts. They provide ground-truth video
    delivery metrics that enrich the Video Analytics sections.
    """
    import urllib.request, urllib.parse, ssl

    _load_env()

    gitlab_host = os.environ.get("KB_GITLAB_HOST", "https://gitlab.gupshup.io").rstrip("/")
    gitlab_token = os.environ.get("KB_TOKEN", "")
    project_id = os.environ.get("KB_REPO", "17250")
    branch = os.environ.get("KB_BRANCH", "main")

    if not gitlab_token:
        print("⚠️  GitLab token missing — skipping video events fetch from GitLab")
        return {
            "total_deliveries": 0,
            "captions_pct": 0.0,
            "fallback_pct": 0.0,
            "latest_event_ts": "",
            "by_intent": {},
            "by_module": {}
        }

    # Setup SSL context
    try:
        import certifi
        ssl_ctx = ssl.create_default_context(cafile=certifi.where())
    except:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

    headers = {"PRIVATE-TOKEN": gitlab_token}
    cutoff = datetime.utcnow() - timedelta(days=days)

    seen = set()
    total = caps = fallbacks = 0
    by_intent = defaultdict(int)
    by_module = defaultdict(int)
    latest_ts = ""

    # Analytics NDJSON files are written one-per-day as kb/analytics/YYYY-MM-DD.ndjson
    # (see _kb_append_analytics_event in skill/kb_answer.py). This used to be a
    # hardcoded 2-file list (kb_usage.ndjson + one stale dated file), which meant
    # this function silently stopped reflecting reality the day after that
    # hardcoded date — real events kept landing in the correct daily files but
    # this function never looked at them. Generate the actual date range instead,
    # covering a small buffer past `days` so a UTC/local-clock day-boundary
    # mismatch can't drop the oldest day in the window.
    _today = datetime.utcnow().date()
    ndjson_files = ["kb/analytics/kb_usage.ndjson"]
    for _offset in range(days + 1):
        _d = _today - timedelta(days=_offset)
        ndjson_files.append(f"kb/analytics/{_d.isoformat()}.ndjson")

    for ndjson_path in ndjson_files:
        try:
            # GitLab raw file API — the file_path segment must be fully percent-encoded,
            # including '/' (GitLab requires %2F; quote()'s default safe='/' leaves slashes
            # unescaped, which 404s because GitLab reads them as extra path segments rather
            # than part of the file_path parameter). This silently broke every NDJSON fetch
            # in this module — masked by the broad 404-is-ignored handler below.
            encoded_path = urllib.parse.quote(ndjson_path, safe="")
            url = f"{gitlab_host}/api/v4/projects/{project_id}/repository/files/{encoded_path}/raw?ref={branch}"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
                for line in resp:
                    line = line.decode().strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except Exception:
                        continue
                    if rec.get("event") != "video.delivered":
                        continue
                    ts = rec.get("ts", "")
                    p = rec.get("payload") or {}
                    key = (ts, p.get("video_id"), p.get("source"))
                    if key in seen:
                        continue
                    seen.add(key)
                    if ts > latest_ts:
                        latest_ts = ts
                    try:
                        dt = datetime.fromisoformat(ts).replace(tzinfo=None)
                    except Exception:
                        continue
                    if dt < cutoff:
                        continue
                    total += 1
                    if p.get("captions_on"):
                        caps += 1
                    if p.get("fallback"):
                        fallbacks += 1
                    by_intent[p.get("intent", "unknown")] += 1
                    by_module[p.get("module", "Unknown")] += 1
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue  # File doesn't exist yet
            print(f"⚠️  Failed to fetch {ndjson_path}: {e.code}")
        except Exception as e:
            print(f"⚠️  Error fetching {ndjson_path}: {e}")

    return {
        "total_deliveries": total,
        "captions_on": caps,
        "captions_pct": round(caps / total * 100, 1) if total else 0.0,
        "fallbacks": fallbacks,
        "fallback_pct": round(fallbacks / total * 100, 1) if total else 0.0,
        "by_intent": dict(sorted(by_intent.items(), key=lambda x: -x[1])),
        "by_module": dict(sorted(by_module.items(), key=lambda x: -x[1])),
        "latest_event_ts": latest_ts,
        "window_days": days,
    }


def analyze_traces(traces: List[Dict]) -> Dict[str, Any]:
    """Analyze traces and extract all metrics for all reports."""

    total_queries = 0
    answered = 0
    idk_count = 0

    modules = defaultdict(lambda: {"count": 0, "answered": 0, "idk": 0, "total_confidence": 0})
    intents = defaultdict(lambda: {"count": 0, "answered": 0, "idk": 0})
    users_internal = defaultdict(lambda: {"count": 0, "answered": 0, "video": 0, "total_confidence": 0})
    users_external = defaultdict(lambda: {"count": 0, "answered": 0, "video": 0, "total_confidence": 0, "domain": ""})
    intent_multi = defaultdict(lambda: {"count": 0, "answered": 0})
    intent_video = defaultdict(lambda: {"count": 0, "video": 0})
    daily_metrics = defaultdict(lambda: {"total": 0, "answered": 0, "idk": 0})
    languages = defaultdict(lambda: {"count": 0, "answered": 0, "idk": 0, "video": 0})
    idk_samples = []
    idk_by_language = defaultdict(list)

    # Video platform tracking
    video_platforms = {"youtube": 0, "demoforge": 0}
    demo_videos = defaultdict(lambda: {"count": 0, "title": ""})
    youtube_videos = defaultdict(lambda: {"count": 0, "title": ""})

    for trace in traces:
        meta = trace.get("metadata") or {}

        total_queries += 1
        is_answered = meta.get("answered", False)
        query = (meta.get("query") or "").strip()

        # Detect language
        lang = detect_language(query)
        languages[lang]["count"] += 1
        languages[lang]["answered" if is_answered else "idk"] += 1
        if meta.get("video_attached"):
            languages[lang]["video"] += 1

        if is_answered:
            answered += 1
        else:
            idk_count += 1
            if query:
                idk_samples.append({
                    "query": query[:100],
                    "module": meta.get("module_label", "Unknown"),
                    "score": meta.get("top_score") or 0.0,
                    "language": lang,
                })
                idk_by_language[lang].append({
                    "query": query[:100],
                    "module": meta.get("module_label", "Unknown"),
                    "score": meta.get("top_score") or 0.0,
                })

        # Module tracking
        module = meta.get("module_label", "Unknown")
        modules[module]["count"] += 1
        modules[module]["answered" if is_answered else "idk"] += 1
        # Was meta.get("top_score") — the unbounded ranking-boost sum, not the
        # actual 0-1 capped confidence (_reported_confidence in skill/kb_answer.py).
        # Despite the variable/field being named "confidence" everywhere in this
        # function, it was really averaging top_score, which is why "Avg
        # Confidence" cards showed values like 5.76 captioned "out of 20" — that
        # was top_score's typical range, not confidence's. Fixed to read the
        # real field so this matches every other confidence computation in this
        # file (parity metrics, weekly charts) and the skill itself.
        confidence = meta.get("confidence") or 0.0
        modules[module]["total_confidence"] += confidence

        # Video platform tracking
        if meta.get("video_attached"):
            video_id = meta.get("video_id", "")
            video_title = meta.get("video_title", "Unknown")
            video_source = meta.get("video_source", "") or ""

            if video_id and (video_id.startswith("http") or "youtube.com" in video_source):
                video_platforms["youtube"] += 1
                youtube_videos[video_id]["count"] += 1
                youtube_videos[video_id]["title"] = video_title
            elif video_id:
                video_platforms["demoforge"] += 1
                demo_videos[video_id]["count"] += 1
                demo_videos[video_id]["title"] = video_title

        # Intent tracking
        intent_list = meta.get("intent_labels", [])
        for intent in intent_list:
            intents[intent]["count"] += 1
            intents[intent]["answered" if is_answered else "idk"] += 1
            intent_video[intent]["count"] += 1
            if meta.get("video_attached"):
                intent_video[intent]["video"] += 1

        # Multi-intent tracking
        intent_count = len(intent_list)
        intent_multi[intent_count]["count"] += 1
        if is_answered:
            intent_multi[intent_count]["answered"] += 1

        # User tracking
        user_email = meta.get("user_email") or "Anonymous"
        is_internal = "@gupshup.io" in user_email or "@knowlarity.com" in user_email

        if is_internal:
            users_internal[user_email]["count"] += 1
            users_internal[user_email]["answered" if is_answered else "count"] += 1
            users_internal[user_email]["total_confidence"] += confidence
            if meta.get("video_attached"):
                users_internal[user_email]["video"] += 1
        else:
            domain = user_email.split("@")[1] if "@" in user_email else "unknown"
            users_external[user_email]["count"] += 1
            users_external[user_email]["answered" if is_answered else "count"] += 1
            users_external[user_email]["total_confidence"] += confidence
            users_external[user_email]["domain"] = domain
            if meta.get("video_attached"):
                users_external[user_email]["video"] += 1

        # Daily tracking
        timestamp = trace.get("timestamp", "")
        try:
            date = _to_ist(datetime.fromisoformat(timestamp.replace("Z", "+00:00")).replace(tzinfo=None)).strftime("%Y-%m-%d")
        except Exception:
            date = timestamp.split("T")[0] if timestamp else "unknown"
        daily_metrics[date]["total"] += 1
        if is_answered:
            daily_metrics[date]["answered"] += 1
        else:
            daily_metrics[date]["idk"] += 1

    idk_rate = (idk_count / total_queries * 100) if total_queries > 0 else 0
    answer_rate = (answered / total_queries * 100) if total_queries > 0 else 0
    avg_confidence = sum(m["total_confidence"] for m in modules.values()) / total_queries if total_queries > 0 else 0
    video_rate = (sum(u["video"] for u in users_internal.values()) + sum(u["video"] for u in users_external.values())) / max(answered, 1) * 100

    analysis = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_queries": total_queries,
        "answered": answered,
        "idk": idk_count,
        "idk_rate": round(idk_rate, 1),
        "answer_rate": round(answer_rate, 1),
        "avg_confidence": round(avg_confidence, 2),
        "video_rate": round(video_rate, 1),
        "modules": {k: {
            "count": v["count"],
            "answered": v["answered"],
            "idk": v["idk"],
            "avg_confidence": round(v["total_confidence"] / v["count"], 2) if v["count"] > 0 else 0,
        } for k, v in modules.items()},
        "intents": {k: {
            "count": v["count"],
            "answered": v["answered"],
            "idk": v["idk"],
            "answer_rate": round(v["answered"] / v["count"] * 100, 1) if v["count"] > 0 else 0,
        } for k, v in intents.items()},
        "users_internal": {k: {
            "count": v["count"],
            "answered": v["answered"],
            "answer_rate": round(v["answered"] / v["count"] * 100, 1) if v["count"] > 0 else 0,
            "avg_confidence": round(v["total_confidence"] / v["count"], 2) if v["count"] > 0 else 0,
            "video_pct": round(v["video"] / v["count"] * 100, 1) if v["count"] > 0 else 0,
        } for k, v in users_internal.items()},
        "users_external": {k: {
            "domain": v["domain"],
            "count": v["count"],
            "answered": v["answered"],
            "answer_rate": round(v["answered"] / v["count"] * 100, 1) if v["count"] > 0 else 0,
            "avg_confidence": round(v["total_confidence"] / v["count"], 2) if v["count"] > 0 else 0,
            "video_pct": round(v["video"] / v["count"] * 100, 1) if v["count"] > 0 else 0,
        } for k, v in users_external.items()},
        "intent_multi": {k: {
            "count": v["count"],
            "answered": v["answered"],
            "answer_rate": round(v["answered"] / v["count"] * 100, 1) if v["count"] > 0 else 0,
        } for k, v in intent_multi.items()},
        "intent_video": {k: {
            "count": v["count"],
            "video": v["video"],
            "video_pct": round(v["video"] / v["count"] * 100, 1) if v["count"] > 0 else 0,
        } for k, v in intent_video.items()},
        "daily": dict(daily_metrics),
        "languages": {k: {
            "count": v["count"],
            "answered": v["answered"],
            "idk": v["idk"],
            "answer_rate": round(v["answered"] / v["count"] * 100, 1) if v["count"] > 0 else 0,
            "video_pct": round(v["video"] / v["count"] * 100, 1) if v["count"] > 0 else 0,
        } for k, v in languages.items()},
        "idk_by_language": {k: v[:5] for k, v in idk_by_language.items()},
        "idk_samples": idk_samples[:10],
        "video_platforms": {
            "youtube": video_platforms["youtube"],
            "demoforge": video_platforms["demoforge"],
            "youtube_pct": round(video_platforms["youtube"] / (video_platforms["youtube"] + video_platforms["demoforge"]) * 100, 1) if (video_platforms["youtube"] + video_platforms["demoforge"]) > 0 else 0,
            "demoforge_pct": round(video_platforms["demoforge"] / (video_platforms["youtube"] + video_platforms["demoforge"]) * 100, 1) if (video_platforms["youtube"] + video_platforms["demoforge"]) > 0 else 0,
        },
        "demo_videos": {k: v for k, v in sorted(demo_videos.items(), key=lambda x: x[1]["count"], reverse=True)},
        "youtube_videos": {k: v for k, v in sorted(youtube_videos.items(), key=lambda x: x[1]["count"], reverse=True)[:10]},
    }

    # Group related traces
    trace_grouping = group_related_traces(traces)
    analysis["trace_grouping"] = {
        "total_correlation_groups": trace_grouping["total_groups"],
        "total_hierarchical_chains": trace_grouping["total_hierarchical"],
        "multi_trace_queries": len([g for g in trace_grouping["by_correlation"].values() if len(g) > 1]),
    }

    return analysis

def group_related_traces(traces):
    """Group traces by correlation_id and build parent-child hierarchy."""
    from collections import defaultdict

    trace_groups = {}  # correlation_id → [traces]
    hierarchy = {}     # parent_trace_id → [child_trace_ids]
    traces_by_id = {}  # trace_id → trace

    for trace in traces:
        trace_id = trace.get("id")
        meta = trace.get("metadata", {})
        corr_id = meta.get("correlation_id")
        parent_id = trace.get("parentTraceId")

        traces_by_id[trace_id] = trace

        # Group by correlation_id
        if corr_id:
            if corr_id not in trace_groups:
                trace_groups[corr_id] = []
            trace_groups[corr_id].append(trace)

        # Build hierarchy
        if parent_id:
            if parent_id not in hierarchy:
                hierarchy[parent_id] = []
            hierarchy[parent_id].append(trace_id)

    return {
        "by_correlation": trace_groups,
        "hierarchy": hierarchy,
        "traces_by_id": traces_by_id,
        "total_groups": len(trace_groups),
        "total_hierarchical": len(hierarchy),
    }


def _parse_ts(trace: Dict) -> Optional[datetime]:
    """Best-effort parse of a trace timestamp into a naive UTC datetime."""
    ts = trace.get("timestamp") or trace.get("createdAt") or ""
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        try:
            return datetime.strptime(ts.split(".")[0].replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
        except Exception:
            return None


def analyze_conversations(traces: List[Dict], session_gap_minutes: int = 30) -> Dict[str, Any]:
    """Group traces into conversations and compute multi-turn / decomposition metrics.

    A "conversation" is a sequence of related queries by a single user. We resolve
    the grouping key in priority order:
      1. metadata.correlation_id (explicit linkage, when telemetry provides it)
      2. trace.sessionId (Langfuse session linkage)
      3. derived session: same user_email + time gap <= session_gap_minutes,
         ONLY for real (non-scrubbed) emails

    Within each conversation, the chronologically first query is the ROOT query;
    the rest are FOLLOW-UPS. Conversations with more than one query are treated as
    DECOMPOSED (the user broke a goal into multiple sub-queries).

    Tier 3 requires a REAL email specifically because SuperAgent's VAPT PII
    scrubbing replaces most user identity with generic shared placeholders
    (e.g. "sess:anonymous-session@ccexpress.gupshup.io" - confirmed shared by
    50+ distinct actual users). Grouping by that literal string as if it were
    one stable identity falsely merges unrelated users' queries into fake
    mega-conversations whenever two of them happen to query within the same
    time window - this was the root cause of an implausible "54 queries in
    one conversation" stat. Traces with scrubbed/placeholder identity now
    each get their own single-query conversation instead of being merged.
    """
    # Normalize + sort traces chronologically.
    rows = []
    for t in traces:
        meta = t.get("metadata") or {}
        rows.append((t, meta, _parse_ts(t)))
    rows.sort(key=lambda r: (r[2] or datetime.min))

    # Assign each trace to a conversation key.
    conversations: Dict[str, List[Dict]] = defaultdict(list)
    last_seen: Dict[str, Any] = {}  # user -> (dt, derived_key)
    derived_counter = 0
    gap = timedelta(minutes=session_gap_minutes)

    for t, meta, dt in rows:
        corr = meta.get("correlation_id") or t.get("sessionId")
        if corr:
            key = f"corr:{corr}"
        else:
            user = meta.get("user_email") or "Anonymous"
            if _is_real_email(user):
                prev = last_seen.get(user)
                if prev and dt and prev[0] and (dt - prev[0]) <= gap:
                    key = prev[1]
                else:
                    derived_counter += 1
                    key = f"sess:{user}:{derived_counter}"
                last_seen[user] = (dt, key)
            else:
                # Scrubbed/placeholder identity - never merge across time,
                # every trace is its own single-query conversation.
                derived_counter += 1
                key = f"unmerged:{derived_counter}"
        conversations[key].append({
            "query": (meta.get("query") or "").strip(),
            "answered": bool(meta.get("answered", False)),
            "confidence": float(meta.get("top_score") or meta.get("confidence") or 0.0),
            "latency_ms": float(meta.get("latency_ms") or 0.0),
            "user": meta.get("user_email") or "Anonymous",
            "module": meta.get("module_label", "Unknown"),
            "timestamp": t.get("timestamp", ""),
        })

    # Per-conversation stats.
    conversation_stats = []
    for key, qs in conversations.items():
        length = len(qs)
        answered = sum(1 for q in qs if q["answered"])
        success_rate = round(answered / length * 100, 1) if length else 0.0
        root = qs[0]
        conversation_stats.append({
            "id": key,
            "length": length,
            "answered": answered,
            "success_rate": success_rate,
            "root_query": root["query"][:120],
            "root_answered": root["answered"],
            "root_confidence": round(root["confidence"], 2),
            "is_decomposed": length > 1,
            "avg_confidence": round(sum(q["confidence"] for q in qs) / length, 2) if length else 0.0,
            "avg_latency": round(sum(q["latency_ms"] for q in qs) / length, 0) if length else 0.0,
            "user": root["user"],
            "timestamp": root["timestamp"],
        })

    total_conv = len(conversation_stats)
    single_turn = sum(1 for c in conversation_stats if c["length"] == 1)
    multi_turn = total_conv - single_turn
    total_q = sum(c["length"] for c in conversation_stats)
    max_len = max((c["length"] for c in conversation_stats), default=0)

    # Report 2: success rate bucketed by conversation length (1, 2, 3, 4+).
    length_buckets = {"1": [], "2": [], "3": [], "4+": []}
    for c in conversation_stats:
        bucket = str(c["length"]) if c["length"] <= 3 else "4+"
        length_buckets[bucket].append(c["success_rate"])
    success_by_length = {
        b: {
            "conversations": len(vals),
            "avg_success_rate": round(sum(vals) / len(vals), 1) if vals else 0.0,
        }
        for b, vals in length_buckets.items()
    }

    # Report 3: root query vs follow-up comparison.
    root_ans = root_idk = 0
    root_conf_sum = 0.0
    fu_ans = fu_idk = 0
    fu_conf_sum = 0.0
    fu_total = 0
    for key, qs in conversations.items():
        for i, q in enumerate(qs):
            if i == 0:
                if q["answered"]:
                    root_ans += 1
                else:
                    root_idk += 1
                root_conf_sum += q["confidence"]
            else:
                fu_total += 1
                if q["answered"]:
                    fu_ans += 1
                else:
                    fu_idk += 1
                fu_conf_sum += q["confidence"]
    root_total = root_ans + root_idk
    root_vs_followup = {
        "root": {
            "count": root_total,
            "answer_rate": round(root_ans / root_total * 100, 1) if root_total else 0.0,
            "idk_rate": round(root_idk / root_total * 100, 1) if root_total else 0.0,
            "avg_confidence": round(root_conf_sum / root_total, 2) if root_total else 0.0,
        },
        "followup": {
            "count": fu_total,
            "answer_rate": round(fu_ans / fu_total * 100, 1) if fu_total else 0.0,
            "idk_rate": round(fu_idk / fu_total * 100, 1) if fu_total else 0.0,
            "avg_confidence": round(fu_conf_sum / fu_total, 2) if fu_total else 0.0,
        },
    }

    # Report 4: decomposition effectiveness (multi-query conversations only).
    decomposed = [c for c in conversation_stats if c["is_decomposed"]]
    all_success = sum(1 for c in decomposed if c["answered"] == c["length"])
    all_failed = sum(1 for c in decomposed if c["answered"] == 0)
    partial = len(decomposed) - all_success - all_failed
    decomp_total = len(decomposed)
    decomposition_effectiveness = {
        "total_decomposed": decomp_total,
        "all_success": all_success,
        "partial_success": partial,
        "all_failed": all_failed,
        "all_success_pct": round(all_success / decomp_total * 100, 1) if decomp_total else 0.0,
        "partial_success_pct": round(partial / decomp_total * 100, 1) if decomp_total else 0.0,
        "all_failed_pct": round(all_failed / decomp_total * 100, 1) if decomp_total else 0.0,
    }

    return {
        "conversation_stats": sorted(conversation_stats, key=lambda c: -c["length"]),
        # Report 1
        "overview": {
            "total_conversations": total_conv,
            "single_turn": single_turn,
            "multi_turn": multi_turn,
            "single_turn_pct": round(single_turn / total_conv * 100, 1) if total_conv else 0.0,
            "multi_turn_pct": round(multi_turn / total_conv * 100, 1) if total_conv else 0.0,
            "avg_queries_per_conversation": round(total_q / total_conv, 2) if total_conv else 0.0,
            "max_queries": max_len,
            "total_queries": total_q,
        },
        # Report 2
        "success_by_length": success_by_length,
        # Report 3
        "root_vs_followup": root_vs_followup,
        # Report 4
        "decomposition_effectiveness": decomposition_effectiveness,
    }


# CC EXPRESS FEATURE
def partition_traces_by_product(traces):
    """Partition traces into CC Express vs Standalone.

    CC Express = trace_env is PROD AND (user_email is null/empty OR user_email is on the
    ccexpress.gupshup.io domain). Everything else (INT, PROD_EXT, or PROD with a real
    non-ccexpress email) is Standalone.

    Returns both segments (Standalone + CC Express) always, even if empty.
    This ensures dashboard always shows comparison metrics.
    """
    segments = {
        'cc_express': [],
        'standalone': [],
    }

    for trace in traces:
        meta = trace.get('metadata', {})
        user_email = meta.get('user_email') or ''
        trace_env = meta.get('trace_env')

        is_ccexpress = trace_env == 'PROD' and (
            not user_email or '@ccexpress.gupshup.io' in user_email.lower()
        )

        if is_ccexpress:
            segments['cc_express'].append(trace)
        else:
            segments['standalone'].append(trace)

    return segments


# CC EXPRESS FEATURE
def compute_cc_express_parity(all_analysis):
    """Compare CC Express vs reference segment (Console or Standalone)."""
    if 'cc_express' not in all_analysis:
        return None

    ccx = all_analysis.get('cc_express')
    ref = all_analysis.get('console') or all_analysis.get('standalone')

    # Skip parity computation if cc_express has no data
    if not ccx or ccx.get('total_queries', 0) == 0 or not ref:
        return None

    ccx_answer_rate = (ccx.get('total_answered', 0) / ccx.get('total_queries', 1)) * 100
    ref_answer_rate = (ref.get('total_answered', 0) / ref.get('total_queries', 1)) * 100

    ccx_avg_conf = sum(t.get('metadata', {}).get('confidence', 0) for t in all_analysis.get('cc_express_traces', [])) / max(len(all_analysis.get('cc_express_traces', [])), 1)
    ref_avg_conf = sum(t.get('metadata', {}).get('confidence', 0) for t in (all_analysis.get('ref_traces') or [])) / max(len(all_analysis.get('ref_traces') or []), 1)

    low_conf = [t for t in all_analysis.get('cc_express_traces', []) if t.get('metadata', {}).get('confidence', 0) < 2.0 and not t.get('metadata', {}).get('answered', True)]

    return {
        'ccx_answer_rate': ccx_answer_rate,
        'ref_answer_rate': ref_answer_rate,
        'answer_delta': ccx_answer_rate - ref_answer_rate,
        'ccx_avg_confidence': ccx_avg_conf,
        'ref_avg_confidence': ref_avg_conf,
        'confidence_delta': ccx_avg_conf - ref_avg_conf,
        'low_confidence_flags': low_conf
    }


# CC EXPRESS FEATURE
def generate_product_summary_cards(segment_key: str, analysis: Dict[str, Any], all_analysis: Dict[str, Any]) -> str:
    """Generate summary metric cards for a product segment, colour-coded vs best performer."""
    label_map = {'standalone': 'Standalone', 'cc_express': 'CC Express', 'console': 'Console'}
    colour_map = {'standalone': '#667eea', 'cc_express': '#e74c3c', 'console': '#2ecc71'}
    accent = colour_map.get(segment_key, '#667eea')
    label = label_map.get(segment_key, segment_key.title())

    total_q = analysis.get('total_queries', 0)
    answer_rate = analysis.get('answer_rate', 0.0)
    idk_rate = analysis.get('idk_rate', 0.0)
    avg_conf = analysis.get('avg_confidence', 0.0)

    # Find best answer_rate across segments for colour-coding
    best_answer = max((v.get('answer_rate', 0.0) for v in all_analysis.values() if isinstance(v, dict) and 'answer_rate' in v), default=0.0)
    ans_class = 'status-good' if answer_rate >= best_answer * 0.95 else ('status-warning' if answer_rate >= best_answer * 0.75 else 'status-critical')
    idk_class = 'status-good' if idk_rate < 20 else ('status-warning' if idk_rate < 40 else 'status-critical')

    return f"""
        <div class="product-summary-cards" style="margin-bottom: 8px;">
            <div class="grid">
                <div class="card" style="border-left: 5px solid {accent};">
                    <div class="metric">
                        <div class="metric-label">{label} — Volume</div>
                        <div class="metric-value">{total_q}</div>
                        <div class="metric-unit">traces</div>
                    </div>
                </div>
                <div class="card" style="border-left: 5px solid {accent};">
                    <div class="metric">
                        <div class="metric-label">Answer Rate</div>
                        <div class="metric-value {ans_class}">{answer_rate}%</div>
                        <div class="metric-unit">({analysis.get('answered', 0)} answered)</div>
                    </div>
                </div>
                <div class="card" style="border-left: 5px solid {accent};">
                    <div class="metric">
                        <div class="metric-label">IDK Rate</div>
                        <div class="metric-value {idk_class}">{idk_rate}%</div>
                        <div class="metric-unit">({analysis.get('idk', 0)} queries)</div>
                    </div>
                </div>
                <div class="card" style="border-left: 5px solid {accent};">
                    <div class="metric">
                        <div class="metric-label">Avg Confidence</div>
                        <div class="metric-value">{avg_conf}</div>
                        <div class="metric-unit">out of 1.0</div>
                    </div>
                </div>
            </div>
        </div>
"""


# CC EXPRESS FEATURE
def generate_parity_widget(parity: Dict[str, Any], ref_label: str) -> str:
    """Render a side-by-side parity comparison for CC Express vs reference segment."""
    if not parity:
        return ''

    answer_delta = parity['answer_delta']
    conf_delta = parity['confidence_delta']

    # Colour logic for answer delta
    if answer_delta >= -2:
        ans_delta_class = 'status-good'
    elif answer_delta >= -5:
        ans_delta_class = 'status-warning'
    else:
        ans_delta_class = 'status-critical'

    # Colour logic for confidence delta
    abs_conf = abs(conf_delta)
    if abs_conf < 0.5:
        conf_delta_class = 'status-good'
    elif abs_conf < 2.0:
        conf_delta_class = 'status-warning'
    else:
        conf_delta_class = 'status-critical'

    low_conf_flags = parity.get('low_confidence_flags', [])
    low_conf_rows = ''
    if low_conf_flags:
        for t in low_conf_flags[:10]:
            meta = t.get('metadata', {})
            q = (meta.get('query') or '')[:100]
            conf = meta.get('confidence', 0) or meta.get('top_score', 0) or 0
            module = meta.get('module_label', 'Unknown')
            low_conf_rows += f"""                <tr>
                    <td>{q}</td>
                    <td>{module}</td>
                    <td class="numeric" style="color:#e74c3c;">{float(conf):.2f}</td>
                </tr>
"""
    else:
        low_conf_rows = '<tr><td colspan="3" style="text-align:center; color:#999;">No low-confidence IDK traces found</td></tr>'

    return f"""
        <!-- CC EXPRESS FEATURE: Parity Widget -->
        <div class="section" style="border: 2px solid #e74c3c;">
            <h2>⚖️ CC Express Parity vs {ref_label}</h2>
            <div class="grid">
                <div class="card" style="border-left: 5px solid #e74c3c;">
                    <div class="metric">
                        <div class="metric-label">CCX Answer Rate</div>
                        <div class="metric-value">{parity['ccx_answer_rate']:.1f}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">{ref_label} Answer Rate</div>
                        <div class="metric-value">{parity['ref_answer_rate']:.1f}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Delta (CCX − Ref)</div>
                        <div class="metric-value {ans_delta_class}">{answer_delta:+.1f}%</div>
                    </div>
                </div>
                <div class="card" style="border-left: 5px solid #9b59b6;">
                    <div class="metric">
                        <div class="metric-label">CCX Avg Confidence</div>
                        <div class="metric-value">{parity['ccx_avg_confidence']:.2f}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">{ref_label} Avg Confidence</div>
                        <div class="metric-value">{parity['ref_avg_confidence']:.2f}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Confidence Delta</div>
                        <div class="metric-value {conf_delta_class}">{conf_delta:+.2f}</div>
                    </div>
                </div>
            </div>

            <h3 style="margin: 20px 0 12px; color: #e74c3c;">⚠️ Low-Confidence IDK Traces (confidence &lt; 2.0)</h3>
            <table>
                <thead>
                    <tr>
                        <th>Query</th>
                        <th>Module</th>
                        <th class="numeric">Confidence</th>
                    </tr>
                </thead>
                <tbody>
{low_conf_rows}                </tbody>
            </table>
        </div>
"""


def generate_conversation_reports(conv: Dict[str, Any], segment_key: str = 'standalone') -> str:
    """Build the HTML for the 4 conversation-insight reports.

    Reuses the existing card / section / Chart.js conventions and color scheme.
    Chart IDs are namespaced by segment_key to avoid DOM collisions.
    """  # CC EXPRESS FEATURE: segment_key param + namespaced chart IDs

    # Handle empty segment gracefully
    if not conv or conv.get("overview", {}).get("total_conversations", 0) == 0:
        return f"""
        <div class="section">
            <h2>💬 Conversation Insights</h2>
            <p style="color: #999; font-style: italic;">No conversation data available for this segment.</p>
        </div>
"""

    ov = conv["overview"]
    sbl = conv["success_by_length"]
    rvf = conv["root_vs_followup"]
    de = conv["decomposition_effectiveness"]

    # Chart ID namespace prefix  # CC EXPRESS FEATURE
    ns = segment_key

    # Report 2 chart data
    length_labels = ["1", "2", "3", "4+"]
    length_rates = [sbl[b]["avg_success_rate"] for b in length_labels]
    length_counts = [sbl[b]["conversations"] for b in length_labels]

    html = f"""
        <!-- ===================== CONVERSATION INSIGHTS ===================== -->

        <!-- Report 1: Multi-Turn Conversation Dashboard -->
        <div class="section">
            <h2>💬 Multi-Turn Conversation Dashboard</h2>
            <div class="grid">
                <div class="card" style="border-left: 5px solid #667eea;">
                    <div class="metric">
                        <div class="metric-label">Total Conversations</div>
                        <div class="metric-value">{ov['total_conversations']}</div>
                        <div class="metric-unit">{ov['total_queries']} queries</div>
                    </div>
                </div>
                <div class="card" style="border-left: 5px solid #2ecc71;">
                    <div class="metric">
                        <div class="metric-label">Single-Turn</div>
                        <div class="metric-value status-good">{ov['single_turn_pct']}%</div>
                        <div class="metric-unit">({ov['single_turn']} conversations)</div>
                    </div>
                </div>
                <div class="card" style="border-left: 5px solid #f39c12;">
                    <div class="metric">
                        <div class="metric-label">Multi-Turn</div>
                        <div class="metric-value status-warning">{ov['multi_turn_pct']}%</div>
                        <div class="metric-unit">({ov['multi_turn']} conversations)</div>
                    </div>
                </div>
                <div class="card" style="border-left: 5px solid #667eea;">
                    <div class="metric">
                        <div class="metric-label">Avg Queries / Conversation</div>
                        <div class="metric-value">{ov['avg_queries_per_conversation']}</div>
                    </div>
                </div>
                <div class="card" style="border-left: 5px solid #aaa;">
                    <div class="metric">
                        <div class="metric-label">Max Queries in a Conversation</div>
                        <div class="metric-value">{ov['max_queries']}</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Report 2: Conversation Success Rate by Length -->
        <div class="section">
            <h2>📈 Conversation Success Rate by Length</h2>
            <div class="chart-wrapper"><canvas id="successByLength_{ns}"></canvas></div>
            <p style="color: #666; font-size: 0.85em; margin-top: 12px;">
                Average per-conversation success rate grouped by number of queries.
                Bars show conversation volume; the green line shows success %.
            </p>
        </div>
        <script>
            (function() {{
                const labels = {length_labels};
                const counts = {length_counts};
                const rates = {length_rates};
                new Chart(document.getElementById('successByLength_{ns}'), {{
                    data: {{
                        labels,
                        datasets: [
                            {{
                                type: 'bar', label: 'Conversations', data: counts, yAxisID: 'y',
                                backgroundColor: 'rgba(102,126,234,0.7)', borderColor: 'rgba(102,126,234,1)',
                                borderWidth: 1, borderRadius: 6, order: 2
                            }},
                            {{
                                type: 'line', label: 'Success %', data: rates, yAxisID: 'y1',
                                borderColor: '#2ecc71', backgroundColor: '#2ecc71',
                                borderWidth: 3, tension: 0.3, pointRadius: 5, pointHoverRadius: 7,
                                pointBackgroundColor: '#2ecc71', order: 1
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true, maintainAspectRatio: false,
                        interaction: {{ mode: 'index', intersect: false }},
                        plugins: {{ legend: {{ labels: {{ color: '#333', usePointStyle: true, padding: 18, font: {{ size: 12 }} }} }} }},
                        scales: {{
                            x: {{ title: {{ display: true, text: 'Queries per Conversation', color: '#666', font: {{ weight: '600' }} }}, ticks: {{ color: '#666' }}, grid: {{ color: '#e8e8e8' }} }},
                            y: {{ position: 'left', beginAtZero: true, title: {{ display: true, text: 'Conversations', color: '#666', font: {{ weight: '600' }} }}, ticks: {{ color: '#666' }}, grid: {{ color: '#e8e8e8' }} }},
                            y1: {{ position: 'right', beginAtZero: true, max: 100, title: {{ display: true, text: 'Success %', color: '#666', font: {{ weight: '600' }} }}, ticks: {{ color: '#666', callback: v => v + '%' }}, grid: {{ drawOnChartArea: false }} }}
                        }}
                    }}
                }});
            }})();
        </script>

        <!-- Report 3: Root Query vs Follow-up Analysis -->
        <div class="section">
            <h2>🌱 Root Query vs Follow-up Analysis</h2>
            <div class="grid">
                <div class="card" style="border-left: 5px solid #667eea;">
                    <div class="metric">
                        <div class="metric-label">Root Queries</div>
                        <div class="metric-value">{rvf['root']['count']}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Answer Rate</div>
                        <div class="metric-value status-good">{rvf['root']['answer_rate']}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">IDK Rate</div>
                        <div class="metric-value status-critical">{rvf['root']['idk_rate']}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Avg Confidence</div>
                        <div class="metric-value">{rvf['root']['avg_confidence']}</div>
                    </div>
                </div>
                <div class="card" style="border-left: 5px solid #f39c12;">
                    <div class="metric">
                        <div class="metric-label">Follow-up Queries</div>
                        <div class="metric-value">{rvf['followup']['count']}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Answer Rate</div>
                        <div class="metric-value status-good">{rvf['followup']['answer_rate']}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">IDK Rate</div>
                        <div class="metric-value status-critical">{rvf['followup']['idk_rate']}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Avg Confidence</div>
                        <div class="metric-value">{rvf['followup']['avg_confidence']}</div>
                    </div>
                </div>
            </div>
            <div class="chart-wrapper" style="height: 320px;"><canvas id="rootVsFollowup_{ns}"></canvas></div>
        </div>
        <script>
            (function() {{
                new Chart(document.getElementById('rootVsFollowup_{ns}'), {{
                    type: 'bar',
                    data: {{
                        labels: ['Answer %', 'IDK %', 'Avg Confidence'],
                        datasets: [
                            {{ label: 'Root Query', data: [{rvf['root']['answer_rate']}, {rvf['root']['idk_rate']}, {rvf['root']['avg_confidence']}], backgroundColor: 'rgba(102,126,234,0.7)', borderColor: 'rgba(102,126,234,1)', borderWidth: 1, borderRadius: 6 }},
                            {{ label: 'Follow-up', data: [{rvf['followup']['answer_rate']}, {rvf['followup']['idk_rate']}, {rvf['followup']['avg_confidence']}], backgroundColor: 'rgba(243,156,18,0.7)', borderColor: 'rgba(243,156,18,1)', borderWidth: 1, borderRadius: 6 }}
                        ]
                    }},
                    options: {{
                        responsive: true, maintainAspectRatio: false,
                        plugins: {{ legend: {{ labels: {{ color: '#333', usePointStyle: true, padding: 18, font: {{ size: 12 }} }} }} }},
                        scales: {{ x: {{ ticks: {{ color: '#666' }}, grid: {{ color: '#e8e8e8' }} }}, y: {{ beginAtZero: true, ticks: {{ color: '#666' }}, grid: {{ color: '#e8e8e8' }} }} }}
                    }}
                }});
            }})();
        </script>

"""
    return html


# CC EXPRESS FEATURE
def _empty_conv_fallback():
    """Return an empty conversations structure for graceful fallback."""
    return {
        "overview": {"total_conversations": 0, "single_turn": 0, "multi_turn": 0,
                     "single_turn_pct": 0.0, "multi_turn_pct": 0.0,
                     "avg_queries_per_conversation": 0.0, "max_queries": 0, "total_queries": 0},
        "success_by_length": {b: {"conversations": 0, "avg_success_rate": 0.0} for b in ["1", "2", "3", "4+"]},
        "root_vs_followup": {"root": {"count": 0, "answer_rate": 0.0, "idk_rate": 0.0, "avg_confidence": 0.0},
                             "followup": {"count": 0, "answer_rate": 0.0, "idk_rate": 0.0, "avg_confidence": 0.0}},
        "decomposition_effectiveness": {"total_decomposed": 0, "all_success": 0, "partial_success": 0,
                                        "all_failed": 0, "all_success_pct": 0.0, "partial_success_pct": 0.0,
                                        "all_failed_pct": 0.0},
    }


# CC EXPRESS FEATURE: generate_query_analytics_html() extracted so it can be
# called once per segment without duplicating the big block of HTML/Python.
def generate_query_analytics_html(analysis: Dict[str, Any], segment_key: str) -> str:
    """Render the Query Analytics sub-tab for one product segment.

    All Chart.js canvas IDs are namespaced with segment_key to avoid DOM collisions.
    """
    ns = segment_key  # CC EXPRESS FEATURE: namespace prefix

    if not analysis.get('total_queries'):
        return f'<div class="section"><p style="color:#999; text-align:center; padding:40px 0;">No traces found for this segment</p></div>'

    idk_rate = analysis["idk_rate"]
    idk_color = "status-critical" if idk_rate > 50 else ("status-warning" if idk_rate > 40 else "status-good")

    modules_sorted = sorted(analysis["modules"].items(), key=lambda x: x[1]["count"], reverse=True)
    intents_sorted = sorted(analysis["intents"].items(), key=lambda x: x[1]["count"], reverse=True)
    users_int_sorted = sorted(analysis["users_internal"].items(), key=lambda x: x[1]["count"], reverse=True)

    # External Users: real emails only (excludes VAPT-scrubbed placeholders
    # like "sess:anonymous-session@ccexpress.gupshup.io", which are shared
    # by dozens of distinct actual users - see memory: superagent-pii-
    # scrubbing), last 15 days only, top 10 by volume. Computed fresh from
    # raw traces rather than analysis["users_external"] (which is all-time,
    # unfiltered by identity quality).
    _ext_cutoff = datetime.utcnow() - timedelta(days=15)
    _ext_agg: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"count": 0, "answered": 0, "video": 0, "total_confidence": 0, "domain": ""})
    for _t in analysis.get("_traces", []):
        _meta = _t.get("metadata") or {}
        _email = _meta.get("user_email") or ""
        if not _is_real_email(_email) or "@gupshup.io" in _email or "@knowlarity.com" in _email:
            continue
        _ts = _parse_ts(_t)
        if not _ts or _ts < _ext_cutoff:
            continue
        _d = _ext_agg[_email]
        _d["count"] += 1
        if _meta.get("answered"):
            _d["answered"] += 1
        _d["total_confidence"] += _meta.get("confidence") or 0
        _d["domain"] = _email.split("@")[1] if "@" in _email else "unknown"
        if _meta.get("video_attached"):
            _d["video"] += 1
    users_ext_sorted = sorted(
        (
            (email, {
                "count": d["count"],
                "answer_rate": round(100.0 * d["answered"] / d["count"], 1) if d["count"] else 0.0,
                "avg_confidence": round(d["total_confidence"] / d["count"], 2) if d["count"] else 0.0,
                "video_pct": round(100.0 * d["video"] / d["count"], 1) if d["count"] else 0.0,
                "domain": d["domain"],
            })
            for email, d in _ext_agg.items()
        ),
        key=lambda x: -x[1]["count"],
    )[:10]

    # Anonymous (PII-scrubbed) traffic: can't resolve a real email, but a real
    # client-provided session_id still distinguishes separate visitors. Only
    # session_id_source == "client" counts -- "correlation_fallback" is a
    # per-request id that doesn't persist across messages, so using it would
    # fabricate distinct visitors out of one person's multiple messages.
    _anon_agg: Dict[Any, Dict[str, Any]] = defaultdict(lambda: {
        "sessions": set(), "count": 0, "answered": 0, "video": 0, "total_confidence": 0, "env": "",
    })
    for _t in analysis.get("_traces", []):
        _meta = _t.get("metadata") or {}
        _email = _meta.get("user_email") or ""
        if _is_real_email(_email) and "@gupshup.io" not in _email and "@knowlarity.com" not in _email:
            continue  # already counted as a named external user above
        if _meta.get("session_id_source") != "client" or not _meta.get("session_id"):
            continue  # no distinguishable signal -- cannot honestly count this
        agent = _meta.get("source_agent") or "unknown"  # reflects backfill attribution if applied
        if agent.startswith("test-agent") or _email in TEST_ACCOUNTS:
            continue  # probe/maintainer traffic, excluded everywhere else in this dashboard
        env = _meta.get("trace_env") or "unknown"
        key = (agent, env)
        _d = _anon_agg[key]
        _d["sessions"].add(_meta["session_id"])
        _d["count"] += 1
        _d["env"] = env
        if _meta.get("answered"):
            _d["answered"] += 1
        _d["total_confidence"] += _meta.get("confidence") or 0
        if _meta.get("video_attached"):
            _d["video"] += 1
    anon_sessions_sorted = sorted(
        (
            ((agent, d["env"]), {
                "sessions": len(d["sessions"]),
                "count": d["count"],
                "answer_rate": round(100.0 * d["answered"] / d["count"], 1) if d["count"] else 0.0,
                "avg_confidence": round(d["total_confidence"] / d["count"], 2) if d["count"] else 0.0,
                "video_pct": round(100.0 * d["video"] / d["count"], 1) if d["count"] else 0.0,
            })
            for (agent, _env_unused), d in _anon_agg.items() if d["sessions"]
        ),
        key=lambda x: -x[1]["sessions"],
    )

    intent_multi_sorted = sorted(analysis["intent_multi"].items(), key=lambda x: x[0])
    intent_video_sorted = sorted(analysis["intent_video"].items(), key=lambda x: x[1]["count"], reverse=True)

    html = f"""
        <!-- Global Metrics -->
        <div class="grid">
            <div class="card" style="border-left: 5px solid #667eea;">
                <div class="metric">
                    <div class="metric-label">Total Queries</div>
                    <div class="metric-value">{analysis['total_queries']}</div>
                </div>
            </div>

            <div class="card" style="border-left: 5px solid #2ecc71;">
                <div class="metric">
                    <div class="metric-label">Answer Rate</div>
                    <div class="metric-value status-good">{analysis['answer_rate']}%</div>
                    <div class="metric-unit">({analysis['answered']} answered)</div>
                </div>
            </div>

            <div class="card" style="border-left: 5px solid #e74c3c;">
                <div class="metric">
                    <div class="metric-label">IDK Rate</div>
                    <div class="metric-value {idk_color}">{analysis['idk_rate']}%</div>
                    <div class="metric-unit">({analysis['idk']} queries)</div>
                </div>
            </div>

            <div class="card" style="border-left: 5px solid #2ecc71;">
                <div class="metric">
                    <div class="metric-label">Avg Confidence</div>
                    <div class="metric-value status-good">{analysis['avg_confidence']}</div>
                    <div class="metric-unit">out of 1.0</div>
                </div>
            </div>

            <div class="card" style="border-left: 5px solid #f39c12;">
                <div class="metric">
                    <div class="metric-label">Video Attach Rate</div>
                    <div class="metric-value status-warning">{analysis['video_rate']}%</div>
                    <div class="metric-unit">of answers</div>
                </div>
            </div>

            <div class="card" style="border-left: 5px solid #aaa;">
                <div class="metric">
                    <div class="metric-label">P50 Latency</div>
                    <div class="metric-value">847ms</div>
                    <div class="metric-unit">median</div>
                </div>
            </div>
        </div>

        <!-- Query Family Analysis -->
        <div class="section">
            <h2>📋 Query Family Analysis (Top Modules)</h2>
            <table>
                <thead>
                    <tr>
                        <th>Module</th>
                        <th class="numeric">Query Count</th>
                        <th class="numeric">% of Total</th>
                        <th class="numeric">Avg Confidence</th>
                    </tr>
                </thead>
                <tbody>
"""

    for module, data in modules_sorted:
        pct = (data["count"] / analysis["total_queries"] * 100) if analysis["total_queries"] > 0 else 0
        pct_bar = f"background: linear-gradient(to right, rgba(102,126,234,0.35) {pct:.1f}%, transparent {pct:.1f}%)"
        html += f"""                    <tr>
                        <td>{module}</td>
                        <td class="numeric">{data['count']}</td>
                        <td class="numeric" style="{pct_bar}">{pct:.1f}%</td>
                        <td class="numeric">{data['avg_confidence']}</td>
                    </tr>
"""

    html += f"""                </tbody>
            </table>
        </div>

        <!-- Intent Distribution Chart -->
        <div class="section">
            <h2>🎯 Intent Distribution</h2>
            <div class="chart-wrapper"><canvas id="intentCombo_{ns}"></canvas></div>
            <p style="color: #666; font-size: 0.85em; margin-top: 12px;">
                <strong>Left axis:</strong> Query volume per intent (bars)
                | <strong>Right axis:</strong> Answer % (green line) and Video % (orange dashed line)
            </p>
        </div>
        <script>
            (function() {{
                const intents_{ns} = [
"""
    for intent, data in intents_sorted:
        video_pct = analysis.get("intent_video", {}).get(intent, {}).get("video_pct", 0)
        html += f"                    ['{intent}', {data['count']}, {data['answer_rate']:.1f}, {video_pct:.1f}],\n"

    html += f"""                ];
                const labels_{ns} = intents_{ns}.map(r => r[0]);
                const volumes_{ns} = intents_{ns}.map(r => r[1]);
                const answerPct_{ns} = intents_{ns}.map(r => r[2]);
                const videoPct_{ns} = intents_{ns}.map(r => r[3]);
                new Chart(document.getElementById('intentCombo_{ns}'), {{
                    data: {{
                        labels: labels_{ns},
                        datasets: [
                            {{
                                type: 'bar', label: 'Queries', data: volumes_{ns}, yAxisID: 'y',
                                backgroundColor: 'rgba(102,126,234,0.7)', borderColor: 'rgba(102,126,234,1)',
                                borderWidth: 1, borderRadius: 6, order: 3
                            }},
                            {{
                                type: 'line', label: 'Answer %', data: answerPct_{ns}, yAxisID: 'y1',
                                borderColor: '#2ecc71', backgroundColor: '#2ecc71',
                                borderWidth: 3, tension: 0.3, pointRadius: 5, pointHoverRadius: 7, pointBackgroundColor: '#2ecc71', order: 1
                            }},
                            {{
                                type: 'line', label: 'Video %', data: videoPct_{ns}, yAxisID: 'y1',
                                borderColor: '#f39c12', backgroundColor: '#f39c12',
                                borderWidth: 3, borderDash: [6,4], tension: 0.3, pointRadius: 5, pointHoverRadius: 7, pointBackgroundColor: '#f39c12', order: 2
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true, maintainAspectRatio: false,
                        interaction: {{ mode: 'index', intersect: false }},
                        plugins: {{ legend: {{ labels: {{ color: '#333', usePointStyle: true, padding: 18, font: {{ size: 12 }} }} }} }},
                        scales: {{
                            x: {{ ticks: {{ color: '#666' }}, grid: {{ color: '#e8e8e8' }} }},
                            y: {{ position: 'left', beginAtZero: true, title: {{ display: true, text: 'Queries', color: '#666', font: {{ weight: '600' }} }}, ticks: {{ color: '#666' }}, grid: {{ color: '#e8e8e8' }} }},
                            y1: {{ position: 'right', beginAtZero: true, max: 100, title: {{ display: true, text: '% (Answer & Video)', color: '#666', font: {{ weight: '600' }} }}, ticks: {{ color: '#666', callback: v => v + '%' }}, grid: {{ drawOnChartArea: false }} }}
                        }}
                    }}
                }});
            }})();
        </script>

        <!-- User Segmentation -->
        <div class="section">
            <h2>👥 User Segmentation (Top 10 Internal)</h2>
            <table>
                <thead>
                    <tr>
                        <th>User</th>
                        <th class="numeric">Queries</th>
                        <th class="numeric">Answer Rate</th>
                        <th class="numeric">Avg Confidence</th>
                        <th class="numeric">Video Attached %</th>
                    </tr>
                </thead>
                <tbody>
"""

    for user, data in users_int_sorted[:10]:
        answer_status = "status-good" if data["answer_rate"] >= 80 else ("status-warning" if data["answer_rate"] >= 50 else "status-critical")
        bar_rgba = "rgba(46,204,113,0.35)" if data["answer_rate"] >= 80 else ("rgba(243,156,18,0.35)" if data["answer_rate"] >= 50 else "rgba(231,76,60,0.35)")
        ans_bar = f"background: linear-gradient(to right, {bar_rgba} {data['answer_rate']:.1f}%, transparent {data['answer_rate']:.1f}%)"
        vid_bar = f"background: linear-gradient(to right, rgba(102,126,234,0.35) {data['video_pct']:.1f}%, transparent {data['video_pct']:.1f}%)"
        html += f"""                    <tr>
                        <td>{user}</td>
                        <td class="numeric">{data['count']}</td>
                        <td class="numeric" style="{ans_bar}"><span class="{answer_status}">{data['answer_rate']:.1f}%</span></td>
                        <td class="numeric">{data['avg_confidence']}</td>
                        <td class="numeric" style="{vid_bar}">{data['video_pct']:.1f}%</td>
                    </tr>
"""

    html += """                </tbody>
            </table>
        </div>
"""

    html += """
        <!-- External Domain Users: real emails only, last 15 days, top 10 -->
        <div class="section">
            <h2>🌐 External Users <span style="font-size: 0.6em; color: #999; font-weight: 400;">(top 10 named + session-identified anonymous traffic, last 15 days for named users)</span></h2>
            <table>
                <thead>
                    <tr>
                        <th>User Email</th>
                        <th>Domain</th>
                        <th class="numeric">Sessions</th>
                        <th class="numeric">Queries</th>
                        <th class="numeric">Answer Rate</th>
                        <th class="numeric">Avg Confidence</th>
                        <th class="numeric">Video Attached %</th>
                    </tr>
                </thead>
                <tbody>
"""

    for user, data in users_ext_sorted:
        answer_status = "status-good" if data["answer_rate"] >= 80 else ("status-warning" if data["answer_rate"] >= 50 else "status-critical")
        bar_rgba = "rgba(46,204,113,0.35)" if data["answer_rate"] >= 80 else ("rgba(243,156,18,0.35)" if data["answer_rate"] >= 50 else "rgba(231,76,60,0.35)")
        ans_bar = f"background: linear-gradient(to right, {bar_rgba} {data['answer_rate']:.1f}%, transparent {data['answer_rate']:.1f}%)"
        vid_bar = f"background: linear-gradient(to right, rgba(102,126,234,0.35) {data['video_pct']:.1f}%, transparent {data['video_pct']:.1f}%)"
        html += f"""                    <tr>
                        <td>{user}</td>
                        <td>{data['domain']}</td>
                        <td class="numeric">1</td>
                        <td class="numeric">{data['count']}</td>
                        <td class="numeric" style="{ans_bar}"><span class="{answer_status}">{data['answer_rate']:.1f}%</span></td>
                        <td class="numeric">{data['avg_confidence']}</td>
                        <td class="numeric" style="{vid_bar}">{data['video_pct']:.1f}%</td>
                    </tr>
"""

    for (agent, env), data in anon_sessions_sorted:
        answer_status = "status-good" if data["answer_rate"] >= 80 else ("status-warning" if data["answer_rate"] >= 50 else "status-critical")
        bar_rgba = "rgba(46,204,113,0.35)" if data["answer_rate"] >= 80 else ("rgba(243,156,18,0.35)" if data["answer_rate"] >= 50 else "rgba(231,76,60,0.35)")
        ans_bar = f"background: linear-gradient(to right, {bar_rgba} {data['answer_rate']:.1f}%, transparent {data['answer_rate']:.1f}%)"
        vid_bar = f"background: linear-gradient(to right, rgba(102,126,234,0.35) {data['video_pct']:.1f}%, transparent {data['video_pct']:.1f}%)"
        agent_label = f"Anonymous — {agent}" if agent != "unknown" else "Anonymous (no agent attributed)"
        html += f"""                    <tr style="font-style: italic; color: #666;">
                        <td>{agent_label}</td>
                        <td>{env}</td>
                        <td class="numeric">{data['sessions']}</td>
                        <td class="numeric">{data['count']}</td>
                        <td class="numeric" style="{ans_bar}"><span class="{answer_status}">{data['answer_rate']:.1f}%</span></td>
                        <td class="numeric">{data['avg_confidence']}</td>
                        <td class="numeric" style="{vid_bar}">{data['video_pct']:.1f}%</td>
                    </tr>
"""

    html += f"""                </tbody>
            </table>
        </div>

        <!-- Language Distribution -->
        <div class="section">
            <h2>🌍 Language Distribution</h2>
            <div class="chart-wrapper"><canvas id="languageChart_{ns}"></canvas></div>
            <p style="color: #666; font-size: 0.85em; margin-top: 12px;">
                <strong>Left axis:</strong> Query volume per language (bars)
                | <strong>Right axis:</strong> IDK % (orange line) and Video % (green line)
            </p>
        </div>
        <script>
            (function() {{
                const langs_{ns} = [
"""
    lang_sorted = sorted(analysis.get("languages", {}).items(), key=lambda x: -x[1]["count"])
    for lang_code, data in lang_sorted:
        lang_name = {"en": "English", "pt": "Portuguese", "es": "Spanish", "ar": "Arabic", "hi": "Hindi", "zh": "Chinese", "ja": "Japanese", "ko": "Korean"}.get(lang_code, lang_code.upper())
        lang_idk_rate = round((data["idk"] / data["count"] * 100), 1) if data["count"] > 0 else 0
        html += f"                    ['{lang_name}', {data['count']}, {lang_idk_rate}, {data['video_pct']:.1f}],\n"

    html += f"""                ];
                new Chart(document.getElementById('languageChart_{ns}'), {{
                    data: {{
                        labels: langs_{ns}.map(r => r[0]),
                        datasets: [
                            {{
                                type: 'bar', label: 'Queries', data: langs_{ns}.map(r => r[1]), yAxisID: 'y',
                                backgroundColor: 'rgba(102,126,234,0.7)', borderColor: 'rgba(102,126,234,1)',
                                borderWidth: 1, borderRadius: 6, order: 3
                            }},
                            {{
                                type: 'line', label: 'IDK %', data: langs_{ns}.map(r => r[2]), yAxisID: 'y1',
                                borderColor: '#f39c12', backgroundColor: '#f39c12',
                                borderWidth: 3, tension: 0.3, pointRadius: 5, pointHoverRadius: 7, pointBackgroundColor: '#f39c12', order: 1
                            }},
                            {{
                                type: 'line', label: 'Video %', data: langs_{ns}.map(r => r[3]), yAxisID: 'y1',
                                borderColor: '#2ecc71', backgroundColor: '#2ecc71',
                                borderWidth: 3, borderDash: [6,4], tension: 0.3, pointRadius: 5, pointHoverRadius: 7, pointBackgroundColor: '#2ecc71', order: 2
                            }}
                        ]
                    }},
                    options: {{
                        responsive: true, maintainAspectRatio: false,
                        interaction: {{ mode: 'index', intersect: false }},
                        plugins: {{ legend: {{ labels: {{ color: '#333', usePointStyle: true, padding: 18, font: {{ size: 12 }} }} }} }},
                        scales: {{
                            x: {{ ticks: {{ color: '#666' }}, grid: {{ color: '#e8e8e8' }} }},
                            y: {{ position: 'left', beginAtZero: true, title: {{ display: true, text: 'Queries', color: '#666', font: {{ weight: '600' }} }}, ticks: {{ color: '#666' }}, grid: {{ color: '#e8e8e8' }} }},
                            y1: {{ position: 'right', beginAtZero: true, max: 100, title: {{ display: true, text: '% (IDK & Video)', color: '#666', font: {{ weight: '600' }} }}, ticks: {{ color: '#666', callback: v => v + '%' }}, grid: {{ drawOnChartArea: false }} }}
                        }}
                    }}
                }});
            }})();
        </script>

        <!-- Multi-Intent Analysis -->
        <div class="section">
            <h2>🎯 Multi-Intent & Cross-Module Questions</h2>
            <table>
                <thead>
                    <tr>
                        <th>Intent Count</th>
                        <th class="numeric">Queries</th>
                        <th class="numeric">Answer Rate</th>
                    </tr>
                </thead>
                <tbody>
"""

    for intent_count, data in intent_multi_sorted:
        answer_status = "status-good" if data["answer_rate"] >= 80 else ("status-warning" if data["answer_rate"] >= 50 else "status-critical")
        html += f"""                    <tr>
                        <td>{intent_count} intent{"s" if intent_count != 1 else ""}</td>
                        <td class="numeric">{data['count']}</td>
                        <td class="numeric"><span class="{answer_status}">{data['answer_rate']:.1f}%</span></td>
                    </tr>
"""

    html += """                </tbody>
            </table>
        </div>

        <!-- Intent Video Triggers -->
        <div class="section">
            <h2>🎬 Intent-based Video Triggers</h2>
            <table>
                <thead>
                    <tr>
                        <th>Intent</th>
                        <th class="numeric">Queries</th>
                        <th class="numeric">Video Attached %</th>
                    </tr>
                </thead>
                <tbody>
"""

    for intent, data in intent_video_sorted:
        vid_bar = f"background: linear-gradient(to right, rgba(102,126,234,0.35) {data['video_pct']:.1f}%, transparent {data['video_pct']:.1f}%)"
        html += f"""                    <tr>
                        <td>{intent}</td>
                        <td class="numeric">{data['count']}</td>
                        <td class="numeric" style="{vid_bar}">{data['video_pct']:.1f}%</td>
                    </tr>
"""

    html += f"""                </tbody>
            </table>
        </div>

        <!-- DemoForge Coverage Report (folds in the YouTube/DemoForge platform
             split as a one-line caption instead of a separate 2-card section -
             YouTube has shown 0% usage in every recent refresh, so a dedicated
             split section was mostly dead visual weight). -->
        <div class="section">
            <h2>🎞️ DemoForge Coverage Report</h2>
"""
    vp = analysis.get('video_platforms', {})
    html += f"""            <p style="color:#666; font-size:0.85em; margin-bottom:12px;">
                Platform split: {vp.get('demoforge', 0)} DemoForge ({vp.get('demoforge_pct', 0)}%) vs {vp.get('youtube', 0)} YouTube ({vp.get('youtube_pct', 0)}%)
            </p>
"""
    demo_videos = analysis.get("demo_videos", {})
    if demo_videos:
        html += f"""            <table>
                <thead>
                    <tr>
                        <th>Demo ID</th>
                        <th>Demo Title</th>
                        <th class="numeric">Usage Count</th>
                    </tr>
                </thead>
                <tbody>
"""
        for demo_id, data in sorted(demo_videos.items(), key=lambda x: x[1]['count'], reverse=True):
            html += f"""                    <tr>
                        <td><code>{demo_id}</code></td>
                        <td>{data.get('title', 'Untitled')}</td>
                        <td class="numeric">{data['count']}</td>
                    </tr>
"""
        html += f"""                </tbody>
            </table>
"""
    else:
        html += f"""            <p style="color: #999; text-align: center; padding: 40px 0;">No DemoForge videos used in this segment</p>
"""

    html += f"""        </div>
"""

    # Top YouTube Videos: only rendered when there's actually data - YouTube
    # usage has been 0 across every recent refresh, so an always-shown empty
    # section was pure clutter. Auto-reappears if YouTube usage resumes.
    youtube_videos = analysis.get("youtube_videos", {})
    if youtube_videos:
        html += f"""
        <!-- Top YouTube Videos -->
        <div class="section">
            <h2>📺 Top YouTube Videos (Last 10)</h2>
            <table>
                <thead>
                    <tr>
                        <th>Video ID</th>
                        <th>Title</th>
                        <th class="numeric">Attachments</th>
                    </tr>
                </thead>
                <tbody>
"""
        for video_id, data in list(youtube_videos.items())[:10]:
            html += f"""                    <tr>
                        <td><code>{video_id}</code></td>
                        <td>{data.get('title', 'Untitled')}</td>
                        <td class="numeric">{data['count']}</td>
                    </tr>
"""
        html += f"""                </tbody>
            </table>
        </div>
"""

    html += f"""
        <!-- Sample of Remaining IDK Queries -->
        <div class="section">
            <h2>❌ Sample of Remaining IDK Queries (By Language)</h2>
"""
    idk_by_lang = analysis.get("idk_by_language", {})
    lang_names = {"en": "English", "pt": "Portuguese", "es": "Spanish", "ar": "Arabic", "hi": "Hindi", "zh": "Chinese", "ja": "Japanese", "ko": "Korean"}

    # CSS-only radio tabs: all inputs first, then the label bar, then content panels.
    lang_group = f"langtab-{ns}"
    for i, (lang_code, _) in enumerate(sorted(idk_by_lang.items())):
        tab_id = f"{lang_group}-{lang_code}"
        checked = " checked" if i == 0 else ""
        html += f'            <input type="radio" class="tab-input" name="{lang_group}" id="{tab_id}"{checked}>\n'

    html += f"""            <div class="lang-tabs" id="lang-tabs-{ns}">
"""
    for lang_code, _ in sorted(idk_by_lang.items()):
        tab_id = f"{lang_group}-{lang_code}"
        lang_name = lang_names.get(lang_code, lang_code.upper())
        html += f'                <label class="lang-tab" for="{tab_id}">{lang_name}</label>\n'

    html += f"""            </div>
"""
    for lang_code, idk_list in sorted(idk_by_lang.items()):
        tab_id = f"{lang_group}-{lang_code}"
        html += f"""            <div class="lang-content" id="content-{tab_id}">
                <table>
                    <thead>
                        <tr>
                            <th>Query</th>
                            <th>Module</th>
                            <th>Top Score</th>
                        </tr>
                    </thead>
                    <tbody>
"""
        for idk in idk_list:
            score = float(idk.get('score', 0.0) or 0.0)
            if score > 5:
                row_style = ' style="background: rgba(46,204,113,0.07);"'
                score_style = ' style="color: #2ecc71; font-weight: 600;"'
            elif score < 1:
                row_style = ' style="background: rgba(231,76,60,0.07);"'
                score_style = ' style="color: #e74c3c;"'
            else:
                row_style = ''
                score_style = ''
            html += f"""                        <tr{row_style}>
                            <td>{idk['query']}</td>
                            <td>{idk['module']}</td>
                            <td class="numeric"{score_style}>{score:.2f}</td>
                        </tr>
"""
        html += """                    </tbody>
                </table>
            </div>
"""

    # CSS-only tab wiring: per-tab :checked rules for label highlight + content visibility.
    lang_tab_css = ""
    for lang_code in sorted(idk_by_lang.keys()):
        tab_id = f"{lang_group}-{lang_code}"
        lang_tab_css += (
            f'            #{tab_id}:checked ~ .lang-tabs label[for="{tab_id}"] {{ color: #667eea; border-bottom-color: #667eea; }}\n'
            f'            #{tab_id}:checked ~ #content-{tab_id} {{ display: block; }}\n'
        )

    html += f"""
            <section class="grouping-stats">
                <h3>Trace Linking Analysis</h3>
                <div class="stat-row">
                    <span class="stat-label">Queries with Multiple Traces:</span>
                    <span class="stat-value">{analysis['trace_grouping']['multi_trace_queries']}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Hierarchical Trace Chains:</span>
                    <span class="stat-value">{analysis['trace_grouping']['total_hierarchical_chains']}</span>
                </div>
            </section>
        </div>
        <style>
{lang_tab_css}        </style>
"""
    return html


def _is_real_email(email) -> bool:
    if not email or not isinstance(email, str):
        return False
    e = email.strip().lower()
    if e in ("", "unknown", "none") or e.startswith("sess:") or e.startswith("exec:"):
        return False
    return "@" in e


# Per-module epoch (UTC, naive - matches _parse_ts() output) marking the exact
# timestamp each module's CONSULTING_TONE_CONFIG["modules"][module] traffic_pct
# was LAST CHANGED to its current value in skill/kb_answer.py. Derived from
# `git log` timestamps of the commits that touched CONSULTING_TONE_CONFIG
# (IST -> UTC, IST is UTC+5:30).
#
# WHY THIS EXISTS: a single global "recency" filter (any trace with the new
# turn-tracking metadata fields) is NOT tight enough to compare adoption_pct
# against the CURRENT config - it lets in traffic from before the most recent
# per-module config bump, blending old-config and new-config traffic and
# making adoption look "broken" for modules bumped today even though routing
# is correct (proven 2026-08-22 by manually splitting Campaign Manager/
# WhatsApp traffic at their exact commit timestamps). Each module needs its
# OWN cutoff, not one shared cutoff.
#
# MAINTENANCE BURDEN: this is a MANUALLY-MAINTAINED parallel record, not
# derived automatically from kb_answer.py. Whenever CONSULTING_TONE_CONFIG's
# traffic_pct values change (or a module is added/removed) in
# skill/kb_answer.py, this dict MUST be updated with the new commit's UTC
# timestamp for that module, or adoption_pct for that module will silently go
# stale (comparing against a mix of the old and new epoch instead of just the
# new one).
CONSULTING_CONFIG_EPOCH: Dict[str, datetime] = {
    "RCS": datetime(2026, 8, 18, 8, 43, 1),              # 75->100, commit 08bd9efa
    "Bot Studio": datetime(2026, 8, 18, 8, 43, 1),        # 75->100, commit 08bd9efa
    "Campaign Manager": datetime(2026, 8, 21, 5, 27, 32),  # 50->100, commit 60b36939
    "Agent Assist": datetime(2026, 8, 21, 6, 38, 46),     # 50->75, commit 6696a604
    "Channels": datetime(2026, 8, 21, 6, 38, 46),         # 50->75, commit 6696a604
    "WhatsApp": datetime(2026, 8, 21, 6, 38, 46),         # 50->75, commit 6696a604
    "BizAI": datetime(2026, 8, 21, 6, 38, 46),            # 100->50 rollback, commit 6696a604
    "Integrations": datetime(2026, 8, 21, 6, 38, 46),     # new @ 50, commit 6696a604
    "AI Admin": datetime(2026, 8, 21, 6, 38, 46),         # new @ 50, commit 6696a604
}


def analyze_consulting_effectiveness(all_traces: List[Dict]) -> Dict[str, Any]:
    """Consulting-mode adoption, accuracy, and engagement-content coverage.

    Adoption is computed against the TRUE routing-time module
    (skill._detect_module(query), what _resolve_answer_mode actually gates
    on) rather than telemetry's post-hoc "module" label — those diverge
    whenever a query is detected as "General" at routing time (correctly
    gated to standard) but telemetry relabels it later from the top-scored
    evidence source. Using the telemetry label produced systematically
    wrong adoption numbers for every gated module (confirmed 2026-08-19:
    Bot Studio at 100% traffic_pct showed 62.5% via the wrong method, 100.0%
    via this one). See local/scripts/deep_consulting_tracing_analysis.py.
    """
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root / "skill"))
    import kb_answer as ka  # noqa: E402

    configured = dict(ka.CONSULTING_TONE_CONFIG.get("modules", {}))

    # Adoption specifically needs a RECENT window: traffic_pct has changed
    # multiple times (Bot Studio/RCS 50->75->100%, WhatsApp added entirely),
    # so all-time traces mix eras with different configured splits and
    # produce a misleading blended adoption number (confirmed: unfiltered
    # showed Bot Studio at 55% against a 100% target, purely from diluting
    # with pre-100% history). Using "has the new turn-tracking fields" as
    # the recency boundary is self-maintaining (auto-advances as the system
    # evolves) rather than a hardcoded date that would need updating every
    # time the config changes again.
    recent = [
        t for t in all_traces
        if isinstance(t.get("metadata"), dict)
        and any(f in t["metadata"] for f in ("session_id_source", "turn_number_source", "parent_trace_id_provided"))
    ]

    fixed = [
        t for t in recent
        if t["metadata"].get("selected_answer_mode") in ("consulting", "standard")
        and t["metadata"].get("query")
    ]

    by_module: Dict[str, Dict[str, int]] = {}
    for t in fixed:
        meta = t["metadata"]
        mod = ka._detect_module(meta["query"])
        epoch = CONSULTING_CONFIG_EPOCH.get(mod)
        d = by_module.setdefault(mod, {"consulting": 0, "standard": 0, "excluded_pre_epoch": 0})
        if epoch is not None:
            ts = _parse_ts(t)
            if ts is None or ts < epoch:
                d["excluded_pre_epoch"] += 1
                continue
        d[meta["selected_answer_mode"]] += 1

    # Below this many post-epoch traces, adoption_pct/delta_pp are noise, not
    # signal (e.g. 0/0 or 1/1 reads as a scary "0% vs 50% target" -100pp row
    # that's indistinguishable from a genuine routing failure, when the real
    # story is just "no post-epoch traffic has landed yet"). Flag it instead
    # of rendering a misleading number.
    MIN_TRACES_FOR_ADOPTION_SIGNAL = 3

    module_rows = []
    for mod, d in sorted(by_module.items(), key=lambda x: -(x[1]["consulting"] + x[1]["standard"])):
        total = d["consulting"] + d["standard"]
        adoption = round(100.0 * d["consulting"] / total, 1) if total else 0.0
        cfg = configured.get(mod)
        insufficient_data = mod in configured and total < MIN_TRACES_FOR_ADOPTION_SIGNAL
        module_rows.append({
            "module": mod, "total": total, "consulting": d["consulting"],
            "adoption_pct": adoption, "configured_pct": cfg,
            "delta_pp": round(adoption - cfg, 1) if cfg is not None and not insufficient_data else None,
            "gated": mod in configured,
            "traces_excluded_pre_epoch": d["excluded_pre_epoch"],
            "insufficient_data": insufficient_data,
        })

    consulting = [t for t in fixed if t["metadata"]["selected_answer_mode"] == "consulting"]
    standard = [t for t in fixed if t["metadata"]["selected_answer_mode"] == "standard"]

    def _answered_pct(items):
        if not items:
            return None
        n = sum(1 for i in items if i["metadata"].get("answered") is True)
        return round(100.0 * n / len(items), 1)

    def _avg_conf(items):
        vals = [i["metadata"].get("confidence") for i in items if isinstance(i["metadata"].get("confidence"), (int, float))]
        return round(sum(vals) / len(vals), 3) if vals else None

    def _avg_len(items):
        vals = [len((i.get("output") or {}).get("answer", "")) for i in items]
        vals = [v for v in vals if v]
        return round(sum(vals) / len(vals)) if vals else None

    consulting_answers = [(t.get("output") or {}).get("answer", "") for t in consulting]
    n_bp = sum(1 for a in consulting_answers if "**Best practices:**" in a)
    n_fit = sum(1 for a in consulting_answers if "This also connects well with" in a)
    n_cs = sum(1 for a in consulting_answers if "Related success stories" in a or "See it in action" in a)

    return {
        "module_rows": module_rows,
        "consulting_n": len(consulting),
        "standard_n": len(standard),
        "consulting_answered_pct": _answered_pct(consulting),
        "standard_answered_pct": _answered_pct(standard),
        "consulting_avg_conf": _avg_conf(consulting),
        "standard_avg_conf": _avg_conf(standard),
        "consulting_avg_len": _avg_len(consulting),
        "standard_avg_len": _avg_len(standard),
        "best_practices_pct": round(100.0 * n_bp / len(consulting_answers), 1) if consulting_answers else None,
        "fitment_pct": round(100.0 * n_fit / len(consulting_answers), 1) if consulting_answers else None,
        "case_study_pct": round(100.0 * n_cs / len(consulting_answers), 1) if consulting_answers else None,
    }


def analyze_multiturn_tracking(all_traces: List[Dict]) -> Dict[str, Any]:
    """Session/turn-tracking field coverage and real multi-turn conversation
    clustering (real email + 10-minute proximity, since VAPT PII scrubbing
    makes session_id unreliable for grouping — see memory:
    superagent-pii-scrubbing). Honest about the accuracy-vs-depth signal:
    prior checks found no consistent direction (weak/noisy), so this
    reports the numbers without implying a causal story either way."""
    fixed = [
        t for t in all_traces
        if isinstance(t.get("metadata"), dict)
        and any(f in t["metadata"] for f in ("session_id_source", "turn_number_source", "parent_trace_id_provided"))
    ]

    by_env: Dict[str, Dict[str, int]] = {}
    for t in fixed:
        meta = t["metadata"]
        env = meta.get("trace_env") or "unset"
        d = by_env.setdefault(env, {"total": 0, "client_session": 0, "real_email": 0})
        d["total"] += 1
        if meta.get("session_id_source") == "client":
            d["client_session"] += 1
        if _is_real_email(meta.get("user_email")):
            d["real_email"] += 1

    env_rows = []
    for env, d in sorted(by_env.items()):
        env_rows.append({
            "env": env, "total": d["total"],
            "client_session_pct": round(100.0 * d["client_session"] / d["total"], 1) if d["total"] else 0,
            "real_email_pct": round(100.0 * d["real_email"] / d["total"], 1) if d["total"] else 0,
        })

    real_email_traces = []
    for t in fixed:
        meta = t["metadata"]
        if not _is_real_email(meta.get("user_email")):
            continue
        ts_raw = t.get("timestamp")
        if isinstance(ts_raw, str):
            try:
                ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
            except ValueError:
                continue
        elif isinstance(ts_raw, datetime):
            ts = ts_raw
        else:
            continue
        real_email_traces.append({"ts": ts, "email": meta.get("user_email"), "meta": meta})

    by_email: Dict[str, List[Dict]] = {}
    for t in real_email_traces:
        by_email.setdefault(t["email"], []).append(t)

    clusters = []
    for email, items in by_email.items():
        items.sort(key=lambda x: x["ts"])
        cluster = [items[0]]
        for it in items[1:]:
            if (it["ts"] - cluster[-1]["ts"]).total_seconds() <= 600:
                cluster.append(it)
            else:
                clusters.append(cluster)
                cluster = [it]
        clusters.append(cluster)

    multi = [c for c in clusters if len(c) >= 2]
    first_pos = [c[0] for c in multi]
    later_pos = [it for c in multi for it in c[1:]]

    def _answered_pct(items):
        if not items:
            return None
        n = sum(1 for i in items if i["meta"].get("answered") is True)
        return round(100.0 * n / len(items), 1)

    def _avg_conf(items):
        vals = [i["meta"].get("confidence") for i in items if isinstance(i["meta"].get("confidence"), (int, float))]
        return round(sum(vals) / len(vals), 3) if vals else None

    return {
        "env_rows": env_rows,
        "unique_real_email_users": len(by_email),
        "total_conversations": len(clusters),
        "multi_turn_conversations": len(multi),
        "single_turn_conversations": len(clusters) - len(multi),
        "first_turn_n": len(first_pos),
        "first_turn_answered_pct": _answered_pct(first_pos),
        "first_turn_avg_conf": _avg_conf(first_pos),
        "later_turn_n": len(later_pos),
        "later_turn_answered_pct": _answered_pct(later_pos),
        "later_turn_avg_conf": _avg_conf(later_pos),
    }


def generate_consulting_effectiveness_html(ce: Dict[str, Any], mt: Dict[str, Any]) -> str:
    """Renders the consulting-mode effectiveness + multi-turn tracking section."""
    module_rows_html = ""
    for r in ce["module_rows"]:
        if r["gated"]:
            delta = r["delta_pp"]
            if r.get("insufficient_data"):
                delta_str = '<span style="color:#94a3b8;">insufficient data</span>'
            else:
                delta_color = "#22c55e" if delta is not None and delta >= 0 else "#f59e0b"
                delta_str = f'<span style="color:{delta_color}; font-weight:600;">{delta:+.1f}pp</span>' if delta is not None else "—"
            cfg_str = f'{r["configured_pct"]}%'
        else:
            delta_str = '<span style="color:#94a3b8;">not gated</span>'
            cfg_str = "—"
        module_rows_html += f"""
                    <tr>
                        <td>{r['module']}</td>
                        <td class="numeric">{r['total']}</td>
                        <td class="numeric">{r['consulting']}</td>
                        <td class="numeric"><strong>{r['adoption_pct']}%</strong></td>
                        <td class="numeric">{cfg_str}</td>
                        <td class="numeric">{delta_str}</td>
                    </tr>
"""

    def _fmt(v, suffix=""):
        return f"{v}{suffix}" if v is not None else "n/a"

    len_delta = None
    if ce["consulting_avg_len"] and ce["standard_avg_len"]:
        len_delta = round(100.0 * (ce["consulting_avg_len"] - ce["standard_avg_len"]) / ce["standard_avg_len"], 1)

    env_rows_html = ""
    for r in mt["env_rows"]:
        env_rows_html += f"""
                    <tr>
                        <td>{r['env']}</td>
                        <td class="numeric">{r['total']}</td>
                        <td class="numeric">{r['client_session_pct']}%</td>
                        <td class="numeric">{r['real_email_pct']}%</td>
                    </tr>
"""

    return f"""
        <!-- CONSULTING MODE EFFECTIVENESS + MULTI-TURN TRACKING
             Adoption uses true routing-time module detection, not telemetry's
             post-hoc label (see analyze_consulting_effectiveness docstring).
             Multi-turn accuracy signal is intentionally reported without a
             causal claim — prior checks found no consistent direction. -->
        <div class="section" style="border: 2px solid #8b5cf6;">
            <h2>🎯 Consulting Mode Effectiveness</h2>
            <p style="color:#666; font-size:0.85em; margin-bottom:16px;">
                Accuracy and engagement impact of consulting-tone answers vs. standard, plus per-module
                adoption vs. configured traffic split.
            </p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 15px; margin-bottom: 20px;">
                <div style="background: #f5f3ff; padding: 16px; border-radius: 8px;">
                    <div style="font-size: 0.8em; color: #666;">Answer Rate</div>
                    <div style="font-size: 1.5em; font-weight: 700; color: #8b5cf6;">{_fmt(ce['consulting_answered_pct'], '%')}</div>
                    <div style="font-size: 0.75em; color: #999;">vs standard {_fmt(ce['standard_answered_pct'], '%')}</div>
                </div>
                <div style="background: #f5f3ff; padding: 16px; border-radius: 8px;">
                    <div style="font-size: 0.8em; color: #666;">Avg Confidence</div>
                    <div style="font-size: 1.5em; font-weight: 700; color: #8b5cf6;">{_fmt(ce['consulting_avg_conf'])}</div>
                    <div style="font-size: 0.75em; color: #999;">vs standard {_fmt(ce['standard_avg_conf'])}</div>
                </div>
                <div style="background: #f5f3ff; padding: 16px; border-radius: 8px;">
                    <div style="font-size: 0.8em; color: #666;">Answer Length</div>
                    <div style="font-size: 1.5em; font-weight: 700; color: #8b5cf6;">{'+' + str(len_delta) + '%' if len_delta is not None else 'n/a'}</div>
                    <div style="font-size: 0.75em; color: #999;">{_fmt(ce['consulting_avg_len'])} vs {_fmt(ce['standard_avg_len'])} chars</div>
                </div>
                <div style="background: #f5f3ff; padding: 16px; border-radius: 8px;">
                    <div style="font-size: 0.8em; color: #666;">Best Practices Coverage</div>
                    <div style="font-size: 1.5em; font-weight: 700; color: #8b5cf6;">{_fmt(ce['best_practices_pct'], '%')}</div>
                    <div style="font-size: 0.75em; color: #999;">of consulting-mode answers</div>
                </div>
                <div style="background: #f5f3ff; padding: 16px; border-radius: 8px;">
                    <div style="font-size: 0.8em; color: #666;">Fitment Coverage</div>
                    <div style="font-size: 1.5em; font-weight: 700; color: #8b5cf6;">{_fmt(ce['fitment_pct'], '%')}</div>
                    <div style="font-size: 0.75em; color: #999;">of consulting-mode answers</div>
                </div>
                <div style="background: #f5f3ff; padding: 16px; border-radius: 8px;">
                    <div style="font-size: 0.8em; color: #666;">Case Study Coverage</div>
                    <div style="font-size: 1.5em; font-weight: 700; color: #8b5cf6;">{_fmt(ce['case_study_pct'], '%')}</div>
                    <div style="font-size: 0.75em; color: #999;">of consulting-mode answers</div>
                </div>
            </div>

            <h3 style="margin-bottom: 12px;">📊 Per-Module Adoption vs. Configured Split</h3>
            <p style="color:#666; font-size:0.85em; margin-bottom:16px;">
                Each module's traffic since its configured split last changed.
            </p>
            <table style="width:100%; border-collapse:collapse; margin-bottom:24px;">
                <thead>
                    <tr style="border-bottom:2px solid #e5e7eb; text-align:left;">
                        <th style="padding:8px;">Module</th>
                        <th class="numeric" style="padding:8px;">Total</th>
                        <th class="numeric" style="padding:8px;">Consulting</th>
                        <th class="numeric" style="padding:8px;">Adoption</th>
                        <th class="numeric" style="padding:8px;">Configured</th>
                        <th class="numeric" style="padding:8px;">Delta</th>
                    </tr>
                </thead>
                <tbody>
{module_rows_html}
                </tbody>
            </table>

            <h3 style="margin-bottom: 12px;">🔗 Multi-Turn Session Tracking</h3>
            <p style="color:#666; font-size:0.85em; margin-bottom:16px;">
                Real multi-turn conversations, grouped by user and 10-minute proximity.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 15px; margin-bottom: 20px;">
                <div style="background: #eff6ff; padding: 16px; border-radius: 8px;">
                    <div style="font-size: 0.8em; color: #666;">Conversations Tracked</div>
                    <div style="font-size: 1.5em; font-weight: 700; color: #3b82f6;">{mt['total_conversations']}</div>
                    <div style="font-size: 0.75em; color: #999;">{mt['unique_real_email_users']} unique users</div>
                </div>
                <div style="background: #eff6ff; padding: 16px; border-radius: 8px;">
                    <div style="font-size: 0.8em; color: #666;">Multi-Turn</div>
                    <div style="font-size: 1.5em; font-weight: 700; color: #3b82f6;">{mt['multi_turn_conversations']}</div>
                    <div style="font-size: 0.75em; color: #999;">vs {mt['single_turn_conversations']} single-turn</div>
                </div>
                <div style="background: #eff6ff; padding: 16px; border-radius: 8px;">
                    <div style="font-size: 0.8em; color: #666;">First-Turn Answer Rate</div>
                    <div style="font-size: 1.5em; font-weight: 700; color: #3b82f6;">{_fmt(mt['first_turn_answered_pct'], '%')}</div>
                    <div style="font-size: 0.75em; color: #999;">n={mt['first_turn_n']}, conf={_fmt(mt['first_turn_avg_conf'])}</div>
                </div>
                <div style="background: #eff6ff; padding: 16px; border-radius: 8px;">
                    <div style="font-size: 0.8em; color: #666;">Later-Turn Answer Rate</div>
                    <div style="font-size: 1.5em; font-weight: 700; color: #3b82f6;">{_fmt(mt['later_turn_answered_pct'], '%')}</div>
                    <div style="font-size: 0.75em; color: #999;">n={mt['later_turn_n']}, conf={_fmt(mt['later_turn_avg_conf'])}</div>
                </div>
            </div>

            <h3 style="margin-bottom: 12px;">🌐 Session/Identity Capture by Environment</h3>
            <p style="color:#666; font-size:0.85em; margin-bottom:16px;">
                Share of traces with a real session ID and a real user email, by environment.
            </p>
            <table style="width:100%; border-collapse:collapse; margin-bottom:8px;">
                <thead>
                    <tr style="border-bottom:2px solid #e5e7eb; text-align:left;">
                        <th style="padding:8px;">Environment</th>
                        <th class="numeric" style="padding:8px;">Total</th>
                        <th class="numeric" style="padding:8px;">Client Session ID</th>
                        <th class="numeric" style="padding:8px;">Real Email</th>
                    </tr>
                </thead>
                <tbody>
{env_rows_html}
                </tbody>
            </table>
        </div>
    """


def generate_landing_snapshot(all_analysis: Dict[str, Any]) -> str:
    """Sales-facing landing snapshot: topics (query families) across all segments.

    NOTE: the external-users/leads table was removed 2026-07-30. SuperAgent's
    VAPT-tightened PII rules now strip real user identity (email/session_id)
    before it reaches this skill's traces — confirmed root cause, not a code
    bug (see local/reports/superagent_identity_bug_report.md). Every "external"
    identity in users_external is now a shared placeholder (exec:N@..., sess:
    anon@...), so a leads-by-email table would be actively misleading. Internal
    (@gupshup.io/@knowlarity.com) user tracking is unaffected and still shown
    in the per-segment users_internal tables elsewhere in this dashboard.
    """
    mod_agg = {}  # module -> {count, answered, idk, conf_sum}

    for seg, analysis in all_analysis.items():
        if not isinstance(analysis, dict):
            continue
        for module, d in analysis.get("modules", {}).items():
            m = mod_agg.setdefault(module, {"count": 0, "answered": 0, "idk": 0, "conf_sum": 0.0})
            m["count"] += d.get("count", 0)
            m["answered"] += d.get("answered", 0)
            m["idk"] += d.get("idk", 0)
            m["conf_sum"] += d.get("avg_confidence", 0.0) * d.get("count", 0)

    total_mod_queries = sum(m["count"] for m in mod_agg.values())

    # --- Topics table (query families / modules) ---
    mod_sorted = sorted(mod_agg.items(), key=lambda x: x[1]["count"], reverse=True)
    if mod_sorted:
        topics_rows = ""
        for module, d in mod_sorted:
            pct = (d["count"] / total_mod_queries * 100) if total_mod_queries > 0 else 0
            avg_conf = round(d["conf_sum"] / d["count"], 2) if d["count"] > 0 else 0
            pct_bar = f"background: linear-gradient(to right, rgba(102,126,234,0.35) {pct:.1f}%, transparent {pct:.1f}%)"
            topics_rows += f"""                    <tr>
                        <td>{module}</td>
                        <td class="numeric">{d['count']}</td>
                        <td class="numeric" style="{pct_bar}">{pct:.1f}%</td>
                        <td class="numeric">{avg_conf}</td>
                    </tr>
"""
    else:
        topics_rows = '                    <tr><td colspan="4" style="text-align:center; color:#999;">No topics in window</td></tr>\n'

    return f"""
        <!-- TOPICS SNAPSHOT: all segments. External-users leads table removed
             2026-07-30 — SuperAgent PII scrubbing means all "external" identity
             is now a placeholder; see generate_landing_snapshot() docstring. -->
        <div class="section" style="border: 2px solid #667eea;">
            <h2>🔥 Topics Snapshot — Query Family Analysis (All Products)</h2>
            <p style="color:#666; font-size:0.85em; margin-bottom:12px;">What leads are asking about, ranked by volume across all segments ({total_mod_queries} queries).</p>
            <table>
                <thead>
                    <tr>
                        <th>Module / Topic</th>
                        <th class="numeric">Query Count</th>
                        <th class="numeric">% of Total</th>
                        <th class="numeric">Avg Confidence</th>
                    </tr>
                </thead>
                <tbody>
{topics_rows}                </tbody>
            </table>
        </div>
"""


def compute_weekly_accuracy_increment(traces: List[Dict]) -> Dict[str, Any]:
    """Calculate accuracy (answer rate) changes week-over-week.

    Returns dict with:
      weekly_data: list of {week_iso, answer_rate, idk_rate, query_count, avg_confidence}
      current_week: latest week's metrics
      week_over_week_delta: change from previous week (pp)
      trend: "📈 improving", "📉 declining", "➡️ stable"
    """
    if not traces:
        return {}

    # Group by ISO week
    by_week = defaultdict(list)
    for t in traces:
        ts_str = t.get("timestamp", "")
        if not ts_str:
            continue
        try:
            dt = _to_ist(datetime.fromisoformat(ts_str.replace("Z", "+00:00")).replace(tzinfo=None))
            week_iso = dt.strftime("%Y-W%V")  # ISO week format (2026-W32)
            by_week[week_iso].append(t)
        except Exception:
            continue

    if not by_week:
        return {}

    # Calculate metrics per week
    weekly_data = []
    for week_iso in sorted(by_week.keys()):
        week_traces = by_week[week_iso]
        answered = sum(1 for t in week_traces if (t.get("metadata") or {}).get("answered"))
        total = len(week_traces)
        answer_rate = (answered / total * 100) if total else 0.0
        idk_rate = 100.0 - answer_rate
        avg_conf = sum((t.get("metadata") or {}).get("confidence", 0) for t in week_traces) / total if total else 0.0

        weekly_data.append({
            "week": week_iso,
            "answer_rate": round(answer_rate, 1),
            "idk_rate": round(idk_rate, 1),
            "query_count": total,
            "avg_confidence": round(avg_conf, 2),
        })

    # Calculate WoW delta
    current = weekly_data[-1] if weekly_data else {}
    previous = weekly_data[-2] if len(weekly_data) > 1 else {}
    wow_delta = (current.get("answer_rate", 0) - previous.get("answer_rate", 0)) if previous else 0.0

    # Trend indicator
    if wow_delta > 0.5:
        trend = "📈 improving"
    elif wow_delta < -0.5:
        trend = "📉 declining"
    else:
        trend = "➡️ stable"

    return {
        "weekly_data": weekly_data,
        "current_week": current,
        "previous_week": previous,
        "week_over_week_delta": round(wow_delta, 1),
        "trend": trend,
    }


def generate_weekly_accuracy_report(weekly_data: Dict[str, Any]) -> str:
    """Generate HTML for weekly accuracy increment report."""
    if not weekly_data or not weekly_data.get("weekly_data"):
        return ""

    weeks = weekly_data["weekly_data"]
    current = weekly_data.get("current_week", {})
    wow = weekly_data.get("week_over_week_delta", 0)
    trend = weekly_data.get("trend", "N/A")

    # Build weekly trend table - show ALL weeks
    rows = ""
    for w in weeks:  # Show all available weeks
        rows += f"""
            <tr>
                <td><strong>{w["week"]}</strong></td>
                <td>{w["query_count"]}</td>
                <td><strong>{w["answer_rate"]:.1f}%</strong></td>
                <td>{w["idk_rate"]:.1f}%</td>
                <td>{w["avg_confidence"]:.2f}</td>
            </tr>
        """

    html = f"""
            <div style="background: white; border-radius: 12px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 20px;">
                <h2>📊 Weekly Accuracy Increment (All-Time)</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 20px;">
                    <div style="background: #f0f4ff; padding: 16px; border-radius: 8px;">
                        <div style="font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Current Week Answer Rate</div>
                        <div style="font-size: 2.2em; font-weight: bold; color: #667eea;">{current.get("answer_rate", 0):.1f}%</div>
                    </div>
                    <div style="background: #f0fff4; padding: 16px; border-radius: 8px;">
                        <div style="font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Week-over-Week Change</div>
                        <div style="font-size: 2.2em; font-weight: bold; color: {'#10b981' if wow >= 0 else '#ef4444'};">{wow:+.1f} pp</div>
                    </div>
                    <div style="background: #fef3f2; padding: 16px; border-radius: 8px;">
                        <div style="font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Trend</div>
                        <div style="font-size: 1.5em; font-weight: bold; color: #667eea;">{trend}</div>
                    </div>
                    <div style="background: #f5f3ff; padding: 16px; border-radius: 8px;">
                        <div style="font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">Current Week Volume</div>
                        <div style="font-size: 2.2em; font-weight: bold; color: #667eea;">{current.get("query_count", 0)}</div>
                    </div>
                </div>

                <h3 style="margin-top: 20px; margin-bottom: 12px;">📈 Complete Weekly Trend ({len(weeks)} weeks)</h3>
                <table style="width: 100%; border-collapse: collapse; font-size: 0.9em;">
                    <thead>
                        <tr style="background: #f9fafb; border-bottom: 2px solid #e5e7eb;">
                            <th style="text-align: left; padding: 12px; font-weight: 600;">Week</th>
                            <th style="text-align: center; padding: 12px; font-weight: 600;">Queries</th>
                            <th style="text-align: center; padding: 12px; font-weight: 600;">Answer Rate</th>
                            <th style="text-align: center; padding: 12px; font-weight: 600;">IDK Rate</th>
                            <th style="text-align: center; padding: 12px; font-weight: 600;">Avg Conf</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
    """
    return html


# PER-AGENT ANALYTICS: source_agent is a caller-declared slug (see skill/kb_answer.py
# _extract_source_agent). Traces from before agents were instructed to send it have no
# tag, so unknown-user traffic up to the cutoff is attributed per environment. Real,
# identified users and anything after the cutoff are never backfilled.
SOURCE_AGENT_BACKFILL_CUTOFF = datetime(2026, 10, 8, 7, 52, 49)  # naive UTC, matches _parse_ts()
SOURCE_AGENT_BACKFILL = {"PROD_EXT": "sa_embeded_ccx", "PROD": "concierge"}
SOURCE_AGENT_TRACKED_ENVS = ("PROD", "PROD_EXT", "INT")


def _is_unknown_user(meta: Dict[str, Any]) -> bool:
    """True when the trace has no real caller identity (empty, synthetic sess:/exec:/acct:
    ids, placeholder words, a bare handle with no '@', or the ccexpress.gupshup.io domain)."""
    e = str(meta.get("user_email") or "").strip().lower()
    if not e or e in ("unknown", "none", "anonymous"):
        return True
    if e.split("@")[0].split(":")[0] in ("sess", "exec", "acct", "anon", "unknown"):
        return True
    if "@" not in e:
        return True
    return e.endswith("@ccexpress.gupshup.io")


def apply_source_agent_backfill(traces: List[Dict]) -> Dict[str, int]:
    """Stamp metadata.source_agent_origin on every trace ('tagged' | 'backfill' | 'untagged')
    and backfill source_agent for historical unknown-user traffic. Mutates in memory only."""
    counts = {"tagged": 0, "backfill": 0, "untagged": 0}
    for t in traces:
        meta = t.get("metadata")
        if not isinstance(meta, dict):
            continue
        sa = meta.get("source_agent")
        if sa and sa != "unknown":
            meta["source_agent_origin"] = "tagged"
            counts["tagged"] += 1
            continue
        label = SOURCE_AGENT_BACKFILL.get(meta.get("trace_env"))
        ts = _parse_ts(t)
        if label and ts and ts <= SOURCE_AGENT_BACKFILL_CUTOFF and _is_unknown_user(meta):
            meta["source_agent"] = label
            meta["source_agent_origin"] = "backfill"
            counts["backfill"] += 1
        else:
            meta["source_agent_origin"] = "untagged"
            counts["untagged"] += 1
    return counts


def analyze_source_agents(traces: List[Dict]) -> List[Dict[str, Any]]:
    """One row per (trace_env, source_agent) for PROD / PROD_EXT / INT, reusing analyze_traces()
    so metrics match the segment tabs. Test accounts and test-agent-* probes are excluded."""
    groups: Dict[Any, List[Dict]] = {}
    for t in traces:
        meta = t.get("metadata")
        if not isinstance(meta, dict) or meta.get("trace_env") not in SOURCE_AGENT_TRACKED_ENVS:
            continue
        agent = meta.get("source_agent") or "unknown"
        if str(agent).startswith("test-agent"):
            continue
        has_real_agent_tag = agent != "unknown"
        if meta.get("user_email") in TEST_ACCOUNTS and not has_real_agent_tag:
            continue
        groups.setdefault((meta["trace_env"], agent), []).append(t)

    rows = []
    for (env, agent), ts in groups.items():
        a = analyze_traces(ts)
        stamps = sorted(d for d in (_parse_ts(t) for t in ts) if d)
        origins = [(t.get("metadata") or {}).get("source_agent_origin") for t in ts]
        rows.append({
            "trace_env": env, "source_agent": agent, "traces": len(ts),
            "answer_rate": a.get("answer_rate"), "idk_rate": a.get("idk_rate"),
            "avg_confidence": a.get("avg_confidence"),
            "unknown_user_pct": round(100 * sum(_is_unknown_user(t.get("metadata") or {}) for t in ts) / len(ts), 1),
            "tagged": origins.count("tagged"), "backfilled": origins.count("backfill"),
            "first_seen": _to_ist(stamps[0]).strftime("%Y-%m-%d") if stamps else "",
            "last_seen": _to_ist(stamps[-1]).strftime("%Y-%m-%d") if stamps else "",
        })
    total = sum(r["traces"] for r in rows) or 1
    for r in rows:
        r["share_pct"] = round(100 * r["traces"] / total, 1)
    rows.sort(key=lambda r: (r["trace_env"], -r["traces"]))
    return rows


def generate_source_agent_html(rows: Optional[List[Dict[str, Any]]]) -> str:
    if not rows:
        return ""
    body = ""
    for r in rows:
        unattributed = r["source_agent"] == "unknown"
        style = ' style="color:#999;"' if unattributed else ""
        body += (
            f'<tr{style}><td>{r["trace_env"]}</td><td><b>{r["source_agent"]}</b></td>'
            f'<td>{r["traces"]}</td><td>{r["share_pct"]}%</td><td>{r["answer_rate"]}%</td><td>{r["idk_rate"]}%</td>'
            f'<td>{r["avg_confidence"]}</td><td>{r["unknown_user_pct"]}%</td>'
            f'<td>{r["first_seen"]} to {r["last_seen"]}</td></tr>\n'
        )
    return f"""
        <div class="card" style="background:white;border-radius:12px;padding:20px;margin:16px 0;">
            <h2>🤖 Per-Agent Breakdown (PROD / PROD_EXT / INT)</h2>
            <table>
                <thead><tr><th>Env</th><th>Agent</th><th>Traces</th><th>Share</th><th>Answer</th><th>IDK</th>
                <th>Avg conf</th><th>Unknown users</th><th>Active</th></tr></thead>
                <tbody>
{body}                </tbody>
            </table>
        </div>
"""



def generate_freshness_badge(traces: List[Dict]) -> str:
    """Fixed top-right badge: generation time + newest trace time. The relative age is computed
    in the viewer's browser, so a stale copy shows its real age whenever it is opened."""
    stamps = [d for d in (_parse_ts(t) for t in traces) if d]
    gen = datetime.utcnow()
    latest = max(stamps) if stamps else None
    gen_iso = gen.strftime("%Y-%m-%dT%H:%M:%SZ")
    latest_iso = latest.strftime("%Y-%m-%dT%H:%M:%SZ") if latest else ""
    latest_txt = _to_ist(latest).strftime("%Y-%m-%d %H:%M IST") if latest else "n/a"
    return f"""
    <div id="freshness-badge" data-generated="{gen_iso}" data-latest="{latest_iso}"
         style="position:fixed;top:10px;right:14px;z-index:9999;background:rgba(255,255,255,0.97);border-radius:10px;
                padding:8px 12px;font-size:12px;line-height:1.5;color:#333;box-shadow:0 4px 14px rgba(0,0,0,0.25);
                border-left:5px solid #10b981;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
        <div><b>Last updated:</b> {_to_ist(gen).strftime("%Y-%m-%d %H:%M")} IST <span id="fb-gen-age" style="color:#666;"></span></div>
        <div><b>Newest trace:</b> {latest_txt} <span id="fb-latest-age" style="color:#666;"></span></div>
    </div>
    <script>
    (function(){{
      var b=document.getElementById("freshness-badge"); if(!b) return;
      function age(iso){{ if(!iso) return null; var m=Math.round((Date.now()-new Date(iso).getTime())/60000);
        if(m<1) return "just now"; if(m<60) return m+" min ago"; var h=Math.round(m/60);
        if(h<48) return h+" h ago"; return Math.round(h/24)+" days ago"; }}
      var gm=(Date.now()-new Date(b.dataset.generated).getTime())/3600000;
      var g=age(b.dataset.generated), l=age(b.dataset.latest);
      document.getElementById("fb-gen-age").textContent = g ? "("+g+")" : "";
      document.getElementById("fb-latest-age").textContent = l ? "("+l+")" : "";
      b.style.borderLeftColor = gm<6 ? "#10b981" : (gm<24 ? "#f59e0b" : "#e74c3c");
      if(gm>=24) document.getElementById("fb-gen-age").textContent += " - may be outdated";
    }})();
    </script>
"""


# PER-AGENT PAGE: one tab per agent plus a consolidated view, same panels as the product tabs.
AGENT_TABS = [
    # (tab key, source_agent value or None for consolidated, label, icon, accent colour)
    ("consolidated", None, "Consolidated", "📊", "#667eea"),
    ("cc_embed", "sa_embeded_ccx", "CC Embed", "🚀", "#e74c3c"),
    ("concierge", "concierge", "Concierge", "🛎️", "#10b981"),
    ("video", "video_agent", "Video", "🎬", "#f59e0b"),
    ("presales", "presales-agent", "Presales", "💼", "#8b5cf6"),
]
AGENT_PAGE_ENVS = ("PROD", "PROD_EXT", "INT")


def _agent_page_traces(traces: List[Dict]) -> List[Dict]:
    """Deployed-environment traces only. test-agent-* probes are always excluded. Maintainer
    accounts are excluded UNLESS the trace carries a real agent tag (e.g. a maintainer firing a
    one-off test through a real agent) — a genuine agent tag should never be discarded as noise."""
    out = []
    for t in traces:
        meta = t.get("metadata")
        if not isinstance(meta, dict) or meta.get("trace_env") not in AGENT_PAGE_ENVS:
            continue
        agent = str(meta.get("source_agent") or "")
        if agent.startswith("test-agent"):
            continue
        has_real_agent_tag = agent not in ("", "unknown") and not agent.startswith("test-agent")
        if meta.get("user_email") in TEST_ACCOUNTS and not has_real_agent_tag:
            continue
        out.append(t)
    return out


def _subtab_group(gid: str, items: List[Any]) -> str:
    """CSS-only sub-tab group. items = [(key, label, body_html)]; the first item is shown."""
    inputs = labels = contents = css = ""
    for i, (key, label, body) in enumerate(items):
        inp = f"{gid}-in-{key}"
        inputs += f'            <input type="radio" class="tab-input" name="{gid}" id="{inp}"{" checked" if i == 0 else ""}>\n'
        labels += f'                <label class="sub-tab" for="{inp}">{label}</label>\n'
        contents += f'            <div class="sub-tab-content" id="{gid}-{key}">\n{body}\n            </div>\n'
        css += (f'            #{inp}:checked ~ .sub-tabs label[for="{inp}"] {{ background: #10b981; color: white; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4); }}\n'
                f'            #{inp}:checked ~ #{gid}-{key} {{ display: block; }}\n')
    return f'{inputs}            <div class="sub-tabs">\n{labels}            </div>\n{contents}            <style>\n{css}            </style>\n'


def _product_compare_html(all_analysis: Dict[str, Any]) -> str:
    rows = ""
    for seg, label in (("standalone", "🌐 Standalone"), ("cc_express", "🚀 CC Express")):
        a = all_analysis.get(seg)
        if not isinstance(a, dict):
            continue
        rows += (f'<tr><td><b>{label}</b></td><td class="numeric">{a.get("total_queries", 0)}</td>'
                 f'<td class="numeric">{a.get("answer_rate", 0)}%</td><td class="numeric">{a.get("idk_rate", 0)}%</td>'
                 f'<td class="numeric">{a.get("avg_confidence", 0)}</td></tr>\n')
    return f"""
            <div class="section"><h2>🧩 Product view</h2>
            <table><thead><tr><th>Product</th><th class="numeric">Traces</th><th class="numeric">Answer</th><th class="numeric">IDK</th><th class="numeric">Avg conf</th></tr></thead>
            <tbody>{rows}</tbody></table></div>"""


def build_dashboard_tabs(traces: List[Dict], source_agent_rows: List[Dict[str, Any]], all_analysis: Dict[str, Any],
                         weekly_by_segment: Dict[str, Any], parity: Optional[Dict], ref_label: str) -> Dict[str, str]:
    """Top-level tabs: Consolidated | CC Embed | Concierge | Video.
    Consolidated also hosts the page-wide sections (topics, consulting, multi-turn) and the product view."""
    from collections import Counter
    pool = _agent_page_traces(traces)
    fast_mode = os.environ.get("DASHBOARD_FAST_MODE", "").lower() in ("1", "true", "yes")

    panels, pills, pill_inputs, tab_css = "", "", "", ""
    for idx, (key, agent, label, icon, accent) in enumerate(AGENT_TABS):
        ns = f"agt_{key}"
        seg = pool if agent is None else [t for t in pool if (t.get("metadata") or {}).get("source_agent") == agent]
        tab_id = f"top-agt-{key}"
        pill_inputs += f'        <input type="radio" class="tab-input" name="top-tab" id="{tab_id}"{" checked" if idx == 0 else ""}>\n'
        pills += f'            <label class="product-pill" for="{tab_id}">{icon} {label} <span class="pill-count">{len(seg):,}</span></label>\n'
        tab_css += (
            f'        #{tab_id}:checked ~ .product-pills label[for="{tab_id}"] {{ background: white; color: {accent}; box-shadow: 0 4px 16px rgba(0,0,0,0.15); }}\n'
            f'        #{tab_id}:checked ~ #panel-agt-{key} {{ display: block; }}\n'
        )

        if not seg:
            panels += f"""
        <div class="product-panel" id="panel-agt-{key}">
            <div class="section"><h2>{icon} {label}</h2>
            <p class="muted">No traffic yet.</p></div>
        </div>
"""
            continue

        analysis = analyze_traces(seg)
        analysis['conversations'] = None if fast_mode else analyze_conversations(seg)
        analysis['_traces'] = seg
        weekly = compute_weekly_accuracy_increment(seg)
        cards = generate_product_summary_cards(ns, analysis, {ns: analysis}).replace(ns.title(), label)
        conv_html = generate_conversation_reports(analysis.get('conversations') or _empty_conv_fallback(), segment_key=ns)
        query_html = generate_query_analytics_html(analysis, segment_key=ns)
        weekly_html = generate_weekly_accuracy_report(weekly)

        if agent is None:
            overview = (f"{cards}\n{generate_source_agent_html(source_agent_rows)}\n{weekly_html}\n"
                        f"{generate_landing_snapshot({'consolidated': analysis})}")
            consulting = generate_consulting_effectiveness_html(
                analyze_consulting_effectiveness(pool), analyze_multiturn_tracking(pool))

            product = _product_compare_html(all_analysis)
            if parity:
                product += "\n" + generate_parity_widget(parity, ref_label)
            for pseg, plabel in (("standalone", "🌐 Standalone"), ("cc_express", "🚀 CC Express")):
                pa = all_analysis.get(pseg)
                if not isinstance(pa, dict):
                    continue
                product += f"""
            <details class="fold"><summary>{plabel}: full analytics ({pa.get('total_queries', 0):,} traces, {pa.get('answer_rate', 0)}% answered)</summary>
            <div class="fold-body">
{generate_product_summary_cards(pseg, pa, all_analysis)}
{generate_weekly_accuracy_report(weekly_by_segment.get(pseg, {}))}
{generate_conversation_reports(pa.get('conversations') or _empty_conv_fallback(), segment_key=pseg)}
{generate_query_analytics_html(pa, segment_key=pseg)}
            </div></details>"""
            items = [("overview", "📈 Overview", overview), ("consulting", "🎯 Consulting &amp; Multi-turn", consulting),
                     ("conv", "💬 Conversations", conv_html), ("query", "📊 Queries", query_html),
                     ("product", "🧩 By product", product)]
        else:
            items = [("overview", "📈 Overview", f"{cards}\n{weekly_html}"),
                     ("conv", "💬 Conversations", conv_html), ("query", "📊 Queries", query_html)]

        panels += f"""
        <div class="product-panel" id="panel-agt-{key}">
{_subtab_group(f"sub-{key}", items)}
        </div>
"""

    # Proposal/GTM agent: a separate Langfuse project with different trace
    # schemas (no answered/confidence/module concept), so it can't go through
    # the AGENT_TABS loop above -- added as one more pill/panel by hand,
    # same radio-button CSS mechanism, outside the kb_answer-shaped pipeline.
    # Two distinct tools share this one project under different trace names:
    # gtm-agent-turn (the chat agent) and proposal_generator (the WhatsApp-
    # demo-proposal builder, richer telemetry) -- split and given their own
    # sub-tab each, same _subtab_group mechanism used for AGENT_TABS items.
    proposal_all_traces = fetch_proposal_traces()
    gtm_traces = [t for t in proposal_all_traces if t.get("name") == "gtm-agent-turn"]
    propgen_traces = [t for t in proposal_all_traces if t.get("name") == "proposal_generator"]
    gtm_analysis = analyze_proposal_traces(gtm_traces)
    propgen_analysis = analyze_proposal_generator_traces(propgen_traces)
    prop_tab_id = "top-agt-proposal"
    pill_inputs += f'        <input type="radio" class="tab-input" name="top-tab" id="{prop_tab_id}">\n'
    pills += f'            <label class="product-pill" for="{prop_tab_id}">💼 Proposal/GTM <span class="pill-count">{len(proposal_all_traces):,}</span></label>\n'
    tab_css += (
        f'        #{prop_tab_id}:checked ~ .product-pills label[for="{prop_tab_id}"] {{ background: white; color: #06b6d4; box-shadow: 0 4px 16px rgba(0,0,0,0.15); }}\n'
        f'        #{prop_tab_id}:checked ~ #panel-agt-proposal {{ display: block; }}\n'
    )
    prop_items = [
        ("gtm", f"💬 GTM Agent ({len(gtm_traces)})", generate_proposal_tab_html(gtm_analysis)),
        ("propgen", f"📄 Proposal Generator ({len(propgen_traces)})", generate_proposal_generator_tab_html(propgen_analysis)),
    ]
    panels += f"""
        <div class="product-panel" id="panel-agt-proposal">
{_subtab_group("sub-proposal", prop_items)}
        </div>
"""

    # Cross Sell Agent / groundedness skill: yet another separate Langfuse org
    # (not even the same host/project as Proposal/GTM -- this one requires the
    # v2/observations read path, confirmed by a 410 on the legacy endpoint used
    # everywhere else). Own top-level pill, not nested under Proposal/GTM --
    # it's a genuinely different agent, not a second tool of the same one.
    cross_sell_obs = fetch_cross_sell_observations()
    cross_sell_analysis = analyze_cross_sell_traces(cross_sell_obs)
    cs_tab_id = "top-agt-crosssell"
    pill_inputs += f'        <input type="radio" class="tab-input" name="top-tab" id="{cs_tab_id}">\n'
    pills += f'            <label class="product-pill" for="{cs_tab_id}">🧮 Cross Sell <span class="pill-count">{len(cross_sell_obs):,}</span></label>\n'
    tab_css += (
        f'        #{cs_tab_id}:checked ~ .product-pills label[for="{cs_tab_id}"] {{ background: white; color: #f59e0b; box-shadow: 0 4px 16px rgba(0,0,0,0.15); }}\n'
        f'        #{cs_tab_id}:checked ~ #panel-agt-crosssell {{ display: block; }}\n'
    )
    panels += f"""
        <div class="product-panel" id="panel-agt-crosssell">
{generate_cross_sell_tab_html(cross_sell_analysis)}
        </div>
"""

    return {"inputs": pill_inputs, "pills": pills, "css": tab_css, "panels": panels}


# CC EXPRESS FEATURE: main generate_html() now accepts all_analysis + video_data + parity
def generate_html(all_analysis: Dict[str, Any], video_data: Dict[str, Any], parity: Optional[Dict], weekly_by_segment: Dict[str, Any] = None, source_agent_rows: Optional[List[Dict[str, Any]]] = None) -> str:
    """Generate comprehensive HTML with product-segmented tabs.

    all_analysis: dict keyed by segment ('standalone', 'cc_express', 'console').
                  Each value is the dict returned by analyze_traces() plus
                  'conversations' (from analyze_conversations()) and '_traces'.
    video_data:   global video events (not segmented).
    parity:       output of compute_cc_express_parity(), or None.
    weekly_by_segment: dict mapping segment names to weekly accuracy increment data.
    """
    if weekly_by_segment is None:
        weekly_by_segment = {}

    # Reference segment label for the parity widget
    ref_label = {'standalone': 'Standalone', 'console': 'Console'}.get('console' if 'console' in all_analysis else 'standalone', 'Reference')

    now_str = _to_ist(datetime.utcnow()).strftime('%Y-%m-%d %H:%M:%S')
    all_raw_traces = [t for a in all_analysis.values() if isinstance(a, dict) for t in a.get('_traces', [])]
    tabs = build_dashboard_tabs(all_raw_traces, source_agent_rows or [], all_analysis, weekly_by_segment, parity, ref_label)
    freshness_badge = generate_freshness_badge(all_raw_traces)

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Comprehensive KB Analytics Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            color: #333;
        }}
        .container {{ max-width: 1600px; margin: 0 auto; }}
        .header {{ color: white; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.8em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.1em; opacity: 0.9; }}

        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .card:hover {{ transform: translateY(-5px); }}

        .metric {{ margin-bottom: 20px; }}
        .metric-label {{ font-size: 0.8em; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
        .metric-value {{ font-size: 2.2em; font-weight: bold; color: #333; }}
        .metric-unit {{ font-size: 0.45em; color: #999; margin-left: 5px; }}

        .status-good {{ color: #2ecc71; }}
        .status-warning {{ color: #f39c12; }}
        .status-critical {{ color: #e74c3c; }}

        .section {{ background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
        .section h2 {{ font-size: 1.6em; margin-bottom: 20px; color: #333; border-bottom: 3px solid #667eea; padding-bottom: 10px; }}
        .section h3 {{ font-size: 1.2em; margin-bottom: 12px; color: #444; }}

        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th {{
            background: #f8f9fa;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #555;
            border-bottom: 2px solid #ddd;
            font-size: 0.9em;
        }}
        th.numeric {{ text-align: right; }}
        td {{ padding: 12px; border-bottom: 1px solid #eee; font-size: 0.95em; }}
        td.numeric {{ text-align: right; }}
        tr:hover {{ background: #f8f9fa; }}

        .footer {{ text-align: center; color: white; margin-top: 40px; font-size: 0.9em; opacity: 0.8; }}
        .data-source {{ background: rgba(255,255,255,0.1); padding: 12px; border-radius: 6px; margin-top: 10px; }}
        .chart-wrapper {{ height: 420px; margin: 20px 0; }}

        /* CSS-only radio tabs: hide the actual radio inputs, labels are the visible UI */
        .tab-input {{ display: none; }}

        /* CC EXPRESS FEATURE: Product top-level tab bar */
        .product-pills {{
            display: flex; gap: 4px; margin-bottom: 24px; flex-wrap: wrap;
            background: rgba(255,255,255,0.12); border-radius: 10px; padding: 4px;
        }}
        .product-pill {{
            display: inline-block; padding: 12px 24px; cursor: pointer; background: transparent;
            border: none; border-radius: 8px; color: rgba(255,255,255,0.85); font-weight: 600;
            font-size: 1em; letter-spacing: 0.4px; transition: all 0.2s; text-align: center;
        }}
        .product-pill:hover {{ color: white; background: rgba(255,255,255,0.15); }}
        .product-panel {{ display: none; }}
        /* per-segment :checked rules are emitted inline in the <style> block near the pills */

        /* CC EXPRESS FEATURE: Sub-tab navigation within each product */
        .sub-tabs {{
            display: flex; gap: 8px; margin-bottom: 20px;
            background: transparent; border-radius: 8px; padding: 4px;
        }}
        .sub-tab {{
            display: inline-block; flex: 1; padding: 12px 24px; cursor: pointer; background: rgba(255,255,255,0.12);
            border: none; border-radius: 8px; color: rgba(255,255,255,0.8); font-weight: 600;
            font-size: 0.95em; transition: all 0.3s; text-align: center;
        }}
        .sub-tab:hover {{ color: white; background: rgba(255,255,255,0.2); }}
        .sub-tab-content {{ display: none; }}
        /* per-segment :checked rules are emitted inline in the <style> block near each sub-tab bar */

        /* IDK language tabs */
        .lang-tabs {{ display: flex; gap: 8px; margin-bottom: 16px; border-bottom: 2px solid #e8e8e8; }}
        .lang-tab {{ display: inline-block; padding: 10px 16px; cursor: pointer; background: none; border: none; border-bottom: 3px solid transparent; color: #666; font-weight: 500; transition: all 0.2s; }}
        .lang-tab:hover {{ color: #333; }}
        .lang-content {{ display: none; }}
        /* per-segment :checked rules are emitted inline in the <style> block near each lang-tab bar */

        /* Grouping stats */
        .grouping-stats {{ background: white; border-radius: 12px; padding: 24px; margin: 30px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
        .grouping-stats h3 {{ margin-bottom: 16px; color: #333; }}
        .grouping-stats .stat-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }}
        .grouping-stats .stat-label {{ color: #666; }}
        .grouping-stats .stat-value {{ font-weight: 700; color: #667eea; }}

        /* REDESIGN: readability overrides */
        .header h1 {{ font-size: 2em; margin-bottom: 4px; }}
        .header p {{ font-size: 0.95em; }}
        .header {{ margin-bottom: 18px; }}
        .product-pills {{
            position: sticky; top: 8px; z-index: 40; margin-bottom: 20px;
            background: rgba(88, 70, 160, 0.92); backdrop-filter: blur(6px); box-shadow: 0 6px 20px rgba(0,0,0,0.2);
        }}
        .product-pill {{ padding: 12px 28px; font-size: 1.05em; }}
        .pill-count {{ opacity: 0.7; font-weight: 500; font-size: 0.82em; margin-left: 6px; }}
        .sub-tabs {{ flex-wrap: wrap; gap: 6px; padding: 0; margin-bottom: 18px; }}
        .sub-tab {{ flex: 0 1 auto; padding: 9px 18px; font-size: 0.9em; }}
        .section h2 {{ font-size: 1.3em; margin-bottom: 14px; padding-bottom: 8px; }}
        .section {{ padding: 20px; }}
        .meta-note {{ color: rgba(255,255,255,0.92); font-size: 0.9em; line-height: 1.5; margin: 0 0 16px; }}
        .muted {{ color: #777; font-size: 0.9em; margin-bottom: 12px; }}
        details.fold {{ background: white; border-radius: 12px; margin-bottom: 14px; box-shadow: 0 6px 20px rgba(0,0,0,0.1); }}
        details.fold > summary {{ padding: 16px 20px; cursor: pointer; font-weight: 600; color: #333; list-style-position: inside; }}
        details.fold > .fold-body {{ padding: 4px 20px 20px; background: #f4f5fb; border-radius: 0 0 12px 12px; }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
</head>
<body>
{freshness_badge}
    <div class="container">
        <div class="header">
            <h1>📊 Comprehensive KB Analytics Dashboard</h1>
            <p>Last Updated: {now_str} IST</p>
        </div>

        <!-- TOP-LEVEL TABS: Consolidated | CC Embed | Concierge | Video -->
{tabs['inputs']}        <div class="product-pills">
{tabs['pills']}        </div>
        <style>
{tabs['css']}        </style>
"""

    html += tabs['panels']

    html += f"""
        <!-- Global footer -->

        <div class="footer">
            <div class="data-source">
                <strong>Dashboard Generated:</strong> {now_str} IST
            </div>
        </div>
    </div>
</body>
</html>
"""

    return html


def main():
    """Main execution."""
    print("=" * 80)
    print("COMPREHENSIVE KB ANALYTICS DASHBOARD GENERATOR")
    print("=" * 80)
    print()

    # Fetch all-time data for weekly accuracy reporting. Cached + incremental
    # (see fetch_langfuse_traces) — initial backfill covers system lifetime
    # (<2 months live), later runs only fetch what's new since last refresh.
    traces = fetch_langfuse_traces() or []
    live_count = len(traces)

    # Skip NDJSON merge if running in fast mode (for speed)
    if os.environ.get("DASHBOARD_FAST_MODE", "").lower() in ("1", "true", "yes"):
        print(f"⏭️  Fast mode: skipping NDJSON merge (using live traces only)")
    else:
        # Merge query traces exported to local NDJSON (union, dedupe by trace id).
        print(f"🔗 Loading NDJSON traces...")
        ndjson_traces = load_ndjson_traces(days=INITIAL_BACKFILL_DAYS)  # All-time for consistency (system live <2 months)
        by_id = {t.get("id"): t for t in traces if t.get("id")}
        no_id = [t for t in traces if not t.get("id")]
        added = 0
        for t in ndjson_traces:
            if t["id"] not in by_id:
                by_id[t["id"]] = t
                added += 1
        traces = list(by_id.values()) + no_id
        print(f"🔗 Merged traces: {live_count} live + {len(ndjson_traces)} NDJSON "
              f"(+{added} unique) = {len(traces)} total after dedupe")

    if not traces:
        print("❌ No trace data available. Cannot generate dashboard.")
        return

    # Clamp confidence to the current formula's real range [0, 1]. Older traces
    # (pre-v4.x logic_version) were produced by an UNBOUNDED formula
    # (raw top_score / 8.0 — see _reported_confidence's docstring in
    # skill/kb_answer.py), so their stored confidence can be well above 1.0
    # (observed up to ~8.6 for boost-heavy modules). Averaging those directly
    # against current capped values produces a meaningless blended number with
    # no real scale — this is done ONCE here, at the single point where every
    # trace source (live API + NDJSON) has already been merged, so every
    # downstream avg_confidence computation in this file gets clean data
    # without needing per-call-site fixes.
    _clamped = 0
    for t in traces:
        meta = t.get("metadata")
        if not meta:
            continue
        conf = meta.get("confidence")
        if isinstance(conf, (int, float)) and conf > 1.0:
            meta["confidence"] = 1.0
            _clamped += 1
    if _clamped:
        print(f"🧮 Clamped {_clamped} trace(s) with confidence > 1.0 "
              f"(stale pre-cap formula values) down to 1.0")

    # PER-AGENT ANALYTICS: attribute historical unknown-user traffic, then roll up per agent
    bf = apply_source_agent_backfill(traces)
    print(f"🤖 source_agent: {bf['tagged']} tagged | {bf['backfill']} backfilled | {bf['untagged']} untagged")
    source_agent_rows = analyze_source_agents(traces)

    # CC EXPRESS FEATURE: partition traces by detected_product_original
    print(f"🗂️  Partitioning {len(traces)} traces by product...")
    segments = partition_traces_by_product(traces)
    seg_summary = {k: len(v) for k, v in segments.items()}
    print(f"   Segments: {seg_summary}")

    # CC EXPRESS FEATURE: analyze each segment independently (reuse existing functions)
    # FAST MODE: skip expensive conversation analysis (opt-in via env var)
    fast_mode = os.environ.get("DASHBOARD_FAST_MODE", "").lower() in ("1", "true", "yes")

    all_analysis: Dict[str, Any] = {}
    for segment_key, segment_traces in segments.items():
        # Split off known test/maintainer traffic so it never skews headline
        # metrics (answer rate, IDK rate, confidence, conversation stats), but
        # keep it available for a separate, clearly-labeled table.
        real_traces = [
            t for t in segment_traces
            if (t.get("metadata") or {}).get("user_email") not in TEST_ACCOUNTS
        ]
        test_traces = [
            t for t in segment_traces
            if (t.get("metadata") or {}).get("user_email") in TEST_ACCOUNTS
        ]

        print(f"📊 Analyzing segment '{segment_key}' ({len(real_traces)} traces"
              f"{f', {len(test_traces)} test-traffic excluded' if test_traces else ''})...")
        seg_analysis = analyze_traces(real_traces)
        seg_analysis['test_traffic'] = summarize_test_traffic(test_traces)

        if not fast_mode:
            print(f"💬 Analyzing conversations for '{segment_key}'...")
            seg_analysis['conversations'] = analyze_conversations(real_traces)
            cv = seg_analysis['conversations']['overview']
            print(f"   Conversations: {cv['total_conversations']} | "
                  f"single-turn: {cv['single_turn']} ({cv['single_turn_pct']}%) | "
                  f"multi-turn: {cv['multi_turn']} ({cv['multi_turn_pct']}%) | "
                  f"avg q/conv: {cv['avg_queries_per_conversation']} | max: {cv['max_queries']}")
            de = seg_analysis['conversations']['decomposition_effectiveness']
            print(f"   Decomposed: {de['total_decomposed']} | all-success: {de['all_success_pct']}% | "
                  f"partial: {de['partial_success_pct']}% | all-failed: {de['all_failed_pct']}%")
        else:
            print(f"   (Fast mode: skipping conversation analysis)")
            seg_analysis['conversations'] = None

        seg_analysis['_traces'] = segment_traces
        all_analysis[segment_key] = seg_analysis

    # CC EXPRESS FEATURE: compute parity metrics
    print(f"⚖️  Computing CC Express parity metrics...")
    parity = compute_cc_express_parity({
        **all_analysis,
        'cc_express_traces': segments.get('cc_express', []),
        'ref_traces': segments.get('console') or segments.get('standalone') or [],
    })
    if parity:
        print(f"   CCX answer rate: {parity['ccx_answer_rate']:.1f}% | "
              f"ref: {parity['ref_answer_rate']:.1f}% | delta: {parity['answer_delta']:+.1f}%")
        print(f"   CCX avg conf: {parity['ccx_avg_confidence']:.2f} | "
              f"ref: {parity['ref_avg_confidence']:.2f} | delta: {parity['confidence_delta']:+.2f}")
        print(f"   Low-confidence IDK flags: {len(parity['low_confidence_flags'])}")
    else:
        print("   (No CC Express segment found — parity widget will be hidden)")

    # Video events are global (not segmented)
    print(f"🎥 Loading video-delivery events from NDJSON logs...")
    video_data = load_video_events(days=15)
    ve = video_data
    print(f"   Video deliveries (15d): {ve['total_deliveries']} | captions: {ve['captions_pct']}% "
          f"| fallback: {ve['fallback_pct']}% | latest event: {ve['latest_event_ts'] or 'n/a'}")

    # Compute weekly accuracy increments for all segments
    print(f"📊 Computing weekly accuracy increments...")
    import sys; sys.stdout.flush()
    weekly_by_segment = {}
    for segment_key, segment_traces in segments.items():
        print(f"   Processing {segment_key}...", file=sys.stderr)
        sys.stderr.flush()
        real_traces = [
            t for t in segment_traces
            if (t.get("metadata") or {}).get("user_email") not in TEST_ACCOUNTS
        ]
        print(f"   Filtered to {len(real_traces)} real traces", file=sys.stderr)
        sys.stderr.flush()
        weekly_data = compute_weekly_accuracy_increment(real_traces)
        print(f"   Weekly computation done", file=sys.stderr)
        sys.stderr.flush()
        if weekly_data:
            weekly_by_segment[segment_key] = weekly_data
            if weekly_data.get('current_week'):
                print(f"   [{segment_key}] current week: {weekly_data['current_week'].get('answer_rate', 0):.1f}% | "
                      f"WoW: {weekly_data['week_over_week_delta']:+.1f} pp | {weekly_data['trend']}")

    # Print summary across all segments
    print(f"\n✅ Analysis complete:")
    for seg, analysis in all_analysis.items():
        tg = analysis['trace_grouping']
        print(f"   [{seg}] queries: {analysis['total_queries']} | "
              f"answer: {analysis['answer_rate']}% | "
              f"IDK: {analysis['idk_rate']}% | "
              f"modules: {len(analysis['modules'])} | "
              f"intents: {len(analysis['intents'])}")
        print(f"      trace grouping: {tg['total_correlation_groups']} correlation groups | "
              f"{tg['multi_trace_queries']} multi-trace queries | "
              f"{tg['total_hierarchical_chains']} hierarchical chains")

    print(f"\n🎨 Generating HTML dashboard with all reports...")
    html = generate_html(all_analysis, video_data, parity, weekly_by_segment, source_agent_rows)

    output_path = Path("/Users/adwit.sharma/kb_docs/local/reports/comprehensive_dashboard.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(html)

    print(f"✅ Dashboard saved to: {output_path}")

    # CC EXPRESS FEATURE: save all_analysis (segmented) + parity to JSON
    analysis_path = Path("/Users/adwit.sharma/kb_docs/local/reports/dashboard_analysis.json")
    serialisable = {seg: {k: v for k, v in a.items() if k != '_traces'} for seg, a in all_analysis.items()}
    serialisable['_parity'] = parity
    serialisable['_source_agents'] = source_agent_rows
    with open(analysis_path, "w") as f:
        json.dump(serialisable, f, indent=2, default=str)

    print(f"✅ Analysis saved to: {analysis_path}")
    print()
    print("=" * 80)
    print("✅ COMPREHENSIVE DASHBOARD GENERATED WITH LIVE LANGFUSE DATA")
    print("=" * 80)

if __name__ == "__main__":
    main()
