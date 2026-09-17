"""Report generator - produce a 3-section supervisor markdown report from 4-bucket verdicts."""

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .trace_analyzer import Gap
from .qwen_interface import QwenInterface
from .gap_classifier import OUT_OF_SCOPE_GENERAL, NOISE

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generate a 3-section markdown supervisor report from pre-computed verdicts."""

    def __init__(self, qwen: QwenInterface) -> None:
        self.qwen = qwen

    def generate_report(
        self,
        gaps: List[Gap],
        traces: List[Dict[str, Any]],
        output_path: Path,
        classifications: Dict[str, Any] = None,
        judge_verdicts: Dict[str, Any] = None,
    ) -> str:
        """Generate the 3-section supervisor report.

        Args:
            gaps: List of selected Gap objects.
            traces: Complete list of all traces (unused in body, kept for signature compat).
            output_path: Path to write report.
            classifications: gap_key -> classify_gap() result dict.
            judge_verdicts: gap_key -> judge_gap_4bucket() result dict.

        Returns:
            Full report text.
        """
        logger.info(f"Generating report ({len(gaps)} gaps)...")

        classifications = classifications or {}
        judge_verdicts = judge_verdicts or {}

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        # Route each gap into its bucket
        fix_now = []       # HAS_DOCS_FAILS
        create_docs = []   # NO_DOCS_IN_SCOPE
        ignored = []       # OUT_OF_SCOPE or NOISE

        for gap in gaps:
            gap_key = f"{gap.module}/{gap.intent}"
            verdict = judge_verdicts.get(gap_key)
            if verdict:
                bucket = verdict.get("bucket", "")
            else:
                # Fall back to classifications
                cat = classifications.get(gap_key, {}).get("category", "")
                if cat in (OUT_OF_SCOPE_GENERAL, NOISE, "OUT_OF_SCOPE_PRICING",
                           "OUT_OF_SCOPE_ACCOUNT_SUPPORT"):
                    bucket = "OUT_OF_SCOPE"
                else:
                    bucket = "HAS_DOCS_FAILS"  # default — actionable

            if bucket == "HAS_DOCS_FAILS":
                fix_now.append((gap, verdict or {}))
            elif bucket == "NO_DOCS_IN_SCOPE":
                create_docs.append((gap, verdict or {}))
            else:
                reason = ""
                if verdict:
                    reason = verdict.get("reason_ignored") or verdict.get("reasoning") or bucket
                else:
                    reason = classifications.get(gap_key, {}).get("category", bucket)
                ignored.append((gap, bucket, reason))

        # Build report
        report_lines = [
            f"# KB Supervisor Report — {timestamp}",
            "",
            "## Summary",
            f"- **Gaps analyzed:** {len(gaps)}",
            f"- **Fix Now (code changes):** {len(fix_now)} gaps — keywords/routing additions that unblock existing docs",
            f"- **Create Docs:** {len(create_docs)} gaps — in-scope topics with no KB coverage",
            f"- **Ignored:** {len(ignored)} gaps (out of scope / noise)",
            "",
            "---",
            "",
        ]

        # Section 1: Fix Now
        report_lines += [
            "## Fix Now — Queries Failing Despite Existing Docs",
            "",
            "> These gaps have KB coverage. The skill is IDKing due to keyword gaps, routing misses, or retrieval rank.",
            "> Action: add the suggested keywords to EXPLICIT_MODULES or CONCEPT_REGISTRY in kb_answer.py.",
            "",
        ]
        for i, (gap, verdict) in enumerate(fix_now, 1):
            matching_doc = verdict.get("matching_doc") or "unknown"
            root_cause = verdict.get("root_cause") or "unknown"
            keywords = verdict.get("keywords_to_add") or []
            sample_queries = (gap.failure_examples or [])[:5]

            report_lines.append(
                f"### Gap #{i}: {gap.module} / {gap.intent} — {gap.failure_count} failures "
                f"({gap.answer_rate:.1%} answer rate)"
            )
            report_lines.append(f"**Matching KB doc:** `{matching_doc}`")
            report_lines.append(f"**Root cause:** {root_cause}")
            if keywords:
                report_lines.append("**Suggested keywords to add:**")
                for kw in keywords:
                    report_lines.append(f'- `"{kw}"`')
            else:
                # Fall back to per_query_notes if judge gave us them
                per_query_notes = verdict.get("per_query_notes") or {}
                if per_query_notes:
                    report_lines.append("**Per-query diagnosis:**")
                    for q_prefix, note in per_query_notes.items():
                        report_lines.append(f"- `{q_prefix}`: {note}")
                else:
                    report_lines.append("**Note:** Judge could not identify specific keywords. "
                                        "Manual investigation of retrieved docs recommended.")
            report_lines.append("")
            report_lines.append("**Reasoning:** " + (verdict.get("reasoning") or ""))
            report_lines.append("")
            report_lines.append("**Sample failing queries:**")
            for q in sample_queries:
                report_lines.append(f'- "{q}"')
            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")

        # Section 2: Create Docs
        report_lines += [
            "## Create Docs — In-Scope Gaps with No KB Coverage",
            "",
            "> These gaps need new KB documents. Prioritized by failure volume and user impact.",
            "",
        ]
        for gap, verdict in create_docs:
            priority = (verdict.get("doc_priority") or "medium").upper()
            doc_to_create = verdict.get("doc_to_create") or f"kb/{gap.module.lower()}/{gap.intent.lower()}.md"
            doc_outline = verdict.get("doc_outline") or "*(no outline generated)*"
            sample_queries = (gap.failure_examples or [])[:5]

            report_lines.append(
                f"### [Priority: {priority}] {gap.module} / {gap.intent} — {gap.failure_count} failures"
            )
            report_lines.append(f"**Suggested file:** `{doc_to_create}`")
            report_lines.append("**Sample queries:**")
            for q in sample_queries:
                report_lines.append(f'- "{q}"')
            report_lines.append("")
            report_lines.append("**Outline:**")
            report_lines.append(doc_outline)
            report_lines.append("")
            report_lines.append("---")
            report_lines.append("")

        # Section 3: Ignored
        report_lines += [
            "## Ignored — Out of Scope / Noise",
            "",
            "| Gap | Failures | Reason |",
            "|---|---|---|",
        ]
        for gap, bucket, reason in ignored:
            reason_str = str(reason).replace("|", "/")
            report_lines.append(f"| {gap.module} / {gap.intent} | {gap.failure_count} | {bucket} — {reason_str} |")
        report_lines.append("")
        report_lines.append("*The skill is correct to return IDK for these. No action needed.*")
        report_lines.append("")

        report = "\n".join(report_lines)

        # Determine write path — use timestamp-based filename if output_path is generic
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        if output_path is None:
            _REPO_ROOT = Path(__file__).resolve().parents[3]
            output_path = _REPO_ROOT / "local" / "reports" / f"supervisor_{ts}.md"
        elif output_path.name == "supervisor_.md" or not output_path.stem.replace("supervisor_", ""):
            output_path = output_path.parent / f"supervisor_{ts}.md"

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                f.write(report)
            logger.info(f"Report written to {output_path}")
        except IOError as e:
            logger.error(f"Failed to write report: {e}")

        return report
