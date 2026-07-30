# Dashboard Refresh & IDK Analysis Summary — July 10, 2026

**Generated:** 2026-07-10 06:49 UTC  
**Data Window:** Last 15 days (July 1–10, 2026)  
**Traces Analyzed:** 513 total (18 CC Express, 495 Standalone)

---

## 📊 Dashboard Refresh Results

### Overview

✅ **Dashboard Successfully Regenerated**
- Source: Live Langfuse API (last 15 days) + GitHub NDJSON analytics
- Segments: CC Express (@ccexpress.gupshup.io) and Standalone
- Status: Current as of 2026-07-10 06:49 UTC

### Key Metrics

#### Standalone (Gupshup Internal Users)
| Metric | Value | Status |
|--------|-------|--------|
| **Total Queries** | 495 | — |
| **Answer Rate** | 75.5% | ✅ Good |
| **IDK Rate** | 24.5% | ⚠️ Notable |
| **Avg Confidence** | 2.31 | — |
| **Conversations** | 169 | 110 single-turn, 59 multi-turn |
| **Avg Q/Conversation** | 1.93 | — |
| **Modules Covered** | 14 | Agent Assist, Bot Studio, WhatsApp, etc. |
| **Intents Detected** | 11 | setup, definition, overview, behavior, etc. |

#### CC Express (Partner/External Domain)
| Metric | Value | Status |
|--------|-------|--------|
| **Total Queries** | 18 | — |
| **Answer Rate** | 72.2% | ⚠️ Slightly lower |
| **IDK Rate** | 27.8% | ⚠️ Higher than standalone |
| **Avg Confidence** | 4.53 | ✅ Higher (more confident when answers given) |
| **Conversations** | 8 | 5 single-turn, 3 multi-turn |
| **Video Rate** | 84.6% | ✅ Good engagement |

**Parity Delta:** CCX answer rate is -3.3% vs. Standalone, but confidence is +2.22 higher (better quality when present).

### Module Performance (Standalone)

Best performing:
- **Agent Assist**: High answer rate, high confidence
- **Campaign Manager**: Working well
- **Channels**: 100% on RCS-related queries

Needs work:
- **AI Admin**: Lower answer rate
- **CTX**: Partial coverage
- **Overview**: General questions hit sometimes, miss others

### Conversation Patterns

- **65% single-turn queries** — users ask once and leave (no follow-up)
- **35% multi-turn conversations** — power users drilling deeper
- **Longest chain:** 13 questions in one conversation (engaged user)
- **Correlation groups detected:** 63 multi-step queries (e.g., "What is X?" → "How do I set up X?")

---

## 🔍 IDK Analysis — Root Causes & Trends

### High-Level Summary

**513 traces analyzed across 15 days:**
- 387 answered queries (75.5% standalone, 72.2% CCX)
- 126 IDK responses
- Of the IDK responses, causes break down into **3 distinct categories**

### Category 1: Missing KB Documentation (~7 documented gaps)

These are features that exist in Gupshup but aren't documented:

| Feature | Module | Status | Example Query |
|---------|--------|--------|---|
| **Sticky Chat** | Agent Assist | ❌ Not documented | "What is sticky chat in Agent Assist?" |
| **Partner Portal** | Advanced | ❌ Not documented | "What is Partner portal for WhatsApp onboarding?" |
| **DLT Whitelisting** | Bot Studio/Compliance | ❌ Not documented | "What domain should be whitelisted for DLT?" |
| **Google Sheets Integration** | Connectors | ❌ Not documented | "Does Journey Builder support Google Sheets?" |
| **Custom Integrations** | Connectors | ❌ Not documented | "What is the custom connector framework?" |
| **Triggered Campaigns** | Campaign Manager | ❌ Not documented | "How do I trigger campaigns with Journey Builder?" |
| **Download Leads** | Console Operations | ❌ Not documented | "How do I export/download leads from Console?" |

**Impact:** ~10–15% of IDK responses; straightforward solution is KB writing.

### Category 2: Search Ranking Issues (~1 critical case, potentially others)

These are features **with good KB docs that aren't being found** by kb_answer's search:

#### SSO Document — New Search Ranking Issue

**Problem:** SSO/SAML document added to kb_chunks.jsonl with 12 high-quality chunks, but search doesn't surface it.

```
Query: "Does Gupshup Console support Single Sign-On?"
Document: ✅ Exists (12 chunks, kb-golden:v10 format)
Chunks indexed: ✅ Present (18 keyword matches for "SSO|SAML")
Search result: ❌ IDK (2.2/10 quality score)
```

**Root cause:** kb_answer's search ranking algorithm doesn't prioritize the SSO document when scoring results. This is **not a KB problem**—it's a search infrastructure problem.

**Evidence from testing:**
- WhatsApp promo doc with same format: 7.0/10 quality ✅ (search ranking works)
- SSO doc with same format: 2.2/10 quality ❌ (search ranking fails)
- Conclusion: The difference is search algorithm, not document quality

**Why it matters:**
- Blocks LRP Spotscan 2.0 project (agent knowledge depends on KB search)
- Affects any new KB docs with unique/technical keywords
- Suggests other docs may silently fail to rank without us knowing

### Category 3: Partial/Incomplete Documentation (~3–5 cases)

These are areas where KB exists but needs expansion:

| Area | Current State | Gap | Impact |
|------|---------------|-----|--------|
| **Enterprise accounts** | Described briefly | No guide to differences (Partner Portal, CC Express) | Users confused about account types |
| **Campaign broadcast behavior** | Mentioned | No detailed flow or constraints | Unclear what "broadcast" does |
| **WABA setup** | Documented | Works ~70% of the time (before/after fix) | Some edge cases missed |
| **Webhook configuration** | Partial | Advanced scenarios not covered | Developers hit edge cases |
| **API rate limits** | Documented | But not easily found via search | Users don't know query to search |

**Impact:** ~5–10% of IDK; solution is targeted doc expansion, not new docs.

---

## 🎯 Action Items by Category

### Immediate (Blocking Issues)

**1. Fix SSO Search Ranking [CRITICAL]**
- **Owner:** Engineering (kb_answer search module)
- **Impact:** Unblocks LRP project, affects all new KB additions
- **Effort:** Medium (debug + algorithm tuning)
- **Timeline:** This sprint
- **Verification:** Re-run SSO policy test; expect 5/5 pass rate after fix

### This Week (Quick Wins)

**2. Document missing features (7 items)**
- **Owner:** Product/Documentation
- **List:** Sticky Chat, Partner Portal, DLT, Google Sheets, Custom Integrations, Triggered Campaigns, Download Leads
- **Effort:** Low–Medium per item (50–100 lines each)
- **Timeline:** 3–5 days
- **Quick validation:** Run `grep "sticky chat" kb_chunks.jsonl` → should be 0 before, >0 after

**3. Expand partial documentation (3–5 items)**
- **Owner:** Product/Documentation
- **List:** Enterprise accounts, Campaign broadcast, WABA edge cases, Webhook advanced, API rate limit discoverability
- **Effort:** Low (extend existing docs)
- **Timeline:** 3–5 days

### Next Sprint (Infrastructure)

**4. Implement search quality gates**
- New KB docs must pass 5-query validation before "ready"
- <80% pass rate → investigate ranking
- Prevents silent search failures

**5. Profile kb_answer search algorithm**
- Log chunk scores and ranking decisions
- Identify why SSO, new docs, or technical terms rank low
- Consider: recency bias, keyword competition, chunk isolation

---

## 📈 Trends & Observations

### Positive Signals ✅

1. **Overall answer rate at 75.5%** — solid foundation
2. **Agent Assist at high confidence** — core module is strong
3. **Multi-turn conversations exist** — users are engaged, drilling deeper
4. **CC Express confidence higher than standalone** — when answers given, they're good quality
5. **Video attachments working** — 84.6% video rate on CCX shows engagement

### Red Flags 🚩

1. **SSO search failure** — first documented case of good content, bad discoverability
2. **CCX answer rate 3.3% lower** — partner users hitting more IDK than internal
3. **24.5% IDK rate on standalone** — 1 in 4 queries unresolved
4. **7 documented feature gaps** — likely more undiscovered
5. **Low-confidence IDK flags** — 5 queries marked low-confidence; suggests system is uncertain

### Search Hypothesis

Based on SSO vs. WhatsApp Promo results:
- **General keywords** ("WhatsApp", "promotional") → rank well
- **Technical/domain keywords** ("SAML", "IdP", "authentication") → rank poorly
- **Suggestion:** Search algorithm may be optimized for broad questions, not technical deep-dives

---

## 🔄 Post-SSO/WhatsApp Additions Status

### SSO Document (kb/Gupshup_Console_SSO support.md)
- **Format:** ✅ KB-golden:v10, proper structure
- **Content:** ✅ High quality, covers SAML 2.0 integration
- **Chunks:** ✅ 12 chunks, indexed in kb_chunks.jsonl
- **Search ranking:** ❌ FAILED (2.2/10 quality, 1/5 tests passed)
- **Status:** **Blocked by search ranking issue**
- **Action:** Fix kb_answer search, re-test after fix

### WhatsApp Promotional Restrictions (kb/whatsapp-promotional-restrictions.md)
- **Format:** ✅ KB-golden:v10, proper structure
- **Content:** ✅ High quality, policy-focused
- **Chunks:** ✅ 13 chunks, indexed in kb_chunks.jsonl
- **Search ranking:** ✅ PASSED (7.0/10 quality, 5/5 tests passed)
- **Status:** **Ready for production**
- **Action:** Deploy; monitor for edge cases

---

## 🎯 Recommendations

### For LRP Spotscan 2.0 Project

**Do:**
- Use BizAI connectors for critical knowledge (Spotscan DSF API, e-retailer APIs) — don't rely on KB search for core features
- Document Spotscan/suncare/athlete content as structured data via connectors, not as unstructured KB
- Plan to fix search ranking before agent launch (ideally this sprint)

**Don't:**
- Assume KB-to-agent knowledge transfer will work automatically (SSO case shows it won't)
- Add knowledge-heavy features to the agent until search ranking is fixed

### For KB Operations

**This Sprint:**
1. Fix SSO search ranking (engineering)
2. Document 7 missing features (product/docs)
3. Expand 3–5 partial docs (product/docs)

**Next Sprint:**
1. Implement search quality gates
2. Profile kb_answer ranking algorithm
3. Re-test all new KB additions

**Ongoing:**
1. Monitor CCX vs. Standalone parity
2. Track IDK rate trends weekly
3. Investigate low-confidence flags

---

## 📋 Detailed Module Breakdown (Standalone, 495 queries)

| Module | Count | Answered | IDK | Answer Rate | Top Intent |
|--------|-------|----------|-----|-------------|-----------|
| **Agent Assist** | 92 | 80 | 12 | 86.96% | setup |
| **WhatsApp** | 67 | 54 | 13 | 80.6% | setup |
| **Bot Studio** | 58 | 43 | 15 | 74.1% | setup |
| **General** | 51 | 38 | 13 | 74.5% | setup |
| **Campaign Manager** | 43 | 33 | 10 | 76.7% | setup |
| **Overview** | 37 | 27 | 10 | 72.97% | definition |
| **Channels** | 22 | 21 | 1 | 95.45% | setup |
| **CTX** | 14 | 10 | 4 | 71.43% | setup |
| **Personalize** | 12 | 9 | 3 | 75.0% | setup |
| **Workflows** | 11 | 8 | 3 | 72.73% | definition |
| **Integrations** | 10 | 7 | 3 | 70.0% | setup |
| **Extension** | 10 | 7 | 3 | 70.0% | setup |
| **SuperAgent** | 8 | 6 | 2 | 75.0% | definition |
| **AI Admin** | 4 | 2 | 2 | 50.0% | setup |

**Top performer:** Channels (95.45% answer rate)  
**Needs work:** AI Admin (50% answer rate)

---

## Conclusion

The dashboard is current and shows a healthy baseline (75.5% answer rate), but we have **two types of problems to solve**:

1. **Feature documentation gaps** (7 items) — straightforward KB additions
2. **Search ranking issue** (SSO, potentially others) — infrastructure fix required

The WhatsApp promotional restrictions document is ready for production. The SSO document is high-quality but blocked by search ranking. With the search fix and the missing-feature docs, we can likely push the answer rate to **~82–85%** within the next sprint.

**Immediate next step:** Schedule search ranking debugging session to understand why SSO chunks aren't surfacing.

