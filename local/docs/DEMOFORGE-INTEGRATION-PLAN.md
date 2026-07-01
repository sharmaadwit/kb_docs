# DemoForge Integration Plan — KB Responses

**Objective:** Replace/augment static YouTube links with dynamic DemoForge demo share links, selected by query intent + module.

**Scope:** Single demo per answer (non-overview intent), matching current YouTube approach.

**Timeline:** 4 phases, ~2-3 weeks (sequential; can parallelize Phase 2-3).

---

## Executive Summary

**Current State:**
- Videos stored in `kb/video_manifest.json` — manually curated KB source → YouTube video_id mappings
- Selection logic in `kb_video.py` — picks by KB page + intent + keyword overlap
- Integration point: post-answer enrichment in `kb_answer.py:6112-6178`

**Desired State:**
- Add DemoForge demo selection alongside YouTube
- Select demo by: query intent + module (+ KB source as tiebreaker)
- Call DemoForge API at response time to mint share token → `/shared/{token}/autoplay` URL
- Embed in response like YouTube (section in answer + telemetry)

**Key Decision:** DemoForge selection is **intent + module driven** (not source-page driven like YouTube), because sales demos are organized by use case/module, not KB structure.

---

## Phase 1: Discovery & Config (Days 1-2)

### 1.1 Map KB Modules → DemoForge Projects

**Objective:** Create a mapping file linking module names to DemoForge project IDs.

**Inputs:**
- Available DemoForge projects (from `demoforge-api.gupshup.io/projects`)
- KB modules in use (from `skill/kb_search.py:30-52` EXPLICIT_MODULES)

**Deliverable:** `kb/demoforge_manifest.json`

**Structure:**
```json
{
  "module_to_projects": {
    "Campaign Manager": {
      "project_id": "...",
      "project_name": "Campaign Manager Demos",
      "intent_demo_map": {
        "how_to": {
          "demo_id": "...",
          "name": "Create Campaign E2E",
          "industry": "Retail",
          "persona": "Marketing Manager",
          "fallback": true
        },
        "overview": {
          "demo_id": "...",
          "name": "Campaign Manager Overview",
          "industry": "General",
          "persona": "All",
          "fallback": false
        }
      }
    },
    "Bot Studio": { ... },
    "Agent Assist": { ... },
    ...
  },
  "demoforge_api": {
    "base_url": "https://demoforge-api.gupshup.io",
    "frontend_url": "https://demoforge-ui.gupshup.io",
    "pat_env_var": "DEMOFORGE_PAT",
    "share_url_template": "{frontend_url}/shared/{share_token}/autoplay"
  },
  "fallback_strategy": {
    "default_demo_id": "console-overview-demo",
    "when_no_match": "broad_discovery",
    "when_api_fails": "youtube_fallback"
  }
}
```

**Tasks:**
- [ ] List all DemoForge projects via API (use test PAT)
- [ ] Map each project to 1-2 KB modules
- [ ] For each module, identify 2-3 key intents (how_to, overview, deep_dive)
- [ ] Pre-select best demo per intent per module (from DemoForge demos list)
- [ ] Store demo_id, name, industry, persona for each mapping
- [ ] Document fallback strategy (which demo if module not mapped, if API fails)

**Output:** `kb/demoforge_manifest.json` (checked into repo, no secrets)

---

## Phase 2: Video Selection Logic (Days 3-4)

### 2.1 Add DemoForge Selection to `kb_video.py`

**Objective:** Create `select_demoforge_demo()` function mirroring `select_video()` but intent + module driven.

**File:** `skill/kb_video.py`

**New function signature:**
```python
def select_demoforge_demo(
    query: str,
    intent: str,
    module: str,
    context: dict,
    language: str = "en"
) -> dict | None:
    """
    Select a DemoForge demo by query intent + module.
    
    Returns:
        {
            "type": "demoforge",
            "demo_id": "...",
            "name": "...",
            "industry": "...",
            "persona": "...",
            "share_token": None,  # filled later via API
            "url": None,  # filled later via API
            "fallback": bool
        }
        or None if no match.
    """
```

**Logic:**
1. Load `demoforge_manifest.json` (cached in context)
2. Look up module in `module_to_projects`
3. If module not found → return fallback demo (broad_discovery)
4. Map intent (overview, how_to, setup, etc) → demo_id from `intent_demo_map`
5. Return demo metadata (demo_id, name, industry, persona)
6. **Do NOT call API here** — that happens in Phase 3 at the integration point

**Tasks:**
- [ ] Implement `select_demoforge_demo()`
- [ ] Add manifest loader (cache in context, like video_manifest)
- [ ] Add intent-to-demo mapper (handle missing intent gracefully)
- [ ] Add fallback logic (module not found, intent not found, etc.)
- [ ] Add unit tests (3-5 test cases: happy path, missing module, missing intent, fallback)

**Output:** `kb_video.py` updated with demo selection logic

---

## Phase 3: API Integration (Days 4-6)

### 3.1 Wire DemoForge into Response Pipeline

**Objective:** Call DemoForge API to mint share links at the moment of answer composition.

**File:** `skill/kb_answer.py`

**Integration point:** `kb_answer.py:6112-6178` (post-answer enrichment)

**Current code pattern:**
```python
# Line 6129-6155
if intent == "overview" and is_platform_pitch_query:
    videos = kb_video.catalog_videos(...)
elif intent == "overview":
    videos = kb_video.select_videos(...)
else:
    videos = [kb_video.select_video(...)]
```

**New pattern:**
```python
# Parallel: try DemoForge first, fallback to YouTube
if intent != "overview":  # single-demo path
    # Try DemoForge demo
    demoforge_candidate = kb_video.select_demoforge_demo(
        query=query,
        intent=intent,
        module=explicit_module,
        context=context,
        language=lang
    )
    if demoforge_candidate:
        # Call API to mint share link
        demoforge_demo = await _mint_demoforge_share_link(
            demo_id=demoforge_candidate["demo_id"],
            context=context
        )
        if demoforge_demo:
            videos = [demoforge_demo]
        else:
            # API failed, fallback to YouTube
            videos = [kb_video.select_video(...)]
    else:
        # No DemoForge match, use YouTube
        videos = [kb_video.select_video(...)]
else:
    # Overview path: YouTube catalog (keep as-is)
    videos = kb_video.catalog_videos(...)
```

### 3.2 Implement `_mint_demoforge_share_link()`

**File:** `skill/kb_answer.py` (new helper function)

**Use code from:** `DEMOFORGE-API-REFERENCE.md` (production-ready snippets included)

**Function signature:**
```python
async def _mint_demoforge_share_link(
    client: httpx.AsyncClient,
    pat: str,
    demo_id: str,
    max_retries: int = 2
) -> dict | None:
    """
    Call DemoForge API to get share token. Idempotent.
    
    Returns:
        {"share_token": "...", "share_status": "active", "share_url": "..."}
        or None on error.
    """
```

**Key behaviors (from live testing):**
1. Load DemoForge PAT from env var `DEMOFORGE_PAT`
2. POST to `/demos/{demo_id}/share` with Bearer auth (timeout: 5s total, 3s connect)
3. Extract `share_token` (UUIDv4) and `share_status` from response
4. Build URL: `https://demoforge.gupshup.io/share/{share_token}` (⚠️ path needs confirmation)
5. Return enriched dict with `share_token`, `share_status`, `share_url`

**Error handling (from API testing):**
- 401 (invalid PAT) → log warning, return None (fallback to YouTube)
- 404 (demo not found) → log warning, return None (fallback to YouTube)
- 400 (bad ID format) → log error, return None (don't retry)
- 5xx (API down) → retry with backoff (max 2 retries), then return None
- Timeout → retry with backoff (max 2 retries), then return None

**Retry strategy:**
- Only retry on 429/5xx + timeouts
- Never retry on 4xx
- Exponential backoff: 250ms → 1s
- Max 2 retries

**Tasks:**
- [ ] Copy `share_demo()` function from DEMOFORGE-API-REFERENCE.md
- [ ] Integrate into kb_answer.py with proper imports
- [ ] Load PAT from env var at skill startup
- [ ] Add telemetry: demo_id, api_latency, error (if any)
- [ ] Log all calls (success + failures) for monitoring

### 3.3 Update Response Embedding

**File:** `skill/kb_answer.py:6160-6165` (_append_videos_section)

**Current:**
```python
def _append_videos_section(answer, videos):
    # Assumes YouTube format
    for v in videos:
        answer += f"\n\n**Watch:** {v['title']}\n{v['url']}"
```

**Updated:**
```python
def _append_videos_section(answer, videos):
    for v in videos:
        if v.get("type") == "demoforge":
            answer += f"\n\n**See it in action:** {v['name']} ({v['industry']} · {v['persona']})\n{v['url']}"
        else:  # YouTube
            answer += f"\n\n**Watch:** {v['title']}\n{v['url']}"
    return answer
```

**Tasks:**
- [ ] Update `_append_videos_section()` to handle DemoForge type
- [ ] Update telemetry/logging to track video type (youtube vs demoforge)
- [ ] Update response schema to include `video_type` field

---

## Phase 4: Testing & Rollout (Days 6-8)

### 4.1 Unit Tests

**File:** `local/tests/test_demoforge_integration.py`

**Test cases:**
```
1. select_demoforge_demo() — happy path (module + intent → demo_id)
2. select_demoforge_demo() — missing module (fallback to broad_discovery)
3. select_demoforge_demo() — missing intent (fallback to default)
4. _mint_demoforge_share_link() — success (demo_id → share_token + URL)
5. _mint_demoforge_share_link() — auth failure (401 → None, no crash)
6. _mint_demoforge_share_link() — not found (404 → None, fallback)
7. _mint_demoforge_share_link() — timeout (>2s → None, fallback)
8. Response embedding — DemoForge demo in answer (check formatting)
9. Response embedding — YouTube fallback when DemoForge unavailable
10. Full integration — query → module detection → demo selection → API call → response
```

**Tasks:**
- [ ] Write unit tests with mocked DemoForge API
- [ ] Test with real DemoForge API (staging PAT) against test project
- [ ] Verify response formatting (demo name + industry + persona + URL)
- [ ] Verify telemetry (video_type, demo_id logged)

### 4.2 Integration Tests

**File:** `local/tests/test_demoforge_end_to_end.py`

**Scenarios:**
1. **Campaign Manager how-to query** → DemoForge demo returned
2. **Bot Studio overview query** → YouTube catalog (not DemoForge)
3. **Unmapped module query** → YouTube fallback
4. **API down scenario** → YouTube fallback, no response delay
5. **Performance** — API call <2s, no response latency spike

**Tasks:**
- [ ] Create 5-10 test queries per module
- [ ] Run against both YouTube and DemoForge enabled
- [ ] Measure API latency + response time
- [ ] Check telemetry for demo selection decisions

### 4.3 Rollout Strategy

**Phase 4a: Canary (Days 6-7)**
- Enable DemoForge for Campaign Manager only (highest demo coverage)
- Monitor: API success rate, latency, fallback rate, user engagement
- Target: >95% API success, <2s latency, <5% fallback

**Phase 4b: Expand (Day 7)**
- Enable for Bot Studio, Agent Assist (next highest coverage)
- Monitor same metrics
- Gather user feedback (ask customers if demos useful)

**Phase 4c: Full Rollout (Day 8)**
- Enable for all mapped modules
- Keep YouTube as fallback for unmapped modules

**Tasks:**
- [ ] Add feature flag: `feature_demoforge_demos` (default: false)
- [ ] Add per-module feature flag: `feature_demoforge_demos.campaign_manager`
- [ ] Add dashboard monitoring (Langfuse) for demo delivery + type
- [ ] Document rollout plan in deployment guide

---

## Deployment & Operations

### Secrets & Config

**Required environment variable:**
```bash
DEMOFORGE_PAT=pat_<43char>
```

**In `context` or config:**
- `kb/demoforge_manifest.json` (no secrets, checked in)
- PAT loaded from env at skill startup

### Monitoring & Observability

**Telemetry points:**
```python
# In kb_answer.py, when demo is selected:
telemetry = {
    "video_type": "demoforge",
    "demo_id": demo_id,
    "module": explicit_module,
    "intent": intent,
    "api_latency_ms": elapsed_time,
    "fallback_reason": None  # or "api_failure", "no_match", "timeout"
}
```

**Dashboard (Langfuse):**
- Demo delivery rate (% of responses with demo)
- API success rate (% of share-link mints successful)
- Fallback rate (% using YouTube instead)
- Average latency (API call time)
- Engagement (future: click-through on demo links)

### Rollback Plan

**If API is down:**
- Automatic fallback to YouTube in `_mint_demoforge_share_link()` → no response degradation

**If integration breaks:**
- Feature flag `feature_demoforge_demos: false` → disables all DemoForge, reverts to YouTube only
- Redeploy last known-good `kb_answer.py`

**If demos are low quality:**
- Update `demoforge_manifest.json` to map to different demos (no code change)
- Or disable per-module: `feature_demoforge_demos.campaign_manager: false`

---

## File Changes Summary

| File | Change | Lines | Priority |
|------|--------|-------|----------|
| `kb/demoforge_manifest.json` | Create | ~100 | P0 |
| `skill/kb_video.py` | Add `select_demoforge_demo()` | +100 | P0 |
| `skill/kb_answer.py` | Add `_mint_demoforge_share_link()` + integration | +150 | P0 |
| `skill/kb_answer.py` | Update `_append_videos_section()` | +10 | P0 |
| `skill/kb_search.py` | (Optional) Use module in selection | ±5 | P1 |
| `local/tests/test_demoforge_integration.py` | Create | +200 | P1 |
| `local/docs/DEMOFORGE-DEPLOYMENT.md` | Create (ops guide) | +100 | P2 |

---

## Success Criteria

- ✅ DemoForge demos served in KB responses for mapped modules
- ✅ API success rate >95%, latency <2s
- ✅ YouTube fallback works seamlessly
- ✅ Zero response degradation (no timeout / block)
- ✅ Telemetry shows demo selection + API performance
- ✅ Staging environment fully tested before prod rollout

---

## API Findings (From Live Testing)

**Tested 2026-07-01. Full reference:** See `DEMOFORGE-API-REFERENCE.md`

| Finding | Impact |
|---------|--------|
| **Latency:** 0.09–0.5s | Recommend 5s timeout (3s connect) — ample headroom |
| **Idempotent** | POST /share called twice → same token returned; safe to retry |
| **Pre-minted token** | Every demo has `share_token` (UUIDv4) before POST; POST just activates `share_status` |
| **Error handling** | 401=PAT invalid, 404=not found, 400=bad ID. Only retry on 429/5xx, NEVER on 4xx |
| **Share URL** | ⚠️ **Unverified** — likely `https://demoforge.gupshup.io/share/{token}` but needs DemoForge confirmation |
| **Code ready** | All snippets in DEMOFORGE-API-REFERENCE.md, production-ready with retry/timeout logic |

---

## Remaining Open Questions (Before Phase 2 Kick-Off)

1. **DemoForge project structure:** How are projects organized? One per module, or shared projects with multiple modules' demos?
2. **Demo availability:** Which modules have >3 completed demos ready? (determines initial rollout scope)
3. **Intent mapping:** Beyond `how_to` and `overview`, what other intents should map to demos? (e.g., `setup`, `troubleshoot`, `best_practices`)
4. **PAT management:** Load from env var `DEMOFORGE_PAT` (recommended for security) ✅ Decided
5. **Metrics:** Beyond API success + latency, what engagement metrics matter most? (demo plays, link clicks, demo completion time?)
6. **Module metadata:** Some KB responses span multiple modules — should we prefer the primary module or allow multi-demo responses?
7. **⚠️ Share URL path:** Confirm exact viewer path with DemoForge team (currently hardcoded as placeholder in code)

---

## Next Steps

1. **Phase 1 kickoff:** Map modules to DemoForge projects (requires access to DemoForge API + project list)
2. **Phase 2 parallel:** Start coding `select_demoforge_demo()` once manifest is clear
3. **Phase 3 parallel:** Wire API calls into response pipeline
4. **Phase 4:** Comprehensive testing + staged rollout

**Estimated effort:** ~40-50 hours across 2-3 weeks, depending on demo availability and API stability.

---

**Created:** 2026-07-01  
**Owner:** Code Change Agent + Analytics Agent  
**Status:** Ready for review & Phase 1 kickoff
