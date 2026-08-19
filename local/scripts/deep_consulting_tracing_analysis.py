#!/usr/bin/env python3
"""
Deep consulting-mode + tracing effectiveness analysis.

Goes beyond the summary in consulting_and_turn_tracking_analysis.py:
- Per-module consulting adoption (does it match configured traffic_pct?)
- Best-practices / fitment / case-study coverage within consulting-mode traces
- Turn-tracking field coverage broken out by trace_env
- Multi-turn clustering (real-email) with per-cluster detail
- Answer length delta consulting vs standard (goal was +engagement content)

Reads from the local trace cache (no live API calls).
"""
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
CACHE_PATH = ROOT / "local" / "cache" / "langfuse_traces_cache.json"
REPORT_DIR = ROOT / "local" / "reports"

NEW_FIELDS = ["session_id_source", "turn_number_source", "parent_trace_id_provided"]


def _load_configured_split():
    """Read CONSULTING_TONE_CONFIG['modules'] directly from skill/kb_answer.py
    instead of hardcoding a copy here, which silently goes stale every time
    the config changes (already happened once: this dict said RCS/Bot Studio
    were at 75% and didn't mention WhatsApp at all, after both had already
    been updated in the skill)."""
    sys.path.insert(0, str(ROOT / "skill"))
    import kb_answer as ka
    return dict(ka.CONSULTING_TONE_CONFIG["modules"])


CONFIGURED_SPLIT = _load_configured_split()


def load_cache():
    with open(CACHE_PATH) as f:
        data = json.load(f)
    return list(data["traces"].values())


def has_new_fields(trace):
    meta = trace.get("metadata") or {}
    return isinstance(meta, dict) and any(f in meta for f in NEW_FIELDS)


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
    return round(100.0 * n / d, 1) if d else None


def avg(vals):
    vals = [v for v in vals if isinstance(v, (int, float))]
    return round(sum(vals) / len(vals), 4) if vals else None


def main():
    traces = load_cache()
    fixed = [t for t in traces if has_new_fields(t)]
    metas = [(t.get("metadata") or {}) for t in fixed]
    answers = [(t.get("output") or {}).get("answer", "") for t in fixed]

    print(f"Total cached traces: {len(traces)}")
    print(f"Post-fix traces: {len(fixed)}\n")

    # --- Per-module adoption vs configured split ---
    # Uses the TRUE routing-time module (_detect_module(query), the actual
    # value _resolve_answer_mode gates on) rather than telemetry's "module"
    # field. Those two differ whenever a query is detected as "General" at
    # routing time (correctly gated to standard, unrelated to traffic_pct)
    # but telemetry later relabels module post-hoc from the top-scored
    # evidence source. Using telemetry's module as the denominator produces
    # systematically wrong adoption rates for EVERY gated module, not just
    # one — confirmed by re-checking Bot Studio at 100% traffic_pct: the
    # telemetry-label method showed 62.5% adoption (looked like a bug), but
    # the true-module method showed exactly 100% (matches config exactly).
    sys.path.insert(0, str(ROOT / "skill"))
    import kb_answer as ka

    print("=" * 70)
    print("PER-MODULE CONSULTING ADOPTION vs CONFIGURED SPLIT (true routing-time module)")
    print("=" * 70)
    by_module = {}
    for m in metas:
        q = m.get("query") or ""
        if not q:
            continue
        mod = ka._detect_module(q)
        by_module.setdefault(mod, {"consulting": 0, "standard": 0, "other": 0})
        mode = m.get("selected_answer_mode")
        if mode == "consulting":
            by_module[mod]["consulting"] += 1
        elif mode == "standard":
            by_module[mod]["standard"] += 1
        else:
            by_module[mod]["other"] += 1

    for mod, counts in sorted(by_module.items()):
        total = sum(counts.values())
        configured = CONFIGURED_SPLIT.get(mod)
        adoption = pct(counts["consulting"], total)
        flag = ""
        if configured is not None and adoption is not None:
            delta = adoption - configured
            flag = f"  (configured={configured}%, delta={delta:+.1f}pp)"
        elif mod not in CONFIGURED_SPLIT:
            flag = "  (not in consulting-mode allowlist -> should be 0% consulting)"
        print(f"  {mod:20s} n={total:3d}  consulting={counts['consulting']:2d} ({adoption}%){flag}")

    # --- Engagement content coverage within consulting-mode traces ---
    print()
    print("=" * 70)
    print("ENGAGEMENT CONTENT COVERAGE (within consulting-mode answers)")
    print("=" * 70)
    consulting_idx = [i for i, m in enumerate(metas) if m.get("selected_answer_mode") == "consulting"]
    consulting_answers = [answers[i] for i in consulting_idx]
    consulting_metas = [metas[i] for i in consulting_idx]

    n_bp = sum(1 for a in consulting_answers if "**Best practices:**" in a)
    n_fit = sum(1 for a in consulting_answers if "This also connects well with" in a)
    n_cs = sum(1 for a in consulting_answers if "Related success stories" in a or "See it in action" in a)
    n_video = sum(1 for a in consulting_answers if "Watch:" in a or "demoforge" in a.lower())

    print(f"  Consulting-mode traces: {len(consulting_answers)}")
    print(f"  Best Practices section present: {n_bp} ({pct(n_bp, len(consulting_answers))}%)")
    print(f"  Fitment (\"connects well with\") present: {n_fit} ({pct(n_fit, len(consulting_answers))}%)")
    print(f"  Case study / demo present: {n_cs} ({pct(n_cs, len(consulting_answers))}%)")
    print(f"  Video link present: {n_video} ({pct(n_video, len(consulting_answers))}%)")

    # --- Answer length: consulting vs standard (engagement-content goal check) ---
    print()
    print("=" * 70)
    print("ANSWER LENGTH: consulting vs standard (goal: consulting should be richer)")
    print("=" * 70)
    standard_idx = [i for i, m in enumerate(metas) if m.get("selected_answer_mode") == "standard"]
    consulting_lens = [len(answers[i]) for i in consulting_idx]
    standard_lens = [len(answers[i]) for i in standard_idx]
    print(f"  Consulting avg length: {avg(consulting_lens)} chars (n={len(consulting_lens)})")
    print(f"  Standard avg length:   {avg(standard_lens)} chars (n={len(standard_lens)})")
    if avg(consulting_lens) and avg(standard_lens):
        delta_pct = round(100.0 * (avg(consulting_lens) - avg(standard_lens)) / avg(standard_lens), 1)
        print(f"  Delta: {delta_pct:+.1f}%")

    # --- Accuracy comparison ---
    print()
    print("=" * 70)
    print("ACCURACY: consulting vs standard")
    print("=" * 70)
    def answered_rate(idxs):
        if not idxs:
            return None
        n = sum(1 for i in idxs if metas[i].get("answered") is True)
        return pct(n, len(idxs))
    def conf(idxs):
        return avg([metas[i].get("confidence") for i in idxs])
    print(f"  Consulting: answered={answered_rate(consulting_idx)}% avg_conf={conf(consulting_idx)} (n={len(consulting_idx)})")
    print(f"  Standard:   answered={answered_rate(standard_idx)}% avg_conf={conf(standard_idx)} (n={len(standard_idx)})")

    # --- Turn-tracking field coverage by trace_env ---
    print()
    print("=" * 70)
    print("TURN-TRACKING FIELD COVERAGE BY trace_env")
    print("=" * 70)
    by_env = {}
    for m in metas:
        env = m.get("trace_env") or "unset"
        by_env.setdefault(env, []).append(m)
    for env, ms in sorted(by_env.items()):
        n = len(ms)
        client_sid = sum(1 for m in ms if m.get("session_id_source") == "client")
        real_sid = sum(1 for m in ms if is_real_email(m.get("user_email")))
        print(f"  {env:12s} n={n:3d}  session_id_source=client: {client_sid} ({pct(client_sid,n)}%)  real_email: {real_sid} ({pct(real_sid,n)}%)")

    # --- Multi-turn clustering detail ---
    print()
    print("=" * 70)
    print("MULTI-TURN CONVERSATION CLUSTERS (real email, 10-min proximity)")
    print("=" * 70)
    real_email_traces = [
        {"ts": t["timestamp"] if isinstance(t.get("timestamp"), datetime) else datetime.fromisoformat(str(t["timestamp"]).replace("Z", "+00:00")),
         "email": (t.get("metadata") or {}).get("user_email"),
         "meta": t.get("metadata") or {}}
        for t in fixed if is_real_email((t.get("metadata") or {}).get("user_email"))
    ]
    by_email = {}
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
                clusters.append((email, cluster))
                cluster = [it]
        clusters.append((email, cluster))

    multi = [(e, c) for e, c in clusters if len(c) >= 2]
    print(f"  {len(multi)} multi-turn clusters found:")
    for email, cluster in multi:
        modes = [c["meta"].get("selected_answer_mode") for c in cluster]
        answered = [c["meta"].get("answered") for c in cluster]
        queries = [c["meta"].get("query", "")[:50] for c in cluster]
        print(f"    {email} ({len(cluster)} turns): modes={modes} answered={answered}")
        for q in queries:
            print(f"      - {q}")

    # Save JSON summary
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_cached": len(traces),
        "post_fix": len(fixed),
        "per_module_adoption": {
            mod: {**counts, "adoption_pct": pct(counts["consulting"], sum(counts.values())),
                  "configured_pct": CONFIGURED_SPLIT.get(mod)}
            for mod, counts in by_module.items()
        },
        "engagement_coverage": {
            "consulting_n": len(consulting_answers),
            "best_practices_pct": pct(n_bp, len(consulting_answers)),
            "fitment_pct": pct(n_fit, len(consulting_answers)),
            "case_study_pct": pct(n_cs, len(consulting_answers)),
            "video_pct": pct(n_video, len(consulting_answers)),
        },
        "answer_length": {
            "consulting_avg": avg(consulting_lens),
            "standard_avg": avg(standard_lens),
        },
        "accuracy": {
            "consulting_answered_pct": answered_rate(consulting_idx),
            "consulting_avg_conf": conf(consulting_idx),
            "standard_answered_pct": answered_rate(standard_idx),
            "standard_avg_conf": conf(standard_idx),
        },
        "multi_turn_clusters": len(multi),
    }
    ts_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    out_path = REPORT_DIR / f"deep_consulting_tracing_analysis_{ts_str}.json"
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
