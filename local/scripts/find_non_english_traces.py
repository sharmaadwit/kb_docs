#!/usr/bin/env python3
"""
Fetch last 30 days of Langfuse traces, detect non-English queries, and extract
action/intent terms to validate the translation layer term map.
"""
from __future__ import annotations

import base64
import json
import os
import re
import unicodedata
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_env():
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())


def fetch_traces(days: int = 30):
    _load_env()
    host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com").rstrip("/")
    pub  = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
    sec  = os.environ.get("LANGFUSE_SECRET_KEY", "")

    if not pub or not sec:
        print("ERROR: LANGFUSE_PUBLIC_KEY / LANGFUSE_SECRET_KEY not set in .env")
        return []

    creds   = base64.b64encode(f"{pub}:{sec}".encode()).decode()
    headers = {"Authorization": f"Basic {creds}", "Content-Type": "application/json"}
    from_ts = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")

    all_traces = []
    page = 1
    while True:
        params = urllib.parse.urlencode({"page": page, "limit": 100, "fromTimestamp": from_ts})
        url = f"{host}/api/public/traces?{params}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read())
        except Exception as e:
            print(f"ERROR fetching page {page}: {e}")
            break

        batch = body.get("data", [])
        all_traces.extend(batch)
        meta  = body.get("meta", {})
        total = meta.get("totalItems", meta.get("total", len(all_traces)))
        print(f"  page {page}: {len(batch)} traces (total seen: {len(all_traces)} / {total})")

        if not batch or len(all_traces) >= total:
            break
        page += 1

    return all_traces


def _extract_query(trace: dict) -> str | None:
    """Pull the user query string from a trace object."""
    # Check common input fields
    for field in ("input", "name"):
        val = trace.get(field)
        if isinstance(val, str) and len(val) > 3:
            return val
        if isinstance(val, dict):
            for sub in ("query", "question", "message", "text", "content"):
                v = val.get(sub)
                if isinstance(v, str) and len(v) > 3:
                    return v
    return None


_ASCII_RE = re.compile(r"^[\x00-\x7F]+$")
_LANG_SCRIPTS = {
    "Arabic":    re.compile(r"[؀-ۿ]"),
    "Hebrew":    re.compile(r"[֐-׿]"),
    "Devanagari": re.compile(r"[ऀ-ॿ]"),
    "Bengali":   re.compile(r"[ঀ-৿]"),
    "CJK":       re.compile(r"[一-鿿]"),
    "Thai":      re.compile(r"[฀-๿]"),
}
# Latin-script non-English detector: common accented chars from PT/ES/FR/DE
_ACCENTED_RE = re.compile(r"[àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ"
                           r"ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞŸ]")


def detect_language_hint(query: str) -> str | None:
    """Return a language hint if query appears non-English, else None."""
    nfc = unicodedata.normalize("NFC", query)
    for lang, pat in _LANG_SCRIPTS.items():
        if pat.search(nfc):
            return lang
    if _ACCENTED_RE.search(nfc):
        # Rough heuristic: Portuguese/Spanish keywords
        lower = nfc.lower()
        if any(w in lower for w in ("ção", "çao", "ões", "ão")):
            return "Portuguese"
        if any(w in lower for w in ("ción", "ción", "ñ", "¿", "¡")):
            return "Spanish"
        return "Latin-accented"
    return None


def main():
    print(f"Fetching last 30 days of Langfuse traces...")
    traces = fetch_traces(days=30)
    print(f"\nTotal traces fetched: {len(traces)}")

    non_english: list[dict] = []
    lang_counter: Counter = Counter()

    for t in traces:
        q = _extract_query(t)
        if not q:
            continue
        lang = detect_language_hint(q)
        if lang:
            non_english.append({"query": q, "lang": lang, "trace_id": t.get("id")})
            lang_counter[lang] += 1

    print(f"\nNon-English queries found: {len(non_english)}")
    print("By language:", dict(lang_counter.most_common()))

    if not non_english:
        print("\nNo non-English traces found in the last 30 days.")
        return

    print("\n--- All non-English queries ---")
    for item in non_english:
        print(f"  [{item['lang']}] {item['query']!r}")

    # Extract individual non-ASCII tokens for term map validation
    all_tokens: Counter = Counter()
    for item in non_english:
        nfc = unicodedata.normalize("NFC", item["query"].lower())
        # For Latin-script: collect words with accented chars
        for word in re.findall(r"[a-zÀ-ɏ]+", nfc):
            if _ACCENTED_RE.search(word):
                all_tokens[word] += 1
        # For non-Latin: collect sequences of script chars
        for pat in _LANG_SCRIPTS.values():
            for m in pat.finditer(nfc):
                span_start = max(0, m.start() - 5)
                span_end   = min(len(nfc), m.end() + 5)
                segment    = nfc[span_start:span_end].strip()
                if len(segment) >= 2:
                    all_tokens[segment] += 1

    print(f"\n--- Top 60 non-ASCII tokens/phrases ---")
    for token, count in all_tokens.most_common(60):
        print(f"  {count:3d}x  {token!r}")

    # Save results
    out_path = ROOT / "local" / "reports" / "non_english_traces_30d.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "fetched_days": 30,
            "total_traces": len(traces),
            "non_english_count": len(non_english),
            "language_counts": dict(lang_counter),
            "top_tokens": dict(all_tokens.most_common(60)),
            "queries": non_english,
        }, f, ensure_ascii=False, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == "__main__":
    main()
