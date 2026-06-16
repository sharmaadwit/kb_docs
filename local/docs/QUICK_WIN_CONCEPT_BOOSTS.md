# Quick Win: Concept Registry Boosts for IDK Fixes
**Priority:** HIGH  
**Effort:** LOW (5 lines of Python)  
**Expected Impact:** Fix 2-3 remaining IDK queries  
**Target File:** `skill/kb_answer.py` (CONCEPT_REGISTRY section, around line 2100+)

---

## Problem

Three remaining IDK queries can be fixed by adding concept registry boosts to the CONCEPT_REGISTRY list in kb_answer.py:

1. **Query:** "How to download leads from Gupshup Console"
   - **Doc exists:** `exploring-insights-and-exporting-raw-data.md` ✅
   - **Issue:** Keyword mismatch ("leads" vs "export/download")
   - **Fix:** Add concept boost

2. **Query:** "What is Custom Integrations in Gupshup Console?"
   - **Doc exists:** `custom-integrations.md` ✅
   - **Issue:** Low kb_search score or missing concept
   - **Fix:** Add explicit concept boost

3. **Query:** "What is sticky chat in Agent Assist?"
   - **Doc exists:** `assignment-enhancements-in-console-7-0.md` ✅ (sticky assignment)
   - **Issue:** Terminology mismatch ("sticky chat" vs "sticky assignment")
   - **Fix:** Add concept with aliases

---

## Implementation

### Step 1: Locate CONCEPT_REGISTRY

File: `skill/kb_answer.py`  
Search for: `CONCEPT_REGISTRY: List[Dict] = [`  
Current section ends around line 2150 (after recent fixes)

### Step 2: Add Three New Concept Entries

Add these 3 entries to the CONCEPT_REGISTRY list before the closing `]`:

```python
{
    "id": "leads_export",
    "aliases": [
        "download leads", "export leads", "lead download",
        "lead export", "download customer leads", "export customer data",
        "leads data", "customer data export", "leads export"
    ],
    "keywords": ["leads", "download", "export", "data", "csv"],
    "source_boosts": {
        "exploring-insights-and-exporting-raw-data.md": 4.0,
        "downloading-chat-transcripts-for-customer-conversations.md": 2.5,
    },
    "source_penalties": {},
    "display": "Downloading and Exporting Leads/Customer Data",
    "module": "Agent Assist",
},
{
    "id": "custom_integrations",
    "aliases": [
        "custom integrations", "custom connector", "custom integration setup",
        "create custom integration", "webhook integration", "external integration"
    ],
    "keywords": ["custom", "integrations", "connector", "webhook", "external"],
    "source_boosts": {
        "custom-integrations.md": 4.5,
        "manage-api.md": 2.0,
    },
    "source_penalties": {},
    "display": "Custom Integrations & Webhooks",
    "module": "Integrations",
},
{
    "id": "sticky_assignment",
    "aliases": [
        "sticky chat", "sticky assignment", "sticky conversation",
        "persistent assignment", "chat assignment", "persistent chat",
        "reassign sticky", "sticky team assignment"
    ],
    "keywords": ["sticky", "assignment", "chat", "persistent", "assignment rules"],
    "source_boosts": {
        "assignment-enhancements-in-console-7-0.md": 4.0,
    },
    "source_penalties": {},
    "display": "Sticky Chat / Assignment Enhancement",
    "module": "Agent Assist",
},
```

---

## Testing

After adding these concepts:

1. **Test Query 1:** "How to download leads from Gupshup Console"
   - Expected: Returns `exploring-insights-and-exporting-raw-data.md` with high confidence
   - Verify: Run `python3 local/test_10_queries.py` (modify to add this query)

2. **Test Query 2:** "What is Custom Integrations in Gupshup Console?"
   - Expected: Returns `custom-integrations.md` content
   - Verify: Should be answerable now

3. **Test Query 3:** "What is sticky chat in Agent Assist?"
   - Expected: Returns `assignment-enhancements-in-console-7-0.md`
   - Verify: Should match on "sticky chat" alias

---

## Validation Checklist

Before considering this complete:

- [ ] All three concept entries added to CONCEPT_REGISTRY
- [ ] Proper indentation and syntax (matches existing entries)
- [ ] `source_boosts` values are reasonable (typically 2.0-5.0)
- [ ] Aliases are comprehensive and realistic
- [ ] Module labels match actual KB modules
- [ ] Test the 3 queries mentioned above
- [ ] Verify no other IDK queries are broken by the changes

---

## Expected Outcome

✅ 2-3 additional IDK queries converted to ANSWERED  
✅ Answer rate improves from 55.6% → ~60%+  
✅ No new regressions (concept boosts are additive)

---

## Files Involved

**To modify:**
- `skill/kb_answer.py` (CONCEPT_REGISTRY, lines ~2100-2150)

**To test:**
- `local/test_10_queries.py` (add 3 test queries)
- `python3 local/scripts/analyze_all_recent.py` (verify in Langfuse)

**No other files need changes.**

---

## Notes

- These are pure concept registry additions (no threshold changes)
- Low risk: Similar to the Q7, Q8, Q9 concept boosts already added
- Can be deployed immediately after testing
- If any query performs worse after this, it's due to the alias matching — easily revertable

