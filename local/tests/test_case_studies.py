"""Smoke tests for case study extraction and kb_answer integration."""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "skill"))

import kb_answer as kb


def _load_local_chunks():
    rows = []
    with open("kb/kb_chunks.jsonl", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


class CaseStudyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chunks = _load_local_chunks()
        cls.product = [
            c for c in cls.chunks if not kb._is_case_study_source(c.get("source", ""))
        ]
        cls.case = [
            c for c in cls.chunks if kb._is_case_study_source(c.get("source", ""))
        ]

    def test_case_study_chunks_ingested(self):
        self.assertGreaterEqual(len(self.case), 400)
        sources = {c["source"] for c in self.case}
        self.assertGreaterEqual(len(sources), 80)

    def test_no_brand_leak_in_anonymized_markdown(self):
        from pathlib import Path
        leaks = []
        for path in Path("kb/case-studies").glob("*.md"):
            text = path.read_text(encoding="utf-8").lower()
            if "sharing tier**: internal_anonymized" not in text:
                continue
            for brand in ("kotak", "hdfc", "treebo", "dream11"):
                if brand in text:
                    leaks.append((path.name, brand))
        self.assertEqual(leaks, [])

    def _answer_with_cases(self, query: str) -> str:
        explicit = kb._detect_module(query)
        entities = kb._extract_entities(query)
        intent = kb._classify_intent(query, entities)
        scored = []
        for c in self.product:
            s = kb._score_chunk(query, c, entities, explicit)
            if s >= kb.MIN_CHUNK_SCORE:
                scored.append({**c, "score": s})
        scored.sort(key=lambda x: x["score"], reverse=True)
        evidence = kb._select_evidence(query, scored, intent, explicit)
        answer = kb._compose_answer(query, intent, entities, evidence, explicit)
        if kb._should_include_case_studies(query, intent, answer, explicit):
            cases = kb._select_case_studies(query, self.case, explicit)
            if cases:
                answer = kb._append_case_study_section(answer, cases)
        return answer

    def test_food_examples_get_case_study_section(self):
        ans = self._answer_with_cases(
            "Give me WhatsApp marketing examples in food and restaurant"
        )
        self.assertIn(kb.CASE_STUDY_SECTION_HEADER, ans)
        self.assertIn("Food & Restaurant", ans)

    def test_schema_query_skips_case_studies(self):
        ans = self._answer_with_cases("What is the payload schema for campaign manager")
        self.assertNotIn(kb.CASE_STUDY_SECTION_HEADER, ans)

    def test_ctwa_retail_stories(self):
        ans = self._answer_with_cases("Show me CTWA success stories for retail")
        self.assertIn(kb.CASE_STUDY_SECTION_HEADER, ans)

    def test_anonymized_slug_does_not_leak_brand(self):
        from pathlib import Path
        BANNED = (
            "kotak", "britannia", "hdfc", "icici", "sbi", "treebo",
            "dream11", "swiggy", "zomato", "lakme", "byju",
            "doubtnut", "wow-momo", "tata-cliq", "horlicks", "ola",
            "cars24", "nobroker", "mtv", "max-fashion", "pureit", "reserva",
        )
        leaks = []
        for path in Path("kb/case-studies").glob("*.md"):
            text = path.read_text(encoding="utf-8").lower()
            if "sharing tier**: internal_anonymized" not in text:
                continue
            slug = path.stem.lower()
            for brand in BANNED:
                if brand in slug:
                    leaks.append((path.name, brand))
        self.assertEqual(leaks, [], f"Anonymized slugs leak brand tokens: {leaks}")

    def test_definition_intent_module_query_shows_cases(self):
        ans = self._answer_with_cases("What is Agent Assist?")
        self.assertIn(kb.CASE_STUDY_SECTION_HEADER, ans)


if __name__ == "__main__":
    unittest.main()
