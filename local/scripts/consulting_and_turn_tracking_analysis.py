#!/usr/bin/env python3
"""
Consulting-mode + turn-tracking fix analysis — broadened scope.

Unlike the earlier code_fix_effectiveness_analysis.py (which filtered to
real-email traces from the last 3-4 days and ended up with n=30, all from
one tester), this script includes ALL traces that carry the NEW telemetry
fields added by the turn-tracking fix (session_id_source, turn_number_source,
parent_trace_id_provided) — since those fields only exist on traces that ran
through the fixed code, this filter is a natural "post-fix" boundary without
needing a manual date cutoff or identity filter.

Reads from the local Langfuse trace cache (local/cache/langfuse_traces_cache.json)
built by generate_analytics_dashboard.py — no live API calls, instant.
"""
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
CACHE_PATH = ROOT / "local" / "cache" / "langfuse_traces_cache.json"
REPORT_DIR = ROOT / "local" / "reports"

NEW_FIELDS = ["session_id_source", "turn_number_source", "parent_trace_id_provided"]


def load_cache():
    with open(CACHE_PATH) as f:
        data = json.load(f)
    return list(data["traces"].values())


def has_new_fields(trace):
    meta = trace.get("metadata") or {}
    if not isinstance(meta, dict):
        return False
    return any(f in meta for f in NEW_FIELDS)


def is_real_email(email):
    if not email or not isinstance(email, str):
        return False
    e = email.strip().lower()
    if e in ("", "unknown", "none"):
        return False
    if e.startswith("sess:") or e.startswith("exec:"):
        return False
    return "@" in e


def pct(n, d):
    return round(100.0 * n / d, 1) if d else 0.0


def avg(vals):
    vals = [v for v in vals if isinstance(v, (int, float))]
    return round(sum(vals) / len(vals), 4) if vals else None


def main():
    all_traces = load_cache()
    print(f"Total cached traces: {len(all_traces)}")

    fixed = [t for t in all_traces if has_new_fields(t)]
    print(f"Traces with new turn-tracking fields (post-fix): {len(fixed)}")

    metas = [t.get("metadata") or {} for t in fixed]

    # --- Field coverage ---
    session_client = sum(1 for m in metas if m.get("session_id_source") == "client")
    session_fallback = sum(1 for m in metas if m.get("session_id_source") == "correlation_fallback")
    turn_client = sum(1 for m in metas if m.get("turn_number_source") == "client")
    turn_missing = sum(1 for m in metas if m.get("turn_number_source") == "missing_client_support")
    parent_provided = sum(1 for m in metas if m.get("parent_trace_id_provided") is True)

    # --- Identity split ---
    real_email_metas = [m for m in metas if is_real_email(m.get("user_email"))]
    scrubbed_metas = [m for m in metas if not is_real_email(m.get("user_email"))]

    # --- Answer quality overall (post-fix) ---
    answered_n = sum(1 for m in metas if m.get("answered") is True)
    answer_rate = pct(answered_n, len(metas))
    avg_conf = avg([m.get("confidence") for m in metas])

    # --- Consulting vs standard mode ---
    mode_counts = {}
    for m in metas:
        mode = m.get("selected_answer_mode") or "unset"
        mode_counts[mode] = mode_counts.get(mode, 0) + 1

    consulting_metas = [m for m in metas if m.get("selected_answer_mode") == "consulting"]
    standard_metas = [m for m in metas if m.get("selected_answer_mode") == "standard"]

    consulting_answer_rate = pct(sum(1 for m in consulting_metas if m.get("answered") is True), len(consulting_metas))
    standard_answer_rate = pct(sum(1 for m in standard_metas if m.get("answered") is True), len(standard_metas))
    consulting_avg_conf = avg([m.get("confidence") for m in consulting_metas])
    standard_avg_conf = avg([m.get("confidence") for m in standard_metas])

    # --- trace_env split (PROD vs PROD_EXT) ---
    env_counts = {}
    for m in metas:
        env = m.get("trace_env") or "unset"
        env_counts[env] = env_counts.get(env, 0) + 1

    # --- Conversation clustering: real-email traces grouped by email + 10-min proximity ---
    def parse_ts(t):
        ts = t.get("timestamp")
        if isinstance(ts, str):
            return datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return ts

    real_email_traces = [t for t in fixed if is_real_email((t.get("metadata") or {}).get("user_email"))]
    for t in real_email_traces:
        t["_ts"] = parse_ts(t)
        t["_email"] = (t.get("metadata") or {}).get("user_email")

    by_email = {}
    for t in real_email_traces:
        by_email.setdefault(t["_email"], []).append(t)

    clusters = []
    for email, items in by_email.items():
        items.sort(key=lambda x: x["_ts"])
        cluster = [items[0]]
        for it in items[1:]:
            if (it["_ts"] - cluster[-1]["_ts"]).total_seconds() <= 600:
                cluster.append(it)
            else:
                clusters.append(cluster)
                cluster = [it]
        clusters.append(cluster)

    multi_turn_clusters = [c for c in clusters if len(c) >= 2]
    first_pos = [c[0] for c in multi_turn_clusters]
    later_pos = [it for c in multi_turn_clusters for it in c[1:]]

    def cluster_answer_rate(items):
        metas_ = [(t.get("metadata") or {}) for t in items]
        return pct(sum(1 for m in metas_ if m.get("answered") is True), len(metas_))

    def cluster_avg_conf(items):
        metas_ = [(t.get("metadata") or {}) for t in items]
        return avg([m.get("confidence") for m in metas_])

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_cached_traces": len(all_traces),
        "post_fix_traces_with_new_fields": len(fixed),
        "identity_split": {
            "real_email_traces": len(real_email_metas),
            "scrubbed_or_missing_email_traces": len(scrubbed_metas),
        },
        "field_coverage": {
            "session_id_source_client_pct": pct(session_client, len(metas)),
            "session_id_source_fallback_pct": pct(session_fallback, len(metas)),
            "turn_number_source_client_pct": pct(turn_client, len(metas)),
            "turn_number_source_missing_pct": pct(turn_missing, len(metas)),
            "parent_trace_id_provided_pct": pct(parent_provided, len(metas)),
        },
        "overall_answer_quality": {
            "answer_rate_pct": answer_rate,
            "avg_confidence": avg_conf,
        },
        "answer_mode_split": mode_counts,
        "consulting_vs_standard": {
            "consulting_n": len(consulting_metas),
            "standard_n": len(standard_metas),
            "consulting_adoption_pct": pct(len(consulting_metas), len(metas)),
            "consulting_answer_rate_pct": consulting_answer_rate,
            "standard_answer_rate_pct": standard_answer_rate,
            "consulting_avg_confidence": consulting_avg_conf,
            "standard_avg_confidence": standard_avg_conf,
        },
        "trace_env_split": env_counts,
        "conversation_clustering_real_email": {
            "unique_real_emails": len(by_email),
            "total_clusters": len(clusters),
            "multi_turn_clusters": len(multi_turn_clusters),
            "first_position_n": len(first_pos),
            "later_position_n": len(later_pos),
            "first_position_answered_rate_pct": cluster_answer_rate(first_pos),
            "later_position_answered_rate_pct": cluster_answer_rate(later_pos),
            "first_position_avg_confidence": cluster_avg_conf(first_pos),
            "later_position_avg_confidence": cluster_avg_conf(later_pos),
        },
    }

    ts_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    json_path = REPORT_DIR / f"consulting_turn_tracking_analysis_{ts_str}.json"
    md_path = REPORT_DIR / f"CONSULTING_TURN_TRACKING_ANALYSIS_{ts_str}.md"

    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)

    md = f"""# Consulting Mode + Turn-Tracking Fix Analysis (Broadened)

Generated: {summary['generated_at']}
Scope: ALL traces carrying the new turn-tracking fields (session_id_source, turn_number_source,
parent_trace_id_provided) — this is a natural post-fix boundary, no manual date/identity filter needed.
Source: local trace cache ({summary['total_cached_traces']} total traces, 90-day backfill).

## Sample size
- Post-fix traces (have new fields): **{summary['post_fix_traces_with_new_fields']}**
- Real-email traces: {summary['identity_split']['real_email_traces']}
- Scrubbed/missing-email traces: {summary['identity_split']['scrubbed_or_missing_email_traces']}

## Field coverage (confirms fix is deployed and behaving as designed)
- session_id_source = "client": {summary['field_coverage']['session_id_source_client_pct']}%
- session_id_source = "correlation_fallback": {summary['field_coverage']['session_id_source_fallback_pct']}%
- turn_number_source = "client": {summary['field_coverage']['turn_number_source_client_pct']}%
- turn_number_source = "missing_client_support": {summary['field_coverage']['turn_number_source_missing_pct']}%
- parent_trace_id_provided = true: {summary['field_coverage']['parent_trace_id_provided_pct']}%

## Overall answer quality (post-fix traffic)
- Answer rate: {summary['overall_answer_quality']['answer_rate_pct']}%
- Avg confidence: {summary['overall_answer_quality']['avg_confidence']}

## Answer mode split
{json.dumps(summary['answer_mode_split'], indent=2)}

## Consulting vs Standard mode
- Consulting: n={summary['consulting_vs_standard']['consulting_n']} ({summary['consulting_vs_standard']['consulting_adoption_pct']}% adoption)
- Standard: n={summary['consulting_vs_standard']['standard_n']}
- Consulting answer rate: {summary['consulting_vs_standard']['consulting_answer_rate_pct']}%
- Standard answer rate: {summary['consulting_vs_standard']['standard_answer_rate_pct']}%
- Consulting avg confidence: {summary['consulting_vs_standard']['consulting_avg_confidence']}
- Standard avg confidence: {summary['consulting_vs_standard']['standard_avg_confidence']}

## trace_env split
{json.dumps(summary['trace_env_split'], indent=2)}

## Conversation clustering (real-email traces only, email + 10-min proximity)
- Unique real emails: {summary['conversation_clustering_real_email']['unique_real_emails']}
- Total clusters: {summary['conversation_clustering_real_email']['total_clusters']}
- Multi-turn clusters (2+): {summary['conversation_clustering_real_email']['multi_turn_clusters']}
- First-position: n={summary['conversation_clustering_real_email']['first_position_n']}, answered={summary['conversation_clustering_real_email']['first_position_answered_rate_pct']}%, avg_conf={summary['conversation_clustering_real_email']['first_position_avg_confidence']}
- Later-position: n={summary['conversation_clustering_real_email']['later_position_n']}, answered={summary['conversation_clustering_real_email']['later_position_answered_rate_pct']}%, avg_conf={summary['conversation_clustering_real_email']['later_position_avg_confidence']}
"""

    with open(md_path, "w") as f:
        f.write(md)

    print(f"\nSaved: {json_path}")
    print(f"Saved: {md_path}")
    print("\n" + md)


if __name__ == "__main__":
    main()
