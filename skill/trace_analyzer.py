#!/usr/bin/env python3
"""Trace analyzer for supervisor agent — analyze traces by (module, intent) and detect gaps.

This module analyzes Langfuse traces grouped by (module, intent) combination,
calculating per-group metrics like success rates, average confidence, and failure
examples. Gaps are ranked by answer_rate (lowest first = biggest gaps).

Usage:
  analyzer = TraceAnalyzer()
  gaps = analyzer.analyze(traces)
  ranked_gaps = analyzer.rank_by_severity(gaps)

  for gap in ranked_gaps[:10]:
      print(f"{gap.module}/{gap.intent}: {gap.answer_rate:.1%} success rate")
      print(f"  Failures: {gap.failure_count}/{gap.total_count}")
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@dataclass
class Gap:
    """Performance gap for a (module, intent) combination.

    Attributes:
        module: Module label (e.g., "WhatsApp", "KB", "Billing")
        intent: Intent classification (e.g., "setup", "troubleshoot", "pricing")
        total_count: Total traces in this group
        success_count: Number of successful answers (answered=true)
        failure_count: Number of failed answers (answered=false)
        answer_rate: Success rate as decimal (success_count / total_count)
        avg_confidence: Mean confidence score across all traces (0-1)
        failure_examples: List of failing query strings (up to 10)
    """

    module: str
    intent: str
    total_count: int
    success_count: int
    failure_count: int
    answer_rate: float
    avg_confidence: float
    failure_examples: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate Gap invariants."""
        if self.total_count < 0:
            raise ValueError(f"total_count must be >= 0, got {self.total_count}")
        if self.success_count < 0 or self.success_count > self.total_count:
            raise ValueError(
                f"success_count {self.success_count} must be in [0, {self.total_count}]"
            )
        if self.failure_count < 0 or self.failure_count > self.total_count:
            raise ValueError(
                f"failure_count {self.failure_count} must be in [0, {self.total_count}]"
            )
        if self.success_count + self.failure_count != self.total_count:
            raise ValueError(
                f"success_count + failure_count ({self.success_count} + {self.failure_count}) "
                f"must equal total_count ({self.total_count})"
            )
        if not 0.0 <= self.answer_rate <= 1.0:
            raise ValueError(
                f"answer_rate must be in [0.0, 1.0], got {self.answer_rate}"
            )
        if not 0.0 <= self.avg_confidence <= 1.0:
            raise ValueError(
                f"avg_confidence must be in [0.0, 1.0], got {self.avg_confidence}"
            )


class TraceAnalyzer:
    """Analyze traces grouped by (module, intent) to detect performance gaps.

    Attributes:
        min_group_size: Minimum traces required to include a group (default: 1)
        max_failure_examples: Maximum failure queries to store per gap (default: 10)
    """

    def __init__(self, min_group_size: int = 1, max_failure_examples: int = 10):
        """Initialize trace analyzer.

        Args:
            min_group_size: Minimum traces in a group for analysis (default: 1)
            max_failure_examples: Max failure query examples per gap (default: 10)

        Raises:
            ValueError: If parameters are invalid
        """
        if min_group_size < 1:
            raise ValueError(f"min_group_size must be >= 1, got {min_group_size}")
        if max_failure_examples < 0:
            raise ValueError(
                f"max_failure_examples must be >= 0, got {max_failure_examples}"
            )

        self.min_group_size = min_group_size
        self.max_failure_examples = max_failure_examples

    def _extract_metadata_field(
        self, trace: Dict[str, Any], field_name: str, default: Any = None
    ) -> Any:
        """Safely extract a field from trace metadata.

        Args:
            trace: Trace object from Langfuse
            field_name: Metadata field name to extract
            default: Default value if field is missing

        Returns:
            Field value from trace.metadata[field_name] or default
        """
        try:
            metadata = trace.get("metadata", {})
            if not isinstance(metadata, dict):
                return default
            return metadata.get(field_name, default)
        except (AttributeError, TypeError):
            return default

    def _is_successful(self, trace: Dict[str, Any]) -> bool:
        """Determine if a trace represents a successful answer.

        Args:
            trace: Trace object from Langfuse

        Returns:
            True if trace.metadata.answered is true, False otherwise
        """
        answered = self._extract_metadata_field(trace, "answered", False)
        return bool(answered)

    def _get_confidence(self, trace: Dict[str, Any]) -> float:
        """Extract confidence score from trace, normalized to [0, 1].

        Args:
            trace: Trace object from Langfuse

        Returns:
            Confidence score in [0, 1], or 0.0 if missing/invalid
        """
        confidence = self._extract_metadata_field(trace, "confidence", None)

        # Handle None or missing
        if confidence is None:
            return 0.0

        # Normalize numeric confidence
        try:
            conf_float = float(confidence)
            # Clamp to [0, 1]
            if conf_float < 0:
                return 0.0
            if conf_float > 1.0:
                return 1.0
            return conf_float
        except (TypeError, ValueError):
            # Invalid confidence value
            logger.debug(f"Invalid confidence: {confidence} (type: {type(confidence)})")
            return 0.0

    def _get_query(self, trace: Dict[str, Any]) -> str:
        """Extract query string from trace.

        Args:
            trace: Trace object from Langfuse

        Returns:
            Query string (up to 500 chars) or "[no query]" if missing
        """
        query = self._extract_metadata_field(trace, "query", None)
        if query is None:
            query = trace.get("input", {}).get("query", "[no query]")

        # Ensure string and truncate
        query_str = str(query) if query is not None else "[no query]"
        if len(query_str) > 500:
            query_str = query_str[:497] + "…"

        return query_str

    def analyze(self, traces: List[Dict[str, Any]]) -> List[Gap]:
        """Analyze traces and group by (module, intent).

        Groups traces by (module_label, intent) combination, calculating:
        - success_count, failure_count, total_count
        - answer_rate (success_count / total_count)
        - avg_confidence (mean of confidence scores)
        - failure_examples (up to max_failure_examples queries)

        Args:
            traces: List of trace objects from Langfuse

        Returns:
            List of Gap objects (unordered, filtered by min_group_size)

        Note:
            - Groups with fewer than min_group_size traces are excluded
            - Traces with missing module or intent are skipped with warning
            - Confidence scores are normalized to [0, 1]
        """
        if not traces:
            logger.info("No traces to analyze")
            return []

        # Group traces by (module, intent)
        groups: Dict[tuple, Dict[str, Any]] = {}

        for trace in traces:
            module = self._extract_metadata_field(trace, "module_label", None)
            intent = self._extract_metadata_field(trace, "intent", None)

            # Skip traces missing module or intent
            if not module or not intent:
                logger.debug(
                    f"Skipping trace {trace.get('id')} with module={module}, intent={intent}"
                )
                continue

            module = str(module).strip()
            intent = str(intent).strip()

            key = (module, intent)
            if key not in groups:
                groups[key] = {
                    "total": 0,
                    "success": 0,
                    "failure": 0,
                    "confidences": [],
                    "failure_queries": [],
                }

            group = groups[key]
            group["total"] += 1

            # Track success/failure
            if self._is_successful(trace):
                group["success"] += 1
            else:
                group["failure"] += 1
                # Collect failure queries (up to max)
                if len(group["failure_queries"]) < self.max_failure_examples:
                    query = self._get_query(trace)
                    group["failure_queries"].append(query)

            # Collect confidence
            conf = self._get_confidence(trace)
            group["confidences"].append(conf)

        # Convert groups to Gap objects
        gaps: List[Gap] = []

        for (module, intent), group in groups.items():
            # Filter by min group size
            if group["total"] < self.min_group_size:
                logger.debug(
                    f"Skipping {module}/{intent}: {group['total']} traces (below threshold)"
                )
                continue

            # Calculate metrics
            answer_rate = (
                group["success"] / group["total"] if group["total"] > 0 else 0.0
            )
            avg_confidence = (
                sum(group["confidences"]) / len(group["confidences"])
                if group["confidences"]
                else 0.0
            )

            gap = Gap(
                module=module,
                intent=intent,
                total_count=group["total"],
                success_count=group["success"],
                failure_count=group["failure"],
                answer_rate=answer_rate,
                avg_confidence=avg_confidence,
                failure_examples=group["failure_queries"],
            )

            gaps.append(gap)
            logger.debug(
                f"Gap: {module}/{intent} - "
                f"success_rate={gap.answer_rate:.1%}, "
                f"avg_confidence={gap.avg_confidence:.2f}"
            )

        logger.info(
            f"Analyzed {len(traces)} traces into {len(gaps)} (module, intent) groups"
        )
        return gaps

    def rank_by_severity(self, gaps: List[Gap]) -> List[Gap]:
        """Sort gaps by answer_rate ascending (lowest first = biggest gaps).

        Ties are broken by total_count descending (more failures = higher priority).

        Args:
            gaps: List of Gap objects to rank

        Returns:
            Sorted list of gaps (lowest answer_rate first)
        """
        if not gaps:
            return []

        sorted_gaps = sorted(
            gaps, key=lambda g: (g.answer_rate, -g.total_count)
        )

        logger.info(f"Ranked {len(sorted_gaps)} gaps by severity")
        return sorted_gaps


if __name__ == "__main__":
    # Smoke test with sample traces
    sample_traces = [
        {
            "id": "trace-1",
            "metadata": {
                "module_label": "WhatsApp",
                "intent": "setup",
                "answered": True,
                "confidence": 0.95,
                "query": "How to set up WhatsApp?",
            },
        },
        {
            "id": "trace-2",
            "metadata": {
                "module_label": "WhatsApp",
                "intent": "setup",
                "answered": False,
                "confidence": 0.45,
                "query": "WhatsApp coexistence eligibility",
            },
        },
        {
            "id": "trace-3",
            "metadata": {
                "module_label": "Billing",
                "intent": "pricing",
                "answered": True,
                "confidence": 0.88,
                "query": "What are your pricing plans?",
            },
        },
        {
            "id": "trace-4",
            "metadata": {
                "module_label": "Billing",
                "intent": "pricing",
                "answered": False,
                "confidence": 0.30,
                "query": "Enterprise discount eligibility",
            },
        },
    ]

    analyzer = TraceAnalyzer()
    gaps = analyzer.analyze(sample_traces)
    ranked = analyzer.rank_by_severity(gaps)

    print(f"\nAnalyzed {len(sample_traces)} traces into {len(gaps)} gaps:")
    for gap in ranked:
        print(
            f"  {gap.module}/{gap.intent}: "
            f"success_rate={gap.answer_rate:.1%}, "
            f"avg_confidence={gap.avg_confidence:.2f}, "
            f"total={gap.total_count}"
        )
