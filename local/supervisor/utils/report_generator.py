"""Report generator - format markdown report and call Qwen for recommendations."""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .trace_analyzer import Gap
from .qwen_interface import QwenInterface

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate markdown report with Qwen-powered gap analysis."""

    def __init__(self, qwen: QwenInterface) -> None:
        """Initialize report generator.

        Args:
            qwen: QwenInterface instance for LLM calls.
        """
        self.qwen = qwen

    def generate_fallback_recommendation(self, gap: Gap) -> str:
        """Generate smart fallback recommendation based on gap analysis.

        Args:
            gap: Gap object with failure patterns.

        Returns:
            Actionable recommendation text.
        """
        # Analyze failure patterns to infer what's missing
        failure_text = " ".join(gap.failure_examples[:5]).lower()

        # Pattern matching for common KB gaps
        if any(word in failure_text for word in ["price", "pricing", "cost", "fee", "rate", "charge"]):
            return f"Add comprehensive pricing documentation to `kb/{gap.module.lower()}/{gap.intent.lower()}.md`. Include: regional rates, volume discounts, payment terms, and FAQ for common pricing questions."

        if any(word in failure_text for word in ["setup", "install", "configure", "onboard", "enable", "activate"]):
            return f"Expand setup/configuration guide in `kb/{gap.module.lower()}/{gap.intent.lower()}.md`. Add step-by-step instructions, prerequisites, troubleshooting, and common configuration scenarios."

        if any(word in failure_text for word in ["api", "endpoint", "request", "response", "parameter", "payload"]):
            return f"Update API reference documentation in `kb/{gap.module.lower()}/{gap.intent.lower()}.md`. Include: endpoint details, request/response formats, error codes, code examples, and authentication."

        if any(word in failure_text for word in ["error", "fail", "bug", "issue", "timeout", "crash"]):
            return f"Add troubleshooting and error handling section to `kb/{gap.module.lower()}/{gap.intent.lower()}.md`. Document common error codes, causes, and resolution steps."

        if any(word in failure_text for word in ["limit", "quota", "rate", "maximum", "minimum", "constraint"]):
            return f"Document limits and constraints in `kb/{gap.module.lower()}/{gap.intent.lower()}.md`. Specify: rate limits, size limits, quotas, thresholds, and workarounds."

        if any(word in failure_text for word in ["feature", "capability", "support", "available", "work", "compatible"]):
            return f"Add feature matrix/capability documentation to `kb/{gap.module.lower()}/{gap.intent.lower()}.md`. List supported features, versions, and platform compatibility."

        if any(word in failure_text for word in ["how", "way", "method", "approach", "best practice"]):
            return f"Add best practices and how-to guides to `kb/{gap.module.lower()}/{gap.intent.lower()}.md`. Include: common use cases, recommended approaches, and code patterns."

        # Default fallback
        failure_rate = (1 - gap.answer_rate) * 100
        return f"Review and expand `kb/{gap.module.lower()}/{gap.intent.lower()}.md` to address {failure_rate:.0f}% of unanswered queries. Analyze sample failures to identify missing sections and add comprehensive documentation."

    def analyze_gap_with_qwen(self, gap: Gap, success_examples: List[str]) -> Dict[str, str]:
        """Analyze gap using Qwen LLM, with smart fallback recommendations.

        Args:
            gap: Gap object to analyze.
            success_examples: Examples of successful queries for comparison.

        Returns:
            Dictionary with 'root_cause', 'kb_gap', and 'recommendation' keys.
        """
        logger.info(f"Analyzing gap: {gap.summary()}")

        # Build prompt for Qwen
        failure_examples = "\n".join(f"  - {q}" for q in gap.failure_examples[:3])
        success_exs = "\n".join(f"  - {q}" for q in success_examples[:3])

        prompt = f"""Analyze this KB gap and provide recommendations.

**Gap Details:**
- Module: {gap.module}
- Intent: {gap.intent}
- Answer Rate: {gap.answer_rate*100:.1f}% ({gap.success_count}/{gap.total_count})
- Failures: {gap.failure_count}

**Failing Queries (examples):**
{failure_examples}

**Successful Queries (for reference):**
{success_exs}

**Task:**
1. Identify the root cause (what's missing from the KB?)
2. Specify the KB file/section that needs updating
3. Provide actionable recommendations for the KB team

Format your response as JSON with these keys:
- root_cause (brief sentence)
- kb_gap (file path, e.g., kb/module/intent.md)
- recommendation (detailed, actionable steps)

Example:
{{"root_cause": "KB missing pricing section", "kb_gap": "kb/whatsapp/pricing.md", "recommendation": "Add regional pricing table..."}}"""

        response = self.qwen.call(prompt)
        if not response:
            logger.warning(f"Qwen call failed for {gap.summary()}, using smart fallback")
            return {
                "root_cause": f"KB section missing or incomplete (based on {gap.failure_count} failures)",
                "kb_gap": f"kb/{gap.module.lower()}/{gap.intent.lower()}.md",
                "recommendation": self.generate_fallback_recommendation(gap),
            }

        # Parse JSON response
        try:
            analysis = json.loads(response)
            return {
                "root_cause": analysis.get("root_cause", ""),
                "kb_gap": analysis.get("kb_gap", ""),
                "recommendation": analysis.get("recommendation", ""),
            }
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse Qwen JSON, using smart fallback: {response[:100]}")
            return {
                "root_cause": f"KB section missing or incomplete (based on {gap.failure_count} failures)",
                "kb_gap": f"kb/{gap.module.lower()}/{gap.intent.lower()}.md",
                "recommendation": self.generate_fallback_recommendation(gap),
            }

    def format_gap_section(self, gap_index: int, gap: Gap, analysis: Dict[str, str]) -> str:
        """Format markdown section for one gap.

        Args:
            gap_index: Gap number (1, 2, 3, etc.).
            gap: Gap object with metrics.
            analysis: Analysis dict from Qwen (root_cause, kb_gap, recommendation).

        Returns:
            Formatted markdown string.
        """
        section = f"""## Gap #{gap_index}: {gap.module} / {gap.intent}

**Severity:** {gap.failure_count} failures, {gap.answer_rate*100:.1f}% answer rate

**Sample Failures:**
"""
        for query in gap.failure_examples[:3]:
            section += f"  - {query}\n"

        section += f"""
**Root Cause:** {analysis.get("root_cause", "N/A")}

**KB File:** `{analysis.get("kb_gap", "N/A")}`

**Recommendation:**
{analysis.get("recommendation", "N/A")}

"""
        return section

    def generate_report(
        self,
        gaps: List[Gap],
        traces: List[Dict[str, Any]],
        output_path: Path,
    ) -> str:
        """Generate full markdown report with Qwen analysis.

        Args:
            gaps: List of selected Gap objects.
            traces: Complete list of all traces (for metrics).
            output_path: Path to write report.

        Returns:
            Full report text.
        """
        logger.info(f"Generating report ({len(gaps)} gaps)...")

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        # Summary section
        total_failures = sum(g.failure_count for g in gaps)
        total_successes = sum(g.success_count for g in gaps)
        overall_answer_rate = (
            (total_successes / (total_successes + total_failures) * 100)
            if (total_successes + total_failures) > 0
            else 0
        )

        report = f"""# KB Supervisor Analysis Report

**Generated:** {timestamp}

## Summary

- **Traces Analyzed:** {len(traces)}
- **Total Failures:** {total_failures}
- **Total Successes:** {total_successes}
- **Overall Answer Rate:** {overall_answer_rate:.1f}%
- **Gaps Identified:** {len(gaps)} (up to 10, severity-driven)

"""

        # Per-gap sections
        for i, gap in enumerate(gaps, 1):
            # Get all success examples from traces for this gap
            success_examples = gap.success_examples or [
                t.get("query", "")
                for t in traces
                if t.get("module") == gap.module
                and t.get("intent") == gap.intent
                and t.get("answered", False)
            ][:3]

            analysis = self.analyze_gap_with_qwen(gap, success_examples)
            gap_section = self.format_gap_section(i, gap, analysis)
            report += gap_section

        # Metrics section
        modules_affected = {}
        for trace in traces:
            module = trace.get("module", "Unknown")
            answered = trace.get("answered", False)
            if module not in modules_affected:
                modules_affected[module] = {"success": 0, "total": 0}
            modules_affected[module]["total"] += 1
            if answered:
                modules_affected[module]["success"] += 1

        report += "## Metrics\n\n**Modules Most Affected:**\n"
        for module, counts in sorted(
            modules_affected.items(),
            key=lambda x: x[1]["success"] / x[1]["total"] if x[1]["total"] > 0 else 1,
        ):
            module_rate = (
                (counts["success"] / counts["total"] * 100)
                if counts["total"] > 0
                else 0
            )
            report += f"  - {module}: {module_rate:.1f}% answer rate ({counts['success']}/{counts['total']})\n"

        report += f"""
## Action Items

"""
        for i, gap in enumerate(gaps, 1):
            report += f"  - [ ] Gap #{i}: {gap.module} team - Review and implement recommendations\n"

        report += f"""
---

**Local Logs:** `local/supervisor/logs/supervisor_*.log`

"""

        # Write report
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                f.write(report)
            logger.info(f"Report written to {output_path}")
        except IOError as e:
            logger.error(f"Failed to write report: {e}")

        return report
