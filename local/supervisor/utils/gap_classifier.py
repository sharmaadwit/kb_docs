"""
GapClassifier - deterministic (no LLM) classification of KB/skill gaps.

Replaces the crude keyword-overlap scoring in kb_searcher.py +
rag_diagnostician.py (which produced a uniform "RETRIEVAL, 85% confidence"
verdict on every gap because kb_searcher's unbounded scores were compared
against hardcoded 0.3/0.6 thresholds on the wrong scale).

Instead this classifier re-runs each gap's failure queries through the REAL
skill pipeline (via SkillPipelineBridge) and applies a small decision tree
built from the actual bugs found manually earlier this session:
  - queries already patched no longer reproduce as IDK -> ALREADY_FIXED
  - entities == [] + a near-miss CONCEPT_REGISTRY keyword hit -> alias gap
  - entities == [] + no near-miss but real on-topic KB content exists ->
    missing CONCEPT_REGISTRY entry
  - entities != [] but still IDK -> a composition/evidence-selection bug,
    flagged for deeper investigation (not something a rule can diagnose)
  - entities == [] + no near-miss + no on-topic content -> genuine content gap
  - pricing / account-support queries are out-of-scope by design, checked
    before pipeline classification
"""
import re

# ---------------------------------------------------------------------------
# Category constants
# ---------------------------------------------------------------------------
ALREADY_FIXED = "ALREADY_FIXED"
CODE_GAP_ALIAS_CANDIDATE = "CODE_GAP_ALIAS_CANDIDATE"
CODE_GAP_MISSING_CONCEPT = "CODE_GAP_MISSING_CONCEPT"
CODE_GAP_NEEDS_INVESTIGATION = "CODE_GAP_NEEDS_INVESTIGATION"
CONTENT_GAP = "CONTENT_GAP"
OUT_OF_SCOPE_PRICING = "OUT_OF_SCOPE_PRICING"
OUT_OF_SCOPE_ACCOUNT_SUPPORT = "OUT_OF_SCOPE_ACCOUNT_SUPPORT"
OUT_OF_SCOPE_GENERAL = "out_of_scope_general"
NOISE = "noise"

# Reused verbatim from report_generator.py's is_pricing_query() — this is an
# existing, established rule in this codebase (pricing IDK = sales signal,
# not a KB gap). Do not second-guess it here.
PRICING_KEYWORDS = [
    "price", "pricing", "cost", "fee", "discount", "subscription", "plan", "payment",
]

# Multi-word phrases (to avoid false positives from single generic words like
# "account" or "code") covering personal account-recovery / OTP / login
# issues, which are not documentable KB topics.
ACCOUNT_SUPPORT_PHRASES = [
    "verification code",
    "código de verificação",
    "codigo de verificacao",
    "can't access my account",
    "cant access my account",
    "não consigo acessar",
    "nao consigo acessar",
    "forgot my account id",
    "não me lembro do id",
    "nao me lembro do id",
    "recover my account",
    "recuperar conta",
    "reset password",
    "redefinir senha",
    "forgot my password",
    "esqueci minha senha",
    "não recebo o e-mail",
    "nao recebo o e-mail",
    "did not receive the otp",
    "didn't receive the otp",
    "otp not received",
]

# Small local stopword set used only if kb.SCORING_STOP_WORDS isn't reachable
# through the bridge (defensive fallback).
_FALLBACK_STOP_WORDS = {
    "how", "to", "use", "from", "in", "a", "the", "my", "is", "it",
    "do", "can", "that", "this", "and", "or", "for", "with", "on",
    "of", "what", "where", "when", "which", "are", "was", "will",
    "should", "does", "have", "not", "but", "they", "their", "its",
}

CONTENT_MATCH_THRESHOLD = 0.7  # "almost all" significant terms must appear

GUPSHUP_PRODUCT_TERMS = {
    "whatsapp", "bot studio", "campaign", "superagent", "super agent",
    "agent assist", "ctx", "bizai", "biz ai", "meta business", "business agent",
    "mba", "channels", "rcs", "integrations", "ai admin", "personalize",
    "wallet", "gupshup", "waba", "instagram", "viber", "telegram",
    "kb", "knowledge base", "ingest", "webhook", "api", "sandbox",
    "template", "hsm", "optin", "opt-in", "flow", "node", "journey",
    "goals", "analytics", "dashboard", "overview",
}


def _is_gupshup_product_query(query: str) -> bool:
    """Return True if query mentions any Gupshup product term."""
    low = (query or "").lower()
    if re.search(r'\bmba\b', low):
        return True
    return any(term in low for term in GUPSHUP_PRODUCT_TERMS)


def _is_noise_query(query: str) -> bool:
    """Return True if query is too short or has no alphabetic content."""
    q = (query or "").strip()
    if not re.search(r'[a-zA-Z]', q):
        return True
    words = q.split()
    if len(words) <= 1:
        return True
    if len(words) <= 3:
        return True
    return False

# Minimal sanity floor for declaring ALREADY_FIXED. Calibrated against known
# examples from this session's manual investigation:
#   - genuine fixes: "how do i configure an intent?" -> top_score 9.6,
#     "How do I save the user input?" -> top_score 5.3 (both comfortably above)
#   - known false positives (non-IDK text, wrong-topic evidence): an IVR query
#     answered from a CC-Express doc, and a "Voice AI / IVR automation" query
#     answered from campaign-performance-monitoring.md at top_score 0.85
# top_score alone can't perfectly separate every case (some legitimate low-
# score template answers exist, e.g. a WABA Solution ID lookup at 0.85), so
# this is intentionally a MINIMAL/conservative floor, not a topic-relevance
# check. Its job is to catch the clearly-weak-evidence cases, not all of them.
ALREADY_FIXED_MIN_SCORE = 2.0


def is_pricing_query(text: str) -> bool:
    low = (text or "").lower()
    return any(word in low for word in PRICING_KEYWORDS)


def is_account_support_query(text: str) -> bool:
    low = (text or "").lower()
    return any(phrase in low for phrase in ACCOUNT_SUPPORT_PHRASES)


class GapClassifier:
    """Classifies gaps by re-running failure queries through the real pipeline."""

    def __init__(self, bridge):
        """
        Args:
            bridge: a SkillPipelineBridge instance (already loaded).
        """
        self.bridge = bridge

    # ------------------------------------------------------------------
    def _significant_terms(self, query: str) -> set:
        tokens = self.bridge._normalize_tokens(query)
        stop_words = getattr(self.bridge.kb, "SCORING_STOP_WORDS", _FALLBACK_STOP_WORDS)
        return {t for t in tokens if len(t) >= 3 and t not in stop_words}

    def _targeted_content_check(self, query: str) -> dict:
        """Bounded, deterministic on-topic content check.

        Does NOT reuse kb_searcher.py's raw score (the miscalibrated system
        being replaced). Instead checks whether any single KB source file's
        filename + section headings contain (as literal substrings) >= 70%
        of the query's significant terms. Body text alone is deliberately
        excluded — it produces false positives (e.g. generic "user" matching
        unrelated Agent Assist pages, seen earlier this session).
        """
        terms = self._significant_terms(query)
        if not terms:
            return {"found": False, "matches": [], "checked_terms": []}

        # Group chunks by source file, concatenating filename + all headings
        # seen for that source into one lowercase haystack.
        by_source = {}
        for c in self.bridge.chunks:
            source = c.get("source", "")
            if not source:
                continue
            haystack = by_source.setdefault(source, set())
            haystack.add(source.lower())
            heading = c.get("heading") or ""
            if heading:
                haystack.add(heading.lower())
            for h in c.get("heading_path") or []:
                haystack.add(str(h).lower())

        matches = []
        for source, headings in by_source.items():
            combined = " ".join(headings)
            combined_tokens = set(re.findall(r"[a-z0-9]+", combined))
            hit_terms = {t for t in terms if t in combined_tokens or any(t in h for h in headings)}
            coverage = len(hit_terms) / len(terms)
            if coverage >= CONTENT_MATCH_THRESHOLD:
                matches.append({
                    "source": source,
                    "coverage": round(coverage, 2),
                    "matched_terms": sorted(hit_terms),
                })

        matches.sort(key=lambda m: m["coverage"], reverse=True)
        return {
            "found": bool(matches),
            "matches": matches[:5],
            "checked_terms": sorted(terms),
        }

    # ------------------------------------------------------------------
    def classify_query(self, query: str) -> dict:
        """Classify a single failure query. Returns the category plus the
        evidence used to reach it."""
        if is_pricing_query(query):
            return {
                "query": query,
                "category": OUT_OF_SCOPE_PRICING,
                "evidence": {"matched_keywords": [w for w in PRICING_KEYWORDS if w in query.lower()]},
            }
        if is_account_support_query(query):
            return {
                "query": query,
                "category": OUT_OF_SCOPE_ACCOUNT_SUPPORT,
                "evidence": {"matched_phrases": [p for p in ACCOUNT_SUPPORT_PHRASES if p in query.lower()]},
            }

        result = self.bridge.run_query_with_signal(query)

        # Diagnostic fields from run_query_with_signal — injected into every evidence dict
        _diag = {
            "top_score": result.get("top_score", 0),
            "score_vs_floor": result.get("score_vs_floor"),
            "concept_matched": result.get("concept_matched"),
            "near_misses": result.get("near_misses") or [],
            "answered_now": result.get("answered_now", False),
            "evidence_sources": result.get("evidence_sources") or [],
        }

        if not result["is_idk"]:
            has_evidence = bool(result["evidence_sources"])
            score_ok = result["top_score"] >= ALREADY_FIXED_MIN_SCORE
            if has_evidence and score_ok:
                # Source alignment check: if entities were matched, verify the
                # answer actually came from the expected source doc(s) for the
                # first matched entity. An entity match alone doesn't mean the
                # skill answered correctly — the top evidence doc may be a
                # plausible-sounding but wrong file (e.g. agent_transfer matched
                # but top doc is superagent/concepts/agents.md instead of
                # agent-transfer-node.md). This is the false-positive pattern
                # identified in this session.
                entities = result["entities"]
                if entities:
                    entity_id = entities[0]
                    source_boosts = self.bridge.get_concept_source_boosts(entity_id)
                    if source_boosts:
                        top_source = result["evidence_sources"][0] or ""
                        expected_keys = list(source_boosts.keys())
                        source_aligned = any(
                            key in top_source for key in expected_keys
                        )
                        if not source_aligned:
                            return {
                                "query": query,
                                "category": CODE_GAP_NEEDS_INVESTIGATION,
                                "evidence": {
                                    "reason": "entity matched but answer came from wrong source doc",
                                    "entity": entity_id,
                                    "expected_sources": expected_keys,
                                    "actual_top_source": top_source,
                                    "answer_preview": (result["answer"] or "")[:200],
                                    "module": result["module"],
                                    "entities": entities,
                                    "evidence_sources": result["evidence_sources"],
                                    "top_score": result["top_score"],
                                },
                            }
                return {
                    "query": query,
                    "category": ALREADY_FIXED,
                    "evidence": {
                        "answer_preview": (result["answer"] or "")[:300],
                        "module": result["module"],
                        "entities": result["entities"],
                        **_diag,
                    },
                }
            # Non-IDK text, but evidence is missing or too weak to trust —
            # don't blindly declare this fixed. A prior manual investigation
            # this session found a non-IDK case whose evidence was real text
            # but from a completely wrong-topic doc (an IVR query answered
            # from a CC-Express page). Flag for human verification instead.
            if not has_evidence:
                weakness = "missing (no evidence_sources)"
            else:
                weakness = (
                    f"weak (top_score {result['top_score']} < floor "
                    f"{ALREADY_FIXED_MIN_SCORE})"
                )
            return {
                "query": query,
                "category": CODE_GAP_NEEDS_INVESTIGATION,
                "evidence": {
                    "reason": f"Answer is not IDK, but evidence is {weakness} "
                              "— non-IDK text alone isn't sufficient proof the answer is "
                              "correct/on-topic (see the CC-Express-doc-answering-an-IVR-"
                              "query false positive found earlier this session). Needs "
                              "human verification, not auto-classification as fixed.",
                    "module": result["module"],
                    "intent": result["intent"],
                    "entities": result["entities"],
                    "evidence_sources": result["evidence_sources"],
                    "top_score": result["top_score"],
                    "answer_preview": (result["answer"] or "")[:300],
                },
            }

        # Still IDK past this point.
        if result["entities"]:
            return {
                "query": query,
                "category": CODE_GAP_NEEDS_INVESTIGATION,
                "evidence": {
                    "reason": "Entities matched but answer is still IDK — likely a "
                              "composition/evidence-selection bug (same pattern as "
                              "the entities[0] bug found earlier this session). "
                              "Needs a deeper investigation agent, not a rule.",
                    "module": result["module"],
                    "intent": result["intent"],
                    "answer": result["answer"],
                    **_diag,
                },
            }

        # entities == [] and still IDK
        near_misses = self.bridge.check_near_miss_concepts(query)
        if near_misses:
            # For intents where a keyword near-miss does NOT imply an alias
            # would fix IDK (troubleshooting/page_lookup/refusal/compare
            # usually mean no KB content exists, not a missing alias), route
            # to investigation rather than auto-proposing an alias.
            _ALIAS_UNSAFE_INTENTS = {"troubleshooting", "page_lookup", "refusal", "compare"}
            intent = result.get("intent") or ""
            if intent in _ALIAS_UNSAFE_INTENTS:
                return {
                    "query": query,
                    "category": CODE_GAP_NEEDS_INVESTIGATION,
                    "evidence": {
                        "reason": (
                            f"Near-miss concept(s) found but intent is '{intent}', "
                            "which typically indicates missing content rather than a "
                            "missing alias — adding an alias is unlikely to fix IDK "
                            "for this intent type. Needs human/Hermes verification."
                        ),
                        "near_miss_concepts": near_misses,
                        "intent": intent,
                        "answer": result["answer"],
                    },
                }
            return {
                "query": query,
                "category": CODE_GAP_ALIAS_CANDIDATE,
                "evidence": {
                    "near_miss_concepts": near_misses,
                    "answer": result["answer"],
                },
            }

        content_check = self._targeted_content_check(query)
        if content_check["found"]:
            return {
                "query": query,
                "category": CODE_GAP_MISSING_CONCEPT,
                "evidence": {
                    "reason": "No CONCEPT_REGISTRY entry/keyword matched this query, "
                              "but on-topic KB content exists. May need a new "
                              "CONCEPT_REGISTRY entry.",
                    "content_check": content_check,
                    "answer": result["answer"],
                },
            }

        return {
            "query": query,
            "category": CONTENT_GAP,
            "evidence": {
                "reason": "No entity/keyword match and no on-topic KB content found.",
                "content_check": content_check,
                "answer": result["answer"],
            },
        }

    # ------------------------------------------------------------------
    def classify_gap(self, gap_failure_examples: list, max_samples: int = 3) -> dict:
        """Classify a gap using up to max_samples of its failure_examples.

        If different sample queries classify differently, the gap is
        heterogeneous — report the full breakdown rather than forcing a
        single label (this is exactly what "AI Admin / General" turned out
        to be: 6+ different problem types mislabeled as one RETRIEVAL gap).
        """
        samples = [q for q in (gap_failure_examples or []) if q][:max_samples]

        # Pre-check 1: noise gate
        if samples:
            noise_count = sum(1 for q in samples if _is_noise_query(q))
            if noise_count / len(samples) >= 0.80:
                return {
                    "category": NOISE,
                    "confidence": "high",
                    "evidence": {"reason": f"{noise_count}/{len(samples)} sample queries are noise (too short or no alphabetic content)"},
                    "per_query_results": [],
                }

        # Pre-check 2: out-of-scope gate
        if samples:
            off_scope_count = sum(1 for q in samples if not _is_gupshup_product_query(q))
            if off_scope_count / len(samples) >= 0.70:
                return {
                    "category": OUT_OF_SCOPE_GENERAL,
                    "confidence": "high",
                    "evidence": {"reason": f"{off_scope_count}/{len(samples)} sample queries contain no Gupshup product terms"},
                    "per_query_results": [],
                }

        per_query_results = [self.classify_query(q) for q in samples]

        categories = [r["category"] for r in per_query_results]
        unique_categories = sorted(set(categories))

        if len(unique_categories) == 1:
            category = unique_categories[0]
            confidence = "high"
        else:
            category = "MIXED"
            confidence = "low"

        breakdown = {}
        for r in per_query_results:
            breakdown.setdefault(r["category"], []).append(r["query"])

        return {
            "category": category,
            "confidence": confidence,
            "evidence": {"category_breakdown": breakdown},
            "per_query_results": per_query_results,
        }
