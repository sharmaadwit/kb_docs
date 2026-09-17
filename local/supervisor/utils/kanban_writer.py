"""
KanbanWriter - writes KB gap tasks to the Hermes kanban board via the
kb-supervisor CLI (subprocess).

Actionable categories (create a task):
  CODE_GAP_ALIAS_CANDIDATE, CODE_GAP_MISSING_CONCEPT, CODE_GAP_NEEDS_INVESTIGATION

Skipped categories (no task):
  ALREADY_FIXED, OUT_OF_SCOPE_PRICING, OUT_OF_SCOPE_ACCOUNT_SUPPORT, CONTENT_GAP

MIXED gaps produce one sub-task per actionable sub-category found in
classification["evidence"]["category_breakdown"].
"""

import json
import logging
import os
import subprocess
from typing import Any, Dict, List, Optional

from local.supervisor.utils.gap_classifier import (
    ALREADY_FIXED,
    CODE_GAP_ALIAS_CANDIDATE,
    CODE_GAP_MISSING_CONCEPT,
    CODE_GAP_NEEDS_INVESTIGATION,
    CONTENT_GAP,
    OUT_OF_SCOPE_ACCOUNT_SUPPORT,
    OUT_OF_SCOPE_PRICING,
)
from local.supervisor.utils.trace_analyzer import Gap

logger = logging.getLogger(__name__)

# Categories for which we DO create a kanban task.
ACTIONABLE_CATEGORIES = {
    CODE_GAP_ALIAS_CANDIDATE,
    CODE_GAP_MISSING_CONCEPT,
    CODE_GAP_NEEDS_INVESTIGATION,
}

# Human-readable short tag used in task titles.
_CATEGORY_TAG = {
    CODE_GAP_ALIAS_CANDIDATE: "alias",
    CODE_GAP_MISSING_CONCEPT: "concept",
    CODE_GAP_NEEDS_INVESTIGATION: "invest",
}

# kb-supervisor binary location (added to PATH if not already present).
_KB_SUPERVISOR_BIN_DIR = os.path.expanduser("~/.local/bin")


def _make_env() -> Dict[str, str]:
    """Return an env dict that includes the kb-supervisor bin directory."""
    env = os.environ.copy()
    path = env.get("PATH", "")
    if _KB_SUPERVISOR_BIN_DIR not in path.split(os.pathsep):
        env["PATH"] = f"{_KB_SUPERVISOR_BIN_DIR}{os.pathsep}{path}"
    return env


class KanbanWriter:
    """Writes KB gap tasks to the Hermes kanban board via kb-supervisor CLI."""

    def __init__(
        self,
        board: str = "kb-gaps",
        assignee: str = "kb-supervisor",
        working_dir: str = "/Users/adwit.sharma/kb_docs",
    ) -> None:
        self.board = board
        self.assignee = assignee
        self.working_dir = working_dir
        self._env = _make_env()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def write_gap_tasks(
        self,
        gap_index: int,
        gap: Gap,
        classification: Dict[str, Any],
    ) -> List[tuple]:
        """Create kanban tasks for actionable categories in *classification*.

        Args:
            gap_index: 1-based rank (used in task titles, e.g. "Gap #1").
            gap: Gap object from TraceAnalyzer.
            classification: Dict returned by GapClassifier.classify_gap().

        Returns:
            List of (task_id, sub_category) tuples (empty if nothing actionable).
        """
        category = classification.get("category", "")
        created_pairs: List[tuple] = []

        if category == "MIXED":
            breakdown: Dict[str, List[str]] = (
                classification.get("evidence", {}).get("category_breakdown", {})
            )
            for sub_category, queries in breakdown.items():
                if sub_category not in ACTIONABLE_CATEGORIES:
                    continue
                per_query = [
                    r
                    for r in classification.get("per_query_results", [])
                    if r.get("category") == sub_category
                ]
                task_id = self._create_gap_task(
                    gap_index=gap_index,
                    gap=gap,
                    category=sub_category,
                    failure_examples=queries,
                    per_query_results=per_query,
                    confidence=classification.get("confidence", "low"),
                )
                if task_id:
                    created_pairs.append((task_id, sub_category))

        elif category in ACTIONABLE_CATEGORIES:
            task_id = self._create_gap_task(
                gap_index=gap_index,
                gap=gap,
                category=category,
                failure_examples=gap.failure_examples,
                per_query_results=classification.get("per_query_results", []),
                confidence=classification.get("confidence", "high"),
            )
            if task_id:
                created_pairs.append((task_id, category))

        else:
            logger.debug(
                "Skipping kanban task for gap #%d (%s/%s): category=%s",
                gap_index, gap.module, gap.intent, category,
            )

        return created_pairs

    def build_finding(
        self,
        sub_category: str,
        gap: Gap,
        classification: Dict[str, Any],
        judge_verdict: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Build the enrichment finding JSON for a kanban task comment.

        This is what ProposalsWriter.load_tasks() reads to tier proposals.

        Args:
            sub_category: The category this specific task was created for.
            gap: Gap object.
            classification: Full GapClassifier result for this gap.
            judge_verdict: HermesJudge verdict (only for CODE_GAP_NEEDS_INVESTIGATION).

        Returns:
            Dict ready for JSON serialisation, or None on error.
        """
        confidence_str = classification.get("confidence", "low")

        if sub_category == CODE_GAP_ALIAS_CANDIDATE:
            # Collect near-miss concepts and failing queries as proposed aliases
            proposed_aliases: List[str] = []
            near_miss_names: List[str] = []
            reasoning_parts: List[str] = []
            kb_evidence_parts: List[str] = []

            for r in classification.get("per_query_results", []):
                if r.get("category") != CODE_GAP_ALIAS_CANDIDATE:
                    continue
                query = r.get("query", "")
                if query and query not in proposed_aliases:
                    proposed_aliases.append(query)
                near_misses = r.get("evidence", {}).get("near_miss_concepts", [])
                for nm in near_misses:
                    cid = nm.get("concept_id", "")
                    keywords = nm.get("matched_keywords", [])
                    aliases_sample = nm.get("existing_aliases_sample", [])
                    if cid and cid not in near_miss_names:
                        near_miss_names.append(cid)
                    reasoning_parts.append(
                        f"Query '{query[:80]}' matched keyword(s) {keywords} "
                        f"on concept '{cid}' but no alias covers it"
                    )
                    kb_evidence_parts.append(
                        f"{cid}: matched_keywords={keywords}, "
                        f"existing_aliases={aliases_sample[:3]}"
                    )

            return {
                "finding_type": "alias_candidate",
                "confidence": confidence_str,
                "ready_for_code_change": confidence_str == "high",
                "proposed_aliases": proposed_aliases[:10],
                "near_miss_concepts": near_miss_names,
                "reasoning": "; ".join(reasoning_parts) or "Near-miss concept found",
                "kb_evidence": "; ".join(kb_evidence_parts),
                "failure_examples": gap.failure_examples[:5],
                "gap_module": gap.module,
                    "gap_trace_module": getattr(gap, "trace_module", gap.module),
                    "gap_module_mismatch": getattr(gap, "module_mismatch", False),
                    "gap_mismatch_detail": getattr(gap, "mismatch_detail", ""),
                    "no_concept_match_count": getattr(gap, "no_concept_match_count", 0),
                "gap_intent": gap.intent,
                "failure_count": gap.failure_count,
            }

        elif sub_category == CODE_GAP_MISSING_CONCEPT:
            kb_files: List[str] = []
            reasoning_parts = []
            for r in classification.get("per_query_results", []):
                if r.get("category") != CODE_GAP_MISSING_CONCEPT:
                    continue
                evidence = r.get("evidence", {})
                content_check = evidence.get("content_check", {})
                for m in content_check.get("matches", []):
                    src = m.get("source", "")
                    cov = int(m.get("coverage", 0) * 100)
                    if src and src not in kb_files:
                        kb_files.append(src)
                    reasoning_parts.append(f"{src} ({cov}% coverage)")

            return {
                "finding_type": "missing_concept",
                "confidence": confidence_str,
                "ready_for_code_change": False,
                "reasoning": (
                    "KB files exist but no CONCEPT_REGISTRY entry claims them: "
                    + "; ".join(reasoning_parts)
                ),
                "kb_evidence": "; ".join(kb_files[:5]),
                "failure_examples": gap.failure_examples[:5],
                "gap_module": gap.module,
                    "gap_trace_module": getattr(gap, "trace_module", gap.module),
                    "gap_module_mismatch": getattr(gap, "module_mismatch", False),
                    "gap_mismatch_detail": getattr(gap, "mismatch_detail", ""),
                    "no_concept_match_count": getattr(gap, "no_concept_match_count", 0),
                "gap_intent": gap.intent,
                "failure_count": gap.failure_count,
            }

        elif sub_category == CODE_GAP_NEEDS_INVESTIGATION:
            samples = gap.failure_examples[:5]
            if judge_verdict and not judge_verdict.get("degraded"):
                conf_float = judge_verdict.get("confidence", 0.0)
                conf_str = "high" if conf_float >= 0.8 else ("medium" if conf_float >= 0.5 else "low")

                # Judge explicitly confirmed IDK is correct — route to ⚫ IDK section
                if judge_verdict.get("finding_type") == "idk_correct":
                    return {
                        "finding_type": "idk_correct",
                        "confidence": conf_str,
                        "ready_for_code_change": False,
                        "reasoning": judge_verdict.get("reasoning", ""),
                        "suggested_next_step": "No action needed.",
                        "failure_examples": samples,
                        "gap_module": gap.module,
                        "gap_trace_module": getattr(gap, "trace_module", gap.module),
                        "gap_intent": gap.intent,
                        "failure_count": gap.failure_count,
                    }

                judge_finding_type = judge_verdict.get("finding_type", "needs_investigation")

                # out_of_scope: judge says IDK is correct for this gap too
                if judge_finding_type == "out_of_scope":
                    return {
                        "finding_type": "idk_correct",
                        "confidence": conf_str,
                        "ready_for_code_change": False,
                        "reasoning": judge_verdict.get("reasoning", ""),
                        "suggested_next_step": "No action needed.",
                        "failure_examples": samples,
                        "gap_module": gap.module,
                        "gap_trace_module": getattr(gap, "trace_module", gap.module),
                        "gap_intent": gap.intent,
                        "failure_count": gap.failure_count,
                    }

                # missing_concept: pass through all structured judge fields
                if judge_finding_type == "missing_concept":
                    finding = {
                        "finding_type": "missing_concept",
                        "confidence": conf_str,
                        "ready_for_code_change": judge_verdict.get("ready_for_code_change", False),
                        "proposed_concept_id": judge_verdict.get("proposed_concept_id") or judge_verdict.get("concept_id"),
                        "proposed_module": judge_verdict.get("proposed_module"),
                        "proposed_aliases": judge_verdict.get("proposed_aliases", []),
                        "reasoning": judge_verdict.get("reasoning", ""),
                        "suggested_next_step": judge_verdict.get("suggested_next_step", ""),
                        "failure_examples": samples,
                        "gap_module": gap.module,
                        "gap_trace_module": getattr(gap, "trace_module", gap.module),
                        "gap_intent": gap.intent,
                        "failure_count": gap.failure_count,
                        "kb_doc_needed": judge_verdict.get("kb_doc_needed", True),
                    }
                    if judge_verdict.get("additional_concepts"):
                        finding["additional_concepts"] = judge_verdict["additional_concepts"]
                    return finding

                root_cause = judge_verdict.get("root_cause", "unknown")
                actionable = root_cause in ("wrong_source_doc", "missing_boost")
                return {
                    "finding_type": judge_finding_type,
                    "confidence": conf_str,
                    "ready_for_code_change": actionable,
                    "root_cause": root_cause,
                    "reasoning": judge_verdict.get("reasoning", ""),
                    "suggested_next_step": judge_verdict.get("suggested_next_step", ""),
                    "proposed_boost_changes": judge_verdict.get("proposed_boost_changes", {}),
                    "failure_examples": samples,
                    "gap_module": gap.module,
                    "gap_trace_module": getattr(gap, "trace_module", gap.module),
                    "gap_module_mismatch": getattr(gap, "module_mismatch", False),
                    "gap_mismatch_detail": getattr(gap, "mismatch_detail", ""),
                    "no_concept_match_count": getattr(gap, "no_concept_match_count", 0),
                    "gap_intent": gap.intent,
                    "failure_count": gap.failure_count,
                }
            else:
                # Hermes unavailable — post degraded finding so task is visible as RED
                return {
                    "finding_type": "needs_investigation",
                    "confidence": "low",
                    "ready_for_code_change": False,
                    "root_cause": "unknown",
                    "reasoning": (
                        judge_verdict.get("reasoning", "Hermes judge unavailable")
                        if judge_verdict else "Hermes judge not called for this task"
                    )[:400],
                    "failure_examples": samples,
                    "gap_module": gap.module,
                    "gap_trace_module": getattr(gap, "trace_module", gap.module),
                    "gap_module_mismatch": getattr(gap, "module_mismatch", False),
                    "gap_mismatch_detail": getattr(gap, "mismatch_detail", ""),
                    "no_concept_match_count": getattr(gap, "no_concept_match_count", 0),
                    "gap_intent": gap.intent,
                    "failure_count": gap.failure_count,
                }

        return None

    def clear_board(self) -> int:
        """Archive all existing tasks on the board before a fresh run.

        Returns:
            Number of tasks archived.
        """
        env = _make_env()
        try:
            result = subprocess.run(
                ["kb-supervisor", "kanban", "--board", self.board, "list", "--json"],
                capture_output=True, text=True, env=env, timeout=30,
                cwd=self.working_dir,
            )
            if result.returncode != 0:
                logger.warning("clear_board: list failed: %s", result.stderr[:200])
                return 0
            data = json.loads(result.stdout)
            tasks = data if isinstance(data, list) else data.get("tasks", [])
        except Exception as exc:
            logger.warning("clear_board: failed to list tasks: %s", exc)
            return 0

        count = 0
        for t in tasks:
            task_id = t.get("id")
            if not task_id:
                continue
            ok = self._run(["kb-supervisor", "kanban", "--board", self.board, "archive", task_id])
            if ok is not None:
                count += 1
            else:
                logger.warning("clear_board: failed to archive %s", task_id)

        logger.info("clear_board: archived %d task(s)", count)
        return count

    def post_hermes_finding(self, task_id: str, finding: Dict[str, Any]) -> bool:
        """Post a Hermes worker finding as a comment on *task_id*.

        Args:
            task_id: Kanban task ID (e.g. "t_5b1891de").
            finding: Arbitrary dict; will be JSON-serialised and posted.

        Returns:
            True on success, False on any error.
        """
        try:
            body = json.dumps(finding, ensure_ascii=False)
        except (TypeError, ValueError) as exc:
            logger.warning("post_hermes_finding: JSON serialise failed: %s", exc)
            return False

        cmd = [
            "kb-supervisor", "kanban", "comment",
            task_id, body,
            "--author", self.assignee,
        ]
        return self._run(cmd) is not None

    def archive_task(self, task_id: str) -> bool:
        """Archive *task_id* on the board.

        Returns:
            True on success, False on any error.
        """
        cmd = ["kb-supervisor", "kanban", "archive", task_id]
        return self._run(cmd) is not None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _create_gap_task(
        self,
        gap_index: int,
        gap: Gap,
        category: str,
        failure_examples: List[str],
        per_query_results: List[Dict[str, Any]],
        confidence: str,
    ) -> Optional[str]:
        """Build title + body for one task, then call _create_task."""
        tag = _CATEGORY_TAG.get(category, "invest")
        # Derive a concept identifier from the gap intent (snake_case)
        concept_id = gap.intent.lower().replace(" ", "_").replace("/", "_")
        title = (
            f"[{tag}] {concept_id} — Gap #{gap_index} "
            f"{gap.module}/{gap.intent} ({gap.failure_count} failures)"
        )
        body = self._build_body(
            gap=gap,
            gap_index=gap_index,
            category=category,
            failure_examples=failure_examples,
            per_query_results=per_query_results,
            confidence=confidence,
        )
        return self._create_task(title, body)

    def _build_body(
        self,
        gap: Gap,
        gap_index: int,
        category: str,
        failure_examples: List[str],
        per_query_results: List[Dict[str, Any]],
        confidence: str,
    ) -> str:
        """Compose a Markdown task body with all context Hermes needs."""
        lines: List[str] = []

        # ---- Severity block ----
        lines.append("## Gap Severity")
        lines.append(f"- **Rank**: #{gap_index}")
        lines.append(f"- **Module / Intent**: {gap.module} / {gap.intent}")
        lines.append(f"- **Failures**: {gap.failure_count} of {gap.total_count} queries")
        lines.append(f"- **Answer rate**: {gap.answer_rate * 100:.1f}%")
        lines.append(f"- **Avg confidence**: {gap.avg_confidence:.3f}")
        lines.append(f"- **Classification**: `{category}` (confidence: {confidence})")
        lines.append("")

        # ---- Failing query samples ----
        samples = (failure_examples or [])[:5]
        if samples:
            lines.append("## Failing Query Samples")
            for i, q in enumerate(samples, 1):
                lines.append(f"{i}. {q}")
            lines.append("")

        # ---- Category-specific evidence ----
        lines.append("## Classification Evidence")

        if category == CODE_GAP_ALIAS_CANDIDATE:
            lines += self._alias_evidence_lines(per_query_results)
        elif category == CODE_GAP_MISSING_CONCEPT:
            lines += self._concept_evidence_lines(per_query_results)
        elif category == CODE_GAP_NEEDS_INVESTIGATION:
            lines += self._invest_evidence_lines(per_query_results)

        lines.append("")

        # ---- KB files to inspect ----
        kb_files = self._extract_kb_files(per_query_results)
        if kb_files:
            lines.append("## KB Files to Read")
            for f in kb_files:
                lines.append(f"- `{f}`")
            lines.append("")

        return "\n".join(lines)

    # ---- Evidence formatters ----

    def _alias_evidence_lines(self, per_query_results: List[Dict[str, Any]]) -> List[str]:
        lines: List[str] = []
        for r in per_query_results:
            if r.get("category") != CODE_GAP_ALIAS_CANDIDATE:
                continue
            near_misses = r.get("evidence", {}).get("near_miss_concepts", [])
            if not near_misses:
                continue
            lines.append(f"**Query**: `{r.get('query', '')}`")
            lines.append("Near-miss concepts:")
            for nm in near_misses:
                concept_id = nm.get("concept_id", "?")
                keywords = ", ".join(nm.get("matched_keywords", []))
                aliases_sample = nm.get("existing_aliases_sample", [])
                alias_str = (
                    ", ".join(f"`{a}`" for a in aliases_sample)
                    if aliases_sample
                    else "none"
                )
                lines.append(
                    f"  - `{concept_id}` — matched keywords: [{keywords}] "
                    f"— existing aliases: {alias_str}"
                )
            lines.append("")
        return lines

    def _concept_evidence_lines(self, per_query_results: List[Dict[str, Any]]) -> List[str]:
        lines: List[str] = []
        for r in per_query_results:
            if r.get("category") != CODE_GAP_MISSING_CONCEPT:
                continue
            evidence = r.get("evidence", {})
            content_check = evidence.get("content_check", {})
            lines.append(f"**Query**: `{r.get('query', '')}`")
            reason = evidence.get("reason", "")
            if reason:
                lines.append(f"Reason: {reason}")
            matches = content_check.get("matches", [])
            if matches:
                lines.append("Content matches (source → coverage → terms):")
                for m in matches:
                    terms = ", ".join(m.get("matched_terms", []))
                    lines.append(
                        f"  - `{m.get('source', '?')}` "
                        f"({m.get('coverage', 0)*100:.0f}% coverage) — [{terms}]"
                    )
            checked = content_check.get("checked_terms", [])
            if checked:
                lines.append(f"Checked terms: {', '.join(checked)}")
            lines.append("")
        return lines

    def _invest_evidence_lines(self, per_query_results: List[Dict[str, Any]]) -> List[str]:
        lines: List[str] = []
        for r in per_query_results:
            if r.get("category") != CODE_GAP_NEEDS_INVESTIGATION:
                continue
            evidence = r.get("evidence", {})
            lines.append(f"**Query**: `{r.get('query', '')}`")
            reason = evidence.get("reason", "")
            if reason:
                lines.append(f"Reason: {reason}")
            entities = evidence.get("entities", [])
            if entities:
                lines.append(f"Matched entities: {entities}")
            sources = evidence.get("evidence_sources", [])
            if sources:
                lines.append(f"Evidence sources: {sources}")
            top_score = evidence.get("top_score")
            if top_score is not None:
                lines.append(f"Top score: {top_score}")
            lines.append("")
        return lines

    def _extract_kb_files(self, per_query_results: List[Dict[str, Any]]) -> List[str]:
        """Collect unique KB file paths from evidence_sources and content_check."""
        seen: set = set()
        files: List[str] = []

        def _add(path: str) -> None:
            if path and path not in seen:
                seen.add(path)
                files.append(path)

        for r in per_query_results:
            evidence = r.get("evidence", {})
            # evidence_sources (invest / already_fixed)
            for src in evidence.get("evidence_sources", []):
                if isinstance(src, str):
                    _add(src)
                elif isinstance(src, dict):
                    _add(src.get("source", ""))
            # content_check matches (concept / content_gap)
            content_check = evidence.get("content_check", {})
            for m in content_check.get("matches", []):
                if isinstance(m, dict):
                    _add(m.get("source", ""))

        return files

    # ------------------------------------------------------------------
    # CLI wrappers
    # ------------------------------------------------------------------

    def _create_task(self, title: str, body: str) -> Optional[str]:
        """Call `kb-supervisor kanban create` and return the new task ID."""
        cmd = [
            "kb-supervisor", "kanban", "--board", self.board, "create",
            title,
            "--body", body,
            "--assignee", self.assignee,
            "--json",
        ]
        output = self._run(cmd)
        if output is None:
            return None
        try:
            data = json.loads(output)
            task_id = data.get("id") or data.get("task_id")
            if not task_id:
                logger.warning("_create_task: no 'id' in CLI response: %s", output[:200])
                return None
            logger.info("Created kanban task %s: %s", task_id, title[:60])
            return str(task_id)
        except json.JSONDecodeError as exc:
            logger.warning("_create_task: JSON parse error (%s) for output: %s", exc, output[:200])
            return None

    def _run(self, cmd: List[str]) -> Optional[str]:
        """Execute *cmd* via subprocess.

        Returns:
            stdout string on success (exit 0), None on any failure.
        """
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.working_dir,
                env=self._env,
                timeout=30,
            )
            if result.returncode != 0:
                logger.warning(
                    "kb-supervisor exited %d for cmd %s: %s",
                    result.returncode,
                    cmd[:3],
                    (result.stderr or "").strip()[:300],
                )
                return None
            return result.stdout
        except FileNotFoundError:
            logger.warning(
                "kb-supervisor CLI not found. Ensure %s is on PATH.", _KB_SUPERVISOR_BIN_DIR
            )
            return None
        except subprocess.TimeoutExpired:
            logger.warning("kb-supervisor timed out for cmd: %s", cmd[:3])
            return None
        except OSError as exc:
            logger.warning("kb-supervisor OS error (%s) for cmd: %s", exc, cmd[:3])
            return None
