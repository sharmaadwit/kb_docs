#!/usr/bin/env python3
"""
Code-fix effectiveness analysis — turn-tracking fix (commit a60b9e49, live 2026-08-17).

Scope: real-identity traces only (user_email present, not scrubbed/placeholder),
from the last N days, to avoid polluting the analysis with pre-fix or
scrubbed-identity data.

Real-email filter excludes known synthetic/placeholder patterns:
  - user_email in (None, "", "unknown")
  - user_email starting with "sess:" or "exec:" (synthetic identity markers,
    see local/reports/superagent_identity_bug_report.md)

Outputs:
  - local/reports/CODE_FIX_EFFECTIVENESS_<timestamp>.md (human-readable report)
  - local/reports/code_fix_effectiveness_<timestamp>.json (structured data)
"""
import os
import sys
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "local" / "scripts"))
from langfuse_client import get_client, list_traces  # noqa: E402

REPORT_DIR = ROOT / "local" / "reports"
LOOKBACK_DAYS = 4
FIX_DEPLOY_TS = datetime(2026, 8, 17, 5, 0, 0, tzinfo=timezone.utc)  # approx redeploy time


def is_real_email(email):
    if not email or not isinstance(email, str):
        return False
    e = email.strip().lower()
    if e in ("", "unknown", "none"):
        return False
    if e.startswith("sess:") or e.startswith("exec:"):
        return False
    if "@" not in e:
        return False
    return True


def fetch_all_traces(client, name="kb_answer", max_total=1000, page_size=100):
    all_traces = []
    page = 1
    while len(all_traces) < max_total:
        batch = list_traces(client, name=name, limit=page_size)
        if not batch:
            break
        all_traces.extend(batch)
        if len(batch) < page_size:
            break
        page += 1
        if page > 10:  # safety cap
            break
    return all_traces


def main():
    client = get_client()
    print("Fetching traces...")
    traces = fetch_all_traces(client, max_total=600)
    print(f"Fetched {len(traces)} total kb_answer traces")

    cutoff = datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)

    filtered = []
    for t in traces:
        meta = t.metadata if hasattr(t, "metadata") and isinstance(t.metadata, dict) else {}
        ts = t.timestamp if hasattr(t, "timestamp") else None
        if ts is None:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if ts < cutoff:
            continue
        email = meta.get("user_email")
        if not is_real_email(email):
            continue
        filtered.append({"trace": t, "meta": meta, "ts": ts})

    print(f"Filtered to {len(filtered)} real-email traces within last {LOOKBACK_DAYS} days")

    pre_fix = [f for f in filtered if f["ts"] < FIX_DEPLOY_TS]
    post_fix = [f for f in filtered if f["ts"] >= FIX_DEPLOY_TS]

    def coverage(items, field, value=None):
        if not items:
            return 0.0
        if value is None:
            n = sum(1 for i in items if i["meta"].get(field) not in (None, ""))
        else:
            n = sum(1 for i in items if i["meta"].get(field) == value)
        return round(100.0 * n / len(items), 1)

    def avg(items, field):
        vals = [i["meta"].get(field) for i in items if isinstance(i["meta"].get(field), (int, float))]
        return round(sum(vals) / len(vals), 4) if vals else None

    def answered_rate(items):
        if not items:
            return None
        n = sum(1 for i in items if i["meta"].get("answered") is True)
        return round(100.0 * n / len(items), 1)

    def mode_split(items):
        modes = {}
        for i in items:
            m = i["meta"].get("selected_answer_mode") or "unset"
            modes[m] = modes.get(m, 0) + 1
        return modes

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "lookback_days": LOOKBACK_DAYS,
        "fix_deploy_ts_assumed": FIX_DEPLOY_TS.isoformat(),
        "total_traces_scanned": len(traces),
        "real_email_traces_in_window": len(filtered),
        "pre_fix_count": len(pre_fix),
        "post_fix_count": len(post_fix),
        "post_fix": {
            "session_id_source_client_pct": coverage(post_fix, "session_id_source", "client"),
            "session_id_source_fallback_pct": coverage(post_fix, "session_id_source", "correlation_fallback"),
            "turn_number_source_client_pct": coverage(post_fix, "turn_number_source", "client"),
            "turn_number_source_missing_pct": coverage(post_fix, "turn_number_source", "missing_client_support"),
            "parent_trace_id_provided_pct": coverage(post_fix, "parent_trace_id_provided", True),
            "answered_rate_pct": answered_rate(post_fix),
            "avg_confidence": avg(post_fix, "confidence"),
            "answer_mode_split": mode_split(post_fix),
        },
        "pre_fix": {
            "answered_rate_pct": answered_rate(pre_fix),
            "avg_confidence": avg(pre_fix, "confidence"),
            "answer_mode_split": mode_split(pre_fix),
        } if pre_fix else None,
    }

    # Conversation clustering by real email + 10-min proximity (post-fix only, real identity = clean signal)
    by_email = {}
    for f in post_fix:
        email = f["meta"].get("user_email")
        by_email.setdefault(email, []).append(f)

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

    multi_turn_clusters = [c for c in clusters if len(c) >= 2]
    first_pos = [c[0] for c in multi_turn_clusters]
    later_pos = [it for c in multi_turn_clusters for it in c[1:]]

    summary["email_based_conversation_clustering"] = {
        "unique_real_emails": len(by_email),
        "total_clusters": len(clusters),
        "multi_turn_clusters": len(multi_turn_clusters),
        "first_position_n": len(first_pos),
        "later_position_n": len(later_pos),
        "first_position_answered_rate_pct": answered_rate(first_pos),
        "later_position_answered_rate_pct": answered_rate(later_pos),
        "first_position_avg_confidence": avg(first_pos, "confidence"),
        "later_position_avg_confidence": avg(later_pos, "confidence"),
    }

    ts_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    json_path = REPORT_DIR / f"code_fix_effectiveness_{ts_str}.json"
    md_path = REPORT_DIR / f"CODE_FIX_EFFECTIVENESS_{ts_str}.md"

    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)

    md = f"""# Code Fix Effectiveness Analysis

Generated: {summary['generated_at']}
Scope: real-identity traces only (scrubbed/placeholder emails excluded), last {LOOKBACK_DAYS} days
Fix: commit a60b9e49 (session_id/turn_number/parent_trace_id provenance), assumed live from ~{FIX_DEPLOY_TS.isoformat()}

## Sample sizes
- Total kb_answer traces scanned: {summary['total_traces_scanned']}
- Real-email traces in window: {summary['real_email_traces_in_window']}
- Pre-fix (in window, before deploy): {summary['pre_fix_count']}
- Post-fix: {summary['post_fix_count']}

## Post-fix field coverage (real-identity traffic only)
- session_id_source = "client": {summary['post_fix']['session_id_source_client_pct']}%
- session_id_source = "correlation_fallback": {summary['post_fix']['session_id_source_fallback_pct']}%
- turn_number_source = "client": {summary['post_fix']['turn_number_source_client_pct']}%
- turn_number_source = "missing_client_support": {summary['post_fix']['turn_number_source_missing_pct']}%
- parent_trace_id_provided = true: {summary['post_fix']['parent_trace_id_provided_pct']}%
- Answered rate: {summary['post_fix']['answered_rate_pct']}%
- Avg confidence: {summary['post_fix']['avg_confidence']}
- Answer mode split: {summary['post_fix']['answer_mode_split']}

## Pre-fix comparison (same window, real-identity traffic)
{"- Answered rate: " + str(summary['pre_fix']['answered_rate_pct']) + "%" if summary['pre_fix'] else "(no pre-fix real-identity traces in window)"}
{"- Avg confidence: " + str(summary['pre_fix']['avg_confidence']) if summary['pre_fix'] else ""}
{"- Answer mode split: " + str(summary['pre_fix']['answer_mode_split']) if summary['pre_fix'] else ""}

## Email-based conversation clustering (post-fix, real identity — clean signal, no PII-scrubbing noise)
- Unique real emails: {summary['email_based_conversation_clustering']['unique_real_emails']}
- Total conversation clusters (10-min proximity): {summary['email_based_conversation_clustering']['total_clusters']}
- Multi-turn clusters (2+): {summary['email_based_conversation_clustering']['multi_turn_clusters']}
- First-position traces: {summary['email_based_conversation_clustering']['first_position_n']} | answered rate: {summary['email_based_conversation_clustering']['first_position_answered_rate_pct']}% | avg confidence: {summary['email_based_conversation_clustering']['first_position_avg_confidence']}
- Later-position traces: {summary['email_based_conversation_clustering']['later_position_n']} | answered rate: {summary['email_based_conversation_clustering']['later_position_answered_rate_pct']}% | avg confidence: {summary['email_based_conversation_clustering']['later_position_avg_confidence']}
"""

    with open(md_path, "w") as f:
        f.write(md)

    print(f"\nSaved: {json_path}")
    print(f"Saved: {md_path}")
    print("\n" + md)


if __name__ == "__main__":
    main()
