# DemoForge Telemetry Integration — State & Requirements

**Last updated:** 2026-07-02
**Purpose:** Portable state doc so any session / smaller model can resume this work.

---

## 1. What this work is

Integrate DemoForge interactive demos into the KB answer flow (replacing/augmenting
static YouTube links) and make the **telemetry clean**:
- All video metrics ride in the **main `kb_answer` trace** (no separate events).
- DemoForge videos emit the **same original telemetry shape** as YouTube videos,
  plus namespaced `demoforge_*` extras.
- Locally-issued test queries are tagged `trace_env=local` so they never pollute
  the CxO/prod dashboard.

## 2. Hard requirements (do NOT regress)

1. **No extra traces.** Never emit a separate `demoforge_share_link` (or
   `video_selection`) Langfuse event. Everything consolidates into `kb_answer`.
2. **Preserve the original telemetry shape.** `video_source` is the **KB source
   path** (e.g. `kb/agent-assist/settings.md`), NOT a type. Never overwrite it
   with "youtube"/"demoforge". The type goes in the separate `video_platform`
   field. For DemoForge (no KB chunk) `video_source` is `None`.
3. **`trace_env=local` for local testing.** Every query issued from local scripts
   must pass `telemetry_env: "local"` so dashboards separate local vs SuperAgent prod.
4. **Never push to git without explicit user permission.**
5. **Skill code transmits via raw HTTP** (unchanged transport). The Langfuse
   **v4 SDK** is used **only** in `local/scripts/` for analysis/cleanup.

## 3. Canonical telemetry shape (video attached)

Emitted by `skill/kb_video.py::video_telemetry_metadata()` — single source of truth
for both platforms:

| Field | YouTube | DemoForge |
|-------|---------|-----------|
| `video_attached` | True | True |
| `video_channel` | `kb_answer` | `kb_answer` |
| `video_id` | YouTube id | **demo_id** (unified asset identity) |
| `video_title` | clip title | demo `name` |
| `video_source` | KB path | `None` (no KB chunk) |
| `video_fallback` | bool | False |
| `video_lang` / `video_captions_on` / `video_start` / `video_end` | as-is | None/False |
| `video_appended_to_answer` | bool | bool |
| `video_platform` | `youtube` | `demoforge` |
| `demoforge_demo_id` | — | demo_id |
| `demoforge_share_token` | — | share token |
| `demoforge_api_latency_ms` | — | int ms |
| `demoforge_fallback_reason` | set on fallback (appended in kb_answer) | set on fallback |

When no video: `{video_attached: False, video_channel: "kb_answer"}`.
Multi-video (overview): adds `video_count`, `video_ids`, `video_sources`.

## 4. Key code locations

- `skill/kb_video.py::video_telemetry_metadata()` (~L641) — builds the full shape;
  handles DemoForge natively (no short-circuit). **Single source of truth.**
- `skill/kb_video.py::select_demoforge_demo()` (~L429) — intent+module → demo dict
  (`type, demo_id, name, industry, persona, share_token`).
- `skill/kb_answer.py` (~L6437-6567) — video selection (DemoForge-first, YouTube
  fallback), calls `video_telemetry_metadata()`, appends `demoforge_fallback_reason`,
  passes `video_meta` into `_send_langfuse()`. **No per-call field patching** — that
  was removed; the shape lives in `video_telemetry_metadata()`.
- `skill/kb_answer.py::_mint_demoforge_share_link()` (~L3605) — POSTs share link;
  emits NO telemetry event (consolidated). Returns
  `{share_token, share_status, share_url, type, api_latency_ms}` or None.
- `skill/kb_answer.py::_telemetry_identifiers()` (~L5965) — `environment`/`trace_env`
  resolved from param `telemetry_env|environment|env|stage` OR secret
  `KB_ENV|APP_ENV|...`. **Local scripts pass `telemetry_env:"local"`.**
- `skill/kb_answer.py::_send_langfuse()` (~L6009) — builds trace; `trace_env` at
  metadata; merges `video_meta`.

## 5. Local analysis tooling (v4 SDK)

- Langfuse SDK is **v4.12.0** (already installed; no pip upgrade was needed).
- `local/scripts/langfuse_client.py` — v4 helper: `get_client()`, `list_traces()`,
  `get_trace()`, `delete_traces()`. Uses `.api.trace.list/get/delete_multiple`
  with 60s timeout (cloud reads are slow from this network). Loads creds from `.env`.
- `local/scripts/test_consolidated_telemetry.py` — runs 2 queries with
  `telemetry_env=local`, then verifies via SDK: (1) no `demoforge_share_link`
  traces, (2) full video shape present. **Adds `skill/` to sys.path** so the flat
  `import kb_video` inside the skill resolves.

### Verified run (2026-07-02, trace `kb-kb_answer-3a498dc4d208431d`)
```
trace_env: local
video_attached: True   video_channel: kb_answer
video_id: 6a4402a6f14e94517beb8474   video_title: Campaign Manager Demo
video_source: None   video_fallback: False   video_appended_to_answer: True
video_platform: demoforge
demoforge_demo_id: 6a4402a6f14e94517beb8474
demoforge_share_token: 3deb4110-e216-4ef8-9082-d78c765ebc4a
demoforge_api_latency_ms: 207
```

## 6. Commit history (skill/telemetry)

- `6e09f065` Remove separate demoforge_share_link event; consolidate into main response.
- `229293f8` Use video_platform instead of overwriting video_source.
- `10c7a485` Preserve original video_meta shape; namespace DemoForge fields.
- (this change) Align DemoForge metadata with original shape in
  `video_telemetry_metadata`; remove duplicated patch block in kb_answer.

## 7. Deployment / environment note

- **SuperAgent prod is UNCHANGED** — no commits have been pushed. All the
  stray `demoforge_share_link` traces seen in Langfuse were from **local testing
  against pre-fix code** (timestamps ≤ 07:47 on 2026-07-02). Post-fix local runs
  create zero separate events.
- SuperAgent pulls skill code from the git remote. Deploying the fix = pushing,
  then SuperAgent redeploys.

## 8. Open / next tasks

- [ ] (this session) Final GitHub push of consolidated + aligned telemetry.
- [ ] Delete pre-fix test traces from Langfuse via
      `langfuse_client.delete_traces()` so the CxO dashboard stays clean.
- [ ] **GitLab migration** (next): collect GitLab URL / project ID / PAT / branch /
      namespace; add GitLab env vars to `.env`; comment out GitHub vars; update
      code that fetches KB content from GitHub → GitLab API; document required
      SuperAgent skill-setting env var changes.
- [ ] Test-harness gaps (from earlier Sonnet run, not code bugs): RCS module
      detection (`Channels` vs `rcs` key), Bot Studio `definition` vs `overview`
      intent expectation, email resolution in `Ctx` for Test E.
