# Langfuse Channel Instrumentation Spec

**For:** Skill code change agent  
**Purpose:** Ensure all KB queries are properly tagged with channel_type in Langfuse  
**Priority:** Medium (improves analytics, no user-facing impact)

---

## 🎯 Objective

Update Langfuse telemetry instrumentation to **reliably capture and report channel_type metadata** for all KB queries, enabling proper multi-channel analytics.

**Current state:** Channel detection works but is ad-hoc (called during telemetry send)  
**Desired state:** Channel detection is systematic and guaranteed for every query

---

## 📋 Requirements

### 1. Capture Channel at Query Time (Not Telemetry Time)

**Current flow:**
```
User query
  ↓
KB answer logic (no channel captured)
  ↓
Build telemetry object
  ↓
Detect channel (via _detect_channel_type)
  ↓
Send to Langfuse
```

**Desired flow:**
```
User query
  ↓
Detect channel from query context/source
  ↓
KB answer logic (channel available throughout)
  ↓
Build telemetry object (with channel already known)
  ↓
Send to Langfuse (channel guaranteed in metadata)
```

### 2. Channel Detection Requirements

The detection should handle:

| Source Type | Should Detect As | Example |
|-------------|------------------|---------|
| `kb/channels/rcs-*.md` | `"rcs"` | kb/channels/rcs-authentication.md |
| `kb/channels/*whatsapp*` | `"whatsapp"` | kb/channels/whatsapp-flows.md |
| `kb/channels/*instagram*` | `"instagram"` | kb/channels/instagram-catalog.md |
| `kb/channels/*web*` | `"web"` | kb/channels/web-widget.md |
| `kb/channels/sms*` | `"sms"` | kb/channels/sms-templates.md |
| Other `kb/channels/*` | `"channels_other"` | kb/channels/channel-types.md |
| All other sources | `"whatsapp"` | kb/bot-studio/*, kb/agent-assist/* |

### 3. Langfuse Metadata Structure

Every KB answer trace **MUST** include:

```json
{
  "metadata": {
    "channel_type": "whatsapp",  // or "rcs", "instagram", "web", "sms", etc.
    "module_label": "Bot Studio",
    "selected_answer_mode": "setup",
    "top_source": "kb/bot-studio/journeys.md",
    "answer": "...",
    "confidence": 7.5,
    "latency_ms": 450,
    // ... other existing fields
  }
}
```

**Critical:** `channel_type` field must **always be present** and **never be null/None**.

---

## 🔧 Implementation Tasks

### Task 1: Update `kb_answer()` Main Function

**What:** Detect channel early in the answer flow  
**Where:** In `kb_answer()`, right after retrieving `top_source`

**Pseudo-code:**
```python
def kb_answer(query, context=None, params=None):
    # ... existing logic to find answer and top_source ...
    
    # NEW: Detect channel from top_source
    detected_channel = _detect_channel_type(top_source)
    
    # Store in result so it's available for telemetry
    answer_metadata = {
        "channel_type": detected_channel,
        "top_source": top_source,
        # ... other metadata
    }
    
    # ... rest of function ...
    
    # When sending to Langfuse, use this metadata
    _send_langfuse(..., metadata=answer_metadata, ...)
```

### Task 2: Update `_send_langfuse()` Function

**What:** Ensure channel_type is always included in Langfuse payload  
**Where:** In `_send_langfuse()` metadata construction

**Changes:**
1. Accept `channel_type` parameter explicitly
2. **Always include** `channel_type` in metadata dict (never omit)
3. Default to `"whatsapp"` if not provided (fallback)

**Pseudo-code:**
```python
def _send_langfuse(
    trace_name, query, answer, evidence, module, intents, 
    mode, is_langfuse_unavailable, latency_ms, context, params,
    channel_type="whatsapp"  # NEW: explicit parameter
):
    metadata = {
        # ... existing fields ...
        "channel_type": channel_type,  # NEW: always include
        # ... rest of metadata ...
    }
    # ... send to Langfuse ...
```

### Task 3: Update All `_send_langfuse()` Call Sites

**What:** Pass channel_type when calling `_send_langfuse()`  
**Where:** Every call to `_send_langfuse()` in kb_answer.py

**Pattern:**
```python
# BEFORE:
_send_langfuse("kb_answer", query, answer, evidence, module, intents, 
               mode, False, latency_ms, context, params)

# AFTER:
_send_langfuse("kb_answer", query, answer, evidence, module, intents, 
               mode, False, latency_ms, context, params,
               channel_type=detected_channel)  # NEW
```

**Count:** Search for `_send_langfuse(` calls and update all of them

### Task 4: Verify Channel Detection Function

**What:** Ensure `_detect_channel_type()` is correct and complete  
**Current implementation:** Line ~2714 in skill/kb_answer.py

**Verification checklist:**
- ✓ Returns "rcs" for kb/channels/rcs-*.md
- ✓ Returns "whatsapp" for kb/channels/whatsapp*
- ✓ Returns "instagram" for kb/channels/instagram*
- ✓ Returns "web" for kb/channels/web*
- ✓ Returns "channels_other" for other kb/channels/*
- ✓ **Returns "whatsapp" (not None) for all other sources**

**Current code (as of June 11):** Already updated to return "whatsapp" as default ✓

---

## ✅ Testing & Validation

### Manual Test Cases

Once implemented, test with these queries:

**Test 1: RCS Query**
```
Query: "How do I authenticate RCS?"
Expected trace:
  - channel_type: "rcs"
  - top_source: kb/channels/rcs-authentication.md
```

**Test 2: WhatsApp Query (explicit)**
```
Query: "How do I set up WhatsApp Flows?"
Expected trace:
  - channel_type: "whatsapp"
  - top_source: kb/channels/whatsapp-flows*.md
```

**Test 3: Legacy Query (default)**
```
Query: "How do I build a journey?"
Expected trace:
  - channel_type: "whatsapp" (default, NOT null/untagged)
  - top_source: kb/bot-studio/journeys.md
```

**Test 4: No Match Query**
```
Query: "Random question with no good match"
Expected trace:
  - channel_type: "whatsapp" (default fallback)
  - top_source: (whatever the bot found)
```

### Automated Check

After deployment, query Langfuse and verify:

```bash
# Check that NO traces have channel_type = null/None
lf traces list --name kb_answer --limit 100 | \
  jq '.[] | select(.metadata.channel_type == null) | length'

# Result should be: 0 (no untagged traces)
```

---

## 📊 Expected Dashboard Impact

### Before Implementation
```
Analytics dashboard shows:
  untagged: 197 queries  ← Unclear/confusing
  rcs:        3 queries
```

### After Implementation
```
Analytics dashboard shows:
  whatsapp:  197 queries  ← Clear: primary channel
  rcs:         3 queries  ← Clear: emerging channel
  instagram:   0 queries
  web:         0 queries
  (All other channels properly tagged when used)
```

---

## 🔗 Related Code Files

**Files to modify:**
- `skill/kb_answer.py` — Main changes
  - Line ~2714: `_detect_channel_type()` ✓ (already updated)
  - Line ~5086+: `kb_answer()` main logic
  - Line ~1200+ (approx): `_send_langfuse()` function
  - All call sites of `_send_langfuse()`

**Files to reference:**
- `local/scripts/comprehensive_analytics_dashboard.py` — Shows expected output
- `local/reports/comprehensive_dashboard.html` — Visual of results

---

## 📋 Checklist for Agent

- [ ] Update `kb_answer()` to call `_detect_channel_type()` early
- [ ] Store detected channel in metadata object
- [ ] Update `_send_langfuse()` signature to accept `channel_type` parameter
- [ ] Ensure `channel_type` is always included in metadata (never omitted)
- [ ] Set fallback default to `"whatsapp"` if not provided
- [ ] Update all `_send_langfuse()` call sites to pass channel_type
- [ ] Verify `_detect_channel_type()` returns "whatsapp" for untagged sources ✓
- [ ] Test with sample queries (RCS, WhatsApp, Bot Studio, no-match)
- [ ] Verify Langfuse traces have channel_type in metadata
- [ ] Commit changes with clear message
- [ ] Notify analytics team to regenerate dashboard

---

## 📞 Success Criteria

✅ **Implementation is successful when:**

1. Every trace sent to Langfuse includes `metadata.channel_type`
2. No traces have `channel_type = null` or `channel_type = undefined`
3. Channel detection is consistent (same source always maps to same channel)
4. Default fallback is `"whatsapp"` (not `None` or `"untagged"`)
5. RCS queries explicitly tagged as `"rcs"`
6. Dashboard regeneration shows WhatsApp (197) + RCS (3) breakdown
7. All future channels (Instagram, Web, SMS) properly detected when sources exist

---

## 🎯 Why This Matters

**Current pain point:** 
- 197 queries show as "untagged" in analytics
- Can't track WhatsApp vs RCS performance separately
- Confusing dashboard (what does "untagged" mean?)

**After implementation:**
- All queries properly categorized by channel
- Clear WhatsApp (primary) vs RCS (emerging) metrics
- Ready to add more channels (Instagram, Web, SMS)
- Analytics dashboard is actionable and clear

---

## 📝 Notes for Agent

1. **No user-facing changes** — This is purely analytics instrumentation
2. **Backward compatible** — Existing queries still work, just properly tagged
3. **Low risk** — Only affects Langfuse metadata, not answer logic
4. **High impact** — Unlocks multi-channel analytics capabilities

---

**Instructions complete. Hand this to the skill code change agent and let them know the comprehensive analytics team is waiting for the updated channel_type data to properly track performance by channel.**
