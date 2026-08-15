# Phase 1: Consulting-Tone Code Implementation Guide

**Date:** 2026-08-11  
**Status:** Design Complete, Ready for Implementation  
**Estimated Implementation Time:** 3-4 hours (code + tests + deploy)  
**Complexity:** LOW (125 LOC total, zero existing logic deleted, pure additive)

---

## Overview

Implement consulting-tone answer generation alongside existing problem-solution framework using feature flag + A/B test approach. **Two-module pilot: RCS + Bot Studio**, 50/50 traffic split within each module.

**Key insight:** The consulting tone is a **composer-layer change** only. No changes to retrieval, scoring, entity detection, or confidence calculation. The infrastructure for controlling this with environment variables already exists.

**Why two modules (revised 2026-08-11):** RCS traffic is campaign-driven — marketing pushes send bursts of near-identical templated queries, which pollutes the engagement/accuracy signal (you're measuring campaign response, not consulting-tone effectiveness). Bot Studio was added as a second, cleaner signal:

| Module | Volume (30d) | Answer Rate | IDK Rate | Traffic character |
|---|---|---|---|---|
| **RCS** | Low, bursty | — | — | Campaign-driven, templated, low diversity |
| **Bot Studio** | 60 | 81.7% | 18.3% | Organic, top-3 by volume, high query diversity |
| WhatsApp (excluded) | 157 | 68.8% | 31.2% | Highest volume but too high-stakes for Phase 1 |
| Channels (considered, not picked) | 40 | 85.0% | 15.0% | Already high-performing, less "it depends" shape |

Bot Studio queries are naturally conditional ("how do I build a flow for X" almost always has 2-3 valid paths depending on use case), which is exactly the shape consulting-tone's diagnosis → context → options → recommended structure is built for. It's also where the P2 content gap article (`bot-studio-journey-patterns.md`, 34 chunks) just shipped, so the pilot tests consulting-tone on freshly-improved evidence rather than stale gaps. WhatsApp is deliberately excluded from Phase 1 — highest volume and most business-critical, so it's held back for Phase 2 once the approach is proven on two lower-stakes modules.

---

## Code Changes Summary

| Component | Lines | Type | Location |
|---|---|---|---|
| `_compose_consulting_answer()` | ~80 | NEW | Insert before `_compose_answer()` at line 6482 |
| `_resolve_answer_mode()` | ~25 | NEW | Insert near line 7650 |
| `_route_answer_composer()` | ~15 | NEW | Insert near line 7650 |
| Caller site modification | 1 | CHANGE | Line 7655 (answer = → answer, mode = ) |
| Telemetry update | 3 | CHANGE | Line ~7840 (policy_meta["answer_mode"]) |
| **TOTAL** | **~125** | **NET ADDITIVE** | Zero existing code deleted |

---

## Step-by-Step Implementation

### Step 1: Add `_compose_consulting_answer()` Function

**Insert at line 6482** (before existing `_compose_answer()` function):

```python
def _compose_consulting_answer(
    query: str,
    intent: str,
    entities: List[Dict],
    evidence: List[Dict],
    explicit_module: str = "General",
    confidence: float = 0.0,
) -> str:
    """
    Consulting-tone composer: diagnosis → context → options → recommended → follow-up.
    
    Flow:
    1. Diagnosis: Acknowledge the user's task/problem
    2. Context: Indicate what depends on their setup
    3. Options: Surface 2-3 paths if low confidence, else direct answer
    4. Recommended: High confidence → surface primary path
    5. Follow-up: Low confidence → ask for clarification
    
    Args:
        query: User's question
        intent: Detected intent (setup, troubleshooting, definition, compare, etc.)
        entities: Detected entities (modules, products, actions)
        evidence: Retrieved KB chunks scored by relevance
        explicit_module: Detected module (RCS, WhatsApp, Bot Studio, etc.)
        confidence: Confidence score (0.0-1.0) from _reported_confidence()
    
    Returns:
        Consulting-formatted answer string. Falls back to IDK if insufficient evidence.
    """
    
    # Early exit: insufficient evidence
    lines = _evidence_lines(evidence)
    if not evidence or not lines:
        return "I don't know based on the current docs."

    # Gate: only apply consulting tone when evidence is substantive
    if not _has_explicit_support(query, intent, evidence, lines, entities, explicit_module):
        return "I don't know based on the current docs."

    # --- 1. DIAGNOSIS ---
    # Acknowledge the user's task or symptom based on intent
    if intent in ("setup", "how_to"):
        diagnosis = f"To set this up, here's what you need to know."
    elif intent == "troubleshooting":
        diagnosis = f"Let's figure out what's going on."
    elif intent == "definition":
        heading = str(evidence[0].get("heading") or "").strip()
        diagnosis = f"Here's what **{heading}** means in this context." if heading else "Here's what this means."
    elif intent == "compare":
        diagnosis = "These are distinct features — let me walk through the key differences."
    else:
        diagnosis = "Here's what the documentation says about this."

    # --- 2. CONTEXT (What depends on their setup?) ---
    # Detect multi-path scenarios from evidence headings
    # Example: "WhatsApp Business" vs "Gupshup Dashboard" in headings suggests multiple paths
    unique_headings = []
    seen = set()
    for c in evidence[:4]:
        h = str(c.get("heading") or "").strip()
        if h and h.lower() not in seen:
            seen.add(h.lower())
            unique_headings.append(h)

    context_lines = []
    if len(unique_headings) >= 2 and confidence < 0.7:
        # Low confidence + multiple paths → acknowledge the branching
        context_lines.append(f"This can vary depending on your setup. The docs cover a few scenarios:")
        for h in unique_headings[:3]:
            context_lines.append(f"- {h}")

    # --- 3. OPTIONS OR DIRECT ANSWER ---
    if len(unique_headings) >= 2 and confidence < 0.7:
        # Multi-path low-confidence scenario: surface each path briefly
        body_parts = []
        for c in evidence[:3]:
            h = str(c.get("heading") or "").strip()
            text_lines = [
                l for l in str(c.get("text") or "").splitlines()
                if _clean_line(l)
            ][:2]
            if h and text_lines:
                body_parts.append(f"**{h}**: {_clean_line(text_lines[0])}")
        body = "\n".join(body_parts)
    else:
        # Single-path or high-confidence: direct answer from evidence
        body = "\n".join(f"- {l}" for l in lines[:5])

    # --- 4. RECOMMENDED (High confidence: surface the primary path) ---
    recommended = ""
    if confidence >= 0.6 and lines:
        recommended = f"Most common case: {lines[0]}"

    # --- 5. FOLLOW-UP (Low confidence: ask for clarification) ---
    follow_up = ""
    if confidence < 0.5:
        if explicit_module != "General":
            follow_up = f"Tell me more about your specific {explicit_module} setup and I can tailor this further."
        else:
            follow_up = "Share more context about what you're trying to accomplish and I can be more specific."

    # --- ASSEMBLE ---
    parts = [diagnosis]
    if context_lines:
        parts.append("\n".join(context_lines))
    parts.append(body)
    if recommended:
        parts.append(recommended)
    if follow_up:
        parts.append(follow_up)

    return "\n\n".join(p for p in parts if p.strip())
```

**Validation:**
- Function is a pure function (no side effects)
- Gracefully handles empty evidence
- Confidence score controls diagnosis vs multi-path vs direct answer
- Falls back to IDK appropriately

---

### Step 2: Add A/B Testing Router Functions

**Insert at line ~7650** (just before the `_compose_answer()` call at line 7655):

```python
def _resolve_answer_mode(params: dict, query: str, explicit_module: str) -> str:
    """
    Resolve answer generation mode (consulting or standard problem-solution).
    
    Priority order:
    1. Explicit param override (for testing/debugging)
    2. Master feature flag
    3. Module-level gate (Phase 1: RCS + Bot Studio)
    4. Deterministic 50/50 hash-based split per query
    5. Default: standard
    
    Environment variables:
    - KB_CONSULTING_TONE_ENABLED: "1" = master switch ON
    - KB_CONSULTING_TONE_MODULES: "RCS,Bot Studio" = allowed modules (comma-separated)
    - KB_CONSULTING_TONE_PCT: "50" = percent of traffic in consulting mode
    - KB_ANSWER_MODE: "consulting" or "standard" = force override (testing only)
    
    Returns:
        "consulting" or "standard"
    """
    import hashlib
    import os

    # 1. Explicit param override (for QA and force-testing)
    explicit = (params or {}).get("answer_mode") or os.getenv("KB_ANSWER_MODE", "")
    if explicit in ("consulting", "standard"):
        return explicit

    # 2. Master feature flag
    if not os.getenv("KB_CONSULTING_TONE_ENABLED", ""):
        return "standard"

    # 3. Module-level gate (Phase 1: RCS + Bot Studio)
    allowed_modules_str = os.getenv("KB_CONSULTING_TONE_MODULES", "RCS,Bot Studio")
    allowed_modules = {m.strip() for m in allowed_modules_str.split(",")}
    if explicit_module not in allowed_modules:
        return "standard"

    # 4. Deterministic 50/50 hash-based split on query
    # Same query always gets same mode (makes debugging reproducible)
    split_pct = int(os.getenv("KB_CONSULTING_TONE_PCT", "50"))
    digest = int(hashlib.md5(query.encode()).hexdigest(), 16)
    return "consulting" if (digest % 100) < split_pct else "standard"


def _route_answer_composer(
    query: str,
    intent: str,
    entities: List[Dict],
    evidence: List[Dict],
    explicit_module: str,
    params: dict,
) -> Tuple[str, str]:
    """
    Route to consulting-tone or problem-solution composer.
    
    Returns:
        Tuple of (answer_text: str, answer_mode: str)
        where answer_mode is "consulting" or "standard"
    
    Usage:
        answer, mode = _route_answer_composer(query, intent, entities, evidence, module, params)
    """
    mode = _resolve_answer_mode(params, query, explicit_module)
    
    if mode == "consulting":
        # Get confidence score for consulting composer
        conf = _reported_confidence(query, evidence)
        answer = _compose_consulting_answer(query, intent, entities, evidence, explicit_module, conf)
    else:
        # Standard problem-solution path (unchanged)
        answer = _compose_answer(query, intent, entities, evidence, explicit_module)
    
    return answer, mode
```

**Key properties:**
- Deterministic: same query always gets same mode (seed on MD5 hash)
- Testable: force override via params["answer_mode"] or env var
- Safe: defaults to "standard" if any feature flag missing
- Scalable: can change `KB_CONSULTING_TONE_PCT` from 50 → 80 → 100 as we gain confidence

---

### Step 3: Update the Caller Site

**Change line 7655** (in main `kb_answer()` function):

```python
# BEFORE (current line 7655):
answer = _compose_answer(query, intent, entities, evidence, explicit_module)

# AFTER:
answer, answer_mode = _route_answer_composer(query, intent, entities, evidence, explicit_module, params)
```

**That's it.** One line changed. Everything else is additive.

---

### Step 4: Update Telemetry

**Around line 7840**, where Langfuse telemetry is sent, add `answer_mode` to the telemetry output:

```python
# Before (current code):
policy_meta = dict(policy_meta or {})
# ... existing policy_meta assignments ...
langfuse_output = {
    "answer": answer,
    "answer_policy": policy_meta,
    # ... other fields ...
}

# After (add one line):
policy_meta = dict(policy_meta or {})
policy_meta["answer_mode"] = answer_mode  # "consulting" or "standard" — NEW LINE
# ... rest of existing code unchanged ...
```

This tags every answer in Langfuse so we can segment metrics by `answer_mode` in dashboards.

---

### Step 5: Environment Variables for Phase 1

**On the test environment, set:**

```bash
export KB_CONSULTING_TONE_ENABLED=1
export KB_CONSULTING_TONE_MODULES="RCS,Bot Studio"
export KB_CONSULTING_TONE_PCT=50
```

**Meaning:**
- `ENABLED=1`: Master switch ON
- `MODULES=RCS`: Only apply to RCS queries (other modules get standard)
- `PCT=50`: 50% of RCS traffic gets consulting, 50% gets standard (A/B test)

**To disable instantly** (rollback):
```bash
unset KB_CONSULTING_TONE_ENABLED
# Or set to empty: export KB_CONSULTING_TONE_ENABLED=
```

---

## Testing & Validation

### Unit Test File: `local/scripts/test_consulting_tone.py`

```python
#!/usr/bin/env python3
"""
Unit tests for consulting-tone answer generation.
Run: python local/scripts/test_consulting_tone.py
"""

import sys
sys.path.insert(0, '.')

from skill.kb_answer import _compose_consulting_answer

def make_evidence(heading, text, score=2.0, source="rcs/setup.json"):
    """Helper: create mock evidence chunk."""
    return {"heading": heading, "text": text, "score": score, "source": source}

# Test cases: (name, inputs, expected_phrases, must_not_contain)
TEST_CASES = [
    {
        "name": "high_confidence_setup",
        "query": "how do I enable RCS on my account",
        "intent": "setup",
        "module": "RCS",
        "confidence": 0.8,
        "evidence": [
            make_evidence(
                "Enable RCS",
                "Go to Settings > Channels > RCS and toggle Enable."
            )
        ],
        "expect_contains": ["Enable RCS", "Most common case"],
        "expect_not_contains": ["I don't know"],
    },
    {
        "name": "low_confidence_multi_path",
        "query": "how does RCS fallback work",
        "intent": "behavior",
        "module": "RCS",
        "confidence": 0.3,
        "evidence": [
            make_evidence(
                "SMS Fallback",
                "When RCS is unavailable, message falls back to SMS."
            ),
            make_evidence(
                "MMS Fallback",
                "Rich media falls back to MMS if RCS fails."
            ),
        ],
        "expect_contains": [
            "vary depending on your setup",
            "SMS Fallback",
            "Tell me more",
        ],
        "expect_not_contains": ["I don't know"],
    },
    {
        "name": "no_evidence_idk",
        "query": "what is the meaning of life",
        "intent": "definition",
        "module": "General",
        "confidence": 0.0,
        "evidence": [],
        "expect_contains": ["I don't know"],
        "expect_not_contains": [],
    },
]

def run_tests():
    passed = 0
    failed = 0
    
    for case in TEST_CASES:
        try:
            answer = _compose_consulting_answer(
                query=case["query"],
                intent=case["intent"],
                entities=[],
                evidence=case["evidence"],
                explicit_module=case["module"],
                confidence=case["confidence"],
            )
            
            # Check expected phrases
            for phrase in case.get("expect_contains", []):
                if phrase.lower() not in answer.lower():
                    raise AssertionError(
                        f"Expected phrase not found: {phrase!r}\n"
                        f"Got: {answer}"
                    )
            
            # Check phrases that should NOT appear
            for phrase in case.get("expect_not_contains", []):
                if phrase.lower() in answer.lower():
                    raise AssertionError(
                        f"Unexpected phrase found: {phrase!r}\n"
                        f"Got: {answer}"
                    )
            
            print(f"✅ PASS: {case['name']}")
            passed += 1
            
        except Exception as e:
            print(f"❌ FAIL: {case['name']}")
            print(f"   Error: {e}")
            failed += 1
    
    print()
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
```

**Run with:**
```bash
cd /Users/adwit.sharma/kb_docs
python local/scripts/test_consulting_tone.py
```

**Expected output:**
```
✅ PASS: high_confidence_setup
✅ PASS: low_confidence_multi_path
✅ PASS: no_evidence_idk

Results: 3 passed, 0 failed
```

---

## Rollback Strategy

### Instant Rollback (No Deployment)

Change one environment variable:
```bash
unset KB_CONSULTING_TONE_ENABLED
```

**Effect:** Immediate. On the next request, `_resolve_answer_mode()` returns "standard" and the existing `_compose_answer()` path is used. Zero behavioral change.

### Automatic Rollback Triggers

Add to monitoring dashboard:
```
IF answer_mode="consulting" AND (
  idK_rate > (idK_rate_standard + 10pp)  // IDK rate for consulting 10pp higher
  OR confidence_avg < 0.4                 // Consulting avg confidence too low
  OR error_rate > 5%                      // Errors spiking
):
  Alert: "Consulting tone health critical"
  → Set KB_CONSULTING_TONE_ENABLED=""
```

### Code Safety Guarantees

1. **Zero existing logic deleted:** `_compose_answer()` untouched
2. **Pure functions:** `_compose_consulting_answer()` has no side effects
3. **Try-catch protected:** Existing error handling at composition layer catches any exception from new function
4. **Additive only:** If new function throws, fallback to IDK (same as low-evidence path)
5. **Deterministic A/B split:** Same query always gets same mode (reproducible debugging)

---

## Success Criteria (Phase 1 Gates)

After deploying with the above code changes and env vars set:

| Gate | Target | Trigger | Recovery |
|---|---|---|---|
| **Engagement** | Multi-turn % ≥ 9.6% | If ≤8.5% after 3 days | Rewrite consulting prompts, retry |
| **Accuracy** | RCS ≥ 65% | If <62% | Revert env var, investigate |
| **Consulting effectiveness** | Question resolution ≥50% | If <35% | Redesign questions, retry |
| **Routing** | Module detection ≥90% | If <88% | Debug routing, revert module |

---

## Deployment Checklist

- [ ] Code changes implemented (Step 1-4 above)
- [ ] Unit tests pass locally (`python local/scripts/test_consulting_tone.py`)
- [ ] Code review: check function signature compatibility
- [ ] Environment variables configured in test environment
- [ ] Langfuse dashboards set up to segment by `answer_mode`
- [ ] Monitoring dashboard ready (see PHASE_1_GATES_AND_MONITORING.md)
- [ ] Rollback procedure documented and tested
- [ ] A/B test launch (50/50 split on RCS)
- [ ] Daily monitoring (check gates hourly)

---

## FAQ

**Q: Why not change existing `_compose_answer()`?**  
A: Zero-risk approach. Existing function unchanged = instant rollback by env var. If we modify existing function, rollback requires code revert + deploy.

**Q: What if consulting tone is slower?**  
A: Monitor `response_time_ms` in Langfuse. If consulting avg >2s vs standard <1.5s, optimize `_compose_consulting_answer()` (likely the evidence loop). If still slow, revert.

**Q: How do we A/B test accurately?**  
A: Hash-based split on query ensures same user asking same question always gets same answer type (consulting or standard). This is better than per-user split (avoids confusion).

**Q: Can we expand to other modules before Phase 1 ends?**  
A: Not recommended. Phase 1 scope is fixed at RCS + Bot Studio. If gates pass after 1 week (evaluated per-module, not blended), Phase 2 expands to Channels/WhatsApp. Expanding mid-week risks confounding variables.

**Q: Why track RCS and Bot Studio separately instead of blending the metrics?**  
A: Different baselines (RCS has near-zero organic baseline; Bot Studio baseline is 81.7% answer rate / 18.3% IDK) and different traffic character (RCS is bursty/campaign-driven, Bot Studio is steady/organic). A blended number would let a good Bot Studio week mask a bad RCS week or vice versa. Gate decisions are made per-module.

**Q: What if the new function crashes?**  
A: It's wrapped in the existing try-except at answer composition layer. If it throws, answer returns IDK (safe degradation). Rollback by unsetting env var.

---

## Timeline

**Today (2026-08-11):** Code design approved ✅  
**Tomorrow (2026-08-12):** Implement code + tests  
**2026-08-13:** Code review + deploy to test environment  
**2026-08-14-20:** Phase 1 pilot (1 week A/B test)  
**2026-08-21:** Gate review (proceed to Phase 2 or investigate)

---

**Status:** Ready for implementation  
**Complexity:** LOW (125 LOC, no existing deletions)  
**Risk:** LOW (feature flag controlled, instant rollback via env var)  
**Expected effort:** 3-4 hours (code + tests + deployment)

