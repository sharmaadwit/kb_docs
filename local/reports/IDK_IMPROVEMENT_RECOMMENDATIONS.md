# IDK Answer Analysis & Improvement Recommendations

**Period:** Last 3 days (June 9-12, 2026)  
**Total Queries:** 27  
**IDK Answers:** 13 (48.1%)  
**Average Confidence:** 2.78/10

---

## 🔴 Critical Issues (>70% IDK Rate)

### 1. Agent Assist Module — 83.3% IDK Rate (5 of 6 queries)

**Problem:** Users asking about Agent Assist are getting "I don't know" responses 5 out of 6 times.

**Sample Unanswered Questions:**
- "For Microsoft Dynamics CRM integration with Gupshup, what is documented for CRM-to-Gupshup data flow and Gupshup-to-CRM data flow using APIs or webhooks?"
- "Is there rate limiting for sending messages via API? What are the limits and how..."
- "Microsoft Dynamics CRM integration..." (appearing multiple times)

**Root Cause:** 
- KB lacks documentation on API rate limiting
- CRM integration flows are not documented
- Agent Assist API documentation is incomplete or in wrong module

**Recommended Actions:**
1. **Create:** `kb/agent-assist/api-rate-limits.md` with specific rate limits per endpoint
2. **Create:** `kb/integrations/crm-integrations.md` covering Dynamics/Salesforce/HubSpot flows
3. **Review:** `kb/agent-assist/agent-assist-api-documentation.md` — currently returning this but still IDK
4. **Priority:** HIGH — Agent Assist is a core product area

---

### 2. CTX Module — 100% IDK Rate (1 of 1 query)

**Problem:** Single CTX query received IDK response.

**Unanswered Question:**
- "Quais são os principais clientes do segmento CPG da Gupshup e quais regiões de atuação? Sei que em Latam temos Diageo"  
  (Translation: "What are the main CPG segment customers and regions of operation? I know Diageo is in LATAM")

**Root Cause:** 
- Question is asking for business/sales information (customer references)
- KB is technical documentation, not sales enablement

**Recommended Actions:**
1. **Not KB-fixable** — This is a sales/presales question, not technical
2. Route to Presales team instead
3. Consider if CTX module needs basic positioning docs

---

### 3. Integrations Module — 66.7% IDK Rate (2 of 3 queries)

**Problem:** Integration questions frequently get IDK responses.

**Unanswered Questions:**
- "Is a Microsoft Marketplace connector for Dynamics CRM officially documented or maintained by Gupshup..."
- "Can we pass the media_id (generated via UploadMedia API) in the media_url field of the MEDIA_MESSAGE_BULK_UPLOAD API?"

**Root Cause:**
- CRM integration documentation is missing
- API field-level details not documented
- Sources returned are wrong modules (WhatsApp voice instead of integrations)

**Recommended Actions:**
1. **Create:** `kb/integrations/crm-dynamics-integration.md` with supported flows
2. **Update:** API documentation with field-level details for media_id behavior
3. **Cross-ref:** Link WhatsApp API docs to integration guides

---

## 🟡 Moderate Issues (40-70% IDK Rate)

### 4. Channels Module — 40% IDK Rate (2 of 5 queries)

**Problem:** Some channel-specific questions not answered.

**Unanswered Questions:**
- "On Gupshup, where do I see client id and secret" (page_lookup intent)
- "Where is p95 shown in Console for the web channel? Which screen or metric shows..." (page_lookup intent)

**Root Cause:**
- Page navigation/UI location questions not well covered
- Channel credentials setup missing from quickstarts
- Performance metrics documentation incomplete

**Recommended Actions:**
1. **Update:** `kb/channels/rcs-quickstart.md` — add "Finding your credentials" section with screenshots
2. **Create:** `kb/channels/channel-analytics-metrics.md` — document where P50/P95/metrics appear
3. **Add:** Step-by-step UI navigation guide with console navigation paths

---

## 🟢 Lower Priority Issues (<40% IDK Rate)

### 5. AI Admin — 100% IDK (1 of 1 query)
- Only 1 query in window; need more data

### 6. Overview — 50% IDK (1 of 2 queries)
- "RCS campaigns overview" — needs RCS campaign guide

### 7. Bot Studio — 20% IDK (1 of 5 queries)
- Good performance overall; 1 edge case about WhatsApp list message JSON structure

---

## 📊 Intent-Based Analysis

### Setup Intent (Most Common IDK) — 8 IDK Answers
Users trying to configure features are most likely to get IDK responses.

**Affected Areas:**
- API rate limiting setup
- CRM integration setup
- Channel credential setup
- Media field behavior

**Action:** Prioritize step-by-step setup guides for these modules

### Page Lookup Intent — 3 IDK Answers
Users looking for where things are in the Console get IDK responses.

**Affected Questions:**
- Where to find credentials
- Where to see metrics
- Which screen shows X

**Action:** Create "where in console" navigation guides with screenshots

### Definition Intent — 2 IDK Answers
Technical definitions/explanations missing.

**Action:** Add glossary-style docs for common terms and concepts

---

## 🎯 Implementation Roadmap

### Phase 1: Critical (Do This Week)
- [ ] Create CRM integration guide (`kb/integrations/crm-dynamics-integration.md`)
- [ ] Document API rate limits (`kb/agent-assist/api-rate-limits.md`)
- [ ] Add credentials location guide (`kb/channels/channel-setup-credentials.md`)

### Phase 2: High Impact (Next Week)
- [ ] Update all quickstarts with credential setup sections
- [ ] Create channel analytics metrics guide
- [ ] Document WhatsApp list message JSON structure thoroughly

### Phase 3: Coverage (Next 2 Weeks)
- [ ] Add "where in console" navigation guides
- [ ] Create RCS campaigns overview
- [ ] Document performance metrics locations

---

## 📈 Expected Impact

| Action | Current IDK Rate | Expected After | Module |
|--------|-----------------|-----------------|--------|
| Add CRM integration docs | 83.3% | 50% | Agent Assist + Integrations |
| Add API rate limits | 83.3% | 60% | Agent Assist |
| Add channel credentials | 40% | 20% | Channels |
| Add console navigation | 40% | 15% | Channels |

**Expected Overall IDK Reduction:** 48.1% → 25-30%

---

## 💡 Root Cause Summary

1. **Missing Documentation** (60% of issues)
   - CRM integrations
   - API rate limits
   - Channel setup details

2. **Wrong Module Returned** (20% of issues)
   - Agent Assist questions returning Integrations docs
   - CTX questions returning unrelated docs

3. **Incomplete Coverage** (20% of issues)
   - Setup guides lack step-by-step details
   - Navigation/UI guidance missing
   - Edge cases not covered

---

## 🔗 Related Files

- **Trace data:** `local/reports/3day_idk_analysis.json`
- **Full dashboard:** `local/reports/3day_dashboard.html`
- **Previous fix:** `local/docs/BUG_FIX_NDJSON_TS_FIELD.md`

---

**Status:** READY FOR IMPLEMENTATION  
**Generated:** 2026-06-12  
**Next Review:** After Phase 1 implementation
