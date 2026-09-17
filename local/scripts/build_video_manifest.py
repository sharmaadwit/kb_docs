#!/usr/bin/env python3
"""Draft video_manifest.json by matching video text to KB source pages."""

import argparse
import json
import math
import os
import re
from collections import Counter, defaultdict


STOPWORDS = {
    "about",
    "above",
    "after",
    "again",
    "against",
    "all",
    "also",
    "and",
    "any",
    "are",
    "because",
    "been",
    "before",
    "being",
    "below",
    "between",
    "both",
    "but",
    "can",
    "did",
    "does",
    "doing",
    "don",
    "down",
    "each",
    "few",
    "for",
    "from",
    "had",
    "has",
    "have",
    "her",
    "here",
    "hers",
    "him",
    "his",
    "how",
    "into",
    "its",
    "itself",
    "just",
    "more",
    "most",
    "not",
    "now",
    "off",
    "once",
    "only",
    "other",
    "our",
    "out",
    "over",
    "own",
    "same",
    "she",
    "should",
    "some",
    "such",
    "than",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "these",
    "they",
    "this",
    "those",
    "through",
    "too",
    "under",
    "until",
    "very",
    "was",
    "were",
    "what",
    "when",
    "where",
    "which",
    "while",
    "who",
    "why",
    "will",
    "with",
    "you",
    "your",
}

TOKEN_RE = re.compile(r"[a-z0-9]+")
TITLE_WEIGHT = 3.0
DESCRIPTION_WEIGHT = 2.0
TRANSCRIPT_WEIGHT = 1.0
ALTERNATIVE_COUNT = 4


def tokenize(text):
    if not text:
        return Counter()
    tokens = (
        token
        for token in TOKEN_RE.findall(text.lower())
        if len(token) >= 3 and token not in STOPWORDS
    )
    return Counter(tokens)


def weighted_overlap(query_tokens, page_tokens):
    if not query_tokens or not page_tokens:
        return 0.0

    overlap = 0.0
    for token, query_count in query_tokens.items():
        page_count = page_tokens.get(token, 0)
        if page_count:
            overlap += min(query_count, page_count) * (1.0 + math.log(page_count))

    query_norm = math.sqrt(sum(count * count for count in query_tokens.values()))
    page_norm = math.sqrt(sum(count * count for count in page_tokens.values()))
    if not query_norm or not page_norm:
        return 0.0
    return overlap / (query_norm * page_norm)


def load_chunks(path):
    pages = defaultdict(Counter)
    with open(path, "r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                chunk = json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Could not parse {path}:{line_number}: {exc}") from exc

            source = chunk.get("source")
            if not source:
                continue
            text_parts = [
                str(chunk.get("heading") or ""),
                str(chunk.get("text") or ""),
            ]
            heading_path = chunk.get("heading_path")
            if isinstance(heading_path, list):
                text_parts.extend(str(part) for part in heading_path)
            pages[source].update(tokenize(" ".join(text_parts)))

    if not pages:
        raise SystemExit(f"No source pages found in chunks file: {path}")
    return pages


def load_video_meta(path):
    if not os.path.exists(path):
        print(f"Video metadata not found at {path}; nothing to map yet.")
        return None

    with open(path, "r", encoding="utf-8") as handle:
        try:
            data = json.load(handle)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Could not parse video metadata {path}: {exc}") from exc

    if not isinstance(data, list):
        raise SystemExit(f"Video metadata must be a JSON list: {path}")
    return data


def load_transcript_text(transcripts_dir, video_id):
    transcript_path = os.path.join(transcripts_dir, f"{video_id}.json")
    if not os.path.exists(transcript_path):
        return ""

    with open(transcript_path, "r", encoding="utf-8") as handle:
        try:
            cues = json.load(handle)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Could not parse transcript {transcript_path}: {exc}") from exc

    if not isinstance(cues, list):
        return ""
    return " ".join(str(cue.get("text") or "") for cue in cues if isinstance(cue, dict))


def score_video_against_pages(video, transcript_text, pages):
    title_tokens = tokenize(video.get("title") or "")
    description_tokens = tokenize(video.get("description") or "")
    transcript_tokens = tokenize(transcript_text)

    ranked = []
    for source, page_tokens in pages.items():
        score = (
            TITLE_WEIGHT * weighted_overlap(title_tokens, page_tokens)
            + DESCRIPTION_WEIGHT * weighted_overlap(description_tokens, page_tokens)
            + TRANSCRIPT_WEIGHT * weighted_overlap(transcript_tokens, page_tokens)
        )
        ranked.append((source, score))

    ranked.sort(key=lambda item: (-item[1], item[0]))
    return ranked


def build_entry(video, source, score, alternatives):
    return {
        "source": source,
        "video_id": video.get("video_id", ""),
        "title": video.get("title", ""),
        "default_lang": video.get("default_lang", ""),
        "caption_langs": video.get("caption_langs") or [],
        "embeddable": bool(video.get("embeddable", False)),
        "_map_score": round(score, 6),
        "_map_alternatives": [
            {"source": alt_source, "score": round(alt_score, 6)}
            for alt_source, alt_score in alternatives
        ],
    }


def draft_manifest(video_meta, transcripts_dir, pages, top_n):
    entries = []
    summaries = []
    for video in video_meta:
        if not isinstance(video, dict):
            continue

        video_id = str(video.get("video_id") or "")
        transcript_text = load_transcript_text(transcripts_dir, video_id)
        ranked = score_video_against_pages(video, transcript_text, pages)
        chosen = ranked[:top_n]
        alternatives = ranked[top_n : top_n + ALTERNATIVE_COUNT]

        for source, score in chosen:
            entries.append(build_entry(video, source, score, alternatives))

        summaries.append(
            {
                "video_id": video_id,
                "title": video.get("title", ""),
                "chosen": chosen,
                "alternatives": alternatives,
                "has_transcript": bool(transcript_text),
            }
        )

    return entries, summaries


def print_review_summary(summaries):
    if not summaries:
        print("No videos found in metadata.")
        return

    print("Proposed video to KB mappings")
    print("=" * 30)
    for summary in summaries:
        print(f"\n{summary['video_id']} - {summary['title']}")
        if not summary["has_transcript"]:
            print("  transcript: missing")
        for index, (source, score) in enumerate(summary["chosen"], start=1):
            print(f"  chosen {index}: {source} (score {score:.6f})")
        if summary["alternatives"]:
            print("  alternatives:")
            for source, score in summary["alternatives"]:
                print(f"    - {source} (score {score:.6f})")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Draft kb/video_manifest.json by mapping videos to KB pages."
    )
    parser.add_argument("--meta", default="local/raw/video_meta.json")
    parser.add_argument("--transcripts-dir", default="kb/video_transcripts")
    parser.add_argument("--chunks", default="kb/kb_chunks.jsonl")
    parser.add_argument("--out", default="kb/video_manifest.json")
    parser.add_argument(
        "--top-n",
        type=int,
        default=1,
        help="Number of top source pages to keep as chosen mappings.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print proposed mappings without writing the manifest.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.top_n < 1:
        raise SystemExit("--top-n must be at least 1")

    video_meta = load_video_meta(args.meta)
    if video_meta is None:
        return 0

    pages = load_chunks(args.chunks)
    entries, summaries = draft_manifest(
        video_meta, args.transcripts_dir, pages, args.top_n
    )
    print_review_summary(summaries)

    if args.dry_run:
        return 0

    out_dir = os.path.dirname(args.out)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(entries, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(f"\nWrote {len(entries)} draft manifest entries to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
