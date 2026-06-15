#!/usr/bin/env python3
import json
import sys
import os
import re

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

# Replicate _has_explicit_support logic with debugging
print("Starting _has_explicit_support check...")

if not evidence:
    print("  No evidence -> return False")
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
initial_check_pass = not (top1.get("score", 0.0) < effective_min and not strong_overlap and not hedged_ok)

print(f"  Initial check: {initial_check_pass}")
if not initial_check_pass:
    print("    -> return False")
    sys.exit(1)

# Unboosted check
has_entity_boost = kb._top_evidence_has_entity_boost(evidence, entities or [])

if not module_match and not has_entity_boost:
    unboosted_floor = kb.MIN_EVIDENCE_SCORE_UNBOOSTED
    if len(evidence) >= 2 and top1_overlap >= 0.25:
        unboosted_floor = kb.MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI

    unboosted_check_pass = not (
        intent != "overview"
        and top1.get("score", 0.0) < unboosted_floor
        and not strong_overlap
        and not hedged_ok
    )
    print(f"  Unboosted check: {unboosted_check_pass}")
    if not unboosted_check_pass:
        print("    -> return False")
        sys.exit(1)

# Topic coverage - this is the key check for intent != overview
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

        coverage_check_pass = kb._evidence_covers_query_topic(query, topic_joined, min_coverage=coverage_threshold)
        print(f"  Coverage check: {coverage_check_pass} (threshold={coverage_threshold})")
        if not coverage_check_pass:
            distinctive = list(set(kb._query_distinctive_tokens(query)))
            j = (topic_joined or "").lower()
            hits = sum(1 for t in distinctive if t in j)
            actual_coverage = hits / len(distinctive) if distinctive else 1.0
            print(f"    Distinctive: {distinctive}")
            print(f"    Coverage: {actual_coverage:.2f}")
            print("    -> return False")
            sys.exit(1)

# Now check the blocks_loose_explicit_support
blocks_loose = kb._blocks_loose_explicit_support(query, intent, joined)
print(f"  blocks_loose_explicit_support: {blocks_loose}")

if not blocks_loose:
    loose_check = top1_overlap >= 0.35 and top1.get("score", 0) >= 2.0
    print(f"    Loose shortcut (overlap>=0.35 && score>=2.0): {loose_check}")
    if loose_check:
        print("    -> return True (loose shortcut)")
        sys.exit(0)

# Setup-specific final check
if intent == "setup":
    long_missing = kb._long_distinctive_terms_missing_from_evidence(query, joined)
    required_missing = kb._setup_evidence_missing_required_terms(query, joined)
    topic_missing = kb._query_topic_not_in_evidence(query, joined)

    print(f"  Setup checks:")
    print(f"    long_distinctive_terms_missing: {long_missing}")
    print(f"    setup_evidence_missing_required_terms: {required_missing}")
    print(f"    query_topic_not_in_evidence: {topic_missing}")

    if long_missing or required_missing or topic_missing:
        print("    -> return False")
        sys.exit(1)

    has_action = any(kb._is_action_oriented(line) for line in lines[:6])
    has_steps_block = any(
        ("steps" in (c.get("heading") or "").lower()
         or "procedure" in (c.get("heading") or "").lower())
        for c in evidence
    )

    core_tokens = [
        t for t in re.findall(r"[a-z0-9&+-]+", kb._normalize_query_for_match(query))
        if len(t) >= 5
        and t not in kb.SCORING_STOP_WORDS
        and t not in {
            "journey", "builder", "studio", "console", "gupshup",
            "steps", "step", "setup", "node", "nodes",
        }
    ]
    core_hits = sum(1 for t in set(core_tokens) if t in joined)

    print(f"    has_action: {has_action}")
    print(f"    has_steps_block: {has_steps_block}")
    print(f"    core_tokens: {core_tokens}")
    print(f"    core_hits: {core_hits}")
    print(f"    overlap: {top1_overlap:.2f}")

    if core_tokens and core_hits == 0 and top1_overlap < 0.45:
        print("    -> return False (core tokens missing)")
        sys.exit(1)

    final_result = ((has_action or has_steps_block) and top1_overlap >= 0.2) or top1_overlap >= 0.45
    print(f"    Final: ((has_action or has_steps_block) and overlap>=0.2) or overlap>=0.45")
    print(f"    Result: {final_result}")
    if final_result:
        print("    -> return True")
        sys.exit(0)
    else:
        print("    -> return False")
        sys.exit(1)

print("  -> return bool(lines) = " + str(bool(lines)))
