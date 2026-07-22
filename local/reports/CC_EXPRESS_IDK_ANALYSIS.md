# CC Express IDK Analysis — Root Causes & Patterns

**Date:** 2026-07-11  
**Focus:** 26 IDK responses out of 65 total CC Express queries (40% IDK rate)  
**Comparison:** Standalone rate 22.2% (17.8% gap favoring standalone)

---

## Executive Summary

CC Express has a **40% IDK rate vs. 22.2% standalone** — a 17.8-point gap. Root causes break into three categories:

1. **Module Knowledge Gaps** (11 IDKs): WhatsApp (5), Bot Studio (4), Channels (1) — topics poorly covered in KB
2. **Content Coverage Issues** (9 IDKs): Tiered pricing, WABA migration, partner setups, sandboxing — specific use cases missing from docs
3. **Anonymous User Bias** (6 IDKs): Repeat user `visitor-8cbe2c97` with 26 total queries has only 23.1% answer rate vs. others at 100%

---

## Part 1: Module-Level Analysis

### High-Failure Modules

| Module | CC Express | Standalone | Gap | Pattern |
|--------|-----------|-----------|-----|---------|
| **WhatsApp** | 0/5 (0%) | 1/14 (7%) | -7% | Completely broken for CCX |
| **Bot Studio** | 3/7 (43%) | 70/75 (93%) | -50% | Major gap, KB works for standalone |
| **Channels** | 9/16 (56%) | 18/30 (60%) | -4% | Slightly worse for CCX |
| **CTX** | 1/4 (25%) | 6/12 (50%) | -25% | Multi-tenant topics hard |
| **General** | 8/12 (67%) | 29/33 (88%) | -21% | Broad topics underperform for CCX |

### Working Modules (No Gap)

- **Campaign Manager:** 6/6 (100% CCX) vs 20/26 (77% standalone) — **CCX performs better**
- **Agent Assist:** 8/8 (100% CCX) vs 41/47 (87% standalone) — **CCX performs better**
- **Integrations:** 1/1 (100% CCX) vs 7/9 (78% standalone) — **CCX performs better**

**Insight:** Structured, feature-specific topics work well. Broad or technical topics (WhatsApp API, Bot Studio, tier info) fail for CCX.

---

## Part 2: Specific IDK Queries (The Smoking Gun)

### WhatsApp Block (5 IDKs, all score 0.0 or very low)

1. **"exact step-by-step documented procedure to configure a WhatsApp Business API sender"** (score 0.0)
   - Issue: Precise API setup docs don't exist in KB for CC Express
   - Gap: No dedicated WhatsApp API integration guide

2. **"How do I onboard an existing WABA account to Gupshup? Migration from another BSP"** (score 0.0)
   - Issue: Migration/existing-account scenarios not documented
   - Gap: KB assumes new WABA creation, not imports

3. **"WhatsApp testing sandbox inbound message reply webhook setup"** (score 0.8, Chinese query)
   - Issue: Sandbox-specific configuration missing
   - Gap: Webhook config guide incomplete for test env

4. **"Documentation for WhatsApp API integration with Gupshup for a SaaS ISV using API only"** (score 1.1)
   - Issue: ISV-specific (no-console) flow not documented
   - Gap: KB assumes console UI path

5. **"Can Gupshup support a WhatsApp chatbot for product info, product hierarchy, custom pricing"** (score 1.1)
   - Issue: Use-case-specific capability question (chatbot, catalog)
   - Gap: No "use-case cookbook" for WhatsApp advanced features

### Pricing & Tier Queries (2 IDKs)

6. **"How do I check my CC Express tier (Starter or Pro)?"** (score 1.0)
   - Issue: Tier info is product metadata, not KB content
   - Gap: No tier-detection guide (should be in "Account Settings" section)

7. **"What is the rate limit for the Gupshup message sending API?"** (score 0.0)
   - Issue: Rate limit is API/platform spec, not KB doc
   - Gap: KB should surface API rate limits in "Integration" or "API Reference"

### Partner & Enterprise Setup (2 IDKs)

8. **"How to create a Gupshup partner account?"** (score 1.1, but marked IDK)
   - Issue: Partner onboarding is external/sales process
   - Gap: KB doesn't cover partner flow

9. **"Partner setup flow for a Tech Provider who wants to use Gupshup APIs"** (score 0.9)
   - Issue: Multi-tenant partner setup not covered
   - Gap: No Tech Provider onboarding guide

### Bot Studio & Channel Setup (5 IDKs)

10. **"How do I check which CC Express tier I have: Starter or Pro?"** (score 0.9, Bot Studio module)
    - Issue: Same as #6, wrong module classification
    - Gap: Tier info missing

11–13. **3 additional Bot Studio IDKs** (scores 1.8–1.9)
    - Pattern: Complex multi-step workflows or advanced features
    - Gap: Bot Studio KB covers basics, not advanced patterns

---

## Part 3: User-Level Analysis — The `visitor-8cbe2c97` Problem

### This One User Drives 40% of CC Express IDKs

| User | Queries | Answered | Rate | Avg Conf | Problem |
|------|---------|----------|------|----------|---------|
| `visitor-8cbe2c97` | **26** | **6** | **23.1%** | 1.36 | Low-quality conversations, poor queries |
| `Anonymous` | 57 | 25 | 43.9% | 1.49 | Generic, but better |
| `visitor-938eafdf` | 7 | 7 | 100% | 7.22 | Expert user, structured queries |
| `visitor-5ceb5a5a` | 1 | 1 | 100% | 1.25 | One query, answered |

### What's Wrong with `visitor-8cbe2c97`?

Looking at their 26 queries:
- **Pattern 1: Over-scoped questions** — "exact step-by-step procedure for WhatsApp API sender" (too technical)
- **Pattern 2: Use-case questions** — "Can Gupshup support a chatbot for X, Y, Z?" (needs sales/product, not docs)
- **Pattern 3: Multi-tenant edge cases** — "SaaS ISV using API only" (niche, specific constraints)
- **Pattern 4: Repeated failures** — Same user retrying WhatsApp/WABA questions after getting IDK

**Root Cause:** This is a power user or integrator asking implementation-level questions that require product expertise or sales, not KB. The KB isn't designed to answer "Can Gupshup do X?" — it answers "How do I configure X in Gupshup?"

---

## Part 4: Intent-Level Breakdown

### By Intent (CC Express)

| Intent | Queries | Answered | Rate | Issue |
|--------|---------|----------|------|-------|
| **setup** | 49 | 28 | 57.1% | Most IDKs are here (21/49). "Setup" is too broad; specific setups fail. |
| **definition** | 14 | 9 | 64.3% | Feature def. questions work OK |
| **overview** | 4 | 3 | 75% | Works well |
| **behavior** | 1 | 1 | 100% | Works |

**Insight:** "Setup" intent has 21 of 26 total IDKs. These are specific, step-by-step configurations that aren't in the KB.

---

## Part 5: Why Standalone Does Better (77.8% vs 60% for CCX)

**Standalone users ask:**
- Known modules with comprehensive coverage (Bot Studio, Agent Assist, Campaign Manager)
- Standard workflows (how do I create X, configure Y)
- Troubleshooting questions (why did my setup fail?)

**CC Express users ask:**
- Feasibility questions ("Can Gupshup do this?")
- Edge-case technical setups (ISV API, multi-tenant, WABA migration)
- Pricing/tier information (not in KB)
- Sales-level questions (partner setup, custom solutions)

---

## Recommendations

### 1. Fix the High-Failure Modules (Quick Wins)

**WhatsApp (0% → target 60%+):**
- Add "WhatsApp Business API Setup" guide (API-only path, no console)
- Add "WABA Migration & Import" guide (existing account scenarios)
- Add "Webhook Configuration for Testing" (sandbox setup)

**Bot Studio (43% → target 75%+):**
- Add advanced workflow patterns (conditional logic, variables, transfers)
- Add multi-channel Bot Studio examples

**CTX (25% → target 60%+):**
- Add multi-tenant architecture guide
- Add Tech Provider onboarding flow

### 2. Add Missing Use-Case Content

- **Product Catalog & Chatbots:** Use-case guide for dynamic pricing, product hierarchies
- **Tier & Pricing Info:** Add "Account & Pricing" section with tier detection, rate limits
- **Partner Setup:** Create "For Partners" or "ISV" section with multi-tenant flows

### 3. Address the Power-User Problem

**For `visitor-8cbe2c97` (and similar power users):**
- These are **integrators/ISVs**, not typical users
- KB can't satisfy all their questions — they need **sales engagement** or **technical support**
- Recommend: Detect multi-query, low-success patterns → offer "Chat with Sales" or "Technical Support" escalation

### 4. Decomposition Effectiveness

CC Express decomposed queries have **28.6% all-success rate** (7 decomposed queries, only 2 fully succeeded). This is low. The KB's retrieval is breaking complex questions into sub-parts that still fail individually.

**Action:** For CC Express, if decomposition fails, escalate to human support rather than returning multiple IDKs.

---

## Summary Table

| Category | CC Express | Standalone | Action |
|----------|-----------|-----------|--------|
| **Overall IDK Rate** | 40% | 22% | Improve KB coverage |
| **WhatsApp** | 0% | 7% | Add API setup & migration guides |
| **Bot Studio** | 43% | 93% | Add advanced patterns |
| **Power User** | 1 user = 40% of IDKs | Distributed | Escalation path for integrators |
| **Setup Intent** | 21/49 IDKs (43%) | Better distributed | Broaden setup documentation |
| **Video Coverage** | 71.8% | 69.6% | No gap (but low-answer queries still need video) |

