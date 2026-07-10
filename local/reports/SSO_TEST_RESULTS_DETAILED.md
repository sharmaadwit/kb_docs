# SSO Document Test Results

## Executive Summary

Tested the newly added Gupshup Console SSO Support document against 5 high-level policy questions using kb_answer.

**Test Results:**
- Passed: 1/5
- Failed: 4/5
- Average Quality Score: 2.2/10

## Detailed Test Results

### Question 1: "Does Gupshup Console support Single Sign-On?"

**Result:** FAIL (Quality: 0/10)

- **Answered:** Yes (by kb_answer flag)
- **Top Source:** kb/overview/welcome-to-gupshup-console.md
- **Confidence:** 0.15
- **Response:** Welcome to Gupshup Console overview page (generic)
- **Expected:** SSO document with definition and features
- **Issue:** Query scored SSO chunks at 0.85 max, but welcome page at 1.20, so generic console page was preferred

### Question 2: "What identity providers does Console SSO support?"

**Result:** FAIL (Quality: 1/10)

- **Answered:** No
- **Top Source:** kb/overview/welcome-to-gupshup-console.md
- **Confidence:** 0.075
- **Response:** "I don't know based on the current docs."
- **Expected:** Active Directory, Azure AD, SAML-supported providers
- **Issue:** Query scored SSO chunks at 0.60 max, too low to trigger retrieval

### Question 3: "Can my organization use SAML 2.0 with Console?"

**Result:** FAIL (Quality: 0/10)

- **Answered:** Yes (by kb_answer flag)
- **Top Source:** kb/overview/welcome-to-gupshup-console.md
- **Confidence:** 0.075
- **Response:** Projects & Organizations page (not relevant)
- **Expected:** SSO document with explicit SAML 2.0 support statement
- **Issue:** Generic console pages score higher than specific SSO content

### Question 4: "Do I need admin access to set up Console SSO?"

**Result:** PASS (Quality: 10/10)

- **Answered:** Yes
- **Top Source:** kb/overview/manage-organisation.md
- **Confidence:** 0.081
- **Response:** Console roles information about Org Admin/Owner
- **Why It Passed:** This question matched admin-related content in manage-organisation.md
- **Note:** The SSO document also contains the answer (Prerequisites section mentions "Admin access to Gupshup Console") at 0.65 score

### Question 5: "What certificate formats are accepted for SSO?"

**Result:** FAIL (Quality: 0/10)

- **Answered:** No
- **Top Source:** kb/bot-studio/functions-from-i-l.md
- **Confidence:** 0.0375
- **Response:** "I don't know based on the current docs."
- **Expected:** .pem and .cer formats per SSO document
- **Issue:** Query scored SSO chunks at 0.30 max, below MIN_CHUNK_SCORE (0.3)

## Detailed Scoring Analysis

### SSO Chunks Performance by Query

Query: **"Does Gupshup Console support Single Sign-On?"**
- SSO chunk top score: 0.850 (Parameters to add on Console)
- Overall winner: 1.200 (Welcome to Gupshup Console)
- Delta: -0.350 (SSO underperforms)

Query: **"What identity providers does Console SSO support?"**
- SSO chunk top score: 0.600 (Overview section)
- Overall winner: 0.600 (Welcome to Gupshup Console)
- Status: Tied but welcome page preferred by evidence selection

Query: **"Can my organization use SAML 2.0 with Console?"**
- SSO chunk top score: 0.600 (Overview with SAML mention)
- Overall winner: 0.600 (Projects & Organizations)
- Status: Tied but generic org page preferred

Query: **"Do I need admin access to set up Console SSO?"**
- SSO chunk top score: 0.650 (Prerequisites section)
- Overall winner: 0.650 (manage-organisation.md console roles)
- Status: Tied, but manage-organisation matched better due to exact "admin" match

Query: **"What certificate formats are accepted for SSO?"**
- SSO chunk top score: 0.300 (Setup path section)
- Overall winner: 0.300 (functions-from-i-l.md)
- Status: Both below effective thresholds

## Successful Query Variations

Tested alternative phrasings to identify queries where SSO document ranks highest:

### "Console SSO configuration" ✓
- SSO chunk top score: 1.050 (Console SSO Integration)
- Overall winner: 1.050 (SSO document itself!)
- **Result:** SSO chunks rank at top

### "How to configure Console SSO" ✓
- SSO chunk top score: 1.050 (Console SSO Integration)
- Overall winner: 1.050 (SSO document itself!)
- **Result:** SSO chunks rank at top

These queries successfully retrieve the SSO documentation, demonstrating that the content is properly indexed and searchable with the right phrasing.

## Root Cause Analysis

### Why the Policy Questions Don't Work

1. **Generic Token Matching:** KB_answer uses keyword/token matching scoring. The queries contain generic terms like "console", "support", "do i need" that match many documents.

2. **Welcome Page Dominance:** The kb/overview/welcome-to-gupshup-console.md page contains generic console references and scores 1.20-1.10 on many "console" queries, beating specialized documents.

3. **Setup Intent:** Queries are classified as "setup" intent, which looks for action-oriented lines. SSO document has minimal action lines in early sections.

4. **Evidence Selection Bias:** For "setup" intent, the scoring algorithm prefers single highest-scoring chunk if it's much higher than action-oriented alternatives. Generic pages score highest.

### Why Some Questions Fail Completely

- **"What identity providers..."**: "providers" token is short/common (< 4 chars after filtering), gets low weight
- **"What certificate formats..."**: "certificate" and "formats" are present but don't match highly; no entity boost
- **"What identity providers..."**: Query normalized to common terms that match many overview pages

## Document Quality Assessment

The Gupshup Console SSO document is:
- ✓ Well-structured with golden v10 marker
- ✓ Properly chunked (12 chunks extracted)
- ✓ Contains all required information
- ✓ Successfully retrieves with optimized queries
- ✗ Not discovered with natural policy question phrasing

## Recommendations

### Short-term: Query Optimization
Rephrase questions to include more specific SSO/SAML terms:
1. "How does Console SSO integration work?" or "Console SSO setup"
2. "Which identity providers work with Console SSO?" (more specific)
3. "Is SAML 2.0 supported by Console?" (more direct)
4. "What admin requirements for Console SSO?" (refocus on SSO context)
5. "What formats for SSO signing certificate?" (more specific)

### Medium-term: Scoring Adjustments
1. **Add SSO module detection**: Detect "sso", "saml", "identity provider" as SSO module query
2. **Boost SSO document**: Add source-specific scoring boost for Gupshup_Console_SSO queries
3. **Policy question intent**: Detect policy/yes-no questions and prefer documentation-focused evidence

### Long-term: Content Structure
1. Create redirect/alias document that mentions SSO features explicitly
2. Add SSO cross-references to admin/organization/security pages
3. Consider adding SSO mentions to welcome/overview pages for better discoverability

## Test Setup Details

- **Document:** kb/Gupshup_Console_SSO support.md
- **Golden Status:** kb-golden:v10 (correctly marked)
- **Chunks Created:** 12
- **Test Date:** 2026-07-09
- **KB Answer Version:** Current
- **Retrieval Method:** kb_answer skill with local chunk loading
