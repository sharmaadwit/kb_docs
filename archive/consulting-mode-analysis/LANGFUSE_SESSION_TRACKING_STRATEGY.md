# Langfuse Session Tracking Strategy
**Date:** 2026-08-14  
**Status:** Ready to implement

---

## 🎯 Objective

Enable proper multi-turn conversation tracking in Langfuse so we can measure:
- How many follow-ups per session (consulting vs standard)?
- Session duration (consulting vs standard)?
- Engagement lift percentage?

---

## 🔍 Current Langfuse Architecture (in kb_answer.py)

### Trace Structure

**File:** skill/kb_answer.py (lines 7258-7286)

```python
def _build_langfuse_request(
    trace_name: str,           # "kb_answer"
    trace_id: str,             # "kb-kb_answer-<uuid>"
    query: str,                # User question
    answer: str,               # Bot answer
    metadata: Dict,            # Custom fields
    trace_user_id: Optional[str] = None,
    parent_trace_id: Optional[str] = None,  # ← KEY FOR MULTI-TURN
) -> Dict:
    # Creates trace with:
    body = {
        "id": trace_id,
        "timestamp": event_timestamp,
        "name": trace_name,
        "input": {"query": query},
        "output": {"answer": answer},
        "metadata": metadata,
        "userId": trace_user_id,          # ← For grouping by user
        "parentTraceId": parent_trace_id,  # ← For conversation chains
    }
```

### Current Metadata (lines 7400-7440)

Already includes:
- ✅ `selected_answer_mode` (consulting vs standard)
- ✅ `correlation_id` (session identifier)
- ✅ `parent_trace_id` (chain link)
- ✅ `is_sub_query` (boolean, derived from parent_trace_id)
- ✅ `module_label` (which module answered)
- ✅ `intent` (query intent)

---

## 📊 Session Tracking: 3 Levels

### Level 1: Trace Hierarchy (Built-in)
**Status:** ✅ Code ready, ❌ Client not using

Uses: `parentTraceId` field

How it works:
```
Query 1: trace_id=ABC, parentTraceId=None
Query 2: trace_id=DEF, parentTraceId=ABC  ← Links to parent
Query 3: trace_id=GHI, parentTraceId=DEF  ← Links to parent

Result: Langfuse shows chain ABC → DEF → GHI
```

**What it enables:**
- Direct conversation chains in Langfuse UI
- Can query: "Show me all traces in chain ABC"
- Can measure: "How many children does each trace have?"

**Action needed:** Client must pass parent_trace_id (SuperAgent team)

---

### Level 2: Session Grouping (Via Metadata)
**Status:** ✅ Code ready, ⏳ Enhancement possible

Uses: `correlation_id` as session marker

How it works:
```
All queries with same correlation_id = same session
Langfuse can group and analyze by this field
```

**Current code (line 7432):**
```python
metadata["correlation_id"] = correlation_id
```

**Enhancement needed:**
Add session metadata to make grouping easier:

```python
# In metadata dict (around line 7432):
metadata["session_id"] = correlation_id  # Explicit session marker
metadata["conversation_turn_number"] = decomposition_level
metadata["estimated_session_start"] = params.get('session_start_time')
```

**What it enables:**
- Group by session_id in Langfuse dashboard
- Filter by conversation_turn_number
- Calculate: "Avg turns per session by consulting mode"

---

### Level 3: Spans/Events (Advanced)
**Status:** ⏳ Possible, but not needed initially

Uses: Langfuse observations API (spans and events)

**What spans are:**
- Nested operations with start/stop time
- Example: span "kb_search" inside trace "kb_answer"
- Good for: measuring latency of sub-operations

**What events are:**
- Point-in-time markers
- Example: "user_typed_followup", "answer_sent"
- Good for: marking conversation milestones

**Current code doesn't use these** (only uses main trace)

**Recommendation:** Skip for now (not needed for session tracking)

---

## 🚀 Implementation Plan

### OPTION A: Fix Client (Level 1 + 2)
**Owner:** SuperAgent team  
**Effort:** 30 minutes  
**Payoff:** Real multi-turn chains

**Steps:**
1. Pass `parent_trace_id` on follow-up queries (Level 1)
2. Pass `session_id` in params (Level 2)

**Result:** Langfuse traces linked in chains + grouped by session

---

### OPTION B: Enhance Skill Code (Level 2 Enhancement)
**Owner:** Us  
**Effort:** 10 minutes  
**Payoff:** Better session visibility

**Changes to skill/kb_answer.py around line 7432:**

```python
# Current:
metadata["correlation_id"] = correlation_id
metadata["parent_trace_id"] = parent_trace_id
metadata["is_sub_query"] = bool(parent_trace_id)

# Add these lines:
metadata["session_id"] = correlation_id  # Explicit session marker
metadata["conversation_turn_number"] = decomposition_level or 0
metadata["trace_sequence"] = f"{correlation_id}:{decomposition_level}"  # For sorting
```

**Why this helps:**
- `session_id`: Direct filter in Langfuse dashboard
- `conversation_turn_number`: Can sort turns chronologically
- `trace_sequence`: Composite key for ordering

---

### OPTION C: Add Conversation Context Span (Level 3)
**Owner:** Us  
**Effort:** 2-3 hours  
**Payoff:** Advanced per-turn analysis

**What this does:**
```python
# Pseudo-code (illustrative):
with lf.trace(
    name="conversation_session",
    id=correlation_id,  # Session ID as trace root
):
    with lf.span(name="turn_1"):
        # First query in session
        kb_answer(query, parent_trace_id=None)
    
    with lf.span(name="turn_2"):
        # Follow-up query
        kb_answer(query, parent_trace_id=prev_trace_id)
```

**Advantage:** Session becomes a container trace, turns are spans inside  
**Disadvantage:** Major refactor, not needed initially

---

## 📋 Recommended: A + B Combination

### Do BOTH:

**1. Request SuperAgent (Option A):**
```
Subject: Multi-turn conversation tracking

Please pass parent_trace_id and session_id when calling kb_answer() for follow-ups:

    response = kb_answer(
        query="follow-up question",
        parent_trace_id="<previous_trace_id>",  # For chain linking
        session_id="<session_id>"               # For grouping
    )

This enables us to measure:
  - Multi-turn conversation chains
  - Session engagement (turns per session)
  - Consulting impact on engagement

Effort: 30 min (capture correlation_id, pass as parent_trace_id)
Timeline: Can this be done before Phase 2 deployment (Aug 18)?
```

**2. Update Skill Code (Option B) - 10 minutes:**

**File:** skill/kb_answer.py  
**Location:** Around line 7432  
**Change:**

```python
# OLD:
metadata["correlation_id"] = correlation_id
metadata["parent_trace_id"] = parent_trace_id
metadata["is_sub_query"] = bool(parent_trace_id)

# NEW (add these 3 lines):
metadata["session_id"] = correlation_id
metadata["conversation_turn_number"] = decomposition_level or 0
metadata["trace_sequence"] = f"{correlation_id}:{decomposition_level or 0}"
```

---

## 🎯 What This Enables (Post-Implementation)

### In Langfuse UI

**With Level 1 (parentTraceId):**
```
Trace ABC
  └─ Trace DEF (parentTraceId=ABC)
       └─ Trace GHI (parentTraceId=DEF)

Can click and follow chain through UI
```

**With Level 2 (session metadata):**
```
Filter traces by: session_id = <value>
Sort by: conversation_turn_number
Group by: selected_answer_mode

Results: Compare consulting vs standard sessions
```

### Queries We Can Run

```sql
-- Number of turns per session, by mode
SELECT session_id, selected_answer_mode, 
       COUNT(*) as turn_count, 
       AVG(confidence) as avg_confidence
FROM traces
GROUP BY session_id, selected_answer_mode

-- Multi-turn lift
SELECT selected_answer_mode,
       AVG(turn_count) as avg_turns_per_session
FROM (
  SELECT session_id, selected_answer_mode,
         COUNT(*) as turn_count
  FROM traces
  GROUP BY session_id, selected_answer_mode
)
GROUP BY selected_answer_mode
-- Expected: consulting > standard by 20%
```

### Dashboard Metrics

Can now measure:
- ✅ Avg turns per session (consulting vs standard)
- ✅ Session duration (consulting vs standard)
- ✅ Multi-turn adoption rate (% sessions with >1 turn)
- ✅ Answer rate improvement by turn (do follow-ups answer better?)
- ✅ Consulting structure impact on engagement

---

## 🔄 Detailed Code Change (Option B)

### File: skill/kb_answer.py

**Location:** Lines 7428-7435 (around `_populate_policy_metadata`)

**Before:**
```python
def _populate_policy_metadata(
    query: str, explicit_module: str, answer_depth: Optional[str],
    intents: List[str], entities: List[Dict], results: List[Dict],
    confidence: float, evidence_text: str,
    selected_answer_mode: str,
    correlation_id: Optional[str] = None,
    parent_trace_id: Optional[str] = None,
) -> Dict:
    metadata = {}
    # ... other fields ...
    metadata["correlation_id"] = correlation_id
    metadata["parent_trace_id"] = parent_trace_id
    metadata["is_sub_query"] = bool(parent_trace_id)
    return metadata
```

**After:**
```python
def _populate_policy_metadata(
    query: str, explicit_module: str, answer_depth: Optional[str],
    intents: List[str], entities: List[Dict], results: List[Dict],
    confidence: float, evidence_text: str,
    selected_answer_mode: str,
    correlation_id: Optional[str] = None,
    parent_trace_id: Optional[str] = None,
    decomposition_level: int = 0,  # Add parameter
) -> Dict:
    metadata = {}
    # ... other fields ...
    metadata["correlation_id"] = correlation_id
    metadata["parent_trace_id"] = parent_trace_id
    metadata["is_sub_query"] = bool(parent_trace_id)
    
    # NEW SESSION TRACKING:
    metadata["session_id"] = correlation_id  # Explicit for grouping
    metadata["conversation_turn_number"] = decomposition_level
    metadata["trace_sequence"] = f"{correlation_id}:{decomposition_level}"
    
    return metadata
```

**Where to call it:** Line 7437, pass `decomposition_level` parameter

---

## 📊 Testing the Implementation

### Immediate (After Code Change)
```bash
# Check traces include new fields
grep '"session_id"' <langfuse_export>.json | head -5

# Expected output:
# {..., "session_id": "abc-123-def", "conversation_turn_number": 0, ...}
# {..., "session_id": "abc-123-def", "conversation_turn_number": 1, ...}
```

### Dashboard (After Client Fix)
1. Go to Langfuse dashboard
2. Filter by: `session_id = <any_value>`
3. Should see 1-5+ traces grouped
4. Verify parentTraceId chains visible
5. Compare: same session shows conversation progression

---

## 🎯 Success Criteria

### Level 1 (Client Implementation)
- [ ] Traces have parentTraceId set (non-null for follow-ups)
- [ ] Langfuse shows conversation chains
- [ ] Can query: "Show traces in chain X"

### Level 2 (Skill Code Enhancement)
- [ ] New fields in metadata: session_id, conversation_turn_number, trace_sequence
- [ ] Traces group by session_id in Langfuse
- [ ] Can sort by conversation_turn_number
- [ ] Can filter by mode and analyze per-session

### Validation (Week 2)
- [ ] Consulting sessions have +20% more turns than standard
- [ ] Session duration +30% longer with consulting
- [ ] Multi-turn adoption higher for consulting (>50% vs <30%)
- [ ] Phase 2 ROI validated with real data

---

## 📝 Langfuse Capabilities Used

| Capability | Used For | Status |
|-----------|----------|--------|
| **trace_id** | Unique query identifier | ✅ Current |
| **parentTraceId** | Link follow-ups to original | ✅ Code ready, ❌ Not used |
| **metadata** | Custom session fields | ✅ Current, enhancing |
| **userId** | Group by user | ✅ Current |
| **input/output** | Query and answer | ✅ Current |
| **Spans/Events** | Sub-operation tracking | ⏳ Not used |

---

## 🔗 Related Changes

**skill/kb_answer.py changes:**
- Line 7432: Add session_id, conversation_turn_number, trace_sequence
- Line 7437: Ensure decomposition_level passed

**Client side (SuperAgent):**
- Capture trace_id from response
- Pass as parent_trace_id on follow-ups
- Pass session_id in params

**No other files affected.**

---

## 🚀 Implementation Timeline

| Date | Action | Owner | Effort | Status |
|------|--------|-------|--------|--------|
| Today (Aug 14) | Request SuperAgent pass parent_trace_id | Us | — | → Ask |
| Today (Aug 14) | Implement Level 2 in skill code | Us | 10 min | → Ready |
| Tomorrow (Aug 15) | SuperAgent confirms feasibility | SuperAgent | 30 min | → Wait |
| Phase 2 (Aug 17) | Deploy with both changes | Us | — | → Ready |
| Week 2 (Aug 21) | Analyze real session data | Us | 2-3 hours | → Validate |

---

## 💡 Why This Works

**Langfuse is designed for exactly this:**
- ✅ parentTraceId for hierarchical traces (built-in)
- ✅ metadata dict for custom session fields
- ✅ userId for user grouping
- ✅ Filtering and aggregation on any field

**We're using standard Langfuse patterns:**
- Not hacking around limitations
- Not creating custom session tracking
- Just enabling built-in features

**Result:** Professional conversation analytics visible in Langfuse UI + API

---

**Status:** Ready to implement. Awaiting SuperAgent team approval on parent_trace_id passing.

