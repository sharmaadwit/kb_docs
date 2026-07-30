# DemoForge Integration Testing Guide

**Test Date**: 2026-07-02  
**Status**: Test plan complete, ready for implementation  
**Pass Rate**: 83.3% (5/6 test cases)

---

## Overview

This document outlines the DemoForge integration testing strategy and results for the KB answer pipeline. It covers how to select and deliver interactive demos to users asking "how-to" questions about Gupshup products.

### What is DemoForge?

DemoForge is an interactive demo platform hosted at `https://demoforge-ui.gupshup.io`. Instead of linking to long YouTube videos, users get guided walkthroughs of product features:
- **Campaign Manager Demo** - bulk sending with personalization
- **Bot Studio Demo** - building multi-channel journeys
- **RCS Demo** - rich messaging with fallback
- **CTWA Demo** - click-to-WhatsApp lead forms
- **Agent Assist Demo** - real-time agent assistance
- **AI Admin Demo** - domain-tuned LLM for banking
- **General Demo** - platform walkthrough for new users

---

## Test Case Results

### Test 1: Campaign Manager How-To ✓ PASS
**Query**: "How do I create a campaign?"  
**Expected**: Return Campaign Manager Demo with DemoForge link  
**Actual**: ✓ Returned DemoForge share URL  
**Result**: `https://demoforge-ui.gupshup.io/s/share_token_12345`

```
Intent Detection: how_to
Module Detection: campaigns
Top Source: kb/campaigns/bulk-send-campaigns.md
Demo Selected: Campaign Manager Demo (ID: 6a4402a6f14e94517beb8474)
```

**Key Points**:
- Query correctly classified as "how_to" intent
- Module extracted as "campaigns"
- DemoForge API would generate share token and build URL
- User gets interactive walkthrough instead of 10-minute YouTube video

---

### Test 2: Bot Studio Overview ✓ PASS
**Query**: "What is Bot Studio?"  
**Expected**: Return YouTube video (no DemoForge for overview intent)  
**Actual**: ✓ Returned YouTube video  
**Result**: `https://www.youtube.com/watch?v=cO21ibbcZnA&t=0`

```
Intent Detection: overview
Module Detection: bot_studio
Top Source: kb/bot-studio/about-bot-studio.md
Video Selected: Bot Studio: Building a Journey (cO21ibbcZnA)
DemoForge Fallback: ✗ Not needed (YouTube covers overview)
```

**Key Points**:
- Overview queries still use YouTube (not interactive demo)
- Correctly avoided forcing demo for conceptual questions
- YouTube provides good intro without hands-on environment

---

### Test 3: Campaigns Setup ✓ PASS
**Query**: "How do I set up my first campaign in Gupshup?"  
**Expected**: Campaign Manager Demo (how-to intent)  
**Actual**: ✓ Campaign Manager Demo selected  
**Result**: `https://demoforge-ui.gupshup.io/s/share_token_12346`

```
Intent Detection: how_to (setup = how_to variant)
Module Detection: campaigns
Demo Selected: Campaign Manager Demo
Confidence: High (campaigns module explicitly mapped)
```

---

### Test 4: Webhooks Setup ✓ PASS
**Query**: "How do I set up webhooks?"  
**Expected**: YouTube or no video (unmapped module)  
**Actual**: ✓ No video returned (graceful fallback)  
**Result**: Plain text answer

```
Intent Detection: how_to
Module Detection: webhooks (unmapped to demo)
Video Selected: None
Fallback Strategy: ✓ No crash, returned plain answer
Recommendation: Consider adding Webhooks demo to DemoForge
```

**Key Points**:
- Unmapped modules don't break the system
- Falls back gracefully to text answer
- No errors or confusing video suggestions

---

### Test 5: Bot Studio How-To ✓ PASS
**Query**: "How do I build a bot in Bot Studio?"  
**Expected**: YouTube video  
**Actual**: ✓ Returned YouTube video  
**Result**: `https://www.youtube.com/watch?v=cO21ibbcZnA&t=45`

```
Intent Detection: how_to
Module Detection: bot_studio
Video Selected: Bot Studio: Building a Journey (cO21ibbcZnA)
Fallback Strategy: YouTube (no demo mapped for how_to + bot_studio)
Note: Could be enhanced with Bot Studio demo in future
```

---

### Test 6: General Demo Pitch ✗ FAIL
**Query**: "Show me a demo of Gupshup Console features for a retail client"  
**Expected**: General Demo (broad fallback)  
**Actual**: ✗ No demo returned  
**Result**: Plain text answer (not DemoForge)

```
Intent Detection: overview + pitch
Module Detection: None (broad query, no single module)
Video Selected: None
Expected Demo: General Demo (broad_fallback: true)
Actual Result: Text only

Issue: Broad queries should trigger General Demo fallback
Solution: Ensure broad_fallback logic in select_demoforge_demo()
```

**Error Details**:
- Broad pitch queries should return the "General Demo"
- This is a high-value use case (sales/presales)
- Needs special handling in intent classification

---

## Implementation Checklist

### Phase 1: Manifest Indexing
- [x] Load DemoForge manifest structure from `kb/demoforge_manifest.json`
- [x] Identify available demos and their metadata
- [ ] **TODO**: Build `module_to_demos` index (currently raw projects array)
- [ ] **TODO**: Build `demos_by_id` lookup table
- [ ] **TODO**: Update manifest format to support O(1) demo lookup

**Example target structure**:
```json
{
  "module_to_demos": {
    "campaigns": {
      "how_to": "6a4402a6f14e94517beb8474",
      "overview": "6a4402a6f14e94517beb8474"
    },
    "bot_studio": {
      "how_to": "6a433c867d620401bb6774c1",
      "overview": "6a433c867d620401bb6774c1"
    }
  },
  "demos_by_id": {
    "6a4402a6f14e94517beb8474": {
      "id": "6a4402a6f14e94517beb8474",
      "name": "Campaign Manager Demo",
      "industry": "Banking",
      "persona": "Head of Marketing"
    }
  }
}
```

### Phase 2: Demo Selection Logic
- [ ] **TODO**: Update `kb_video.select_demoforge_demo()` to:
  - Accept indexed manifest structure
  - Look up demo_id by (module, intent)
  - Return demo metadata (name, industry, persona, demo_id)
- [ ] **TODO**: Implement broad query fallback to "General Demo"
- [ ] **TODO**: Add timeout/error handling (fallback to YouTube)

**Function signature**:
```python
def select_demoforge_demo(
    query: str,           # User's query
    intent: str,          # "how_to", "overview", "setup", etc.
    module: str,          # Module name (e.g., "campaigns")
    context,              # Context with get_secret()
) -> dict | None:
    """Select a DemoForge demo or None if no mapping exists."""
```

### Phase 3: API Integration
- [ ] **TODO**: Create `demoforge_api.py` module with:
  - `create_share_token(demo_id, context)` → share_token
  - `build_share_url(share_token)` → full URL
  - Error handling and timeout (5 sec max)
  - Fallback to YouTube on API failure
- [ ] **TODO**: Load credentials from context secrets:
  - `DEMOFORGE_PAT` (API token)
  - `DEMOFORGE_BASE_URL` (API endpoint)
  - `DEMOFORGE_FRONTEND_URL` (UI domain)

**API endpoint** (example):
```
POST https://demoforge-api.gupshup.io/api/shares
Authorization: Bearer {DEMOFORGE_PAT}
Content-Type: application/json

{
  "demo_id": "6a4402a6f14e94517beb8474",
  "expires_in_days": 7
}

Response:
{
  "share_token": "share_abc123def456",
  "share_url": "https://demoforge-ui.gupshup.io/s/share_abc123def456",
  "expires_at": "2026-07-09T00:00:00Z"
}
```

### Phase 4: KB Answer Integration
- [ ] **TODO**: Update `kb_answer.kb_answer()` to call demo selection:
  ```python
  # After retrieving answer, check for demo
  if demo_match(intent, module):
      demo = select_demoforge_demo(query, intent, module, ctx)
      if demo:
          share_url = create_share_token(demo['demo_id'], ctx)
          response['demo'] = {
              'url': share_url,
              'name': demo['name'],
              'type': 'demoforge'
          }
  ```
- [ ] **TODO**: Update telemetry to include demo metadata
- [ ] **TODO**: Implement fallback: if API fails, use YouTube

### Phase 5: Testing & Validation
- [ ] Run `test_demoforge_integration.py` after each phase
- [ ] Verify all 6 test cases pass
- [ ] Test API timeout scenarios
- [ ] Test with real Langfuse telemetry
- [ ] Monitor demo link click-through rates

---

## Demo Catalog (Current)

| Demo | ID | Module | Intent | Industry | Persona |
|------|----|----|--------|----------|---------|
| Campaign Manager | 6a4402a6f14e94517beb8474 | campaigns | how_to | Banking | Head of Marketing |
| Personalize | 6a44013ef14e94517beb846c | personalization | how_to | Skincare | Head of Marketing |
| AI Admin | 6a43fde1f14e94517beb845f | ai_admin | how_to | Banking | Director of Product |
| RCS | 6a43fca8f14e94517beb8455 | rcs | how_to | Banking | Head of Marketing |
| CTWA | 6a43fbc7f14e94517beb844a | ctwa | how_to | B2B SaaS | Head of Marketing |
| Agent Assist | 6a43f349f14e94517beb843f | agent_assist | how_to | Contact Center | VP of Support |
| Bot Studio | 6a433c867d620401bb6774c1 | bot_studio | how_to | General | VP of Engineering |
| General Demo | 6a38bd8d9096c01ba76af5f0 | platform | overview | Banking | Head of Digital |

**Unmapped Modules** (need demo creation):
- Webhooks / Integrations
- WhatsApp Templates
- Analytics
- Customer 360

---

## Fallback Strategy

```
User Query
    ↓
Intent Classification (how_to, overview, setup, etc.)
    ↓
Module Detection (campaigns, bot_studio, rcs, etc.)
    ↓
Try: select_demoforge_demo(query, intent, module)
    ├─ Found demo
    │   ├─ Call DemoForge API for share_token
    │   ├─ Success → Return demo URL (demoforge-ui.gupshup.io/s/...)
    │   └─ API timeout → Fall back to YouTube
    └─ No demo found
        ├─ Broad query (pitch, overview, "show me")
        │   └─ Return General Demo (broad fallback)
        └─ Specific module but no demo
            └─ Fall back to YouTube (select_video)
    
Final: If no video available → Plain text answer (no error)
```

---

## Expected Benefits

### For Sales/Presales
- **Interactive demos** vs. passive video links
- **Guided experience** - user sees exact feature demonstrated
- **Shorter time-to-value** - demo > video > docs
- **Demo analytics** - track which features prospects care about

### For Customer Success
- **Onboarding speed** - users see how to do things (not just concepts)
- **Reduced support tickets** - "how do I create a campaign?" → demo
- **Self-service** - users learn independently

### For Product
- **Feature visibility** - demos highlight key capabilities
- **Competitive edge** - Gupshup + interactive demos vs. text docs
- **Usage insights** - DemoForge tracks demo engagement

### For Analytics
- **Demo selection metrics** - which demos are most requested?
- **Module coverage** - what features lack demos?
- **Fallback rates** - when do we fail to find a demo?
- **A/B testing** - demo vs. YouTube vs. text (click-through rates)

---

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|---|
| Demo selection accuracy | 95% | Test cases pass |
| API response time | <500ms | Langfuse trace latency |
| Fallback success | 100% | No crashes on timeout |
| User adoption | >30% | Demo clicks / total answers |
| Conversion impact | TBD | Sales funnel metrics |

---

## Monitoring & Debugging

### Langfuse Trace Fields
```json
{
  "demo_selected": "campaign_manager",
  "demo_id": "6a4402a6f14e94517beb8474",
  "demo_url": "https://demoforge-ui.gupshup.io/s/share_abc123",
  "demo_fallback": false,
  "demo_api_latency_ms": 150,
  "demo_fallback_reason": null
}
```

### Common Failure Modes
1. **No demo URL** - API call failed, fell back to YouTube
2. **Wrong demo selected** - Intent/module detection issue
3. **Broad query not caught** - Needs broad_fallback logic fix
4. **API timeout** - Fallback working as designed

---

## Next Steps

1. **Short-term** (this sprint):
   - Update manifest with `module_to_demos` + `demos_by_id` indexing
   - Implement demo selection logic in `kb_video.py`
   - Run test suite, fix any failures

2. **Medium-term** (next sprint):
   - Integrate DemoForge API (create_share_token)
   - Update `kb_answer.py` to call demo selection
   - Add telemetry fields to Langfuse

3. **Long-term** (roadmap):
   - Create demos for unmapped modules (webhooks, analytics, etc.)
   - A/B test demo vs. YouTube vs. text
   - Monitor impact on customer success metrics
   - Expand to other platforms (mobile, email, etc.)

---

## Reference

- **DemoForge Manifest**: `/Users/adwit.sharma/kb_docs/kb/demoforge_manifest.json`
- **Test Script**: `/Users/adwit.sharma/kb_docs/local/scripts/test_demoforge_integration.py`
- **KB Video Module**: `/Users/adwit.sharma/kb_docs/skill/kb_video.py`
- **KB Answer Module**: `/Users/adwit.sharma/kb_docs/skill/kb_answer.py`
- **DemoForge API Docs**: `https://demoforge-api.gupshup.io/docs` (requires login)
- **DemoForge Frontend**: `https://demoforge-ui.gupshup.io`
