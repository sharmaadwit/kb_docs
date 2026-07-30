# DemoForge Integration - Quick Reference

**Status**: Test plan complete, ready for sprint planning  
**Pass Rate**: 5/6 tests (83.3%)  
**Total Effort**: ~22 hours  
**Timeline**: 3-4 weeks

---

## What is DemoForge?

Interactive guided product demos hosted at `https://demoforge-ui.gupshup.io`. Users see features in action instead of watching videos or reading docs.

**Benefits**:
- Sales: Close faster with interactive demos
- CS: Onboard users faster with guided walkthroughs
- Product: See which features users care about

---

## Test Results at a Glance

| Query | Intent | Module | Expected | Result | Status |
|-------|--------|--------|----------|--------|--------|
| "How do I create a campaign?" | how_to | campaigns | DemoForge | Campaign Manager Demo | ✅ |
| "What is Bot Studio?" | overview | bot_studio | YouTube | Bot Studio video | ✅ |
| "How do I set up a campaign?" | how_to | campaigns | DemoForge | Campaign Manager Demo | ✅ |
| "How do I set up webhooks?" | how_to | webhooks | Fallback | Text answer | ✅ |
| "How do I build a bot?" | how_to | bot_studio | YouTube | YouTube video | ✅ |
| "Show me a demo of Gupshup" | overview | None | DemoForge (General) | Text answer | ⚠️ FAIL |

---

## Available Demos (8 Total)

| Demo | Module | Use Case | Best For |
|------|--------|----------|----------|
| Campaign Manager | campaigns | Bulk sending with personalization | Marketing teams |
| Personalize | personalization | Event-driven profile enrichment | Segmentation |
| AI Admin | ai_admin | Domain-tuned LLM for banking | Banking support |
| RCS | rcs | Rich messaging with fallback | Marketing campaigns |
| CTWA | ctwa | Click-to-WhatsApp lead forms | B2B sales |
| Agent Assist | agent_assist | Real-time agent suggestions | Support teams |
| Bot Studio | bot_studio | Multi-channel bot building | Product teams |
| General Demo | platform | Platform walkthrough | Sales/presales |

**Unmapped modules** (need demos):
- Webhooks / Integrations
- WhatsApp Templates
- Analytics
- Customer 360

---

## How It Works

```
User Question
    ↓
KB Answer Pipeline
    ├─ Detect Intent (how_to, overview, setup, etc.)
    ├─ Detect Module (campaigns, bot_studio, etc.)
    ├─ Generate Answer
    └─ Attach Demo
        ├─ Try DemoForge (intent + module → demo_id)
        ├─ Call API for share token
        ├─ Build share URL
        └─ Return with answer

Result: "Here's the answer... Try it live: https://demoforge-ui.gupshup.io/s/share_abc123"
```

---

## Implementation Phases

### Phase 1: Manifest Indexing (2h)
Update `kb/demoforge_manifest.json` to add:
```json
{
  "module_to_demos": {
    "campaigns": {"how_to": "6a4402a6f14e94517beb8474"},
    ...
  },
  "demos_by_id": {...}
}
```

### Phase 2: Demo Selection (4h)
Update `kb_video.py`:
- `select_demoforge_demo(query, intent, module, context)` → demo dict
- Add broad query fallback
- Handle unmapped modules gracefully

### Phase 3: API Integration (6h)
Create `demoforge_api.py`:
- `create_share_token(demo_id, context)` → share_token
- `build_share_url(share_token)` → full URL
- Handle errors: timeout, 401, 429, 500
- Fallback to YouTube on failure

### Phase 4: KB Answer Integration (3h)
Update `kb_answer.py`:
- Call demo selection after generating answer
- Add demo to response dict
- Add Langfuse telemetry fields

### Phase 5: Testing (4h)
- Run full test suite
- Manual testing with real queries
- Verify fallback behavior

### Phase 6: Monitoring (3h)
- Add Langfuse dashboard
- Set up alerts
- Track demo metrics

**Total: ~22 hours, 3-4 weeks**

---

## Key Metrics to Monitor

| Metric | Target | Purpose |
|--------|--------|---------|
| Demo selection accuracy | 95%+ | Users get right demo |
| API latency | <500ms | No user wait |
| Fallback success rate | 100% | Never crash |
| Demo adoption rate | >20% | Users click links |
| Feature coverage | 100% | All modules have demos |

---

## Files to Review

| File | Purpose | Size |
|------|---------|------|
| `demoforge_integration_test.json` | Test results (detailed) | 5 KB |
| `DEMOFORGE_INTEGRATION_GUIDE.md` | Full implementation guide | 15 KB |
| `DEMOFORGE_API_INTEGRATION.md` | API client code & examples | 12 KB |
| `DEMOFORGE_TEST_EXECUTION_SUMMARY.md` | Test analysis & next steps | 18 KB |
| `test_demoforge_integration.py` | Test harness (runnable) | 6 KB |

---

## Failure Analysis

### Test 6 Failed: Broad Pitch Queries
**Issue**: General Demo not returned for "Show me a demo of Gupshup"

**Root Cause**: Broad query fallback logic not implemented in `select_demoforge_demo()`

**Fix**: Add check before returning None:
```python
if entry is None and _is_broad_query(query):
    # Return General Demo as fallback
```

**Impact**: Medium (sales/presales use case, but YouTube fallback works)

---

## API Details

**Endpoint**: `https://demoforge-api.gupshup.io/api/shares`

**Auth**: `Authorization: Bearer {DEMOFORGE_PAT}`

**Request**:
```json
{
  "demo_id": "6a4402a6f14e94517beb8474",
  "expires_in_days": 7,
  "metadata": {"source": "kb_answer", "query": "..."}
}
```

**Response**:
```json
{
  "share_token": "share_abc123def456",
  "share_url": "https://demoforge-ui.gupshup.io/s/share_abc123def456",
  "demo_id": "6a4402a6f14e94517beb8474",
  "created_at": "2026-07-02T10:30:00Z",
  "expires_at": "2026-07-09T10:30:00Z"
}
```

**Timeout**: 5 seconds (fallback to YouTube if API slow)

**Errors**: 400, 401, 429, 5xx → fallback gracefully

---

## Environment Variables

```bash
# Required
DEMOFORGE_PAT=pat_GHOIyphtorBRclEv_gXpcfSKE4nMqNuZlHUue0Gq3jI
DEMOFORGE_BASE_URL=https://demoforge-api.gupshup.io
DEMOFORGE_FRONTEND_URL=https://demoforge-ui.gupshup.io

# Optional (already in code defaults)
KB_DEMOFORGE_MANIFEST_PATH=kb/demoforge_manifest.json
```

---

## Rollout Plan

### Phase 1: Staging
- Deploy to staging environment
- Run full test suite
- Manual testing with real API
- Measure baseline metrics

### Phase 2: Beta
- Deploy to 10% of users
- Monitor Langfuse for errors
- Gather user feedback
- Fix any issues

### Phase 3: Gradual Rollout
- Deploy to 25%, 50%, 100% over 1-2 weeks
- Monitor metrics continuously
- Be ready to rollback if issues

### Phase 4: Full Production
- All users get DemoForge integration
- Monitor long-term adoption
- Plan next iteration (unmapped modules, etc.)

---

## Troubleshooting Checklist

**Demo not showing?**
- [ ] Manifest has `module_to_demos` index? `grep -c "module_to_demos" kb/demoforge_manifest.json`
- [ ] `DEMOFORGE_PAT` loaded? `echo $DEMOFORGE_PAT`
- [ ] Intent/module detected? Check Langfuse trace
- [ ] API responding? `curl -H "Authorization: Bearer $PAT" https://demoforge-api.gupshup.io/api/demos/{demo_id}`

**API timeout?**
- Check DemoForge status page
- Verify network connectivity
- Monitor `demo_api_latency_ms` in Langfuse
- Fallback to YouTube should work automatically

**Test failing?**
- Run: `python3 local/scripts/test_demoforge_integration.py`
- Check log output for specific errors
- Review `demoforge_integration_test.json` for results

---

## Success Looks Like

✅ **After implementation**:
- User asks "How do I create a campaign?"
- Gets answer + "Try it live: https://demoforge-ui.gupshup.io/s/share_abc123"
- Clicks link, sees 5-minute guided demo
- Clicks "Create Campaign" button in demo
- Goes back to Gupshup console to set up campaign
- *Success!* Demo reduced time-to-value by 50%

---

## Questions for Team

1. **Should we launch with all 8 demos, or start with campaigns + bot_studio only?**
   - Risk-minimization: Start with 2, expand later
   - Full-feature: Launch all 8, some may not be used

2. **Do we need explicit user consent to track demo clicks?**
   - Already captured in Langfuse (implicit analytics)
   - Consider privacy policy review

3. **What's the SLA if DemoForge API is down?**
   - 5-second timeout → fallback to YouTube
   - This should handle most outages

4. **How do we measure ROI?**
   - Track: demo clicks, completion time, conversion impact
   - Compare: demo users vs. non-demo users (A/B test later)

5. **Timeline: Can this ship in 3-4 weeks?**
   - Yes, if allocated full-time (22 hours total)
   - Depends on: API access, team bandwidth, testing schedule

---

## Contact & Resources

**Documentation**:
- Full guide: `local/reports/DEMOFORGE_INTEGRATION_GUIDE.md`
- API guide: `local/reports/DEMOFORGE_API_INTEGRATION.md`
- Test summary: `local/reports/DEMOFORGE_TEST_EXECUTION_SUMMARY.md`

**Code**:
- Test script: `local/scripts/test_demoforge_integration.py`
- KB Video module: `skill/kb_video.py` (add select_demoforge_demo)
- KB Answer module: `skill/kb_answer.py` (integrate demo selection)

**External**:
- DemoForge UI: https://demoforge-ui.gupshup.io
- DemoForge API: https://demoforge-api.gupshup.io/docs
- Manifest: `kb/demoforge_manifest.json`

---

**Last Updated**: July 2, 2026  
**Next Review**: Sprint planning meeting  
**Owner**: Analytics & Telemetry Team
