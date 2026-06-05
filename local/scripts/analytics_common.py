"""Shared loaders and normalizers for KB usage analytics (local scripts only)."""
from __future__ import annotations

import json
import os
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

ROOT = Path(__file__).resolve().parents[2]
ANALYTICS_DIR = ROOT / "kb" / "analytics"
CHUNKS_PATH = ROOT / "kb" / "kb_chunks.jsonl"
MANIFEST_PATH = ROOT / "kb" / "video_manifest.json"
REPORTS_DIR = ROOT / "local" / "reports"
STATE_PATH = REPORTS_DIR / "state.json"
RUNS_DIR = REPORTS_DIR / "runs"
DASHBOARD_DIR = REPORTS_DIR / "dashboard"

INTERNAL_EMAIL_SUFFIXES = ("@gupshup.com", "@gupshup.io")

PITCH_QUERY_RE = re.compile(
    r"\b(what can you do|what are you trained|how can you help|what do you know|"
    r"what product areas|demo|walkthrough|overview video|pitch|capabilities)\b",
    re.I,
)

VOICE_QUERY_RE = re.compile(
    r"\b(voice ai|pstn|voice bot|voice journey|telephony|ivr)\b",
    re.I,
)
WHATSAPP_QUERY_RE = re.compile(r"\b(whatsapp|wa template|waba|24[- ]?hour)\b", re.I)
INTEGRATION_QUERY_RE = re.compile(
    r"\b(integrat|third[- ]?party|webhook|api|handover|external bot|widget)\b",
    re.I,
)

LOW_SCORE_THRESHOLD = 1.0
IDK_PHRASES = ("i don't know", "i don t know", "i don't know based", "not in the current docs")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso(s: str) -> Optional[datetime]:
    if not s:
        return None
    s = str(s).strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def date_key(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%d")


def module_from_source(source: str) -> str:
    s = "/" + (source or "").lower().replace("\\", "/")
    rules = (
        ("/agent-assist/", "Agent Assist"),
        ("/bot-studio-analytics/", "Analytics"),
        ("/bot-studio/", "Bot Studio"),
        ("/campaign-manager/", "Campaign Manager"),
        ("/channels/", "Channels"),
        ("/goals/", "Goals"),
        ("/integrations/", "Integrations"),
        ("/workflows/", "Workflows"),
        ("/ctx/", "CTX"),
        ("/ai-admin/", "AI Admin"),
        ("/wallet/", "Wallet"),
        ("/personalize/", "Personalize"),
        ("/superagent/", "SuperAgent"),
        ("/overview/", "Overview"),
        ("/case-studies/", "Case Studies"),
    )
    for needle, label in rules:
        if needle in s:
            return label
    if "/analytics/" in s:
        return "Analytics"
    return "General"


def is_idk(answer: str, unanswered: Optional[bool] = None) -> bool:
    if unanswered is True:
        return True
    low = (answer or "").lower()
    return any(p in low for p in IDK_PHRASES)


def is_internal_email(email: Optional[str]) -> bool:
    if not email:
        return False
    e = email.strip().lower()
    return any(e.endswith(suffix) for suffix in INTERNAL_EMAIL_SUFFIXES)


def pct(n: float, total: float) -> float:
    if total <= 0:
        return 0.0
    return round(100.0 * n / total, 1)


def pct_str(n: float, total: float) -> str:
    return f"{pct(n, total):.1f}%"


@dataclass
class QueryEvent:
    ts: datetime
    source: str  # langfuse | ndjson_telemetry | ndjson_usage
    action: str  # kb_answer | kb_search | other
    user_email: str
    query: str
    module: str
    intents: List[str]
    mode: str
    top_source: str
    top_score: Optional[float]
    source_count: int
    answered: bool
    idk: bool
    clarification: bool
    refusal: bool
    video_attached: bool
    video_appended: bool
    video_fallback: bool
    video_id: str
    latency_ms: Optional[int]
    environment: str
    release: str
    trace_id: str
    dedupe_key: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ts": self.ts.isoformat(),
            "source": self.source,
            "action": self.action,
            "user_email": self.user_email,
            "query": self.query,
            "module": self.module,
            "intents": self.intents,
            "mode": self.mode,
            "top_source": self.top_source,
            "top_score": self.top_score,
            "answered": self.answered,
            "idk": self.idk,
            "video_attached": self.video_attached,
            "trace_id": self.trace_id,
        }


@dataclass
class VideoEvent:
    ts: datetime
    channel: str
    video_id: str
    title: str
    source: str
    module: str
    intent: str
    fallback: bool
    query_preview: str
    user_email: str = ""


def _dedupe_key(trace_id: str, ts: datetime, user: str, query: str, action: str) -> str:
    if trace_id:
        return f"trace:{trace_id}"
    q = (query or "")[:120]
    return f"ev:{action}:{date_key(ts)}:{user}:{hash(q) & 0xFFFFFFFF:08x}"


def load_all_ndjson_lines() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if not ANALYTICS_DIR.is_dir():
        return rows
    for path in sorted(ANALYTICS_DIR.glob("*.ndjson")):
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rows


def fetch_langfuse_traces(since: datetime, limit: int = 5000, trace_name: str = "kb_answer") -> List[Dict[str, Any]]:
    if not os.environ.get("LANGFUSE_PUBLIC_KEY") or not os.environ.get("LANGFUSE_SECRET_KEY"):
        return []
    since_str = since.strftime("%Y-%m-%d")
    cmd = [
        "lf", "--json", "traces", "list",
        "--name", trace_name,
        "--from", since_str,
        "--limit", str(limit),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "lf traces list failed")
    data = json.loads(proc.stdout)
    if not isinstance(data, list):
        raise RuntimeError("lf traces list: expected JSON array")
    return data


def trace_to_event(t: Dict[str, Any]) -> QueryEvent:
    meta = t.get("metadata") if isinstance(t.get("metadata"), dict) else {}
    inp = t.get("input") if isinstance(t.get("input"), dict) else {}
    out = t.get("output") if isinstance(t.get("output"), dict) else {}
    query = str(inp.get("query") or meta.get("query") or "")
    answer = str(out.get("answer") or meta.get("answer_preview") or "")
    ts = parse_iso(str(t.get("timestamp") or "")) or utc_now()
    user = str(t.get("userId") or meta.get("user_email") or "")
    intents = [str(x) for x in (meta.get("intent_labels") or [])]
    mode = str(meta.get("selected_answer_mode") or "")
    top_source = str(meta.get("top_source") or "")
    module = str(meta.get("module_label") or module_from_source(top_source) or "General")
    refusal = mode == "refusal" or "refusal" in intents
    unanswered = meta.get("unanswered") is True
    idk = is_idk(answer, unanswered)
    answered = meta.get("answered") is True or (bool(answer.strip()) and not idk and not meta.get("clarification_asked"))
    trace_id = str(t.get("id") or "")
    try:
        top_score = float(meta.get("top_score")) if meta.get("top_score") is not None else None
    except (TypeError, ValueError):
        top_score = None
    try:
        lat = int(meta.get("latency_ms")) if meta.get("latency_ms") else None
    except (TypeError, ValueError):
        lat = None
    return QueryEvent(
        ts=ts,
        source="langfuse",
        action="kb_answer",
        user_email=user,
        query=query,
        module=module,
        intents=intents,
        mode=mode,
        top_source=top_source,
        top_score=top_score,
        source_count=int(meta.get("source_count") or 0),
        answered=answered and not idk,
        idk=idk,
        clarification=meta.get("clarification_asked") is True,
        refusal=refusal,
        video_attached=meta.get("video_attached") is True,
        video_appended=meta.get("video_appended_to_answer") is True,
        video_fallback=meta.get("video_fallback") is True,
        video_id=str(meta.get("video_id") or ""),
        latency_ms=lat,
        environment=str(meta.get("environment") or meta.get("trace_env") or t.get("environment") or "unknown"),
        release=str(meta.get("release") or t.get("release") or ""),
        trace_id=trace_id,
        dedupe_key=_dedupe_key(trace_id, ts, user, query, "kb_answer"),
    )


def ndjson_row_to_events(row: Dict[str, Any]) -> Tuple[List[QueryEvent], List[VideoEvent]]:
    queries: List[QueryEvent] = []
    videos: List[VideoEvent] = []
    ts = parse_iso(str(row.get("ts") or "")) or utc_now()
    event_name = row.get("event")
    if event_name == "video.delivered":
        p = row.get("payload") or {}
        videos.append(
            VideoEvent(
                ts=ts,
                channel=str(p.get("channel") or ""),
                video_id=str(p.get("video_id") or ""),
                title=str(p.get("title") or ""),
                source=str(p.get("source") or ""),
                module=str(p.get("module") or module_from_source(str(p.get("source") or ""))),
                intent=str(p.get("intent") or ""),
                fallback=bool(p.get("fallback")),
                query_preview=str(p.get("query_preview") or ""),
            )
        )
        return queries, videos
    if event_name == "video.clicked":
        return queries, videos
    if event_name == "kb_answer_telemetry":
        p = row.get("payload") or {}
        query = str(p.get("query") or "")
        prev = str(p.get("answer_preview") or "")
        user = str(p.get("user_email") or "")
        top_source = str(p.get("top_source") or "")
        module = str(p.get("module_label") or p.get("explicit_module") or module_from_source(top_source))
        intents = [str(x) for x in (p.get("intent_labels") or [])]
        mode = str(p.get("selected_answer_mode") or "")
        trace_id = str(p.get("trace_id") or "")
        idk = is_idk(prev)
        try:
            top_score = float(p.get("top_score")) if p.get("top_score") is not None else None
        except (TypeError, ValueError):
            top_score = None
        try:
            lat = int(p.get("latency_ms")) if p.get("latency_ms") else None
        except (TypeError, ValueError):
            lat = None
        queries.append(
            QueryEvent(
                ts=ts,
                source="ndjson_telemetry",
                action="kb_answer",
                user_email=user,
                query=query,
                module=module,
                intents=intents,
                mode=mode,
                top_source=top_source,
                top_score=top_score,
                source_count=int(p.get("source_count") or 0),
                answered=not idk and bool(prev.strip()),
                idk=idk,
                clarification=False,
                refusal=mode == "refusal",
                video_attached=False,
                video_appended=False,
                video_fallback=False,
                video_id="",
                latency_ms=lat,
                environment="unknown",
                release="",
                trace_id=trace_id,
                dedupe_key=_dedupe_key(trace_id, ts, user, query, "kb_answer"),
            )
        )
        return queries, videos
    # Legacy kb_usage.ndjson flat rows (may lack event wrapper)
    action = str(row.get("action") or row.get("event") or "")
    if action in ("kb_answer", "kb_search", "github_kb_answer"):
        act = "kb_answer" if "answer" in action else "kb_search"
        query = str(row.get("query") or "")
        user = str(row.get("user_email") or "")
        unanswered = row.get("unanswered")
        idk = unanswered is True
        try:
            lat = int(row.get("t_total_ms") or row.get("latency_ms") or 0) or None
        except (TypeError, ValueError):
            lat = None
        queries.append(
            QueryEvent(
                ts=ts,
                source="ndjson_usage",
                action=act,
                user_email=user,
                query=query,
                module="General",
                intents=[],
                mode="",
                top_source="",
                top_score=None,
                source_count=int(row.get("results_count") or 0),
                answered=not idk and int(row.get("results_count") or 0) > 0,
                idk=idk,
                clarification=False,
                refusal=False,
                video_attached=False,
                video_appended=False,
                video_fallback=False,
                video_id="",
                latency_ms=lat,
                environment="unknown",
                release="",
                trace_id="",
                dedupe_key=_dedupe_key("", ts, user, query, act),
            )
        )
    return queries, videos


def count_ndjson_events(since: datetime, event_name: str) -> int:
    n = 0
    for row in load_all_ndjson_lines():
        if row.get("event") != event_name:
            continue
        ts = parse_iso(str(row.get("ts") or ""))
        if ts and ts >= since:
            n += 1
    return n


def build_corpus(since_30d: datetime) -> Tuple[List[QueryEvent], List[VideoEvent], Dict[str, Any]]:
    """Merge Langfuse + all NDJSON; dedupe preferring langfuse."""
    meta: Dict[str, Any] = {"langfuse_count": 0, "ndjson_rows": 0, "errors": []}
    by_key: Dict[str, QueryEvent] = {}
    videos: List[VideoEvent] = []

    rows = load_all_ndjson_lines()
    meta["ndjson_rows"] = len(rows)
    for row in rows:
        qev, vid = ndjson_row_to_events(row)
        videos.extend(vid)
        for ev in qev:
            existing = by_key.get(ev.dedupe_key)
            if existing is None:
                by_key[ev.dedupe_key] = ev
            elif existing.source != "langfuse" and ev.source == "langfuse":
                by_key[ev.dedupe_key] = ev

    try:
        traces = fetch_langfuse_traces(since_30d, limit=5000)
        meta["langfuse_count"] = len(traces)
        for t in traces:
            ev = trace_to_event(t)
            by_key[ev.dedupe_key] = ev
    except Exception as exc:
        meta["errors"].append(f"langfuse: {exc}")

    events = sorted(by_key.values(), key=lambda e: e.ts)
    return events, videos, meta


def filter_events(events: Iterable[QueryEvent], since: datetime, until: Optional[datetime] = None) -> List[QueryEvent]:
    out: List[QueryEvent] = []
    for e in events:
        if e.ts < since:
            continue
        if until and e.ts >= until:
            continue
        out.append(e)
    return out


def load_kb_index() -> Tuple[Set[str], Counter]:
    """Unique doc paths and chunk counts per module from kb_chunks.jsonl."""
    paths: Set[str] = set()
    per_module = Counter()
    if not CHUNKS_PATH.is_file():
        return paths, per_module
    with CHUNKS_PATH.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            src = str(row.get("source") or "")
            if not src:
                continue
            paths.add(src)
            per_module[module_from_source(src)] += 1
    return paths, per_module


def load_manifest_index() -> Tuple[Set[str], List[Dict[str, Any]], Set[str]]:
    """All KB paths covered by manifest; manifest entries; modules with pitch videos."""
    covered: Set[str] = set()
    entries: List[Dict[str, Any]] = []
    pitch_modules: Set[str] = set()
    if not MANIFEST_PATH.is_file():
        return covered, entries, pitch_modules
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        return covered, entries, pitch_modules
    for ent in data:
        if not isinstance(ent, dict):
            continue
        entries.append(ent)
        src = str(ent.get("source") or "")
        if src:
            covered.add(src)
            mod = module_from_source(src)
            if ent.get("pitch"):
                pitch_modules.add(mod)
        for also in ent.get("also_sources") or []:
            covered.add(str(also))
    return covered, entries, pitch_modules


def simple_theme(query: str) -> str:
    q = query or ""
    if PITCH_QUERY_RE.search(q):
        return "pitch_capability"
    if INTEGRATION_QUERY_RE.search(q):
        return "integration_handover"
    if VOICE_QUERY_RE.search(q):
        return "voice_pstn"
    if WHATSAPP_QUERY_RE.search(q):
        return "whatsapp"
    if re.search(r"\b(troubleshoot|error|failed|not working|why)\b", q, re.I):
        return "troubleshooting"
    if re.search(r"\b(compare|vs|difference|versus)\b", q, re.I):
        return "compare"
    if re.search(r"\b(how to|setup|configure|create|enable)\b", q, re.I):
        return "setup_howto"
    if re.search(r"\b(what is|overview|about)\b", q, re.I):
        return "definition_overview"
    return "general"
