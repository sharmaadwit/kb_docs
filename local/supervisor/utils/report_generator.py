"""Report generator — single-table supervisor report from 4-bucket verdicts."""

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .trace_analyzer import Gap
from .qwen_interface import QwenInterface
from .gap_classifier import OUT_OF_SCOPE_GENERAL, NOISE

logger = logging.getLogger(__name__)

_BUCKET_LABEL = {
    "HAS_DOCS_FAILS": "Fix Now",
    "NO_DOCS_IN_SCOPE": "Create Docs",
    "OUT_OF_SCOPE": "Ignored",
    "NOISE": "Ignored",
    "UNKNOWN": "⚠ Judge Failed",
}


def _cell(text: str, max_len: int = 80) -> str:
    """Truncate and strip newlines for a table cell."""
    text = str(text or "").replace("\n", " ").replace("|", "/").strip()
    return text[:max_len] + "…" if len(text) > max_len else text


class ReportGenerator:
    """Generate a single-table supervisor report from pre-computed verdicts."""

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
        logger.info(f"Generating report ({len(gaps)} gaps)...")

        classifications = classifications or {}
        judge_verdicts = judge_verdicts or {}

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        rows = []  # (gap, bucket, verdict)

        for gap in gaps:
            gap_key = f"{gap.module}/{gap.intent}"
            verdict = judge_verdicts.get(gap_key) or {}
            if verdict:
                bucket = verdict.get("bucket", "")
            else:
                cat = classifications.get(gap_key, {}).get("category", "")
                if cat in (OUT_OF_SCOPE_GENERAL, NOISE, "OUT_OF_SCOPE_PRICING",
                           "OUT_OF_SCOPE_ACCOUNT_SUPPORT"):
                    bucket = "OUT_OF_SCOPE"
                else:
                    bucket = "HAS_DOCS_FAILS"
            rows.append((gap, bucket, verdict))

        # Sort: Fix Now first, then Create Docs by failure count, then Ignored, then Unknown last
        bucket_order = {"HAS_DOCS_FAILS": 0, "NO_DOCS_IN_SCOPE": 1, "OUT_OF_SCOPE": 2, "NOISE": 2, "UNKNOWN": 3}
        rows.sort(key=lambda r: (bucket_order.get(r[1], 9), -r[0].failure_count))

        fix_now_count   = sum(1 for _, b, _ in rows if b == "HAS_DOCS_FAILS")
        create_count    = sum(1 for _, b, _ in rows if b == "NO_DOCS_IN_SCOPE")
        ignored_count   = sum(1 for _, b, _ in rows if b in ("OUT_OF_SCOPE", "NOISE"))
        unknown_count   = sum(1 for _, b, _ in rows if b == "UNKNOWN")

        lines = [
            f"# KB Supervisor Report — {timestamp}",
            "",
            "## Summary",
            f"| | Count |",
            f"|---|---|",
            f"| Gaps analyzed | {len(gaps)} |",
            f"| Fix Now (keyword / routing fix in code) | {fix_now_count} |",
            f"| Create Docs (missing KB coverage) | {create_count} |",
            f"| Ignored (out of scope / noise) | {ignored_count} |",
            *(
                [f"| ⚠ Judge failed (worker error / timeout) | {unknown_count} |"]
                if unknown_count else []
            ),
            "",
            "---",
            "",
            "## Gaps",
            "",
            "| # | Gap | Failures | Bucket | Priority | Recommendation | Top failing query |",
            "|---|---|---|---|---|---|---|",
        ]

        for i, (gap, bucket, verdict) in enumerate(rows, 1):
            label = _BUCKET_LABEL.get(bucket, bucket)
            priority = (verdict.get("doc_priority") or "—").upper()

            if bucket == "HAS_DOCS_FAILS":
                keywords = verdict.get("keywords_to_add") or []
                matching_doc = verdict.get("matching_doc") or "?"
                if keywords:
                    recommendation = f"Add keywords to kb_answer.py: {', '.join(f'`{k}`' for k in keywords[:3])}"
                else:
                    recommendation = f"Investigate retrieval for `{matching_doc}`"

            elif bucket == "NO_DOCS_IN_SCOPE":
                doc_path = verdict.get("doc_to_create") or f"kb/{gap.module.lower()}/{gap.intent.lower()}.md"
                recommendation = f"Create `{doc_path}`"

            elif bucket == "UNKNOWN":
                recommendation = _cell(verdict.get("reasoning") or "worker error / timeout — rerun to retry", 80)
                priority = "—"

            else:
                reason = (verdict.get("reason_ignored") or verdict.get("reasoning")
                          or classifications.get(f"{gap.module}/{gap.intent}", {}).get("category", bucket))
                recommendation = _cell(reason, 60)
                priority = "—"

            top_query = _cell((gap.failure_examples or ["?"])[0], 70)

            lines.append(
                f"| {i} | {gap.module} / {gap.intent} | {gap.failure_count} "
                f"({gap.answer_rate:.0%}) | {label} | {priority} "
                f"| {_cell(recommendation, 80)} | {top_query} |"
            )

        lines += ["", "---", ""]

        # Detail section — one block per actionable gap, no outlines
        actionable = [(i+1, g, b, v) for i, (g, b, v) in enumerate(rows)
                      if b in ("HAS_DOCS_FAILS", "NO_DOCS_IN_SCOPE")]
        if actionable:
            lines += ["## Detail — Actionable Gaps", ""]
            for idx, gap, bucket, verdict in actionable:
                label = _BUCKET_LABEL[bucket]
                lines.append(f"### #{idx} {gap.module} / {gap.intent} — {label}")
                lines.append("")

                if bucket == "HAS_DOCS_FAILS":
                    lines.append(f"**Matching doc:** `{verdict.get('matching_doc') or '?'}`")
                    lines.append(f"**Root cause:** {verdict.get('root_cause') or verdict.get('reasoning') or '?'}")
                    keywords = verdict.get("keywords_to_add") or []
                    if keywords:
                        lines.append(f"**Keywords to add:** {', '.join(f'`{k}`' for k in keywords)}")
                else:
                    doc_path = verdict.get("doc_to_create") or f"kb/{gap.module.lower()}/{gap.intent.lower()}.md"
                    lines.append(f"**Create:** `{doc_path}`")
                    lines.append(f"**Why missing:** {verdict.get('reasoning') or '?'}")

                lines.append("")
                lines.append("**Failing queries:**")
                for q in (gap.failure_examples or [])[:5]:
                    lines.append(f'- "{_cell(q, 120)}"')
                lines.append("")

        report = "\n".join(lines)

        # Write
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        if output_path is None:
            _REPO_ROOT = Path(__file__).resolve().parents[3]
            output_path = _REPO_ROOT / "local" / "reports" / f"supervisor_{ts}.md"
        elif output_path.name == "supervisor_.md" or not output_path.stem.replace("supervisor_", ""):
            output_path = output_path.parent / f"supervisor_{ts}.md"

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(report, encoding="utf-8")
            logger.info(f"Report written to {output_path}")
        except IOError as e:
            logger.error(f"Failed to write report: {e}")

        return report
