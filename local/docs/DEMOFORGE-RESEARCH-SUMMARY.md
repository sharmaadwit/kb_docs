# DemoForge Integration — Research Complete

**Status:** ✅ All research done. Ready for Phase 1-4 implementation.

**Documents Created:**
1. `DEMOFORGE-INTEGRATION-PLAN.md` — 4-phase implementation roadmap
2. `DEMOFORGE-API-REFERENCE.md` — Full API docs + production-ready code

---

## What We Learned

### Current KB Video Architecture
- Videos stored in `kb/video_manifest.json` (KB source → YouTube)
- Selected in `kb_video.py` (source-page driven)
- Integrated post-answer in `kb_answer.py:6112-6178`
- Available metadata: query, intent, module, evidence (source, heading, score)

### DemoForge API (Live Tested)
- **3 endpoints:** list projects, list demos, mint share link
- **Latency:** 0.09–0.5s (5s timeout recommended)
- **Idempotent:** POST /share always returns same token for same demo
- **Schemas:** Full JSON documented in DEMOFORGE-API-REFERENCE.md
- **Error handling:** Only retry on 429/5xx + timeouts, never on 4xx
- **Integration-ready:** All code snippets provided

### Integration Strategy
- Create `demoforge_manifest.json` — intent + module → demo_id mapping
- Add `select_demoforge_demo()` in kb_video.py (intent + module driven)
- Call DemoForge API at response time in kb_answer.py (post-answer, after YouTube selection)
- Fallback to YouTube on any API error (no response degradation)
- Feature-flagged rollout per module

---

## Ready to Build

### Phase 1: Config (Days 1-2)
- Map modules to DemoForge projects
- Create `demoforge_manifest.json` with intent→demo mappings
- **Blocker:** Confirm share URL path with DemoForge team

### Phase 2: Selection Logic (Days 3-4)
- Add `select_demoforge_demo()` to kb_video.py
- Code template ready (from research)

### Phase 3: API Integration (Days 4-6)
- Wire DemoForge into kb_answer.py:6112-6178
- All code snippets in DEMOFORGE-API-REFERENCE.md, production-ready
- Implement `_mint_demoforge_share_link()` with retry/timeout

### Phase 4: Testing & Rollout (Days 6-8)
- Unit tests: selection logic, API calls, error handling
- Integration tests: 5-10 queries per module
- Canary rollout: Campaign Manager → Bot Studio → full enable

---

## Next Steps

1. **Confirm with DemoForge team:**
   - Which projects map to which modules? (Campaign Manager, Bot Studio, etc.)
   - Which modules have ≥3 complete demos ready?
   - **Exact share URL path** (confirm `https://demoforge.gupshup.io/share/{token}`)

2. **Start Phase 1:**
   - Once project mappings known, build `demoforge_manifest.json`

3. **Parallel Phase 2-3:**
   - Code `select_demoforge_demo()` + wire API calls into kb_answer.py

4. **Phase 4:**
   - Comprehensive testing + canary rollout

---

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| DemoForge API down | Graceful fallback to YouTube (no response delay) |
| Share URL path wrong | Placeholder code; easy fix once confirmed |
| Low demo coverage | Start with Campaign Manager (highest coverage), expand gradually |
| Performance regression | <2s API timeout; async calls don't block response |
| Demo quality poor | Feature flag per module; easy to disable/swap demos |

---

## Files & Code

**Reference documents:**
- `DEMOFORGE-INTEGRATION-PLAN.md` — Full 4-phase plan
- `DEMOFORGE-API-REFERENCE.md` — API schemas + production code snippets

**To be created:**
- `kb/demoforge_manifest.json` — Intent+module → demo mappings (Phase 1)
- `skill/kb_video.py` — `select_demoforge_demo()` function (Phase 2)
- `skill/kb_answer.py` — API integration + `_mint_demoforge_share_link()` (Phase 3)
- `local/tests/test_demoforge_integration.py` — Unit + integration tests (Phase 4)

---

## Key Metrics (Monitoring)

Track in Langfuse dashboard:
- Demo delivery rate (% of responses with DemoForge)
- API success rate (% of share-link mints successful)
- Fallback rate (% reverting to YouTube)
- API latency (p50/p95)
- Module-level breakdown (which modules benefited most)

---

**Research completed:** 2026-07-01  
**Status:** Ready for Phase 1 kickoff  
**Owner:** Code Change Agent + Subagent (Opus)

