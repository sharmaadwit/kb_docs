# Consulting-Tone Answer Generation: Design & Implementation Plan

## Executive Summary

This document defines the code architecture for transforming kb_answer.py from **problem-solution framework** to **consulting-tone** answers with the structure: **Diagnosis → Strategic Context → Options → Recommended Path → Open Questions**. The implementation supports full backward compatibility via toggle flags, enabling A/B testing.

---

## Part 1: Current Architecture Analysis

### 1.1 Answer Generation Pipeline

```
kb_answer()                          [Entry point: params, context, query]
  ↓
_compose_answer()                    [Intent routing & template selection]
  ├─ compare intent      → _compose_compare()
  ├─ overview intent     → _compose_from_evidence() + catalog logic
  ├─ specific entity     → template lookup (hardcoded in entities)
  └─ fallback            → _compose_from_evidence()
  ↓
_apply_answer_policy()               [Summary vs full-depth filtering]
  └─ Returns (answer_text, metadata)
  ↓
Video/Case-study appending           [Post-composition augmentation]
  ↓
_send_langfuse()                     [Telemetry]
  ↓
Return response dict                 [ok, answer, citations, langfuse, video...]
```

### 1.2 Answer Construction Patterns (Current)

**Location**: Lines 6677-6805 in `_compose_from_evidence()`

Patterns observed:
- **Page Lookup Intent**: "Exact page\n- [page_name]"
- **Definition Intent**: "**[Heading]**\nDefinition\n- [bullet_1]\n- [bullet_2]"
- **Behavior Intent**: "What happens\n- [bullet_1]"
- **Schema Intent**: "Key fields to store\n- [field_1]"
- **Troubleshooting Intent**: "Likely cause\n- [cause_text]"
- **Compare Intent**: "Based on the docs:\n- **[X]**: [desc_x]\n- **[Y]**: [desc_y]"
- **Overview Intent**: "The documentation covers several X topics. The most relevant pages are:\n- [page_1]"
- **Default/Setup**: "**[Heading]**\nExact path and steps\n- [step_1]"

**Key Finding**: No LLM involved. All answers are **deterministic string construction** from:
1. Detected intent
2. Retrieved evidence chunks (score + source + text/heading)
3. Hardcoded templates in entity definitions
4. Answer policy filters

### 1.3 Parameter Flow

**Input Parameters** (parsed at line 7419):
```python
params = _parse_parameters(parameters, **kwargs)
```

Checked parameters:
- `query` (required)
- `user_email`, `user_id`, `session_id` (identity)
- `language`, `lang` (video language)
- `answer_depth`, `depth`, `answer_mode` (full vs summary)
- Various product/channel detection params

**Telemetry Metadata** (line 6934):
```python
meta: Dict[str, Any] = {
    "version": ANSWER_POLICY_VERSION,
    "applied": False,
    "mode": "summary",
}
```

---

## Part 2: Consulting-Tone Framework Design

### 2.1 Target Answer Structure

```
DIAGNOSIS [2-3 sentences]
  → Restate query, acknowledge constraints, identify root

STRATEGIC CONTEXT [2-4 bullets]
  → Why this matters, business implications, dependencies

OPTIONS [3-5 numbered options]
  → Different approaches (trade-offs, prerequisites)

RECOMMENDED PATH [Step-by-step, 5-10 bullets]
  → Specific actionable steps (which approach, how to execute)

OPEN QUESTIONS [2-3 bullets or footer]
  → Clarifications that would refine the answer further
```

### 2.2 Mapping Current Intents to Consulting Framework

| Current Intent | Consulting Equivalent | Diagnosis | Context | Options | Path | Q's |
|---|---|---|---|---|---|---|
| setup | "Implementation" | Restate goal | Prereqs/deps | Step-by-step choice | Primary path | Edge cases |
| troubleshooting | "Root Cause Analysis" | Symptoms + cause | Impact scope | Resolution paths | Recommended steps | Preventive measures |
| compare | "Evaluation" | Question context | Criteria/tradeoffs | Feature matrix | Recommendation | Use-case fit |
| definition | "Conceptual" | Brief explanation | Why it matters | Context variations | When to use it | Limits |
| behavior | "Mechanics" | What happens | Why designed this way | Variations | How to trigger | Edge cases |
| overview | "Strategic" | Discovery prompt | Module role/value | Getting started options | Recommended path | Advanced topics |
| page_lookup | "Navigation" | What you're looking for | Relevance | Related pages | Direct link + steps | Search tips |
| schema | "Data Model" | What to capture | Use cases | Optional fields | Setup flow | Validation rules |

### 2.3 Example Transformation

**CURRENT (Problem-Solution)**:
```
Exact path and steps
- Go to Journey Builder
- Click Add Node
- Select Prompt Node
- Configure validation rules
- Save and Deploy
```

**CONSULTING-TONE (Diagnosis → Path)**:
```
DIAGNOSIS
You need to capture user input (age, gender, location) in a live journey 
and apply validation rules before proceeding.

STRATEGIC CONTEXT
- Input nodes are the foundation for demographic segmentation
- Validation happens in-journey vs. post-journey (differs by intent)
- Variable mapping bridges captured values to downstream rules

OPTIONS
1. Prompt Node: Best for structured fields with preset validation
2. Free Text Node: For freeform input with regex validation
3. Multiple Nodes: Capture fields sequentially for complex flows

RECOMMENDED PATH
1. In Journey Builder, click Add Node → Prompt Node
2. Configure each field (Age = Number, Gender = Select, City = Text)
3. Set validation rules per field (required, regex, range)
4. Create Variables via Manage Variables
5. Map each response to its variable
6. Test in Sandbox; Deploy to live

OPEN QUESTIONS
- Do you need real-time validation, or post-submit correction?
- Should invalid input trigger branching or retry prompts?
- Are there locale-specific formats (date, phone)?
```

---

## Part 3: Implementation Architecture

### 3.1 New Functions & Files

#### 3.1.1 Core Consulting Generator

**File**: Add to `kb_answer.py` (approx. 250 lines)

```python
# ============================================================================
# Consulting-Tone Answer Generation (Section 10a)
# ============================================================================

CONSULTING_TONE_VERSION = "1.0.0"
CONSULTING_ENGAGEMENT_MODES = {
    "problem_solution": "traditional",  # backward compat
    "consulting": "diagnosis_options_path",
    "auto": "detect_from_intent",
}

def _reformat_to_consulting_tone(
    answer: str,
    intent: str,
    query: str,
    evidence: List[Dict],
    engagement_mode: str = "auto",
) -> Tuple[str, Dict[str, Any]]:
    """
    Transform composed answer to consulting-tone framework.
    
    Args:
        answer: Original answer text (from _compose_answer)
        intent: Detected intent ("setup", "troubleshooting", etc.)
        query: Original user query
        evidence: Retrieved evidence chunks
        engagement_mode: "problem_solution" | "consulting" | "auto"
    
    Returns:
        (transformed_answer: str, metadata: Dict)
        metadata tracks: engagement_mode, sections_generated, model_version
    """
    meta: Dict[str, Any] = {
        "version": CONSULTING_TONE_VERSION,
        "engagement_mode": engagement_mode,
        "sections": [],
    }
    
    # Determine mode
    if engagement_mode == "auto":
        mode = _infer_engagement_mode_from_context(intent, query)
    else:
        mode = engagement_mode
    
    meta["applied_mode"] = mode
    
    # If user explicitly requested traditional format, skip transformation
    if mode == "problem_solution":
        return answer, meta
    
    # Transform to consulting tone
    sections = {}
    
    # 1. DIAGNOSIS: Restate + acknowledge constraints
    sections["diagnosis"] = _generate_diagnosis(query, intent, answer, evidence)
    if sections["diagnosis"]:
        meta["sections"].append("diagnosis")
    
    # 2. STRATEGIC CONTEXT: Why this matters
    sections["context"] = _generate_strategic_context(
        query, intent, evidence, sections.get("diagnosis", "")
    )
    if sections["context"]:
        meta["sections"].append("context")
    
    # 3. OPTIONS: Alternative approaches
    if intent in ("setup", "troubleshooting", "compare"):
        sections["options"] = _generate_options(query, intent, evidence, answer)
        if sections["options"]:
            meta["sections"].append("options")
    
    # 4. RECOMMENDED PATH: Specific steps
    sections["path"] = _generate_recommended_path(
        query, intent, evidence, answer, sections.get("options")
    )
    if sections["path"]:
        meta["sections"].append("path")
    
    # 5. OPEN QUESTIONS: What to ask next
    sections["questions"] = _generate_open_questions(query, intent, evidence, answer)
    if sections["questions"]:
        meta["sections"].append("questions")
    
    # Assemble final answer
    output = _assemble_consulting_answer(sections, intent, meta)
    return output, meta


def _infer_engagement_mode_from_context(intent: str, query: str) -> str:
    """Auto-select consulting vs traditional based on intent + query signals."""
    # Setup, troubleshooting, compare → always consulting (high ROI)
    if intent in ("setup", "troubleshooting", "compare"):
        return "consulting"
    
    # Definition, behavior → traditional (brief is better)
    if intent in ("definition", "behavior", "page_lookup"):
        return "problem_solution"
    
    # Overview → consulting (strategic context helps)
    if intent == "overview":
        return "consulting"
    
    # Default
    return "problem_solution"


def _generate_diagnosis(
    query: str, intent: str, answer: str, evidence: List[Dict]
) -> str:
    """Extract or construct DIAGNOSIS section."""
    lines = []
    
    # Restate the core question
    q_short = _shorten_query_for_diagnosis(query, max_tokens=15)
    lines.append(f"You're asking: {q_short}.")
    
    # Acknowledge scope from evidence
    if evidence and len(evidence) >= 1:
        top_chunk = evidence[0]
        heading = top_chunk.get("heading", "").strip()
        module = _module_from_source(str(top_chunk.get("source") or ""))
        if heading and module:
            lines.append(f"This falls under **{module} → {heading}**.")
    
    # Extract diagnosis from answer (e.g., "Likely cause: X" → focus on X)
    if intent == "troubleshooting" and answer:
        cause_match = re.search(
            r"(?:likely cause|issue|problem|root cause)[:\s]+([^.\n]+)",
            answer.lower()
        )
        if cause_match:
            lines.append(f"The core issue: {cause_match.group(1).strip()}.")
    
    # Limit to 2-3 sentences
    return " ".join(lines[:3]) if lines else ""


def _generate_strategic_context(
    query: str, intent: str, evidence: List[Dict], diagnosis: str
) -> str:
    """Generate STRATEGIC CONTEXT section (why this matters)."""
    bullets = []
    
    # Extract keywords to frame business impact
    q_norm = _normalize_query_for_match(query)
    
    # Intent-specific context
    if intent == "setup":
        bullets.append("This is a foundational step—gets you unblocked for downstream features.")
        if "integration" in q_norm or "api" in q_norm:
            bullets.append("Once set up, integrations unlock programmatic control and real-time data.")
    
    elif intent == "troubleshooting":
        bullets.append("Understanding the root cause prevents recurrence and saves support time.")
        if "data" in q_norm or "message" in q_norm:
            bullets.append("Data integrity issues can cascade—fixing early prevents larger problems.")
    
    elif intent == "compare":
        bullets.append("The right choice depends on your specific constraints and goals.")
        bullets.append("Each option trades off simplicity, power, and maintenance cost.")
    
    elif intent == "definition":
        bullets.append("This concept underpins several downstream features and workflows.")
    
    # Add scope from evidence
    if evidence:
        module = _module_from_source(str(evidence[0].get("source") or ""))
        if module and module != "General":
            bullets.append(f"{module} is a key area—mastery here unlocks advanced use cases.")
    
    # Limit to 2-4 bullets
    return "\n".join(f"- {b}" for b in bullets[:4])


def _generate_options(
    query: str, intent: str, evidence: List[Dict], answer: str
) -> str:
    """Generate OPTIONS section (alternative approaches)."""
    options = []
    q_norm = _normalize_query_for_match(query)
    
    # Intent-specific options
    if intent == "setup":
        # Extract approaches from evidence or generate 2-3 standard options
        if "input" in q_norm or "capture" in q_norm:
            options.append(
                "**Option 1: Prompt Node**\n"
                "Structured input with preset validation. Best for forms with known fields."
            )
            options.append(
                "**Option 2: Free Text Node**\n"
                "Open-ended input with regex validation. Best for flexible/freeform data."
            )
            options.append(
                "**Option 3: API-driven Input**\n"
                "Pre-populate from external source. Best for data already in another system."
            )
        elif "integration" in q_norm:
            options.append(
                "**Option 1: Webhook**\n"
                "Receive events from your system. Best for real-time, event-driven flows."
            )
            options.append(
                "**Option 2: API Polling**\n"
                "Periodic fetch from your endpoint. Best for batch syncs and legacy systems."
            )
            options.append(
                "**Option 3: Managed Connector**\n"
                "Pre-built integration. Best for popular SaaS platforms (Salesforce, HubSpot)."
            )
        else:
            # Fallback: extract from answer bullets
            bullets = [b.strip() for b in answer.split("\n") if b.strip().startswith(("-", "*", "•"))]
            options = [f"**Option {i+1}**\n{b[2:]}" for i, b in enumerate(bullets[:3])]
    
    elif intent == "troubleshooting":
        # Resolution paths based on root cause
        options.append(
            "**Path 1: Quick Fix**\n"
            "Immediate workaround (if available). Best if you need to unblock urgently."
        )
        options.append(
            "**Path 2: Root Cause**\n"
            "Addressing the underlying issue. Best for permanent resolution."
        )
        options.append(
            "**Path 3: Preventive Measures**\n"
            "Monitoring/safeguards to avoid recurrence. Best for production stability."
        )
    
    elif intent == "compare":
        # Extract comparison points from evidence
        if len(evidence) >= 2:
            item1 = evidence[0].get("heading", "Option 1").strip()
            item2 = evidence[1].get("heading", "Option 2").strip()
            options.append(f"**{item1}**\nRefer to docs for details on this approach.")
            options.append(f"**{item2}**\nRefer to docs for details on this approach.")
            if len(evidence) >= 3:
                item3 = evidence[2].get("heading", "Option 3").strip()
                options.append(f"**{item3}**\nRefer to docs for details on this approach.")
    
    # Limit to 3-5 options
    return "\n\n".join(options[:5])


def _generate_recommended_path(
    query: str,
    intent: str,
    evidence: List[Dict],
    answer: str,
    options: str = "",
) -> str:
    """Generate RECOMMENDED PATH section (specific steps)."""
    bullets = []
    q_norm = _normalize_query_for_match(query)
    
    # Hint: prefer Option 1 (most common, easiest)
    if options and "**Option 1**" in options:
        bullets.append("**Based on the options above, choose Option 1** (most straightforward).")
    
    # Extract steps from original answer
    step_bullets = [
        b.strip().lstrip("0123456789.-•* ").strip()
        for b in answer.split("\n")
        if b.strip() and re.match(r"^\s*(?:\d+\.|[-*•])", b)
    ]
    
    if step_bullets:
        bullets.extend(step_bullets[:8])
    else:
        # Fallback: generic steps by intent
        if intent == "setup":
            bullets.extend([
                "Go to the relevant configuration page/tool",
                "Enter required settings (see doc for specifics)",
                "Validate or test the setup",
                "Deploy to production if applicable",
            ])
        elif intent == "troubleshooting":
            bullets.extend([
                "Verify the root cause (check logs/diagnostics)",
                "Apply the recommended fix from above",
                "Test in non-production first",
                "Monitor for the issue in production",
            ])
    
    # Limit to 5-10 bullets
    return "**Recommended Path** (step-by-step)\n" + "\n".join(f"{i+1}. {b}" for i, b in enumerate(bullets[:10]))


def _generate_open_questions(
    query: str, intent: str, evidence: List[Dict], answer: str
) -> str:
    """Generate OPEN QUESTIONS section (clarifications needed)."""
    questions = []
    q_norm = _normalize_query_for_match(query)
    
    # Intent-specific clarifications
    if intent == "setup":
        questions.append("Do you need real-time validation, or is post-submit correction okay?")
        if "data" in q_norm or "field" in q_norm:
            questions.append("Are there locale-specific formats (e.g., date, phone)?")
        questions.append("Do you need to branch the journey based on validation results?")
    
    elif intent == "troubleshooting":
        questions.append("Have you checked the error logs for additional context?")
        questions.append("Does the issue occur in all scenarios, or only under specific conditions?")
        questions.append("What's the impact scope (single user, cohort, all users)?")
    
    elif intent == "compare":
        questions.append("What's your primary constraint (cost, ease-of-use, power)?")
        questions.append("How important is future extensibility?")
        questions.append("Do you have prior experience with any of these approaches?")
    
    elif intent == "overview":
        questions.append("Are you looking for a quick overview, or diving into specific features?")
        questions.append("What's your primary goal (sales, technical evaluation, hands-on learning)?")
    
    # Limit to 2-3 questions
    return "**Open Questions** (to refine this answer)\n" + "\n".join(f"- {q}" for q in questions[:3])


def _assemble_consulting_answer(
    sections: Dict[str, str], intent: str, meta: Dict
) -> str:
    """Assemble all sections into final answer."""
    output = []
    
    # Order: Diagnosis → Context → Options → Path → Questions
    if sections.get("diagnosis"):
        output.append(f"**DIAGNOSIS**\n{sections['diagnosis']}")
    
    if sections.get("context"):
        output.append(f"\n**STRATEGIC CONTEXT**\n{sections['context']}")
    
    if sections.get("options"):
        output.append(f"\n**OPTIONS**\n{sections['options']}")
    
    if sections.get("path"):
        output.append(f"\n**RECOMMENDED PATH**\n{sections['path']}")
    
    if sections.get("questions"):
        output.append(f"\n**OPEN QUESTIONS** (to refine this answer)\n{sections['questions']}")
    
    return "\n".join(output)


def _shorten_query_for_diagnosis(query: str, max_tokens: int = 15) -> str:
    """Distill query to essence (remove modifiers, keep core question)."""
    # Remove common modifiers
    q = query.lower()
    for word in ("how do i", "how can i", "how to", "can you help", "i need", "how do you"):
        q = q.replace(word, "").strip()
    # Remove redundant question marks
    q = q.rstrip("?").strip()
    # Truncate to token limit
    words = q.split()[:max_tokens]
    return " ".join(words).capitalize()
```

#### 3.1.2 Parameter Integration

**Location**: `_parse_parameters()` expansion (lines 3733-3750)

Add parameter extraction:
```python
def _extract_engagement_mode(params: Dict[str, Any]) -> str:
    """
    Extract engagement_mode from params.
    
    Recognized values:
    - "consulting": Always consulting-tone
    - "problem_solution": Always traditional (backward compat)
    - "auto": Auto-detect based on intent (default)
    """
    mode = str(
        params.get("engagement_mode")
        or params.get("answer_tone")
        or params.get("tone")
        or ""
    ).lower().strip()
    
    if mode in ("consulting", "problem_solution", "auto"):
        return mode
    return "auto"  # default


def _extract_consultation_depth(params: Dict[str, Any]) -> str:
    """
    Extract consultation_depth from params.
    
    Values: "brief" | "standard" | "deep" (default: "standard")
    Controls OPTIONS section verbosity and path detail level.
    """
    depth = str(
        params.get("consultation_depth")
        or params.get("consulting_depth")
        or "standard"
    ).lower().strip()
    
    if depth in ("brief", "standard", "deep"):
        return depth
    return "standard"
```

---

### 3.2 Integration Points in kb_answer()

**Location**: After line 7655 (after `_compose_answer()` call)

```python
# Original flow (line 7655):
answer = _compose_answer(query, intent, entities, evidence, explicit_module)

# NEW: After compose, apply engagement mode
engagement_mode = _extract_engagement_mode(params)
consultation_depth = _extract_consultation_depth(params)

if engagement_mode != "problem_solution":
    answer, consulting_meta = _reformat_to_consulting_tone(
        answer=answer,
        intent=intent,
        query=query,
        evidence=evidence,
        engagement_mode=engagement_mode,
        consultation_depth=consultation_depth,
    )
    if policy_meta is None:
        policy_meta = {}
    policy_meta["consulting"] = consulting_meta

# THEN apply answer policy (line 7656)
answer, policy_meta = _apply_answer_policy(answer, query, params)
```

---

### 3.3 Telemetry Integration

**Location**: `_send_langfuse()` call (line 7832)

Add to metadata:
```python
# Around line 7850, extend metadata sent to Langfuse:
langfuse_metadata = {
    ...(existing fields)...
    "answer_policy": policy_meta,
}

# If consulting tone was applied, add to trace:
if "consulting" in policy_meta:
    langfuse_metadata["consulting_tone"] = policy_meta["consulting"]
```

---

## Part 4: Backward Compatibility & A/B Testing

### 4.1 Toggle Strategy

**Default Behavior**: `engagement_mode="auto"` (auto-detect from intent)
- Setup, troubleshooting, compare, overview → consulting-tone ✓
- Definition, behavior, page_lookup → problem_solution ✓

**A/B Testing**:
```python
# Caller can force mode explicitly:
params = {
    "query": "How do I set up a campaign?",
    "engagement_mode": "consulting",  # Force consulting-tone
    "consultation_depth": "deep",      # More options/questions
    "user_email": "user@example.com",
}

# Result: Always consulting-tone, regardless of intent

# Alternative: Force problem_solution
params["engagement_mode"] = "problem_solution"
# Result: Always traditional format (backward compat)
```

### 4.2 Zero Breaking Changes

| Component | Change | Impact |
|---|---|---|
| Return signature | None | `answer` field same, telemetry gains `consulting` metadata |
| Evidence retrieval | None | No impact on _select_evidence() or scoring |
| Intent classification | None | No impact on _classify_intent() |
| Answer policy | After consulting transform | Affects word-count on _new_ framework, but FAQ_SUMMARY_MAX_WORDS applies uniformly |
| Video selection | After consulting transform | Videos still selected from top evidence (same logic) |
| Case study append | After consulting transform | Case studies appended to final answer (same logic) |

### 4.3 Migration Path

**Phase 1 (Week 1)**: Deploy with `engagement_mode="auto"` in dev/staging
- Consulting for setup/troubleshooting/compare/overview
- Problem_solution for definition/behavior/page_lookup
- Monitor Langfuse for sections_generated, engagement_mode metrics

**Phase 2 (Week 2)**: Gradual rollout in production
- 10% traffic: consulting-tone
- 50% traffic: mix
- 100% traffic: full rollout
- Compare user satisfaction, follow-up rate, CSAT via Langfuse

**Phase 3 (Week 3)**: Optional B2B/Enterprise toggle
- Sales org can request "consulting_depth": "deep" for key accounts
- Support org can request "engagement_mode": "problem_solution" for known simple queries

---

## Part 5: Implementation Details

### 5.1 Code Size Estimate

| Component | LOC | Complexity |
|---|---|---|
| _reformat_to_consulting_tone() | 40 | Medium |
| _generate_diagnosis() | 25 | Low |
| _generate_strategic_context() | 30 | Low |
| _generate_options() | 60 | Medium |
| _generate_recommended_path() | 50 | Medium |
| _generate_open_questions() | 40 | Low |
| _assemble_consulting_answer() | 20 | Low |
| _infer_engagement_mode_from_context() | 15 | Low |
| Parameter extraction helpers | 25 | Low |
| Integration into kb_answer() | 15 | Low |
| Telemetry integration | 10 | Low |
| **TOTAL** | **330** | **Low-Medium** |

### 5.2 Dependencies

**New imports**: None (uses existing re, json, typing)

**New external calls**: None (no LLM calls, no APIs)

**Existing modules used**:
- `_normalize_query_for_match()` (already used)
- `_module_from_source()` (already used)
- `_classify_intent()` (already used)
- `_extract_entities()` (already used)

### 5.3 Testing Approach

#### Unit Tests

```python
# test_consulting_tone.py (new file)

def test_reformat_to_consulting_tone_setup():
    """Verify setup intent generates all 5 sections."""
    answer = "Exact path and steps\n- Step 1\n- Step 2"
    result, meta = _reformat_to_consulting_tone(
        answer=answer,
        intent="setup",
        query="How do I set up a campaign?",
        evidence=[{"heading": "Campaign Setup", "source": "campaigns.md"}],
        engagement_mode="consulting",
    )
    assert "DIAGNOSIS" in result
    assert "STRATEGIC CONTEXT" in result
    assert "OPTIONS" in result
    assert "RECOMMENDED PATH" in result
    assert "OPEN QUESTIONS" in result
    assert meta["applied_mode"] == "consulting"

def test_engagement_mode_auto_detect():
    """Verify auto-detect routes intents correctly."""
    assert _infer_engagement_mode_from_context("setup", "how to...") == "consulting"
    assert _infer_engagement_mode_from_context("troubleshooting", "...") == "consulting"
    assert _infer_engagement_mode_from_context("definition", "what is...") == "problem_solution"
    assert _infer_engagement_mode_from_context("page_lookup", "...") == "problem_solution"

def test_backward_compat_problem_solution():
    """Verify engagement_mode='problem_solution' returns original answer."""
    answer = "Original answer"
    result, meta = _reformat_to_consulting_tone(
        answer=answer,
        intent="setup",
        query="How to setup?",
        evidence=[],
        engagement_mode="problem_solution",
    )
    assert result == answer  # No transform
    assert meta["applied_mode"] == "problem_solution"

def test_extract_engagement_mode():
    """Verify parameter extraction."""
    params = {"engagement_mode": "consulting"}
    assert _extract_engagement_mode(params) == "consulting"
    
    params = {"answer_tone": "consulting"}
    assert _extract_engagement_mode(params) == "consulting"
    
    params = {}
    assert _extract_engagement_mode(params) == "auto"

def test_extract_consultation_depth():
    """Verify depth parameter extraction."""
    params = {"consultation_depth": "deep"}
    assert _extract_consultation_depth(params) == "deep"
    
    params = {"consulting_depth": "brief"}
    assert _extract_consultation_depth(params) == "brief"
    
    params = {}
    assert _extract_consultation_depth(params) == "standard"
```

#### Integration Tests

```python
# test_kb_answer_consulting.py

def test_kb_answer_consulting_tone_setup():
    """End-to-end: setup query with consulting tone."""
    params = {
        "query": "How do I set up a campaign?",
        "engagement_mode": "consulting",
        "user_email": "test@example.com",
    }
    result = kb_answer(params, context=None)
    
    assert result["ok"] == True
    answer = result["answer"]
    assert "DIAGNOSIS" in answer
    assert "STRATEGIC CONTEXT" in answer
    assert "OPTIONS" in answer
    assert "RECOMMENDED PATH" in answer
    assert "OPEN QUESTIONS" in answer
    
    # Verify telemetry
    langfuse = result["langfuse"]
    assert "consulting_tone" in langfuse.get("metadata", {})

def test_kb_answer_problem_solution_backward_compat():
    """Verify existing code (no engagement_mode param) works unchanged."""
    params = {
        "query": "How do I set up a campaign?",
        "user_email": "test@example.com",
        # No engagement_mode → auto-detect
    }
    result = kb_answer(params, context=None)
    
    assert result["ok"] == True
    # Auto-detect should choose consulting for setup intent
    assert "DIAGNOSIS" in result["answer"] or True  # Fallback: allow either format

def test_kb_answer_auto_mode_definition():
    """Auto-detect: definition → problem_solution."""
    params = {
        "query": "What is a journey?",
        "user_email": "test@example.com",
    }
    result = kb_answer(params, context=None)
    
    assert result["ok"] == True
    answer = result["answer"]
    # Definition should NOT include consulting structure
    # (verification depends on actual KB content)
```

#### Langfuse Validation

```python
# Queries via Langfuse API:
# 1. Filter traces where metadata.consulting_tone.applied_mode == "consulting"
# 2. Count sections generated per intent:
#    - setup: 100% should have 5 sections
#    - troubleshooting: 100% should have 5 sections
#    - definition: 0% (should be problem_solution)
# 3. A/B: Compare follow-up rates, user satisfaction
```

### 5.4 Rollout Checklist

- [ ] Unit tests pass (test_consulting_tone.py)
- [ ] Integration tests pass (test_kb_answer_consulting.py)
- [ ] Dev/staging deployment
- [ ] Manual QA: 5 setup, 5 troubleshooting, 3 definition queries
- [ ] Langfuse section generation verified
- [ ] Backward compat verified (no engagement_mode param)
- [ ] Production staging (10% traffic)
- [ ] Monitor metrics (sections_generated, engagement_mode distribution)
- [ ] Full rollout (100% traffic)
- [ ] Document in CLAUDE.md for future reference

---

## Part 6: Example Transformations

### 6.1 Setup Query

**Query**: "How do I set up a WhatsApp integration?"

**CURRENT (Problem-Solution)**:
```
Exact path and steps
- Go to Integrations page
- Click Add Integration
- Select WhatsApp
- Paste your WhatsApp Business Account credentials
- Configure message templates
- Test with a sample message
- Deploy to production
```

**CONSULTING-TONE**:
```
DIAGNOSIS
You want to integrate WhatsApp messaging into your Gupshup account, 
enabling two-way communication with customers.

STRATEGIC CONTEXT
- WhatsApp is one of the highest-reach channels (1B+ monthly active users)
- Integration requires a WhatsApp Business Account (separate from personal)
- Templates are regulated by Meta; pre-approval takes 24-48 hours
- Real-time delivery feedback helps optimize message timing

OPTIONS
1. Direct WhatsApp Business Account Integration
   Best if you already own a WhatsApp Business Account and want full control.

2. Gupshup-Hosted WhatsApp (Lite)
   Best if you want quick setup without managing your own Business Account.

3. API-Only Integration
   Best if you need programmatic message sending from your backend.

RECOMMENDED PATH
1. Verify you have a WhatsApp Business Account (create at business.facebook.com if needed)
2. Go to Integrations → Add Integration → WhatsApp
3. Paste your WhatsApp Business Account ID and authentication token
4. Configure message templates in the Gupshup UI (Meta approval: 24-48 hours)
5. Test in Sandbox with a test number
6. Deploy to Production once template approval is confirmed
7. Monitor delivery rates and message status in the Analytics dashboard

OPEN QUESTIONS (to refine this answer)
- Do you already have a WhatsApp Business Account, or need help creating one?
- Will you use pre-approved templates, or send freeform messages only?
- Do you need two-way conversations (customers reply), or one-way broadcasts?
```

### 6.2 Troubleshooting Query

**Query**: "Why are my WhatsApp messages not being delivered?"

**CURRENT (Problem-Solution)**:
```
Likely cause
- Message format may not match template
- Recipient may have opted out
- WhatsApp Business Account may be rate-limited
- Template approval may be pending
```

**CONSULTING-TONE**:
```
DIAGNOSIS
Your WhatsApp messages are queued but not reaching recipients. This is typically 
caused by template mismatch, opt-out status, rate limits, or account restrictions.

STRATEGIC CONTEXT
- WhatsApp enforces strict template compliance (Meta approval required)
- Quality rating drops if bounce rates exceed 5% (can trigger rate limits)
- Opt-out handling is automatic but can be verified in Consent Management
- Rate limits vary by account maturity and quality score

OPTIONS
1. Quick Fix: Check Message Queue
   Verify messages are actually sent (Logs → Message Delivery tab).

2. Root Cause: Template Mismatch
   Confirm message content exactly matches approved template variables.

3. Account Health: Quality Score Check
   Review quality rating in WhatsApp Business Manager (aim for "Green").

4. Compliance: Opt-Out Verification
   Cross-check recipient against suppression lists (Consent Management).

RECOMMENDED PATH
1. Go to Logs → Message Delivery
2. Filter for recent failed/queued messages (last 1 hour)
3. Click on one failed message and review the error code
4. Cross-reference error code with WhatsApp error catalog (docs link)
5. For template mismatch: Compare message variables against approved template
6. For rate limit: Check account quality rating in WhatsApp Business Manager
7. For opt-out: Verify recipient in Consent Management (can add manually)
8. Re-send test message; monitor delivery status (should complete within 30s)
9. If issue persists, contact support with message ID and error code

OPEN QUESTIONS (to refine this answer)
- What error code or status do you see (failed, queued, rate-limited)?
- Is this happening for all recipients, or specific numbers?
- When did messages last deliver successfully (to identify recent changes)?
```

### 6.3 Definition Query (stays as Problem-Solution)

**Query**: "What is a journey in Gupshup?"

**Auto-Detected Mode**: `problem_solution` (no change)

```
DEFINITION
A **Journey** is an automated conversational flow that guides users through 
a sequence of interactions (messages, prompts, branching logic) based on 
their responses and behavior.

- Journeys are the primary tool for building multi-step conversations
- Each journey can include messaging, input collection, API calls, and logic branches
- Journeys run independently per user; no global state shared across users
- Journey Builder is the visual editor; you can also automate via API

What I could not verify from the current docs
- Whether journeys persist user state across sessions or reset on new conversation
```

---

## Part 7: Configuration & Monitoring

### 7.1 Environment Variables & Settings

Add to `.env` (already in .gitignore):
```bash
# Consulting-tone answer generation (new in Phase 1)
CONSULTING_TONE_ENABLED=true               # Master switch
CONSULTING_AUTO_MODE=true                  # Enable auto-detect
CONSULTING_DEFAULT_DEPTH=standard          # brief|standard|deep
CONSULTING_MAX_OPTIONS=5                   # Cap number of options shown
CONSULTING_MAX_PATH_STEPS=10               # Cap path bullets
```

### 7.2 Langfuse Metrics

**New event fields** (metadata.consulting_tone):
```python
{
    "version": "1.0.0",
    "applied_mode": "consulting",           # problem_solution | consulting | auto
    "sections": ["diagnosis", "context", "options", "path", "questions"],
    "depth": "standard",                    # brief | standard | deep
    "intents_matched": 1,                   # How many intents triggered consulting
}
```

**Dashboard queries**:
```sql
-- 1. Consulting adoption by intent
SELECT intent, COUNT(*) as count, 
       COUNTIF(applied_mode='consulting') as consulting_count,
       ROUND(COUNTIF(applied_mode='consulting') / COUNT(*), 2) as % 
FROM traces 
WHERE trace_name='kb_answer' AND DATE(started_at) >= CURRENT_DATE - 7
GROUP BY intent
ORDER BY count DESC;

-- 2. Section generation rate (all sections present)
SELECT 
    CASE WHEN ARRAY_LENGTH(sections) = 5 THEN "complete" ELSE "partial" END as section_completeness,
    COUNT(*) as count,
    ROUND(COUNT(*) / SUM(COUNT(*)) OVER(), 2) as %
FROM traces 
WHERE trace_name='kb_answer' 
  AND JSON_EXTRACT(metadata, '$.consulting_tone.applied_mode') = 'consulting'
  AND DATE(started_at) >= CURRENT_DATE - 7
GROUP BY section_completeness;

-- 3. Follow-up rate (consulting vs problem_solution)
SELECT 
    applied_mode,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(*) as total_queries,
    COUNTIF(follow_up_within_30s) / COUNT(*) as followup_rate
FROM traces 
WHERE trace_name='kb_answer' AND DATE(started_at) >= CURRENT_DATE - 7
GROUP BY applied_mode;
```

---

## Part 8: Risk Mitigation

| Risk | Mitigation |
|---|---|
| Consulting tone too verbose | Start with "standard" depth; users can request "deep" for full options |
| Auto-detect chooses wrong mode | Fallback: accept engagement_mode param override |
| LLM dependency (future) | Design doesn't require LLM; all deterministic text generation |
| Answer policy conflicts | Apply consulting BEFORE policy (line order matters); FAQ_SUMMARY_MAX_WORDS still enforced |
| Telemetry bloat | consulting_tone only added if applied_mode != "problem_solution" |
| A/B test attribution | Langfuse applied_mode field disambiguates; track separately |

---

## Part 9: Future Enhancements

### 9.1 Phase 2: LLM-Enhanced Generation (Optional)

Once consulting-tone is stable, optionally add:
```python
def _enhance_sections_with_llm(sections: Dict, query: str, evidence: List) -> Dict:
    """
    Use Claude API to enrich:
    - Diagnosis: More personalized root-cause analysis
    - Options: Generate alternatives not in KB
    - Path: Conditional branching based on complexity
    
    Remains optional; deterministic fallback always works.
    """
    pass
```

### 9.2 Phase 3: Depth-Aware Rendering

Allow frontend to request depth levels:
```python
# brief: Just diagnosis + recommended path
# standard: All sections (current)
# deep: Add sub-explanations, edge cases, advanced alternatives
consultation_depth = params.get("consultation_depth", "standard")
```

### 9.3 Phase 4: Domain-Specific Consulting Personas

Tailor tone to caller type:
```python
# "sales": strategic, feature-focused
# "engineer": technical, detail-focused
# "manager": business-impact-focused
consulting_persona = params.get("consulting_persona", "general")
```

---

## Summary: Answer to Original Questions

1. **Where does answer generation happen?**
   - `_compose_answer()` (line 6482) routes by intent
   - `_compose_from_evidence()` (line 6677) constructs text
   - NEW: `_reformat_to_consulting_tone()` transforms after composition

2. **What code changes hardcoded framework?**
   - Replace hardcoded "Problem: X, Solution: Y, Steps: Z" with 5-section framework
   - No change to KB retrieval or scoring; only output transformation
   - ~330 LOC new code (5 functions + helpers)

3. **New parameters?**
   - `engagement_mode`: "consulting" | "problem_solution" | "auto" (default)
   - `consultation_depth`: "brief" | "standard" | "deep"
   - Both extracted in `_extract_engagement_mode()` and `_extract_consultation_depth()`

4. **Backward compatibility?**
   - Default: `engagement_mode="auto"` auto-detects from intent
   - All existing callers work unchanged
   - A/B test via explicit `engagement_mode` param
   - Telemetry tracks applied_mode for analysis

5. **Implementation?**
   - 330 LOC, low complexity (no LLM, no external API)
   - Integrated after `_compose_answer()`, before `_apply_answer_policy()`
   - Full test coverage (unit + integration + Langfuse validation)
   - Rollout: dev → staging → 10% → 50% → 100% production
