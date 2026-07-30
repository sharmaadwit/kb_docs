# DemoForge + Langfuse Integration — Test Plan

**Test script:** `local/tests/test_demoforge_langfuse_integration.py`
**Report output:** `local/reports/test_demoforge_langfuse_report.json`
**Status:** Design + code ready. NOT executed yet.

---

## 0. Integration-readiness finding (read first)

The skill currently implements demo **selection** only:

- `kb_video.select_demoforge_demo(query, intent, module, context)` returns
  `{type, demo_id, name, industry, persona, share_token=None}`.

The following pieces described in the objective **do not exist yet** in the skill:

| Piece | Current state |
|---|---|
| DemoForge `create_share_token` API call | Not implemented (`share_token` is always `None`) |
| `video_selection` discrete Langfuse event | Not implemented — telemetry goes through `_send_langfuse` as flat `video_meta` fields |
| `superagentData.email` in request body | Not implemented (no API call exists) |
| `video_type` / `source` / `fallback_reason` / `api_latency_ms` fields | Not emitted |
| DemoForge share URL `https://demoforge-ui.gupshup.io/shared/{token}/autoplay` | Not built (kb_video only builds YouTube `/watch` URLs) |

Because of the project role rules (analytics/testing agent — no skill edits without
approval), the test was written to the **target contract**. It:

- Runs today without failing (DemoForge assertions report **PENDING**, not FAIL).
- Auto-detects when the integration lands via hooks
  (`kb_video.create_share_token` / `kb_answer._demoforge_share` /
  `demoforge_share_token`) and then activates full assertions.
- Serves as the **acceptance gate** for the integration work.

Environment is ready: `.env` already contains `DEMOFORGE_PAT`,
`DEMOFORGE_BASE_URL=https://demoforge-api.gupshup.io`,
`DEMOFORGE_FRONTEND_URL=https://demoforge-ui.gupshup.io`, and all three Langfuse keys.

---

## 1. Setup

1. `DEMOFORGE_PAT` present in `.env` — confirmed
   (`pat_GHOIyphtorBRclEv_gXpcfSKE4nMqNuZlHUue0Gq3jI`).
2. Langfuse `LANGFUSE_HOST` / `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` — confirmed present.
3. Test email: `test@demoforge-integration.test` (constant `TEST_EMAIL` in the script).
4. Required local data files (used as the network-boundary stubs):
   - `kb/kb_chunks.jsonl`
   - `kb/video_manifest.json`, `kb/video_transcripts/`
   - `kb/demoforge_manifest.json`

The script reads `.env` itself (no `python-dotenv` dependency) and only POSTs to
Langfuse / DemoForge in `--live` mode.

---

## 2. Execution plan (step by step)

### Step 1 — Offline mock run (default, deterministic, CI-safe)
```bash
python3 local/tests/test_demoforge_langfuse_integration.py --verbose
```
- Exercises the real `kb_answer()` / `kb_video` code paths.
- Stubs the network boundary: chunk loading, `kb_storage.read_json`, Langfuse
  ingestion (captured in-process), and the DemoForge share-token transport (mock).
- Writes `local/reports/test_demoforge_langfuse_report.json`.
- Exit code `0` when no `FAIL`/`ERROR` (PENDING/PARTIAL are acceptable pre-integration).

### Step 2 — Inspect the report
- Confirm `meta.demoforge_api_wired`. If `false`, DemoForge checks are PENDING by design.
- Confirm Test B and Test D (YouTube-expected) PASS today — those need no DemoForge.

### Step 3 — Live run (after integration lands, real APIs)
```bash
python3 local/tests/test_demoforge_langfuse_integration.py --live --verbose
```
- Uses real DemoForge `create_share_token` and real Langfuse ingestion.
- Captures real Langfuse trace IDs and real `api_latency_ms`.
- Verify traces in the Langfuse UI using the `trace_id`s in the report.

### Step 4 — Error/fallback matrix
- Runs automatically in every invocation (`error_scenarios` section): timeout,
  invalid PAT, demo-not-found. Confirms each raises a known error type that the
  integration must catch and downgrade to YouTube.

---

## 3. Test cases

| ID | Query | Expected video_type | Key assertions |
|---|---|---|---|
| A | "How do I create a campaign in Gupshup?" | demoforge | intent=how_to, module=campaigns, demo_id=`6a4402a6f14e94517beb8474`, share_token set, url starts `https://demoforge-ui.gupshup.io/...`, ends `/autoplay`, source=demoforge, api_latency_ms recorded |
| B | "What is Bot Studio?" | youtube | intent=overview, url contains youtube.com, no demo_id, fallback_reason=`overview_intent` |
| C | "How do I send an RCS message?" | demoforge OR youtube | intent=how_to, module=rcs (mapping-dependent, lenient) |
| D | "How do I use the API?" | youtube | no demo_id, fallback_reason=`no_demoforge_match` |
| E | "How do I create a campaign in Gupshup?" | demoforge | request body contains `{"superagentData":{"email":"test@demoforge-integration.test"}}` |

---

## 4. Langfuse telemetry fields verified

Event name (target): `video_selection`. Fields checked:

| Field | Type | When present | Assertion |
|---|---|---|---|
| `intent` | string | always | matches expected (lenient today) |
| `module` | string | always | matches expected (lenient today) |
| `video_type` | enum[demoforge, youtube, none] | always | strict per test case |
| `demo_id` | string | demoforge only | equals expected id / absent on youtube |
| `share_token` | string | demoforge only | populated / absent on youtube |
| `api_latency_ms` | number | demoforge only | recorded AND < 2000 |
| `source` | string | demoforge only | equals `demoforge` |
| `fallback_reason` | string | youtube only | `overview_intent` / `no_demoforge_match` |
| `email` | string | demoforge request | equals test email in `superagentData.email` |

---

## 5. Error scenarios (must NOT block the answer)

| Scenario | Simulated by | Expected behaviour |
|---|---|---|
| API timeout | `MockDemoForgeAPI(mode="timeout")` | catch → YouTube, `fallback_reason=api_timeout` |
| Invalid PAT | `mode="invalid_pat"` (HTTP 401) | catch → YouTube, `fallback_reason=invalid_pat` |
| Demo not found | `mode="not_found"` (HTTP 404) | catch → YouTube, `fallback_reason=demo_not_found` |

All fallbacks must return a valid answer; the DemoForge failure is non-fatal.

---

## 6. Performance metrics

- DemoForge share-token latency: **< 2s** hard assert; **< 1s** observed target.
- Total response time must not regress vs. YouTube-only baseline.
- No timeout errors in the happy path (`mode="ok"` ~0.4s in mock).

---

## 7. Expected output format

`local/reports/test_demoforge_langfuse_report.json`:

```json
{
  "meta": {
    "generated_at": "<iso8601>",
    "mode": "offline_mock | live",
    "demoforge_api_wired": false,
    "demoforge_hook": null,
    "test_email": "test@demoforge-integration.test",
    "demoforge_pat_present": true,
    "langfuse_configured": true,
    "note": "DemoForge API not yet wired ..."
  },
  "summary": { "pass": 0, "fail": 0, "partial": 0, "error": 0, "total": 5 },
  "tests": [
    {
      "id": "A_campaign_manager_how_to",
      "query": "How do I create a campaign in Gupshup?",
      "status": "PASS | PARTIAL | FAIL | ERROR",
      "trace_id": "kb-...-<hex>",
      "view": {
        "video_type": "demoforge",
        "url": "https://demoforge-ui.gupshup.io/shared/<token>/autoplay",
        "demo_id": "6a4402a6f14e94517beb8474",
        "share_token": "tok_...",
        "source": "demoforge",
        "fallback_reason": null,
        "api_latency_ms": 412.3,
        "email_in_body": "test@demoforge-integration.test"
      },
      "checks": [
        { "check": "video_type", "status": "PASS", "detail": "..." }
      ]
    }
  ],
  "error_scenarios": [
    { "mode": "timeout", "expected_fallback_reason": "api_timeout", "checks": [ ... ] }
  ],
  "langfuse_traces": [
    { "trace_id": "kb-...", "query": "...", "intents": ["..."], "module": "...", "video_meta": { } }
  ]
}
```

---

## 8. Verification checklist

**Setup**
- [ ] `.env` has `DEMOFORGE_PAT`, `DEMOFORGE_BASE_URL`, `DEMOFORGE_FRONTEND_URL`
- [ ] `.env` has `LANGFUSE_HOST` / `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY`
- [ ] `kb/demoforge_manifest.json` maps `campaign_manager.overview → 6a4402a6f14e94517beb8474`
- [ ] `kb/kb_chunks.jsonl` and `kb/video_manifest.json` present

**Offline run**
- [ ] Script runs to completion, writes the report JSON
- [ ] Test B (Bot Studio overview) → youtube, PASS
- [ ] Test D (API query) → youtube, PASS
- [ ] DemoForge tests (A, E) show PENDING while `demoforge_api_wired=false`
- [ ] `error_scenarios` all raise known error types

**Live run (post-integration)**
- [ ] `meta.demoforge_api_wired = true`
- [ ] Test A: demo_id, share_token, url `/autoplay`, source=demoforge, api_latency < 2s
- [ ] Test E: `email_in_body == test@demoforge-integration.test`
- [ ] Langfuse UI shows a `video_selection` event per query using reported trace_ids
- [ ] All error scenarios return a YouTube answer (never block)

---

## 9. Results interpretation

| Status | Meaning | Action |
|---|---|---|
| **PASS** | All active checks passed | none |
| **PARTIAL** | Functional checks pass; DemoForge checks PENDING (API not wired) | expected pre-integration; re-run after wiring |
| **PENDING** (per check) | Assertion deferred because the integration hook is absent | not a defect yet |
| **FAIL** | An active assertion failed | investigate: wrong video_type, missing token, bad URL, email not in body |
| **ERROR** | Exception during the run | check `traceback` in the report entry |

**Interpretation notes**
- Exit code is `0` unless there is a real FAIL/ERROR, so the harness is safe in CI
  before the integration exists.
- When `demoforge_api_wired` flips to `true`, PENDING checks become live — a
  previously-PARTIAL Test A that is still PARTIAL/FAIL then indicates a real gap.
- `api_latency_ms` in offline mode is the mock's simulated latency (~0.4s); trust
  the `--live` report for real numbers.

---

## 10. Wiring the integration to this harness (for the implementer)

The harness auto-activates full DemoForge assertions when ONE of these exists and
performs the share-token call:

- `kb_video.create_share_token(demo_id, email=..., pat=..., base_url=...)`, or
- `kb_answer._demoforge_share(...)`, or
- `*.demoforge_share_token(...)`

and when the selected video dict / `video_meta` carries:
`type="demoforge"`, `demo_id`, `share_token`, `source="demoforge"`,
`fallback_reason` (youtube path), `api_latency_ms`, and the share URL
`https://demoforge-ui.gupshup.io/shared/{token}/autoplay`.

The request body sent to DemoForge must be
`{"superagentData": {"email": "<user email>"}}` with `Authorization: Bearer <PAT>`.
```
```
