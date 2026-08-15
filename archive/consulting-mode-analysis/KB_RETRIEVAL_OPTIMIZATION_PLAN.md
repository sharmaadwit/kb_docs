# KB Retrieval Optimization Plan
**Date:** 2026-08-13  
**Status:** Initial Analysis Complete  
**Method:** Live SuperAgent microagent endpoint testing

---

## Test Results Summary

**Tested 3 critical queries against live KB retrieval:**

| Query | Result | Status | Issue |
|-------|--------|--------|-------|
| "prevent infinite loops in Bot Studio" | 5,112 chars | ✅ GOOD | Relevant content retrieved |
| "conditional branching to route users" | 2,754 chars | ❌ POOR | Generic fallback instead of KB |
| "handle complex multi-turn conversations" | 6,670 chars | ❌ POOR | Generic fallback instead of KB |

**Overall:** 1/3 good, 2/3 poor retrieval (33% success rate on critical queries)

---

## Root Cause Analysis

### Query 1: "prevent infinite loops" ✅
- **Why it works:** Bot Studio content includes loop prevention documentation
- **Evidence:** Correct content retrieved with relevant keywords
- **Confidence:** High

### Query 2: "conditional branching" ❌
- **What happened:** SuperAgent fell back to generic "planning tool actions" answer
- **Root cause:** One of:
  1. **KB missing:** Conditional branching documentation doesn't exist or is incomplete
  2. **Retrieval gap:** Chunks exist but weren't ranked high enough
  3. **Semantic mismatch:** Query terms don't match chunk language/titles
  4. **Chunking issue:** Chunks are too broad or lack semantic markers

**Supporting evidence:** Earlier Phase 1 traces showed same wrong answer ("HTTP Status Code Branching" instead of conditional routing)

### Query 3: "multi-turn conversations" ❌
- **What happened:** Generic Gupshup advice instead of state management patterns
- **Root cause:** Likely same as Query 2 — missing KB content or retrieval gap

---

## KB Optimization Checklist

### Phase 1: KB Content Audit

- [ ] **Check Bot Studio content exists for:**
  - [ ] Conditional routing / decision nodes
  - [ ] Multi-turn state management
  - [ ] Complex journey patterns
  - [ ] Loop prevention (already working ✅)

- [ ] **Commands to run:**
  ```bash
  # Search KB for conditional routing content
  grep -r "conditional\|decision\|branching" kb/kb_chunks.jsonl | wc -l
  
  # Search for multi-turn patterns
  grep -r "multi-turn\|state\|session" kb/kb_chunks.jsonl | wc -l
  
  # Check what Bot Studio chunks exist
  grep "bot studio\|journey" kb/kb_chunks.jsonl | grep -i "conditional\|routing" | head -5
  ```

### Phase 2: Retrieval Ranking Analysis

- [ ] **Check retrieval ranking algorithm:**
  - BM25 score weight
  - Embedding similarity threshold
  - Recency/freshness weighting
  - Metadata field matching

- [ ] **Test query reformulations:**
  ```
  Original: "How do I use conditional branching..."
  Variants:
    - "conditional logic in Bot Studio"
    - "decision node routing"
    - "route users based on conditions"
    - "branch journey with if-then"
  ```

- [ ] **Evaluate chunk overlap:**
  - Are multiple chunks covering the same content?
  - Is primary/authoritative chunk ranked first?
  - Are synonyms properly indexed?

### Phase 3: Semantic Enhancement

- [ ] **Add semantic metadata to chunks:**
  - Primary topic keywords (e.g., "conditional routing", "decision node")
  - Intent tags (e.g., "howto", "pattern", "best-practice")
  - Related topics (cross-references)
  - Synonyms (e.g., "branching", "routing", "conditional logic")

- [ ] **Review chunk titles:**
  - Are they descriptive enough for search?
  - Do they contain keywords from common queries?
  - Example: "Conditional Routing in Bot Studio Journeys" vs "Step 2: Enable Status Code Branching"

- [ ] **Check chunk boundaries:**
  - Are chunks too large (multiple concepts)?
  - Are chunks too small (incomplete explanation)?
  - Should similar content be merged?

### Phase 4: Re-Testing

- [ ] **Run retrieval test again:**
  ```bash
  python3 local/scripts/test_kb_retrieval_live.py
  ```

- [ ] **Add more test queries:**
  - "journey builder patterns"
  - "state management in journeys"
  - "error handling in Bot Studio"
  - "webhook integration patterns"

- [ ] **Monitor Phase 1 traces:**
  - Check if consulting-tone traces improve after KB fixes
  - Compare accuracy before/after for same queries
  - Use Langfuse filtering: `module = "Bot Studio" AND intent = "setup"`

---

## Quick Investigation Commands

**Run these to understand current KB state:**

```bash
# 1. Count total Bot Studio chunks
grep -i "bot studio" kb/kb_chunks.jsonl | wc -l

# 2. Find conditional/routing content
grep -i "conditional\|decision\|branching\|routing" kb/kb_chunks.jsonl | head -10

# 3. Find multi-turn/state content
grep -i "multi-turn\|session\|state\|memory" kb/kb_chunks.jsonl | head -10

# 4. See chunk structure (first chunk example)
head -1 kb/kb_chunks.jsonl | jq '.' | head -30

# 5. Count chunks by source file
jq '.source' kb/kb_chunks.jsonl | sort | uniq -c | sort -rn
```

---

## Recommendation: Priority Order

### Immediate (Today)
1. **Run KB content audit** — Confirm what content exists for conditional routing
2. **Check retrieval logs** — See what scores/rankings were assigned to candidates
3. **Test query variants** — Try synonym-based queries to isolate search issue

### Short-term (This Week)
1. **Add metadata** to existing chunks if content exists
2. **Refactor chunk boundaries** if chunks are poorly split
3. **Re-test** with live endpoint
4. **Monitor Langfuse** for accuracy changes

### Medium-term (If needed)
1. **Create new content** if Bot Studio conditional routing docs are missing
2. **Enhance KB embeddings** if semantic search not working
3. **Tune BM25 weights** if keyword search needs calibration

---

## Success Metrics

After optimization, target:
- ✅ **All 3 test queries:** Good/Partial relevance (≥60% keyword match)
- ✅ **Phase 1 traces:** Improved answer accuracy for Bot Studio queries
- ✅ **Langfuse dashboard:** +5-10pp accuracy lift for "conditional routing" intent

---

## Files & Scripts

**Test script:** `local/scripts/test_kb_retrieval_live.py`
```bash
python3 local/scripts/test_kb_retrieval_live.py
```

**Results:** `local/reports/kb_retrieval_test_results.json`

**Next test run:** After KB adjustments

---

## Next Step

**Run the KB audit commands above** to understand what content currently exists. Once we know the baseline, we can decide whether to:
1. Enhance existing chunks with better metadata
2. Refactor chunk boundaries
3. Create new content
4. Tune retrieval ranking

Share the results and I'll create a targeted optimization plan.
