# Analytics Report: 3-Day Window (2026-06-04 to 2026-06-06)

**Generated:** 2026-06-07 | **Data Source:** Langfuse API + kb/analytics | **Scope:** Internal + External users

---

## Executive Summary

### 🎯 Key Highlights

| Metric | Value | vs 30d Baseline | Status |
|--------|-------|-----------------|--------|
| **Query Volume** | 144 queries (48/day) | +405% ↑ | 🟢 High engagement |
| **Overall IDK Rate** | 29.9% | -1.7pp ↓ | 🟢 Better |
| **Video Attach Rate** | 38.2% | +19.7pp ↑ | 🟢 **Nearly 2x!** |
| **Top Module** | Bot Studio (35.4%) | Stable | — |
| **Critical Spikes** | 3 modules | AI Admin, Analytics, Channels | 🔴 Needs attention |

### 💡 Bottom Line
- **Volume is up significantly** (48 queries/day vs 10/day baseline) — indicates strong interest
- **Overall quality is stable/improving** — IDK rate down 1.7 percentage points
- **Video attach rate doubled** — recent improvements working well
- **3 modules showing quality degradation** — Channels, Analytics, AI Admin need investigation

---

## 📊 Detailed Findings

### 1. Volume Surge

**3-day total: 144 queries** across 3 days = **48 queries/day**  
30-day baseline: 10 queries/day

- This is **not anomalous** — the 30-day period includes sparse early days (May 5–18)
- June 4–6 represents normal usage patterns
- **User composition**: 57.6% from single internal user (adwit.sharma@gupshup.io); 6+ other active users

---

### 2. Module-Level Analysis

#### 🟢 **Stable/Improving Modules** (7 modules)

| Module | 3d-IDK | 30d-IDK | Delta | Notes |
|--------|--------|---------|-------|-------|
| **Bot Studio** | 21.6% | 34.9% | -13.3 | **Improving** — Better intent routing or recent doc updates |
| **Agent Assist** | 20.0% | 17.9% | +2.1 | Stable — High answer rate (80%) |
| **Goals** | 0.0% | 0.0% | — | Perfect — No documentation gaps |
| **Campaign Manager** | 11.1% | 7.7% | +3.4 | Stable — Still strong (88.9% answer rate) |
| **Integrations** | 66.7% | 75.0% | -8.3 | Improving — Better webhook/setup guidance |
| **CTX** | 60.0% | 66.7% | -6.7 | Improving — Small sample (n=5) |
| **Overview** | 38.5% | 38.1% | +0.4 | Stable — Persistent challenge (~40% unanswered) |

#### 🔴 **Degrading Modules** (3 modules)

##### **Channels: IDK +55.6pp** (0% → 100%) ⚠️ CRITICAL
- **Sample:** 4 queries, all 4 unanswered
- **Top unanswered topics:**
  - WhatsApp API onboarding requirements
  - WhatsApp event creation
  - Subscription modes (self-serve vs partner API)
  - Catalog message API
- **Problem:** Queries matched to pages like `whatsapp-business-api.md` but gates are rejecting them
- **Recommendation:** Skill agent should check concept registry boosts for `Channels` + `whatsapp-api` keywords; possibly add clarification responses for these APIs

##### **Analytics: IDK +11.9pp** (71.4% → 83.3%)
- **Sample:** 6 queries, 5 unanswered (83%)
- **Top unanswered topics:**
  - Analytics UI access / dashboard navigation
  - Multi-language queries (Portuguese: "Como acessar... analytics de WhatsApp e campanhas...")
  - Cross-module queries (e.g., "hotel chain features")
  - Campaign analytics overview
- **Root cause:** Analytics module has low KB coverage (170 chunks vs 2,340 for Bot Studio); also receives platform-wide capability questions that don't map clearly
- **Recommendation:** Skill agent should review query intent detection for Analytics module; consider if some queries should defer to other modules (Bot Studio analytics, Campaign Manager)

##### **AI Admin: IDK +13.5pp** (29.4% → 42.9%)
- **Sample:** 7 queries, 3 unanswered (43%)
- **Top unanswered topics:**
  - Developer onboarding / API references
  - Retail use-case fit
  - Feature comparison
- **Problem:** Queries are generic platform questions, matching to AI Admin "developer mode" docs but not finding clear answers
- **Recommendation:** Verify concept registry; check if queries should route to Overview/Goals instead of AI Admin

---

### 3. Video Attach Rate Surge ✨

**Now: 38.2% | Was: 18.5% | Improvement: +19.7 percentage points**

#### By Module (answered queries with video):
- **Overview:** 100% (8/8) 🏆
- **CTX:** 100% (2/2)
- **SuperAgent:** 85.7% (6/7)
- **Agent Assist:** 66.7% (16/24)
- **Campaign Manager:** 50% (4/8)
- **Bot Studio:** 32.5% (13/40)
- **AI Admin:** 25% (1/4) ← Opportunity
- **Analytics:** 100% (1/1) ← Limited answers, but videos attached when provided

**Likely cause:** Recent `video_manifest.json` updates or concept registry improvements for module-level platform queries (`overview`, `capability` pitches).

**Opportunity:** AI Admin and Bot Studio have lower video attach rates even when answering — check manifest coverage for these modules.

---

### 4. User & Environment

#### Top Users (3d)
1. **adwit.sharma@gupshup.io** — 83 queries (57.6%) — Heavy internal testing
2. **brendon.castelino@gupshup.io** — 9 queries
3. **digital2@keyaseth.in** — 8 queries (external)
4. **siddharth.barwal@gupshup.io** — 7 queries

#### Environment Split
- **PROD_EXT:** 65% — Production external deployments
- **INT:** 20% — Internal testing
- **PROD:** 15% — Production core

---

### 5. Performance

- **Latency P50:** 863ms
- **Latency P95:** 5,733ms (spike risk)
- **Average:** 2.5 seconds

Acceptable but P95 is high. Check KB storage I/O during peak queries.

---

## 🎯 Recommendations by Priority

### **Priority 1: Channels Module** (Critical)
**Action:** Skill agent should investigate gates for Channels-related queries

- Add explicit concept registry boosters for `whatsapp-api`, `subscription-modes`, `catalog-message`
- Consider adding a clarification response for API vs No-Code question
- Check if WhatsApp Business API documentation is being gated too aggressively

**Estimated Impact:** Could recover ~4 answers (100% of current IDK in Channels)

---

### **Priority 2: Analytics Module** (Investigate intent routing)
**Action:** Analytics agent should trace IDK queries to understand intent misclassification

- 5 of 6 queries are unanswered — very low confidence signal
- Many are cross-module (hotel features, retail capabilities) that end up in Analytics incorrectly
- Consider: Are these queries actually about Analytics, or do they need to route to Overview/Goals?

**Estimated Impact:** Could improve by reframing module detection for platform-capability queries

---

### **Priority 3: AI Admin Module** (Medium)
**Action:** Review concept registry and gate thresholds

- 3/7 unanswered in 3d window
- Queries are specific (developer docs, API refs, retail use cases) but matching low-quality sources
- Increasing from 29% to 43% IDK rate suggests a pattern

**Estimated Impact:** Could recover ~2 answers; validate with skill agent review

---

### **Priority 4: Video Coverage** (Leverage success)
**Action:** Continue video_manifest.json investment

- Current 38.2% attach rate is excellent (was 18.5%)
- Keep eye on Bot Studio (32.5%) and AI Admin (25%) — both have good KB but lower video coverage
- High-value topics to video: API nodes, integration patterns, admin workflows

---

### **Priority 5: Bot Studio & Integrations** (Celebrate)
**Action:** Document what's working

- Bot Studio IDK rate improved from 35% to 22% in 3 days
- Integrations improved from 75% to 67%
- Root cause: Better gate calibration? Recent KB edits? Copy any improvements to other modules

---

## 📈 Suggested Next Steps (Analytics Agent)

1. **Run regression harness** (local/scripts/idk_regression.py) to confirm 3-day trends are stable
2. **Trace failing Analytics queries** — do they belong in different modules?
3. **Generate skill agent spec** (`local/docs/`) for Channels/AI Admin/Analytics fixes
4. **Monitor next 3 days** — if Channels/Analytics spikes persist, escalate to skill agent

---

## 📌 Appendix: Sample Unanswered Queries

### Channels (all 4 unanswered)
- "For a prospect evaluating Gupshup for WhatsApp API, what documented onboarding r…"
- "How do I create events using WhatsApp API?"
- "modes of subscription for WhatsApp self-serve or partner API"
- "Catalog message API"

### Analytics (5 of 6 unanswered)
- "Como acessar no Gupshup Console os analytics de WhatsApp e campanhas para ver mé…" (Portuguese)
- "What can Gupshup do for my hotel chain? Show me all features and walkthrough vid…"
- "WHat is CX Analytics inconsole extensions"
- "For a retail/FMCG company, what Gupshup capabilities help with commerce, custome…"
- "campaign analytics overview video"

### AI Admin (3 of 7 unanswered)
- "A prospect evaluating Gupshup WhatsApp API asks: 'Could you please share the rel…"
- "What onboarding resources, developer documentation, API references, and technica…"
- "For retail/FMCG companies, what Gupshup features have helped other clients? Plea…"

---

**Report Format:** 3-day rolling window. Next update: 2026-06-09 (via cron or manual run).
