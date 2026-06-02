# Video integration for the KB assistant skill

## 1. Overview

Videos are registered in a `video_manifest.json` that maps KB pages to YouTube videos; transcripts are stored per video so the skill can compute the right start/end timestamp for a given question. Videos are additive — if none match, the answer is shown without a video.

## 2. YouTube link mechanics (constraints)

| Topic | Behavior |
|-------|----------|
| Start + end time | Only the **embed** URL form honors both: `https://www.youtube.com/embed/VIDEO_ID?start=S&end=E` where `S` and `E` are whole seconds from the start of the video. A normal `watch?v=...&t=` link supports **start only**, not end. |
| Captions | Controllable by URL: append `cc_load_policy=1&cc_lang_pref=<lang>&hl=<lang>` where `<lang>` is an ISO 639-1 code (e.g. `en`, `hi`). |
| Audio track | **Not** controllable by URL (no parameter exists). For multi-audio videos, YouTube picks the track from the viewer's account preference. This is accepted — audio is left to YouTube. |
| Embedding | The video must allow embedding or the embed link will not play. |

**Example embed URL** (start 42s, end 120s, Hindi captions):

```
https://www.youtube.com/embed/dQw4w9WgXcQ?start=42&end=120&cc_load_policy=1&cc_lang_pref=hi&hl=hi
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
| `source` | string | KB page path this video covers (e.g. `kb/bot-studio/agent-transfer-node.md`). |
| `video_id` | string | YouTube video ID (from `watch?v=`). |
| `title` | string | Human-readable label for the clickable link shown after the answer. |
| `default_lang` | string | ISO 639-1 default caption language for the entry. |
| `caption_langs` | array of strings | ISO 639-1 codes for caption tracks actually published on the video. |
| `embeddable` | boolean | Whether embedding is enabled on YouTube (should be `true` before use). |
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
2. Take the **top-ranked KB page** (`source` path).
3. Look up manifest entries for that `source`, optionally filtering by matching `intents` and/or the active KB heading (for `chapters`).
4. If `chapters` contains the current heading, use its pre-defined `start` and `end` directly.
5. Otherwise, score **windows of transcript cues** against the question and select the best contiguous start/end window (capped to about **90 seconds**).
6. Build the embed URL with whole-second `start` and `end`, plus caption parameters when the language is supported.
7. If no manifest entry matches (or embedding is disabled), return the text answer only — no video link.
