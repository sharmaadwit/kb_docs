# Skill Enhancement Spec: Case Studies & Demo Routing

**Date:** 2026-06-07  
**Priority:** High  
**Impact:** Enables sales/non-technical users to discover customer success stories and demos  
**Context:** Analytics revealed 10+ IDK queries (15% of IDK) are asking for success stories/demos that exist but aren't discoverable via KB agent

---

## Overview

Integrate case studies module (`kb/case-studies/`) into the KB answer pipeline so queries asking for demos, success stories, and customer examples route to case study docs and return relevant industry-specific content.

Currently:
- 94 case study markdown files exist (organized by industry)
- Case studies have structured metadata (company, industry, headline, confidentiality)
- But KB agent has NO routing logic for "demo", "success story", "case study" queries
- These queries fail with IDK (29.9% IDK rate on 7-day data)

After:
- Queries like "show me retail success stories" → surface relevant case studies
- "demo for hotel industry" → return Travel & Hospitality case studies
- Video attach rate will improve as case study queries get matched docs

---

## Implementation Tasks

### Task 1: Add Case Study Routing Logic in `skill/kb_answer.py`

**File:** `skill/kb_answer.py`

**Objective:** Detect case-study-related queries and route them to `kb/case-studies/` folder instead of regular KB search.

**Location in code:** Add new function in the `_answer_from_kb` pipeline, called BEFORE the standard TF-IDF search. This should be a gate that detects intent early.

**Implementation:**

```python
def _is_case_study_query(query: str) -> bool:
    """
    Detect if query is asking for demos, success stories, case studies, or customer examples.
    Returns True if query should be routed to case-studies folder.
    """
    case_study_keywords = [
        "demo", "walkthrough", "customer story", "success story", "case study",
        "customer example", "customer win", "customer reference", "show me",
        "what can.*do for", "how has.*helped", "customer use case",
        "customer success", "client example", "brand example", "customer reference",
        "customer examples", "use cases", "real world"
    ]
    
    query_lower = query.lower()
    
    # Check for case study keywords
    keyword_match = any(re.search(kw, query_lower) for kw in case_study_keywords)
    
    # Also check for industry keywords that often appear with case study queries
    # (these boost confidence if case_study keyword found)
    industry_keywords = [
        "retail", "cpg", "e-commerce", "finance", "financial", "bank", "insurance",
        "travel", "hospitality", "hotel", "restaurant", "food", "education",
        "healthcare", "automotive", "automobile", "telecom", "government",
        "ride-hailing", "beverage", "beauty", "fashion", "d2c"
    ]
    industry_match = any(ind in query_lower for ind in industry_keywords)
    
    # Return True if we found case study keywords + optionally industry context
    return keyword_match
```

**Where to place:** Add before line ~XXX where `_score_chunk` is called. Suggest adding around the `_answer_from_kb` function, as an early gate.

**Integration point:** 
```python
# Existing code flow (approx):
def _answer_from_kb(query, module_label, ...):
    # NEW: Add this check
    if _is_case_study_query(query):
        return _answer_from_case_studies(query, module_label)
    
    # Existing flow continues
    chunks = kb_search(query, ...)
    ...
```

**Function: `_answer_from_case_studies`**

```python
def _answer_from_case_studies(query: str, module_label: str = None) -> dict:
    """
    Search case studies by industry/company/headline and return matches.
    
    Args:
        query: User question
        module_label: Detected module (e.g., "Retail", "Finance") - optional
    
    Returns:
        {
            "answered": True,
            "answer": "Here are relevant case studies...",
            "sources": [list of case study markdown files],
            "case_studies": [list of matched records from _manifest.json],
            "confidence": float (0-10)
        }
    """
    # 1. Load case studies manifest
    manifest_path = Path("kb/case-studies/_manifest.json")
    with open(manifest_path) as f:
        case_studies = json.load(f)
    
    # 2. Extract industry from query if present
    # Use simple keyword matching or NLP to detect industry
    detected_industry = _detect_industry_from_query(query)
    
    # 3. Filter case studies by industry (if detected)
    if detected_industry:
        filtered = [cs for cs in case_studies if cs["industry"].lower() == detected_industry.lower()]
    else:
        filtered = case_studies
    
    # 4. Rank by headline relevance (simple keyword matching)
    scored = _score_case_studies(query, filtered)
    
    # 5. Format answer
    top_matches = scored[:5]  # Return top 5 case studies
    
    if not top_matches:
        return {
            "answered": False,
            "answer": "I don't have case studies matching your query.",
            "sources": []
        }
    
    # Build markdown answer with case study links
    answer_md = f"Here are relevant customer success stories:\n\n"
    for cs in top_matches:
        answer_md += f"- **{cs['company']}** ({cs['industry']}): {cs['headline']}\n"
    
    return {
        "answered": True,
        "answer": answer_md,
        "sources": [f"kb/case-studies/{cs['file']}" for cs in top_matches],
        "case_studies": top_matches,
        "confidence": 8.5  # Case studies are high-confidence when matched
    }
```

**Helper functions needed:**

```python
def _detect_industry_from_query(query: str) -> Optional[str]:
    """
    Extract industry keyword from query.
    Maps query text to case study industries.
    """
    industry_map = {
        "retail|e-commerce|fashion|d2c|store": "Retail & D2C",
        "cpg|beverage|consumer goods|fmcg": "CPG",
        "finance|bank|financial|insurance": "Financial Services",
        "travel|hotel|hospitality|restaurant": "Travel & Hospitality",
        "education|edtech|school|university": "Education",
        "healthcare|hospital|medical": "Healthcare",
        "auto|automotive|car|vehicle": "Automotive",
        "telecom|mobile|network": "Telecom",
        "ride|ride-hailing|uber|taxi": "Ride Hailing",
        "government|public sector": "Government",
        "entertainment|sports|media": "Entertainment"
    }
    
    query_lower = query.lower()
    for pattern, industry in industry_map.items():
        if re.search(pattern, query_lower):
            return industry
    
    return None

def _score_case_studies(query: str, candidates: list) -> list:
    """
    Score case studies by relevance to query.
    Simple keyword matching on headline + company.
    """
    scored = []
    query_words = set(query.lower().split())
    
    for cs in candidates:
        text = (cs.get("headline", "") + " " + cs.get("company", "")).lower()
        matches = sum(1 for word in query_words if word in text)
        score = matches / len(query_words) if query_words else 0
        scored.append((cs, score))
    
    # Sort by score descending, keep non-confidential first
    scored.sort(key=lambda x: (-x[1], x[0].get("confidential", False)))
    
    return [cs for cs, _ in scored]
```

---

### Task 2: Boost Concept Registry for Industry Keywords

**File:** `skill/kb_answer.py`

**Objective:** Ensure case study queries get proper module classification and scoring via concept registry.

**Current situation:** Concept registry likely has boosts for product terms (e.g., "bot studio", "agent assist") but not for industry/vertical terms that appear in case study queries.

**Implementation:**

Add/update the concept registry to include industry boost patterns:

```python
# In kb_answer.py, find CONCEPT_REGISTRY or similar section
# Add these patterns:

INDUSTRY_CONCEPTS = {
    "Retail & D2C": {
        "keywords": ["retail", "e-commerce", "ecommerce", "fashion", "apparel", "d2c", "online store", "shopping"],
        "boost": 2.5,
        "module": "Overview"  # Case studies are platform-wide
    },
    "CPG": {
        "keywords": ["cpg", "consumer goods", "fmcg", "beverage", "food", "brand"],
        "boost": 2.5,
        "module": "Overview"
    },
    "Financial Services": {
        "keywords": ["bank", "banking", "finance", "financial", "insurance", "fintech", "investment"],
        "boost": 2.5,
        "module": "Overview"
    },
    "Travel & Hospitality": {
        "keywords": ["hotel", "travel", "hospitality", "airline", "tourism", "resort"],
        "boost": 2.5,
        "module": "Overview"
    },
    "Healthcare": {
        "keywords": ["healthcare", "hospital", "medical", "clinic", "health"],
        "boost": 2.5,
        "module": "Overview"
    },
    "Automotive": {
        "keywords": ["auto", "automotive", "car", "vehicle", "automobile", "dealership"],
        "boost": 2.5,
        "module": "Overview"
    },
    "Education": {
        "keywords": ["education", "school", "university", "edtech", "student", "learning"],
        "boost": 2.5,
        "module": "Overview"
    },
}

def _apply_industry_boosts(scored_chunks: list, query: str) -> list:
    """
    Boost scores for chunks if query contains industry keywords.
    This helps case study queries rank higher when industry is mentioned.
    """
    query_lower = query.lower()
    
    boosted = []
    for chunk_record in scored_chunks:
        chunk_text = (chunk_record.get("text", "") + chunk_record.get("title", "")).lower()
        score = chunk_record.get("score", 0)
        
        # Check each industry pattern
        for industry, concept in INDUSTRY_CONCEPTS.items():
            # If query has industry keyword AND chunk is case study or industry-related
            industry_in_query = any(kw in query_lower for kw in concept["keywords"])
            industry_in_chunk = any(kw in chunk_text for kw in concept["keywords"])
            
            if industry_in_query:
                # Boost case study chunks significantly
                if "case-studies" in chunk_record.get("source", ""):
                    score *= concept["boost"]
                # Also boost industry-specific product docs
                elif industry_in_chunk:
                    score *= 1.5
        
        boosted.append({**chunk_record, "score": score})
    
    return sorted(boosted, key=lambda x: -x["score"])
```

**Where to call:** In `_answer_from_kb`, after `_score_chunk` and before the gate check:

```python
# Existing code:
scored_chunks = [_score_chunk(chunk, query, ...) for chunk in chunks]

# NEW: Add this
scored_chunks = _apply_industry_boosts(scored_chunks, query)

# Then continue with gate
if not _has_explicit_support(scored_chunks):
    return {"answered": False, ...}
```

---

### Task 3: Add Intent Detection for Case Study Queries

**File:** `skill/kb_answer.py` and `skill/SKILL.md`

**Objective:** Classify case study queries with new intent type so they're handled differently (surfaced prominently for sales users, etc.).

**Implementation in kb_answer.py:**

```python
def _detect_intent(query: str) -> str:
    """
    Detect query intent. Returns one of:
    - 'setup', 'overview', 'definition', 'schema', 'troubleshooting'
    - 'sales_pitch' (NEW) - for demo/case study requests
    - 'case_study_lookup' (NEW) - explicit case study search
    """
    query_lower = query.lower()
    
    # NEW: Case study intents
    case_study_keywords = {
        "sales_pitch": ["show me", "demo", "customer example", "what can.*do for", "help.*industry", "use case"],
        "case_study_lookup": ["case study", "success story", "customer story", "customer win", "client reference"]
    }
    
    for intent, keywords in case_study_keywords.items():
        if any(re.search(kw, query_lower) for kw in keywords):
            return intent
    
    # Existing intent detection
    if re.search(r"how.*setup|how.*install|how.*get.*start|configure|onboard", query_lower):
        return "setup"
    elif re.search(r"what is|explain|overview|tell me about|define", query_lower):
        return "overview"
    # ... rest of existing logic
    
    return "overview"  # default
```

**Update SKILL.md:**

In the system prompt, add guidance for case study queries:

```markdown
## Case Study Queries (NEW)

When user asks for:
- "Show me demos" / "customer examples" / "success stories" → Intent: sales_pitch
- Explicit "case study" requests → Intent: case_study_lookup

For these queries:
1. Search kb/case-studies/ by industry
2. Return company name + headline + brief context
3. Offer to share full case study docs (kb/case-studies/{filename}.md)
4. If available, attach demo/walkthrough videos

Example response:
"Here are relevant customer success stories for your industry:

**Company A** (Retail & D2C): Grew sales 30% YoY with personalized WhatsApp campaigns
**Company B** (Retail & D2C): Achieved 4X ROAS with Click-to-WhatsApp ads

Would you like the full case study for Company A?"
```

---

## Testing & Validation

### Pre-deployment Checklist

1. **Unit tests** for new functions:
   - `_is_case_study_query()` — test with demo/success story/case study queries
   - `_detect_industry_from_query()` — test industry detection (retail, cpg, finance, etc.)
   - `_score_case_studies()` — test ranking by headline relevance

2. **Regression harness** (`local/scripts/idk_regression.py`):
   Add these test queries to the harness:
   
   ```python
   # Case study queries
   {
       "id": "cs_1",
       "query": "Show me retail success stories with WhatsApp",
       "expected_module": "Overview",
       "expected_answer_mode": "case_study_lookup",
       "should_have_sources": True
   },
   {
       "id": "cs_2",
       "query": "What can Gupshup do for a hotel chain? Show me examples.",
       "expected_module": "Overview",
       "expected_answer_mode": "sales_pitch",
       "should_have_sources": True
   },
   {
       "id": "cs_3",
       "query": "CPG case studies - how have brands used Gupshup?",
       "expected_module": "Overview",
       "expected_answer_mode": "case_study_lookup",
       "should_return_industry": "CPG"
   }
   ```

3. **Manual spot checks:**
   - Run: `"retail customer success story WhatsApp campaign"` → should surface Retail & D2C cases
   - Run: `"financial services demo"` → should surface Financial Services cases
   - Run: `"show me a demo of gupshup and its features"` → should trigger case study routing

4. **Regression target:** Maintain ≥22/26 on existing curated set (from `local/scripts/idk_regression.py`)

### Expected Improvements

From the 7-day IDK analysis:
- **13 demo requests** currently failing → should be answered
- **10 success story requests** currently failing → should be answered
- Overall IDK rate could drop 1-2 percentage points if case studies are indexed well

---

## Files to Modify

| File | Changes | Priority |
|------|---------|----------|
| `skill/kb_answer.py` | Add case study routing, industry boosts, intent detection | High |
| `skill/SKILL.md` | Add section on case study response format | Medium |
| `local/scripts/idk_regression.py` | Add case study test queries | High |

---

## Notes for Coder

1. **Case studies are already indexed:** `kb/case-studies/_manifest.json` is your source of truth. No need to rebuild chunks.

2. **Confidentiality:** Some cases are marked `"confidential": true` — your code should handle this (return them but note they're confidential, or filter them based on a setting).

3. **Industry matching is fuzzy:** The current implementation uses simple keyword matching. If you want better accuracy, consider:
   - Loading industry list from manifest once (cache it)
   - Using more robust NLP or fuzzy matching for industry detection

4. **Integration with existing gates:** 
   - Case study queries should probably bypass the `_has_explicit_support` gate (they're inherently high-confidence if manifesto has matches)
   - Or create a separate gate: `_has_explicit_case_studies()`

5. **Performance:** Case studies folder has only 94 files, so linear search is fine. But manifest.json should be loaded once at startup (not per query).

---

## Success Criteria

✅ When deployed, these queries should be ANSWERED (not IDK):

1. "show me retail success stories with WhatsApp" → Return 3-5 Retail case studies
2. "demo for hotel industry" → Return Travel & Hospitality case studies
3. "case studies or demos for CPG brands" → Return CPG case studies
4. "What can Gupshup do for my financial services company?" → Return Finance case studies + brief product overview

✅ All existing regression tests still pass (≥22/26)

✅ Video attach rate stays ≥35% (currently 38.2%)

---

## Questions for Author

Before starting, clarify with Adwit:
- Should confidential case studies be returned? (suggested: yes, with flag)
- Is there a preferred NLP library for industry detection, or keep it simple regex?
- Should case study routing bypass all gates, or apply some validation?
