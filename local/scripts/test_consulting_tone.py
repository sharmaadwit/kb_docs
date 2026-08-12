#!/usr/bin/env python3
"""
Unit tests for consulting-tone answer generation (Phase 1: RCS + Bot Studio pilot).
Run: python3 local/scripts/test_consulting_tone.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

from skill.kb_answer import (
    _compose_consulting_answer,
    _resolve_answer_mode,
    _gate_module_for_consulting,
)


def make_evidence(heading, text, score=2.0, source="rcs/setup.json"):
    return {"heading": heading, "text": text, "score": score, "source": source}


COMPOSER_CASES = [
    {
        "name": "high_confidence_setup",
        "query": "how do I enable RCS on my account",
        "intent": "setup",
        "module": "RCS",
        "confidence": 0.8,
        "evidence": [make_evidence("Enable RCS", "Go to Settings > Channels > RCS and toggle Enable.", score=3.5)],
        "expect_contains": ["toggle Enable", "Most common case"],
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
                "When RCS is unavailable, the message automatically falls back to SMS so delivery still works.",
                score=3.5,
            ),
            make_evidence(
                "MMS Fallback",
                "Rich media automatically falls back to MMS if RCS fallback to SMS cannot support it, so delivery still works.",
                score=3.5,
            ),
        ],
        "expect_contains": ["vary depending on your setup", "SMS Fallback", "Tell me more"],
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
    {
        "name": "bot_studio_conditional_low_confidence",
        "query": "how do I build a journey with conditional branching",
        "intent": "setup",
        "module": "Bot Studio",
        "confidence": 0.35,
        "evidence": [
            make_evidence(
                "Single Condition Routing",
                "To build a journey with a single conditional branch, use a Decision node with one condition to branch the journey.",
                score=3.5,
                source="bot-studio/patterns.json",
            ),
            make_evidence(
                "Multiple Condition Routing",
                "To build a journey with complex conditional branching, combine AND/OR logic in a Decision node to branch multiple paths.",
                score=3.5,
                source="bot-studio/patterns.json",
            ),
        ],
        "expect_contains": ["vary depending on your setup", "Bot Studio"],
        "expect_not_contains": ["I don't know"],
    },
]

GATE_MODULE_CASES = [
    {
        "name": "rcs_query_channels_bucket_resolves_to_RCS",
        "query": "how do I send an RCS campaign",
        "explicit_module": "Channels",
        "expect": "RCS",
    },
    {
        "name": "non_rcs_channels_query_stays_Channels",
        "query": "how do I connect my Instagram channel",
        "explicit_module": "Channels",
        "expect": "Channels",
    },
    {
        "name": "bot_studio_explicit_module_passthrough",
        "query": "how do I build a journey builder flow",
        "explicit_module": "Bot Studio",
        "expect": "Bot Studio",
    },
    {
        "name": "whatsapp_module_passthrough_unaffected",
        "query": "how do I send a whatsapp template message",
        "explicit_module": "WhatsApp",
        "expect": "WhatsApp",
    },
    {
        "name": "campaign_flavored_rcs_query_resolves_to_RCS",
        "query": "should I use RCS or WhatsApp for my campaign",
        "explicit_module": "Campaign Manager",
        "expect": "RCS",
    },
    {
        "name": "non_rcs_campaign_query_stays_Campaign_Manager",
        "query": "how do I schedule a campaign send for tomorrow",
        "explicit_module": "Campaign Manager",
        "expect": "Campaign Manager",
    },
]

MODE_RESOLUTION_CASES = [
    {
        "name": "disabled_by_default_returns_standard",
        "env": {},
        "query": "how do I send an RCS campaign",
        "explicit_module": "Channels",
        "expect": "standard",
    },
    {
        "name": "enabled_but_module_not_in_allowlist_returns_standard",
        "env": {"KB_CONSULTING_TONE_ENABLED": "1", "KB_CONSULTING_TONE_MODULES": "Bot Studio"},
        "query": "how do I send an RCS campaign",
        "explicit_module": "Channels",
        "expect": "standard",
    },
    {
        "name": "explicit_force_override_wins",
        "env": {"KB_ANSWER_MODE": "consulting"},
        "query": "anything",
        "explicit_module": "General",
        "expect": "consulting",
    },
    {
        "name": "deterministic_same_query_same_mode",
        "env": {"KB_CONSULTING_TONE_ENABLED": "1", "KB_CONSULTING_TONE_MODULES": "Bot Studio", "KB_CONSULTING_TONE_PCT": "50"},
        "query": "how do I build a journey with conditional branching",
        "explicit_module": "Bot Studio",
        "expect": None,  # checked via repeat-call comparison below, not a fixed value
    },
]


def run():
    passed = 0
    failed = 0

    for case in COMPOSER_CASES:
        try:
            answer = _compose_consulting_answer(
                query=case["query"],
                intent=case["intent"],
                entities=[],
                evidence=case["evidence"],
                explicit_module=case["module"],
                confidence=case["confidence"],
            )
            for phrase in case.get("expect_contains", []):
                assert phrase.lower() in answer.lower(), f"Missing: {phrase!r}\nGot: {answer}"
            for phrase in case.get("expect_not_contains", []):
                assert phrase.lower() not in answer.lower(), f"Unexpected: {phrase!r}\nGot: {answer}"
            print(f"PASS composer:{case['name']}")
            passed += 1
        except Exception as e:
            print(f"FAIL composer:{case['name']}: {e}")
            failed += 1

    for case in GATE_MODULE_CASES:
        try:
            result = _gate_module_for_consulting(case["query"], case["explicit_module"])
            assert result == case["expect"], f"Expected {case['expect']!r}, got {result!r}"
            print(f"PASS gate_module:{case['name']}")
            passed += 1
        except Exception as e:
            print(f"FAIL gate_module:{case['name']}: {e}")
            failed += 1

    for case in MODE_RESOLUTION_CASES:
        try:
            saved = {}
            for k in ("KB_ANSWER_MODE", "KB_CONSULTING_TONE_ENABLED", "KB_CONSULTING_TONE_MODULES", "KB_CONSULTING_TONE_PCT"):
                saved[k] = os.environ.pop(k, None)
            for k, v in case["env"].items():
                os.environ[k] = v

            if case["name"] == "deterministic_same_query_same_mode":
                r1 = _resolve_answer_mode({}, case["query"], case["explicit_module"])
                r2 = _resolve_answer_mode({}, case["query"], case["explicit_module"])
                assert r1 == r2, f"Non-deterministic: {r1!r} vs {r2!r}"
            else:
                result = _resolve_answer_mode({}, case["query"], case["explicit_module"])
                assert result == case["expect"], f"Expected {case['expect']!r}, got {result!r}"

            print(f"PASS mode:{case['name']}")
            passed += 1
        except Exception as e:
            print(f"FAIL mode:{case['name']}: {e}")
            failed += 1
        finally:
            for k, v in saved.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v

    print()
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
