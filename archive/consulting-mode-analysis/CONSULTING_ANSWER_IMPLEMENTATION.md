# Consulting-Tone Answer Implementation Guide

**Date:** 2026-08-11  
**Purpose:** Technical specifications for adding consulting-tone answers to `kb_answer.py`  
**Audience:** Engineering team (Python, Langfuse integration)

---

## Overview

This guide shows how to integrate the consulting-tone framework into the existing `kb_answer.py` system without breaking current functionality. The approach is **opt-in**, allowing gradual rollout.

---

## Part 1: High-Level Architecture

### Current Flow
```
query → kb_answer() 
  → _compose_answer() 
    → [template/evidence-based] → string answer
  → [apply policy] 
    → final answer (string)
```

### Proposed Flow (with Consulting Mode)
```
query → kb_answer(answer_mode="consulting"|"solution") 
  → if mode == "consulting": 
      _compose_consulting_answer()
  → else: 
      _compose_answer() [current]
  → [apply policy] 
    → final answer (string)
```

### Entry Points for Consulting Mode

1. **Parameter-based** (from API caller):
   ```python
   kb_answer(query, answer_mode="consulting")  # opt-in
   kb_answer(query)  # defaults to "solution" (current)
   ```

2. **Policy-based** (automatic):
   ```python
   if _policy_should_use_consulting_mode(query, intent, evidence):
       return _compose_consulting_answer(...)
   ```

3. **User-driven** (from query language):
   ```python
   if "which approach" in query.lower() or "trade-offs" in query.lower():
       return _compose_consulting_answer(...)
   ```

---

## Part 2: Data Structures

### New: `ConsultingAnswer` Dataclass

```python
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ConsultingAnswer:
    """Structured consulting-tone answer."""
    
    # DIAGNOSIS: What scenario is this?
    diagnosis: str  # "Based on your question about X, I'm seeing..."
    diagnosis_scenarios: List[str]  # ["Scenario A", "Scenario B", "Scenario C"]
    
    # STRATEGIC CONTEXT: Why does it matter?
    strategic_context: str  # "Why this matters: [business impact]..."
    business_outcome: str  # "revenue", "retention", "cost", "risk", "speed"
    
    # MULTIPLE APPROACHES: Paths with trade-offs
    approaches: List[Dict]  # See structure below
    
    # RECOMMENDED PATH: Starting point
    recommended_approach_id: int  # Index into approaches[]
    recommendation_reasoning: str  # "I'd typically start with X because..."
    evolution_path: Optional[str]  # "Once you see Y, try Z"
    
    # OPEN QUESTIONS: Unknowns
    open_questions: List[Dict]  # See structure below
    open_question_categories: List[str]  # ["Audience & Scale", "Business Priority", ...]
    
    # METADATA
    confidence_level: str  # "HIGH", "MEDIUM", "LOW"
    confidence_reasoning: str  # "Backed by 10+ case studies" or "Limited coverage"
    kb_evidence_count: int  # How many KB chunks support this?
    persona_detected: Optional[str]  # "startup", "enterprise", "agency", etc.
    tone_markers_used: List[str]  # ["I'm seeing", "Trade-offs", "Worth exploring"]


@dataclass
class ConsultingApproach:
    """Single path/approach within answer."""
    
    id: int  # Approach 1, 2, 3, ...
    name: str  # e.g., "RCS-First + SMS Safety Net"
    description: str  # "What it is" (1-2 sentences)
    
    preconditions: List[str]  # "When it works best"
    # e.g., ["High-value campaigns", "Audience 60%+ RCS-capable"]
    
    strengths: List[str]  # 2-3 benefits
    trade_offs: List[str]  # 2-3 explicit costs
    risks: List[str]  # Edge cases or failure modes
    
    implementation_complexity: str  # "Low", "Medium", "High"
    implementation_steps: List[str]  # Numbered steps (if applicable)
    
    example_scenario: str  # "Fashion retailer, 45% revenue lift…"
    example_metric: Optional[str]  # "78% conversion uplift" or "30% reduction in support tickets"
    
    data_dependency: Optional[str]  # "Requires audience segmentation data"
    timeline_dependency: Optional[str]  # "Meta Flow approval (5-10 days)"


@dataclass
class ConsultingOpenQuestion:
    """Single question to refine recommendation."""
    
    id: int  # Question order
    category: str  # "Audience & Scale", "Business Priority", etc.
    question: str  # "What's your current RCS reach?"
    why_it_matters: str  # "Determines channel priority"
    example_answer_a: str  # "We're under 40% RCS reach"
    example_answer_b: str  # "We're above 60% RCS reach"
    impact_if_a: str  # "SMS-Dominant is smarter"
    impact_if_b: str  # "RCS-First is better"
```

### Approach Selection Logic

```python
def select_consulting_approaches(
    query: str,
    intent: str,
    entities: List[Dict],
    evidence: List[Dict],
    explicit_module: str = "General",
) -> List[ConsultingApproach]:
    """
    Choose 2-3 approaches based on query intent and evidence.
    
    Logic:
    - intent="setup" → implementation paths (approach A, approach B, approach C)
    - intent="compare" → comparison strategies (when to use each)
    - intent="troubleshooting" → diagnosis paths (likely cause vs. edge cases)
    - intent="overview" → architecture paths (high-level strategies)
    """
    approaches = []
    
    # Example for setup intent: "How to capture demographics?"
    if intent == "setup" and entities:
        primary_entity = entities[0]
        
        # Rule: If entity is "prompt_node" or "form-like", offer 3 capture strategies
        if primary_entity.get("id") in ["prompt_node", "whatsapp_flow", "free_text_node"]:
            approaches = [
                ConsultingApproach(
                    id=1,
                    name="Minimal In-Journey Capture",
                    description="Ask only questions that branch bot logic",
                    preconditions=["Clear bot branches", "Mobile-first audience"],
                    strengths=["Fast UX (30-45 seconds)", "Clear intent", "High completion"],
                    trade_offs=["Separate sequential inputs", "Feels less native"],
                    risks=["If fields don't branch logic, dropout rises 25-40%"],
                    implementation_complexity="Low",
                    example_scenario="E-commerce bot captures age (product recs) + city (shipping)",
                    example_metric="65% completion rate"
                ),
                ConsultingApproach(
                    id=2,
                    name="WhatsApp Flow (Native Form)",
                    description="Use Meta's Flows for single-screen form UX",
                    preconditions=["4-6 demographic fields needed", "Can handle Meta approval"],
                    strengths=["Native form UX", "Higher completion (50-75%)", "Mobile app–like"],
                    trade_offs=["Meta approval required (5-10 days)", "New tool to learn"],
                    risks=["Approval delays", "Updates need re-approval"],
                    implementation_complexity="Medium",
                    timeline_dependency="5-10 days for Meta approval",
                    example_scenario="Banking bot captures KYC via Flow",
                    example_metric="72% completion rate"
                ),
                ConsultingApproach(
                    id=3,
                    name="Phased Capture (Progressive Profiling)",
                    description="Capture 1-2 fields now, add more later in conversation",
                    preconditions=["First-time heavy audience", "Long customer lifetime"],
                    strengths=["Lowest friction on first touch", "Progressive trust", "High volume friendly"],
                    trade_offs=["Longer time to complete profile", "Complex flow logic"],
                    risks=["Must re-ask skipped fields later"],
                    implementation_complexity="High",
                    example_scenario="E-commerce captures age (msg 1), city (msg 3)",
                    example_metric="92% first-message, 75% three-message completion"
                ),
            ]
    
    return approaches or []
```

---

## Part 3: Core Function: `_compose_consulting_answer()`

### Function Signature

```python
def _compose_consulting_answer(
    query: str,
    intent: str,
    entities: List[Dict],
    evidence: List[Dict],
    explicit_module: str = "General",
) -> str:
    """
    Main consulting-tone answer composition.
    
    Flow:
    1. Detect scenario from query language (diagnosis)
    2. Build strategic context (why it matters)
    3. Select 2-3 approaches with trade-offs
    4. Pick recommended starting point
    5. Surface open questions
    6. Return formatted answer
    """
    
    # Step 1: DIAGNOSIS — What's the customer's actual situation?
    diagnosis = _diagnose_customer_scenario(query, intent, entities)
    scenarios = diagnosis.get("scenarios", [])
    persona = diagnosis.get("persona")  # "startup", "enterprise", etc.
    
    # Step 2: STRATEGIC CONTEXT — Why does the answer matter?
    strategy = _build_strategic_context(query, intent, evidence, persona)
    business_outcome = strategy.get("outcome")  # "revenue", "retention", etc.
    context_text = strategy.get("text")
    
    # Step 3: SELECT APPROACHES — What are the viable paths?
    approaches = select_consulting_approaches(query, intent, entities, evidence)
    if not approaches:
        # Fallback: If no consulting paths, use current logic
        return _compose_answer(query, intent, entities, evidence, explicit_module)
    
    # Step 4: RECOMMEND STARTING POINT
    recommended_idx = _rank_approaches_for_recommendation(
        approaches, persona, business_outcome, entities, evidence
    )
    recommended_approach = approaches[recommended_idx]
    recommendation_text = _format_recommendation(recommended_approach, approaches)
    
    # Step 5: OPEN QUESTIONS — What unknowns refine this?
    open_questions = _generate_open_questions(
        query, intent, entities, recommended_approach, approaches
    )
    
    # Step 6: FORMAT & RETURN
    answer_parts = [
        _format_diagnosis(diagnosis),
        _format_strategic_context(strategy),
        _format_approaches(approaches, recommended_idx),
        _format_recommendation(recommended_approach, approaches),
        _format_open_questions(open_questions),
    ]
    
    return "\n\n".join(filter(None, answer_parts))
```

### Helper Functions

#### 1. Diagnosis Detection

```python
def _diagnose_customer_scenario(
    query: str, intent: str, entities: List[Dict]
) -> Dict[str, Any]:
    """
    Infer customer's actual situation from query language.
    
    Returns:
    {
        "scenarios": ["Scenario A", "Scenario B"],
        "persona": "startup",  # or "enterprise", "agency", "freelancer"
        "scale_signal": "low",  # "low" (<1K), "medium" (1K-100K), "high" (100K+)
        "urgency_signal": "high",  # "low", "medium", "high"
        "stage_signal": "planning",  # "planning", "live", "optimizing", "scaling"
    }
    """
    q = _normalize_query_for_match(query)
    signals = {}
    
    # PERSONA DETECTION
    if any(w in q for w in ["startup", "small team", "bootstrapped", "lean"]):
        signals["persona"] = "startup"
    elif any(w in q for w in ["enterprise", "large scale", "10k+", "100k+"]):
        signals["persona"] = "enterprise"
    elif any(w in q for w in ["agency", "client", "clients"]):
        signals["persona"] = "agency"
    else:
        signals["persona"] = "generic"
    
    # SCALE SIGNAL
    if any(w in q for w in ["million", "100k+", "enterprise", "scale"]):
        signals["scale_signal"] = "high"
    elif any(w in q for w in ["thousand", "small", "initial"]):
        signals["scale_signal"] = "low"
    else:
        signals["scale_signal"] = "medium"
    
    # URGENCY SIGNAL
    if any(w in q for w in ["urgent", "asap", "today", "now", "immediately", "holiday", "peak"]):
        signals["urgency_signal"] = "high"
    elif any(w in q for w in ["upcoming", "next week", "soon"]):
        signals["urgency_signal"] = "medium"
    else:
        signals["urgency_signal"] = "low"
    
    # STAGE SIGNAL
    if any(w in q for w in ["how do", "setup", "configure", "deploy", "launch"]):
        signals["stage_signal"] = "planning"
    elif any(w in q for w in ["already", "currently", "live", "running", "deployed"]):
        signals["stage_signal"] = "live"
    elif any(w in q for w in ["optimize", "improve", "performance", "best practice"]):
        signals["stage_signal"] = "optimizing"
    elif any(w in q for w in ["scale", "100x", "growth", "millions"]):
        signals["stage_signal"] = "scaling"
    
    # SCENARIOS (intent-specific)
    scenarios = _match_scenarios_for_intent(intent, signals, query)
    signals["scenarios"] = scenarios
    
    return signals


def _match_scenarios_for_intent(intent: str, signals: Dict, query: str) -> List[str]:
    """
    Map detected signals to scenario labels.
    
    Example for setup intent:
    - If stage is "planning" + urgency is "high" → "Time-pressured initial setup"
    - If stage is "live" + scale is "high" → "Optimizing at scale"
    """
    scenarios = []
    
    if intent == "setup":
        if signals.get("urgency_signal") == "high" and signals.get("stage_signal") == "planning":
            scenarios.append("Time-pressured initial setup")
        if signals.get("scale_signal") == "high" and signals.get("stage_signal") == "live":
            scenarios.append("Optimizing at scale")
        if signals.get("persona") == "startup":
            scenarios.append("Resource-constrained implementation")
    
    if intent == "compare":
        if "trade" in query.lower() or "pros and cons" in query.lower():
            scenarios.append("Weighing options before decision")
        if "already using" in query.lower():
            scenarios.append("Considering migration or multi-channel")
    
    if intent == "troubleshooting":
        if signals.get("urgency_signal") == "high":
            scenarios.append("Production incident, high impact")
        if signals.get("scale_signal") == "high":
            scenarios.append("Scaled system with emergent issues")
    
    return scenarios or ["General scenario"]
```

#### 2. Strategic Context

```python
def _build_strategic_context(
    query: str, intent: str, evidence: List[Dict], persona: str
) -> Dict[str, Any]:
    """
    Extract "Why this matters" from KB evidence + business logic.
    
    Returns:
    {
        "outcome": "revenue",  # or "retention", "cost", "risk", "speed"
        "text": "Strategic context paragraph",
        "metrics": ["Metric A", "Metric B"],
    }
    """
    context = {}
    
    # Infer business outcome from intent + query
    if intent == "setup" and any(w in query.lower() for w in ["conversion", "sales", "revenue"]):
        context["outcome"] = "revenue"
        context["text"] = (
            "Why this matters: Setup quality directly impacts conversion rates. "
            "A poor implementation can cause 20-30% higher dropout or 2x slower performance."
        )
    elif intent == "setup" and any(w in query.lower() for w in ["retention", "loyalty", "repeat"]):
        context["outcome"] = "retention"
        context["text"] = (
            "Why this matters: Retention flows need fast, reliable delivery. "
            "Latency or errors reduce trust and cause churn."
        )
    elif intent == "compare":
        context["outcome"] = "cost"
        context["text"] = (
            "Why this matters: Channel choice affects cost per message, delivery speed, and user experience. "
            "The wrong choice can 2-3x your messaging costs or reduce engagement significantly."
        )
    
    # Extract business metrics from KB evidence
    metrics = []
    for ev in evidence[:3]:
        text = str(ev.get("text") or "")
        if "%" in text or "x" in text:
            # Try to extract numeric metrics
            import re
            numbers = re.findall(r"(\d+(?:\.\d+)?[%x]?)\s+(open rate|conversion|lift|improvement)", text.lower())
            metrics.extend([f"{num[0]} {num[1]}" for num in numbers[:2]])
    
    context["metrics"] = metrics[:3]
    return context
```

#### 3. Approach Ranking

```python
def _rank_approaches_for_recommendation(
    approaches: List[ConsultingApproach],
    persona: str,
    business_outcome: str,
    entities: List[Dict],
    evidence: List[Dict],
) -> int:
    """
    Rank approaches and return index of best starting point.
    
    Ranking logic:
    - Startup persona → Prefer Low complexity
    - High urgency → Prefer low timeline_dependency
    - High scale → Prefer approaches that scale
    - Revenue outcome → Prefer high-impact approaches
    """
    scores = []
    
    for i, approach in enumerate(approaches):
        score = 0
        
        # Persona fit
        if persona == "startup" and approach.implementation_complexity == "Low":
            score += 3
        elif persona == "enterprise" and approach.implementation_complexity == "High":
            score += 2
        
        # Timeline dependency (prefer no dependencies if urgent)
        if not approach.timeline_dependency:
            score += 2
        
        # Scale fit
        if business_outcome == "revenue":
            if any("conversion" in s.lower() for s in approach.strengths):
                score += 2
        elif business_outcome == "retention":
            if any("retention" in s.lower() or "trust" in s.lower() for s in approach.strengths):
                score += 2
        
        # Generally prefer lower complexity as starting point
        if approach.implementation_complexity == "Low":
            score += 1
        
        scores.append((score, i))
    
    # Return index of highest-scoring approach
    if scores:
        return max(scores, key=lambda x: x[0])[1]
    return 0  # Default to first approach
```

#### 4. Question Generation

```python
def _generate_open_questions(
    query: str,
    intent: str,
    entities: List[Dict],
    recommended_approach: ConsultingApproach,
    all_approaches: List[ConsultingApproach],
) -> List[ConsultingOpenQuestion]:
    """
    Generate 3-5 questions to refine the recommendation.
    
    Logic: Ask about preconditions for recommended approach + differentiate between approaches.
    """
    questions = []
    question_id = 1
    
    # Category 1: AUDIENCE & SCALE
    if "scale" in [p.lower() for ap in all_approaches for p in ap.preconditions]:
        questions.append(ConsultingOpenQuestion(
            id=question_id,
            category="Audience & Scale",
            question="How many users are you targeting in this campaign?",
            why_it_matters="Determines whether complexity is worth it (low scale = keep it simple)",
            example_answer_a="Under 1,000",
            example_answer_b="10,000+",
            impact_if_a="Approach 1 (simple) is better",
            impact_if_b="Approach 2 or 3 (more sophisticated) justified"
        ))
        question_id += 1
    
    # Category 2: BUSINESS PRIORITY
    if len(all_approaches) > 1:
        questions.append(ConsultingOpenQuestion(
            id=question_id,
            category="Business Priority",
            question="What's more important right now—speed to launch or optimal user experience?",
            why_it_matters="Drives choice between Low-complexity paths vs. High-polish paths",
            example_answer_a="Speed (launch this week)",
            example_answer_b="Experience (can wait 2 weeks)",
            impact_if_a=f"Approach 1 ({all_approaches[0].implementation_complexity} complexity) works",
            impact_if_b=f"Approach 2 ({all_approaches[1].implementation_complexity} complexity) better"
        ))
        question_id += 1
    
    # Category 3: OPS & INTEGRATION
    if any("integration" in str(ap.data_dependency or "") for ap in all_approaches):
        questions.append(ConsultingOpenQuestion(
            id=question_id,
            category="Ops & Integration",
            question="Do you have journey orchestration set up, or starting from scratch?",
            why_it_matters="Multi-channel approaches require message sequencing logic",
            example_answer_a="Starting from scratch",
            example_answer_b="Already orchestrating journeys",
            impact_if_a="Simpler single-channel path is better",
            impact_if_b="Can leverage multi-channel if needed"
        ))
        question_id += 1
    
    return questions[:5]  # Limit to 5 questions
```

---

## Part 4: Formatting Functions

```python
def _format_diagnosis(diagnosis: Dict) -> str:
    """Format diagnosis section (optional; can be skipped for brevity)."""
    if not diagnosis.get("scenarios"):
        return ""
    
    scenarios = diagnosis.get("scenarios", [])
    if len(scenarios) == 1:
        return f"**Understanding Your Scenario**\nI'm seeing: {scenarios[0]}."
    
    return (
        "**Understanding Your Scenario**\n"
        "This question typically comes from one of these situations:\n"
        + "\n".join(f"- {s}" for s in scenarios)
    )


def _format_strategic_context(strategy: Dict) -> str:
    """Format strategic context section."""
    text = strategy.get("text", "")
    if not text:
        return ""
    
    parts = [text]
    metrics = strategy.get("metrics", [])
    if metrics:
        parts.append("Key context:\n" + "\n".join(f"- {m}" for m in metrics))
    
    return "\n\n".join(parts)


def _format_approaches(approaches: List[ConsultingApproach], recommended_idx: int) -> str:
    """Format all approaches with trade-offs."""
    lines = ["## Viable Approaches"]
    
    for i, ap in enumerate(approaches):
        is_recommended = (i == recommended_idx)
        marker = "✅ RECOMMENDED STARTING POINT" if is_recommended else f"Option {i + 1}"
        
        lines.append(f"\n**{marker}: {ap.name}**")
        lines.append(f"*{ap.description}*")
        
        lines.append("\n**When it works best:**")
        lines.extend(f"- {p}" for p in ap.preconditions)
        
        lines.append("\n**Strengths:**")
        lines.extend(f"- {s}" for s in ap.strengths)
        
        lines.append("\n**Trade-offs:**")
        lines.extend(f"- {t}" for t in ap.trade_offs)
        
        if ap.risks:
            lines.append("\n**Risks:**")
            lines.extend(f"- {r}" for r in ap.risks)
        
        lines.append(f"\n**Complexity:** {ap.implementation_complexity}")
        
        if ap.example_scenario:
            lines.append(f"\n**Example:** {ap.example_scenario}")
            if ap.example_metric:
                lines.append(f"*Result: {ap.example_metric}*")
    
    return "\n".join(lines)


def _format_recommendation(recommended: ConsultingApproach, all_approaches: List) -> str:
    """Format the recommended starting point."""
    lines = [
        "\n## Recommended Starting Point",
        f"I'd typically start with **{recommended.name}** because:",
    ]
    
    # Add 2-3 reason bullets
    lines.append(f"- {recommended.preconditions[0] if recommended.preconditions else 'Solid fit for your scenario'}")
    if len(recommended.strengths) > 0:
        lines.append(f"- {recommended.strengths[0]}")
    if recommended.implementation_complexity != "High":
        lines.append(f"- You can get results fast ({recommended.implementation_complexity} complexity)")
    
    # Add evolution path if relevant
    if len(all_approaches) > 1:
        other_approaches = [a for i, a in enumerate(all_approaches) if i != 0]
        if other_approaches:
            next_approach = other_approaches[0]
            lines.append(
                f"\nOnce you see results here, you can evolve to **{next_approach.name}** "
                f"if [specific condition happens]."
            )
    
    return "\n".join(lines)


def _format_open_questions(questions: List[ConsultingOpenQuestion]) -> str:
    """Format open questions by category."""
    if not questions:
        return ""
    
    lines = ["\n## To Refine This Recommendation"]
    lines.append("It helps to know:")
    
    # Group by category
    by_category = {}
    for q in questions:
        if q.category not in by_category:
            by_category[q.category] = []
        by_category[q.category].append(q)
    
    for category, qs in by_category.items():
        lines.append(f"\n**{category}**")
        for q in qs:
            lines.append(f"- {q.question}")
            if q.why_it_matters:
                lines.append(f"  *(Helps determine: {q.why_it_matters})*")
    
    return "\n".join(lines)
```

---

## Part 5: Integration with `kb_answer()`

### Modified `kb_answer()` Signature

```python
def kb_answer(
    parameters: object = None,
    context=None,
    correlation_id: Optional[str] = None,
    parent_trace_id: Optional[str] = None,
    answer_mode: str = "solution",  # NEW: "solution" or "consulting"
    **kwargs
) -> dict:
    """
    Main KB answer function (modified).
    
    Args:
        answer_mode: "solution" (current behavior) or "consulting" (new)
    """
    # ... existing setup code ...
    
    # Parse query, entities, evidence (existing)
    query = str(parameters.get("query", "")).strip()
    entities = kb_entities(query)
    evidence = kb_search(query)
    intent = _infer_intent(query)
    
    # NEW: Check if should use consulting mode
    if answer_mode == "consulting" or _policy_should_use_consulting_mode(query, intent, evidence):
        answer_text = _compose_consulting_answer(query, intent, entities, evidence)
    else:
        answer_text = _compose_answer(query, intent, entities, evidence)
    
    # Apply policy (existing)
    final_answer = _apply_answer_policy(answer_text, query, intent)
    
    return {
        "answer": final_answer,
        "mode": answer_mode,
        "evidence_count": len(evidence),
        **metadata
    }
```

### Policy: Auto-Enable Consulting Mode

```python
def _policy_should_use_consulting_mode(query: str, intent: str, evidence: List[Dict]) -> bool:
    """
    Heuristic: When to auto-enable consulting mode without explicit parameter.
    
    Auto-enable for:
    - Compare intent (natural for consulting)
    - Setup with 3+ entities (complex decision)
    - Troubleshooting with low confidence (alternative paths useful)
    - User explicitly asks for trade-offs or options
    """
    q = _normalize_query_for_match(query)
    
    # Explicit ask
    if any(phrase in q for phrase in ["trade-off", "pros and cons", "options", "approaches"]):
        return True
    
    # Intent-based
    if intent == "compare":
        return True  # Always consult for comparisons
    
    # Complexity-based
    if intent == "setup" and evidence and len(evidence) >= 3:
        # Multiple valid paths exist
        return True
    
    return False
```

---

## Part 6: Testing & Validation

### Unit Tests

```python
def test_consulting_answer_structure():
    """Test that consulting answer has all required sections."""
    answer = _compose_consulting_answer(
        query="How to capture demographics in a WhatsApp bot?",
        intent="setup",
        entities=[{"id": "prompt_node", "display": "Prompt Node"}],
        evidence=[
            {"text": "Use Prompt Node for free text input", "score": 1.0, "source": "setup-page"},
            {"text": "Number Node validates numeric input", "score": 0.95, "source": "setup-page"},
        ]
    )
    
    # Check sections
    assert "What I'm" in answer or "scenario" in answer.lower()  # Diagnosis
    assert "Why this matters" in answer or "strategic" in answer.lower()  # Context
    assert "Approach" in answer  # Multiple paths
    assert "recommended" in answer.lower() or "I'd typically" in answer.lower()  # Recommendation
    assert "refine" in answer.lower() or "helps to know" in answer.lower()  # Questions


def test_consulting_confidence_levels():
    """Test confidence tagging in consulting answers."""
    answer = _compose_consulting_answer(...)
    
    # Should have confidence language
    confidence_words = ["documented", "case studies", "tested", "proven", "limited coverage", "uncertain"]
    assert any(w in answer.lower() for w in confidence_words)
```

### Langfuse Integration

Track new metrics for consulting answers:

```python
# In Langfuse observation for answer
observation = {
    "name": "kb_answer",
    "input": query,
    "output": answer_text,
    "metadata": {
        "answer_mode": "consulting",  # NEW
        "approaches_offered": 3,  # NEW
        "questions_offered": 5,  # NEW
        "recommended_approach_id": 1,  # NEW
        "confidence_level": "HIGH",  # NEW
        "kb_evidence_count": 8,  # NEW
    }
}
```

---

## Part 7: Rollout Plan

### Phase 1: Pilot (Week 1)
- [ ] Implement core functions (Diagnosis, Strategic Context, Approaches)
- [ ] Test on 5 setup + 2 compare queries manually
- [ ] Verify formatting and tone
- [ ] **Metrics:** Does answer feel advisory, not prescriptive?

### Phase 2: Gradual Rollout (Weeks 2-3)
- [ ] Enable `_policy_should_use_consulting_mode()` for compare intent (always)
- [ ] Monitor Langfuse for answer length, user engagement, follow-up rates
- [ ] Gather feedback from 10-20 users
- [ ] **Metrics:** Click-through rate on follow-ups, satisfaction scores

### Phase 3: Full Scale (Week 4+)
- [ ] Enable for setup + compare + overview intents (majority of queries)
- [ ] Keep option to pass `answer_mode="solution"` for users who prefer old style
- [ ] Update dashboard to track consulting vs. solution mode adoption
- [ ] **Metrics:** User retention, repeat query rate, NPS

---

## Success Criteria

| Criterion | Target |
|-----------|--------|
| **Answer completeness** | 4+ sections (diagnosis, context, paths, recommendations) |
| **Readability** | <15 minute read time; scannable with headers |
| **Engagement** | 40%+ of consulting answers prompt follow-up questions |
| **Accuracy** | Zero regressions vs. current system (same or better) |
| **Performance** | <500ms additional latency for consulting composition |

---

## References

- `CONSULTING_TONE_FRAMEWORK.md` — Full framework and mock answers
- `kb_answer.py` — Current implementation (lines 6482-6700)
- `local/reports/RCS_CONSULTING_QUESTIONS_TEST.md` — Real consulting Q&A examples
- Langfuse dashboard — Track metrics for consulting vs. solution mode

