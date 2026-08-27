#!/usr/bin/env python3
"""Gap identifier for supervisor agent — filter and rank performance gaps by severity.

This module takes ranked gaps from the analyzer and applies severity scoring to identify
the most impactful performance issues for Qwen root-cause analysis. Severity is calculated
as: severity_score = (failure_count × answer_rate_impact), where answer_rate_impact is
the complement (1 - answer_rate), representing the performance deficit.

Gap enrichment prepares a summary sentence for each selected gap to provide context to
the Qwen analysis engine.

Usage:
  identifier = GapIdentifier()
  priority_gaps = identifier.identify(
      gaps=ranked_gaps,
      max_gaps=10,
      min_severity=0.5
  )

  for gap in priority_gaps:
      print(f"{gap.module}/{gap.intent}: severity={gap.severity_score:.2f}")
      print(f"  Summary: {gap.summary}")
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# For module imports in skill/, use absolute path or inline Gap class
# (trace_analyzer is in same directory as gap_identifier)
try:
    from trace_analyzer import Gap
except ImportError:
    # Fallback: define minimal Gap interface locally for testing
    from dataclasses import dataclass as dc

    @dc
    class Gap:  # type: ignore
        """Minimal Gap interface for testing."""
        module: str
        intent: str
        total_count: int
        success_count: int
        failure_count: int
        answer_rate: float
        avg_confidence: float
        failure_examples: List[str] = field(default_factory=list)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@dataclass
class EnrichedGap:
    """Performance gap with calculated severity and enrichment for root-cause analysis.

    Extends the base Gap with severity scoring and a summary prepared for
    Qwen analysis. The severity_score reflects the combined impact of failure
    frequency and answer rate deficit.

    Attributes:
        module: Module label (e.g., "WhatsApp", "KB", "Billing")
        intent: Intent classification (e.g., "setup", "troubleshoot", "pricing")
        total_count: Total traces in this group
        success_count: Number of successful answers (answered=true)
        failure_count: Number of failed answers (answered=false)
        answer_rate: Success rate as decimal (success_count / total_count)
        avg_confidence: Mean confidence score across all traces (0-1)
        failure_examples: List of failing query strings (up to 10)
        severity_score: Calculated severity = failure_count × (1 - answer_rate)
        summary: Enriched summary sentence for Qwen analysis
    """

    module: str
    intent: str
    total_count: int
    success_count: int
    failure_count: int
    answer_rate: float
    avg_confidence: float
    failure_examples: List[str] = field(default_factory=list)
    severity_score: float = 0.0
    summary: str = ""

    def __post_init__(self) -> None:
        """Validate EnrichedGap invariants."""
        if self.severity_score < 0.0:
            raise ValueError(
                f"severity_score must be >= 0.0, got {self.severity_score}"
            )


class GapIdentifier:
    """Identify and rank performance gaps by severity for supervisor analysis.

    This class filters gaps based on severity thresholds and selects top-N gaps
    for Qwen root-cause analysis. Severity is calculated as:
      severity_score = failure_count × (1 - answer_rate)

    This formula captures both the frequency of failures and the magnitude of the
    performance deficit relative to perfect (1.0) answer rate.

    Attributes:
        default_min_severity: Minimum severity threshold (default: 0.1)
    """

    def __init__(self, default_min_severity: float = 0.1):
        """Initialize gap identifier.

        Args:
            default_min_severity: Default minimum severity threshold (default: 0.1)

        Raises:
            ValueError: If default_min_severity is negative
        """
        if default_min_severity < 0.0:
            raise ValueError(
                f"default_min_severity must be >= 0.0, got {default_min_severity}"
            )
        self.default_min_severity = default_min_severity

    def calculate_severity(self, gap: Gap) -> float:
        """Calculate severity score for a gap.

        Severity captures both the magnitude and frequency of the performance deficit:
          severity_score = failure_count × (1 - answer_rate)

        Where:
        - failure_count: Absolute count of failures (higher = more urgent)
        - (1 - answer_rate): Performance deficit (higher = worse answer rate)

        A gap with 10 failures and 50% answer_rate gets score 5.0.
        A gap with 100 failures and 90% answer_rate also gets score 10.0.
        Both are equally severe from the system's perspective.

        Args:
            gap: Gap object to score

        Returns:
            Severity score >= 0.0

        Raises:
            ValueError: If gap data is invalid
        """
        if gap.failure_count < 0:
            raise ValueError(f"gap.failure_count must be >= 0, got {gap.failure_count}")

        if not 0.0 <= gap.answer_rate <= 1.0:
            raise ValueError(
                f"gap.answer_rate must be in [0.0, 1.0], got {gap.answer_rate}"
            )

        # Calculate answer rate impact (complement: how far from perfect)
        answer_rate_impact = 1.0 - gap.answer_rate

        # Severity = frequency × magnitude of deficit
        severity_score = gap.failure_count * answer_rate_impact

        logger.debug(
            f"Severity {gap.module}/{gap.intent}: "
            f"failures={gap.failure_count}, impact={answer_rate_impact:.2f}, "
            f"score={severity_score:.2f}"
        )

        return severity_score

    def _generate_summary(self, gap: Gap, severity_score: float) -> str:
        """Generate an enriched summary sentence for Qwen analysis.

        The summary provides context about the gap's characteristics, helping
        the root-cause analyzer understand the scope and nature of the problem.

        Args:
            gap: Gap object to summarize
            severity_score: Calculated severity score

        Returns:
            Summary string (max 200 chars)
        """
        # Build severity label
        if severity_score >= 10.0:
            severity_label = "critical"
        elif severity_score >= 5.0:
            severity_label = "high"
        elif severity_score >= 2.0:
            severity_label = "medium"
        else:
            severity_label = "low"

        # Build summary with key metrics
        summary = (
            f"{severity_label.upper()} gap in {gap.module}/{gap.intent}: "
            f"{gap.failure_count} failures / {gap.total_count} attempts "
            f"({gap.answer_rate:.0%} success). "
            f"Avg confidence: {gap.avg_confidence:.2f}."
        )

        # Truncate if needed (shouldn't happen with typical data)
        if len(summary) > 200:
            summary = summary[:197] + "…"

        return summary

    def identify(
        self,
        gaps: List[Gap],
        max_gaps: int = 10,
        min_severity: Optional[float] = None,
    ) -> List[EnrichedGap]:
        """Filter and rank gaps by severity, selecting top N for analysis.

        This method:
        1. Calculates severity_score for each gap
        2. Filters by minimum severity threshold
        3. Selects top N gaps (ranked by severity descending)
        4. Enriches each gap with summary for Qwen

        Args:
            gaps: List of Gap objects from analyzer (already ranked by answer_rate)
            max_gaps: Maximum number of gaps to return (default: 10)
            min_severity: Minimum severity threshold (uses default if None)

        Returns:
            List of EnrichedGap objects (up to max_gaps), ranked by severity (highest first)

        Raises:
            ValueError: If max_gaps < 1 or min_severity is negative
        """
        # Validate parameters
        if max_gaps < 1:
            raise ValueError(f"max_gaps must be >= 1, got {max_gaps}")

        if min_severity is None:
            min_severity = self.default_min_severity

        if min_severity < 0.0:
            raise ValueError(f"min_severity must be >= 0.0, got {min_severity}")

        if not gaps:
            logger.info("No gaps to identify")
            return []

        # Calculate severity for all gaps
        enriched: List[EnrichedGap] = []

        for gap in gaps:
            severity_score = self.calculate_severity(gap)

            # Filter by minimum severity
            if severity_score < min_severity:
                logger.debug(
                    f"Skipping {gap.module}/{gap.intent}: "
                    f"severity {severity_score:.2f} < {min_severity:.2f}"
                )
                continue

            # Generate enriched summary
            summary = self._generate_summary(gap, severity_score)

            # Create enriched gap
            enriched_gap = EnrichedGap(
                module=gap.module,
                intent=gap.intent,
                total_count=gap.total_count,
                success_count=gap.success_count,
                failure_count=gap.failure_count,
                answer_rate=gap.answer_rate,
                avg_confidence=gap.avg_confidence,
                failure_examples=gap.failure_examples,
                severity_score=severity_score,
                summary=summary,
            )

            enriched.append(enriched_gap)

        # Sort by severity descending (highest first)
        sorted_enriched = sorted(enriched, key=lambda g: g.severity_score, reverse=True)

        # Select top N
        selected = sorted_enriched[:max_gaps]

        logger.info(
            f"Identified {len(selected)} gaps above severity {min_severity:.2f} "
            f"(from {len(gaps)} total gaps, {len(enriched)} above threshold)"
        )

        for i, gap in enumerate(selected, 1):
            logger.info(
                f"  {i}. {gap.module}/{gap.intent}: severity={gap.severity_score:.2f}, "
                f"answer_rate={gap.answer_rate:.1%}"
            )

        return selected


if __name__ == "__main__":
    # Smoke test with sample gaps from trace_analyzer
    sample_gaps = [
        Gap(
            module="WhatsApp",
            intent="setup",
            total_count=10,
            success_count=7,
            failure_count=3,
            answer_rate=0.7,
            avg_confidence=0.78,
            failure_examples=["How to set up WhatsApp?", "WhatsApp coexistence"],
        ),
        Gap(
            module="Billing",
            intent="pricing",
            total_count=20,
            success_count=8,
            failure_count=12,
            answer_rate=0.4,
            avg_confidence=0.65,
            failure_examples=["Enterprise discount", "Volume pricing"],
        ),
        Gap(
            module="KB",
            intent="search",
            total_count=50,
            success_count=45,
            failure_count=5,
            answer_rate=0.9,
            avg_confidence=0.92,
            failure_examples=["Obscure query"],
        ),
        Gap(
            module="Integration",
            intent="troubleshoot",
            total_count=100,
            success_count=20,
            failure_count=80,
            answer_rate=0.2,
            avg_confidence=0.45,
            failure_examples=["API timeout", "Connection refused"],
        ),
    ]

    identifier = GapIdentifier(default_min_severity=0.5)
    priority_gaps = identifier.identify(
        gaps=sample_gaps,
        max_gaps=10,
        min_severity=1.0,
    )

    print(f"\nIdentified {len(priority_gaps)} priority gaps (min_severity=1.0):")
    for i, gap in enumerate(priority_gaps, 1):
        print(f"\n  {i}. {gap.module}/{gap.intent}")
        print(f"     Severity: {gap.severity_score:.2f}")
        print(f"     Answer Rate: {gap.answer_rate:.1%} ({gap.failure_count}/{gap.total_count})")
        print(f"     Summary: {gap.summary}")
        if gap.failure_examples:
            print(f"     Examples: {gap.failure_examples[:2]}")
