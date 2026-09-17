#!/usr/bin/env python3
"""Download YouTube captions via yt-dlp and convert to canonical transcript JSON."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, TypeVar

YOUTUBE_ID_RE = re.compile(r"^[a-zA-Z0-9_-]{11}$")
BACKOFF_SECONDS = (5, 15, 45)
TRANSIENT_MARKERS = ("HTTP Error 429", "Too Many Requests", "Unable to download", "Connection reset")

T = TypeVar("T")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch YouTube captions and convert them to canonical transcript JSON.",
    )
    parser.add_argument("--cookies", required=True, help="Path to Netscape cookies file for yt-dlp")
    url_group = parser.add_mutually_exclusive_group(required=True)
    url_group.add_argument("--urls-file", help="Text file with one video URL or ID per line")
    url_group.add_argument("--urls", nargs="+", help="Video URLs or 11-char IDs")
    parser.add_argument(
        "--langs",
        default="en",
        help='Comma-separated subtitle language codes (default: "en")',
    )
    parser.add_argument(
        "--out-dir",
        default="kb/video_transcripts",
        help="Directory for per-video transcript JSON (default: kb/video_transcripts)",
    )
    parser.add_argument(
        "--meta-out",
        default="local/raw/video_meta.json",
        help="Aggregate metadata JSON for downstream auto-mapper (default: local/raw/video_meta.json)",
    )
    parser.add_argument(
        "--srt",
        action="append",
        default=[],
        metavar="VIDEO_ID=PATH",
        help="Manual SRT/VTT ingest for a video ID (bypasses yt-dlp for that ID)",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=4.0,
        help="Seconds to sleep between videos (default: 4)",
    )
    return parser.parse_args(argv)


def resolve_video_id(url_or_id: str) -> str:
    raw = url_or_id.strip()
    if YOUTUBE_ID_RE.fullmatch(raw):
        return raw

    match = re.search(r"(?:youtu\.be/|youtube\.com/watch\?v=|youtube\.com/embed/)([a-zA-Z0-9_-]{11})", raw)
    if match:
        return match.group(1)

    match = re.search(r"[?&]v=([a-zA-Z0-9_-]{11})", raw)
    if match:
        return match.group(1)

    raise ValueError(f"Could not resolve YouTube video id from: {url_or_id!r}")


def watch_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"


def load_urls(args: argparse.Namespace) -> List[str]:
    if args.urls:
        return list(args.urls)
    path = Path(args.urls_file)
    lines: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append(stripped)
    return lines


def parse_srt_overrides(values: Sequence[str]) -> Dict[str, Path]:
    overrides: Dict[str, Path] = {}
    for item in values:
        if "=" not in item:
            raise ValueError(f"--srt value must be VIDEO_ID=PATH, got: {item!r}")
        video_id, path_str = item.split("=", 1)
        video_id = video_id.strip()
        if not YOUTUBE_ID_RE.fullmatch(video_id):
            raise ValueError(f"Invalid video id in --srt: {video_id!r}")
        overrides[video_id] = Path(path_str.strip())
    return overrides


def is_transient_error(message: str) -> bool:
    upper = message.upper()
    if "429" in message or "TOO MANY REQUESTS" in upper:
        return True
    return any(marker.upper() in upper for marker in TRANSIENT_MARKERS)


def run_yt_dlp(args: List[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, "-m", "yt_dlp", *args]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )
    combined = (result.stdout or "") + (result.stderr or "")
    if result.returncode != 0:
        if check:
            raise RuntimeError(combined.strip() or f"yt-dlp failed with exit code {result.returncode}")
    return result


def with_retries(
    label: str,
    fn: Callable[[], T],
    *,
    max_attempts: int = 3,
) -> T:
    last_error: Optional[Exception] = None
    for attempt in range(1, max_attempts + 1):
        if attempt > 1:
            wait = BACKOFF_SECONDS[min(attempt - 2, len(BACKOFF_SECONDS) - 1)]
            print(f"  retry {attempt}/{max_attempts} for {label} after {wait}s", file=sys.stderr)
            time.sleep(wait)
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001 - batch CLI continues per video
            last_error = exc
            message = str(exc)
            if attempt >= max_attempts or not is_transient_error(message):
                raise
    assert last_error is not None
    raise last_error


def fetch_metadata(cookies: Path, url: str) -> Dict[str, Any]:
    def _fetch() -> Dict[str, Any]:
        result = run_yt_dlp(
            [
                "-J",
                "--skip-download",
                "--cookies",
                str(cookies),
                "--impersonate",
                "chrome",
                url,
            ]
        )
        return json.loads(result.stdout)

    return with_retries("metadata", _fetch)


def available_caption_langs(info: Dict[str, Any]) -> List[str]:
    langs = set(info.get("subtitles") or {})
    langs.update(info.get("automatic_captions") or {})
    return sorted(langs)


def embeddable_from_info(info: Dict[str, Any]) -> bool:
    if "playable_in_embed" in info:
        return bool(info["playable_in_embed"])
    availability = info.get("availability")
    if isinstance(availability, str):
        lowered = availability.lower()
        if "embed" in lowered and "not" in lowered:
            return False
        if lowered in {"private", "needs_auth", "unlisted"}:
            return True
    return True


def download_captions(
    cookies: Path,
    url: str,
    langs: Sequence[str],
    manual_langs: Sequence[str],
    auto_langs: Sequence[str],
    out_template: str,
) -> None:
    if manual_langs:
        run_yt_dlp(
            [
                "--skip-download",
                "--write-subs",
                "--sub-langs",
                ",".join(manual_langs),
                "--sub-format",
                "json3",
                "--cookies",
                str(cookies),
                "--impersonate",
                "chrome",
                "-o",
                out_template,
                url,
            ]
        )
    if auto_langs:
        run_yt_dlp(
            [
                "--skip-download",
                "--write-auto-subs",
                "--sub-langs",
                ",".join(auto_langs),
                "--sub-format",
                "json3",
                "--cookies",
                str(cookies),
                "--impersonate",
                "chrome",
                "-o",
                out_template,
                url,
            ]
        )
    if not manual_langs and not auto_langs:
        raise RuntimeError(f"No caption tracks available for requested langs: {', '.join(langs)}")


def json3_to_cues(data: Dict[str, Any], lang: str) -> List[Dict[str, Any]]:
    cues: List[Dict[str, Any]] = []
    for event in data.get("events") or []:
        segs = event.get("segs")
        if not segs:
            continue
        text = "".join(seg.get("utf8", "") for seg in segs).strip()
        if not text:
            continue
        start_ms = event.get("tStartMs", 0)
        dur_ms = event.get("dDurationMs", 0)
        cues.append(
            {
                "start": start_ms / 1000.0,
                "dur": dur_ms / 1000.0,
                "text": text,
                "lang": lang,
            }
        )
    return cues


def parse_timestamp(value: str) -> float:
    value = value.strip()
    if value.count(":") == 2:
        hours, minutes, rest = value.split(":")
    elif value.count(":") == 1:
        hours = "0"
        minutes, rest = value.split(":")
    else:
        raise ValueError(f"Invalid timestamp: {value!r}")

    if "," in rest:
        seconds, millis = rest.split(",", 1)
    elif "." in rest:
        seconds, millis = rest.split(".", 1)
    else:
        seconds, millis = rest, "0"

    return int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(millis.ljust(3, "0")[:3]) / 1000.0


def parse_srt_or_vtt(path: Path, lang: str) -> List[Dict[str, Any]]:
    content = path.read_text(encoding="utf-8", errors="replace")
    content = re.sub(r"\r\n?", "\n", content)
    if content.startswith("\ufeff"):
        content = content[1:]

    blocks = re.split(r"\n\s*\n", content.strip())
    entries: List[Tuple[float, float, str]] = []

    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if not lines:
            continue
        if lines[0].upper().startswith("WEBVTT"):
            continue
        if lines[0].isdigit():
            lines = lines[1:]
        if not lines:
            continue

        timing_match = re.match(
            r"(\d{1,2}:?\d{2}:\d{2}[.,]\d{3})\s*-->\s*(\d{1,2}:?\d{2}:\d{2}[.,]\d{3})",
            lines[0],
        )
        if not timing_match:
            continue

        start = parse_timestamp(timing_match.group(1))
        end = parse_timestamp(timing_match.group(2))
        text = " ".join(line.strip() for line in lines[1:] if line.strip())
        text = re.sub(r"<[^>]+>", "", text).strip()
        if not text:
            continue
        entries.append((start, end, text))

    entries.sort(key=lambda item: item[0])
    cues: List[Dict[str, Any]] = []
    for idx, (start, end, text) in enumerate(entries):
        if end <= start and idx + 1 < len(entries):
            dur = max(0.0, entries[idx + 1][0] - start)
        else:
            dur = max(0.0, end - start)
        cues.append({"start": start, "dur": dur, "text": text, "lang": lang})
    return cues


def find_json3_file(work_dir: Path, lang: str) -> Optional[Path]:
    candidates = sorted(work_dir.glob(f"*{lang}.json3"))
    if candidates:
        return candidates[0]
    candidates = sorted(work_dir.glob("*.json3"))
    for candidate in candidates:
        if candidate.name.endswith(f".{lang}.json3") or f".{lang}." in candidate.name:
            return candidate
    return None


def process_video(
    *,
    video_ref: str,
    cookies: Path,
    langs: Sequence[str],
    out_dir: Path,
    ytsub_root: Path,
    srt_path: Optional[Path],
    default_lang: str,
) -> Tuple[Optional[Dict[str, Any]], str]:
    video_id = resolve_video_id(video_ref)
    url = watch_url(video_id)

    if srt_path is not None:
        if not srt_path.is_file():
            raise FileNotFoundError(f"SRT/VTT file not found: {srt_path}")
        cues = parse_srt_or_vtt(srt_path, default_lang)
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{video_id}.json"
        out_path.write_text(json.dumps(cues, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        meta = {
            "video_id": video_id,
            "title": video_id,
            "description": "",
            "caption_langs": [default_lang],
            "default_lang": default_lang,
            "embeddable": True,
            "url": url,
        }
        return meta, f"{video_id}: ok (srt) cues={len(cues)} langs={default_lang}"

    info = fetch_metadata(cookies, url)
    video_id = info.get("id") or video_id
    url = watch_url(video_id)
    title = info.get("title") or video_id
    description = info.get("description") or ""
    subtitles = info.get("subtitles") or {}
    automatic = info.get("automatic_captions") or {}
    embeddable = embeddable_from_info(info)

    manual_langs = [lang for lang in langs if lang in subtitles]
    auto_langs = [lang for lang in langs if lang not in subtitles and lang in automatic]
    missing = [lang for lang in langs if lang not in manual_langs and lang not in auto_langs]
    if missing:
        print(f"  warning: no tracks for {', '.join(missing)} on {video_id}", file=sys.stderr)

    work_dir = ytsub_root / video_id
    work_dir.mkdir(parents=True, exist_ok=True)
    for old in work_dir.glob("*.json3"):
        old.unlink()

    out_template = str(work_dir / "cap.%(ext)s")

    def _download() -> None:
        download_captions(
            cookies,
            url,
            langs,
            manual_langs,
            auto_langs,
            out_template,
        )

    with_retries("captions", _download)

    all_cues: List[Dict[str, Any]] = []
    written_langs: List[str] = []
    for lang in langs:
        json3_path = find_json3_file(work_dir, lang)
        if json3_path is None:
            continue
        data = json.loads(json3_path.read_text(encoding="utf-8"))
        cues = json3_to_cues(data, lang)
        if not cues:
            continue
        all_cues.extend(cues)
        written_langs.append(lang)

    if not all_cues:
        raise RuntimeError(f"No caption cues produced for {video_id}")

    all_cues.sort(key=lambda cue: (cue["start"], cue["lang"]))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{video_id}.json"
    out_path.write_text(json.dumps(all_cues, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    default_written = next((lang for lang in langs if lang in written_langs), written_langs[0])
    meta = {
        "video_id": video_id,
        "title": title,
        "description": description,
        "caption_langs": written_langs,
        "default_lang": default_written,
        "embeddable": embeddable,
        "url": url,
    }
    return meta, f"{video_id}: ok cues={len(all_cues)} langs={','.join(written_langs)}"


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    cookies = Path(args.cookies)
    if not cookies.is_file():
        print(f"Cookies file not found: {cookies}", file=sys.stderr)
        return 2

    langs = [part.strip() for part in args.langs.split(",") if part.strip()]
    if not langs:
        print("No languages requested via --langs", file=sys.stderr)
        return 2

    try:
        srt_overrides = parse_srt_overrides(args.srt)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    try:
        url_refs = load_urls(args)
    except OSError as exc:
        print(f"Failed to read URLs: {exc}", file=sys.stderr)
        return 2

    if not url_refs:
        print("No URLs to process", file=sys.stderr)
        return 2

    out_dir = Path(args.out_dir)
    meta_out = Path(args.meta_out)
    ytsub_root = Path("local/raw/ytsub")
    ytsub_root.mkdir(parents=True, exist_ok=True)

    meta_entries: List[Dict[str, Any]] = []
    summaries: List[str] = []

    for index, url_ref in enumerate(url_refs):
        try:
            video_id = resolve_video_id(url_ref)
        except ValueError as exc:
            summaries.append(f"{url_ref}: fail ({exc})")
            continue

        srt_path = srt_overrides.get(video_id)
        default_lang = langs[0]
        try:
            meta, summary = process_video(
                video_ref=url_ref,
                cookies=cookies,
                langs=langs,
                out_dir=out_dir,
                ytsub_root=ytsub_root,
                srt_path=srt_path,
                default_lang=default_lang,
            )
            if meta is not None:
                meta_entries.append(meta)
            summaries.append(summary)
        except Exception as exc:  # noqa: BLE001 - continue batch on per-video failure
            summaries.append(f"{video_id}: fail ({exc})")
            print(f"  error for {video_id}: {exc}", file=sys.stderr)

        if index + 1 < len(url_refs) and args.sleep > 0:
            time.sleep(args.sleep)

    meta_out.parent.mkdir(parents=True, exist_ok=True)
    meta_out.write_text(json.dumps(meta_entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("Summary:")
    for line in summaries:
        print(f"  {line}")
    print(f"Wrote {len(meta_entries)} meta entries to {meta_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
