"""Report generator — supervisor report from full action-taxonomy verdicts."""

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .trace_analyzer import Gap
from .qwen_interface import QwenInterface
from .gap_classifier import OUT_OF_SCOPE_GENERAL, NOISE

logger = logging.getLogger(__name__)

_BUCKET_LABEL = {
    # Legacy / pre-classified buckets — kept for backward compatibility
    "HAS_DOCS_FAILS": "Fix Now",
    "NO_DOCS_IN_SCOPE": "Create Docs",
    "LANGUAGE_COVERAGE_GAP": "Add Language",
    "OUT_OF_SCOPE": "Ignored",
    "NOISE": "Ignored",
    "UNKNOWN": "⚠ Judge Failed",
    # New taxonomy buckets
    "NEEDS_BOOST": "Raise Boost",
    "NEW_CONCEPT_NEEDED": "New Concept",
    "GUARDRAIL_FALSE_POSITIVE": "Fix Guardrail",
    "IMPROVE_TELEMETRY": "Add Telemetry",
    "MARK_RESOLVED": "Already Fixed",
}

# Map action_type (from judge verdict) → display bucket string
_ACTION_TYPE_TO_BUCKET = {
    "ADD_ALIAS": "Fix Now",
    "ADD_KEYWORD": "Fix Now",
    "RAISE_SOURCE_BOOST": "Raise Boost",
    "NEW_CONCEPT": "New Concept",
    "ADD_LANGUAGE_MAPPING": "Add Language",
    "CREATE_DOC": "Create Docs",
    "EXPAND_DOC_SECTION": "Create Docs",
    "ADJUST_GUARDRAIL": "Fix Guardrail",
    "IMPROVE_TELEMETRY": "Add Telemetry",
    "MARK_RESOLVED": "Already Fixed",
    "INSUFFICIENT_DATA": "⚠ Insufficient Data",
}

# Sort order for display buckets
_BUCKET_SORT_ORDER = {
    "Fix Now": 0,
    "Raise Boost": 1,
    "New Concept": 2,
    "Add Language": 3,
    "Fix Guardrail": 4,
    "Add Telemetry": 5,
    "Create Docs": 6,
    "Already Fixed": 7,
    "Ignored": 8,
    "⚠ Insufficient Data": 9,
    "⚠ Judge Failed": 10,
}


def _cell(text: str, max_len: int = 80) -> str:
    """Truncate and strip newlines for a table cell."""
    text = str(text or "").replace("\n", " ").replace("|", "/").strip()
    return text[:max_len] + "…" if len(text) > max_len else text


def _display_bucket(bucket: str, verdict: Dict[str, Any]) -> str:
    """Return the display-friendly bucket label for a row."""
    # If verdict contains an action_type from the new taxonomy, use that mapping
    action_type = verdict.get("action_type") if verdict else None
    if action_type and action_type in _ACTION_TYPE_TO_BUCKET:
        return _ACTION_TYPE_TO_BUCKET[action_type]
    # Fall back to legacy bucket label
    return _BUCKET_LABEL.get(bucket, bucket)


def _recommendation_for(bucket: str, verdict: Dict[str, Any], gap: "Gap",
                         classifications: Dict[str, Any]) -> str:
    """Build recommendation text for the gap table."""
    action_type = verdict.get("action_type") if verdict else None

    if action_type == "ADD_ALIAS":
        term = verdict.get("term") or verdict.get("alias") or "?"
        concept = verdict.get("concept_target") or "?"
        return f"Add alias `{term}` to concept `{concept}`"

    if action_type == "ADD_KEYWORD":
        keywords = verdict.get("keywords_to_add") or []
        concept = verdict.get("concept_target") or "?"
        if keywords:
            kw_str = ", ".join(f"`{k}`" for k in keywords[:3])
            return f"Add keyword {kw_str} to concept `{concept}`"
        return f"Add keyword to concept `{concept}`"

    if action_type == "RAISE_SOURCE_BOOST":
        doc = verdict.get("target_doc") or verdict.get("matching_doc") or "?"
        concept = verdict.get("concept_id") or verdict.get("concept_target") or "?"
        current = verdict.get("current_boost", "?")
        recommended = verdict.get("recommended_boost", "?")
        return f"Raise boost: `{doc}` in concept `{concept}` from {current} → {recommended}"

    if action_type == "NEW_CONCEPT":
        name = verdict.get("concept_name") or verdict.get("concept_target") or "?"
        doc = verdict.get("target_doc") or verdict.get("matching_doc") or "?"
        return f"Create concept `{name}` with source_boosts for `{doc}`"

    if action_type == "ADD_LANGUAGE_MAPPING":
        mappings = verdict.get("language_mappings") or []
        if mappings:
            sample = mappings[0]
            return f"Add to _MULTILINGUAL_TERMS: `{sample.get('term','?')}` → `{sample.get('english','?')}`"
        return "Extend _MULTILINGUAL_TERMS in skill/kb_answer.py"

    if action_type == "IMPROVE_TELEMETRY":
        field = verdict.get("missing_field") or verdict.get("field") or "?"
        reason = verdict.get("reason") or ""
        return f"Add `{field}` to kb_answer.py telemetry: {reason}"[:80]

    if action_type == "MARK_RESOLVED":
        return "Already resolved — add to deployed_fixes.json"

    if action_type == "ADJUST_GUARDRAIL":
        query_type = verdict.get("query_type") or verdict.get("pattern") or "?"
        return f"Fix guardrail pattern blocking: `{query_type}`"

    if action_type == "INSUFFICIENT_DATA":
        return "Fewer than 2 traces — no pattern to diagnose"

    if action_type in ("CREATE_DOC", "EXPAND_DOC_SECTION"):
        doc_path = verdict.get("doc_to_create") or f"kb/{gap.module.lower()}/{gap.intent.lower()}.md"
        if action_type == "EXPAND_DOC_SECTION":
            section = verdict.get("section") or "?"
            return f"Expand section `{section}` in `{doc_path}`"
        return f"Create `{doc_path}`"

    # Legacy fallback paths
    if bucket == "HAS_DOCS_FAILS":
        keywords = verdict.get("keywords_to_add") or []
        matching_doc = verdict.get("matching_doc") or "?"
        if keywords:
            return f"Add keywords to kb_answer.py: {', '.join(f'`{k}`' for k in keywords[:3])}"
        return f"Investigate retrieval for `{matching_doc}`"

    if bucket == "LANGUAGE_COVERAGE_GAP":
        mappings = verdict.get("language_mappings") or []
        if mappings:
            sample = mappings[0]
            return f"Add to _MULTILINGUAL_TERMS: `{sample.get('term','?')}` → `{sample.get('english','?')}`"
        return "Extend _MULTILINGUAL_TERMS in skill/kb_answer.py"

    if bucket == "NO_DOCS_IN_SCOPE":
        doc_path = verdict.get("doc_to_create") or f"kb/{gap.module.lower()}/{gap.intent.lower()}.md"
        return f"Create `{doc_path}`"

    if bucket == "UNKNOWN":
        return _cell(verdict.get("reasoning") or "worker error / timeout — rerun to retry", 80)

    reason = (verdict.get("reason_ignored") or verdict.get("reasoning")
              or classifications.get(f"{gap.module}/{gap.intent}", {}).get("category", bucket))
    return _cell(reason, 60)


class ReportGenerator:
    """Generate a supervisor report from pre-computed verdicts (full action taxonomy)."""

    def __init__(self, qwen: QwenInterface) -> None:
        self.qwen = qwen

    def generate_report(
        self,
        gaps: List[Gap],
        traces: List[Dict[str, Any]],
        output_path: Path,
        classifications: Dict[str, Any] = None,
        judge_verdicts: Dict[str, Any] = None,
        trace_window_days: int = 0,
    ) -> str:
        logger.info(f"Generating report ({len(gaps)} gaps)...")

        classifications = classifications or {}
        judge_verdicts = judge_verdicts or {}

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        window_label = f"last {trace_window_days} days" if trace_window_days > 0 else "all time"

        rows = []  # (gap, legacy_bucket, verdict, display_bucket)

        for gap in gaps:
            gap_key = f"{gap.module}/{gap.intent}"
            if gap.pre_classified_bucket:
                bucket = gap.pre_classified_bucket
                verdict = {
                    "bucket": bucket,
                    "reason_ignored": gap.intent.replace("_", " ") + " — pre-classified by trace analyzer",
                }
            else:
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

            display = _display_bucket(bucket, verdict)
            rows.append((gap, bucket, verdict, display))

        # Sort by display bucket order, then by failure count descending
        rows.sort(key=lambda r: (_BUCKET_SORT_ORDER.get(r[3], 99), -r[0].failure_count))

        # Count per display bucket
        from collections import Counter
        display_counts: Counter = Counter(r[3] for r in rows)

        # Build summary rows — only show buckets with count > 0
        summary_rows = [
            ("Gaps analyzed", len(gaps)),
            ("Fix Now (alias / keyword fix in code)", display_counts.get("Fix Now", 0)),
            ("Raise Boost (source_boosts adjustment)", display_counts.get("Raise Boost", 0)),
            ("New Concept (CONCEPT_REGISTRY addition)", display_counts.get("New Concept", 0)),
            ("Add Language (extend _MULTILINGUAL_TERMS)", display_counts.get("Add Language", 0)),
            ("Fix Guardrail", display_counts.get("Fix Guardrail", 0)),
            ("Add Telemetry (improve trace signal)", display_counts.get("Add Telemetry", 0)),
            ("Create Docs (missing KB coverage)", display_counts.get("Create Docs", 0)),
            ("Already Fixed (stale traces)", display_counts.get("Already Fixed", 0)),
            ("Ignored (out of scope / noise)", display_counts.get("Ignored", 0)),
            ("⚠ Insufficient Data", display_counts.get("⚠ Insufficient Data", 0)),
            ("⚠ Judge failed (worker error / timeout)", display_counts.get("⚠ Judge Failed", 0)),
        ]

        lines = [
            f"# KB Supervisor Report — {timestamp}  |  Traces: {window_label}  |  N={len(traces)}",
            "",
            "## Summary",
            "| | Count |",
            "|---|---|",
        ]

        for label, count in summary_rows:
            # Always show "Gaps analyzed"; for others only show if count > 0
            if label == "Gaps analyzed" or count > 0:
                lines.append(f"| {label} | {count} |")

        lines += [
            "",
            "---",
            "",
            "## Gaps",
            "",
            "| # | Gap | Failures | Bucket | Priority | Recommendation | Top failing query |",
            "|---|---|---|---|---|---|---|",
        ]

        for i, (gap, bucket, verdict, display) in enumerate(rows, 1):
            priority = (verdict.get("doc_priority") or "—").upper()
            # Priority not meaningful for telemetry/resolved/ignored buckets
            if display in ("Add Telemetry", "Already Fixed", "Ignored", "⚠ Insufficient Data", "⚠ Judge Failed"):
                priority = "—"

            recommendation = _recommendation_for(bucket, verdict, gap, classifications)
            if bucket == "UNKNOWN" and not verdict.get("action_type"):
                priority = "—"

            top_query = _cell((gap.failure_examples or ["?"])[0], 70)

            lines.append(
                f"| {i} | {gap.module} / {gap.intent} | {gap.failure_count} "
                f"({gap.answer_rate:.0%}) | {display} | {priority} "
                f"| {_cell(recommendation, 80)} | {top_query} |"
            )

        lines += ["", "---", ""]

        # Detail section — all actionable display buckets
        actionable_displays = {
            "Fix Now", "Raise Boost", "New Concept", "Add Language",
            "Fix Guardrail", "Add Telemetry", "Create Docs",
        }
        actionable = [
            (i + 1, g, b, v, d)
            for i, (g, b, v, d) in enumerate(rows)
            if d in actionable_displays
        ]

        if actionable:
            lines += ["## Detail — Actionable Gaps", ""]
            for idx, gap, bucket, verdict, display in actionable:
                lines.append(f"### #{idx} {gap.module} / {gap.intent} — {display}")
                lines.append("")

                action_type = verdict.get("action_type") if verdict else None

                if action_type == "RAISE_SOURCE_BOOST":
                    concept = verdict.get("concept_id") or verdict.get("concept_target") or "?"
                    current = verdict.get("current_boost", "not set")
                    recommended = verdict.get("recommended_boost", "?")
                    target_doc = verdict.get("target_doc") or verdict.get("matching_doc") or "?"
                    reason = verdict.get("reasoning") or verdict.get("reason") or "?"
                    lines.append(f"**Concept:** `{concept}`")
                    lines.append(f"**Current boost:** {current}")
                    lines.append(f"**Recommended boost:** {recommended}")
                    lines.append(f"**Target doc:** `{target_doc}`")
                    lines.append(f"**Reason:** {reason}")

                elif action_type == "IMPROVE_TELEMETRY":
                    field = verdict.get("missing_field") or verdict.get("field") or "?"
                    why = verdict.get("why_needed") or verdict.get("reason") or "?"
                    fix = verdict.get("suggested_fix") or "?"
                    impact = verdict.get("impact") or "?"
                    lines.append(f"**Missing field:** `{field}`")
                    lines.append(f"**Why needed:** {why}")
                    lines.append(f"**Suggested fix:** {fix}")
                    lines.append(f"**Impact:** {impact}")

                elif action_type == "MARK_RESOLVED":
                    lines.append("**Status:** Stale trace — live skill now answers this query")
                    lines.append("**Action:** Add to deployed_fixes.json and remove from active monitoring")

                elif action_type == "NEW_CONCEPT":
                    name = verdict.get("concept_name") or verdict.get("concept_target") or "?"
                    source_boosts = verdict.get("source_boosts") or {}
                    aliases = verdict.get("suggested_aliases") or []
                    rationale = verdict.get("rationale") or verdict.get("reasoning") or "?"
                    lines.append(f"**Concept to create:** `{name}`")
                    if source_boosts:
                        lines.append(f"**Source boosts:** `{source_boosts}`")
                    if aliases:
                        lines.append(f"**Suggested aliases:** {', '.join(f'`{a}`' for a in aliases)}")
                    lines.append(f"**Rationale:** {rationale}")

                elif action_type == "ADJUST_GUARDRAIL":
                    query_type = verdict.get("query_type") or verdict.get("pattern") or "?"
                    reasoning = verdict.get("reasoning") or "?"
                    lines.append(f"**Pattern blocking:** `{query_type}`")
                    lines.append(f"**Root cause:** {reasoning}")

                elif action_type in ("ADD_ALIAS", "ADD_KEYWORD") or bucket == "HAS_DOCS_FAILS":
                    lines.append(f"**Matching doc:** `{verdict.get('matching_doc') or '?'}`")
                    lines.append(f"**Root cause:** {verdict.get('root_cause') or verdict.get('reasoning') or '?'}")
                    concept = verdict.get("concept_target")
                    if concept:
                        lines.append(f"**Concept target:** `{concept}`")
                    doc_evidence = verdict.get("doc_evidence")
                    if doc_evidence:
                        lines.append(f"**Doc evidence:** \"{_cell(doc_evidence, 200)}\"")
                    keywords = verdict.get("keywords_to_add") or []
                    if keywords:
                        lines.append(f"**Keywords to add:** {', '.join(f'`{k}`' for k in keywords)}")
                    alias = verdict.get("term") or verdict.get("alias")
                    if alias:
                        lines.append(f"**Alias to add:** `{alias}`")

                elif action_type == "ADD_LANGUAGE_MAPPING" or bucket == "LANGUAGE_COVERAGE_GAP":
                    lines.append(f"**Matching doc:** `{verdict.get('matching_doc') or '?'}`")
                    lines.append("**Root cause:** language_gap — foreign phrase not in _MULTILINGUAL_TERMS")
                    concept = verdict.get("concept_target")
                    if concept:
                        lines.append(f"**Concept target:** `{concept}`")
                    mappings = verdict.get("language_mappings") or []
                    if mappings:
                        lines.append("**Mappings to add to `_MULTILINGUAL_TERMS` in `skill/kb_answer.py`:**")
                        for m in mappings:
                            lang = m.get("language", "?")
                            lines.append(f'  - `"{m.get("term","?")}"` → `"{m.get("english","?")}"` ({lang})')
                    else:
                        lines.append("**Mappings to add:** (judge did not specify — investigate manually)")

                elif action_type in ("CREATE_DOC", "EXPAND_DOC_SECTION") or bucket == "NO_DOCS_IN_SCOPE":
                    doc_path = verdict.get("doc_to_create") or f"kb/{gap.module.lower()}/{gap.intent.lower()}.md"
                    lines.append(f"**Create:** `{doc_path}`")
                    if action_type == "EXPAND_DOC_SECTION":
                        section = verdict.get("section") or "?"
                        lines.append(f"**Section to expand:** `{section}`")
                    lines.append(f"**Why missing:** {verdict.get('reasoning') or '?'}")

                else:
                    # Fallback for any unhandled action_type
                    lines.append(f"**Root cause:** {verdict.get('reasoning') or verdict.get('reason') or '?'}")

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
