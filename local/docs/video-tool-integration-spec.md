# Video Tool Integration Specification
**For:** Internal Video Generation Tool Engineers Meeting
**Date:** 2026-06-23
**Purpose:** Replace YouTube with an on-demand internal video generation tool, without regressing today's selection behavior.
**Audience:** Backend engineers implementing the tool's API.

---

## Part 1: How Video Selection Works Today

When the KB answers a question, it tries to attach the *single most relevant* video (or several, for broad questions) and deep-link the user to the **exact 90-second moment** that answers them. All of this logic lives in `skill/kb_video.py` and is **fully synchronous and in-process** — there is no network call today. Videos are static YouTube clips described by a hand-curated manifest.

### The pipeline (one specific question → one video link)

1. **Find candidate pages.** KB search has already ranked the top KB pages (`ranked_rows`). Each row has a `source` path like `kb/bot-studio/message-template.md`.

2. **Map pages → videos.** `kb/video_manifest.json` maps each KB page to a video. One video can cover several pages via `also_sources`. A page may have several candidate videos.

3. **Score candidates** (higher = better):
   - **Intent match:** query intent is in the video's `intents` list → favored.
   - **Keyword/title overlap:** count of tokens shared between the query and the video's `title` + `keywords`.
   - **Relevance guard:** if *no* query token overlaps the page/title/keywords, the candidate is dropped (unless query↔page token overlap ≥ 40%, which rescues it). This is what stops "how to send a message" from surfacing an unrelated video.
   - **Embeddable filter:** candidates with `"embeddable": false` are excluded entirely.
   - The highest scorer wins. For overview/new-user queries, a `broad_fallback` video is used instead.

4. **Pick the 90-second window (the key trick).** Once a video is chosen, we deep-link into the most relevant 90 seconds rather than the start:
   - Load the transcript (`kb/video_transcripts/{video_id}.json`), a list of caption cues `{start, dur, text}`.
   - Tokenize the query (stop-words removed, tokens ≥ 3 chars).
   - **Slide a ≤90s window** across the cues; score each window by `len(query_tokens ∩ window_tokens)`. Pick the highest-scoring window; ties go to the earliest start.
   - **Fallbacks:** no token match → `(start=0, end=min(90, video_end))`. Missing/invalid transcript → `(start=0, end=None)` (link to start, no window). If `chapters` exist in the manifest, exact chapter timings are preferred over transcript scanning.

5. **Pick the caption language** (`pick_language`):
   - If the user's requested language ∈ `caption_langs` → use it, captions on.
   - Else if `default_lang` ∈ `caption_langs` → use it, captions on.
   - Else → no captions (`lang=None, captions_on=False`).
   - Note: caption choice is driven by what the **video** offers, not the query language.

### Embeddable, precisely
"Embeddable" today does **not** mean iframe-embeddable. The URL we emit is a **top-level YouTube watch page** that the user opens directly:

```
https://www.youtube.com/watch?v=p8XsoaMUyd0&t=120
# with captions:
https://www.youtube.com/watch?v=p8XsoaMUyd0&t=120&cc_load_policy=1&cc_lang_pref=pt&hl=pt
```

We deliberately use `/watch` (not `/embed/`) because `/embed/` URLs return **Error 153** when opened as a top-level link. `embeddable: false` simply means "do not surface this video at all yet." Also note: YouTube watch URLs have **no native stop parameter**, so `end` is returned as metadata only and is **never** put in the URL — the 90s window is informational for the caller, not enforced by the player.

### Data model (current)

Manifest entry (`kb/video_manifest.json`, a JSON array). Required: `source`, `video_id`, `title`, `default_lang`, `caption_langs`. Optional: `also_sources`, `keywords`, `intents`, `chapters`, `embeddable`, `pitch`, `pitch_order`, `broad_fallback`, `note`.

```json
{
  "source": "kb/bot-studio/message-template.md",
  "also_sources": ["kb/bot-studio/carousel-and-lto-template.md"],
  "video_id": "p8XsoaMUyd0",
  "title": "Creating & Publishing Message Templates",
  "keywords": ["template", "message", "publish"],
  "intents": ["template_creation", "template_publishing"],
  "chapters": {"Creating a Template": {"start": 15, "end": 120}, "Publishing": {"start": 120, "end": 180}},
  "default_lang": "en",
  "caption_langs": ["en", "pt", "es"],
  "embeddable": true,
  "pitch": true,
  "pitch_order": 2,
  "broad_fallback": true
}
```

Transcript (`kb/video_transcripts/{video_id}.json`, a JSON array of cues):

```json
[
  {"start": 0.0, "dur": 5.2, "text": "In this video we'll explore message templates", "lang": "en"},
  {"start": 5.2, "dur": 4.1, "text": "A template lets you reuse messages", "lang": "en"}
]
```

### Public functions (what kb_answer calls)

| Function | Returns | Notes |
|---|---|---|
| `select_video(query, intent, module, ranked_rows, language=None, context=None)` | one video dict or `None` | best video for a specific question |
| `select_videos(..., max_videos=6, require_query_overlap=True)` | list (≤6) | one video per distinct module/page for broad answers |
| `catalog_videos(query, language=None, context=None, max_videos=10)` | list (≤10) | curated platform tour, `pitch=true`, sorted by `pitch_order` |

All three are wrapped in try/except: **any failure returns `None`/`[]`** and the answer is rendered without a video. Returned video dict:

```python
{"video_id": "p8XsoaMUyd0", "title": "...", "url": "https://...&t=120",
 "start": 120, "end": 180, "lang": "pt", "captions_on": True,
 "source": "kb/bot-studio/message-template.md", "fallback": False}
```

---

## Part 2: What Needs to Change

### Integration points (`skill/kb_answer.py`, lines ~5838–5872)

| Line | Call | When |
|---|---|---|
| ~5838 | `catalog_videos(...)` | overview query + platform pitch ("what can Gupshup do?") |
| ~5844 | `select_videos(..., require_query_overlap=False)` | broad answer spanning modules |
| ~5849 | `select_video(...)` | specific question |
| ~5864/~5872 | `video_telemetry_metadata(...)` / `record_video_delivery(...)` | log delivery to Langfuse + NDJSON |

The selection/window/language logic in `kb_video.py` **stays in the skill**. The tool's job is to **replace the data source** (manifest + transcripts + URLs) that this logic reads from. Concretely, three things move behind the tool's API:

1. **Metadata lookup** — replaces reading `kb/video_manifest.json`.
2. **Transcript lookup** — replaces reading `kb/video_transcripts/{id}.json`.
3. **URL construction** — replaces `build_video_url()`.

The video metadata JSON the tool returns must carry the same fields as the manifest entry above (`source`, `also_sources`, `video_id`, `title`, `keywords`, `intents`, `chapters`, `duration`, `default_lang`, `caption_langs`, `embeddable`, `pitch`, `pitch_order`, `broad_fallback`) plus an inline or separately-fetchable `transcript`.

---

## Part 3: Improvements

Split by whether they are **required to replicate current behavior** vs. **bonus**.

### Must-have for migration (these unblock parity — without them we regress)

1. **Source → metadata lookup** (`GET /for-source`). Replaces the manifest. Must return all current fields. Without this, no video can be selected.
2. **Transcript retrieval** (`GET /{id}/transcript`). The 90-second window selection depends entirely on cue-level `{start, dur, text}` transcripts. No transcripts → every video links to `t=0`.
3. **Stable deep-link URLs** with `t` (seconds) and `lang`, openable directly (top-level page, no iframe required). Replaces `build_video_url()`.
4. **Intent + keyword fields populated** on metadata. Scoring and tie-breaking rely on `intents`/`keywords`; empty fields collapse scoring quality to title-overlap only.
5. **`embeddable` honored.** Caller filters on `embeddable is not False`.
6. **Graceful, fast failure.** Lookups must fail fast and let the caller degrade to "no video" (see Part 4 latencies). The selection path is synchronous and on the answer's critical path.

### Future enhancements (bonus — improve quality, not required for cutover)

7. **Intent-targeted generation** — generate a video specifically for a detected intent rather than reusing a generic clip.
8. **Module/KB-structure-aware generation** — `POST /generate` with KB markdown + section outline so chapters mirror the KB page structure and transcripts are auto-authored from source.
9. **On-demand generation with caching** — cache by source hash (`kb/video_cache/{source_hash}.json`); regenerate only when the KB page's mtime is newer than the cache.
10. **Semantic window selection** — replace token-overlap window scoring with embedding cosine-similarity over chapter/cue text.

---

## Part 4: API Contract

### Conventions (apply to all endpoints)

- **Latency budgets.** Selection-path reads (`/for-source`, `/transcript`, `/url`) are on the synchronous answer critical path: **p99 < 100 ms; hard client timeout 250 ms.** On timeout the caller drops the video and answers without it — never block the answer.
- **Async generation.** `POST /generate` is **asynchronous**. It returns `202 Accepted` with `{ "video_id", "status": "generating" }` immediately (target < 500 ms). The caller polls `GET /for-source` (or `GET /{id}`) until `status: "ready"`. Generation is **never** awaited inline during a user answer. Generation SLA target: < 5 min/video.
- **Retries.** Idempotent GETs: retry up to **2 times** on `5xx`/timeout with exponential backoff (100 ms, 300 ms), capped by the 250 ms client timeout (so effectively at most one fast retry). `POST /generate` is **not** auto-retried (use an idempotency key, below).
- **Rate limits.** Read endpoints: ≥ 50 req/s sustained per service. `POST /generate`: ≥ 5 concurrent jobs / "5–10 videos per KB update" burst. On limit, return `429` with `Retry-After` (seconds); caller backs off and degrades to no-video for that request.
- **Idempotency.** `POST /generate` accepts `Idempotency-Key` header; same key + same `source` returns the existing job/video instead of creating a duplicate.
- **Errors.** JSON body `{ "error": { "code": "...", "message": "..." } }`. Codes: `not_found` (404), `rate_limited` (429), `generation_failed` (5xx), `invalid_request` (400). **A missing video is `404`, not an error to surface** — caller treats it as "no video."

### Endpoint 1 — Metadata for a KB source (replaces manifest)
```
GET /api/videos/for-source?source=kb/bot-studio/message-template.md

200 → [ { video_id, title, keywords, intents, chapters, duration,
          default_lang, caption_langs, embeddable, source, also_sources,
          pitch, pitch_order, broad_fallback, status, transcript? } ]
404 → no video mapped to this source   (caller answers with no video)
```
`transcript` may be inlined or omitted (then fetched via Endpoint 4). `status` ∈ `ready | generating | failed`.

### Endpoint 2 — Search by intent + module
```
GET /api/videos/search?intent=template_creation&module=Bot+Studio&query=create+message&max=6
200 → [ { …same shape… }, … ]   # ranked by relevance, ≤ max
200 → []   # no matches (valid, not an error)
```

### Endpoint 3 — Generate (async)
```
POST /api/videos/generate
Idempotency-Key: <hash(source)>
{ "source": "...", "module": "...", "intent": "...",
  "kb_content": "# markdown…", "structure": {"sections": [...]},
  "caption_languages": ["en","pt","es"], "target_duration_seconds": 120 }

202 → { "video_id": "internal-gen-001", "status": "generating" }
200 → { "video_id": "internal-gen-001", "status": "ready", … }   # idempotency hit
429 → rate limited (Retry-After)
```

### Endpoint 4 — Transcript (drives window selection)
```
GET /api/videos/{video_id}/transcript?lang=pt
200 → [ {start, dur, text, lang}, … ]
404 → no transcript            (caller links to t=0, no window)
```
**Transcript edge cases the caller handles — define your behavior for each:**
- **No captions at all** → return `404`. Caller links to `t=0`.
- **Partial language coverage** (e.g. `pt` requested but only `en` exists) → return the `en` transcript (window matching still works on any language's cues) OR `404`; specify which. Caption *display* language is decided separately via `caption_langs`.
- **Missing `dur`** on a cue → caller coerces to 0; prefer to always emit `dur`.
- **Out-of-order / overlapping cues** → caller tolerates but window quality drops; emit sorted, non-overlapping cues.

### Endpoint 5 — Deep-link URL (replaces build_video_url)
```
GET /api/videos/{video_id}/url?t=120&lang=pt
200 → { "url": "https://video-tool.internal/watch/internal-gen-001?t=120&lang=pt" }
```
The URL **must be openable as a top-level page** (the user clicks it in Slack/email/chat). Do **not** require an iframe. `t` is start-seconds; there is no stop parameter expected (the caller's `end` stays metadata-only). Include captions-on behavior when `lang` is present.

---

## Part 5: Worked Examples

### A. Happy path — specific query
**Query:** "how to create message templates in portuguese", intent `template_creation`, `language="pt"`.
1. KB search yields `ranked_rows` incl. `kb/bot-studio/message-template.md`.
2. Caller → `GET /for-source?source=kb/bot-studio/message-template.md` → metadata for `p8XsoaMUyd0`, `caption_langs:["en","pt","es"]`, `intents` includes `template_creation` (scores well).
3. Caller → `GET /{id}/transcript?lang=pt` → cues. Window scan finds best 90s at `start=120,end=180`.
4. Language: `pt ∈ caption_langs` → `lang="pt", captions_on=true`.
5. Caller → `GET /{id}/url?t=120&lang=pt`.
**Response to user:** deep link at `t=120`, Portuguese captions on.

### B. Failure mode — transcript service times out
On step 3, `GET /transcript` exceeds the 250 ms budget. One fast retry fails too.
**Degrade:** caller skips window selection, links to `t=0` (or chapter timing if `chapters` present in metadata), still serves the video. The answer is **never** blocked.

### C. Failure mode — no video for the source
`GET /for-source` → `404`. Caller treats as "no video," renders the text answer alone. Not logged as an error.

### D. Async generation (post-launch)
KB page updated → background job `POST /generate` (idempotency key = source hash) → `202 generating`. The live answer path meanwhile serves the previous cached/manifest video (or none). When status flips to `ready`, subsequent `/for-source` calls return it. No user request ever waits on generation.

---

## Part 6: Migration Checklist

**Phase 1 — API parity (Wk 1–2):** Endpoints 1, 4, 5 live; URLs open top-level in Slack/email; transcript format `[{start,dur,text}]`; languages en/pt/es/ar; `404`/timeout degrade paths verified.
**Phase 2 — Metadata mapping (Wk 2–3):** Seed metadata for the ~30 existing videos; map `intents`, `source`/`also_sources`; set `pitch`/`pitch_order`; create the `broad_fallback` video.
**Phase 3 — Code swap in `skill/kb_video.py` (Wk 3–4):** Repoint `build_video_url`, manifest reads, and transcript reads to the tool API behind a flag. **Keep window/scoring/language logic unchanged.**
**Phase 4 — Validation (Wk 4):** 20+ real queries through `select_video`/`select_videos`/`catalog_videos`; confirm window matching and caption selection unchanged vs. YouTube baseline.
**Phase 5 — On-demand generation (post-launch):** `POST /generate` wiring, cache invalidation on KB mtime, latency/quality metrics.

---

## Part 7: Backward Compatibility

- **Parallel run:** YouTube manifest and internal tool both available during cutover.
- **Feature flag:** `USE_INTERNAL_VIDEO_TOOL=true/false` in context secrets.
- **Fallback chain:** internal tool → YouTube manifest → no video (never an error to the user).
- **Analytics:** keep emitting `video_attached`, `video_source`, `video_id` to Langfuse + NDJSON.

---

## Open Questions for the Meeting

1. **Generation:** confirmed async + polling? Per-video SLA? Can you sustain 5–10 generations per KB update?
2. **Transcripts:** auto-STT or authored? Quality bar? Behavior on partial-language coverage (Endpoint 4)?
3. **Intent input:** can `/generate` accept intent + KB structure and shape chapters accordingly?
4. **Languages:** en/pt/es/ar guaranteed? fr next?
5. **Embeddability:** all URLs openable top-level (no iframe)? Any restricted videos?
6. **Storage/retention/versioning:** where stored, how long, how versioned across KB updates?

---

**Reference files**
- `skill/kb_video.py` — selection, 90s window, language, URL logic
- `skill/kb_answer.py` ~5838–5872 — call sites
- `kb/video_manifest.json` — current data model
- `kb/video_transcripts/` — sample transcripts
