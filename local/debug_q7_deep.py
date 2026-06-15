#!/usr/bin/env python3
"""Deep debug of Q7 to understand all failure points."""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skill"))
import kb_answer as kb

CHUNKS_PATH = os.path.join(os.path.dirname(__file__), "..", "kb", "kb_chunks.jsonl")

def _load_chunks():
    items = []
    with open(CHUNKS_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    items.append(json.loads(line))
                except Exception:
                    pass
    return items

CACHED_CHUNKS = _load_chunks()

query = "How do I configure a WABA in the Gupshup Console and register webhook endpoints?"

print(f"Query: {query}\n")

# Prep
chunks = CACHED_CHUNKS
explicit_module = kb._detect_module(query)
entities = kb._extract_entities(query)
intent = kb._classify_intent(query, entities)

scored = []
for c in chunks:
    s = kb._score_chunk(query, c, entities, explicit_module)
    if s > 0:
        row = dict(c)
        row["score"] = s
        scored.append(row)
scored.sort(key=lambda x: x.get("score", 0.0), reverse=True)

evidence = kb._select_evidence(query, scored, intent, explicit_module)
lines = kb._evidence_lines(evidence)

print(f"Module: {explicit_module}")
print(f"Intent: {intent}")
print(f"Entities: {entities}")
print(f"Evidence: {len(evidence)} chunks")
for e in evidence:
    print(f"  - {e['source']}: {e['score']:.2f}")

# Manual _has_explicit_support walk-through
if not evidence:
    print("\nNo evidence -> False")
    sys.exit(1)

top1 = evidence[0]
top_source_mod = kb._module_from_source(str(top1.get("source") or ""))
module_match = (
    explicit_module != "General"
    and top_source_mod.lower() == explicit_module.lower()
)

top1_overlap = kb._query_overlap_score(query, top1)
strong_overlap = top1_overlap >= 0.7 and top1.get("score", 0.0) >= 0.5
hedged_ok = (
    (top1_overlap >= 0.7 and top1.get("score", 0.0) >= 0.5)
    or (top1_overlap >= 0.5 and top1.get("score", 0.0) >= 0.85)
)

effective_min = 0.8 if module_match else kb.MIN_EVIDENCE_SCORE
initial_pass = not (top1.get("score", 0.0) < effective_min and not strong_overlap and not hedged_ok)

print(f"\nInitial checks:")
print(f"  module_match: {module_match}")
print(f"  top1_overlap: {top1_overlap:.2f}")
print(f"  strong_overlap: {strong_overlap}")
print(f"  hedged_ok: {hedged_ok}")
print(f"  effective_min: {effective_min}")
print(f"  top1.score: {top1.get('score', 0.0):.2f}")
print(f"  -> initial_pass: {initial_pass}")

if not initial_pass:
    print("\nFailed initial check!")
    sys.exit(1)

# Unboosted check
has_entity_boost = kb._top_evidence_has_entity_boost(evidence, entities or [])

if not module_match and not has_entity_boost:
    unboosted_floor = kb.MIN_EVIDENCE_SCORE_UNBOOSTED
    if len(evidence) >= 2 and top1_overlap >= 0.25:
        unboosted_floor = kb.MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI

    unboosted_pass = not (
        intent != "overview"
        and top1.get("score", 0.0) < unboosted_floor
        and not strong_overlap
        and not hedged_ok
    )

    print(f"\nUnboosted check (module_match={module_match}, entity_boost={has_entity_boost}):")
    print(f"  unboosted_floor: {unboosted_floor}")
    print(f"  -> unboosted_pass: {unboosted_pass}")

    if not unboosted_pass:
        print("\nFailed unboosted check!")
        sys.exit(1)

# Topic coverage check
joined = "\n".join(lines).lower()
source_text = " ".join(str(c.get("source") or "").lower() for c in evidence)
topic_joined = joined + "\n" + source_text

qn = kb._normalize_query_for_match(query)
if not kb._is_agent_assist_api_inventory_query(qn):
    if intent != "overview":
        if intent == "setup":
            coverage_threshold = 0.15 if module_match else 0.3
        else:
            coverage_threshold = 0.2 if module_match else 0.4

        coverage_pass = kb._evidence_covers_query_topic(query, topic_joined, min_coverage=coverage_threshold)

        print(f"\nTopic coverage check (intent=setup):")
        print(f"  coverage_threshold: {coverage_threshold}")
        print(f"  -> coverage_pass: {coverage_pass}")

        if not coverage_pass:
            distinctive = list(set(kb._query_distinctive_tokens(query)))
            j = (topic_joined or "").lower()
            hits = sum(1 for t in distinctive if t in j)
            actual_coverage = hits / len(distinctive) if distinctive else 1.0
            print(f"  Distinctive tokens: {distinctive}")
            print(f"  Coverage: {hits}/{len(distinctive)} = {actual_coverage:.2f}")
            print("\nFailed coverage check!")
            sys.exit(1)

# Setup-specific checks
print(f"\nSetup-specific checks:")
print(f"  long_distinctive_terms_missing: {kb._long_distinctive_terms_missing_from_evidence(query, joined)}")
print(f"  setup_evidence_missing_required_terms: {kb._setup_evidence_missing_required_terms(query, joined)}")
print(f"  query_topic_not_in_evidence: {kb._query_topic_not_in_evidence(query, joined)}")

if kb._long_distinctive_terms_missing_from_evidence(query, joined):
    print("\nFailed: long_distinctive_terms_missing")
    sys.exit(1)

if kb._setup_evidence_missing_required_terms(query, joined):
    print("\nFailed: setup_evidence_missing_required_terms")
    sys.exit(1)

if kb._query_topic_not_in_evidence(query, joined):
    print("\nFailed: query_topic_not_in_evidence")
    sys.exit(1)

# Final setup logic
has_action = any(kb._is_action_oriented(line) for line in lines[:6])
has_steps_block = any(
    ("steps" in (c.get("heading") or "").lower()
     or "procedure" in (c.get("heading") or "").lower())
    for c in evidence
)

final_result = ((has_action or has_steps_block) and top1_overlap >= 0.2) or top1_overlap >= 0.45

print(f"\nFinal setup logic:")
print(f"  has_action: {has_action}")
print(f"  has_steps_block: {has_steps_block}")
print(f"  top1_overlap: {top1_overlap:.2f}")
print(f"  -> result: {final_result}")

if not final_result:
    print("\nFailed final setup logic!")
    sys.exit(1)

print("\n✅ All checks passed!")
