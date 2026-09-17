"""Trace analyzer — group failures by (module, intent), re-deriving module from
the actual skill pipeline rather than trusting the downstream trace label.

Why: the trace's module_label is whatever kb_answer.py decided at runtime.
That decision can be wrong (stale CONCEPT_REGISTRY, no concept match, BM25
noise). If the supervisor trusts the trace label, every downstream judgment
inherits that error. We re-run _detect_module + _extract_entities on each
failing query against the *current* code and use that as ground truth.
Module mismatches are surfaced per-gap so proposals can flag routing bugs.
"""

import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ── Skill pipeline import ─────────────────────────────────────────────────────
_SKILL_ROOT = str(Path(__file__).parents[3])
if _SKILL_ROOT not in sys.path:
    sys.path.insert(0, _SKILL_ROOT)

try:
    from skill import kb_answer as _kb
    _detect_module = getattr(_kb, "_detect_module", None)
    _extract_entities = getattr(_kb, "_extract_entities", None)
    _SKILL_AVAILABLE = _detect_module is not None and _extract_entities is not None
    if not _SKILL_AVAILABLE:
        logger.warning("kb_answer._detect_module/_extract_entities not importable — falling back to trace label")
except Exception as exc:
    _SKILL_AVAILABLE = False
    logger.warning("Could not import skill.kb_answer: %s — falling back to trace label", exc)


def _skill_module(query: str) -> Tuple[Optional[str], Optional[str]]:
    """Re-derive (module, concept_id) by running the actual skill pipeline.

    Returns (module, concept_id) or (None, None) if skill unavailable / no match.
    """
    if not _SKILL_AVAILABLE or not query:
        return None, None
    try:
        entities = _extract_entities(query)
        if entities:
            e = entities[0]
            return e.get("module"), e.get("id")
        # No concept matched — use _detect_module as fallback
        result = _detect_module(query)
        return result.get("module") if isinstance(result, dict) else str(result), None
    except Exception as exc:
        logger.debug("_skill_module failed for query %r: %s", query[:60], exc)
        return None, None


@dataclass
class Gap:
    """A KB gap: failing (module, intent) bucket with evidence."""

    module: str                          # Ground-truth module from skill pipeline
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
        logger.info("Analyzing %d traces (skill pipeline re-routing: %s)...",
                    len(traces), "ON" if _SKILL_AVAILABLE else "OFF — trace labels only")

        # ── Pass 1: collect per-query routing decisions ───────────────────────
        # key = (skill_module, intent) — ground truth from current code
        groups: Dict[tuple, Dict] = {}

        for trace in traces:
            meta = trace.get("metadata") or {}
            trace_module = meta.get("module_label") or meta.get("module") or trace.get("module", "Unknown")
            intents = meta.get("intent_labels") or []
            intent = intents[0] if intents else (meta.get("intent") or trace.get("intent", "Unknown"))
            query = meta.get("query") or (trace.get("input") or {}).get("query") or trace.get("query", "")
            answered = bool(meta.get("answered") or trace.get("answered", False))
            confidence = meta.get("top_score") or meta.get("confidence") or trace.get("confidence", 0.0)

            # Re-derive module from actual skill code
            skill_mod, concept_id = _skill_module(query) if not answered else (None, None)
            # For answered traces use trace label (skill got it right)
            # For failed traces use skill re-derivation (trace label may be stale/wrong)
            if answered or not _SKILL_AVAILABLE:
                effective_module = trace_module
            else:
                effective_module = skill_mod or trace_module

            key = (effective_module, intent)

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
                    "trace_modules": {},      # {trace_module: count}
                    "no_concept_count": 0,
                }

            groups[key]["total"] += 1
            tm = groups[key]["trace_modules"]
            tm[trace_module] = tm.get(trace_module, 0) + 1

            if not answered and concept_id is None and _SKILL_AVAILABLE:
                groups[key]["no_concept_count"] += 1

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

        # ── Pass 2: build Gap objects, flag routing mismatches ────────────────
        gaps = []
        for (skill_module, intent), g in groups.items():
            avg_conf = (sum(g["confidences"]) / len(g["confidences"])
                        if g["confidences"] else 0.0)

            # Dominant trace module for this group
            dominant_trace_module = max(g["trace_modules"], key=g["trace_modules"].get) if g["trace_modules"] else skill_module
            mismatch = (dominant_trace_module != skill_module and _SKILL_AVAILABLE
                        and skill_module not in (None, "Unknown"))
            mismatch_detail = f"trace={dominant_trace_module}, skill={skill_module}" if mismatch else ""

            if mismatch:
                logger.warning("Module routing mismatch in gap %s/%s: %s", skill_module, intent, mismatch_detail)

            gap = Gap(
                module=skill_module,
                intent=intent,
                total_count=g["total"],
                success_count=g["success"],
                failure_count=g["failure"],
                answer_rate=g["success"] / g["total"] if g["total"] > 0 else 0.0,
                avg_confidence=avg_conf,
                failure_examples=g["failures"][:5],
                success_examples=g["successes"][:3],
                trace_module=dominant_trace_module,
                module_mismatch=mismatch,
                mismatch_detail=mismatch_detail,
                no_concept_match_count=g["no_concept_count"],
            )
            gaps.append(gap)

        self.gaps = gaps
        logger.info("Identified %d unique (module, intent) combinations", len(gaps))
        mismatches = [g for g in gaps if g.module_mismatch]
        if mismatches:
            logger.warning("%d gap(s) have skill/trace module mismatch — trace labels were unreliable", len(mismatches))

        return self.rank_by_severity(gaps)

    def rank_by_severity(self, gaps: List[Gap]) -> List[Gap]:
        sorted_gaps = sorted(gaps, key=lambda g: (g.answer_rate, g.failure_count), reverse=False)
        if sorted_gaps:
            logger.info("Ranked gaps. Top: %s", sorted_gaps[0].summary())
        return sorted_gaps
