# Skill Code Change: Add Concept Boosts for Quick Win IDK Fixes

**File:** `skill/kb_answer.py`  
**Section:** CONCEPT_REGISTRY (lines 225-2134)  
**Change Type:** ADD 3 new concept entries  
**Difficulty:** Easy (copy-paste with minor adjustments)  
**Impact:** Fix 2-3 remaining IDK queries  

---

## What to Change

### Location
- **File:** `skill/kb_answer.py`
- **Line:** 2133 (before the closing `]`)
- **Context:** Right before the final `]` that closes CONCEPT_REGISTRY

### Current Code (lines 2118-2134)
```python
    {
        "id": "campaign_creation",
        "aliases": [
            "create campaign", "campaign creation", "new campaign",
            "start campaign", "first campaign", "campaign manager setup",
            "creating your first campaign",
        ],
        "keywords": ["campaign", "create", "creation", "first"],
        "source_boosts": {
            "creating-your-first-campaign.md": 3.0,
        },
        "source_penalties": {},
        "display": "Creating Your First Campaign",
        "page_display": "Creating Your First Campaign",
        "module": "Campaign Manager",
    },
]
```

### New Code to Insert (before the `]`)
Replace the closing `]` with these 3 new concept entries, then the `]`:

```python
    {
        "id": "campaign_creation",
        "aliases": [
            "create campaign", "campaign creation", "new campaign",
            "start campaign", "first campaign", "campaign manager setup",
            "creating your first campaign",
        ],
        "keywords": ["campaign", "create", "creation", "first"],
        "source_boosts": {
            "creating-your-first-campaign.md": 3.0,
        },
        "source_penalties": {},
        "display": "Creating Your First Campaign",
        "page_display": "Creating Your First Campaign",
        "module": "Campaign Manager",
    },
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
        "page_display": "Downloading and Exporting Leads/Customer Data",
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
        "page_display": "Custom Integrations & Webhooks",
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
        "page_display": "Sticky Chat / Assignment Enhancement",
        "module": "Agent Assist",
    },
]
```

---

## Detailed Breakdown

### Concept 1: `leads_export`
**Purpose:** Fix "How to download leads from Gupshup Console"

**Aliases:** (9 variations to catch different phrasings)
- "download leads"
- "export leads"
- "lead download"
- "lead export"
- "download customer leads"
- "export customer data"
- "leads data"
- "customer data export"
- "leads export"

**Keywords:** ["leads", "download", "export", "data", "csv"]

**Boosts:**
- `exploring-insights-and-exporting-raw-data.md`: 4.0 (primary doc)
- `downloading-chat-transcripts-for-customer-conversations.md`: 2.5 (secondary)

**Module:** Agent Assist

---

### Concept 2: `custom_integrations`
**Purpose:** Fix "What is Custom Integrations in Gupshup Console?"

**Aliases:** (5 variations)
- "custom integrations"
- "custom connector"
- "custom integration setup"
- "create custom integration"
- "webhook integration"
- "external integration"

**Keywords:** ["custom", "integrations", "connector", "webhook", "external"]

**Boosts:**
- `custom-integrations.md`: 4.5 (primary doc, primary purpose)
- `manage-api.md`: 2.0 (secondary, API integration)

**Module:** Integrations

---

### Concept 3: `sticky_assignment`
**Purpose:** Fix "What is sticky chat in Agent Assist?" (sticky chat = sticky assignment)

**Aliases:** (7 variations)
- "sticky chat"
- "sticky assignment"
- "sticky conversation"
- "persistent assignment"
- "chat assignment"
- "persistent chat"
- "reassign sticky"
- "sticky team assignment"

**Keywords:** ["sticky", "assignment", "chat", "persistent", "assignment rules"]

**Boosts:**
- `assignment-enhancements-in-console-7-0.md`: 4.0 (contains sticky assignment info)

**Module:** Agent Assist

---

## Testing After Implementation

### Test these 3 queries to verify the fix:

```bash
# After deploying the code change:

# Test 1: Download Leads
echo "Query: How to download leads from Gupshup Console"
# Expected: Returns exploring-insights-and-exporting-raw-data.md with high confidence

# Test 2: Custom Integrations  
echo "Query: What is Custom Integrations in Gupshup Console?"
# Expected: Returns custom-integrations.md content

# Test 3: Sticky Chat
echo "Query: What is sticky chat in Agent Assist?"
# Expected: Returns assignment-enhancements-in-console-7-0.md with sticky assignment content
```

### Run the comprehensive test:
```bash
python3 local/test_10_queries.py
# Should show all 10 queries passing (or at least these 3 fixed)
```

---

## Checklist Before Committing

- [ ] All 3 concept entries added to CONCEPT_REGISTRY
- [ ] Correct indentation (4 spaces, matching other entries)
- [ ] All closing braces/brackets are correct
- [ ] No missing commas between entries
- [ ] Module names match existing KB modules (Agent Assist, Integrations)
- [ ] `source_boosts` values are in reasonable range (2.0-5.0)
- [ ] File syntax is valid Python (no syntax errors)
- [ ] Tested the 3 queries mentioned above
- [ ] No regressions on baseline queries (Q1-Q5, Q10)

---

## Rollback Plan

If any test query breaks:

1. Revert the 3 new concept entries
2. Keep the CONCEPT_REGISTRY structure intact
3. Re-run tests to verify baseline is restored
4. Identify which specific concept caused the issue
5. Adjust that concept's aliases or boost values

---

## Expected Results After Deployment

| Metric | Before | After | Status |
|--------|--------|-------|--------|
| **IDK Rate** | 44.4% (16/36) | ~42% (15/36) | -1-2 IDK responses |
| **Answer Rate** | 55.6% (20/36) | ~58% (21/36) | +1-2 answered |
| **Q: Download Leads** | ❌ IDK | ✅ Answered | FIXED |
| **Q: Custom Integrations** | ❌ IDK | ✅ Answered | FIXED |
| **Q: Sticky Chat** | ❌ IDK | ✅ Answered | FIXED |

---

## Notes

- These are **additive changes** (only adding new concepts, no threshold modifications)
- **Low risk:** Similar structure to Q7, Q8, Q9 concepts already deployed
- **No other files** need to be modified
- The concept boosts work by making kb_search return higher-scoring results for these queries
- If a query still fails after this, it's likely a different root cause (e.g., document content issue)

