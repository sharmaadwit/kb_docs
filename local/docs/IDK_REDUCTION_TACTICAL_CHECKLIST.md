# Tactical Checklist: IDK Reduction Implementation

---

## Phase 1: Quick Win (48 Hours)
**Target:** Reduce IDK from 45.8% → 40-42%

### Setup (15 minutes)
- [ ] Read `/Users/adwit.sharma/kb_docs/local/docs/QUICK_WIN_IMPLEMENTATION_GUIDE.md`
- [ ] Verify access to `/Users/adwit.sharma/kb_docs/skill/kb_answer.py`
- [ ] Create feature branch (optional): `git checkout -b idk-quick-win`
- [ ] Note current time (for effort tracking)

### Code Changes (2-3 hours)
- [ ] **Step 1: Update CONCEPT_REGISTRY (lines 2167-2183)**
  - [ ] Backup current kb_answer.py (copy locally)
  - [ ] Replace sticky_assignment concept with version that includes definition template
  - [ ] Add 14 new concepts (enterprise_account_types through mo_callback_event)
  - [ ] Verify closing `]` matches opening
  - [ ] Check for syntax errors: `python3 -m py_compile skill/kb_answer.py`

- [ ] **Step 2: Add Intent Fallback Function (around line 3050)**
  - [ ] Add new function `_should_accept_search_result_despite_intent_mismatch()`
  - [ ] Verify function signature matches docstring
  - [ ] Check indentation (4-space standard)

- [ ] **Step 3: Modify kb_answer() Logic (around line 3150)**
  - [ ] Find section: "if intent == 'definition' and concept:"
  - [ ] Replace IDK return with conditional fallback
  - [ ] Verify surrounding code unchanged
  - [ ] Re-check syntax: `python3 -m py_compile skill/kb_answer.py`

### Validation (45 minutes)

#### Unit Tests (10 minutes)
- [ ] Test imports: `python3 -c "from skill.kb_answer import kb_answer, CONCEPT_REGISTRY; print('OK')"`
- [ ] Verify concept count: `python3 << 'EOF'`
```python
from skill.kb_answer import CONCEPT_REGISTRY
print(f"Concepts: {len(CONCEPT_REGISTRY)}")
assert len(CONCEPT_REGISTRY) >= 70, "Expected ≥70 concepts after additions"
print("✓ Concept count OK")
EOF
```
- [ ] Check new concepts exist:
```bash
python3 << 'EOF'
from skill.kb_answer import _CONCEPT_INDEX
new_ids = [
    "sticky_assignment", "enterprise_account_types", "partner_portal",
    "dlt_compliance", "google_sheets_integration", "campaign_broadcast",
    "api_node_vs_json_handler", "customer_360_node", "flow_id_definition",
    "webhook_payload_schema", "template_operations_guidelines",
    "ai_admin_features", "cc_express", "peoplstrong_api_integration",
    "mo_callback_event", "external_event_passthrough"
]
for cid in new_ids:
    assert cid in _CONCEPT_INDEX, f"Missing concept: {cid}"
    print(f"✓ {cid}")
print(f"✓ All {len(new_ids)} new concepts found")
EOF
```

#### Regression Test (20 minutes)
- [ ] Run existing test suite:
```bash
cd /Users/adwit.sharma/kb_docs
python3 local/scripts/idk_regression.py
```
- [ ] Verify output:
  - [ ] Q1-Q10: Still 9/10 passing
  - [ ] No new IDK on previously-answered queries
  - [ ] Confidence scores reasonable
  - [ ] No syntax errors

#### Definition Intent Test (15 minutes)
Test 5 definition-intent queries:
- [ ] Query: "What is sticky chat in Agent Assist?"
  - [ ] Expected: ANSWERED (was IDK before)
  - [ ] Verify: kb_search finds doc + kb_answer accepts it
  - [ ] Log result

- [ ] Query: "What is a Customer 360 node?"
  - [ ] Expected: ANSWERED
  - [ ] Verify: Concept definition template used
  - [ ] Log result

- [ ] Query: "What is the API node?"
  - [ ] Expected: ANSWERED
  - [ ] Verify: Concept or kb_search result accepted
  - [ ] Log result

- [ ] Query: "What is flow ID?"
  - [ ] Expected: ANSWERED
  - [ ] Verify: Concept definition template
  - [ ] Log result

- [ ] Query: "What is the Customer 360?"
  - [ ] Expected: ANSWERED
  - [ ] Verify: Concept definition template
  - [ ] Log result

#### New Concept Test (15 minutes)
Test 5 new concept queries:
- [ ] Query: "What's an enterprise WhatsApp account?"
  - [ ] Expected: Better kb_search results or ANSWERED
  - [ ] Verify: Concept boost working
  - [ ] Log result

- [ ] Query: "What is DLT whitelisting?"
  - [ ] Expected: Better results (future doc will improve)
  - [ ] Verify: Concept exists and boosts relevant doc
  - [ ] Log result

- [ ] Query: "Difference between API node and JSON handler?"
  - [ ] Expected: ANSWERED via comparison template
  - [ ] Verify: Concept definition or kb_search accepted
  - [ ] Log result

- [ ] Query: "Google Sheets integration with Gupshup?"
  - [ ] Expected: Better results or ANSWERED
  - [ ] Verify: Concept boost working
  - [ ] Log result

- [ ] Query: "What's a webhook payload schema?"
  - [ ] Expected: Better results
  - [ ] Verify: Concept found and boosted
  - [ ] Log result

### Deployment (30 minutes)

#### Pre-Deployment Checklist
- [ ] All validation tests passed
- [ ] No regressions detected
- [ ] No syntax errors
- [ ] Definition intent tests show improvement
- [ ] New concept tests show expected behavior
- [ ] Code review completed (self-review minimum)

#### Deployment Steps
- [ ] Stage changes: `git add skill/kb_answer.py`
- [ ] Create commit:
```bash
git commit -m "Fix definition intent matching + add 14 concept boosts for IDK reduction (Phase 1 quick win)"
```
- [ ] Verify commit: `git log --oneline -1`
- [ ] Note commit hash for monitoring

#### Post-Deployment (First 24 Hours)
- [ ] Monitor Langfuse traces (check every 6 hours):
  - [ ] Last 50 traces: IDK rate should decrease
  - [ ] Compare to baseline: should be 3-5% improvement
  - [ ] Check for new wrong answers (should be 0)
  - [ ] Check confidence scores healthy
- [ ] Daily regression test:
```bash
python3 local/scripts/idk_regression.py
# Should show 9/10 still passing
```
- [ ] If issues detected:
  - [ ] Document issue
  - [ ] Revert if necessary: `git revert HEAD`
  - [ ] Diagnose and fix

#### Success Criteria (After 24 Hours)
- [ ] ✅ IDK rate decreased 3-5% (45.8% → 41-42%)
- [ ] ✅ Q1-Q10 regression test still 9/10
- [ ] ✅ No new wrong answers
- [ ] ✅ Definition queries improved noticeably
- [ ] ✅ New concepts working as expected

### Documentation (15 minutes)
- [ ] Update git commit message (if vague)
- [ ] Create summary of results:
  - [ ] Starting IDK rate
  - [ ] Ending IDK rate
  - [ ] Number of queries fixed
  - [ ] Any issues encountered
- [ ] Document results in local/reports/PHASE_1_RESULTS.md

---

## Phase 2: Medium-Term (Weeks 2-3)
**Target:** Reduce IDK to 30-35%

### Document Creation (11 hours)

#### Document 1: Enterprise Account Types (2 hours)
- [ ] Create: `/Users/adwit.sharma/kb_docs/kb/channels/enterprise-account-types.md`
- [ ] Structure:
  - [ ] Overview: What is enterprise account?
  - [ ] Standard vs Enterprise comparison
  - [ ] Billing differences
  - [ ] Support differences
  - [ ] Use cases
  - [ ] How to upgrade
- [ ] Link to related: WABA, whatsapp-business-api.md
- [ ] Verify syntax and formatting

#### Document 2: Partner Portal & White-Label Setup (3 hours)
- [ ] Create: `/Users/adwit.sharma/kb_docs/kb/ctx/partner-portal-white-label-setup.md`
- [ ] Structure:
  - [ ] What is Partner Portal?
  - [ ] White-label overview
  - [ ] How to set up white-label
  - [ ] PAMS integration
  - [ ] Partner dashboard walkthrough
  - [ ] Billing for partners
- [ ] Link to: CTX docs, integration patterns
- [ ] Verify syntax and formatting

#### Document 3: DLT Compliance & Whitelisting (2 hours)
- [ ] Create: `/Users/adwit.sharma/kb_docs/kb/channels/dlt-compliance-whitelisting.md`
- [ ] Structure:
  - [ ] What is DLT?
  - [ ] Why whitelisting required?
  - [ ] Whitelisting process
  - [ ] CTA domain whitelisting
  - [ ] Compliance requirements
  - [ ] Troubleshooting whitelisting issues
- [ ] Link to: WhatsApp API, compliance docs
- [ ] Verify syntax and formatting

#### Document 4: Google Sheets Integration Pattern (2 hours)
- [ ] Create: `/Users/adwit.sharma/kb_docs/kb/integrations/google-sheets-integration-pattern.md`
- [ ] Structure:
  - [ ] Overview: Sheets API integration
  - [ ] Prerequisites (Sheets API, OAuth)
  - [ ] Step-by-step setup
  - [ ] Webhook payload for Sheets append
  - [ ] Data sync patterns
  - [ ] Troubleshooting
- [ ] Include code examples
- [ ] Link to: webhooks.md, integrations docs
- [ ] Verify syntax and formatting

#### Document 5: Campaign Broadcast Rules (2 hours)
- [ ] Create: `/Users/adwit.sharma/kb_docs/kb/campaign-manager/campaign-broadcast-rules.md`
- [ ] Structure:
  - [ ] Broadcast vs Triggered campaigns
  - [ ] When to use broadcast
  - [ ] Broadcast workflow
  - [ ] Scheduling rules
  - [ ] Retry logic
  - [ ] One-time vs recurring
- [ ] Link to: creating-your-first-campaign.md, campaign-manager overview
- [ ] Verify syntax and formatting

### Concept Registry Updates (1 hour)
- [ ] Update concept boosts to point to new docs:
  - [ ] `enterprise_account_types` → `channels/enterprise-account-types.md` (5.0 boost)
  - [ ] `partner_portal` → `ctx/partner-portal-white-label-setup.md` (5.0 boost)
  - [ ] `dlt_compliance` → `channels/dlt-compliance-whitelisting.md` (5.0 boost)
  - [ ] `google_sheets_integration` → `integrations/google-sheets-integration-pattern.md` (4.5 boost)
  - [ ] `campaign_broadcast` → `campaign-manager/campaign-broadcast-rules.md` (4.0 boost)
- [ ] Verify boosts in kb_answer.py

### Re-Index KB (30 minutes)
- [ ] Add new docs to kb_chunks.jsonl:
```bash
cd /Users/adwit.sharma/kb_docs
python3 -c "from skill.kb_chunks_utils import index_kb_folder; index_kb_folder('kb')"
```
- [ ] Verify new docs indexed:
```bash
grep -c "enterprise-account-types" kb_chunks.jsonl
grep -c "partner-portal" kb_chunks.jsonl
# Should be >0 for each
```

### Bot Studio Scoring Refactor (3 hours)
- [ ] Identify overly-generic Bot Studio pages
- [ ] Add negative weights in `_score_search_result()`:
  - [ ] "overview-of-bot-studio.md" → -0.5
  - [ ] "about-bot-studio.md" → -0.5
- [ ] Boost node-specific docs:
  - [ ] "json-handler-instead-of-code-node.md" → +1.0
  - [ ] "api-node-setup.md" → +1.0 (if exists)
  - [ ] "customer-360-node.md" → +0.5
- [ ] Test 20 Bot Studio queries
- [ ] Verify no regression on baseline

### Testing (1.5 hours)
- [ ] Test each new document with 3-5 sample queries:
  - [ ] Enterprise account doc: "What's enterprise account?", "Difference between standard and enterprise?"
  - [ ] Partner portal doc: "How to set up white-label?", "What is Partner Portal?"
  - [ ] DLT doc: "What is DLT whitelisting?", "How to whitelist domains?"
  - [ ] Sheets doc: "Can I integrate Google Sheets?", "How to sync data to Sheets?"
  - [ ] Campaign doc: "Broadcast vs triggered campaigns?", "Can I schedule campaigns?"
- [ ] Run regression test (Q1-Q10): should still be 9/10
- [ ] Run Bot Studio spot check (20 queries)

### Deployment (1 hour)
- [ ] Stage changes:
```bash
git add kb/channels/enterprise-account-types.md
git add kb/ctx/partner-portal-white-label-setup.md
git add kb/channels/dlt-compliance-whitelisting.md
git add kb/integrations/google-sheets-integration-pattern.md
git add kb/campaign-manager/campaign-broadcast-rules.md
git add skill/kb_answer.py  # Updated concept boosts + scoring
```
- [ ] Create commit:
```bash
git commit -m "Phase 2: Add 5 missing KB docs + boost concepts + refactor Bot Studio scoring"
```
- [ ] Monitor for 48 hours

### Success Criteria
- [ ] ✅ New docs indexed and searchable
- [ ] ✅ Concept boosts working
- [ ] ✅ IDK rate decreased 5-10% total (40-42% → 30-35%)
- [ ] ✅ New docs tested with sample queries
- [ ] ✅ No regressions on Q1-Q10
- [ ] ✅ Bot Studio queries improved

---

## Phase 3: Long-Term (Weeks 4+)
**Target:** Reach 25% IDK rate

### Troubleshooting Documentation (10 hours)
- [ ] Create folder: `kb/troubleshooting/`
- [ ] Create 10 troubleshooting guides:
  - [ ] Error code reference (4006, 429, etc.)
  - [ ] WhatsApp delivery troubleshooting
  - [ ] Webhook debugging guide
  - [ ] Campaign delivery issues
  - [ ] Journey Builder debugging
  - [ ] Bot Studio common issues
  - [ ] Integration troubleshooting
  - [ ] Performance & latency issues
  - [ ] Data sync troubleshooting
  - [ ] Authentication & authorization errors
- [ ] Add error-code concepts to registry

### API Reference Consolidation (5 hours)
- [ ] Create: `kb/integrations/api-fields-reference.md`
- [ ] Include:
  - [ ] Webhook payload schema
  - [ ] Webhook response format
  - [ ] Message API fields
  - [ ] Customer API fields
  - [ ] Campaign API fields
- [ ] Add cross-references to integration docs

### Comparative Documentation (4 hours)
- [ ] Create: `kb/overview/feature-comparisons.md`
- [ ] Include comparisons:
  - [ ] Campaign Manager vs Journey Builder
  - [ ] Business Hours vs Auto Replies
  - [ ] RCS vs WhatsApp API
  - [ ] Partner Portal vs CC Express vs Custom Integration

### Intent Classifier Overhaul (8 hours)
- [ ] Collect 200+ traced queries with intent labels
- [ ] Fine-tune intent classifier using training data
- [ ] Separate "definition" into 3 sub-intents:
  - [ ] feature_definition
  - [ ] architecture_definition
  - [ ] comparison_definition
- [ ] Test on full 200-query dataset
- [ ] Integrate into kb_answer.py

### Deployment & Stabilization (2 hours)
- [ ] Deploy troubleshooting docs
- [ ] Deploy API reference
- [ ] Deploy comparisons
- [ ] Deploy intent classifier
- [ ] Monitor for 2 weeks for stability

### Final Success Criteria
- [ ] ✅ IDK rate ≤ 25%
- [ ] ✅ Answer rate ≥ 75%
- [ ] ✅ Wrong answers = 0%
- [ ] ✅ All modules ≥ 70% answer rate
- [ ] ✅ No regressions on Q1-Q10 (still 9/10)

---

## Monitoring & Alerting

### Daily Checks (5 minutes)
```bash
# Run daily at same time
python3 << 'EOF'
import json
import os
from datetime import datetime

# Read latest results from local/reports/idk_regression_baseline.json
with open('local/reports/idk_regression_baseline.json') as f:
    data = json.load(f)
    
idk_count = data['summary']['outcomes']['idk']
total = data['summary']['total']
idk_rate = (idk_count / total * 100) if total else 0

print(f"[{datetime.now().isoformat()}] IDK Rate: {idk_rate:.1f}% ({idk_count}/{total})")

# Alert if increase >2%
baseline_rate = 45.8
if idk_rate > baseline_rate + 2:
    print(f"⚠️  ALERT: IDK rate increased {baseline_rate}% → {idk_rate:.1f}%")
else:
    print(f"✓ OK")
EOF
```

### Weekly Checks (30 minutes)
- [ ] Run 26-query regression test
- [ ] Calculate IDK rate by module
- [ ] Check for trending issues
- [ ] Review Langfuse traces for patterns

### Bi-Weekly Reviews (1 hour)
- [ ] Run 100-query comprehensive test
- [ ] Analyze answer rate by:
  - [ ] Module (should increase)
  - [ ] Intent (definition queries should improve)
  - [ ] Query family (enterprise, integrations, etc.)
- [ ] Document progress
- [ ] Adjust strategy if needed

---

## Rollback Procedures

### If Phase 1 fails to improve IDK
```bash
# Revert Phase 1 commit
git revert <commit-hash>
git push origin main

# Investigate:
# 1. Check concept matching: did new concepts register correctly?
# 2. Check intent logic: did fallback function execute?
# 3. Check Langfuse data: are traces using new code?
# 4. Test 5 sample queries manually
```

### If Phase 2 docs are low quality
```bash
# Remove problematic doc
git rm kb/path/to/doc.md

# Remove concept boost
# Edit kb_answer.py, comment out boost for that doc

git commit -m "Remove low-quality doc pending revision"
git push origin main

# Have product review + rewrite doc
# Re-add after approval
```

### If Phase 3 breaks classifier
```bash
# Revert intent classifier changes
git revert <commit-hash>
git push origin main

# Fallback to Phase 2 state (good classifier)
# Re-implement classifier more carefully
```

---

## Success Tracking

### Metrics Dashboard (Weekly Update)

```markdown
# IDK Reduction Progress

## Phase 1 (Weeks 1-2)
- [ ] Week 1, Day 2: IDK 45.8% → 40-42%? ____%
- [ ] Week 2, Day 1: Stable? ____%

## Phase 2 (Weeks 2-3)
- [ ] Week 2, Day 7: After docs → 35-40%? ____%
- [ ] Week 3, Day 3: Stable? ____%

## Phase 3 (Weeks 4+)
- [ ] Week 4, Day 1: Troubleshooting docs → 30-35%? ____%
- [ ] Week 4, Day 7: Classifier tuning → 25-30%? ____%
- [ ] Final: Reach 25%? ____%

## Overall
- [ ] Target: 25% IDK rate
- [ ] Achieved: ____%
- [ ] Date achieved: __________
```

---

## Summary

**Phase 1 (48 hours):** Quick win with concept boosts + intent fixes  
**Phase 2 (2 weeks):** Document gaps + scoring improvements  
**Phase 3 (2 weeks):** Troubleshooting + API reference + classifier  
**Total:** 30 days to reach 25% IDK rate

Start Phase 1 immediately. Success gates proceed to Phase 2. Phase 2 success gates Phase 3.
