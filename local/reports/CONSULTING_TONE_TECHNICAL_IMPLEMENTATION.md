# Consulting Tone: Technical Implementation Guide
## kb_answer.py Mechanics & Code Patterns

**Document:** Maps consulting-tone shift to specific code locations and refactoring patterns  
**Target Audience:** Engineers implementing Phase 1-4 consulting rollout  
**Status:** Ready for implementation

---

## PART 1: Current Architecture (Problem-Solution Model)

### Main Entry Point: kb_answer()

**Location:** `kb_answer.py:7418`

```python
def kb_answer(parameters: object = None, context=None, correlation_id: Optional[str] = None, 
              parent_trace_id: Optional[str] = None, **kwargs) -> dict:
    """Main skill entry point. Returns answer dict with telemetry."""
    
    # Current flow:
    # 1. Parse query + entities
    # 2. Search KB (kb_search)
    # 3. Compose answer (_compose_answer)
    # 4. Apply policy (FAQ summary cap)
    # 5. Return answer with confidence telemetry
```

**Current Return Structure:**
```python
{
    "answer": "...",  # String, HTML-formatted
    "confidence": 0.7,  # Float 0.0-1.0
    "query": "...",
    "intent": "...",
    # ... telemetry
}
```

### Answer Composition: _compose_answer()

**Location:** `kb_answer.py:6482`

```python
def _compose_answer(
    query: str,
    intent: str,
    entities: List[Dict],
    evidence: List[Dict],
    explicit_module: str = "General",
) -> str:  # Returns STRING (not Dict)
    """Main answer composition: pick the best strategy based on intent + entities."""
    
    # Current decision tree:
    # 1. Entity match + template found? → return template (deterministic)
    # 2. Comparison intent? → compose comparison (deterministic)
    # 3. Overview intent? → compose overview (deterministic)
    # 4. Evidence exists? → compose from evidence (deterministic)
    # 5. No evidence? → return "I don't know" (hard boundary)
```

**Key Pattern: Single String Return**
- All paths return a string
- No metadata, no follow-up prompts
- Conversation ends after kb_answer's turn

### Confidence Reporting: _reported_confidence()

**Location:** `kb_answer.py:5812`

```python
def _reported_confidence(query: str, results: List[Dict]) -> float:
    """Confidence = 0.7 * relevance + 0.3 * normalized_score"""
    
    if not results:
        return 0.0
    top = results[0]
    score_component = min(1.0, max(0.0, top.get("score", 0.0) / 8.0))
    relevance = _query_overlap_score(query, top)  # [0, 1]
    confidence = 0.7 * relevance + 0.3 * score_component
    return min(1.0, max(0.0, confidence))
```

**Current Logic:**
- Confidence = retrieval quality (query token overlap + normalized score)
- Does NOT account for:
  - User context (tech level, use case, scale)
  - Answer applicability (does this solve their problem?)
  - Evidence coverage (does KB have context-specific variant?)

### Evidence-Based Fallback: _compose_from_evidence()

**Location:** `kb_answer.py:6677`

```python
def _compose_from_evidence(
    query: str, intent: str, evidence: List[Dict], lines: List[str],
    entities: List[Dict] = None, explicit_module: str = "General",
) -> str:
    """Fallback: compose answer purely from retrieved evidence."""
    
    if not evidence or not lines:
        return "I don't know based on the current docs."
    
    if not _has_explicit_support(query, intent, evidence, lines, entities, explicit_module):
        return "I don't know based on the current docs."  # Hard boundary
    
    # Format answer based on intent
    if intent == "definition":
        return f"**{heading}**\n Definition\n- " + "\n- ".join(lines[:4])
    elif intent == "behavior":
        return "What happens\n- " + "\n- ".join(lines[:4])
    # ... more intent-specific formatting ...
```

**Current Pattern:**
- Binary: either format answer OR return "I don't know"
- No gradation, no follow-ups, no context-checking

---

## PART 2: Consulting Tone Refactoring (Phase 1-4)

### Phase 1: Soft Gradient Threshold

**Goal:** Replace binary confidence threshold with gradient

**Current Problem:**
```python
confidence = 0.49 → IDK (satisfaction 8%)
confidence = 0.51 → Answer (satisfaction 75%)
# Hard boundary, 0.02 confidence difference → 67% satisfaction difference
```

**Proposed Fix:**
```python
def kb_answer(...) -> dict:
    """Modified: return answer even for lower confidence."""
    
    confidence = _reported_confidence(query, results)
    
    # OLD:
    # if confidence < 0.5:
    #     return {"answer": "I don't know...", "confidence": 0.0}
    # else:
    #     return {"answer": "...", "confidence": confidence}
    
    # NEW: Soft gradient
    if confidence >= 0.8:
        answer = _compose_answer(...)
        return {"answer": answer, "confidence": confidence, "mode": "full"}
    
    elif confidence >= 0.6:
        answer = _compose_answer(...)
        return {"answer": answer, "confidence": confidence, "mode": "full"}
    
    elif confidence >= 0.4:
        # Search result exists but confidence low
        if results and results[0].get("score", 0) > 5.0:
            answer = _compose_answer(...)  # Fall back to search result
            return {"answer": answer, "confidence": confidence, "mode": "fallback"}
        else:
            return {"answer": "I don't know...", "confidence": confidence}
    
    else:
        return {"answer": "I don't know...", "confidence": confidence}
```

**Code Changes:**
- Location: `kb_answer()` function (line 7418)
- Impact: ~20 lines added
- Risk: LOW (only affects low-confidence queries)
- Validation: Ensure IDK rate drops 45.7% → 35%

**Test Cases:**
```python
# Test 1: Confidence 0.85 → Should return full answer
assert kb_answer("How do I enable 2FA?")["mode"] == "full"

# Test 2: Confidence 0.45, search score 10 → Should return fallback
assert kb_answer("Why did my charge fail?")["mode"] == "fallback"

# Test 3: Confidence 0.35 → Should return IDK
assert "I don't know" in kb_answer("How do I configure quantum tunneling?")["answer"]
```

---

### Phase 2: Response Metadata & Follow-Ups

**Goal:** Add follow-up prompts to medium-confidence answers

**Current Return Type:**
```python
{"answer": "string", "confidence": 0.7, ...}  # No metadata
```

**Proposed New Return Type:**
```python
{
    "answer": "string",
    "confidence": 0.7,
    "mode": "full" | "fallback" | "consulting",
    
    # NEW: Metadata for multi-turn support
    "follow_up": "string?" ,  # Conditional follow-up question
    "context_assumptions": ["list", "of", "assumptions"],  # What we assumed about user
    "is_consulting": bool,  # Whether this is a consulting-mode response
}
```

**Implementation:**
```python
def _compose_answer_with_followup(
    query: str,
    intent: str,
    entities: List[Dict],
    evidence: List[Dict],
    confidence: float,
    explicit_module: str = "General",
) -> Dict:
    """Compose answer + optional follow-up based on confidence."""
    
    answer = _compose_answer(query, intent, entities, evidence, explicit_module)
    
    if confidence >= 0.75:
        # High confidence: full answer, optional follow-up
        return {
            "answer": answer,
            "confidence": confidence,
            "follow_up": None,
            "context_assumptions": [],
        }
    
    elif confidence >= 0.55:
        # Medium confidence: answer + context check
        assumptions = _extract_assumptions(query, entities, evidence)
        follow_up = _generate_context_check(query, assumptions)
        
        return {
            "answer": answer,
            "confidence": confidence,
            "follow_up": follow_up,
            "context_assumptions": assumptions,
            "is_consulting": True,
        }
    
    elif confidence >= 0.35:
        # Low confidence, evidence exists: consulting mode
        assumptions = _extract_assumptions(query, entities, evidence)
        follow_up = _generate_diagnostic_question(query, assumptions)
        
        return {
            "answer": None,
            "confidence": confidence,
            "follow_up": follow_up,
            "context_assumptions": assumptions,
            "is_consulting": True,
        }
    
    else:
        # No confidence: IDK
        return {
            "answer": "I don't know...",
            "confidence": 0.0,
            "follow_up": None,
        }
```

**New Helper Functions Needed:**
```python
def _extract_assumptions(query: str, entities: List[Dict], evidence: List[Dict]) -> List[str]:
    """List what we assumed about user's context."""
    assumptions = []
    
    # Example: if answer assumes basic CLI knowledge
    if intent == "setup" and "command line" in evidence_text.lower():
        assumptions.append("You have basic CLI experience")
    
    # Example: if answer assumes standard scale
    if "small teams" in evidence_text.lower():
        assumptions.append("Your team size is < 50")
    
    return assumptions

def _generate_context_check(query: str, assumptions: List[str]) -> str:
    """Generate follow-up to verify assumptions."""
    if not assumptions:
        return None
    
    # Example: "Quick question to make sure this fits your situation:"
    return f"Quick question to verify this fits your situation: Do you have {assumptions[0]}?"

def _generate_diagnostic_question(query: str, ambiguity_type: str) -> str:
    """Generate diagnostic question for ambiguous queries."""
    
    # Detect ambiguity type from query + evidence
    if "setup" in query.lower() and not _has_use_case_signal(query):
        return "Before I answer—are you setting this up for [use case A] or [use case B]?"
    
    elif "configure" in query.lower() and not _has_scale_signal(query):
        return "How many users/records are you managing?"
    
    # ... more diagnostic patterns ...
```

**Code Changes:**
- Add new functions: _extract_assumptions, _generate_context_check, _generate_diagnostic_question
- Modify _compose_answer return type from str → Dict
- Update kb_answer() to wrap response with metadata
- Impact: ~150 lines added
- Risk: MEDIUM (changes return type, requires UI update)

---

### Phase 3: Consulting Questions for Ambiguous Queries

**Goal:** Ask diagnostic questions instead of IDK for genuinely ambiguous queries

**Pattern Recognition:**
```python
def _is_ambiguous_query(query: str, evidence: List[Dict]) -> bool:
    """Detect if query has multiple valid answers depending on context."""
    
    # Pattern 1: Multi-path decision ("should I use X or Y?")
    if _is_comparison_intent(query):
        return True  # "Use API vs webhooks?" → different answer per use case
    
    # Pattern 2: Context-dependent setup ("how do I set up X?")
    if _is_setup_intent(query) and not _has_contextual_signal(query):
        # Check if evidence covers multiple use cases
        use_cases = _extract_use_cases_from_evidence(evidence)
        return len(use_cases) > 1  # Multiple paths in docs
    
    # Pattern 3: Scale-dependent advice ("what's the best approach?")
    if "best" in query.lower() and not _has_scale_signal(query):
        return True  # "Best way to store data?" depends on volume, latency, etc.
    
    return False
```

**Diagnostic Questions Library:**
```python
DIAGNOSTIC_QUESTIONS = {
    "use_case": [
        "Are you using this for [option A] or [option B]?",
        "Which of these scenarios matches yours: [A], [B], or [C]?",
        "Is your primary goal [A] or [B]?",
    ],
    "scale": [
        "How many users/records are you managing?",
        "What's your current data volume?",
        "Are you optimizing for speed or cost?",
    ],
    "tech_level": [
        "Have you set up [prerequisite] before?",
        "Are you comfortable with APIs?",
        "Do you have engineering support?",
    ],
    "context": [
        "Is this a production system or test?",
        "Are you integrating with [platform]?",
        "What's your timeline for this?",
    ],
}

def _select_diagnostic_question(
    query: str,
    evidence: List[Dict],
    missing_context: str,  # "use_case", "scale", "tech_level", etc.
) -> str:
    """Select appropriate diagnostic question based on missing context."""
    
    questions = DIAGNOSTIC_QUESTIONS.get(missing_context, [])
    
    # Score each question based on query relevance
    best_question = max(
        questions,
        key=lambda q: _similarity_score(query, q)
    )
    
    return best_question
```

**Consulting Mode Flow:**
```python
def _compose_answer_consulting(
    query: str,
    intent: str,
    entities: List[Dict],
    evidence: List[Dict],
    confidence: float,
    user_context: Optional[Dict] = None,
) -> Dict:
    """Consulting mode: ask diagnostic questions instead of IDK."""
    
    if confidence >= 0.6:
        # Confident enough to answer
        answer = _compose_answer(...)
        return {"answer": answer, "confidence": confidence, "mode": "full"}
    
    # Low confidence: check if ambiguous
    if _is_ambiguous_query(query, evidence):
        # Ambiguous: ask diagnostic question
        missing_contexts = _identify_missing_context(query, user_context)
        
        if missing_contexts:
            diagnostic_q = _select_diagnostic_question(
                query, evidence, missing_contexts[0]
            )
            
            return {
                "answer": None,
                "follow_up": diagnostic_q,
                "confidence": 0.4,
                "mode": "consulting",
                "is_consulting": True,
                "expected_next_turn": "user provides context",
            }
    
    # Not ambiguous, just low evidence: IDK
    return {
        "answer": "I don't know...",
        "confidence": 0.0,
        "mode": "idk",
    }
```

**Code Changes:**
- Add DIAGNOSTIC_QUESTIONS dict with patterns
- Add _is_ambiguous_query, _identify_missing_context, _select_diagnostic_question functions
- Modify confidence >= 0.4 tier to route to consulting
- Impact: ~250 lines added
- Risk: MEDIUM (new logic path, requires context tracking)

---

### Phase 4: Context-Gated Confidence Calibration

**Goal:** Adjust confidence based on user context fit, not just retrieval quality

**Context Tracking:**
```python
class ConversationContext:
    """Track user context across turns."""
    
    def __init__(self):
        self.use_case: Optional[str] = None
        self.scale: Optional[str] = None
        self.tech_level: Optional[str] = None
        self.explicit_module: Optional[str] = None
        self.turn_number: int = 0
    
    def update_from_user_input(self, user_message: str):
        """Extract context from user message."""
        self.use_case = _extract_use_case(user_message)
        self.scale = _extract_scale(user_message)
        self.tech_level = _infer_tech_level(user_message)
```

**Context-Aware Confidence:**
```python
def _consulting_confidence(
    query: str,
    evidence: List[Dict],
    user_context: Optional[ConversationContext] = None,
) -> float:
    """
    Confidence = Prob(answer solves user's problem | evidence, context)
    
    Blends:
    - Retrieval quality (does evidence match query?)
    - Context fit (does evidence solve user's specific situation?)
    - Coverage (does evidence address user's constraints?)
    """
    
    if not evidence:
        return 0.0
    
    # Base confidence: retrieval quality
    retrieval_conf = _reported_confidence(query, evidence)  # 0.7*rel + 0.3*score
    
    # Context multiplier: how well does evidence fit user's situation?
    if user_context is None:
        context_fit = 0.60  # Unknown context = lower fit
    else:
        context_fit = 1.0
        
        # Adjust down if user's use case not covered by evidence
        if user_context.use_case:
            use_case_coverage = _does_evidence_cover_use_case(
                evidence, user_context.use_case
            )
            context_fit *= use_case_coverage  # 0.4-1.0
        
        # Adjust down if scale is out of bounds
        if user_context.scale:
            scale_fit = _is_scale_in_documented_range(
                evidence, user_context.scale
            )
            context_fit *= scale_fit  # 0.3-1.0
        
        # Adjust down if prerequisites not met
        if user_context.tech_level == "beginner":
            prereq_coverage = _does_evidence_explain_prerequisites(evidence)
            context_fit *= prereq_coverage  # 0.5-1.0
    
    # Final confidence: blend retrieval + context fit
    # Retrieval dominates (we trust our search), but context is meaningful
    final_confidence = 0.6 * retrieval_conf + 0.4 * context_fit
    
    return min(1.0, max(0.0, final_confidence))
```

**Helper Functions for Context Evaluation:**
```python
def _extract_use_case(user_message: str) -> Optional[str]:
    """Detect use case signal from user input."""
    use_case_patterns = {
        "salesforce": ["salesforce", "crm", "sync"],
        "whatsapp": ["whatsapp", "waba", "messaging"],
        "api": ["api", "http", "webhook", "integration"],
        "personal": ["personal", "hobby", "test", "learning"],
        "enterprise": ["enterprise", "production", "scale", "thousands"],
    }
    
    msg_lower = user_message.lower()
    for use_case, keywords in use_case_patterns.items():
        if any(kw in msg_lower for kw in keywords):
            return use_case
    
    return None

def _does_evidence_cover_use_case(evidence: List[Dict], use_case: str) -> float:
    """Score: [0-1] how well does evidence cover this use case?"""
    
    if not evidence:
        return 0.0
    
    # Check if use case mentioned in top chunks
    evidence_text = "\n".join([str(c.get("text", "")) for c in evidence[:3]])
    
    use_case_keywords = {
        "salesforce": ["salesforce", "crm", "contact", "lead"],
        "whatsapp": ["whatsapp", "waba", "message", "chat"],
        "api": ["api", "http", "endpoint", "request"],
    }
    
    if use_case not in use_case_keywords:
        return 0.7  # Unknown use case, assume moderate coverage
    
    keywords = use_case_keywords[use_case]
    coverage = sum(1 for kw in keywords if kw in evidence_text.lower()) / len(keywords)
    
    return coverage

def _is_scale_in_documented_range(evidence: List[Dict], scale: str) -> float:
    """Score: [0-1] does evidence address user's scale?"""
    
    scale_levels = {
        "small": ["small", "personal", "few", "10", "100"],
        "medium": ["team", "scale", "1000", "10k"],
        "large": ["enterprise", "million", "100k", "scale"],
    }
    
    if scale not in scale_levels:
        return 0.7
    
    evidence_text = "\n".join([str(c.get("text", "")) for c in evidence[:3]])
    
    # Check if evidence discusses this scale level
    keywords = scale_levels[scale]
    mentions = sum(1 for kw in keywords if kw in evidence_text.lower())
    
    return min(1.0, mentions / len(keywords))
```

**Code Changes:**
- Add ConversationContext class
- Add context extraction functions: _extract_use_case, _extract_scale, _infer_tech_level
- Add context evaluation: _does_evidence_cover_use_case, _is_scale_in_documented_range
- Modify _consulting_confidence to blend retrieval + context fit
- Impact: ~300 lines added
- Risk: HIGH (major refactor, requires conversation state tracking)

---

## PART 3: Testing & Validation

### Test Suite for Phase 1-4

**Phase 1 Tests (Soft Gradient):**
```python
def test_phase1_soft_gradient():
    """Verify confidence gradient replaces binary threshold."""
    
    # Test 1: High confidence → full answer
    result = kb_answer("How do I enable 2FA?")
    assert result["confidence"] >= 0.75
    assert result["answer"] is not None
    assert result["answer"] != "I don't know"
    
    # Test 2: Medium confidence → fallback if search found result
    result = kb_answer("Why did my webhook fail?")
    if result["confidence"] >= 0.4 and result["confidence"] < 0.6:
        # Should use search fallback, not IDK
        assert "I don't know" not in result.get("answer", "")
    
    # Test 3: Low confidence, no search result → IDK
    result = kb_answer("How do I configure quantum tunneling?")
    assert result["confidence"] < 0.4 or "I don't know" in result["answer"]

def test_phase1_idk_rate_reduction():
    """Verify IDK rate drops from 45.7% to 35%."""
    
    test_queries = [...]  # 100 queries with known IDK rate
    
    idk_count = sum(1 for q in test_queries if "i don't know" in kb_answer(q)["answer"].lower())
    idk_rate = idk_count / len(test_queries)
    
    assert idk_rate <= 0.35, f"IDK rate {idk_rate} should be <= 0.35"
```

**Phase 2 Tests (Follow-Ups):**
```python
def test_phase2_followup_metadata():
    """Verify response includes follow-up metadata."""
    
    result = kb_answer("How do I configure webhooks?")
    
    assert "follow_up" in result
    assert "context_assumptions" in result
    assert "is_consulting" in result
    
    # Medium confidence should have follow-up
    if 0.4 < result["confidence"] < 0.8:
        assert result.get("follow_up") is not None or result.get("is_consulting") is False
```

**Phase 3 Tests (Consulting Questions):**
```python
def test_phase3_consulting_questions():
    """Verify diagnostic questions for ambiguous queries."""
    
    # Ambiguous query
    result = kb_answer("What's the best way to store data?")
    
    if result["confidence"] < 0.6 and _is_ambiguous_query("What's the best way..."):
        assert result.get("follow_up") is not None
        assert result.get("is_consulting") is True
        assert result.get("answer") is None or result.get("answer") == ""
```

**Phase 4 Tests (Context-Gated Confidence):**
```python
def test_phase4_context_confidence():
    """Verify confidence adjusts based on user context."""
    
    # Same query, different contexts
    query = "How do I configure webhooks?"
    
    # Unknown context
    result1 = kb_answer(query)
    conf1 = result1["confidence"]
    
    # Known context (Salesforce + enterprise)
    result2 = kb_answer(query, user_context={
        "use_case": "salesforce",
        "scale": "large",
    })
    conf2 = result2["confidence"]
    
    # With context, confidence should be higher (if evidence covers it)
    # or lower (if evidence doesn't cover use case)
    assert conf2 != conf1, "Context should affect confidence"
```

---

## PART 4: Rollout Checklist

### Phase 1: Soft Gradient Threshold

- [ ] Modify kb_answer() to use 0.2/0.4/0.6/0.8 gradient instead of 0.5 binary
- [ ] Add search fallback for 0.4-0.6 tier
- [ ] Test IDK rate drops to ~35%
- [ ] Deploy to staging, validate 48 hours
- [ ] Monitor: IDK rate, follow-up rate, satisfaction

### Phase 2: Response Metadata

- [ ] Expand return dict: add follow_up, context_assumptions, is_consulting
- [ ] Implement _extract_assumptions, _generate_context_check
- [ ] Update UI to render follow_up when present
- [ ] Test response structure on 20 queries
- [ ] Deploy to staging, validate 48 hours
- [ ] Monitor: follow-up propensity (target 40%+)

### Phase 3: Consulting Questions

- [ ] Build DIAGNOSTIC_QUESTIONS library (20-30 patterns)
- [ ] Implement _is_ambiguous_query, _identify_missing_context
- [ ] Test consulting questions on 10 ambiguous queries
- [ ] Deploy to staging, validate 1 week
- [ ] Monitor: consulting question engagement (target 60%+ follow-up)

### Phase 4: Context-Gated Confidence

- [ ] Implement ConversationContext class
- [ ] Add context extraction: use case, scale, tech level
- [ ] Implement _consulting_confidence (blend retrieval + context)
- [ ] Test confidence calibration on 50 queries with known outcomes
- [ ] Deploy to staging, validate 1 week
- [ ] Monitor: confidence correlation with satisfaction (target r > 0.65)

---

## PART 5: Code Locations Reference

| Component | Location | Lines | Complexity |
|-----------|----------|-------|-----------|
| kb_answer() entry point | 7418 | 200 | LOW |
| _compose_answer() | 6482 | 130 | MEDIUM |
| _compose_from_evidence() | 6677 | 130 | MEDIUM |
| _reported_confidence() | 5812 | 25 | LOW |
| NEW: _soft_gradient_tier() | TBD | 30 | LOW |
| NEW: _extract_assumptions() | TBD | 40 | MEDIUM |
| NEW: _is_ambiguous_query() | TBD | 50 | MEDIUM |
| NEW: _consulting_confidence() | TBD | 60 | HIGH |
| NEW: ConversationContext | TBD | 40 | MEDIUM |

**Total changes:** ~500-600 lines of code across 4 phases

---

**Next Step:** Start with Phase 1 (soft gradient) for quick IDK reduction, then stage Phase 2-4 over 4 weeks.

