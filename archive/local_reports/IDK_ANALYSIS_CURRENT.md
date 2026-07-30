# IDK Analysis — Current KB State (July 10, 2026)

**Generated:** 2026-07-10  
**Scope:** Analysis of I-don't-know responses across recent test cycles and KB additions  
**Status:** Post-SSO & WhatsApp Promo KB additions

---

## Executive Summary

Following the addition of two new KB documents (SSO and WhatsApp Promotional Restrictions), we conducted workflow-based testing to evaluate answer quality across high-level policy questions. Results show:

- **SSO Document**: 1/5 high-level policy questions answered (20% pass rate, 2.2/10 quality)
- **WhatsApp Document**: 5/5 high-level policy questions answered (100% pass rate, 7.0/10 quality)
- **Root cause for SSO IDK**: Search ranking issue — chunks exist in kb_chunks.jsonl but aren't being surfaced by kb_answer's search algorithm

---

## Problem Breakdown

### 1. SSO Document Search Ranking Issue

**The Issue:**
The SSO document was added to kb_chunks.jsonl with 12 chunks covering SAML 2.0, IdP integration, Azure AD setup, and troubleshooting. However, when test queries like "Does Gupshup Console support Single Sign-On?" are run, kb_answer returns IDK instead of the SSO content.

**Why It Happens:**
- Chunks are present and valid (verified: `grep "SSO\|SAML" kb_chunks.jsonl | wc -l` → 18 matches)
- kb_answer retrieves these chunks but doesn't rank them in top results
- Instead, search returns unrelated content (e.g., Console overview, other WhatsApp docs)
- This is a **search relevance/ranking problem**, not a document quality or format problem

**Evidence:**
```
Test Query: "Does Gupshup Console support Single Sign-On?"
Expected: SSO document chunks with SAML 2.0 definition
Actual: "I don't know based on the available documentation"
Top Results: Console overview, WhatsApp Flows, other unrelated docs
```

**Why This Isn't a KB Content Issue:**
- Document structure follows KB standards ✅
- Content covers the core question ✅
- Chunks are indexed ✅
- *Problem is the search algorithm doesn't prioritize them*

---

### 2. WhatsApp Promotional Restrictions — Working Well

**The Good:**
All 5 high-level policy questions about WhatsApp promotional restrictions are answered:
- "Can I send promotional messages on WhatsApp Business?" ✅
- "Are there restrictions on dietary supplement promotion?" ✅
- "Do I need user consent before sending promotional messages?" ✅
- "What types of content violate WhatsApp guidelines?" ✅
- "Can I promote multivitamins on WhatsApp?" ✅

**Quality:** 7.0/10 — solid for a policy doc, answers yes/no and restriction questions directly

**Why It Works:**
- Cleaner keyword matching (promotional, WhatsApp, restrictions, dietary supplements)
- Less competition from unrelated docs
- Content is well-scoped to the use case

---

## Known IDK Categories (Historical + Current)

From the June 16 analysis (REMAINING_IDK_ANALYSIS.md), 16 IDK queries clustered into:

| Category | Count | Example | Status |
|----------|-------|---------|--------|
| **Missing KB** | 7 | Sticky Chat, Partner Portal, DLT Whitelisting | Undocumented features |
| **Search Ranking** | 4 | SSO, WABA config (before fix) | Algorithm issue |
| **Partial Answers** | 3 | Enterprise accounts, Campaign broadcast | Needs expansion |
| **Integration Patterns** | 2 | Google Sheets, PeopleStrong APIs | Custom integrations gap |

### Newly Identified: SSO Search Ranking

The SSO document is **not a missing KB problem** — it's our **first confirmed search-ranking issue**. Unlike the 7 truly missing features, SSO content exists and is well-structured; the problem is discoverability.

---

## Root Cause Analysis: Why SSO Doesn't Rank

### Hypothesis 1: Keyword Competition (Unlikely)
Search for "Console SSO" should be specific enough. The SSO document's definition includes exact keywords:
```
"Console SSO (Single Sign-On) integration enables organizations to authenticate 
users through their own identity provider (IdP) using SAML 2.0."
```

### Hypothesis 2: Search Algorithm Deprioritizes New Docs (Possible)
The search ranking logic may:
- Weight document age/freshness negatively
- Prioritize older, "proven" documents over newly added ones
- Use TF-IDF or similar without recency normalization

### Hypothesis 3: Chunk Isolation Without Document Metadata (Likely)
If search operates at the chunk level without document-level signals:
- Individual chunks may score low
- No document-level boost for "this is an official SSO guide"
- Chunks from general docs (e.g., "Gupshup Console Overview") may rank higher by accident

### Hypothesis 4: Search Windows / Context Limits (Possible)
If the retrieval step truncates results early, new/low-scoring chunks are dropped before the ranker sees them.

---

## Impact on Current Projects

### LRP Spotscan 2.0 / Meta Project
**Risk:** If we add agent knowledge via the KB and it doesn't surface in search, the conversational AI won't find it.
- SSO/SAML for Console administration was meant as policy guidance
- With SSO search failing, similar docs (e.g., "WhatsApp Business Account Setup") may also fail if they're new
- **Mitigation:** Use BizAI connectors to pull live data instead of relying on KB search for critical knowledge

### Future KB Additions
**Going Forward:**
1. Test every new KB doc immediately after adding it via test queries
2. If a doc doesn't surface in search, investigate search ranking before considering it "ready"
3. Consider adding docs in batches to establish search baselines

---

## Recommendations

### Immediate (This Week)

1. **Investigate kb_answer search algorithm**
   - Debug why SSO chunks aren't ranking despite being present
   - Check: relevance scoring, chunk deduping, result truncation
   - File: `skill/kb_answer.py` around search/retrieval stages

2. **Workaround for LRP Project**
   - For critical agent knowledge, use BizAI connectors instead of KB search
   - Example: Spotscan results → call LRP's DSF API directly, don't rely on KB

3. **Re-test SSO after fix**
   - Once search is corrected, re-run SSO policy questions
   - Expected: 5/5 pass rate, ~8.0/10 quality (like WhatsApp doc)

### Short-term (This Sprint)

4. **Implement search quality gates**
   - New KB docs → 5-query validation before marking "ready for production"
   - If <80% of queries return relevant answers, investigate ranking

5. **Profile search performance**
   - Measure chunk relevance scores pre/post ranking
   - Log why certain chunks were dropped from top results
   - Feed back into ranking algorithm tuning

### Medium-term (Next Sprint)

6. **Document search ranking model**
   - What signals matter? (keyword match, chunk age, document type, user feedback)
   - How are scores normalized across documents?
   - What's the cutoff for "relevant enough to return"?

7. **Add document-level metadata**
   - Mark critical docs (e.g., "SSO is a core feature") → boost ranking
   - Tag docs by module/use case → help search contextualize
   - Version document updates → don't penalize recency

---

## Test Results Summary

### SSO Document
```
Test: 5 high-level policy questions
Results:
  ✅ Document structure valid
  ✅ Chunks present (12 chunks, 18 keyword matches)
  ❌ Search ranking failed (2.2/10 quality, 1/5 passed)
  ❌ Root cause: kb_answer not surfacing SSO in results

Next: Debug kb_answer search, re-test after fix
```

### WhatsApp Promotional Restrictions
```
Test: 5 high-level policy questions
Results:
  ✅ 5/5 questions answered (100% pass rate)
  ✅ Quality 7.0/10 (solid for policy doc)
  ✅ Keyword matching working
  ✅ Ready for production

Next: Deploy to production, monitor for edge cases
```

---

## Appendix: Previously Documented IDK Gaps

| Gap | Category | Priority | Solution |
|-----|----------|----------|----------|
| Sticky Chat | Missing KB | Medium | Create Agent Assist feature guide |
| Partner Portal | Missing KB | High | Document partner onboarding flow |
| DLT Whitelisting | Missing KB | Medium | Document compliance & URL setup |
| Google Sheets Integration | Missing KB | Low | Create integration cookbook |
| Custom Integrations | Missing KB | Medium | Document connector framework |
| SSO Search Ranking | Algorithm | **Critical** | Fix kb_answer search |
| WhatsApp Promo | Document | ✅ Resolved | Deploy |
| Triggered Campaigns | Missing KB | Medium | Document Journey Builder triggers |

---

## Conclusion

We now have **two distinct IDK problem categories**:

1. **Missing documentation** (7 features) — requires KB writing
2. **Search ranking** (SSO, potentially others) — requires search algorithm fix

The SSO document is production-ready in content; it's the search infrastructure that needs fixing. With WhatsApp promo working well, we can proceed with that, but SSO needs the search fix before it's useful at scale.

**Recommended action:** Treat SSO search ranking as a blocking issue for the LRP project (which depends on similar KB-to-agent knowledge transfer).

