#!/usr/bin/env python3
"""
Generate Comprehensive KB Analytics Dashboard with All Reports
Always fetches LIVE data from Langfuse API, never uses cached JSON files.
Includes: Global metrics, module analysis, intent distribution, user segmentation, video analytics, etc.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional, Dict, List, Any
import re

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

def fetch_langfuse_traces(days: int = 7) -> Optional[List[Dict]]:
    """Fetch real traces from Langfuse API."""
    print(f"🔄 Fetching Langfuse data for last {days} days...")

    _load_env()

    # Method 1: Langfuse REST API (v2 traces endpoint)
    try:
        import urllib.request, urllib.parse, base64, ssl
        host   = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")
        pub    = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
        sec    = os.environ.get("LANGFUSE_SECRET_KEY", "")

        # Build a verified SSL context (macOS system Python often lacks a CA bundle).
        try:
            import certifi
            ssl_ctx = ssl.create_default_context(cafile=certifi.where())
        except Exception:
            print("⚠️  certifi unavailable — falling back to unverified TLS (run: pip install certifi)")
            ssl_ctx = ssl.create_default_context()
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_NONE

        if pub and sec:
            creds  = base64.b64encode(f"{pub}:{sec}".encode()).decode()
            headers = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

            from_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")
            all_traces = []
            page = 1

            while True:
                params = urllib.parse.urlencode({"page": page, "limit": 100, "fromTimestamp": from_date})
                url = f"{host}/api/public/traces?{params}"
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
                    body = json.loads(resp.read())

                batch = body.get("data", [])
                all_traces.extend(batch)
                meta  = body.get("meta", {})
                total = meta.get("totalItems", meta.get("total", len(all_traces)))

                if not batch or len(all_traces) >= total:
                    break
                page += 1

            if all_traces:
                print(f"✅ Fetched {len(all_traces)} traces via Langfuse REST API")
                return all_traces
        else:
            print("⚠️  Langfuse credentials missing from env")
    except Exception as e:
        print(f"⚠️  REST API fetch failed: {e}")

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

    # Method 3: Load local backup (marked as cached)
    print("⚠️  Langfuse API unavailable, using cached backup (DATED DATA)")
    backup_files = [
        Path("/Users/adwit.sharma/kb_docs/local/reports/langfuse_traces_7day_offline.json"),
        Path("/Users/adwit.sharma/kb_docs/local/reports/comprehensive_analytics.json"),
    ]

    for backup_file in backup_files:
        if backup_file.exists():
            try:
                with open(backup_file) as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        traces = data.get("traces", data.get("data", []))
                    else:
                        traces = data
                    if traces:
                        print(f"✅ Loaded {len(traces)} traces from cache: {backup_file.name}")
                        return traces
            except Exception as e:
                print(f"❌ Failed to read {backup_file}: {e}")

    print("❌ No trace data available")
    return None

def load_ndjson_traces(days: int = 7) -> List[Dict]:
    """Load query traces exported to local NDJSON logs (kb/analytics/*.ndjson).

    Some NDJSON rows are full Langfuse trace exports (keys: id, name, input,
    output, metadata, timestamp) rather than 'video.delivered' events. These are
    real query traces and share the same id format as the live REST API, so the
    caller can union them with the live pull and dedupe by trace id.
    """
    import glob
    analytics_dir = Path(__file__).parent.parent.parent / "kb" / "analytics"
    cutoff = datetime.utcnow() - timedelta(days=days)

    traces = {}
    for fn in glob.glob(str(analytics_dir / "*.ndjson")):
        try:
            with open(fn) as f:
                for line in f:
                    line = line.strip()
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
        except FileNotFoundError:
            continue
    return list(traces.values())


def load_video_events(days: int = 7) -> Dict[str, Any]:
    """Load real video-delivery events from local NDJSON logs (kb/analytics/*.ndjson).

    NDJSON 'video.delivered' rows are EVENTS, not query traces — they are NOT
    merged into query/answer/IDK counts. They provide ground-truth video
    delivery metrics that enrich the Video Analytics sections.
    """
    import glob
    analytics_dir = Path(__file__).parent.parent.parent / "kb" / "analytics"
    cutoff = datetime.utcnow() - timedelta(days=days)

    seen = set()
    total = caps = fallbacks = 0
    by_intent = defaultdict(int)
    by_module = defaultdict(int)
    latest_ts = ""

    for fn in glob.glob(str(analytics_dir / "*.ndjson")):
        try:
            with open(fn) as f:
                for line in f:
                    line = line.strip()
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
        except FileNotFoundError:
            continue

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

    for trace in traces:
        meta = trace.get("metadata") or {}
        if meta.get("user_email") == "adwit.sharma@gupshup.io":
            continue

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
        confidence = meta.get("top_score") or 0.0
        modules[module]["total_confidence"] += confidence

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
      3. derived session: same user_email + time gap <= session_gap_minutes

    Within each conversation, the chronologically first query is the ROOT query;
    the rest are FOLLOW-UPS. Conversations with more than one query are treated as
    DECOMPOSED (the user broke a goal into multiple sub-queries).
    """
    # Normalize + sort traces chronologically, skipping the owner's own traffic.
    rows = []
    for t in traces:
        meta = t.get("metadata") or {}
        if meta.get("user_email") == "adwit.sharma@gupshup.io":
            continue
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
            prev = last_seen.get(user)
            if prev and dt and prev[0] and (dt - prev[0]) <= gap:
                key = prev[1]
            else:
                derived_counter += 1
                key = f"sess:{user}:{derived_counter}"
            last_seen[user] = (dt, key)
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
    """Partition traces by multi-signal CC Express detection (equal weight for all signals).

    CC Express users identified by ANY of these signals (equal probability):
    1. Email domain: *@ccexpress.gupshup.io (authentication-based)
    2. Query mention: "CC Express" explicitly in query text (user-stated preference)
    3. Detected product: detected_product_original == 'cc_express' (system detection)

    All three signals weighted equally — a trace needs >=1 signal to be tagged as CC Express.
    This catches CC Express users who use normal email addresses but mention "CC Express" in queries.

    Returns both segments (Standalone + CC Express) always, even if empty.
    This ensures dashboard always shows comparison metrics.
    """
    def is_cc_express_user_by_email(email):
        """Signal 1: Check if email belongs to CC Express domain."""
        if not email:
            return False
        return '@ccexpress.gupshup.io' in email.lower()

    def is_cc_express_mention_in_query(query):
        """Signal 2: Check if query explicitly mentions 'CC Express'."""
        if not query:
            return False
        query_norm = query.lower()
        return 'cc express' in query_norm or 'ccexpress' in query_norm

    def is_cc_express_detected_by_system(detected_product):
        """Signal 3: Check if system detected CC Express as product."""
        return detected_product == 'cc_express'

    segments = {
        'cc_express': [],
        'standalone': [],
    }

    for trace in traces:
        meta = trace.get('metadata', {})
        user_email = meta.get('user_email') or ''
        query = meta.get('query') or ''
        detected_product = meta.get('detected_product_original')

        # Multi-signal detection (equal weight)
        signal_count = 0
        signals_detected = []

        if is_cc_express_user_by_email(user_email):
            signal_count += 1
            signals_detected.append('email')

        if is_cc_express_mention_in_query(query):
            signal_count += 1
            signals_detected.append('query_mention')

        if is_cc_express_detected_by_system(detected_product):
            signal_count += 1
            signals_detected.append('system_detection')

        # Tag as CC Express if any signal detected (>=1)
        # Traces can have: [email + query], [email + system], [query + system], or just [email] or [query] or [system]
        if signal_count >= 1:
            segments['cc_express'].append(trace)
            # Store signal sources in metadata for analysis (optional)
            trace['_cc_express_signals'] = signals_detected
        else:
            segments['standalone'].append(trace)

    return segments


# CC EXPRESS FEATURE
def compute_cc_express_parity(all_analysis):
    """Compare CC Express vs reference segment (Console or Standalone)."""
    if 'cc_express' not in all_analysis:
        return None

    ccx = all_analysis['cc_express']
    ref = all_analysis.get('console') or all_analysis.get('standalone')
    if not ref:
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
                        <div class="metric-unit">out of 20</div>
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

        <!-- Report 4: Decomposition Effectiveness -->
        <div class="section">
            <h2>🧩 Decomposition Effectiveness</h2>
            <p style="color: #666; font-size: 0.9em; margin-bottom: 16px;">
                Of {de['total_decomposed']} decomposed (multi-query) conversations, how many had
                <strong>all</strong>, <strong>some</strong>, or <strong>none</strong> of their sub-queries answered.
            </p>
            <div class="chart-wrapper" style="height: 360px;"><canvas id="decompChart_{ns}"></canvas></div>
        </div>
        <script>
            (function() {{
                new Chart(document.getElementById('decompChart_{ns}'), {{
                    type: 'doughnut',
                    data: {{
                        labels: ['All Answered ({de['all_success_pct']}%)', 'Partial ({de['partial_success_pct']}%)', 'All Failed ({de['all_failed_pct']}%)'],
                        datasets: [{{
                            data: [{de['all_success']}, {de['partial_success']}, {de['all_failed']}],
                            backgroundColor: ['rgba(46,204,113,0.8)', 'rgba(243,156,18,0.8)', 'rgba(231,76,60,0.8)'],
                            borderColor: ['#2ecc71', '#f39c12', '#e74c3c'], borderWidth: 2
                        }}]
                    }},
                    options: {{
                        responsive: true, maintainAspectRatio: false,
                        plugins: {{ legend: {{ position: 'right', labels: {{ color: '#333', usePointStyle: true, padding: 18, font: {{ size: 13 }} }} }} }}
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
    users_ext_sorted = sorted(analysis["users_external"].items(), key=lambda x: x[1]["count"], reverse=True)
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
                    <div class="metric-unit">out of 20</div>
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

        <!-- External Domain Users -->
        <div class="section">
            <h2>🌐 External Users</h2>
            <table>
                <thead>
                    <tr>
                        <th>User Email</th>
                        <th>Domain</th>
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

        <!-- Sample of Remaining IDK Queries -->
        <div class="section">
            <h2>❌ Sample of Remaining IDK Queries (By Language)</h2>
            <div class="lang-tabs" id="lang-tabs-{ns}">
"""
    idk_by_lang = analysis.get("idk_by_language", {})
    lang_names = {"en": "English", "pt": "Portuguese", "es": "Spanish", "ar": "Arabic", "hi": "Hindi", "zh": "Chinese", "ja": "Japanese", "ko": "Korean"}
    for i, (lang_code, _) in enumerate(sorted(idk_by_lang.items())):
        lang_name = lang_names.get(lang_code, lang_code.upper())
        active_class = " active" if i == 0 else ""
        html += f'                <button class="lang-tab{{active_class}}" onclick="showLangTab_{ns}(event, \'{{lang_code}}\')">{lang_name}</button>\n'

    html += f"""            </div>
"""
    for i, (lang_code, idk_list) in enumerate(sorted(idk_by_lang.items())):
        lang_name = lang_names.get(lang_code, lang_code.upper())
        active_class = " active" if i == 0 else ""
        html += f"""            <div class="lang-content{{active_class}}" id="lang-{ns}-{{lang_code}}">
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
        <script>
            function showLangTab_{ns}(event, langCode) {{
                const tabs = document.getElementById('lang-tabs-{ns}').querySelectorAll('.lang-tab');
                tabs.forEach(t => t.classList.remove('active'));
                event.target.classList.add('active');
                // Hide all lang-content for this segment
                document.querySelectorAll('[id^="lang-{ns}-"]').forEach(c => c.classList.remove('active'));
                const target = document.getElementById('lang-{ns}-' + langCode);
                if (target) target.classList.add('active');
            }}
        </script>
"""
    return html


# CC EXPRESS FEATURE: main generate_html() now accepts all_analysis + video_data + parity
def generate_html(all_analysis: Dict[str, Any], video_data: Dict[str, Any], parity: Optional[Dict]) -> str:
    """Generate comprehensive HTML with product-segmented tabs.

    all_analysis: dict keyed by segment ('standalone', 'cc_express', 'console').
                  Each value is the dict returned by analyze_traces() plus
                  'conversations' (from analyze_conversations()) and '_traces'.
    video_data:   global video events (not segmented).
    parity:       output of compute_cc_express_parity(), or None.
    """

    # CC EXPRESS FEATURE: display order + labels
    # Always show Standalone and CC Express, optionally Console if present
    segment_order = [k for k in ['standalone', 'cc_express'] if k in all_analysis] + \
                    [k for k in ['console'] if k in all_analysis]
    segment_labels = {'standalone': 'Standalone', 'cc_express': 'CC Express', 'console': 'Console'}
    segment_icons  = {'standalone': '🌐', 'cc_express': '🚀', 'console': '🖥️'}

    # Reference segment label for the parity widget
    ref_label = segment_labels.get('console' if 'console' in all_analysis else 'standalone', 'Reference')

    # Build per-segment HTML blocks
    segment_blocks = {}
    for seg in segment_order:
        analysis = all_analysis[seg]
        ns = seg

        # Conversation Insights sub-tab  # CC EXPRESS FEATURE: namespaced
        conv_html = generate_conversation_reports(
            analysis.get('conversations', _empty_conv_fallback()),
            segment_key=ns,
        )

        # Query Analytics sub-tab  # CC EXPRESS FEATURE: namespaced
        query_html = generate_query_analytics_html(analysis, segment_key=ns)

        # CC Express parity widget only in the cc_express segment  # CC EXPRESS FEATURE
        parity_html = ''
        if seg == 'cc_express' and parity:
            parity_html = generate_parity_widget(parity, ref_label)

        # Product summary cards  # CC EXPRESS FEATURE
        summary_cards = generate_product_summary_cards(seg, analysis, all_analysis)

        segment_blocks[seg] = (summary_cards, conv_html, query_html, parity_html)

    # --- Build the first tab ID (the active one) ---
    first_seg = segment_order[0] if segment_order else 'standalone'

    # Product pill buttons  # CC EXPRESS FEATURE
    product_pill_buttons = ''
    for i, seg in enumerate(segment_order):
        active = ' active' if i == 0 else ''
        label = segment_icons.get(seg, '') + ' ' + segment_labels.get(seg, seg.title())
        product_pill_buttons += f'            <button class="product-pill{active}" onclick="showProduct(event, \'{seg}\')">{label}</button>\n'

    now_str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

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

        /* CC EXPRESS FEATURE: Product pill selector */
        .product-pills {{
            display: flex; gap: 10px; margin-bottom: 24px; flex-wrap: wrap;
        }}
        .product-pill {{
            padding: 12px 24px; cursor: pointer; background: rgba(255,255,255,0.15);
            border: none; border-radius: 24px; color: white; font-weight: 600;
            font-size: 1em; letter-spacing: 0.4px; transition: all 0.2s;
        }}
        .product-pill:hover {{ background: rgba(255,255,255,0.3); }}
        .product-pill.active {{ background: white; color: #667eea; box-shadow: 0 4px 16px rgba(0,0,0,0.15); }}
        .product-panel {{ display: none; }}
        .product-panel.active {{ display: block; }}

        /* CC EXPRESS FEATURE: Sub-tab navigation within each product */
        .sub-tabs {{
            display: flex; gap: 8px; margin-bottom: 20px;
            background: transparent; border-radius: 8px; padding: 4px;
        }}
        .sub-tab {{
            flex: 1; padding: 12px 24px; cursor: pointer; background: rgba(255,255,255,0.12);
            border: none; border-radius: 8px; color: rgba(255,255,255,0.8); font-weight: 600;
            font-size: 0.95em; transition: all 0.3s; text-align: center;
        }}
        .sub-tab:hover {{ color: white; background: rgba(255,255,255,0.2); }}
        .sub-tab.active {{ background: #10b981; color: white; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4); }}
        .sub-tab-content {{ display: none; }}
        .sub-tab-content.active {{ display: block; }}

        /* IDK language tabs */
        .lang-tabs {{ display: flex; gap: 8px; margin-bottom: 16px; border-bottom: 2px solid #e8e8e8; }}
        .lang-tab {{ padding: 10px 16px; cursor: pointer; background: none; border: none; border-bottom: 3px solid transparent; color: #666; font-weight: 500; transition: all 0.2s; }}
        .lang-tab.active {{ color: #667eea; border-bottom-color: #667eea; }}
        .lang-tab:hover {{ color: #333; }}
        .lang-content {{ display: none; }}
        .lang-content.active {{ display: block; }}

        /* Grouping stats */
        .grouping-stats {{ background: white; border-radius: 12px; padding: 24px; margin: 30px 0; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
        .grouping-stats h3 {{ margin-bottom: 16px; color: #333; }}
        .grouping-stats .stat-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }}
        .grouping-stats .stat-label {{ color: #666; }}
        .grouping-stats .stat-value {{ font-weight: 700; color: #667eea; }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Comprehensive KB Analytics Dashboard</h1>
            <p>Live Langfuse Telemetry • Last Updated: {now_str} UTC</p>
        </div>

        <!-- CC EXPRESS FEATURE: Product pill selector (replaces 2-button tab nav) -->
        <div class="product-pills">
{product_pill_buttons}        </div>
"""

    # CC EXPRESS FEATURE: Emit one panel per product
    for i, seg in enumerate(segment_order):
        active = ' active' if i == 0 else ''
        summary_cards, conv_html, query_html, parity_html = segment_blocks[seg]
        ns = seg
        label = segment_labels.get(seg, seg.title())

        html += f"""
        <!-- CC EXPRESS FEATURE: product panel for {seg} -->
        <div class="product-panel{active}" id="panel-{seg}">

            <!-- Product summary cards -->
{summary_cards}

            <!-- CC EXPRESS FEATURE: Sub-tab nav (Conversation Insights | Query Analytics) -->
            <div class="sub-tabs" id="sub-tabs-{ns}">
                <button class="sub-tab active" onclick="showSubTab(event, '{ns}', 'conv')">💬 Conversation Insights</button>
                <button class="sub-tab" onclick="showSubTab(event, '{ns}', 'query')">📊 Query Analytics</button>
            </div>

            <!-- Sub-tab: Conversation Insights -->
            <div class="sub-tab-content active" id="subtab-{ns}-conv">
{conv_html}
            </div>

            <!-- Sub-tab: Query Analytics -->
            <div class="sub-tab-content" id="subtab-{ns}-query">
{query_html}
            </div>
"""
        # CC EXPRESS FEATURE: parity widget only in cc_express panel
        if parity_html:
            html += f"""
            <!-- CC EXPRESS FEATURE: Parity widget (cc_express only) -->
{parity_html}
"""

        html += """        </div>
"""

    html += f"""
        <!-- Global footer -->
        <script>
            // CC EXPRESS FEATURE: product pill switching
            function showProduct(event, segKey) {{
                document.querySelectorAll('.product-panel').forEach(p => p.classList.remove('active'));
                document.querySelectorAll('.product-pill').forEach(b => b.classList.remove('active'));
                document.getElementById('panel-' + segKey).classList.add('active');
                event.target.classList.add('active');
            }}

            // CC EXPRESS FEATURE: two-level sub-tab switching
            function showSubTab(event, ns, subKey) {{
                const panel = document.getElementById('panel-' + ns);
                panel.querySelectorAll('.sub-tab').forEach(t => t.classList.remove('active'));
                panel.querySelectorAll('.sub-tab-content').forEach(c => c.classList.remove('active'));
                event.target.classList.add('active');
                const target = document.getElementById('subtab-' + ns + '-' + subKey);
                if (target) target.classList.add('active');
            }}
        </script>

        <div class="footer">
            <div class="data-source">
                <strong>Data Source:</strong> Live Langfuse API (Real-time telemetry)
                <br>
                <strong>Dashboard Generated:</strong> {now_str} UTC
                <br>
                <strong>Coverage:</strong> Last 7 days of production queries
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

    traces = fetch_langfuse_traces(days=7) or []
    live_count = len(traces)

    # Merge query traces exported to local NDJSON (union, dedupe by trace id).
    ndjson_traces = load_ndjson_traces(days=7)
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

    # CC EXPRESS FEATURE: partition traces by detected_product_original
    print(f"🗂️  Partitioning {len(traces)} traces by product...")
    segments = partition_traces_by_product(traces)
    seg_summary = {k: len(v) for k, v in segments.items()}
    print(f"   Segments: {seg_summary}")

    # CC EXPRESS FEATURE: analyze each segment independently (reuse existing functions)
    all_analysis: Dict[str, Any] = {}
    for segment_key, segment_traces in segments.items():
        print(f"📊 Analyzing segment '{segment_key}' ({len(segment_traces)} traces)...")
        seg_analysis = analyze_traces(segment_traces)

        print(f"💬 Analyzing conversations for '{segment_key}'...")
        seg_analysis['conversations'] = analyze_conversations(segment_traces)
        cv = seg_analysis['conversations']['overview']
        print(f"   Conversations: {cv['total_conversations']} | "
              f"single-turn: {cv['single_turn']} ({cv['single_turn_pct']}%) | "
              f"multi-turn: {cv['multi_turn']} ({cv['multi_turn_pct']}%) | "
              f"avg q/conv: {cv['avg_queries_per_conversation']} | max: {cv['max_queries']}")
        de = seg_analysis['conversations']['decomposition_effectiveness']
        print(f"   Decomposed: {de['total_decomposed']} | all-success: {de['all_success_pct']}% | "
              f"partial: {de['partial_success_pct']}% | all-failed: {de['all_failed_pct']}%")

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
    video_data = load_video_events(days=7)
    ve = video_data
    print(f"   Video deliveries (7d): {ve['total_deliveries']} | captions: {ve['captions_pct']}% "
          f"| fallback: {ve['fallback_pct']}% | latest event: {ve['latest_event_ts'] or 'n/a'}")

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
    html = generate_html(all_analysis, video_data, parity)

    output_path = Path("/Users/adwit.sharma/kb_docs/local/reports/comprehensive_dashboard.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(html)

    print(f"✅ Dashboard saved to: {output_path}")

    # CC EXPRESS FEATURE: save all_analysis (segmented) + parity to JSON
    analysis_path = Path("/Users/adwit.sharma/kb_docs/local/reports/dashboard_analysis.json")
    serialisable = {seg: {k: v for k, v in a.items() if k != '_traces'} for seg, a in all_analysis.items()}
    serialisable['_parity'] = parity
    with open(analysis_path, "w") as f:
        json.dump(serialisable, f, indent=2, default=str)

    print(f"✅ Analysis saved to: {analysis_path}")
    print()
    print("=" * 80)
    print("✅ COMPREHENSIVE DASHBOARD GENERATED WITH LIVE LANGFUSE DATA")
    print("=" * 80)

if __name__ == "__main__":
    main()
