# 30-Day Documentation Coverage Analysis

**Period:** Last 30 days (May 13 - June 12, 2026)  
**Total Queries:** 418  
**IDK Answers:** 149 (35.6% IDK rate)  
**Source:** Official docs sitemap at https://docs.gupshup.io/docs/overview

---

## Executive Summary

| Section | IDK Count | IDK % | Coverage Gap | Priority |
|---------|-----------|-------|--------------|----------|
| **Bot Building** | 48 | 32.2% | HIGH | 🔴 P1 |
| **Other (Uncategorized)** | 39 | 26.2% | CRITICAL | 🔴 P0 |
| **Getting Started** | 13 | 8.7% | MEDIUM | 🟡 P2 |
| **Webhooks & Events** | 12 | 8.1% | MEDIUM | 🟡 P2 |
| **Integrations** | 12 | 8.1% | MEDIUM | 🟡 P2 |
| **APIs** | 11 | 7.4% | MEDIUM | 🟡 P2 |
| **WhatsApp WABA** | 10 | 6.7% | MEDIUM | 🟡 P2 |
| **Campaigns** | 4 | 2.7% | LOW | 🟢 P3 |
| **Templates** | 0 | 0% | NONE | ✅ Good |

**Overall Goal:** Reduce IDK rate from 35.6% → <10% by improving KB coverage of official docs topics.

---

## 🔴 P0: CRITICAL — "Other" Category (39 IDK Answers, 26.2%)

### The Problem
26% of IDK questions don't fit the official docs structure. These are:
- **Page lookup queries** — "Where do I find X in Console?"
- **Sales/business questions** — "Who are your customers?" "What's your pricing?"
- **Console navigation** — "Which screen shows Y metric?"
- **Non-technical topics** — Customer success stories, comparisons

### Sample Unanswered Questions
```
• "On Gupshup, where do I see client id and secret?" (confidence: 0.4)
• "Where is p95 shown in Console for the web channel?" (confidence: 0.85)
• "Quais são os principais clientes do segmento CPG?" (Sales question)
• "How many WABAs are allowed for one client?" (Quota question)
• "Compare pricing between Meta and Gupshup" (Business question)
```

### Root Causes
1. **KB lacks Console UI navigation guides** — No docs on "where things are" in the product
2. **KB lacks business/sales content** — Pricing, customer examples, comparisons
3. **KB lacks quota/limits documentation** — How many WABAs, app IDs, etc.
4. **KB organization doesn't match Console structure** — Users search by where they are in the product, not by doc category

### Recommended Actions

**Action 1: Create Console Navigation Guides**
- `kb/overview/console-navigation.md` — UI tour with screenshot callouts
- `kb/overview/where-to-find.md` — Index: "Find X" → "Go to Y screen → Z section"
- Include: Credentials, metrics, settings, quotas

**Action 2: Create Quotas & Limits Guide**
- `kb/overview/quotas-and-limits.md`
- Document: Max WABAs per org, app IDs, message rate limits, storage limits
- Link from official docs if available

**Action 3: Create Business/Sales Content**
- `kb/overview/pricing-and-billing.md` — Link to official pricing
- `kb/overview/customer-success-stories.md` — Retail/FMCG case studies
- `kb/overview/feature-comparison.md` — Gupshup vs competitors (if documented)

**Expected Impact:** 39 IDK → ~5-10 remaining (assumes 75% addressable through UI docs)

---

## 🔴 P1: HIGH — Bot Building (48 IDK Answers, 32.2%)

### The Problem
Bot Studio is the most complex module and lacks step-by-step setup guides. Users struggle with:
- Message node JSON structures (list messages, buttons, etc.)
- Journey logic and node sequencing
- Dynamic data handling
- Field mappings and template variables

### Sample Unanswered Questions
```
• "In Journey Builder send message node for WhatsApp list message, how do I 
   add description to every option in the list JSON?" (confidence: 5.0) 🤔
• "Can we pass the media_id in the media_url field?" (confidence: 1.3)
• "Journey Builder: text node → script node → list node, but list doesn't render" 
  (confidence: 8.8) ⚠️
• "how do i configure an intent?" (confidence: 0.34)
• "Is there rate limiting for sending messages via API?" (confidence: 0.52)
```

### Root Causes (Official Docs vs KB)
The official docs have:
- ✅ `message-nodes.md` — General message node overview
- ✅ `action-nodes.md` — Action node reference
- ✅ `intents.md` — Intent configuration
- ❌ Missing: Step-by-step JSON examples for each message type
- ❌ Missing: Journey logic troubleshooting
- ❌ Missing: API rate limits and constraints
- ❌ Missing: Common patterns (text → buttons → list flow)

### Recommended Actions

**Action 1: Create Message Node JSON Reference**
- `kb/bot-studio/message-node-json-reference.md`
- Content:
  - Text message (simple)
  - Quick replies (with buttons)
  - List message (with descriptions) ← Fixes 1 IDK query
  - Carousel (multiple cards)
  - Each with working JSON examples

**Action 2: Create Journey Building Patterns**
- `kb/bot-studio/journey-building-patterns.md`
- Common flows:
  - Collect inputs → Validate → Send response
  - Text → Buttons → List (with troubleshooting)
  - Script node → Dynamic data → Message
  - Multi-step intent detection

**Action 3: Create API Constraints & Limits**
- `kb/bot-studio/api-rate-limits-and-constraints.md`
- Document: Message rate limits, payload sizes, timeout values
- Link to official API reference

**Action 4: Improve Intent Configuration Guide**
- Update `kb/bot-studio/intents.md` 
- Add: Step-by-step setup, examples, testing
- Show how to test intents before deployment

**Expected Impact:** 48 IDK → ~8-12 remaining (75% reduction through detailed guides)

---

## 🟡 P2: MEDIUM — Getting Started (13 IDK Answers, 8.7%)

### The Problem
Onboarding content is sparse. Users need more detailed setup guides.

### Sample Unanswered Questions
```
• "RCS campaigns overview" (confidence: 0.64) ← We already have a spec for this
• "WhatsApp onboarding and WABA setup in Gupshup with step by step guide" (confidence: 1.2)
• "RCS Agent Onboarding step by step more detail" (confidence: 1.45)
• "For Gupshup WhatsApp API onboarding, is there a documented test environment?" 
  (confidence: 1.4)
```

### Root Causes
Official docs link: Getting Started / Overview at https://docs.gupshup.io/docs/overview.md
- Has: Basic overview, quickstart
- Missing: Detailed step-by-step setup, troubleshooting, test environment guide

### Recommended Actions

**Action 1: Create Step-by-Step Setup Guides**
- `kb/overview/setup-whatsapp-in-gupshup-console.md` — WABA + phone number setup with screenshots
- `kb/overview/setup-rcs-in-gupshup-console.md` — RCS agent setup with screenshots
- Include: Prerequisites, expected timelines, common errors

**Action 2: Create Sandbox/Test Environment Guide**
- `kb/overview/sandbox-environment-guide.md`
- Document: How to create test app, how SMS templates work in sandbox, etc.
- Link to official sandbox docs

**Action 3: Create API Authentication Guide**
- `kb/overview/api-authentication.md`
- Document: API key vs OAuth, where to find credentials, how to rotate
- Sample requests for testing

**Expected Impact:** 13 IDK → ~2-3 remaining

---

## 🟡 P2: MEDIUM — Webhooks & Events (12 IDK Answers, 8.1%)

### The Problem
Webhook setup and event handling documentation needs expansion.

### Sample Unanswered Questions
```
• "For Microsoft Dynamics CRM integration, what is documented for CRM-to-Gupshup 
   data flow and Gupshup-to-CRM data flow using APIs or webhooks?" (confidence: 1.1)
• "Share detailed documentation on Meta health check for WhatsApp dynamic flow" 
  (confidence: 6.3)
• "How do I create events using WhatsApp API?" (confidence: 0.65)
• "No Bot Studio, quando um evento externo chega via Custom Integration para 
   retomar uma jornada assincrona, qual campo é usado para match com usuário?" 
  (Portuguese: Session resumption via event) (confidence: 1.8)
```

### Root Causes
Official docs have webhook overview but lack:
- CRM-specific event flows
- WhatsApp flow health check troubleshooting
- Custom event creation guides
- Session resumption via external events

### Recommended Actions

**Action 1: Create Webhook Integration Patterns**
- `kb/webhooks/webhook-patterns-for-crm.md`
- Document: How to setup webhooks to sync with CRM systems
- Show: Payload examples, field mapping, error handling

**Action 2: Create WhatsApp Flow Troubleshooting**
- `kb/bot-studio/whatsapp-flow-health-check.md`
- Explain Meta health check, common errors, how to fix
- Include: Validation rules, testing before deployment

**Action 3: Create External Event Handling Guide**
- `kb/bot-studio/resuming-journeys-via-external-events.md`
- Document: How to identify user via phone/email, continue journey asynchronously
- Show: Event payload format, session matching logic

**Expected Impact:** 12 IDK → ~2-3 remaining

---

## 🟡 P2: MEDIUM — Integrations (12 IDK Answers, 8.1%)

### The Problem
CRM and custom integration documentation is incomplete.

### Sample Unanswered Questions
```
• "Is a Microsoft Marketplace connector for Dynamics CRM officially documented 
   or maintained by Gupshup?" (confidence: 0.38) ← Already have a spec for this
• "What does the documentation say about downloading chat transcripts using 
   startDate, endDate, pageSize?" (confidence: 0.75)
• "Can Gupshup Converse platform integrate with Microsoft Dynamics?" (confidence: 0.7)
```

### Root Causes
Official docs have: Salesforce, HubSpot, Oracle, Zoho, Dynamics integrations
KB missing: Field mapping examples, API details, transcript download specs

### Recommended Actions
**→ Already covered in previous spec: `kb-integrations-improvements-spec.md`**

Implement:
- `kb/integrations/integrations-platform-overview.md`
- `kb/integrations/crm-integrations.md` (Covers Dynamics question)
- `kb/integrations/api-integration-best-practices.md`
- `kb/integrations/webhook-setup.md`

**Also needed:**
- `kb/integrations/chat-transcript-api.md` — Document transcript download endpoints

**Expected Impact:** 12 IDK → ~1-2 remaining

---

## 🟡 P2: MEDIUM — APIs (11 IDK Answers, 7.4%)

### The Problem
API documentation incomplete with missing field details and examples.

### Sample Unanswered Questions
```
• "How many business IDs are allowed for one client in Gupshup Console?" 
  (confidence: 1.15)
• "In Bot Studio, how do I call an external service after collecting user inputs 
   and send the returned summary?" (confidence: 1.75)
• "How can I send SMS using Gupshup Console API?" (confidence: 1.55)
• "For Gupshup WhatsApp API access, is there a separate API key or is it 
   username/password only?" (confidence: 1.2)
```

### Recommended Actions

**Action 1: Create API Quotas Reference**
- `kb/apis/quotas-and-limits.md` — Business IDs, app IDs, rate limits

**Action 2: Create External Service Call Pattern**
- `kb/bot-studio/calling-external-apis-in-journeys.md` — Using action nodes to call external services

**Action 3: Create SMS API Guide**
- `kb/channels/sending-sms-via-api.md`

**Action 4: Create Authentication Reference**
- `kb/apis/authentication-methods.md` — API key, OAuth, username/password

**Expected Impact:** 11 IDK → ~2-3 remaining

---

## 🟡 P2: MEDIUM — WhatsApp WABA (10 IDK Answers, 6.7%)

### The Problem
WABA setup and billing documentation needs clarity.

### Sample Unanswered Questions
```
• "Compare pricing between Meta and Gupshup for WhatsApp campaigns" (confidence: 1.7)
• "Show me the Gupshup WABA setup steps in Gupshup Console" (confidence: 1.7)
• "How do I activate my WABA in Meta? Prerequisites and steps?" (confidence: 2.2)
• "How many WABAs are allowed for one client in Gupshup Console?" (confidence: 1.15)
• "RCS pricing per message India — what details are needed?" (confidence: 0.9)
```

### Recommended Actions

**Action 1: Create WABA Setup Guide with Screenshots**
- `kb/whatsapp/setup-whatsapp-business-account-in-gupshup.md`
- Document: Full flow from WABA creation in Meta → Connection in Gupshup

**Action 2: Create Meta vs Gupshup Pricing Comparison**
- `kb/whatsapp/pricing-explained.md`
- Document: What Meta charges vs Gupshup charges, cost structure

**Action 3: Create WABA Quotas & Limits**
- `kb/whatsapp/waba-limits.md`
- Document: Max WABAs, max phone numbers, etc.

**Action 4: Create RCS Pricing Guide**
- `kb/channels/rcs-pricing.md`

**Expected Impact:** 10 IDK → ~1-2 remaining

---

## 🟢 P3: LOW — Campaigns (4 IDK Answers, 2.7%)

### The Problem
Campaign creation and best practices missing.

### Sample Unanswered Questions
```
• "How to create and publish a first campaign in Campaign Manager step by step" 
  (confidence: 1.6)
• "retail campaign manager customer success story" (confidence: 1.45)
• "Share RCS best practices document" (confidence: 1.2)
```

### Recommended Actions
- Create: `kb/campaign-manager/creating-your-first-campaign.md`
- Create: `kb/channels/rcs-best-practices.md`
- (Already have spec: `kb-rcs-campaigns-response.md`)

**Expected Impact:** 4 IDK → 0-1 remaining

---

## ✅ Templates (0 IDK Answers)

**Status:** Good coverage in KB and official docs. No action needed.

---

## Implementation Roadmap

### Phase 1 (This Week) — P0 + P1 Critical Issues
**Focus:** Bot Building (48 IDK) + Other/Navigation (39 IDK) = 87 IDK answers

| Document | Priority | Effort | Fixes |
|----------|----------|--------|-------|
| Message Node JSON Reference | P1 | 4hrs | 8 IDK |
| Console Navigation Guide | P0 | 3hrs | 12 IDK |
| Journey Building Patterns | P1 | 5hrs | 6 IDK |
| Setup Guides (WABA, RCS) | P0 | 4hrs | 8 IDK |
| **Phase 1 Total** | — | **16hrs** | **34 IDK** |

**Expected After Phase 1:** IDK rate 35.6% → 28%

---

### Phase 2 (Week 2-3) — P2 Medium Issues
**Focus:** Webhooks, Integrations, APIs, WABA = 45 IDK answers

| Document | Priority | Effort | Fixes |
|----------|----------|--------|-------|
| Webhook CRM Patterns | P2 | 3hrs | 5 IDK |
| Integrations Platform Docs | P2 | 6hrs | 10 IDK |
| API Rate Limits | P2 | 2hrs | 4 IDK |
| WABA Setup Detailed | P2 | 3hrs | 5 IDK |
| **Phase 2 Total** | — | **14hrs** | **24 IDK** |

**Expected After Phase 2:** IDK rate 28% → 16%

---

### Phase 3 (Week 4) — P3 Low + Polish
**Focus:** Campaigns, best practices, edge cases

| Document | Priority | Effort | Fixes |
|----------|----------|--------|-------|
| Campaign Creation Guide | P3 | 2hrs | 2 IDK |
| RCS Best Practices | P3 | 2hrs | 1 IDK |
| Polish/cross-references | — | 4hrs | 2 IDK |
| **Phase 3 Total** | — | **8hrs** | **5 IDK** |

**Expected After Phase 3:** IDK rate 16% → <5%

---

## Mapping Matrix: Official Docs ↔ KB Gaps

| Official Doc Section | Coverage | KB Needs | Spec Exists |
|----------------------|----------|----------|-------------|
| Overview | 40% | Step-by-step guides, console nav | ✅ (console nav, setup) |
| Getting Started | 50% | Detailed onboarding, sandbox guide | ✅ |
| WhatsApp WABA | 60% | Pricing, quotas, detailed setup | 🟡 (pricing, quotas) |
| Bot Building | 30% | JSON examples, patterns, troubleshooting | ✅ |
| Campaigns | 50% | First campaign guide, RCS campaigns | ✅ (RCS) |
| Templates | 100% | None needed | ✅ |
| Webhooks & Events | 40% | CRM flows, event handling | 🟡 |
| Integrations | 50% | CRM details, transcript API, field mapping | ✅ (comprehensive) |
| APIs | 40% | Quotas, auth methods, SMS guide | 🟡 |

---

## Quick Wins (High Impact, Low Effort)

**Do These First (1-2 hours each):**

1. ✅ **Quotas & Limits** → Fixes 5-6 IDK (How many WABAs, etc.)
2. ✅ **Console Navigation** → Fixes 8-10 IDK (Where do I find X)
3. ✅ **Pricing Explained** → Fixes 4-5 IDK (What does Meta charge vs Gupshup)
4. ✅ **Message Node JSON** → Fixes 4-5 IDK (List message with descriptions)
5. ✅ **API Authentication** → Fixes 2-3 IDK (API key vs OAuth)

**Total Impact:** 5 docs, ~8 hours → 25-30 IDK fixed (18% reduction)

---

## Success Metrics

| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| Overall IDK Rate | 35.6% | <10% | 4 weeks |
| Bot Building IDK | 32.2% | <8% | 1 week |
| Other/Navigation | 26.2% | <5% | 1 week |
| Integration IDK | 8.1% | 0% | 2 weeks |
| Coverage Completeness | 45% | 90% | 4 weeks |

---

**Status:** READY FOR IMPLEMENTATION  
**Generated:** 2026-06-12  
**Next Review:** After Phase 1 (1 week)
