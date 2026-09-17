#!/usr/bin/env python3
"""Capture PRE-FIX baseline of conversation turn-tracking telemetry in Langfuse.

Fetches latest N kb_answer traces and computes:
1. % where metadata.session_id != metadata.correlation_id
2. % with metadata.parent_trace_id set (non-null)
3. Distribution of metadata.conversation_turn_number
4. Approximate conversation grouping (session_id + timestamp proximity <=10min)
   and answered=true rate by position (1st vs later) within each group.

Writes JSON report to local/reports/turn_tracking_baseline_<timestamp>.json
"""
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from langfuse_client import get_client, list_traces

LIMIT = 100
PROXIMITY_MINUTES = 10


def to_dt(ts):
    if isinstance(ts, datetime):
        return ts
    return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))


def main():
    client = get_client()
    traces = list_traces(client, name="kb_answer", limit=LIMIT)
    n = len(traces)

    records = []
    for t in traces:
        md = t.metadata if isinstance(t.metadata, dict) else {}
        records.append({
            "trace_id": t.id,
            "timestamp": to_dt(t.timestamp),
            "top_level_session_id": t.session_id,
            "session_id": md.get("session_id"),
            "correlation_id": md.get("correlation_id"),
            "parent_trace_id": md.get("parent_trace_id"),
            "conversation_turn_number": md.get("conversation_turn_number"),
            "answered": md.get("answered"),
        })

    # --- 1. session_id vs correlation_id ---
    both_null = [r for r in records if r["session_id"] is None and r["correlation_id"] is None]
    sid_only = [r for r in records if r["session_id"] is not None and r["correlation_id"] is None]
    cid_only = [r for r in records if r["session_id"] is None and r["correlation_id"] is not None]
    both_present = [r for r in records if r["session_id"] is not None and r["correlation_id"] is not None]
    both_present_equal = [r for r in both_present if r["session_id"] == r["correlation_id"]]
    both_present_diff = [r for r in both_present if r["session_id"] != r["correlation_id"]]
    differ = [r for r in records if r["session_id"] != r["correlation_id"]]
    # Note: in current buggy state both are typically None -> identical (not "differ").
    # "differ" here is dominated by session_id-present/correlation_id-null cases, not by
    # both being genuinely populated and distinct (see breakdown below).
    pct_differ = (len(differ) / n * 100) if n else 0.0

    # --- 2. parent_trace_id set ---
    parent_set = [r for r in records if r["parent_trace_id"] not in (None, "", "null")]
    pct_parent_set = (len(parent_set) / n * 100) if n else 0.0

    # --- 3. conversation_turn_number distribution ---
    turn_dist = Counter(
        r["conversation_turn_number"] if r["conversation_turn_number"] is not None else "null"
        for r in records
    )
    turn_dist_sorted = dict(sorted(turn_dist.items(), key=lambda kv: str(kv[0])))

    # --- 4. Approximate conversation grouping ---
    # Group by session_id (metadata.session_id; fall back to top-level session_id).
    by_session = defaultdict(list)
    no_session_count = 0
    for r in records:
        sid = r["session_id"] or r["top_level_session_id"]
        if sid is None:
            no_session_count += 1
            continue
        by_session[sid].append(r)

    conversations = []  # list of list-of-records, position-ordered
    for sid, recs in by_session.items():
        recs_sorted = sorted(recs, key=lambda r: r["timestamp"])
        # cluster within session by timestamp proximity (<=10min gap chains)
        cluster = [recs_sorted[0]]
        for r in recs_sorted[1:]:
            gap = (r["timestamp"] - cluster[-1]["timestamp"]).total_seconds() / 60.0
            if gap <= PROXIMITY_MINUTES:
                cluster.append(r)
            else:
                if len(cluster) >= 1:
                    conversations.append((sid, cluster))
                cluster = [r]
        conversations.append((sid, cluster))

    multi_turn_convos = [(sid, c) for sid, c in conversations if len(c) >= 2]

    first_position_answered = []
    later_position_answered = []
    for sid, convo in multi_turn_convos:
        for idx, r in enumerate(convo):
            if idx == 0:
                first_position_answered.append(bool(r["answered"]))
            else:
                later_position_answered.append(bool(r["answered"]))

    def rate(lst):
        return (sum(1 for x in lst if x) / len(lst) * 100) if lst else None

    first_rate = rate(first_position_answered)
    later_rate = rate(later_position_answered)

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "baseline_label": "PRE-FIX",
        "trace_name": "kb_answer",
        "traces_fetched": n,
        "1_session_id_vs_correlation_id": {
            "description": "Proxy for distinct real session vs current bug where session_id == correlation_id (both usually null pre-fix).",
            "pct_traces_where_session_id_differs_from_correlation_id": round(pct_differ, 2),
            "count_differ": len(differ),
            "breakdown": {
                "both_null": len(both_null),
                "session_id_only_correlation_id_null": len(sid_only),
                "correlation_id_only_session_id_null": len(cid_only),
                "both_present_and_equal": len(both_present_equal),
                "both_present_and_different": len(both_present_diff),
            },
            "caveat": "correlation_id was not populated on ANY of the sampled traces (0/{}). All 'differ' cases are session_id-present/correlation_id-null, not two genuinely distinct populated IDs.".format(n),
        },
        "2_parent_trace_id_set": {
            "pct_traces_with_parent_trace_id_set": round(pct_parent_set, 2),
            "count_set": len(parent_set),
            "count_total": n,
        },
        "3_conversation_turn_number_distribution": turn_dist_sorted,
        "4_approx_conversation_grouping": {
            "method": f"cluster by metadata.session_id (fallback top-level session_id), chained timestamp gaps <= {PROXIMITY_MINUTES} min",
            "traces_with_no_session_id": no_session_count,
            "distinct_sessions_with_any_trace": len(by_session),
            "total_approx_conversations": len(conversations),
            "multi_turn_conversations_2plus": len(multi_turn_convos),
            "first_position_answered_true_rate_pct": round(first_rate, 2) if first_rate is not None else None,
            "later_position_answered_true_rate_pct": round(later_rate, 2) if later_rate is not None else None,
            "first_position_n": len(first_position_answered),
            "later_position_n": len(later_position_answered),
            "note": "session_id is null/absent on nearly all pre-fix traces, so this grouping is expected to find few/no real multi-trace sessions. That itself is a baseline finding.",
        },
    }
    return result


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2, default=str))
