#!/usr/bin/env python3
"""Best-effort accuracy-vs-conversation-depth correlation using PROXY turn data.

Real metadata.conversation_turn_number is not populated in production traces
(see turn_tracking_baseline_*.json). As an interim proxy, this script clusters
the latest N kb_answer traces by (metadata.session_id, chained timestamp gaps
<= PROXIMITY_MINUTES) -- same method as turn_tracking_baseline.py -- and
compares position-1 ("first turn") vs position-2+ ("later turn") traces on:
  - answered=true rate
  - average metadata.confidence

This is groundwork only. It does NOT decide between expanding consulting-mode
topic coverage vs improving the next-step suggester -- it just produces data
and an honest confidence rating for that future decision.

Writes JSON report to local/reports/accuracy_vs_depth_proxy_<timestamp>.json
"""
import json
import os
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from langfuse_client import get_client, list_traces

LIMIT = 150
PAGE_SIZE = 100  # Langfuse API caps `limit` at 100 per request; paginate to reach LIMIT.
PROXIMITY_MINUTES = 10


def to_dt(ts):
    if isinstance(ts, datetime):
        return ts
    return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))


def fetch_latest_traces(client, name, total):
    """Paginate client.api.trace.list to collect `total` most-recent traces."""
    collected = []
    page = 1
    while len(collected) < total:
        remaining = total - len(collected)
        page_limit = min(PAGE_SIZE, remaining)
        batch = list_traces(client, name=name, limit=page_limit) if page == 1 else \
            client.api.trace.list(name=name, limit=page_limit, page=page).data
        if not batch:
            break
        collected.extend(batch)
        if len(batch) < page_limit:
            break
        page += 1
    return collected[:total]


def main():
    client = get_client()
    traces = fetch_latest_traces(client, "kb_answer", LIMIT)
    n = len(traces)

    records = []
    for t in traces:
        md = t.metadata if isinstance(t.metadata, dict) else {}
        records.append({
            "trace_id": t.id,
            "timestamp": to_dt(t.timestamp),
            "top_level_session_id": t.session_id,
            "session_id": md.get("session_id"),
            "answered": md.get("answered"),
            "confidence": md.get("confidence"),
        })

    # --- Approximate conversation grouping (same method as turn_tracking_baseline.py) ---
    by_session = defaultdict(list)
    no_session_count = 0
    for r in records:
        sid = r["session_id"] or r["top_level_session_id"]
        if sid is None:
            no_session_count += 1
            continue
        by_session[sid].append(r)

    conversations = []  # list of (sid, [records sorted by time])
    for sid, recs in by_session.items():
        recs_sorted = sorted(recs, key=lambda r: r["timestamp"])
        cluster = [recs_sorted[0]]
        for r in recs_sorted[1:]:
            gap = (r["timestamp"] - cluster[-1]["timestamp"]).total_seconds() / 60.0
            if gap <= PROXIMITY_MINUTES:
                cluster.append(r)
            else:
                conversations.append((sid, cluster))
                cluster = [r]
        conversations.append((sid, cluster))

    multi_turn_convos = [(sid, c) for sid, c in conversations if len(c) >= 2]

    first_answered, later_answered = [], []
    first_confidence, later_confidence = [], []
    cluster_details = []

    for sid, convo in multi_turn_convos:
        detail = {"session_id": sid, "size": len(convo), "positions": []}
        for idx, r in enumerate(convo):
            pos_label = "first" if idx == 0 else f"pos_{idx + 1}"
            detail["positions"].append({
                "trace_id": r["trace_id"],
                "position": idx + 1,
                "answered": r["answered"],
                "confidence": r["confidence"],
            })
            if idx == 0:
                first_answered.append(bool(r["answered"]))
                if isinstance(r["confidence"], (int, float)):
                    first_confidence.append(r["confidence"])
            else:
                later_answered.append(bool(r["answered"]))
                if isinstance(r["confidence"], (int, float)):
                    later_confidence.append(r["confidence"])
        cluster_details.append(detail)

    def rate(lst):
        return (sum(1 for x in lst if x) / len(lst) * 100) if lst else None

    def avg(lst):
        return round(statistics.fmean(lst), 4) if lst else None

    first_answered_rate = rate(first_answered)
    later_answered_rate = rate(later_answered)
    first_conf_avg = avg(first_confidence)
    later_conf_avg = avg(later_confidence)

    answered_delta = (
        round(later_answered_rate - first_answered_rate, 2)
        if first_answered_rate is not None and later_answered_rate is not None
        else None
    )
    confidence_delta = (
        round(later_conf_avg - first_conf_avg, 4)
        if first_conf_avg is not None and later_conf_avg is not None
        else None
    )

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "label": "ACCURACY-VS-DEPTH PROXY ANALYSIS (interim, pre real-turn-tracking)",
        "trace_name": "kb_answer",
        "traces_fetched": n,
        "proxy_method": (
            f"cluster by metadata.session_id (fallback top-level session_id), "
            f"chained timestamp gaps <= {PROXIMITY_MINUTES} min. Position 1 = "
            f"'first turn', position 2+ = 'later turn'."
        ),
        "grouping_stats": {
            "traces_with_no_session_id": no_session_count,
            "distinct_sessions_with_any_trace": len(by_session),
            "total_approx_conversations": len(conversations),
            "multi_turn_conversations_2plus": len(multi_turn_convos),
        },
        "answered_rate_by_position": {
            "first_position_pct": round(first_answered_rate, 2) if first_answered_rate is not None else None,
            "later_position_pct": round(later_answered_rate, 2) if later_answered_rate is not None else None,
            "delta_later_minus_first_pct_points": answered_delta,
            "first_position_n": len(first_answered),
            "later_position_n": len(later_answered),
        },
        "avg_confidence_by_position": {
            "first_position_avg": first_conf_avg,
            "later_position_avg": later_conf_avg,
            "delta_later_minus_first": confidence_delta,
            "first_position_n_with_confidence": len(first_confidence),
            "later_position_n_with_confidence": len(later_confidence),
        },
        "cluster_details": cluster_details,
        "caveats": [
            "This uses session_id + timestamp-proximity as a PROXY for conversation "
            "turn position. metadata.conversation_turn_number is not populated in "
            "current production traces (0 traces with turn>=1 per turn_tracking_baseline).",
            "session_id itself is absent/null on a large fraction of traces "
            "(see turn_tracking_baseline: 67/100 in the prior 100-trace sample), so "
            "clustering only covers the minority of traces that carry a session_id.",
            "Sample of genuine multi-turn clusters is expected to be small (single "
            "digits to low teens), so any delta here is NOT statistically robust.",
            "A prior file-based analysis (local/reports/consultation_qa_research_report.md) "
            "found conversation length correlates only WEAKLY with quality/engagement "
            "(r=0.31). This trace-proxy result should be read as directionally "
            "consistent-or-not with that finding, not as a stronger or independent signal.",
            "This script produces data only. It does NOT make the expand-topic-coverage "
            "vs improve-next-step-suggester decision.",
        ],
    }
    return result


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2, default=str))
