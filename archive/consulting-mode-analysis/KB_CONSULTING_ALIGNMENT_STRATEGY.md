# KB Consulting-Tone Alignment Strategy
**Date:** 2026-08-13  
**Status:** Comprehensive audit completed  
**Scope:** Entire KB across 14 major topics  

---

## Executive Summary

**Goal:** Align entire KB to support consulting-tone answers (diagnosis → context → options → recommended → follow-up) across all topics, not just Bot Studio.

**Current State:**
- **14 major topics** (Bot Studio, WhatsApp, SMS, RCS, Campaign Manager, SuperAgent, Agent Assist, etc.)
- **7,144 total KB chunks** (largest: Bot Studio 2,391 chunks; smallest: SMS 10 chunks)
- **Consulting readiness scores** vary widely:
  - ✅ HIGH (65-70%): Campaign Manager, SuperAgent
  - ⚠️ MEDIUM (45-55%): Channels, Agent Assist, Goals & Analytics, RCS
  - ❌ LOW (25-40%): WhatsApp, Bot Studio, Integrations, Personalize

**Key Finding:** All topics can support consulting-tone, but require restructuring to:
1. Add diagnostic questions (identify use case)
2. Provide context (prerequisites, trade-offs)
3. Present options (2-4 paths)
4. Recommend approach (evidence-based)
5. Enable follow-ups (for multi-turn conversations)

---

## Critical Issues Found

### Structure Problems (95% of KB affected)
- **6,768 chunks (95%)** have duplicate heading markers (e.g., `## Definition\n## Definition`) hurting semantic search
- **Inconsistent chunk sizing:** 1-69 chunks per document (no consistent strategy)
- **27 orphaned chunks** (<50 bytes) polluting retrieval with low-value hits
- **Missing metadata:** 95 chunks lack heading_path, 77 lack section_type classification
- **Limited cross-references:** Only 65 chunks (0.9%) include 'see also' markers for multi-turn support

### Content Gaps (Consulting perspective)
| Topic | Current Structure | Gap | Impact |
|-------|-------------------|-----|--------|
| **WhatsApp** | Setup → Troubleshooting | No diagnosis of use case or business context | 25% consulting-ready; customers pick wrong setup path |
| **Bot Studio** | 98 node files (node-driven) | No workflow-level guidance; lacks 'when' + 'why' | 30% consulting-ready; high time-to-first-working-bot |
| **RCS** | Feature gallery + best practices | No readiness diagnosis (carrier support, compliance) | 55% consulting-ready; unclear setup prerequisites |
| **Integrations** | Platform docs + setup steps | No decision framework for which CRM/integration to pick | 40% consulting-ready; scope creep in implementations |
| **Campaign Manager** | Strong procedural docs | Missing business goal diagnosis | 70% consulting-ready; already relatively strong |

### Metadata Gaps (All topics)
1. **No intent classification** — Can't distinguish 'how-to' from 'troubleshoot' from 'concept'
2. **No cross-references** — Multi-turn conversations unsupported
3. **No consulting markers** — Can't flag sections that support multi-turn consulting
4. **No audience/persona** — Can't tailor to developer vs admin vs end-user
5. **No complexity rating** — Can't scale explanations for different knowledge levels

---

## Optimization Strategy: 3-Batch Rollout

### BATCH 1: Immediate (Week 1) — HIGH IMPACT
**Timeline:** Aug 13-19  
**Topics:** Bot Studio, RCS Setup, Error Handling & Resilience  
**Effort:** 15 chunks, 8-10 hours  
**Expected accuracy gain:** +10-15pp (from 62% baseline to 75%+)

#### Bot Studio Journey Configuration
- **Action:** Restructure 3 high-impact chunks
  1. Split journey builder UI into: Diagnosis (when to build) → Context (journey types) → Options (5 node types) → Recommended → Best practices
  2. Create dedicated conditional branching chunk with diagnosis (routing scenario?) → context (Decision node types) → options (3 patterns) → recommended → troubleshooting
  3. Reorganize loop prevention into diagnostic checklist format
- **Impact:** Unlocks 35% of high-volume Bot Studio queries to consulting structure
- **Validation:** "How do I use conditional branching?" should show diagnosis + 3+ options + recommended path

#### RCS Setup & Configuration
- **Action:** Add 4 new chunks + 1 rewrite
  1. **Diagnosis:** "When to use RCS" with decision tree (Is RCS available in your market? Do you have >10K/day volume?)
  2. **Context:** "RCS prerequisites" (carrier support, compliance, scale requirements)
  3. **Options:** "3 setup paths" (manual <10K/day, API-driven for scaling, hybrid RCS+SMS)
  4. **Recommended:** Production pattern with carrier timeline (4-6 weeks approval)
  5. **Rewrite:** "How to set up RCS" from generic to context-gated answer
- **Impact:** Moves from 75% accuracy (but low consulting) to 80%+ accuracy + 70% consulting quality
- **Validation:** "How do I set up RCS?" should show diagnosis + prerequisites + 3 setup paths + recommended based on scale

#### Error Handling & API Resilience
- **Action:** Build new diagnostic section (6 chunks)
  1. **Diagnosis:** "Which error patterns?" (HTTP status, timeouts, validation, auth)
  2. **Context:** "Error recovery stages" (request → response → parsing)
  3. **Options:** "3 recovery strategies" (status code check, smart retry, fallback services)
  4. **Recommended:** Production error handling checklist
  5. **Follow-up:** Troubleshooting tree (endpoint accessible? auth headers?)
- **Impact:** Addresses 3 critical low-accuracy queries; unlocks 25% of advanced setup queries
- **Validation:** "How do I handle errors in API nodes?" should show diagnosis + 3 recovery options + recommended production pattern

---

### BATCH 2: High Priority (Week 2) — SCALING CONCEPTS
**Timeline:** Aug 20-26  
**Topics:** WhatsApp Advanced, SMS Error Codes, Webhook Integration  
**Effort:** 12 chunks, 7-8 hours  
**Expected accuracy gain:** +8-12pp

**Key Work:**
- WhatsApp: Add decision framework (WABA vs Simple API vs Resellers)
- SMS: Create diagnostic tree for DLT/compliance scenarios
- Webhooks: Add payload structure guides + security best practices

---

### BATCH 3: Medium Priority (Weeks 3-4) — FULL PLATFORM
**Timeline:** Aug 27-Sep 9  
**Topics:** Campaign Manager, Personalize/CDP, Analytics Strategy  
**Effort:** 10 chunks, 5-6 hours  
**Expected accuracy gain:** +5-8pp

**Key Work:**
- Campaign Manager: Add business goal diagnosis (acquisition vs retention vs re-engagement)
- Personalize: Create business case (when CDP makes sense, ROI models)
- Analytics: Industry benchmarks + goal-setting framework

---

## Critical Success Factors

### Accuracy Threshold: 75%+
- **MUST achieve before enabling consulting-tone broadly**
- Consulting structure masks inaccuracy (false confidence risk)
- User principle: "Consulting make sense only when we have accuracy. We don't need confident false positives"

### Validation Gates
**Batch 1 must pass all checks before Batch 2 starts:**
1. ✅ 75%+ accuracy on validation queries (human review)
2. ✅ <10% retrieval regression (queries that were high-confidence should still rank top-5)
3. ✅ Multi-chunk coherence (if answer requires context + options + recommendation, all chunks must retrieve together)

**If accuracy drops below 70% on any Batch 1 topic after 1 week live:**
- 🛑 PAUSE consulting structure rollout
- Revert to problem-solution format
- Investigate root cause

---

## Risk Mitigation

| Risk | Detection | Mitigation |
|------|-----------|-----------|
| **Retrieval Regression** | Monitor retrieval scores pre/post restructure. Alert if >10% of topic queries show score drop >1.5 points | Phase rollout by topic. Validate retrieval before moving to next batch. Use semantic bridges linking old to new structure. |
| **False Confidence** | Weekly accuracy spot-checks (10 random queries per topic, human review). If average <70%, pause | Never add consulting to chunks with accuracy <65%. Rewrite for accuracy FIRST, add consulting second. |
| **Chunk Interdependency Breaks** | Track multi-chunk retrievals. If >15% of queries retrieve 1 chunk when they should retrieve 2+, dependency broken | Add cross-references: "See Prerequisites [link]". Create chunking matrix for co-retrieval. Tag chunks with required companion chunks. |
| **Routing Violations** | Monthly audit: sample 50 queries per topic, measure consulting score distribution. Alert if drift >5% | Start Batch 2/3 with 'soft' consulting (follow-ups only). Tag chunks with consulting_intent flags. Implement routing gates based on confidence. |
| **Accuracy Floor Not Met** | If Batch 1 doesn't reach 75%, don't proceed to Batch 2 | Prerequisite: Verify baseline retrieval ≥65% before restructuring. Run 'accuracy pre-audit' before starting batch. |

---

## Content Gaps Requiring New Docs (Priority Order)

### Tier 1: Decision Frameworks (1 per major topic)
- "Should I use WhatsApp?" (with diagnosis flowchart)
- "Should I build a bot?" (vs API vs manual)
- "Should I implement Agent Assist?" (readiness assessment)
- "Which CRM should I integrate?" (Salesforce vs HubSpot vs Dynamics decision tree)

### Tier 2: Use-Case Scenario Library
- E-commerce order tracking (WhatsApp + goals)
- Support escalation (Bot Studio + Agent Assist + CRM)
- Lead qualification (Bot Studio + campaigns)
- Re-engagement campaign (Personalize + Campaign Manager)

### Tier 3: Anti-Patterns & Common Mistakes
- "Don't create 1 massive bot when 3 focused bots work better"
- "Don't sync all customer data on day 1"
- "Don't use campaigns when you need real-time engagement"

### Tier 4: Implementation Roadmaps
- Phased progression for each major feature
- Example: Campaign Manager Week 1 (single channel) → Week 2 (segmentation) → Week 3 (multi-channel)

### Tier 5: Industry Benchmarks
- By vertical: e-commerce, financial services, healthcare, SaaS
- Expected metrics: CTR, CSAT, resolution time, AOV

---

## Immediate Next Steps

### Week 1 (Now → Aug 19)
1. ✅ Fix KB structure issues (remove duplicate headings from 6,768 chunks)
2. ✅ Create Batch 1 chunks (Bot Studio, RCS, Error Handling)
3. ✅ Run validation queries (human review for accuracy)
4. ✅ Measure retrieval quality (pre/post comparison)
5. ✅ Gate accuracy ≥75% before Batch 2 start

### Week 2-4 (Aug 20-Sep 9)
- Execute Batch 2 & 3 rollout
- Maintain 75%+ accuracy threshold
- Monitor false confidence risk
- Add missing content (decision frameworks, use-case scenarios)

### Success Metric
- **By Sep 9:** Entire KB consultable across 14 topics with:
  - 75%+ average accuracy per topic
  - <10% retrieval regression
  - 40%+ of KB chunks supporting multi-turn conversations
  - Consulting-tone enabled universally (not just Phase 1 modules)

---

## Files & Results

**Audit Results:**
- Topics breakdown: 14 major topics, 7,144 chunks total
- Retrieval quality: 6/9 test queries GOOD or MEDIUM (67%)
- Consulting readiness: Range 25%-70% (avg 47%)

**Optimization Details:**
- Batch 1: 15 chunks, 3 topics, 8-10 hours
- Batch 2: 12 chunks, 3 topics, 7-8 hours
- Batch 3: 10 chunks, 3 topics, 5-6 hours
- **Total:** 37 chunks of new/restructured content, ~20-24 hours work

**Validation Plan:**
- 5 validation queries per batch
- Human accuracy review (0-100 scale)
- Retrieval regression monitoring
- Weekly spot-checks (10 random queries per topic)

---

## Decision Point

**Option A:** Start Batch 1 immediately (Week 1)
- Restructure Bot Studio, RCS, Error Handling chunks
- Validate 75%+ accuracy
- Risk: High effort this week, but unlocks consulting for 35% of KB

**Option B:** Do KB structure cleanup first (deduplicate headings, metadata)
- Fix 6,768 duplicate heading issues (single post-processing pass)
- Should improve baseline retrieval +15-20%
- Then proceed to Batch 1 with better foundation

**Recommendation:** Option B → Option A
- Cleanup alone improves retrieval without consulting restructure (low risk)
- Then proceed to consulting format with better baseline

---

*Prepared by: Consulting KB Audit Workflow*  
*Confidence Level: High (based on structural analysis + 9 sample queries + metadata review)*
