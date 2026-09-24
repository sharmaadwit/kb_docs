"""Trace analyzer — group Langfuse trace failures by (module, intent).

Source of truth: Langfuse trace metadata only.
The trace's `module` field is what kb_answer decided at runtime — that IS the
ground truth for what actually happened in production. We do NOT re-run the
skill pipeline here; doing so would pollute the analysis with current code
state rather than what was live when the trace was recorded.

Isolation principle: the supervisor is a read-only analysis loop over telemetry.
It never executes skill code or calls any live endpoint.
"""

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ── Pre-classification keyword sets ──────────────────────────────────────────
# FIX 1: Pricing query detection
PRICING_KEYWORDS: frozenset = frozenset({
    "price", "prices", "priced", "pricing",
    "cost", "costs", "costing",
    "rate", "rates",
    "charge", "charges",
    "fee", "fees",
    "billing", "bill", "invoice",
    "plan", "plans",
    "subscription", "subscriptions",
    "tariff", "tariffs",
    "tarifa", "tarifas",
    "valor",
    "precio", "precios",
    "costo", "costos",
    "custo", "custos",
    "mensalidad", "mensualidad",
    "preço",
    "cobr",
    "pagar",
    "mensual", "monthly",
    "recharge",
    "per message",
    "per session",
})

# Tokens that indicate the query is about a *product feature* even if a
# pricing keyword also appears (e.g. "how to create a campaign plan").
_PRICING_EXCLUSION_TOKENS: frozenset = frozenset({
    "bot", "studio", "campaign", "flow", "webhook", "template",
    "button", "node", "journey", "integration", "setup", "configure",
})


def _is_pricing_query(query: str) -> bool:
    """Return True if query is primarily asking about pricing/cost.

    Detects multi-word phrases ("per message", "per session") as well as
    single tokens.  Excludes queries that contain product-feature tokens
    alongside a pricing word (e.g. "pricing of the API node in Bot Studio").
    """
    q_lower = query.lower()
    # Multi-word phrase check first
    if "per message" in q_lower or "per session" in q_lower:
        return True
    toks = set(re.findall(r"[a-z0-9]+", q_lower))
    if not (toks & PRICING_KEYWORDS):
        return False
    # Guard: don't capture product-feature questions that mention cost in passing
    return not bool(toks & _PRICING_EXCLUSION_TOKENS)


# FIX 2: WhatsApp Coexistence query detection
COEXISTENCE_KEYWORDS: frozenset = frozenset({
    "coexistence", "coexistência", "coexistencia",
    "3-month", "3 month", "three month",
    "existing number", "migrate number", "number migration",
    "whatsapp business app to api",
})


def _is_coexistence_query(query: str) -> bool:
    """Return True if query is about WhatsApp number coexistence / migration."""
    q_lower = query.lower()
    # Multi-word phrases
    for phrase in (
        "3-month", "3 month", "three month",
        "existing number", "migrate number", "number migration",
        "whatsapp business app to api",
    ):
        if phrase in q_lower:
            return True
    toks = set(re.findall(r"[a-z0-9]+", q_lower))
    return bool(toks & COEXISTENCE_KEYWORDS)


def _cluster_queries(
    queries: List[str],
    min_gap_size: int = 8,
    max_clusters: int = 3,
    split_threshold: float = 0.15,
) -> List[List[str]]:
    """Greedy Jaccard clustering of queries. Returns list of clusters.

    Only meaningful if len(queries) >= min_gap_size. If the gap is too small,
    returns a single cluster containing all queries (no split).
    """
    if len(queries) < min_gap_size:
        return [queries]

    def _tok(s: str) -> set:
        return set(re.findall(r"[a-z0-9]+", s.lower()))

    def _jaccard(a: set, b: set) -> float:
        if not a and not b:
            return 1.0
        union = a | b
        return len(a & b) / len(union) if union else 0.0

    token_sets = [_tok(q) for q in queries]
    clusters: List[List[int]] = []  # list of index lists

    for idx, toks in enumerate(token_sets):
        if not clusters:
            clusters.append([idx])
            continue
        # Find nearest cluster by average Jaccard to cluster members
        best_cluster, best_sim = -1, -1.0
        for ci, cluster in enumerate(clusters):
            sim = sum(_jaccard(toks, token_sets[j]) for j in cluster) / len(cluster)
            if sim > best_sim:
                best_sim, best_cluster = sim, ci
        if best_sim >= split_threshold or len(clusters) >= max_clusters:
            clusters[best_cluster].append(idx)
        else:
            clusters.append([idx])

    return [[queries[i] for i in c] for c in clusters]


@dataclass
class Gap:
    """A KB gap: failing (module, intent) bucket with evidence."""

    module: str                          # Module from Langfuse trace metadata
    intent: str
    total_count: int
    success_count: int
    failure_count: int
    answer_rate: float
    avg_confidence: float
    failure_examples: List[str] = field(default_factory=list)
    success_examples: List[str] = field(default_factory=list)

    # Routing quality fields
    trace_module: str = ""               # What the trace metadata claimed
    module_mismatch: bool = False        # True if skill disagrees with trace
    mismatch_detail: str = ""           # e.g. "trace=AI Admin, skill=Channels"
    no_concept_match_count: int = 0      # Queries with no entity match (pure BM25)

    # Pre-classification: set by Pass 0 for pricing / coexistence gaps so the
    # coordinator can skip full Hermes analysis and emit the bucket directly.
    pre_classified_bucket: str = ""      # e.g. "OUT_OF_SCOPE" — empty = not pre-classified

    def __post_init__(self) -> None:
        if self.total_count > 0 and self.answer_rate == 0:
            self.answer_rate = self.success_count / self.total_count
        elif self.total_count == 0:
            self.answer_rate = 0.0

    def summary(self) -> str:
        mismatch = f" ⚠ routing mismatch ({self.mismatch_detail})" if self.module_mismatch else ""
        return (
            f"{self.module} / {self.intent}: "
            f"{self.failure_count} failures ({self.answer_rate*100:.1f}% answer rate)"
            f"{mismatch}"
        )


class TraceAnalyzer:
    """Analyze traces: group by (module, intent), re-derive module from skill code."""

    def __init__(self) -> None:
        self.gaps: List[Gap] = []

    def analyze(self, traces: List[Dict]) -> List[Gap]:
        logger.info("Analyzing %d traces (source: Langfuse metadata only)...", len(traces))

        # Shared groups dict — populated by Pass 0, then Pass 1
        groups: Dict[tuple, Dict] = {}

        # ── Pass 0: pre-classify pricing and coexistence traces ──────────────
        # Scan ALL traces first for known OUT_OF_SCOPE categories.  Matching
        # *unanswered* traces are routed into canonical synthetic keys and
        # removed from regular grouping so they never scatter across modules.
        # FIX 3 & 4 per diagnosis.
        _PRE_CLASSIFIED_KEYS: Dict[tuple, str] = {
            ("Pricing", "pricing"): "OUT_OF_SCOPE",
            ("WhatsApp", "coexistence"): "OUT_OF_SCOPE",
        }
        # Set of trace indices that were consumed by Pass 0
        _pass0_consumed: set = set()

        for _idx, trace in enumerate(traces):
            meta = trace.get("metadata") or {}
            answered = bool(meta.get("answered") or trace.get("answered", False))
            if answered:
                continue  # answered traces never pre-classified as gaps
            query = (
                meta.get("query")
                or (trace.get("input") or {}).get("query")
                or trace.get("query", "")
            )
            if not query:
                continue

            if _is_pricing_query(query):
                _pass0_consumed.add(_idx)
                key = ("Pricing", "pricing")
            elif _is_coexistence_query(query):
                _pass0_consumed.add(_idx)
                key = ("WhatsApp", "coexistence")
            else:
                continue

            confidence = (
                meta.get("top_score")
                or meta.get("confidence")
                or trace.get("confidence", 0.0)
            )
            trace_module = (
                meta.get("module_label")
                or meta.get("module")
                or trace.get("module", "Unknown")
            )

            if key not in groups:
                groups[key] = {
                    "total": 0,
                    "success": 0,
                    "failure": 0,
                    "confidences": [],
                    "failures": [],
                    "successes": [],
                    "seen_failures": set(),
                    "seen_successes": set(),
                    "pre_classified_bucket": _PRE_CLASSIFIED_KEYS[key],
                }

            groups[key]["total"] += 1
            groups[key]["failure"] += 1
            groups[key]["confidences"].append(confidence)
            if query not in groups[key]["seen_failures"]:
                groups[key]["seen_failures"].add(query)
                groups[key]["failures"].append(query)

        if _pass0_consumed:
            logger.info(
                "Pass 0: pre-classified %d traces (pricing=%d, coexistence=%d)",
                len(_pass0_consumed),
                len(groups.get(("Pricing", "pricing"), {}).get("failures", [])),
                len(groups.get(("WhatsApp", "coexistence"), {}).get("failures", [])),
            )

        # ── Pass 1: group traces by (module, intent) from trace metadata ────────
        # Source of truth: Langfuse metadata only. No live skill execution.
        for _idx, trace in enumerate(traces):
            # Skip traces already bucketed by Pass 0
            if _idx in _pass0_consumed:
                continue

            meta = trace.get("metadata") or {}
            trace_module = meta.get("module") or meta.get("module_label") or trace.get("module", "Unknown")
            intents = meta.get("intent_labels") or []
            intent = intents[0] if intents else (meta.get("intent") or trace.get("intent", "Unknown"))
            query = meta.get("query") or (trace.get("input") or {}).get("query") or trace.get("query", "")
            answered = bool(meta.get("answered") or trace.get("answered", False))
            confidence = meta.get("top_score") or meta.get("confidence") or trace.get("confidence", 0.0)

            key = (trace_module, intent)

            if key not in groups:
                groups[key] = {
                    "total": 0,
                    "success": 0,
                    "failure": 0,
                    "confidences": [],
                    "failures": [],
                    "successes": [],
                    "seen_failures": set(),
                    "seen_successes": set(),
                    "pre_classified_bucket": "",  # empty = not pre-classified
                }

            groups[key]["total"] += 1

            if answered:
                groups[key]["success"] += 1
                if query and query not in groups[key]["seen_successes"]:
                    groups[key]["seen_successes"].add(query)
                    groups[key]["successes"].append(query)
            else:
                groups[key]["failure"] += 1
                if query and query not in groups[key]["seen_failures"]:
                    groups[key]["seen_failures"].add(query)
                    groups[key]["failures"].append(query)

            groups[key]["confidences"].append(confidence)

        # ── Pass 2: build Gap objects ─────────────────────────────────────────
        gaps = []
        for (module, intent), g in groups.items():
            avg_conf = (sum(g["confidences"]) / len(g["confidences"])
                        if g["confidences"] else 0.0)

            gap = Gap(
                module=module,
                intent=intent,
                total_count=g["total"],
                success_count=g["success"],
                failure_count=g["failure"],
                answer_rate=g["success"] / g["total"] if g["total"] > 0 else 0.0,
                avg_confidence=avg_conf,
                failure_examples=g["failures"][:20],
                success_examples=g["successes"][:3],
                trace_module=module,
                module_mismatch=False,
                mismatch_detail="",
                no_concept_match_count=0,
                pre_classified_bucket=g.get("pre_classified_bucket", ""),
            )
            gaps.append(gap)

        # ── Pass 3: sub-gap splitting for large, diverse gaps ─────────────────
        split_gaps: List[Gap] = []
        for gap in gaps:
            examples = gap.failure_examples or []
            # Never split pre-classified gaps — they must stay consolidated so
            # the coordinator emits a single OUT_OF_SCOPE verdict.
            if gap.pre_classified_bucket:
                split_gaps.append(gap)
                continue
            if len(examples) < 8:
                split_gaps.append(gap)
                continue
            clusters = _cluster_queries(examples)
            if len(clusters) <= 1:
                split_gaps.append(gap)
                continue
            logger.info(
                "Split %s/%s into %d sub-gaps", gap.module, gap.intent, len(clusters)
            )
            total_queries = len(examples)
            for i, cluster in enumerate(clusters):
                ratio = len(cluster) / total_queries if total_queries > 0 else 0.0
                sub_failure = max(1, round(gap.failure_count * ratio))
                sub_total = max(sub_failure, round(gap.total_count * ratio))
                sub_success = sub_total - sub_failure
                sub_gap = Gap(
                    module=gap.module,
                    intent=f"{gap.intent}__{i}",
                    total_count=sub_total,
                    success_count=sub_success,
                    failure_count=sub_failure,
                    answer_rate=gap.answer_rate,
                    avg_confidence=gap.avg_confidence,
                    failure_examples=cluster,
                    success_examples=gap.success_examples,
                    trace_module=gap.trace_module,
                    module_mismatch=gap.module_mismatch,
                    mismatch_detail=gap.mismatch_detail,
                    no_concept_match_count=round(gap.no_concept_match_count * ratio),
                    pre_classified_bucket="",  # sub-gaps inherit no pre-classification
                )
                split_gaps.append(sub_gap)
        gaps = split_gaps

        self.gaps = gaps
        logger.info("Identified %d unique (module, intent) combinations (after sub-gap splitting)", len(gaps))
        mismatches = [g for g in gaps if g.module_mismatch]
        if mismatches:
            logger.warning("%d gap(s) have skill/trace module mismatch — trace labels were unreliable", len(mismatches))

        return self.rank_by_severity(gaps)

    def rank_by_severity(self, gaps: List[Gap]) -> List[Gap]:
        sorted_gaps = sorted(gaps, key=lambda g: (g.answer_rate, g.failure_count), reverse=False)
        if sorted_gaps:
            logger.info("Ranked gaps. Top: %s", sorted_gaps[0].summary())
        return sorted_gaps
