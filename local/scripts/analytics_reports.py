"""Report builders and rule-based qualitative insights (local analytics only)."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

from analytics_common import (
    LOW_SCORE_THRESHOLD,
    QueryEvent,
    VideoEvent,
    date_key,
    is_internal_email,
    module_from_source,
    pct,
    pct_str,
    simple_theme,
    utc_now,
)

Insight = Dict[str, str]  # severity, text


def _top_counter(c: Counter, n: int = 15) -> List[Dict[str, Any]]:
    total = sum(c.values()) or 1
    return [
        {"label": k, "count": v, "pct": pct_str(v, total)}
        for k, v in c.most_common(n)
    ]


def _module_stats(events: List[QueryEvent]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {"queries": 0, "idk": 0, "answered": 0, "video_attached": 0, "scores": []}
    )
    for e in events:
        m = out[e.module]
        m["queries"] += 1
        if e.idk:
            m["idk"] += 1
        if e.answered:
            m["answered"] += 1
        if e.video_attached:
            m["video_attached"] += 1
        if e.top_score is not None:
            m["scores"].append(e.top_score)
    for m in out.values():
        q = m["queries"] or 1
        m["idk_rate"] = pct(m["idk"], q)
        m["answer_rate"] = pct(m["answered"], q)
        m["video_rate"] = pct(m["video_attached"], q)
        sc = m.pop("scores")
        m["avg_top_score"] = round(sum(sc) / len(sc), 2) if sc else None
    return dict(out)


def build_all_reports(
    all_events: List[QueryEvent],
    all_videos: List[VideoEvent],
    window_3d: List[QueryEvent],
    window_30d: List[QueryEvent],
    videos_30d: List[VideoEvent],
    video_clicks_30d: int,
    prev_3d: List[QueryEvent],
    kb_paths: set,
    chunks_per_module: Counter,
    manifest_covered: set,
    manifest_entries: List[Dict],
    pitch_modules: set,
) -> Dict[str, Any]:
    unmapped_paths = sorted(p for p in kb_paths if p not in manifest_covered)
    unmapped_by_module = Counter(module_from_source(p) for p in unmapped_paths)

    # --- Popularity (B*) ---
    mod_30 = Counter(e.module for e in window_30d)
    mod_3 = Counter(e.module for e in window_3d)
    src_30 = Counter(e.top_source for e in window_30d if e.top_source)
    src_3 = Counter(e.top_source for e in window_3d if e.top_source)

    # --- Users (C*) ---
    user_30 = Counter(e.user_email for e in window_30d if e.user_email)
    user_3 = Counter(e.user_email for e in window_3d if e.user_email)
    leaderboard = []
    for email, count in user_30.most_common(50):
        user_ev = [e for e in window_30d if e.user_email == email]
        mods = Counter(e.module for e in user_ev)
        idk_n = sum(1 for e in user_ev if e.idk)
        leaderboard.append({
            "user_email": email,
            "queries_30d": count,
            "queries_3d": user_3.get(email, 0),
            "internal": is_internal_email(email),
            "top_modules": _top_counter(mods, 5),
            "idk_rate": pct_str(idk_n, len(user_ev)),
            "idk_count": idk_n,
        })

    one_shot = sum(1 for _, c in user_30.items() if c == 1)
    power_users = sum(1 for _, c in user_30.items() if c >= 5)

    # --- Quality (D*) ---
    mod_stats_30 = _module_stats(window_30d)
    idk_by_source = Counter(e.top_source for e in window_30d if e.idk and e.top_source)
    low_conf_answered = [
        e for e in window_30d
        if e.answered and e.top_score is not None and e.top_score < LOW_SCORE_THRESHOLD
    ]
    themes_30 = Counter(simple_theme(e.query) for e in window_30d if e.query)

    backlog = []
    for mod, st in mod_stats_30.items():
        if st["queries"] < 2:
            continue
        idk_r = st["idk"] / st["queries"]
        avg_sc = st["avg_top_score"] or 0
        priority = st["queries"] * (0.5 + idk_r) * (2.0 - min(avg_sc, 2.0))
        backlog.append({
            "module": mod,
            "queries": st["queries"],
            "idk_rate": st["idk_rate"],
            "priority_score": round(priority, 2),
            "avg_top_score": st["avg_top_score"],
        })
    backlog.sort(key=lambda x: -x["priority_score"])

    sample_queries: Dict[str, List[str]] = defaultdict(list)
    for e in window_30d:
        if e.idk and e.query:
            key = e.top_source or e.module
            if len(sample_queries[key]) < 3:
                sample_queries[key].append(e.query[:280])

    # --- Video (E*) + static (A*) ---
    lf_answer_30 = [e for e in window_30d if e.action == "kb_answer" and e.source == "langfuse"]
    video_attach_n = sum(1 for e in lf_answer_30 if e.video_attached)
    video_append_n = sum(1 for e in lf_answer_30 if e.video_appended)
    fallback_n = sum(1 for e in lf_answer_30 if e.video_fallback)

    hot_sources_no_video = []
    for src, cnt in src_30.most_common(30):
        att = sum(1 for e in window_30d if e.top_source == src and e.video_attached)
        if cnt >= 2 and att == 0:
            hot_sources_no_video.append({"source": src, "queries": cnt, "module": module_from_source(src)})

    manifest_sources_hit = Counter()
    for e in window_30d:
        if e.top_source in manifest_covered:
            manifest_sources_hit[e.top_source] += 1
    never_hit_manifest = []
    for ent in manifest_entries:
        src = str(ent.get("source") or "")
        if src and manifest_sources_hit.get(src, 0) == 0:
            never_hit_manifest.append({"source": src, "title": ent.get("title"), "module": module_from_source(src)})

    vid_delivered = Counter()
    for v in videos_30d:
        if v.video_id:
            vid_delivered[v.video_id] += 1

    # --- Investment (G*) ---
    matrix = []
    for mod, st in mod_stats_30.items():
        doc_chunks = chunks_per_module.get(mod, 0)
        matrix.append({
            "module": mod,
            "queries": st["queries"],
            "answer_rate": st["answer_rate"],
            "idk_rate": st["idk_rate"],
            "doc_chunks": doc_chunks,
            "queries_per_100_chunks": round(100 * st["queries"] / doc_chunks, 1) if doc_chunks else None,
        })
    matrix.sort(key=lambda x: -x["queries"])

    rising_modules = []
    for mod in set(mod_3) | set(mod_30):
        c3 = mod_3.get(mod, 0)
        c30 = mod_30.get(mod, 0)
        if c30 >= 5:
            rising_modules.append({
                "module": mod,
                "queries_3d": c3,
                "queries_30d": c30,
                "share_3d": pct_str(c3, len(window_3d) or 1),
            })
    rising_modules.sort(key=lambda x: -x["queries_3d"])

    # --- Ops (F*) ---
    latencies = [e.latency_ms for e in window_30d if e.latency_ms]
    latencies.sort()
    p50 = latencies[len(latencies) // 2] if latencies else None
    p95 = latencies[int(len(latencies) * 0.95)] if len(latencies) >= 10 else (latencies[-1] if latencies else None)
    env_c = Counter(e.environment for e in window_30d)
    action_c = Counter(e.action for e in window_30d)
    source_c = Counter(e.source for e in window_30d)

    search_30 = [e for e in window_30d if e.action == "kb_search"]
    answer_30 = [e for e in window_30d if e.action == "kb_answer"]

    external_30 = [e for e in window_30d if e.user_email and not is_internal_email(e.user_email)]
    internal_30 = [e for e in window_30d if is_internal_email(e.user_email)]

    pitch_queries = [e for e in window_30d if simple_theme(e.query) == "pitch_capability"]

    reports = {
        "A1_video_manifest_gaps_by_module": {
            "unmapped_doc_count": len(unmapped_paths),
            "by_module": _top_counter(unmapped_by_module, 20),
            "sample_unmapped_paths": unmapped_paths[:40],
        },
        "A2_hot_pages_without_video": hot_sources_no_video[:25],
        "A3_manifest_never_hit": never_hit_manifest[:25],
        "A4_pitch_coverage": {
            "pitch_modules_in_manifest": sorted(pitch_modules),
            "pitch_queries_30d": len(pitch_queries),
        },
        "A5_kb_inventory_by_module": _top_counter(chunks_per_module, 20),
        "B1_module_popularity_30d": _top_counter(mod_30, 20),
        "B1_module_popularity_3d": _top_counter(mod_3, 20),
        "B2_topic_popularity_30d": _top_counter(src_30, 25),
        "B2_topic_popularity_3d": _top_counter(src_3, 15),
        "B3_intent_mode_mix_30d": {
            "intents": _top_counter(Counter(i for e in window_30d for i in e.intents), 20),
            "modes": _top_counter(Counter(e.mode for e in window_30d if e.mode), 15),
        },
        "B4_cross_module_users": _cross_module_users(window_30d),
        "B5_audience_split_30d": {
            "internal_queries": len(internal_30),
            "external_queries": len(external_30),
            "unknown_user": len(window_30d) - len(internal_30) - len(external_30),
        },
        "B6_emerging_modules": rising_modules[:15],
        "B7_pitch_queries": len(pitch_queries),
        "C1_user_leaderboard": leaderboard,
        "C2_user_depth": {"one_shot_users": one_shot, "power_users_5plus": power_users, "unique_users_30d": len(user_30)},
        "C3_inactive_internal": [],  # filled from state in main
        "D1_idk_by_module": [
            {"module": m, **{k: st[k] for k in ("queries", "idk", "idk_rate")}}
            for m, st in sorted(mod_stats_30.items(), key=lambda x: -x[1]["idk"])
        ],
        "D1_idk_by_source": _top_counter(idk_by_source, 20),
        "D2_low_confidence_answered": len(low_conf_answered),
        "D2_samples": [
            {"query": e.query[:200], "top_source": e.top_source, "top_score": e.top_score}
            for e in low_conf_answered[:15]
        ],
        "D3_query_themes_30d": _top_counter(themes_30, 12),
        "D4_compare_troubleshoot_pain": _intent_pain(window_30d, ("compare", "troubleshooting")),
        "D5_clarification_refusal": {
            "clarification": sum(1 for e in window_30d if e.clarification),
            "refusal": sum(1 for e in window_30d if e.refusal),
        },
        "D7_editorial_backlog": backlog[:20],
        "D8_sample_idk_queries": dict(list(sample_queries.items())[:15]),
        "E1_video_attach_rate": {
            "denominator_langfuse_kb_answer": len(lf_answer_30),
            "attached": video_attach_n,
            "pct": pct_str(video_attach_n, len(lf_answer_30) or 1),
            "appended": video_append_n,
            "fallback": fallback_n,
        },
        "E4_top_videos_delivered": _top_counter(vid_delivered, 15),
        "E5_video_funnel": {
            "delivered_30d": len(videos_30d),
            "clicked_30d": video_clicks_30d,
            "conversion_pct": pct_str(video_clicks_30d, len(videos_30d) or 1),
            "note": "video.clicked events require agent UI to call kb_analytics",
        },
        "E7_video_backlog_union": _video_backlog(hot_sources_no_video, backlog),
        "F1_latency": {"p50_ms": p50, "p95_ms": p95, "samples": len(latencies)},
        "F2_data_sources_30d": dict(source_c),
        "F3_environments": _top_counter(env_c, 10),
        "F4_action_mix": dict(action_c),
        "F5_search_vs_answer": {"kb_answer": len(answer_30), "kb_search": len(search_30)},
        "G1_investment_matrix": matrix[:20],
        "G2_demand_vs_doc_size": matrix[:15],
        "G3_rising_demand_3d": rising_modules[:12],
        "G4_pitch_gap": {
            "pitch_queries": len(pitch_queries),
            "pitch_modules": sorted(pitch_modules),
        },
        "G6_voice_whatsapp_interest": {
            "voice": sum(1 for e in window_30d if simple_theme(e.query) == "voice_pstn"),
            "whatsapp": sum(1 for e in window_30d if simple_theme(e.query) == "whatsapp"),
            "integration": sum(1 for e in window_30d if simple_theme(e.query) == "integration_handover"),
        },
        "summary_counts": {
            "all_events_deduped": len(all_events),
            "window_30d": len(window_30d),
            "window_3d": len(window_3d),
            "prev_window_3d": len(prev_3d),
            "videos_30d": len(videos_30d),
        },
    }
    return reports


def _cross_module_users(events: List[QueryEvent]) -> List[Dict[str, Any]]:
    per_user: Dict[str, set] = defaultdict(set)
    for e in events:
        if e.user_email:
            per_user[e.user_email].add(e.module)
    rows = []
    for email, mods in per_user.items():
        if len(mods) >= 2:
            rows.append({"user_email": email, "module_count": len(mods), "modules": sorted(mods)})
    rows.sort(key=lambda x: -x["module_count"])
    return rows[:25]


def _intent_pain(events: List[QueryEvent], labels: Tuple[str, ...]) -> List[Dict[str, Any]]:
    rows = []
    for lab in labels:
        sub = [e for e in events if lab in e.intents or lab in e.mode]
        if not sub:
            continue
        idk = sum(1 for e in sub if e.idk)
        rows.append({"intent": lab, "queries": len(sub), "idk": idk, "idk_rate": pct_str(idk, len(sub))})
    return rows


def _video_backlog(hot_no_video: List[Dict], backlog: List[Dict]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for row in hot_no_video[:10]:
        key = row.get("source") or row.get("module")
        if key in seen:
            continue
        seen.add(key)
        out.append({"type": "high_traffic_no_video", **row})
    for row in backlog[:10]:
        m = row["module"]
        if m in seen:
            continue
        seen.add(m)
        out.append({"type": "high_idk_module", "module": m, "idk_rate": row["idk_rate"], "queries": row["queries"]})
    return out


def build_insights(
    reports: Dict[str, Any],
    window_30d: List[QueryEvent],
    window_3d: List[QueryEvent],
    prev_3d: List[QueryEvent],
    daily_trend: List[Dict[str, Any]],
) -> List[Insight]:
    insights: List[Insight] = []
    n30 = len(window_30d) or 1
    n3 = len(window_3d) or 1
    nprev = len(prev_3d) or 1

    idk_30 = sum(1 for e in window_30d if e.idk)
    if pct(idk_30, n30) >= 20:
        insights.append({
            "severity": "high",
            "text": f"IDK/unanswered rate is {pct_str(idk_30, n30)} over 30 days — prioritize doc gaps in top modules from report D1.",
        })

    delta_q = n3 - nprev
    if nprev > 0 and abs(delta_q) >= max(3, 0.2 * nprev):
        direction = "up" if delta_q > 0 else "down"
        insights.append({
            "severity": "info",
            "text": f"Query volume in the last 3 days is {direction} ({n3} vs {nprev} in the prior 3-day window).",
        })

    hot = reports.get("A2_hot_pages_without_video") or []
    if hot:
        top = hot[0]
        insights.append({
            "severity": "medium",
            "text": f"High-traffic page without video: {top.get('source')} ({top.get('queries')} queries) — consider manifest mapping or new walkthrough.",
        })

    gaps = reports.get("A1_video_manifest_gaps_by_module") or {}
    um = gaps.get("unmapped_doc_count") or 0
    if um > 50:
        insights.append({
            "severity": "medium",
            "text": f"{um} indexed KB doc paths have no video manifest entry — review A1 by module before filming new content.",
        })

    ext = (reports.get("B5_audience_split_30d") or {}).get("external_queries", 0)
    if ext > 0 and ext >= 0.15 * n30:
        insights.append({
            "severity": "info",
            "text": f"Non-internal users account for {pct_str(ext, n30)} of 30-day queries — weight B1/C1 toward external domains for sales enablement.",
        })

    attach = reports.get("E1_video_attach_rate") or {}
    if attach.get("denominator_langfuse_kb_answer", 0) >= 5:
        ap = attach.get("pct", "0%")
        if float(ap.rstrip("%")) < 25:
            insights.append({
                "severity": "medium",
                "text": f"Video attach rate on Langfuse kb_answer traces is only {ap} — tune manifest also_sources or chapter windows (E1/E6).",
            })

    backlog = reports.get("D7_editorial_backlog") or []
    if backlog:
        b0 = backlog[0]
        insights.append({
            "severity": "high",
            "text": f"Top editorial priority: {b0.get('module')} (priority score {b0.get('priority_score')}, IDK rate {b0.get('idk_rate')}).",
        })

    lb = reports.get("C1_user_leaderboard") or []
    if lb:
        insights.append({
            "severity": "info",
            "text": f"Most active user (30d): {lb[0].get('user_email')} with {lb[0].get('queries_30d')} queries.",
        })

    themes = reports.get("D3_query_themes_30d") or []
    if themes:
        insights.append({
            "severity": "info",
            "text": f"Dominant query theme: {themes[0].get('label')} ({themes[0].get('count')} queries) — align KB and video scripts to this pattern.",
        })

    g6 = reports.get("G6_voice_whatsapp_interest") or {}
    if (g6.get("integration") or 0) >= 5:
        insights.append({
            "severity": "medium",
            "text": "Integration/handover themed queries are frequent — expand Agent Assist / API handover docs and demo videos.",
        })

    if daily_trend:
        last7 = daily_trend[-7:]
        counts = [d.get("queries", 0) for d in last7]
        if counts and max(counts) > 2 * (sum(counts) / len(counts) + 0.1):
            peak = max(last7, key=lambda d: d.get("queries", 0))
            insights.append({
                "severity": "info",
                "text": f"Recent spike on {peak.get('date')}: {peak.get('queries')} queries (7-day view).",
            })

    if not insights:
        insights.append({
            "severity": "info",
            "text": "Insufficient volume for strong signals in this window — keep collecting traces and NDJSON events.",
        })
    return insights


def update_state(
    state: Dict[str, Any],
    all_events: List[QueryEvent],
    run_id: str,
) -> Dict[str, Any]:
    state.setdefault("version", 1)
    state.setdefault("daily", {})
    state.setdefault("cumulative", {"total_queries": 0, "by_module": {}, "by_user": {}})
    state.setdefault("runs", [])

    daily: Dict[str, Dict[str, int]] = state["daily"]
    for e in all_events:
        dk = date_key(e.ts)
        day = daily.setdefault(dk, {"queries": 0, "idk": 0, "kb_answer": 0, "kb_search": 0})
        day["queries"] += 1
        if e.idk:
            day["idk"] += 1
        if e.action == "kb_answer":
            day["kb_answer"] += 1
        else:
            day["kb_search"] += 1

    # Trim daily to last 90 days
    cutoff = (utc_now() - timedelta(days=90)).strftime("%Y-%m-%d")
    state["daily"] = {k: v for k, v in daily.items() if k >= cutoff}

    cum = state["cumulative"]
    cum["total_queries"] = len(all_events)
    cum["by_module"] = dict(Counter(e.module for e in all_events))
    cum["by_user"] = dict(Counter(e.user_email for e in all_events if e.user_email))

    state["last_run"] = run_id
    state["runs"] = (state.get("runs") or [])[-29:]
    return state


def daily_trend_series(state: Dict[str, Any], days: int = 30) -> List[Dict[str, Any]]:
    daily = state.get("daily") or {}
    end = utc_now().date()
    series = []
    for i in range(days - 1, -1, -1):
        d = (end - timedelta(days=i)).strftime("%Y-%m-%d")
        row = daily.get(d) or {}
        series.append({
            "date": d,
            "queries": row.get("queries", 0),
            "idk": row.get("idk", 0),
            "kb_answer": row.get("kb_answer", 0),
        })
    return series
