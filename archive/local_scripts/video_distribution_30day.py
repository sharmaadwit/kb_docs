#!/usr/bin/env python3
"""
30-Day Video & Distribution Metrics from live Langfuse traces.
Fetches LIVE data via Langfuse REST API (never cached).
"""

import json
import os
import base64
import urllib.request
import urllib.parse
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict


def load_env():
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


def fetch_traces(days=30):
    load_env()
    host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")
    pub = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
    sec = os.environ.get("LANGFUSE_SECRET_KEY", "")
    if not (pub and sec):
        raise SystemExit("Missing Langfuse credentials in .env")

    creds = base64.b64encode(f"{pub}:{sec}".encode()).decode()
    headers = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}

    from_dt = datetime.utcnow() - timedelta(days=days)
    from_date = from_dt.strftime("%Y-%m-%dT00:00:00Z")

    all_traces = []
    page = 1
    while True:
        params = urllib.parse.urlencode({"page": page, "limit": 100, "fromTimestamp": from_date})
        url = f"{host}/api/public/traces?{params}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read())
        batch = body.get("data", [])
        all_traces.extend(batch)
        meta = body.get("meta", {})
        total = meta.get("totalItems", meta.get("total", len(all_traces)))
        print(f"  page {page}: +{len(batch)} (running {len(all_traces)}/{total})")
        if not batch or len(all_traces) >= total:
            break
        page += 1
    return all_traces, from_date


def pct(n, d):
    return round(n / d * 100, 1) if d else 0.0


def main():
    print("Fetching 30-day Langfuse traces...")
    traces, from_date = fetch_traces(30)
    today = datetime.utcnow().strftime("%Y-%m-%d")

    total = 0
    total_videos = 0
    video_by_module = defaultdict(int)
    video_by_intent = defaultdict(int)

    modules = defaultdict(lambda: {"count": 0, "answered": 0, "idk": 0, "conf": 0.0, "video": 0})
    intents = defaultdict(lambda: {"count": 0, "answered": 0, "idk": 0, "conf": 0.0, "video": 0})

    for tr in traces:
        meta = tr.get("metadata") or {}
        # Skip owner's own test queries (consistent with dashboard logic)
        if meta.get("user_email") == "adwit.sharma@gupshup.io":
            continue

        total += 1
        is_answered = bool(meta.get("answered", False))
        has_video = bool(meta.get("video_attached", False))
        conf = float(meta.get("top_score") or 0.0)

        if has_video:
            total_videos += 1

        module = meta.get("module_label", "Unknown") or "Unknown"
        m = modules[module]
        m["count"] += 1
        m["conf"] += conf
        if is_answered:
            m["answered"] += 1
        else:
            m["idk"] += 1
        if has_video:
            m["video"] += 1
            video_by_module[module] += 1

        intent_list = meta.get("intent_labels") or []
        if not intent_list:
            intent_list = ["(none)"]
        for intent in intent_list:
            it = intents[intent]
            it["count"] += 1
            it["conf"] += conf
            if is_answered:
                it["answered"] += 1
            else:
                it["idk"] += 1
            if has_video:
                it["video"] += 1
                video_by_intent[intent] += 1

    # Build sorted rows
    mod_rows = sorted(modules.items(), key=lambda x: x[1]["count"], reverse=True)
    int_rows = sorted(intents.items(), key=lambda x: x[1]["count"], reverse=True)

    out = []
    out.append("=" * 78)
    out.append(f"REPORT: 30-Day Analytics ({from_date[:10]} to {today})")
    out.append("=" * 78)
    out.append(f"Total Traces: {total}")
    out.append(f"Total Videos Shown: {total_videos} ({pct(total_videos, total)}% of all traces)")
    out.append("")

    out.append("VIDEO DISTRIBUTION BY MODULE:")
    if video_by_module:
        for mod, c in sorted(video_by_module.items(), key=lambda x: x[1], reverse=True):
            out.append(f"  {mod}: {c} videos shown")
    else:
        out.append("  (no videos attached in window)")
    out.append("")

    out.append("VIDEO DISTRIBUTION BY INTENT:")
    if video_by_intent:
        for it, c in sorted(video_by_intent.items(), key=lambda x: x[1], reverse=True):
            out.append(f"  {it}: {c} videos shown")
    else:
        out.append("  (no videos attached in window)")
    out.append("")

    # Module distribution table
    out.append("MODULE DISTRIBUTION:")
    hdr = f"  {'Module':<32}{'Queries':>9}{'Ans%':>8}{'IDK%':>8}{'AvgConf':>9}{'Video%':>9}"
    out.append(hdr)
    out.append("  " + "-" * (len(hdr) - 2))
    for mod, d in mod_rows:
        avg_conf = round(d["conf"] / d["count"], 2) if d["count"] else 0.0
        name = mod if len(mod) <= 32 else mod[:29] + "..."
        out.append(
            f"  {name:<32}{d['count']:>9}{pct(d['answered'], d['count']):>8}"
            f"{pct(d['idk'], d['count']):>8}{avg_conf:>9}{pct(d['video'], d['count']):>9}"
        )
    out.append("")

    # Intent distribution table
    out.append("INTENT DISTRIBUTION:")
    hdr2 = f"  {'Intent':<32}{'Queries':>9}{'Ans%':>8}{'IDK%':>8}{'AvgConf':>9}{'Video%':>9}"
    out.append(hdr2)
    out.append("  " + "-" * (len(hdr2) - 2))
    for it, d in int_rows:
        avg_conf = round(d["conf"] / d["count"], 2) if d["count"] else 0.0
        name = it if len(it) <= 32 else it[:29] + "..."
        out.append(
            f"  {name:<32}{d['count']:>9}{pct(d['answered'], d['count']):>8}"
            f"{pct(d['idk'], d['count']):>8}{avg_conf:>9}{pct(d['video'], d['count']):>9}"
        )

    report = "\n".join(out)
    print()
    print(report)

    # Save JSON alongside reports
    json_out = {
        "window": {"from": from_date[:10], "to": today, "days": 30},
        "total_traces": total,
        "total_videos_shown": total_videos,
        "video_rate_pct": pct(total_videos, total),
        "video_by_module": dict(video_by_module),
        "video_by_intent": dict(video_by_intent),
        "module_distribution": {
            mod: {
                "total_queries": d["count"],
                "answered_count": d["answered"],
                "answer_rate": pct(d["answered"], d["count"]),
                "idk_rate": pct(d["idk"], d["count"]),
                "avg_confidence": round(d["conf"] / d["count"], 2) if d["count"] else 0.0,
                "videos_shown_count": d["video"],
                "video_rate": pct(d["video"], d["count"]),
            }
            for mod, d in mod_rows
        },
        "intent_distribution": {
            it: {
                "total_queries": d["count"],
                "answered_count": d["answered"],
                "answer_rate": pct(d["answered"], d["count"]),
                "idk_rate": pct(d["idk"], d["count"]),
                "avg_confidence": round(d["conf"] / d["count"], 2) if d["count"] else 0.0,
                "videos_shown_count": d["video"],
                "video_rate": pct(d["video"], d["count"]),
            }
            for it, d in int_rows
        },
    }
    out_path = Path(__file__).parent.parent / "reports" / "video_distribution_30day.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(json_out, f, indent=2)
    print(f"\nJSON saved to: {out_path}")


if __name__ == "__main__":
    main()
