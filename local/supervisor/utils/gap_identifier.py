"""Gap identifier - select top gaps by severity."""

import logging
from typing import List

from .trace_analyzer import Gap

logger = logging.getLogger(__name__)


class GapIdentifier:
    """Identify and rank top gaps by severity."""

    def __init__(self) -> None:
        """Initialize identifier."""
        pass

    def calculate_severity(self, gap: Gap) -> float:
        """Calculate severity score for a gap.

        Severity = failure_count × (1 - answer_rate)
        This prioritizes gaps with many failures and low answer rates.

        Args:
            gap: Gap object to score.

        Returns:
            Severity score (higher = more severe).
        """
        if gap.total_count == 0:
            return 0.0

        failure_impact = gap.failure_count
        answer_rate_impact = 1.0 - gap.answer_rate

        severity = failure_impact * answer_rate_impact
        return severity

    def identify(
        self,
        gaps: List[Gap],
        max_gaps: int = 10,
        min_severity: float = 0.0,
    ) -> List[Gap]:
        """Select top N gaps by severity, filtered by minimum threshold.

        Args:
            gaps: List of ranked Gap objects (from TraceAnalyzer).
            max_gaps: Maximum number of gaps to return (default 10).
            min_severity: Minimum severity score to include (default 0.0 = no filter).

        Returns:
            List of top gaps (up to max_gaps), sorted by severity descending.
        """
        logger.info(
            f"Identifying top gaps: max_gaps={max_gaps}, min_severity={min_severity}"
        )

        # Calculate severity for each gap
        gap_scores = []
        for gap in gaps:
            severity = self.calculate_severity(gap)
            gap_scores.append((gap, severity))

        # Filter by minimum severity
        filtered = [(gap, score) for gap, score in gap_scores if score >= min_severity]
        logger.info(f"Filtered to {len(filtered)} gaps above min_severity={min_severity}")

        # Sort by severity descending (highest first)
        sorted_gaps = sorted(filtered, key=lambda x: x[1], reverse=True)

        # Select top N
        selected = [gap for gap, _ in sorted_gaps[:max_gaps]]
        logger.info(f"Selected {len(selected)} top gaps for analysis")

        # Log top gaps
        for i, gap in enumerate(selected, 1):
            severity = self.calculate_severity(gap)
            logger.info(f"  Gap #{i}: {gap.summary()} (severity={severity:.2f})")

        return selected
