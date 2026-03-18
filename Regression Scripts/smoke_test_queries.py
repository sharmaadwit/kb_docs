"""
Smoke test: run curated single-intent, multi-intent, and negative queries
through kb_answer.py to verify expected entity extraction, intent, and answers.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import kb_answer as kba

# ---------------------------------------------------------------------------
# Build synthetic chunks (same as local_regression_test.py)
# ---------------------------------------------------------------------------
def _build_synthetic_chunks():
    chunks = []
    seen_slugs = set()
    for concept in kba.CONCEPT_REGISTRY:
        cid = concept["id"]
        display = concept.get("display", cid)
        module = concept.get("module", "General")
        page_display = concept.get("page_display", display)
        for slug in concept.get("source_boosts", {}).keys():
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)
            source_path = f"kb/{module.lower().replace(' ', '-')}/{slug}.md"
            heading = page_display
            heading_path = [f"# {page_display}"]
            setup_template = concept.get("templates", {}).get("setup", "")
            page_template = concept.get("templates", {}).get("page_lookup", "")
            behavior_template = concept.get("templates", {}).get("behavior", "")
            text_body = setup_template or page_template or behavior_template or f"Documentation for {display}."
            text = f"source_url: https://console-docs.gupshup.io/docs/{slug}\n# {page_display}\n\n{text_body}"
            chunks.append({
                "source": source_path, "path": source_path,
                "heading": heading, "heading_path": heading_path,
                "text": text, "chunk_id": f"{slug}#L0",
                "section_type": "general",
            })
            aliases_text = ", ".join(concept.get("aliases", [])[:5])
            if aliases_text:
                chunks.append({
                    "source": source_path, "path": source_path,
                    "heading": f"{page_display} — Overview",
                    "heading_path": heading_path + [f"## Overview"],
                    "text": f"This page covers: {aliases_text}. Module: {module}.",
                    "chunk_id": f"{slug}#L1",
                    "section_type": "concept",
                })
    for ps in kba.GLOBAL_PENALTY_SOURCES:
        if ps not in seen_slugs:
            seen_slugs.add(ps)
            chunks.append({
                "source": f"kb/general/{ps}.md", "path": f"kb/general/{ps}.md",
                "heading": ps, "heading_path": [f"# {ps}"],
                "text": f"General page: {ps}.",
                "chunk_id": f"{ps}#L0", "section_type": "general",
            })
    return chunks

SYNTHETIC_CHUNKS = _build_synthetic_chunks()
kba._load_chunks = lambda ctx: SYNTHETIC_CHUNKS


# ---------------------------------------------------------------------------
# Smoke test queries
# ---------------------------------------------------------------------------
SMOKE_TESTS = [
    # --- Single intent ---
    {
        "id": "S1", "type": "single",
        "query": "Where do I configure business hours?",
        "expect_entities": ["business_hours"],
        "expect_intent": "page_lookup",
        "expect_answer_contains": ["business hours"],
    },
    {
        "id": "S2", "type": "single",
        "query": "What is sticky assignment?",
        "expect_entities": ["sticky_assignment"],
        "expect_intent": "definition",
        "expect_answer_contains": ["sticky assignment"],
    },
    {
        "id": "S3", "type": "single",
        "query": "How do I test my bot before going live?",
        "expect_entities": ["test_your_bot"],
        "expect_intent": "setup",
        "expect_answer_contains": ["test your bot"],
    },
    {
        "id": "S4", "type": "single",
        "query": "What does Goal Achieved mean in goal analytics?",
        "expect_entities": ["goal_analytics"],
        "expect_intent": "definition",
        "expect_answer_contains": ["goal"],
    },
    {
        "id": "S5", "type": "single",
        "query": "Where do I add a webhook callback URL?",
        "expect_entities": ["webhooks"],
        "expect_intent": "page_lookup",
        "expect_answer_contains": ["webhook"],
    },
    {
        "id": "S6", "type": "single",
        "query": "How do I collect text user input in a journey?",
        "expect_entities": ["prompt_node"],
        "expect_intent": "setup",
        "expect_answer_contains": ["prompt node"],
    },
    {
        "id": "S7", "type": "single",
        "query": "What happens when a prompt node times out?",
        "expect_entities": ["prompt_timeout"],
        "expect_intent": "behavior",
        "expect_answer_contains": ["timeout"],
    },
    {
        "id": "S8", "type": "single",
        "query": "Which dashboard shows ongoing chats and wait time metrics?",
        "expect_entities": ["live_monitoring"],
        "expect_intent": "page_lookup",
        "expect_answer_contains": ["live monitoring"],
    },

    # --- Multi-intent / Compare ---
    {
        "id": "M1", "type": "compare",
        "query": "Should I check business hours or auto replies for away messages?",
        "expect_entities": ["business_hours", "auto_replies"],
        "expect_intent": "compare",
        "expect_answer_contains": ["business hours", "auto replies"],
    },
    {
        "id": "M2", "type": "compare",
        "query": "What is the difference between save and save & deploy?",
        "expect_entities": ["save_deploy"],
        "expect_intent": "compare",
        "expect_answer_contains": ["save"],
    },
    {
        "id": "M3", "type": "compare",
        "query": "Which page shows campaign click metrics vs goal conversions?",
        "expect_entities": ["campaign_analytics", "goal_analytics"],
        "expect_intent": "compare",
        "expect_answer_contains": ["campaign", "goal"],
    },
    {
        "id": "M4", "type": "compare",
        "query": "Should I debug in test your bot first or check the live channel?",
        "expect_entities": ["test_your_bot"],
        "expect_intent": "setup",
        "expect_answer_contains": ["test your bot"],
    },
    {
        "id": "M5", "type": "compare",
        "query": "Where do I configure sticky assignment vs assignment rules?",
        "expect_entities": ["sticky_assignment", "assignment_rules"],
        "expect_intent": "compare",
        "expect_answer_contains": ["assignment"],
    },
    {
        "id": "M6", "type": "compare",
        "query": "CTWA traffic or campaign analytics — where do I check conversions?",
        "expect_entities": ["ctwa_to_goals", "campaign_analytics"],
        "expect_intent": "compare",
        "expect_answer_contains": ["ctwa", "campaign"],
    },

    # --- Negative / Off-topic ---
    {
        "id": "N1", "type": "negative",
        "query": "How do I make pizza?",
        "expect_entities": [],
        "expect_intent": None,
        "expect_answer_contains": ["can't help", "can help only"],
    },
    {
        "id": "N2", "type": "negative",
        "query": "What is the weather today?",
        "expect_entities": [],
        "expect_intent": None,
        "expect_answer_contains": ["can't help", "can help only"],
    },
    {
        "id": "N3", "type": "negative",
        "query": "Tell me about Salesforce CRM integrations",
        "expect_entities": [],
        "expect_intent": None,
        "expect_answer_contains": ["can't help", "can help only"],
    },
    {
        "id": "N4", "type": "negative",
        "query": "How do I hack into the admin panel?",
        "expect_entities": [],
        "expect_intent": None,
        "expect_answer_contains": ["can't help", "can help only"],
    },
]


# ---------------------------------------------------------------------------
# Run tests
# ---------------------------------------------------------------------------
def run():
    print("=" * 70)
    print("SMOKE TEST — entity extraction, intent classification, answers")
    print("=" * 70)

    passed = 0
    failed = 0
    results = []

    for test in SMOKE_TESTS:
        tid = test["id"]
        query = test["query"]
        ttype = test["type"]

        # Entity extraction
        entities = kba._extract_entities(query)
        entity_ids = [e["id"] for e in entities]

        # Intent classification
        intent = kba._classify_intent(query, entities)

        # Full answer
        try:
            result = kba.kb_answer({"query": query}, context=None)
            answer = result.get("answer", "")
        except Exception as exc:
            answer = f"ERROR: {exc}"

        answer_low = answer.lower()

        # Check expectations
        issues = []

        # Entity check
        for expected_ent in test["expect_entities"]:
            if expected_ent not in entity_ids:
                issues.append(f"missing entity '{expected_ent}' (got: {entity_ids[:4]})")

        # Intent check (skip for negative)
        if test["expect_intent"] and intent != test["expect_intent"]:
            issues.append(f"intent='{intent}' expected='{test['expect_intent']}'")

        # Answer content check
        if ttype == "negative":
            has_refusal = any(p in answer_low for p in [
                "i can't help", "i can help only", "i don't have",
                "outside the scope", "not something i can",
            ])
            if not has_refusal:
                issues.append(f"expected refusal, got: {answer[:80]}")
        else:
            for keyword in test["expect_answer_contains"]:
                if keyword.lower() not in answer_low:
                    issues.append(f"answer missing '{keyword}'")

        status = "PASS" if not issues else "FAIL"
        if status == "PASS":
            passed += 1
        else:
            failed += 1

        results.append({
            "id": tid, "type": ttype, "status": status,
            "query": query,
            "entities_found": entity_ids[:5],
            "intent": intent,
            "answer_preview": answer[:150],
            "issues": issues,
        })

        icon = "OK" if status == "PASS" else "XX"
        print(f"\n[{icon}] {tid} ({ttype}): {query[:70]}")
        print(f"     entities: {entity_ids[:5]}")
        print(f"     intent:   {intent}")
        if issues:
            for iss in issues:
                print(f"     ISSUE: {iss}")
        print(f"     answer:   {answer[:120]}")

    print("\n" + "=" * 70)
    print(f"SMOKE TEST RESULTS: {passed} passed, {failed} failed out of {len(SMOKE_TESTS)}")
    print("=" * 70)

    out_path = os.path.join(os.path.dirname(__file__), "artifacts", "smoke_test_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed results: {out_path}")


if __name__ == "__main__":
    run()
