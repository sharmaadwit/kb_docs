"""Tests for _semantic_relevance_check in hermes_judge.py.

Covers:
  - True positive: snippet that genuinely addresses the query
  - False positive prevention: high-BM25 snippet from a different topic
  - The coexistence regression: pricing snippet must NOT pass as relevant for coexistence query
  - Degraded mode: no hermes binary → falls back to True (never blocks)

Run with:
    python3 -m pytest local/supervisor/tests/test_semantic_check.py -v
"""

import importlib
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

# Ensure project root is on path
import os, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from local.supervisor.utils.hermes_judge import _semantic_relevance_check


RELEVANT_SNIPPET = (
    "WhatsApp Coexistence allows a phone number to run both WhatsApp Business App "
    "and WhatsApp Business API simultaneously. Eligibility requires the number to have "
    "been registered on WhatsApp Business App for at least 3 months before migration. "
    "The 3-month period is calculated from the original registration date, not the "
    "migration date. Meta determines eligibility dynamically based on account history."
)

IRRELEVANT_SNIPPET = (
    "2. Service Messages\n"
    "Exact path and steps\n"
    "- WhatsApp Message Pricing\n"
    "- Message Categories\n"
    "- 2. Service Messages\n"
    "- Messages sent outside the 24-hour window\n"
    "- Used for account updates, order confirmations, appointment reminders"
)

COEXISTENCE_QUERY = (
    "WhatsApp coexistence eligibility 3-month requirement for WhatsApp Business App. "
    "If a phone number used WhatsApp Messenger for years, and is migrated to WhatsApp "
    "Business App today, does the prior Messenger usage count?"
)

MFA_QUERY = "Gupshup Console login MFA: Add MFA Device screen asks for Device label"

MFA_SNIPPET = (
    "Console Navigation Guide\n"
    "How to access the Gupshup Console, login URL, navigation menu, account settings, "
    "roles and permissions. The console is available at console.gupshup.io."
)


def _make_hermes_mock(json_output: str):
    """Returns a mock that mimics subprocess.run + file write for hermes."""
    import json as _json

    def fake_run(cmd, timeout, capture_output, env):
        proc = MagicMock()
        proc.returncode = 0
        return proc

    return fake_run


class TestSemanticRelevanceCheck(unittest.TestCase):

    def _run_with_mock(self, query, snippet, source, hermes_response: dict):
        """Run _semantic_relevance_check with a mocked hermes subprocess."""
        import json
        import tempfile

        with patch("local.supervisor.utils.hermes_judge.shutil.which", return_value="/usr/local/bin/hermes"), \
             patch("local.supervisor.utils.hermes_judge.subprocess.run") as mock_run, \
             patch("builtins.open", unittest.mock.mock_open(read_data=json.dumps(hermes_response))), \
             patch("pathlib.Path.mkdir"):
            mock_run.return_value = MagicMock(returncode=0)
            return _semantic_relevance_check(query, snippet, source, timeout=5)

    def test_relevant_snippet_returns_true(self):
        result = self._run_with_mock(
            COEXISTENCE_QUERY, RELEVANT_SNIPPET, "kb/whatsapp/coexistence.md",
            {"relevant": True}
        )
        self.assertTrue(result, "Expected True for snippet that directly answers coexistence query")

    def test_irrelevant_pricing_snippet_returns_false(self):
        """Regression: pricing snippet must NOT be marked relevant for coexistence query."""
        result = self._run_with_mock(
            COEXISTENCE_QUERY, IRRELEVANT_SNIPPET, "kb/whatsapp/whatsapp-pricing.md",
            {"relevant": False}
        )
        self.assertFalse(result, "Pricing snippet must NOT pass as relevant for coexistence eligibility query")

    def test_mfa_snippet_not_relevant_for_mfa_query(self):
        """Console navigation snippet must NOT pass as covering MFA device setup."""
        result = self._run_with_mock(
            MFA_QUERY, MFA_SNIPPET, "kb/overview/console-navigation-guide.md",
            {"relevant": False}
        )
        self.assertFalse(result, "Console nav snippet must NOT pass as relevant for MFA device label query")

    def test_degraded_no_hermes_returns_false(self):
        """If hermes binary is missing, fall back to False (conservative — prevents false any_content=True)."""
        with patch("local.supervisor.utils.hermes_judge.shutil.which", return_value=None):
            result = _semantic_relevance_check(COEXISTENCE_QUERY, IRRELEVANT_SNIPPET, "any.md")
        self.assertFalse(result, "Degraded mode must return False — conservative prevents cross-domain false positives")

    def test_degraded_subprocess_error_returns_false(self):
        """If hermes subprocess crashes, fall back to False (conservative)."""
        with patch("local.supervisor.utils.hermes_judge.shutil.which", return_value="/usr/local/bin/hermes"), \
             patch("local.supervisor.utils.hermes_judge.subprocess.run", side_effect=OSError("crash")):
            result = _semantic_relevance_check(COEXISTENCE_QUERY, IRRELEVANT_SNIPPET, "any.md")
        self.assertFalse(result, "Subprocess crash must fall back to False")

    def test_degraded_bad_json_returns_false(self):
        """If hermes returns unparseable JSON, fall back to False (conservative)."""
        with patch("local.supervisor.utils.hermes_judge.shutil.which", return_value="/usr/local/bin/hermes"), \
             patch("local.supervisor.utils.hermes_judge.subprocess.run") as mock_run, \
             patch("builtins.open", unittest.mock.mock_open(read_data="not json at all")), \
             patch("pathlib.Path.mkdir"):
            mock_run.return_value = MagicMock(returncode=0)
            result = _semantic_relevance_check(COEXISTENCE_QUERY, IRRELEVANT_SNIPPET, "any.md", timeout=5)
        self.assertFalse(result, "Bad JSON from hermes must fall back to False")


class TestContentAvailabilityBlockIntegration(unittest.TestCase):
    """Integration tests for _content_availability_block using mocked bridge + semantic check."""

    def _make_bridge(self, top_score, sources, answer):
        bridge = MagicMock()
        bridge.run_query.return_value = {
            "top_score": top_score,
            "evidence_sources": sources,
            "answer": answer,
        }
        return bridge

    def test_high_score_pricing_doc_caught_by_cross_domain_precheck(self):
        """BM25 score 12 on a pricing doc for a coexistence query → caught by cross-domain pre-check."""
        from local.supervisor.utils.hermes_judge import _content_availability_block

        bridge = self._make_bridge(12.0, ["kb/whatsapp/whatsapp-pricing.md"], IRRELEVANT_SNIPPET)

        # Semantic check should NOT be called — cross-domain pre-check fires first
        with patch("local.supervisor.utils.hermes_judge._semantic_relevance_check") as mock_sem:
            block = _content_availability_block([COEXISTENCE_QUERY], bridge)

        mock_sem.assert_not_called()
        self.assertIn("cross-domain mismatch", block, "Block must flag the pricing doc as cross-domain")
        self.assertIn('kb_doc_needed": true', block, "Must recommend kb_doc_needed=true when no relevant doc")

    def test_high_score_relevant_doc_marked_as_content(self):
        """BM25 score 8 on a doc that passes semantic check → any_content True."""
        from local.supervisor.utils.hermes_judge import _content_availability_block

        bridge = self._make_bridge(8.0, ["kb/whatsapp/coexistence.md"], RELEVANT_SNIPPET)

        with patch("local.supervisor.utils.hermes_judge._semantic_relevance_check", return_value=True):
            block = _content_availability_block([COEXISTENCE_QUERY], bridge)

        self.assertIn("semantically relevant", block, "Block must flag doc as semantically relevant")
        self.assertIn("kb_doc_needed\": false", block, "Must recommend kb_doc_needed=false when relevant doc found")

    def test_low_score_skips_semantic_check(self):
        """Score ≤ 1.0 — semantic check must not be called."""
        from local.supervisor.utils.hermes_judge import _content_availability_block

        bridge = self._make_bridge(0.5, ["kb/whatsapp/irrelevant.md"], "some snippet")

        with patch("local.supervisor.utils.hermes_judge._semantic_relevance_check") as mock_sem:
            block = _content_availability_block([COEXISTENCE_QUERY], bridge)

        mock_sem.assert_not_called()
        self.assertIn("kb_doc_needed\": true", block)


if __name__ == "__main__":
    unittest.main()
