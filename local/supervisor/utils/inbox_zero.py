"""
inbox_zero.py - InboxZero: Claude reads the kb-gaps kanban board and presents
a one-line decision table for user approval.

Inbox zero format (monospace-aligned):
  #KB-001  [alias]    console_navigation   +4 aliases   HIGH  ✅   → y/n/detail
  #KB-002  [concept]  template_lifecycle   new entry    MED   ✅   → y/n/detail
  #KB-003  [invest]   whatsapp_coexist     investigate  LOW   ⚠️   → y/n/detail

Usage:
    iz = InboxZero()
    tasks = iz.load_pending()
    iz.run_regression()
    print(iz.format_table(tasks))
    # ... user replies ...
    decisions = iz.parse_decisions(tasks, "y n detail 3 y")
    for task_id, decision in decisions.items():
        iz.mark_done(task_id, decision)
"""

import json
import logging
import os
import re
import subprocess
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# kb-supervisor CLI must be on PATH
_CLI_ENV = {
    **os.environ,
    "PATH": "/Users/adwit.sharma/.local/bin:" + os.environ.get("PATH", ""),
}

# Regression test command (run from project root)
_PROJECT_ROOT = "/Users/adwit.sharma/kb_docs"
_REGRESSION_CMD = ["python3", "local/tests/test_regression.py"]

# Maximum pre-existing failures that are acceptable (won't count as new)
_ACCEPTABLE_FAILURES = 2

# Column widths for monospace table alignment
_W_ID = 8        # "#KB-001 "
_W_TYPE = 11     # "[alias]    "
_W_CONCEPT = 22  # "console_navigation    "
_W_SUMMARY = 13  # "+4 aliases   "
_W_CONF = 5      # "HIGH "
_W_ICON = 4      # "✅   " (emoji takes 2 display cols)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _run_kanban(args: List[str]) -> subprocess.CompletedProcess:
    cmd = ["kb-supervisor", "kanban"] + args
    return subprocess.run(cmd, capture_output=True, text=True, env=_CLI_ENV)


def _parse_hermes_finding(comments: List[Dict]) -> Optional[Dict]:
    """Extract and parse the Hermes finding from task comments.

    Hermes posts its result as a comment whose body is a JSON string.
    Returns the parsed dict, or None if no valid Hermes comment found.
    """
    for comment in reversed(comments):  # most recent first
        author = comment.get("author", "")
        raw_body = comment.get("body", "")
        if not raw_body:
            continue
        # Hermes comments have a JSON body (may be a string or already a dict)
        if isinstance(raw_body, dict):
            finding = raw_body
        else:
            try:
                finding = json.loads(raw_body)
            except (json.JSONDecodeError, TypeError):
                continue
        # Accept if it looks like a Hermes finding
        if isinstance(finding, dict) and "finding_type" in finding:
            return finding
    return None


def _extract_type_and_concept(title: str) -> Tuple[str, str]:
    """Parse '[type] concept_id' from a task title.

    Returns (type_str, concept_id) e.g. ("alias", "console_navigation").
    Falls back gracefully for non-standard titles.
    """
    m = re.match(r"\[([^\]]+)\]\s*(.+)", title.strip())
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return "invest", title.strip()


def _change_summary(type_str: str, finding: Optional[Dict]) -> str:
    """Derive the short change_summary column from task type and finding."""
    if finding is None:
        return "pending"

    if type_str == "alias":
        aliases = finding.get("proposed_aliases", [])
        count = len(aliases)
        return f"+{count} alias{'es' if count != 1 else ''}" if count else "+? aliases"
    if type_str == "concept":
        return "new entry"
    if type_str == "invest":
        return "investigate"
    return "pending"


def _conf_label(finding: Optional[Dict]) -> str:
    """Normalise confidence to HIGH/MED/LOW/???."""
    if finding is None:
        return "???"
    raw = str(finding.get("confidence", "")).lower()
    if raw in ("high",):
        return "HIGH"
    if raw in ("medium", "med"):
        return "MED"
    if raw in ("low",):
        return "LOW"
    return "???"


def _regression_icon(regression_result: Optional[bool]) -> str:
    """Map regression result to display icon."""
    if regression_result is True:
        return "OK"   # will be rendered as ✅
    if regression_result is False:
        return "FAIL"  # will be rendered as ❌
    return "UNK"       # will be rendered as ⚠️


def _icon_str(reg_key: str) -> str:
    if reg_key == "OK":
        return "✅"
    if reg_key == "FAIL":
        return "❌"
    return "⚠️"


# ---------------------------------------------------------------------------
# InboxZero
# ---------------------------------------------------------------------------

class InboxZero:
    """Reads the kb-gaps kanban board and renders a decision table for review."""

    def __init__(self, board: str = "kb-gaps") -> None:
        self.board = board
        self._regression_result: Optional[bool] = None  # True=pass, False=fail, None=unknown

    # ------------------------------------------------------------------
    # load_pending
    # ------------------------------------------------------------------

    def load_pending(self) -> List[Dict]:
        """Read all pending tasks from the board.

        Includes:
          - status == "done"  (Hermes completed analysis)
          - status == "ready" with at least one Hermes finding comment

        Returns enriched task dicts with a parsed "hermes_finding" key.
        """
        result = _run_kanban(["--board", self.board, "list", "--json"])
        if result.returncode != 0:
            logger.error("kanban list failed: %s", result.stderr)
            return []

        try:
            all_tasks = json.loads(result.stdout)
        except json.JSONDecodeError:
            logger.error("kanban list returned non-JSON: %s", result.stdout[:200])
            return []

        pending: List[Dict] = []

        for task in all_tasks:
            status = task.get("status", "")
            task_id = task.get("id", "")

            if status not in ("done", "ready"):
                continue

            # Fetch full task detail to get comments
            detail_result = _run_kanban(["--board", self.board, "show", task_id, "--json"])
            if detail_result.returncode != 0:
                logger.warning("kanban show %s failed: %s", task_id, detail_result.stderr)
                comments = []
            else:
                try:
                    detail = json.loads(detail_result.stdout)
                    comments = detail.get("comments", [])
                except json.JSONDecodeError:
                    comments = []

            finding = _parse_hermes_finding(comments)

            # For "ready" tasks: only include if there's a Hermes finding
            if status == "ready" and finding is None:
                continue

            type_str, concept_id = _extract_type_and_concept(task.get("title", ""))

            enriched = {
                **task,
                "hermes_finding": finding,
                "_type_str": type_str,
                "_concept_id": concept_id,
                "_comments": comments,
            }
            pending.append(enriched)

        logger.info("Loaded %d pending tasks from board %s", len(pending), self.board)
        return pending

    # ------------------------------------------------------------------
    # run_regression
    # ------------------------------------------------------------------

    def run_regression(self) -> bool:
        """Run the regression test suite.

        Returns True if there are 0 *new* failures (up to
        _ACCEPTABLE_FAILURES pre-existing ones are allowed).
        Caches the result for use by format_table.
        """
        try:
            result = subprocess.run(
                _REGRESSION_CMD,
                capture_output=True,
                text=True,
                cwd=_PROJECT_ROOT,
            )
            output = result.stdout + result.stderr
            logger.debug("Regression output (last 10 lines):\n%s",
                         "\n".join(output.splitlines()[-10:]))

            # Look for a "N failed" or "N passed" summary line
            # pytest: "X failed, Y passed" / "X passed"
            # Custom: "FAILURES: N" / "PASS"
            failed_count = 0

            # pytest-style
            m = re.search(r"(\d+) failed", output)
            if m:
                failed_count = int(m.group(1))
            elif re.search(r"(\d+) passed", output) or re.search(r"PASS", output):
                failed_count = 0
            elif result.returncode != 0:
                # Non-zero exit but no parseable count — treat conservatively
                failed_count = _ACCEPTABLE_FAILURES + 1

            new_failures = max(0, failed_count - _ACCEPTABLE_FAILURES)
            passed = new_failures == 0

            logger.info(
                "Regression: total_failed=%d, acceptable=%d, new=%d -> %s",
                failed_count, _ACCEPTABLE_FAILURES, new_failures,
                "PASS" if passed else "FAIL",
            )
            self._regression_result = passed
            return passed

        except FileNotFoundError:
            logger.warning("Regression test file not found — marking as unknown")
            self._regression_result = None
            return False
        except Exception as exc:
            logger.error("Regression run error: %s", exc)
            self._regression_result = None
            return False

    # ------------------------------------------------------------------
    # format_table
    # ------------------------------------------------------------------

    def format_table(self, tasks: List[Dict]) -> str:
        """Render the inbox-zero decision table as a monospace-aligned string."""
        if not tasks:
            return "(no pending tasks)\n"

        reg_key = _regression_icon(self._regression_result)

        header = (
            f"{'#ID':<{_W_ID}}"
            f"{'TYPE':<{_W_TYPE}}"
            f"{'CONCEPT':<{_W_CONCEPT}}"
            f"{'CHANGE':<{_W_SUMMARY}}"
            f"{'CONF':<{_W_CONF}}"
            f"{'REG':<{_W_ICON}}"
            f"DECISION"
        )
        separator = "-" * (len(header) + 2)

        rows = [header, separator]

        for i, task in enumerate(tasks, 1):
            task_id = task.get("id", f"???{i}")
            finding = task.get("hermes_finding")
            type_str = task.get("_type_str", "invest")
            concept_id = task.get("_concept_id", "unknown")

            # Format task_id as #KB-NNN if it looks like a number, else as-is
            if re.match(r"^\d+$", str(task_id)):
                id_display = f"#KB-{int(task_id):03d}"
            else:
                id_display = f"#{task_id}"

            type_display = f"[{type_str}]"
            summary = _change_summary(type_str, finding)
            conf = _conf_label(finding)
            icon = _icon_str(reg_key)

            # Truncate concept_id if too long
            concept_display = concept_id if len(concept_id) <= _W_CONCEPT - 2 else concept_id[:_W_CONCEPT - 5] + "..."

            row = (
                f"{id_display:<{_W_ID}}"
                f"{type_display:<{_W_TYPE}}"
                f"{concept_display:<{_W_CONCEPT}}"
                f"{summary:<{_W_SUMMARY}}"
                f"{conf:<{_W_CONF}}"
                f"{icon:<{_W_ICON}}"
                f"→ y/n/detail"
            )
            rows.append(row)

        rows.append(separator)
        rows.append("")
        rows.append('Reply with decisions (e.g. "y n detail 3 y n"):')

        return "\n".join(rows) + "\n"

    # ------------------------------------------------------------------
    # parse_decisions
    # ------------------------------------------------------------------

    def parse_decisions(self, tasks: List[Dict], response: str) -> Dict[str, str]:
        """Parse user response string into per-task decisions.

        Supported tokens: y, n, skip, detail (standalone or "detail N").
        "detail N" means expand task at 1-indexed position N.
        Remaining tasks beyond the response tokens default to "skip".

        Returns {task_id: "y"|"n"|"detail"|"skip"}.
        """
        decisions: Dict[str, str] = {}
        tokens = response.strip().split()
        task_ids = [t.get("id", "") for t in tasks]
        n_tasks = len(task_ids)

        # Walk tokens, consuming 1 or 2 per task slot
        task_idx = 0
        tok_idx = 0

        while task_idx < n_tasks and tok_idx < len(tokens):
            tok = tokens[tok_idx].lower()

            if tok == "detail":
                # "detail N" -> expand task at position N (1-indexed)
                if tok_idx + 1 < len(tokens) and re.match(r"^\d+$", tokens[tok_idx + 1]):
                    target_pos = int(tokens[tok_idx + 1]) - 1
                    if 0 <= target_pos < n_tasks:
                        decisions[task_ids[target_pos]] = "detail"
                    tok_idx += 2
                    # "detail N" doesn't consume a task slot in the linear walk
                    continue
                else:
                    # "detail" without a number: applies to current task
                    decisions[task_ids[task_idx]] = "detail"

            elif tok in ("y", "yes"):
                decisions[task_ids[task_idx]] = "y"

            elif tok in ("n", "no"):
                decisions[task_ids[task_idx]] = "n"

            elif tok in ("skip", "s"):
                decisions[task_ids[task_idx]] = "skip"

            else:
                # Unrecognised token: treat as skip for this slot
                logger.warning("Unrecognised decision token '%s' for task %s — defaulting to skip",
                               tok, task_ids[task_idx])
                decisions[task_ids[task_idx]] = "skip"

            task_idx += 1
            tok_idx += 1

        # Any remaining tasks default to "skip"
        for remaining_id in task_ids[task_idx:]:
            if remaining_id not in decisions:
                decisions[remaining_id] = "skip"

        return decisions

    # ------------------------------------------------------------------
    # format_detail
    # ------------------------------------------------------------------

    def format_detail(self, task: Dict) -> str:
        """Return full detail for one task as a human-readable string."""
        task_id = task.get("id", "?")
        title = task.get("title", "(no title)")
        body = task.get("body", "")
        finding = task.get("hermes_finding")
        type_str = task.get("_type_str", "invest")
        concept_id = task.get("_concept_id", "unknown")

        lines = [
            "=" * 60,
            f"TASK {task_id}: {title}",
            "=" * 60,
            "",
        ]

        # Gap description from task body
        if body:
            lines.append("Gap description:")
            lines.append(body.strip())
            lines.append("")

        if finding:
            lines.append("Hermes finding:")
            lines.append(f"  finding_type : {finding.get('finding_type', 'unknown')}")
            lines.append(f"  concept_id   : {finding.get('concept_id', concept_id)}")
            lines.append(f"  confidence   : {finding.get('confidence', 'unknown')}")
            lines.append(f"  ready        : {finding.get('ready_for_code_change', False)}")

            reasoning = finding.get("reasoning", "")
            if reasoning:
                lines.append(f"  reasoning    : {reasoning}")

            aliases = finding.get("proposed_aliases", [])
            if aliases:
                lines.append("  proposed aliases:")
                for a in aliases:
                    lines.append(f"    - {a}")

            kb_ev = finding.get("kb_evidence", "")
            if kb_ev:
                lines.append("")
                lines.append("KB evidence:")
                lines.append(f'  "{kb_ev}"')

            lines.append("")
        else:
            lines.append("(No Hermes finding yet — analysis pending)")
            lines.append("")

        # Failing query samples from task comments (non-Hermes comments)
        comments = task.get("_comments", [])
        query_samples = []
        for c in comments:
            raw = c.get("body", "")
            if isinstance(raw, str) and not raw.startswith("{"):
                # Plain-text comment — may contain failure queries
                for line in raw.splitlines():
                    line = line.strip()
                    if line and len(line) > 8:
                        query_samples.append(line)

        if query_samples:
            lines.append("Failing query samples (from comments):")
            for q in query_samples[:5]:
                lines.append(f"  - {q}")
            lines.append("")

        # Proposed code change hint
        if type_str == "alias" and finding:
            aliases = finding.get("proposed_aliases", [])
            lines.append("Proposed change (for user approval):")
            lines.append(f"  Add aliases to CONCEPT_REGISTRY entry '{concept_id}':")
            for a in aliases:
                lines.append(f'    "{a}",')
        elif type_str == "concept":
            lines.append("Proposed change (for user approval):")
            lines.append(f"  Add new CONCEPT_REGISTRY entry for '{concept_id}'")
        elif type_str == "invest":
            lines.append("Action required:")
            lines.append(f"  Investigate root cause for '{concept_id}' — see Hermes finding above.")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines) + "\n"

    # ------------------------------------------------------------------
    # mark_done
    # ------------------------------------------------------------------

    def mark_done(self, task_id: str, decision: str) -> None:
        """Apply the user's decision to a kanban task.

        - "y"      : archive the task (approved / will be implemented)
        - "n"      : post rejection comment, then archive
        - "skip"   : leave the task as-is
        - "detail" : no action (detail was already shown; awaiting follow-up)
        """
        if decision == "skip":
            logger.debug("Skipping task %s (no action)", task_id)
            return

        if decision == "detail":
            logger.debug("Detail shown for task %s — no state change", task_id)
            return

        if decision == "n":
            # Post rejection comment before archiving
            comment_result = _run_kanban([
                "--board", self.board,
                "comment", task_id, "rejected by user",
                "--author", "kb-supervisor",
            ])
            if comment_result.returncode != 0:
                logger.warning("Failed to post rejection comment on %s: %s",
                               task_id, comment_result.stderr)

        if decision in ("y", "n"):
            archive_result = _run_kanban([
                "--board", self.board,
                "archive", task_id,
            ])
            if archive_result.returncode != 0:
                logger.error("Failed to archive task %s: %s",
                             task_id, archive_result.stderr)
            else:
                logger.info("Task %s archived (decision=%s)", task_id, decision)
