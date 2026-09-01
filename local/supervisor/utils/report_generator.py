"""Report generator - format markdown report from gap classifications."""

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .trace_analyzer import Gap
from .qwen_interface import QwenInterface

logger = logging.getLogger(__name__)

# Human-readable labels + one-line action guidance per category. Keeps the
# per-gap rendering logic (format_gap_section) a lookup instead of a long
# if/elif chain, and keeps the "what do I do about this" guidance in one
# place instead of scattered across category-specific branches.
_CATEGORY_LABELS = {
    "ALREADY_FIXED": "✅ Already Fixed",
    "CODE_GAP_ALIAS_CANDIDATE": "🔧 Code Gap — Alias Candidate",
    "CODE_GAP_MISSING_CONCEPT": "🔧 Code Gap — Missing Concept Entry",
    "CODE_GAP_NEEDS_INVESTIGATION": "🔎 Code Gap — Needs Investigation",
    "CONTENT_GAP": "📄 Content Gap",
    "OUT_OF_SCOPE_PRICING": "💰 Out of Scope — Pricing (Sales Signal)",
    "OUT_OF_SCOPE_ACCOUNT_SUPPORT": "🔐 Out of Scope — Account/Support",
    "MIXED": "⚠️ Mixed — Heterogeneous Gap",
}

_CATEGORY_ACTIONS = {
    "ALREADY_FIXED": "No action needed — a prior fix already resolved this. Verify on next supervisor run that it stays fixed.",
    "CODE_GAP_ALIAS_CANDIDATE": "Add the suggested aliases to the named CONCEPT_REGISTRY entry in skill/kb_answer.py, verify via the offline regression harness, then commit.",
    "CODE_GAP_MISSING_CONCEPT": "Review the matched KB files below — likely needs a new CONCEPT_REGISTRY entry (not just aliases on an existing one).",
    "CODE_GAP_NEEDS_INVESTIGATION": "Rule-based classification can't diagnose this — needs a code investigation agent (see Hermes judge verdict below, if available).",
    "CONTENT_GAP": "No matching KB content found. Route to the KB content team — this is not a code fix.",
    "OUT_OF_SCOPE_PRICING": "Forward to sales/deals team. This skill intentionally does not answer pricing questions.",
    "OUT_OF_SCOPE_ACCOUNT_SUPPORT": "Route to account support — not a documentable KB topic (personal account recovery / OTP / login issues).",
    "MIXED": "This gap groups multiple distinct problem types under one (module, intent) label — review the per-category breakdown below rather than treating it as one issue.",
}


class ReportGenerator:
    """Generate markdown report from GapClassifier output."""

    def __init__(self, qwen: QwenInterface = None) -> None:
        """Initialize report generator.

        Args:
            qwen: Unused by the current classification-driven report (kept
                for backward compatibility / future optional LLM commentary).
        """
        self.qwen = qwen

    def format_gap_section(
        self,
        gap_index: int,
        gap: Gap,
        classification: Dict[str, Any],
        judge_verdict: Dict[str, Any] = None,
    ) -> str:
        """Format markdown section for one gap from its classification result.

        Args:
            gap_index: Gap number (1, 2, 3, etc.).
            gap: Gap object with metrics.
            classification: Result dict from GapClassifier.classify_gap()
                (category, confidence, evidence, per_query_results).
            judge_verdict: Optional Hermes judge result for
                CODE_GAP_NEEDS_INVESTIGATION cases.

        Returns:
            Formatted markdown string.
        """
        category = classification["category"]
        label = _CATEGORY_LABELS.get(category, category)
        action = _CATEGORY_ACTIONS.get(category, "Review manually.")

        section = f"""## Gap #{gap_index}: {gap.module} / {gap.intent}

**Severity:** {gap.failure_count} failures, {gap.answer_rate*100:.1f}% answer rate

**Classification:** {label} (confidence: {classification['confidence']})

**Sample Failures:**
"""
        for query in gap.failure_examples[:3]:
            section += f"  - {query}\n"

        if category == "MIXED":
            breakdown = classification["evidence"]["category_breakdown"]
            section += "\n**Category Breakdown:**\n"
            for sub_category, queries in breakdown.items():
                sub_label = _CATEGORY_LABELS.get(sub_category, sub_category)
                section += f"  - {sub_label} ({len(queries)} sample{'s' if len(queries) != 1 else ''}):\n"
                for q in queries:
                    section += f"      - {q[:120]}\n"
        else:
            section += self._format_category_evidence(category, classification)

        if judge_verdict is not None:
            section += "\n**Hermes Judge Verdict:**\n"
            if judge_verdict.get("degraded"):
                section += f"  - ⚠️ Degraded (Hermes unavailable): {judge_verdict['reasoning']}\n"
            else:
                section += f"  - Root cause: `{judge_verdict['root_cause']}` (confidence: {judge_verdict['confidence']:.0%})\n"
                section += f"  - Reasoning: {judge_verdict['reasoning']}\n"
                section += f"  - Suggested next step: {judge_verdict['suggested_next_step']}\n"

        section += f"\n**Recommendation:** {action}\n\n"
        return section

    def _format_category_evidence(self, category: str, classification: Dict[str, Any]) -> str:
        """Render category-specific evidence from the first per-query result."""
        per_query = classification.get("per_query_results", [])
        if not per_query:
            return ""
        result = per_query[0]
        evidence = result.get("evidence", {})
        out = ""

        if category == "ALREADY_FIXED":
            out += f"\n**Evidence:** Re-running against current skill code now produces a real answer.\n"
            out += f"  - Answer preview: {evidence.get('answer_preview', '')}\n"
            out += f"  - Evidence sources: {', '.join(evidence.get('evidence_sources', [])) or 'none'}\n"

        elif category == "CODE_GAP_ALIAS_CANDIDATE":
            out += "\n**Near-Miss Concepts (alias candidates):**\n"
            for concept in evidence.get("near_miss_concepts", []):
                out += f"  - `{concept['concept_id']}` — matched keywords: {concept['matched_keywords']}\n"
                out += f"    existing aliases (sample): {concept['existing_aliases_sample']}\n"

        elif category == "CODE_GAP_MISSING_CONCEPT":
            content_check = evidence.get("content_check", {})
            out += f"\n**On-topic KB content found (no CONCEPT_REGISTRY entry claims it):**\n"
            for m in content_check.get("matches", []):
                out += f"  - `{m['source']}` (coverage: {m['coverage']:.0%}, matched terms: {m['matched_terms']})\n"

        elif category == "CODE_GAP_NEEDS_INVESTIGATION":
            out += f"\n**Evidence:** {evidence.get('reason', 'entities matched but answer is still IDK')}\n"
            out += f"  - Module/Intent: {evidence.get('module')} / {evidence.get('intent')}\n"
            out += f"  - Entities matched: {evidence.get('entities', [])}\n"
            out += f"  - Evidence sources: {', '.join(evidence.get('evidence_sources', [])) or 'none'}\n"
            out += f"  - Top score: {evidence.get('top_score')}\n"

        elif category == "CONTENT_GAP":
            content_check = evidence.get("content_check", {})
            out += f"\n**Evidence:** No entity/keyword match and no on-topic KB content found.\n"
            if content_check.get("checked_terms"):
                out += f"  - Terms checked: {content_check['checked_terms']}\n"

        elif category == "OUT_OF_SCOPE_PRICING":
            out += f"\n**Matched pricing keywords:** {evidence.get('matched_keywords', [])}\n"

        elif category == "OUT_OF_SCOPE_ACCOUNT_SUPPORT":
            out += f"\n**Matched account/support phrases:** {evidence.get('matched_phrases', [])}\n"

        return out

    def generate_report(
        self,
        gaps: List[Gap],
        traces: List[Dict[str, Any]],
        output_path: Path,
        classifications: Dict[str, Dict[str, Any]] = None,
        judge_verdicts: Dict[str, Dict[str, Any]] = None,
    ) -> str:
        """Generate full markdown report from gap classifications.

        Args:
            gaps: List of selected Gap objects.
            traces: Complete list of all traces (for metrics).
            output_path: Path to write report.
            classifications: Dict of gap_id -> GapClassifier.classify_gap() result.
            judge_verdicts: Dict of gap_id -> HermesJudge.judge_gap() result
                (only present for gaps that needed judging).

        Returns:
            Full report text.
        """
        logger.info(f"Generating report ({len(gaps)} gaps)...")
        classifications = classifications or {}
        judge_verdicts = judge_verdicts or {}

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

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

        if classifications:
            category_counts: Dict[str, int] = {}
            for result in classifications.values():
                category_counts[result["category"]] = category_counts.get(result["category"], 0) + 1

            report += "## Classification Summary\n\n"
            for category, count in sorted(category_counts.items(), key=lambda x: -x[1]):
                label = _CATEGORY_LABELS.get(category, category)
                report += f"- **{label}:** {count} gap{'s' if count != 1 else ''}\n"
            report += "\n"

        # Per-gap sections
        for i, gap in enumerate(gaps, 1):
            gap_key = f"Gap #{i}"
            classification = classifications.get(gap_key)
            judge_verdict = judge_verdicts.get(gap_key)

            if classification is None:
                # No classifier result available for this gap (shouldn't
                # normally happen) — render a minimal fallback section.
                report += f"## Gap #{i}: {gap.module} / {gap.intent}\n\n"
                report += f"**Severity:** {gap.failure_count} failures, {gap.answer_rate*100:.1f}% answer rate\n\n"
                report += "**Classification:** unavailable\n\n"
                continue

            report += self.format_gap_section(i, gap, classification, judge_verdict)

        # Metrics section
        modules_affected: Dict[str, Dict[str, int]] = {}
        for trace in traces:
            metadata = trace.get("metadata", {})
            module = metadata.get("module_label", trace.get("module", "Unknown"))
            answered = metadata.get("answered", trace.get("answered", False))
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

        report += "\n## Action Items\n\n"
        for i, gap in enumerate(gaps, 1):
            gap_key = f"Gap #{i}"
            classification = classifications.get(gap_key)
            category = classification["category"] if classification else "unavailable"
            label = _CATEGORY_LABELS.get(category, category)
            report += f"  - [ ] Gap #{i}: {gap.module} / {gap.intent} — {label}\n"

        report += f"\n---\n\n**Local Logs:** `local/supervisor/logs/supervisor_*.log`\n\n"

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                f.write(report)
            logger.info(f"Report written to {output_path}")
        except IOError as e:
            logger.error(f"Failed to write report: {e}")

        return report
