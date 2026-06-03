# Video integration for the KB assistant skill

## 1. Overview

Videos are registered in a `video_manifest.json` that maps KB pages to YouTube videos; transcripts are stored per video so the skill can compute the right start/end timestamp for a given question. Videos are additive — if none match, the answer is shown without a video.

## 2. YouTube link mechanics (constraints)

The skill appends a **clickable link** that opens as a normal (top-level) YouTube page, so it MUST use the `watch` URL form. `/embed/` URLs only play inside an `<iframe>` and fail with **"Error 153 — Video player configuration error"** when opened directly as a link.

| Topic | Behavior |
|-------|----------|
| Start time | `https://www.youtube.com/watch?v=VIDEO_ID&t=S` opens the video at second `S`. This is what the skill emits. |
| End / stop time | **Not possible on a clickable link.** Only an embedded `<iframe>` player honors `end=`. The skill still computes the relevant window and stores `end` for metadata, but a watch link cannot auto-stop. If a true auto-stop is required, the rendering surface must embed an iframe (see below). |
| Captions | Append `cc_load_policy=1&cc_lang_pref=<lang>&hl=<lang>` (`<lang>` = ISO 639-1, e.g. `en`, `hi`). |
| Audio track | **Not** controllable by URL. For multi-audio videos YouTube picks the track from the viewer's account preference. Accepted — audio is left to YouTube. |
| Embedding | Still enable "Allow embedding" so the iframe option remains available; not required for the watch link. |

**Example watch URL the skill emits** (start 42s, English captions):

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42&cc_load_policy=1&cc_lang_pref=en&hl=en
```

**Optional — iframe form** (only if the surface can render inline HTML; honors start **and** end):

```
<iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ?start=42&end=120&cc_load_policy=1&cc_lang_pref=en&hl=en"></iframe>
```

## 3. One-time-per-video YouTube operations (step by step)

1. **Enable embedding:** YouTube Studio → Content → select the video → Edit → ensure **Allow embedding** is on; set visibility to **Public** or **Unlisted**.
2. **Get the video ID** from the watch URL `https://www.youtube.com/watch?v=<ID>` (the `<ID>` segment).
3. **Add multi-language audio tracks:** Studio → Subtitles/Languages → Languages → Add language → under **Dub**, upload each language's audio file. (YouTube does not auto-generate dubs; record or outsource first.)
4. **Add caption tracks per language:** Studio → Subtitles → add or select each language → upload or auto-sync → publish. Note each language's ISO 639-1 code.
5. **Export the transcript** (pick one method):
   - **YouTube Studio:** open the published caption → Edit → download as `.srt` or `.sbv`.
   - **yt-dlp:** `yt-dlp --write-subs --write-auto-subs --sub-langs en,hi --skip-download --sub-format srv1 "https://youtu.be/<ID>"` (srv1/json3 include per-cue start and duration).
   - **YouTube Data API v3:** `captions.list` then `captions.download` (requires OAuth as the channel owner).
6. **Convert the transcript** into the cue JSON format in [section 5](#5-video_transcriptsvideo_idjson-schema) below (a small one-off converter that turns SRT/SBV timecodes into seconds).
7. **Register the video** in `video_manifest.json` ([section 4](#4-video_manifestjson-schema)) mapping the KB page path(s) to the video ID with its caption languages.
8. **Commit** `video_manifest.json` and the transcript file to the KB content repo under the configured paths.

## 4. `video_manifest.json` schema

`video_manifest.json` is a **JSON array** of video entries. Each entry ties one or more KB pages to a YouTube video and its caption metadata.

| Field | Type | Description |
|-------|------|-------------|
| `source` | string | Canonical KB page path this video covers (e.g. `kb/bot-studio/agent-transfer-node.md`). Used as the displayed `source` for the chosen video. |
| `also_sources` | array of strings (optional) | Additional **neighbor** KB pages that should surface the same video (e.g. sibling pages in the same topic cluster). The video is selected if the retriever's top row matches `source` **or** any path in `also_sources`. Keep these **disjoint across entries** — a given page must map to at most one video (the canonical `source` always wins). |
| `video_id` | string | YouTube video ID (from `watch?v=`). |
| `title` | string | Human-readable label for the clickable link shown after the answer. |
| `default_lang` | string | ISO 639-1 default caption language for the entry. |
| `caption_langs` | array of strings | ISO 639-1 codes for caption tracks actually published on the video. |
| `embeddable` | boolean | Whether embedding is enabled on YouTube (should be `true` before use). |
| `broad_fallback` | boolean (optional) | Mark **exactly one** entry `true` to make it the overview video shown for broad discovery/pitch questions (e.g. "what can Gupshup do", "which modules suit retail") when no specific page-mapped video matched. Helps new users / sales who don't know the module map. |
| `intents` | array of strings (optional) | Intent labels that restrict when this video is eligible (e.g. `setup`, `definition`, `overview`). Omit to allow any intent for this `source`. |
| `chapters` | object (optional) | Maps a KB heading string to `{ "start": int, "end": int }` (seconds) to skip transcript matching when timestamps are pre-known. Keys must match heading text on the `source` page. |

**Granularity:** one manifest row per KB `source` page, optionally narrowed by `intents` and/or a `chapters` heading.

**Example** (minimal entry + entry with `intents` and `chapters`):

```json
[
  {
    "source": "kb/bot-studio/agent-transfer-node.md",
    "video_id": "a1b2c3d4e5f",
    "title": "Agent transfer node walkthrough",
    "default_lang": "en",
    "caption_langs": ["en", "hi"],
    "embeddable": true
  },
  {
    "source": "kb/bot-studio/flow-builder-overview.md",
    "video_id": "x9y8z7w6v5u",
    "title": "Flow Builder overview",
    "default_lang": "en",
    "caption_langs": ["en", "hi", "ta"],
    "embeddable": true,
    "intents": ["overview", "definition"],
    "chapters": {
      "Creating a new flow": { "start": 0, "end": 95 },
      "Publishing and versioning": { "start": 312, "end": 402 }
    }
  }
]
```

## 5. `video_transcripts/<video_id>.json` schema

Each file is a **JSON array** of caption cues for one `video_id`. Cues are ordered by `start` and used to score time windows against the user's question.

| Field | Type | Description |
|-------|------|-------------|
| `start` | float | Cue start time in seconds from the beginning of the video. |
| `dur` | float | Cue duration in seconds. |
| `text` | string | Caption text for this cue. |
| `lang` | string | ISO 639-1 language of this cue's track. |

**Example** (three cues):

```json
[
  { "start": 0.0, "dur": 4.2, "text": "Welcome to the agent transfer node.", "lang": "en" },
  { "start": 4.2, "dur": 6.8, "text": "First, open the node settings panel.", "lang": "en" },
  { "start": 11.0, "dur": 5.1, "text": "Map your intent labels to the target queue.", "lang": "en" }
]
```

Store one file per video: `video_transcripts/<video_id>.json` (e.g. `video_transcripts/a1b2c3d4e5f.json`).

## 6. Language handling

- The skill accepts an optional `language` parameter. If absent, it detects the script of the query (e.g. Devanagari → `hi`) and otherwise falls back to `default_lang` or `en`.
- The chosen language is validated against the entry's `caption_langs`. If it is not available, caption URL parameters (`cc_load_policy`, `cc_lang_pref`, `hl`) are omitted, but the timestamped embed link (`start` / `end`) is still appended.

## 7. How the skill picks a video and timestamp (summary)

1. Reuse the answer pipeline's existing **intent** and **ranked evidence**.
2. Scan the **top ranked KB pages** (up to 8) for the first whose path matches a manifest entry's `source` **or** `also_sources`.
3. Look up manifest entries for that page, optionally filtering by matching `intents` and/or the active KB heading (for `chapters`). When several videos map to the same page, the one whose title/keywords best overlap the query wins.
   - **Relevance guard:** the matched page must share at least one distinctive token with the query (via its source path / heading / video title / keywords). This matters for `kb_search`, which has no "I don't know" gate — without it an off-topic query (e.g. "refund policy") could attach the nearest result's video. If the top mapped row fails the guard, the scan continues to the next ranked row, and if none qualify no video is shown.
4. If `chapters` contains the current heading, use its pre-defined `start` and `end` directly.
5. Otherwise, score **windows of transcript cues** against the question and select the best contiguous start/end window (capped to about **90 seconds**).
6. Build the embed URL with whole-second `start` and `end`, plus caption parameters when the language is supported.
7. If no specific page matched **and** the question is a broad discovery/pitch ask, fall back to the entry flagged `broad_fallback` (the overview video) so the first answer still carries a video. Otherwise return the text answer only — no video link.

**Answer gate note:** a video is only appended to a **substantive** answer — never to an "I don't know" response. `kb_answer`'s support gate trusts **strong lexical overlap**: if the best evidence page overlaps the query terms by ≥ 0.7 (with a small positive score), it is accepted even when its absolute score is below the usual floors. This recovers clearly on-topic questions that previously refused (and thus lets their mapped video surface) without lowering the global thresholds. Off-topic queries (low overlap) still refuse and get no video.

## 8. Video consumption telemetry

The skill tracks **delivery** (a video was selected and returned), not YouTube play time. Two sinks:

| Sink | What is recorded |
|------|------------------|
| **Langfuse** (`kb_answer` only, when `LANGFUSE_*` secrets are set) | Flat metadata on each trace: `video_attached`, `video_id`, `video_title`, `video_start`, `video_source`, `video_channel` (`kb_answer` / `kb_search`), `video_fallback`, `video_lang`, `video_captions_on`, and for answers `video_appended_to_answer` (Watch line in answer text). Filter traces where `video_attached = true`. |
| **NDJSON** (`kb_analytics`, when GitHub secrets are set) | Event `video.delivered` appended to `kb/analytics/kb_usage.ndjson` and the daily file. Payload: `channel`, `video_id`, `title`, `start`, `source`, `fallback`, `lang`, `query_preview`, plus `intent` / `module`. |

**Click / watch consumption** is not visible to the skill when the user opens YouTube in a new tab. Have the Gupshup agent (or UI) call `kb_analytics` when the user clicks **Watch**:

```python
kb_analytics(
    event="video.clicked",
    payload={
        "video_id": "<from tool result>",
        "channel": "agent_ui",
        "query_preview": "<user question>",
    },
    context=context,
)
```

Compare `video.delivered` vs `video.clicked` in NDJSON to measure attach-to-click conversion. YouTube Studio remains the source of truth for watch time.
