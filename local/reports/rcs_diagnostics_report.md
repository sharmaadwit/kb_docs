# RCS Performance Diagnostics & Remediation Report

**Generated:** 2026-06-10  
**Data Period:** Last 2 days (RCS deployed June 9)  
**Status:** Early-stage monitoring — recommend recheck after 50+ traces

---

## Executive Summary

**RCS Answer Rate: 33.3% (1/3 answered)** ⚠️ **CRITICAL**

RCS launched June 9 with comprehensive documentation (9 files, 187 chunks), but early traces show poor matching:
- Only 1 of 3 queries answered
- Average confidence: 1.37/10 (should be >5)
- All failures in authentication/setup queries despite having relevant docs

**Root Cause Hypothesis:** KB matching/scoring is either too strict for RCS content, or RCS queries use phrasing that doesn't match chunk headers/content well.

---

## Step 1: Regression Test Results

**Command:** `python3 local/scripts/idk_regression.py --label rcs-followup`

**Result:** ✅ **Stable** — 24/26 (92.3%) pass rate maintained

| Metric | Value | Status |
|--------|-------|--------|
| Overall Pass Rate | 92.3% | ✅ No regression |
| Answered Queries | 12 | Stable |
| IDK (deferred) | 11 | Stable |
| Video on Answered | 7 | Stable |

**Interpretation:** Case study routing, marketing docs, and other KB changes haven't degraded overall system performance. RCS-specific issues are isolated to new RCS content, not systemic.

---

## Step 2: RCS Documentation & Chunking Analysis

### Documentation Inventory

| File | Chunks | Size | Key Topics |
|------|--------|------|-----------|
| rcs-agent-setup.md | 20 | 8.3K | Agent registration, credentials, verification |
| rcs-authentication.md | 23 | 6.6K | OAuth2, token flow, credential management |
| rcs-messaging-api.md | 24 | 10K | Message types, payloads, endpoints |
| rcs-webhooks-and-callbacks.md | 27 | 7.5K | Webhook setup, event handling |
| rcs-templates.md | 31 | 13K | Template types, submission, compliance |
| rcs-api-reference.md | 19 | 11K | Endpoints, parameters, response schemas |
| rcs-quickstart.md | 15 | 5.7K | 5-step setup guide |
| rcs-faq.md | 16 | 11K | Common Q&A, troubleshooting |
| rcs-overview.md | 12 | 5.6K | Feature overview, use cases |
| **TOTAL** | **187** | **~79K** | — |

### Chunking Quality Assessment

✅ **Good:**
- Comprehensive coverage across 9 files
- Reasonable chunk count (15-31 per file)
- Mix of reference, procedural, and FAQ content

⚠️ **Potential Issues:**
1. **rcs-authentication.md** (23 chunks) covers OAuth2 flows, credentials, errors, but first 3 chunks are basic headers
   - Query "RCS Authentication & Credentials authentication flow..." should match, but scored only 1.45
   - Suggests: either chunk size is too small or TF-IDF isn't picking up multi-keyword matches
   
2. **rcs-agent-setup.md** (20 chunks) performed well (1 answered at 2.05)
   - Chunks include detailed setup steps and API parameters
   - This succeeded because chunks are dense with procedural detail

3. **rcs-overview.md** (12 chunks) minimal chunks for 5.6K content
   - May be combining multiple sections per chunk, losing granularity

### Scoring Pattern

**Successful query:** "RCS Agent Setup & Onboarding" → rcs-agent-setup.md (confidence 2.05)
- This file has detailed procedure sections with clear headings
- Chunks likely contain full context (definition → steps → examples)

**Failed queries:** 
- "RCS Authentication & Credentials" → rcs-authentication.md (confidence 1.45)
- "How to enable RCS" → no good match (confidence 0.60)

**Hypothesis:** Chunks are indexed but query keywords ("credentials", "authentication", "enable") aren't matching well with chunk headers. May need concept registry boosting for RCS keywords.

---

## Step 3: Video Manifest Status

**Current Status:** 🔴 **RCS videos disabled**

**Reason:** Commit `4fd4f9d` (June 9, 13:33):
> "Exclude RCS from video until RCS-specific videos available"

**Video Attachment Rate (RCS traces):** 0/1 answered (0%)
- Expected once videos are enabled

**Action:** Once RCS-specific walkthrough videos are available:
1. Create or locate RCS video IDs (setup, auth, messaging, templates)
2. Add entries to `kb/video_manifest.json` under `channels: rcs-*` sources
3. Set `video_disabled: false` in manifest
4. Re-ingest with `kb_ingest`

**Estimated Impact:** Video attachment should raise confidence on answered queries, improving perceived quality.

---

## Step 4: Detailed Query Analysis

### Query 1: "RCS Agent Setup & Onboarding steps to register an RCS agent"

✅ **ANSWERED** (confidence: 2.05)

- **Matched source:** kb/channels/rcs-agent-setup.md
- **Mode:** setup
- **Answer preview:** "Register your brand as an RCS agent on Gupshup's Dotgo RBM Hub..."
- **Analysis:** Good match. File has "Definition" section explaining agent setup clearly.

---

### Query 2: "RCS Authentication & Credentials authentication flow register RCS agent client id client secret bot"

❌ **UNANSWERED** (confidence: 1.45)

- **Attempted match:** kb/channels/rcs-authentication.md (likely)
- **Expected answer:** OAuth2 Client Credentials flow, token obtainment, credential management
- **Problem:** Low confidence despite exact keyword match
- **Root cause:** Likely TF-IDF issue:
  - Query is long with multiple keywords: "authentication", "credentials", "flow", "client_id", "secret", "bot"
  - Chunks may have low frequency of all these terms together
  - Header "RCS Authentication & Credentials" should match, but scoring is weak

**Recommendation:** 
- Check if KB gate threshold is too strict for multi-keyword queries
- Consider adding concept registry entry for `{"module": "Channels", "concept": "rcs_auth", "boost": 1.5}`
- Or: verify that authentication.md chunks are properly indexed and searchable

---

### Query 3: "How to enable RCS on a project"

❌ **UNANSWERED** (confidence: 0.60)

- **Should match:** rcs-quickstart.md or rcs-agent-setup.md
- **Problem:** Very low confidence (0.60) indicates no good chunk match
- **Root cause:** Query is short and generic ("enable RCS on a project")
  - No module context ("Channels")
  - Could match: activation, onboarding, setup, deployment
  - Chunks may use different terminology (e.g., "register", "configure", "create agent")

**Recommendation:**
- Add an FAQ entry: "How do I enable/activate RCS?" → link to quickstart
- Check rcs-quickstart.md for a section titled "Enable RCS" or "Activate RCS"
- Or: update rcs-overview.md to explicitly state "To enable RCS, follow the Agent Setup process in rcs-agent-setup.md"

---

## Recommendations (Prioritized)

### Priority 1: Investigate Concept Registry & Scoring

**Why:** 33% answer rate on RCS is critical. Regression is stable, so issue is specific to RCS chunking/scoring.

**Action:**
```bash
# Manually test scoring on RCS queries
python3 local/scripts/idk_regression.py --debug-query "RCS Authentication & Credentials"
```

Check:
1. Are rcs-authentication.md chunks being retrieved?
2. What are their TF-IDF scores before gating?
3. Are gates rejecting valid matches?

**Owner:** Skill agent (requires code inspection)  
**Timeline:** 1-2 hours

---

### Priority 2: Add RCS-Specific Concept Registry Entries

**Why:** RCS is a new, distinct channel with unique terminology. Concept registry can help queries find the right docs.

**Action:** Update `skill/kb_answer.py` concept registry:
```python
{
    "module": "Channels",
    "intent": ["setup", "definition"],
    "concepts": [
        "rcs", "rich communication services", "dotgo", "rbm", "agent",
        "authentication", "oauth", "client credentials", "token",
        "messaging", "templates", "webhooks"
    ],
    "boost": 1.3
}
```

**Owner:** Skill agent (code edit)  
**Timeline:** 1 hour

---

### Priority 3: Enhance FAQ Coverage

**Why:** Query 3 ("How to enable RCS") shows that users expect procedural answers to simple questions.

**Action:** Add FAQ section to rcs-overview.md or rcs-quickstart.md:
```markdown
## Frequently Asked Questions

### How do I enable RCS on my project?
1. Go to Gupshup Console → Channels → RCS
2. Click "Add RCS Agent"
3. Follow the Agent Setup process (see rcs-agent-setup.md)
...
```

**Owner:** Product/marketing  
**Timeline:** 30 minutes

---

### Priority 4: Prepare for Video Integration

**Why:** Videos will improve perceived quality and engagement on answered queries.

**Action:**
1. Identify or create RCS videos:
   - RCS Agent Setup (how to register)
   - Authentication & token flow (how to get credentials)
   - Sending a message (end-to-end demo)
   - Template submission (compliance)

2. Once available, update video_manifest.json:
   ```json
   {
       "source": "kb/channels/rcs-agent-setup.md",
       "video_id": "YOUR_VIDEO_ID",
       "title": "RCS Agent Setup & Onboarding",
       ...
   }
   ```

3. Re-run `kb_ingest` to rebuild chunks with video metadata.

**Owner:** Marketing/video team  
**Timeline:** Pending video creation (1-2 weeks)

---

## Monitoring Plan

### Daily (first week after RCS launch)

```bash
# Refresh RCS analytics
set -a && source .env && set +a
python3 local/scripts/rcs_analytics.py
open local/reports/rcs_dashboard.html
```

**Alert threshold:** If answer rate drops below 25%, escalate to skill agent.

### Weekly (month 1)

```bash
# Run full regression test
python3 local/scripts/idk_regression.py --label rcs-weekly
```

Track:
- Overall IDK rate (should stay ≥22/26)
- RCS-specific queries (expect 5-10 per day after ramping)
- Video attach rate (expect 0% until videos enabled)

### Monthly (ongoing)

Analyze:
- RCS query volume trend
- Confidence distribution (should shift from 1.37 avg toward >5)
- User feedback on RCS docs (from console/support)
- Video attach rate (once enabled)

---

## Appendix: RCS Chunk Sample

### rcs-authentication.md :: Chunk 5

```
Heading: "Step 2: Obtain Access Token"
Text: "Use your Client ID and Client Secret to request an access token:

Endpoint: POST https://auth.dotgo.com/auth/oauth/token

Request Format:
POST https://auth.dotgo.com/auth/oauth/token?grant_type=client_credentials HTTP/1.1
Host: auth.dotgo.com
Content-Type: application/x-www-form-urlencoded
Authorization: Basic <base64(clientId:clientSecret)>

grant_type=client_credentials

Authorization Header:
- Encode clientId:clientSecret as base64
- Prefix with 'Basic '
- Example: Authorization: Basic aWFtY2xpZW50OnlvdW93ZXpzYW1lbHk="
```

**Observation:** Rich, procedural content. Should score well but isn't. Likely query phrasing mismatch.

---

## Summary for Next Session

| Item | Status | Owner | ETA |
|------|--------|-------|-----|
| Regression test | ✅ Stable (92.3%) | Automated | Continuous |
| Chunk analysis | ✅ Complete (187 chunks, good coverage) | Analytics | Done |
| Concept registry | ⏳ Pending investigation | Skill agent | 1-2h |
| Video prep | ⏳ Pending video creation | Marketing | 1-2w |
| Monitoring dashboard | ✅ Live (rcs_analytics.py) | Analytics | Continuous |

**Next action:** Skill agent to investigate concept registry and scoring on rcs-authentication queries.

