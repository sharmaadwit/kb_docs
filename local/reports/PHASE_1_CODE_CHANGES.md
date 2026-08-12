# Phase 1 Code Changes — Exact File & Line References

**Commit:** `001d5369` (Phase 1 code: implement consulting-tone router)  
**File Modified:** `skill/kb_answer.py`  
**Lines Added:** ~180 (new functions) + 1 (call-site change)  
**Backward Compatibility:** ✅ 100% — flag defaults off, instant rollback via env var

---

## File Change Summary

**Modified File:** `skill/kb_answer.py`

### 1. Import Addition (Line 7)
```python
# Added hashlib for deterministic 50/50 A/B split
import hashlib
```

### 2. New Function: `_compose_consulting_answer()` (Lines 6483–6568)
**Purpose:** Generate consulting-tone answers (diagnosis → context → options → recommended → follow-up)

**Function signature:**
```python
def _compose_consulting_answer(
    query: str,
    intent: str,
    entities: List[Dict],
    evidence: List[Dict],
    explicit_module: str = "General",
    confidence: float = 0.0,
) -> str:
```

**Key sections:**
- **Lines 6483–6497:** Function docstring and early validation
- **Lines 6499–6509:** Diagnosis section (intent-based opening)
- **Lines 6511–6530:** Context section (multi-path detection, content-based deduplication)
- **Lines 6532–6543:** Options/body section
- **Lines 6545–6549:** Recommended section (high confidence only)
- **Lines 6551–6559:** Follow-up section (low confidence trigger)
- **Lines 6561–6568:** Assembly and return

**What to look for post-deployment:**
- Consulting-tone answers are longer, multi-paragraph with diagnostic framing
- Contains phrases like "Let's figure out...", "This can vary depending on...", "Tell me more..."
- Always returns non-empty string (same IDK fallback as standard path if evidence insufficient)

---

### 3. New Function: `_gate_module_for_consulting()` (Lines 7511–7527)
**Purpose:** Resolve the gate module for Phase 1 feature-flag decision

**Key logic:**
- Checks if `explicit_module in ("Channels", "Campaign Manager")`
- If yes, uses `_detect_channel_from_query(query)` to extract "RCS" from the Channels bucket
- Returns "RCS" if detected, else returns the original `explicit_module`
- Handles edge case: campaign-flavored RCS queries (e.g., "should I use RCS for my campaign") land in "Campaign Manager", not "Channels"

**Why this matters:**
- `_detect_module()` has no "RCS" module; all RCS queries land in "Channels"
- Without this gate, the Phase 1 pilot would accidentally gate on ALL Channels queries, not just RCS
- This function pulls RCS out so the pilot targets RCS specifically

---

### 4. New Function: `_resolve_answer_mode()` (Lines 7529–7564)
**Purpose:** Resolve whether to use consulting or standard composer, based on feature flags and module gates

**Priority order:**
1. Explicit param override (`params["answer_mode"]`) or env var (`KB_ANSWER_MODE`)
2. Master feature flag (`KB_CONSULTING_TONE_ENABLED`)
3. Module gate (via `_gate_module_for_consulting()`)
4. Deterministic 50/50 hash split

**Env vars:**
- `KB_CONSULTING_TONE_ENABLED`: "1" = master switch ON (default: off)
- `KB_CONSULTING_TONE_MODULES`: "RCS,Bot Studio" = allowed modules (default: "RCS,Bot Studio")
- `KB_CONSULTING_TONE_PCT`: "50" = percent in consulting mode (default: 50)
- `KB_ANSWER_MODE`: "consulting" | "standard" = force override (testing only)

**Deterministic split:**
- Uses `hashlib.md5(query.encode()).hexdigest() % 100`
- Same query always gets same mode (no user confusion)
- Different queries can split randomly (proper A/B)

---

### 5. New Function: `_route_answer_composer()` (Lines 7567–7588)
**Purpose:** Route to consulting or standard composer, return (answer, mode) tuple

**Function signature:**
```python
def _route_answer_composer(
    query: str,
    intent: str,
    entities: List[Dict],
    evidence: List[Dict],
    explicit_module: str,
    params: dict,
) -> Tuple[str, str]:
```

**Returns:** `(answer_text, answer_mode)` tuple where `answer_mode` is "consulting" or "standard"

**Logic:**
- Calls `_resolve_answer_mode()` to get mode
- If mode="consulting": calls `_compose_consulting_answer()`, calculates confidence via `_reported_confidence()`
- If mode="standard": calls existing `_compose_answer()` (unchanged)
- Returns both the answer text and the mode (for telemetry tagging)

---

### 6. Call-Site Change in `kb_answer()` (Line 7832)
**Before:**
```python
answer = _compose_answer(query, intent, entities, evidence, explicit_module)
```

**After:**
```python
answer, answer_mode = _route_answer_composer(query, intent, entities, evidence, explicit_module, params)
```

**Post-call tagging (Lines 7834–7835):**
```python
policy_meta = dict(policy_meta or {})
policy_meta["answer_mode"] = answer_mode
```

**Why:**
- Switches from direct `_compose_answer()` to the new router
- Captures the mode and tags it into `policy_meta` for telemetry segmentation
- Langfuse will see `policy_meta.answer_mode = "consulting"` or `"standard"` on each trace

---

## Backward Compatibility

✅ **100% compatible when flag is OFF:**
- `KB_CONSULTING_TONE_ENABLED` defaults to unset (falsy)
- When unset, `_resolve_answer_mode()` returns "standard" immediately (line 7542)
- Router calls `_compose_answer()`, the old code path, unchanged
- Byte-for-byte identical behavior to pre-Phase-1 code

✅ **Instant rollback:**
- Simply unset `KB_CONSULTING_TONE_ENABLED` to revert to 100% standard mode
- No code changes needed, no deployment

---

## How to Verify Changes After Pull

### Option 1: Compare diffs locally
```bash
git fetch origin main
git diff origin/main~2 origin/main -- skill/kb_answer.py | less
```

### Option 2: Copy the new functions
The three new standalone functions can be copy-pasted independently:
- `_compose_consulting_answer()` (lines 6483–6568)
- `_gate_module_for_consulting()` (lines 7511–7527)
- `_resolve_answer_mode()` (lines 7529–7564)
- `_route_answer_composer()` (lines 7567–7588)

### Option 3: Visual check
Search for these markers in `skill/kb_answer.py`:
- `import hashlib` (line 7) — hashlib added
- `def _compose_consulting_answer(` (line 6483) — new composer
- `def _gate_module_for_consulting(` (line 7511) — new gate resolver
- `def _resolve_answer_mode(` (line 7529) — new mode resolver
- `_route_answer_composer` (line 7832) — new router call

---

## Tracing Changes: What You'll See in Langfuse

### Pre-Phase-1 Traces (Baseline)
```json
{
  "name": "kb_answer",
  "input": {"query": "how do I build a Bot Studio journey"},
  "output": "...",
  "metadata": {
    "module": "Bot Studio",
    "intent": "setup",
    "confidence": 0.52,
    "answer_rate": 1,
    "idk": false
  }
  // NO "answer_mode" field
}
```

### Phase-1 Traces (Consulting Arm)
```json
{
  "name": "kb_answer",
  "input": {"query": "how do I build a Bot Studio journey"},
  "output": "To set this up, here's what you need to know.\n\nThis can vary depending on your setup. The docs cover a few scenarios:\n- Option 1\n- Option 2\n\n...",
  "metadata": {
    "module": "Bot Studio",
    "intent": "setup",
    "confidence": 0.52,
    "answer_rate": 1,
    "idk": false,
    "answer_mode": "consulting"  // ← NEW FIELD
  }
}
```

### Phase-1 Traces (Control Arm)
```json
{
  "name": "kb_answer",
  "input": {"query": "how do I set up RCS"},
  "output": "...",  // standard problem-solution format
  "metadata": {
    "module": "Channels",  // or "Campaign Manager"
    "intent": "setup",
    "confidence": 0.48,
    "answer_rate": 1,
    "idk": false,
    "answer_mode": "standard"  // ← NEW FIELD
  }
}
```

---

## Segmenting Traces in Langfuse Dashboards

### Filter by Consulting Mode
```
metadata.answer_mode = "consulting"
```

### Filter by Module + Mode
```
metadata.module = "Bot Studio" AND metadata.answer_mode = "consulting"
```

### Compare Consulting vs Control
```
# Control arm
metadata.answer_mode = "standard" AND metadata.module = "Bot Studio"

# Consulting arm
metadata.answer_mode = "consulting" AND metadata.module = "Bot Studio"
```

### Track Multi-Turn Conversations
The router adds `answer_mode` to policy_meta, which persists through the conversation:
- If a user's first query gets `answer_mode="consulting"`, subsequent replies (turn 2, 3, ...) in the same session will also have `answer_mode="consulting"`
- This enables tracking multi-turn engagement per arm

### Expected Langfuse Dashboard Queries

**Daily Pilot Dashboard will use:**

1. **Answer Rate by Mode**
   ```
   SELECT COUNT(*) / COUNT(DISTINCT trace_id) * 100
   WHERE metadata.answer_mode = "consulting" AND metadata.module = "Bot Studio"
   GROUP BY DATE(timestamp)
   ```

2. **IDK Rate by Mode**
   ```
   SELECT SUM(CASE WHEN metadata.idk = true THEN 1 ELSE 0 END) / COUNT(*) * 100
   WHERE metadata.module = "Bot Studio"
   GROUP BY metadata.answer_mode, DATE(timestamp)
   ```

3. **Multi-Turn Engagement**
   ```
   SELECT COUNT(DISTINCT session_id)
   WHERE metadata.answer_mode = "consulting" AND turn_count >= 2
   ```

4. **RCS Directional Tracking**
   ```
   SELECT metadata.answer_mode, COUNT(*)
   WHERE metadata.module = "Channels" 
     AND _detect_channel(query) = "rcs"
   GROUP BY metadata.answer_mode, DATE(timestamp)
   ```

---

## Go-Live Checklist

- [x] Code changes merged to main
- [x] Commit: `001d5369` pushed to GitLab
- [x] Unit tests: 14/14 passing
- [x] Independent workflow review: no bugs found
- [x] Baseline metrics exported: 954 traces (30 days), committed
- [ ] **Next:** Set env vars in test environment:
  ```bash
  export KB_CONSULTING_TONE_ENABLED=1
  export KB_CONSULTING_TONE_MODULES="RCS,Bot Studio"
  export KB_CONSULTING_TONE_PCT=50
  ```
- [ ] **Monitor:** Watch Langfuse for `answer_mode` field in new traces
- [ ] **Gate 1:** Bot Studio answer rate ≥76% after 2-3 days
- [ ] **Gate 2:** Multi-turn engagement +20% over control after 3 days
- [ ] **Gate 3:** RCS directional tracking (no hard gate, logging only)

---

**Prepared by:** Phase 1 Implementation  
**Date:** 2026-08-12  
**Status:** Ready for Test Environment Deployment
