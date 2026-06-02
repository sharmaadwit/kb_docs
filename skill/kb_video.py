import logging
import re
from urllib.parse import urlencode

import kb_storage


logger = logging.getLogger(__name__)

_STOP_WORDS = {
    "how",
    "to",
    "use",
    "from",
    "in",
    "a",
    "the",
    "my",
    "is",
    "it",
    "do",
    "can",
    "that",
    "this",
    "and",
    "or",
    "for",
    "with",
    "on",
    "of",
    "what",
    "where",
    "when",
    "which",
    "are",
    "was",
    "will",
    "should",
    "does",
    "have",
    "not",
    "but",
    "they",
    "their",
    "its",
    "all",
    "an",
    "be",
    "so",
    "if",
    "am",
    "trying",
    "want",
    "ensure",
    "also",
    "need",
    "using",
    "about",
    "into",
    "would",
    "could",
    "dont",
    "get",
    "set",
    "go",
    "see",
    "way",
    "like",
    "just",
    "any",
    "has",
    "been",
    "being",
    "were",
    "did",
    "had",
    "than",
    "then",
    "there",
    "here",
    "these",
    "those",
    "each",
    "every",
    "some",
    "such",
    "own",
    "same",
    "other",
    "only",
}


def _tokenize(text):
    text = str(text or "").lower()
    tokens = []
    for token in re.findall(r"[a-z0-9]+", text):
        if len(token) < 3 or token in _STOP_WORDS:
            continue
        tokens.append(token)
    return tokens


_BROAD_QUERY_PATTERNS = (
    "what can gupshup",
    "what does gupshup",
    "what is gupshup",
    "what all can",
    "use case",
    "use-case",
    "suitable for",
    "suited for",
    "good for",
    "best for",
    "right for",
    "which module",
    "what module",
    "what modules",
    "which industr",
    "getting started",
    "get started",
    "new to gupshup",
    "introduction to",
    "overview of gupshup",
    "tell me about gupshup",
    "pitch",
)


def _is_broad_query(query: str) -> bool:
    # Discovery / pitch / "what can it do" style asks from new users or sales,
    # where no single KB page is the answer. Used only as a fallback to surface
    # a high-level overview video when no specific page-mapped video matched.
    q = str(query or "").lower()
    return any(p in q for p in _BROAD_QUERY_PATTERNS)


def _safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def _get_secret(context, name):
    if context is None:
        return None
    try:
        value = context.get_secret(name)
    except Exception:
        return None
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def build_video_url(video_id: str, start, end=None, lang=None) -> str:
    # The skill emits a clickable link that opens as a top-level YouTube page.
    # We must use a normal /watch URL: /embed/ URLs only play inside an <iframe>
    # and fail with "Error 153" when opened directly. Watch URLs honour a start
    # offset (t=) but have no native stop/end param (only an iframe can auto-end),
    # so `end` is accepted for metadata but intentionally not placed in the URL.
    params = [("v", video_id), ("t", _safe_int(start, 0))]
    if lang:
        params.append(("cc_load_policy", 1))
        params.append(("cc_lang_pref", str(lang)))
        params.append(("hl", str(lang)))
    return f"https://www.youtube.com/watch?{urlencode(params)}"


def derive_window(cues, query_text: str, max_seconds: int = 90):
    max_seconds = max(1, _safe_int(max_seconds, 90))
    normalized = []
    for cue in cues or []:
        if not isinstance(cue, dict):
            continue
        start = _safe_float(cue.get("start"), 0.0)
        dur = _safe_float(cue.get("dur"), 0.0)
        if dur < 0:
            dur = 0.0
        end = start + dur
        normalized.append(
            {
                "start": start,
                "dur": dur,
                "end": end,
                "tokens": set(_tokenize(cue.get("text", ""))),
            }
        )

    if not normalized:
        return (0, max_seconds)

    query_tokens = set(_tokenize(query_text))
    total_end = int(normalized[-1]["end"])

    best_score = -1
    best_start = 0
    best_end = min(max_seconds, total_end) if total_end > 0 else max_seconds

    for i in range(len(normalized)):
        start = normalized[i]["start"]
        window_tokens = set()
        last_end = start

        for j in range(i, len(normalized)):
            candidate_end = normalized[j]["end"]
            if j > i and candidate_end - start > max_seconds:
                break
            window_tokens.update(normalized[j]["tokens"])
            last_end = candidate_end

            score = len(query_tokens.intersection(window_tokens))
            if score > best_score:
                best_score = score
                best_start = int(start)
                best_end = int(last_end)
            elif score == best_score and int(start) < best_start:
                best_start = int(start)
                best_end = int(last_end)

    if best_score <= 0:
        fallback_end = total_end if total_end > 0 else max_seconds
        return (0, min(max_seconds, fallback_end))

    if best_end < best_start:
        best_end = best_start
    if best_end - best_start > max_seconds:
        best_end = best_start + max_seconds
    return (best_start, best_end)


def pick_language(requested_lang, query_text: str, entry: dict):
    del query_text
    entry = entry or {}
    caption_langs = entry.get("caption_langs") or []
    if requested_lang and requested_lang in caption_langs:
        return requested_lang, True

    default_lang = entry.get("default_lang")
    if default_lang and default_lang in caption_langs:
        return default_lang, True
    return None, False


def select_video(query: str, intent: str, module: str, ranked_rows, language=None, context=None):
    del module
    try:
        manifest_path = _get_secret(context, "KB_VIDEO_MANIFEST_PATH") or "kb/video_manifest.json"
        transcript_dir = _get_secret(context, "KB_VIDEO_TRANSCRIPT_DIR") or "kb/video_transcripts"

        manifest = kb_storage.read_json(manifest_path, context)
        if not ranked_rows or not manifest:
            return None
        if not isinstance(ranked_rows, list):
            return None

        query_tokens = set(_tokenize(query))

        def score_candidate(entry, row_heading):
            intents = entry.get("intents")
            chapters = entry.get("chapters") if isinstance(entry.get("chapters"), dict) else {}
            intent_match = int(isinstance(intents, list) and intent in intents)
            chapter_match = int(bool(row_heading) and row_heading in chapters)
            # Tie-break when several videos map to the same KB page: prefer the
            # one whose title/keywords overlap the query the most.
            kw_text = " ".join(
                [str(entry.get("title") or "")]
                + [str(k) for k in (entry.get("keywords") or [])]
            )
            kw_overlap = len(query_tokens.intersection(set(_tokenize(kw_text))))
            return (intent_match, chapter_match, kw_overlap)

        def row_is_relevant(row, row_heading, chosen):
            # Guard against attaching a video to a barely-related top result.
            # kb_search has no "I don't know" gate, so without this an off-topic
            # query (e.g. "refund policy") could still surface the nearest page's
            # video. Require at least one distinctive token shared between the
            # query and the matched page / video entry.
            ref_tokens = set(_tokenize(row.get("source", "")))
            ref_tokens |= set(_tokenize(row_heading))
            ref_tokens |= set(_tokenize(chosen.get("title") or ""))
            for kw in (chosen.get("keywords") or []):
                ref_tokens |= set(_tokenize(kw))
            return bool(query_tokens & ref_tokens)

        # Scan the top ranked rows for the first one that maps to a manifest
        # entry, so a relevant video is not missed just because the single best
        # evidence row happens to be an unmapped page.
        primary = None
        entry = None
        heading = ""
        for row in ranked_rows[:8]:
            if not isinstance(row, dict):
                continue
            source = row.get("source")
            if not source:
                continue
            candidates = [
                e for e in manifest
                if isinstance(e, dict)
                and e.get("embeddable") is not False
                and (
                    e.get("source") == source
                    or (
                        isinstance(e.get("also_sources"), list)
                        and source in e.get("also_sources")
                    )
                )
            ]
            if not candidates:
                continue
            row_heading = row.get("heading") or ""
            best = max(candidates, key=lambda e: score_candidate(e, row_heading))
            if not row_is_relevant(row, row_heading, best):
                continue
            primary = row
            heading = row_heading
            entry = best
            break

        # Broad / discovery questions (e.g. "what can Gupshup do", "which modules
        # suit retail", a sales pitch) rarely map to one page, so the scan above
        # finds nothing. For new users and sales, still attach a high-level
        # overview video flagged `broad_fallback` so the first answer carries one.
        is_fallback = False
        if entry is None and _is_broad_query(query):
            fallback = next(
                (
                    e for e in manifest
                    if isinstance(e, dict)
                    and e.get("broad_fallback") is True
                    and e.get("embeddable") is not False
                    and e.get("video_id")
                ),
                None,
            )
            if fallback is not None:
                entry = fallback
                primary = {"source": fallback.get("source"), "text": ""}
                heading = ""
                is_fallback = True

        if entry is None or primary is None:
            return None

        lang, cc_on = pick_language(language, query, entry)

        start = 0
        end = None
        chapters = entry.get("chapters")
        chapter = None
        if isinstance(chapters, dict) and heading:
            chapter = chapters.get(heading)
        if isinstance(chapter, dict) and "start" in chapter and "end" in chapter:
            start = _safe_int(chapter.get("start"), 0)
            end = _safe_int(chapter.get("end"), start)
        else:
            transcript = None
            video_id = entry.get("video_id")
            if video_id:
                transcript_path = f"{transcript_dir}/{video_id}.json"
                try:
                    transcript = kb_storage.read_json(transcript_path, context)
                except Exception:
                    transcript = None
            if isinstance(transcript, list) and transcript:
                combined_query = f"{query or ''} {primary.get('text', '')}".strip()
                start, end = derive_window(transcript, combined_query)
            else:
                start, end = 0, None

        video_id = entry.get("video_id")
        if not video_id:
            return None

        url = build_video_url(video_id, start, end, lang if cc_on else None)
        return {
            "video_id": video_id,
            "title": entry.get("title", ""),
            "start": start,
            "end": end,
            "lang": lang,
            "captions_on": cc_on,
            "url": url,
            "source": entry.get("source"),
            "fallback": is_fallback,
        }
    except Exception:
        logger.exception("Failed selecting video")
        return None
