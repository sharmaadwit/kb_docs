"""Trace analyzer - group and calculate metrics."""

import logging
from dataclasses import dataclass, field
from typing import Dict, List

logger = logging.getLogger(__name__)


@dataclass
class Gap:
    """Represents a KB gap identified from trace analysis."""

    module: str
    intent: str
    total_count: int
    success_count: int
    failure_count: int
    answer_rate: float
    avg_confidence: float
    failure_examples: List[str] = field(default_factory=list)
    success_examples: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate and compute derived fields."""
        if self.total_count > 0:
            if self.answer_rate == 0:
                self.answer_rate = self.success_count / self.total_count
        else:
            self.answer_rate = 0.0

    def summary(self) -> str:
        """Generate one-line summary of gap."""
        return (
            f"{self.module} / {self.intent}: "
            f"{self.failure_count} failures ({self.answer_rate*100:.1f}% answer rate)"
        )


class TraceAnalyzer:
    """Analyze traces: group by module×intent, calculate metrics."""

    def __init__(self) -> None:
        """Initialize analyzer."""
        self.gaps: List[Gap] = []

    def analyze(self, traces: List[Dict]) -> List[Gap]:
        """Analyze traces: group by (module, intent) and compute metrics.

        Args:
            traces: List of trace dictionaries from TraceLoader (from dashboard cache).

        Returns:
            List of Gap objects, ranked by answer_rate (ascending).
        """
        logger.info(f"Analyzing {len(traces)} traces...")

        # Group by (module, intent)
        groups: Dict[tuple, Dict] = {}

        for trace in traces:
            # Extract fields from nested metadata (dashboard cache structure)
            metadata = trace.get("metadata", {})
            module = metadata.get("module_label", trace.get("module", "Unknown"))
            intent = metadata.get("query_family", trace.get("intent", "Unknown"))

            key = (module, intent)

            if key not in groups:
                groups[key] = {
                    "total": 0,
                    "success": 0,
                    "failure": 0,
                    "confidences": [],
                    "failures": [],
                    "successes": [],
                }

            groups[key]["total"] += 1

            # answered field is in metadata
            answered = metadata.get("answered", trace.get("answered", False))

            # Extract confidence from output or metadata
            output = trace.get("output", {})
            confidence_score = output.get("confidence_score", 0.0)
            if not confidence_score:
                confidence_score = metadata.get("confidence_score", 0.0)

            # Extract query from input
            input_data = trace.get("input", {})
            query = input_data.get("query", "")

            if answered:
                groups[key]["success"] += 1
                if query:
                    groups[key]["successes"].append(query)
            else:
                groups[key]["failure"] += 1
                if query:
                    groups[key]["failures"].append(query)

            groups[key]["confidences"].append(confidence_score)

        # Convert to Gap objects
        gaps = []
        for (module, intent), group_data in groups.items():
            avg_conf = (
                sum(group_data["confidences"]) / len(group_data["confidences"])
                if group_data["confidences"]
                else 0.0
            )

            gap = Gap(
                module=module,
                intent=intent,
                total_count=group_data["total"],
                success_count=group_data["success"],
                failure_count=group_data["failure"],
                answer_rate=group_data["success"] / group_data["total"] if group_data["total"] > 0 else 0.0,
                avg_confidence=avg_conf,
                failure_examples=group_data["failures"][:5],  # Top 5 failures
                success_examples=group_data["successes"][:3],  # Top 3 successes
            )

            gaps.append(gap)

        self.gaps = gaps
        logger.info(f"Identified {len(gaps)} unique (module, intent) combinations")

        return self.rank_by_severity(gaps)

    def rank_by_severity(self, gaps: List[Gap]) -> List[Gap]:
        """Rank gaps by answer_rate (ascending = biggest gaps first).

        Args:
            gaps: List of Gap objects to rank.

        Returns:
            Sorted list of gaps (lowest answer_rate first).
        """
        sorted_gaps = sorted(gaps, key=lambda g: (g.answer_rate, g.failure_count), reverse=False)
        logger.info(f"Ranked gaps by severity. Top gap: {sorted_gaps[0].summary() if sorted_gaps else 'None'}")
        return sorted_gaps
