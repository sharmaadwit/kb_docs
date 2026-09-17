"""
SkillPipelineBridge - runs queries through the REAL skill/kb_answer.py pipeline
offline, so diagnostic tooling reasons about actual pipeline behavior instead of
an independent keyword-overlap scorer.

Pattern copied from local/tests/test_regression.py (sys.path insert + direct
import of kb_answer, single load of kb/kb_chunks.jsonl, manual re-run of the
per-chunk scoring + evidence-selection + composition steps offline).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "skill"))
import kb_answer as kb  # noqa: E402

CHUNKS_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "kb", "kb_chunks.jsonl"
)

# Small local fallback stopword set, only used if kb.SCORING_STOP_WORDS is
# somehow unavailable (defensive - the real skill module always defines it).
_FALLBACK_STOP_WORDS = {
    "how", "to", "use", "from", "in", "a", "the", "my", "is", "it",
    "do", "can", "that", "this", "and", "or", "for", "with", "on",
    "of", "what", "where", "when", "which", "are", "was", "will",
}

# Keywords so generic they fire on almost any query — near-miss hits on these
# alone are noise, not signal. A concept that only matches via one of these
# is NOT a meaningful near-miss; it just means the query contains a common word.
_NOISE_KEYWORDS = {
    "api", "whatsapp", "sms", "message", "available", "setup", "configure",
    "create", "add", "get", "set", "enable", "send", "use", "channel",
    "number", "account", "user", "data", "type", "list", "name", "id",
    "gupshup",
}


def _load_chunks():
    items = []
    with open(CHUNKS_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except Exception:
                pass
    return items


def _is_idk(answer: str) -> bool:
    low = (answer or "").lower()
    return "i don't know" in low or "i don t know" in low


class SkillPipelineBridge:
    """Bridges diagnostic tooling to the real kb_answer.py retrieval pipeline."""

    def __init__(self):
        self.kb = kb
        self.chunks = _load_chunks()

    # ------------------------------------------------------------------
    def run_query(self, query: str) -> dict:
        """Run the full real pipeline for one query, offline.

        Mirrors local/tests/test_regression.py's run_pipeline(), with the
        guardrail-refusal short-circuit reused verbatim, extended with the
        fields the gap classifier needs (evidence_sources, is_idk).
        """
        guardrail = kb._guardrail_answer(query)
        if guardrail:
            return {
                "module": "General",
                "intent": "refusal",
                "entities": [],
                "evidence_sources": [],
                "top_score": 0,
                "answer": guardrail,
                "is_idk": _is_idk(guardrail),
            }

        chunks = self.chunks
        explicit_module = kb._detect_module(query)
        entities = kb._extract_entities(query)
        intent = kb._classify_intent(query, entities)

        scored = []
        threshold = getattr(kb, "MIN_CHUNK_SCORE", 0.0)
        for c in chunks:
            s = kb._score_chunk(query, c, entities, explicit_module)
            if threshold > 0 and s < threshold:
                continue
            elif threshold == 0 and s <= 0:
                continue
            row = dict(c)
            row["score"] = s
            scored.append(row)
        scored.sort(key=lambda x: x.get("score", 0.0), reverse=True)

        evidence = kb._select_evidence(query, scored, intent, explicit_module)
        answer = kb._compose_answer(query, intent, entities, evidence, explicit_module)

        return {
            "module": explicit_module,
            "intent": intent,
            "entities": [e["id"] for e in entities],
            "evidence_sources": [e.get("source") for e in evidence],
            "top_score": round(evidence[0].get("score", 0), 2) if evidence else 0,
            "answer": answer,
            "is_idk": _is_idk(answer),
        }

    # ------------------------------------------------------------------
    def _normalize_tokens(self, query: str) -> set:
        """Normalize+tokenize a query the same way the real pipeline does."""
        normalize_fn = getattr(kb, "_normalize_query_for_match", None)
        if normalize_fn:
            qn = normalize_fn(query)
        else:
            qn = (query or "").lower()
        return set(re.findall(r"[a-z0-9]+", qn))

    def get_concept_source_boosts(self, concept_id: str) -> dict:
        """Return source_boosts for a concept_id from CONCEPT_REGISTRY, or {}.

        Used by GapClassifier to verify that the answer came from the expected
        source document(s) for a matched entity — a non-empty mismatch means
        the entity matched but evidence came from the wrong doc (false positive
        for ALREADY_FIXED).
        """
        for concept in kb.CONCEPT_REGISTRY:
            if concept.get("id") == concept_id:
                return concept.get("source_boosts", {})
        return {}

    def check_near_miss_concepts(self, query: str) -> list:
        """Find concepts that got exactly 1 keyword hit for this query — the
        boundary case blocked by _extract_entities' Pass 2 "< 2 hits" gate
        (skill/kb_answer.py, near line 5335: `if len(kw_hits) < 2 and not
        has_context: continue`). A near-miss here is a strong signal that the
        concept's `keywords`/`aliases` list is missing a term this query uses
        (the exact pattern that surfaced the prompt_node / ai_admin_intents
        gaps earlier this session).

        Only meaningful to call when run_query() returned entities == [].
        """
        query_tokens = self._normalize_tokens(query)
        stop_words = getattr(kb, "SCORING_STOP_WORDS", _FALLBACK_STOP_WORDS)
        significant_tokens = query_tokens - stop_words

        near_misses = []
        for concept in kb.CONCEPT_REGISTRY:
            keywords = concept.get("keywords", [])
            hits = [k for k in keywords if k in significant_tokens or k in query_tokens]
            hit_count = len(hits)
            if 1 <= hit_count < 2:
                # Filter out hits where the only matched keyword is a noise token.
                # e.g. matching "api" on api_node or "whatsapp" on waba_setup for
                # any query mentioning those words is not a meaningful near-miss —
                # it just means the query uses a common word, not that an alias is
                # missing. Only surface the near-miss if at least one hit is specific.
                meaningful_hits = [h for h in hits if h not in _NOISE_KEYWORDS]
                if not meaningful_hits:
                    continue
                near_misses.append({
                    "concept_id": concept["id"],
                    "matched_keywords": hits,
                    "existing_aliases_sample": concept.get("aliases", [])[:3],
                    "display": concept.get("display"),
                    "module": concept.get("module"),
                })
        return near_misses
