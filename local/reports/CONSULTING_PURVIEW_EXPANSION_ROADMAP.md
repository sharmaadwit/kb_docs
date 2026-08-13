# Consulting-Tone Expansion: Complete Purview Roadmap
**Date:** 2026-08-13  
**Status:** Phase 1 deployed, Phases 2-4 planned

---

## 🎯 Mission: Consulting-Tone for ALL Topics

Transform the entire KB to support diagnosis-driven, multi-turn engagement across all 14+ topics.

---

## 📋 Full Topic Inventory (14 Topics)

### ✅ Phase 1 (DEPLOYED - 3 topics, 14 files, 75 chunks)
1. **Bot Studio** (3 consulting files)
   - consulting-conditional-branching.md
   - consulting-loop-prevention.md
   - consulting-when-to-build.md

2. **RCS** (5 consulting files)
   - rcs-readiness-diagnosis.md
   - rcs-prerequisites-checklist.md
   - rcs-setup-paths.md
   - rcs-fallback-strategy.md
   - rcs-setup-comprehensive.md

3. **Error Handling** (6 consulting files)
   - error-handling-diagnosis.md
   - error-handling-http.md
   - error-handling-timeouts.md
   - error-handling-retry.md
   - error-handling-fallback.md
   - error-handling-production-checklist.md

### ⏳ Phase 2 (HIGH IMPACT - 3 topics, estimate 12-15 files)
4. **Channels & Integration** (SMS, WhatsApp, Email, Facebook, Telegram, LinkedIn)
   - channels-routing-diagnosis.md (when to use each channel)
   - channels-compliance-checklist.md (regulatory requirements per channel)
   - channels-fallback-strategy.md (SMS fallback from RCS/WhatsApp)
   - channels-error-codes-by-platform.md (channel-specific errors)
   - channels-rate-limiting-strategy.md

5. **Agent Assist** (AI-powered agent responses)
   - agent-assist-readiness-diagnosis.md (when AI agent vs rule-based)
   - agent-assist-prompt-design.md (crafting effective system prompts)
   - agent-assist-guardrails-checklist.md (safety + compliance)
   - agent-assist-hallucination-mitigation.md (fact-checking strategies)
   - agent-assist-fallback-to-rules.md

6. **Campaign Manager** (Multi-channel campaigns)
   - campaign-strategy-diagnosis.md (campaign type selection)
   - campaign-segmentation-paths.md (audience segmentation approaches)
   - campaign-performance-monitoring.md (KPI tracking + optimization)
   - campaign-ab-testing-framework.md

### ⏳ Phase 3 (FOUNDATION - 3 topics, estimate 10-12 files)
7. **SuperAgent** (Platform orchestration)
   - superagent-architecture-diagnosis.md
   - superagent-routing-strategies.md
   - superagent-multi-hop-resolution.md

8. **Goals & Analytics** (Conversation analytics + funnel tracking)
   - goals-funnel-design.md (setup + tracking)
   - analytics-query-classification.md (understand user intent)
   - analytics-accuracy-improvement-roadmap.md

9. **Integrations** (APIs, webhooks, 3rd-party services)
   - integrations-readiness-diagnosis.md
   - integrations-webhook-strategy.md
   - integrations-error-recovery-paths.md

### ⏳ Phase 4 (ADVANCED - 5 topics, estimate 12-15 files)
10. **Personalization** (User context, preference storage)
    - personalization-strategy-diagnosis.md
    - personalization-data-model-design.md
    - personalization-privacy-compliance.md

11. **AI Admin** (Model management, fine-tuning)
    - ai-admin-model-selection.md
    - ai-admin-fine-tuning-strategy.md
    - ai-admin-performance-benchmarking.md

12. **Context Management** (Session state, memory)
    - context-memory-strategies.md
    - context-state-machine-design.md
    - context-cleanup-retention-policy.md

13. **Gupshup Console** (Admin/onboarding)
    - console-account-setup-diagnosis.md
    - console-team-collaboration-paths.md
    - console-security-checklist.md

14. **Webhooks & Callbacks** (Event handling)
    - webhooks-event-routing-diagnosis.md
    - webhooks-retry-strategy.md
    - webhooks-idempotency-guarantee.md

---

## 🚀 Execution Strategy

### Phase 1 Already Complete ✅
- **Status**: Deployed to GitLab + kb_chunks.jsonl
- **Pending**: SuperAgent embedding indexing
- **Next**: Monitor live accuracy, gather user feedback

### Phase 2: Launch Timeline (Week 1-2)

**Step 1: Content Audit** (4 hours)
- List existing KB files for each Phase 2 topic
- Identify gaps: what consulting questions users ask but KB doesn't cover
- Prioritize high-impact files (e.g., channels errors, agent guardrails)

**Step 2: Consulting File Creation** (12-15 files, ~8-10 hours)
- Follow Phase 1 template: diagnosis → context → options → recommended → followup
- Channels: Routing logic, compliance, fallback strategies
- Agent Assist: Readiness criteria, prompt design, hallucination mitigation
- Campaign Manager: Strategy selection, segmentation, optimization

**Step 3: KB Chunk Conversion** (2 hours)
- Extract sections into JSONL chunks
- Tag with `intent: "consulting"`, version, update_date
- Add to kb_chunks.jsonl

**Step 4: SuperAgent Deployment** (1 hour)
- Push updated kb_chunks.jsonl to GitLab
- Request SuperAgent embedding indexing
- Monitor traces for new consulting chunks in retrieval

**Step 5: Accuracy Validation** (4-6 hours)
- Test 10-15 queries per topic
- Target: 75%+ accuracy for Phase 2
- Adjust content if needed

### Phase 3: Medium-Term (Week 2-3)
- SuperAgent orchestration (platform-level routing)
- Analytics & goals (user behavior, funnel tracking)
- Integrations (API patterns, error recovery)

### Phase 4: Long-Term (Week 3-4)
- Advanced topics (personalization, AI admin, context management)
- Gupshup-specific (console setup, team collaboration)
- Event handling (webhooks, async patterns)

---

## 📊 Coverage by Topic Type

### Procedural Topics (how-to guides) → Consulting Perfect Fit
- Channels setup
- RCS configuration
- Campaign creation
- Webhook integration
- **Action**: Create diagnosis (which channel?), options (3 setup paths), recommended (best practice)

### Reference Topics (API docs, schemas) → Limited Consulting Value
- Gupshup Console structure
- Model card specs
- Webhook event formats
- **Action**: Keep mostly standard format, add context section for "when/why use this"

### Troubleshooting Topics (errors, debugging) → Consulting Strong Fit
- Error codes (channels, Agent Assist)
- Timeout strategies
- Rate limiting
- **Action**: Diagnosis (error classification), options (recovery strategies), recommended (most common fix)

### Conceptual Topics (patterns, best practices) → Consulting Good Fit
- Personalization strategy
- Campaign segmentation
- AI safety guardrails
- **Action**: Diagnosis (user's goal), options (architectural approaches), recommended (trade-offs)

---

## 🎯 Accuracy & Quality Gates

### Pre-Expansion Gate (Phase 2+)
- [ ] Phase 1 accuracy: 75%+ across all 3 topics
- [ ] Phase 1 engagement metrics: +15% conversation turns
- [ ] Consulting chunks properly indexed in SuperAgent

### Phase 2 Launch Gate
- [ ] 12-15 new consulting files created
- [ ] 60-80 new chunks in kb_chunks.jsonl
- [ ] Validation: 75%+ accuracy on sample queries
- [ ] No regression on Phase 1 topics

### Phase 3/4 Incremental Gates
- Each phase: 75%+ accuracy minimum before rollout
- No topic expansion until prior phase stabilizes
- Gradual traffic allocation (10% → 50% → 100%)

---

## 💰 Estimated Effort

| Phase | Topics | Files | Chunks | Effort | Timeline |
|-------|--------|-------|--------|--------|----------|
| 1 | 3 | 14 | 75 | ✅ Done | Week 0 |
| 2 | 3 | 12-15 | 60-80 | 25-30h | Week 1-2 |
| 3 | 3 | 10-12 | 50-65 | 20-25h | Week 2-3 |
| 4 | 5 | 12-15 | 65-80 | 30-35h | Week 3-4 |
| **TOTAL** | **14** | **48-56** | **250-300** | **75-90h** | **Month 1** |

---

## 🔧 Tools & Resources Needed

### From KB Team (Us)
1. Consulting file creation (markdown authoring)
2. KB chunk conversion (JSONL formatting)
3. Accuracy validation (live trace analysis)
4. Documentation & playbooks

### From SuperAgent Team
1. **Embedding generation** for 250-300 new chunks
2. **Vector DB indexing** (weekly re-indexing as chunks added)
3. **Search performance** monitoring (ensure new chunks appear in retrieval)
4. **Fallback logic** if consulting chunks aren't retrieved

### External (Optional)
- Customer feedback loop (which topics need consulting most?)
- Analytics dashboard (engagement lift by topic)
- A/B testing infrastructure (consulting vs standard side-by-side)

---

## 📈 Success Metrics (Post-Expansion)

### By Topic Accuracy
- Phase 1 (Bot Studio, RCS, Error Handling): 75%+
- Phase 2 (Channels, Agent Assist, Campaign): 75%+
- Phase 3 (SuperAgent, Goals, Integrations): 72%+ (foundation layer)
- Phase 4 (Advanced topics): 70%+ (niche use cases)

### Engagement Metrics (A/B comparison)
- **Conversation Turns**: Baseline + 20%
- **Session Duration**: Baseline + 30%
- **Follow-up Rate**: Baseline + 25% (consulting triggers more multi-turn)
- **Bot Abandonment**: Baseline - 20% (clearer escalation paths)

### Content Quality
- False confidence cases: <3% (requires accurate evidence)
- Consulting structure adherence: 95%+ (diagnosis + options + recommended present)
- User satisfaction (if available): 80%+ (consulting perceived as helpful)

---

## ⚠️ Risks & Mitigations

### Risk 1: Consulting chunks not indexed
- **Symptom**: Queries still retrieve old chunks despite new files in JSONL
- **Mitigation**: Coordinate weekly with SuperAgent team on embedding updates
- **Fallback**: Include consulting content in existing chunk updates

### Risk 2: Accuracy drops with expanded topics
- **Symptom**: Phase 2+ topics show <70% accuracy
- **Mitigation**: Lighter consulting structure (skip options if only 1 path), more diagn osis focus
- **Fallback**: Revert to standard format for low-accuracy topics

### Risk 3: False confidence increases
- **Symptom**: Consulting answers wrong but sound confident
- **Mitigation**: Stricter confidence thresholds (only consulting if confidence >0.65)
- **Fallback**: Add disclaimers to consulting answers under uncertainty

### Risk 4: User confusion with too many topics
- **Symptom**: Consulting queries not segmented by module, mixed with standard
- **Mitigation**: Consulting enabled only for Phase 1 initially, gradual rollout
- **Fallback**: Feature flag to disable consulting per-topic

---

## 📋 Action Plan (Next 24 Hours)

1. **[ ] Prioritize Phase 2 Topics**
   - Which 3 topics drive most user engagement?
   - Which have most support requests?
   - Which have clearest consulting format?

2. **[ ] SuperAgent Coordination**
   - Confirm: Can they index 250-300 chunks weekly?
   - Confirm: Vector DB re-indexing frequency
   - Confirm: Search performance monitoring

3. **[ ] Create Phase 2 Skeleton**
   - List 12-15 consulting files needed
   - Assign effort estimate per file
   - Draft outline for high-priority files

4. **[ ] Establish Accuracy Baseline**
   - Run 30-query validation across Phases 2-4 topics
   - Document current accuracy (pre-consulting)
   - Set 75%+ target per phase

5. **[ ] Setup Monitoring Dashboard**
   - Track consulting chunk retrieval rate by topic
   - Track accuracy by topic + answer_mode
   - Alert if consulting chunk retrieval <50%

---

## 🔑 Key Principles

1. **Diagnostic-First**: Every consulting file starts with "What's your situation?" not "Here's how to..."
2. **Options-Based**: Offer 2-4 paths, NOT single prescriptive answer
3. **Evidence-Backed**: Only offer consulting if KB evidence is strong (>0.65 confidence)
4. **Accuracy Before Scale**: Stabilize Phase 1 (75%+) before expanding to Phase 2
5. **Gradual Rollout**: 10% → 50% → 100% traffic per topic, not all-or-nothing
6. **Fallback Ready**: Always have standard format as fallback if consulting fails

---

## 📞 Decision Gate

**Before proceeding with Phase 2, confirm:**

1. [ ] SuperAgent team can handle weekly embedding indexing
2. [ ] Phase 1 topics reach 75%+ accuracy (not just coverage)
3. [ ] Engagement metrics show +15% turns baseline (not just theoretical)
4. [ ] Consulting structure working end-to-end (diagnosis → options → recommended)

---

**Next Step**: Run Phase 1 validation + SuperAgent indexing coordination. Target Phase 2 kickoff once Phase 1 stabilizes (likely within 3-5 days).

