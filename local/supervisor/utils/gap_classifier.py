"""
GapClassifier - deterministic (no LLM) classification of KB/skill gaps.

Source of truth: Langfuse trace metadata only. No live skill execution.

Isolation principle: the supervisor is a read-only analysis loop over
telemetry. It never imports or runs skill/kb_answer.py. Any diagnostic
signal that is missing from traces (e.g. concept_matched, score_vs_floor)
is surfaced as a TELEMETRY_GAP so the engineer knows to add that field to
kb_answer.py's Langfuse instrumentation — not to re-run queries offline.

Classifies each gap's failure queries using:
  - What the trace recorded: top_score, top_source, answered, confidence
  - Query-text heuristics: pricing/noise/account-support gates
  - Missing trace fields → category CODE_GAP_NEEDS_INVESTIGATION with
    evidence.telemetry_gap describing what to add to kb_answer.py
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
    """Classifies gaps from Langfuse trace metadata. No live skill execution."""

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    def classify_query_from_trace(self, query: str, trace_meta: dict) -> dict:
        """Classify one failure query using its Langfuse trace metadata.

        trace_meta: the 'metadata' dict from the Langfuse trace for this query.
        Falls back to query-text heuristics when trace fields are absent.
        """
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

        answered = bool(trace_meta.get("answered"))
        top_score = trace_meta.get("top_score") or 0
        top_source = trace_meta.get("top_source") or ""
        confidence = trace_meta.get("confidence") or 0
        failure_type = trace_meta.get("failure_type") or ""

        evidence = {
            "top_score": top_score,
            "top_source": top_source,
            "confidence": confidence,
            "failure_type": failure_type,
            "answered": answered,
        }

        if answered:
            if top_score >= ALREADY_FIXED_MIN_SCORE and top_source:
                return {"query": query, "category": ALREADY_FIXED, "evidence": evidence}
            return {"query": query, "category": CODE_GAP_NEEDS_INVESTIGATION,
                    "evidence": {**evidence, "reason": "answered in trace but low score — may be false positive"}}

        # IDK in trace
        if top_score > 0 and top_source:
            # Doc was retrieved but skill still IDKed — routing/floor issue
            return {"query": query, "category": CODE_GAP_NEEDS_INVESTIGATION,
                    "evidence": {**evidence, "reason": f"IDK despite retrieval: top_score={top_score:.2f} from {top_source}"}}

        if top_score == 0 or not top_source:
            # Nothing retrieved — content gap or missing concept
            return {"query": query, "category": CONTENT_GAP,
                    "evidence": {**evidence, "reason": "IDK with no retrieval — content gap or concept missing"}}

        return {"query": query, "category": CODE_GAP_NEEDS_INVESTIGATION,
                "evidence": {**evidence, "reason": "unclassified IDK pattern"}}

    # ------------------------------------------------------------------
    def classify_gap(self, gap_failure_examples: list, max_samples: int = 10,
                     traces_for_gap: list = None) -> dict:
        """Classify a gap from Langfuse trace metadata.

        gap_failure_examples: list of query strings from the gap.
        traces_for_gap: list of Langfuse trace dicts matching this gap's queries.
                        When provided, each query's trace metadata is used.
                        When absent, query-text heuristics only (pricing/noise gates).
        """
        samples = [q for q in (gap_failure_examples or []) if q][:max_samples]

        if not samples:
            return {"category": NOISE, "confidence": "high",
                    "evidence": {"reason": "no failure examples"}, "per_query_results": []}

        # Noise gate
        noise_count = sum(1 for q in samples if _is_noise_query(q))
        if noise_count / len(samples) >= 0.80:
            return {
                "category": NOISE, "confidence": "high",
                "evidence": {"reason": f"{noise_count}/{len(samples)} queries are noise"},
                "per_query_results": [],
            }

        # Out-of-scope gate
        off_scope_count = sum(1 for q in samples if not _is_gupshup_product_query(q))
        if off_scope_count / len(samples) >= 0.70:
            return {
                "category": OUT_OF_SCOPE_GENERAL, "confidence": "high",
                "evidence": {"reason": f"{off_scope_count}/{len(samples)} queries have no Gupshup product terms"},
                "per_query_results": [],
            }

        # Build a query → trace_meta lookup from the provided traces
        query_to_meta: dict = {}
        if traces_for_gap:
            for t in traces_for_gap:
                m = t.get("metadata") or {}
                q = m.get("query") or (t.get("input") or {}).get("query") or ""
                if q:
                    query_to_meta[q] = m
                    # Also index by prefix (queries may be truncated in failure_examples)
                    query_to_meta[q[:100]] = m

        per_query_results = []
        for q in samples:
            meta = query_to_meta.get(q) or query_to_meta.get(q[:100]) or {}
            per_query_results.append(self.classify_query_from_trace(q, meta))

        categories = [r["category"] for r in per_query_results]
        unique_categories = sorted(set(categories))

        if len(unique_categories) == 1:
            category = unique_categories[0]
            confidence = "high"
        else:
            category = "MIXED"
            confidence = "low"

        breakdown: dict = {}
        for r in per_query_results:
            breakdown.setdefault(r["category"], []).append(r["query"])

        return {
            "category": category,
            "confidence": confidence,
            "evidence": {"category_breakdown": breakdown},
            "per_query_results": per_query_results,
        }
