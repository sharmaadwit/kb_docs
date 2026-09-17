"""
ProposalsWriter — generates the async decision document for KB gap approvals.

Flow:
  1. Claude reads done Kanban tasks  (load_tasks)
  2. Writes proposals/YYYY-MM-DD.md  (write_document)
  3. User edits the file at their pace (checks/unchecks boxes, deletes lines)
  4. Claude reads back and applies    (read_approved)

Risk tiers
  GREEN  — alias-only + HIGH confidence + regression passed  → pre-ticked [x], batch
  YELLOW — invest/concept + HIGH confidence                  → unchecked [ ], individual
  RED    — low confidence OR ambiguous concept               → unchecked [ ], sign-off
"""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

_KB_SUPERVISOR_BIN = "kb-supervisor"
_BOARD = "kb-gaps"

_HIGH = "high"
_MED  = "medium"
_LOW  = "low"

_GREEN_FINDING_TYPES = {"alias_candidate"}


def _run_kb(args: List[str]) -> Optional[Any]:
    """Run kb-supervisor CLI, return parsed JSON or None on failure."""
    env = {**os.environ, "PATH": f"/Users/adwit.sharma/.local/bin:{os.environ.get('PATH', '')}"}
    try:
        result = subprocess.run(
            [_KB_SUPERVISOR_BIN, "kanban", "--board", _BOARD] + args + ["--json"],
            capture_output=True, text=True, env=env, timeout=30,
        )
        if result.returncode != 0:
            logger.warning("kb-supervisor error: %s", result.stderr[:300])
            return None
        return json.loads(result.stdout)
    except Exception as exc:
        logger.warning("kb-supervisor call failed: %s", exc)
        return None


def _run_kb_no_json(args: List[str]) -> bool:
    """Run kb-supervisor CLI without --json flag, return success bool."""
    env = {**os.environ, "PATH": f"/Users/adwit.sharma/.local/bin:{os.environ.get('PATH', '')}"}
    try:
        result = subprocess.run(
            [_KB_SUPERVISOR_BIN, "kanban", "--board", _BOARD] + args,
            capture_output=True, text=True, env=env, timeout=30,
        )
        return result.returncode == 0
    except Exception as exc:
        logger.warning("kb-supervisor call failed: %s", exc)
        return False


def _parse_finding(comment_body: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(comment_body)
    except Exception:
        return None


def _tier(finding: Optional[Dict], task: Optional[Dict] = None) -> str:
    """Return 'green', 'yellow', 'red', or 'idk' for a task."""
    if finding is not None and finding.get("finding_type", "").lower() in ("idk_correct", "out_of_scope"):
        return "idk"
    # Also check the kanban task's sub_category field
    if task is not None and "idk_correct" in str(task.get("sub_category", "")):
        return "idk"
    if finding is None:
        return "yellow"
    confidence = finding.get("confidence", "low").lower()
    finding_type = finding.get("finding_type", "").lower()
    ready = finding.get("ready_for_code_change", False)

    if not ready:
        return "red"
    if confidence == _LOW:
        return "red"
    if confidence == _HIGH and finding_type in _GREEN_FINDING_TYPES:
        return "green"
    if finding_type == "missing_concept" and confidence == _HIGH:
        return "yellow"
    return "yellow"


def _run_regression() -> Tuple[bool, str]:
    """Run regression tests, return (passed, summary_line)."""
    try:
        result = subprocess.run(
            ["python3", "local/tests/test_regression.py"],
            capture_output=True, text=True,
            cwd="/Users/adwit.sharma/kb_docs", timeout=120,
        )
        output = result.stdout + result.stderr
        m = re.search(r"TOTAL: (\d+) passed, (\d+) failed", output)
        if m:
            passed, failed = int(m.group(1)), int(m.group(2))
            ok = failed <= 2
            icon = "✅" if ok else "❌"
            return ok, f"{icon} {passed}/{passed+failed}"
        return True, "⚠️ unknown"
    except Exception as exc:
        return True, f"⚠️ {exc}"


def _render_concept_entry(lines: List[str], concept_id: str, module: str, aliases: List[str], kb_doc_needed: bool = True) -> None:
    """Render a single CONCEPT_REGISTRY + KB doc block."""
    module_slug = module.lower().replace(" ", "_")
    concept_slug = concept_id.replace("_", "-")
    kb_file = f"kb/{module_slug}/{concept_slug}.md"
    lines.append("**CONCEPT_REGISTRY change:**")
    lines.append(f"  - `id`: `{concept_id}`")
    lines.append(f"  - `module`: `{module}`")
    if aliases:
        lines.append("  - `aliases`:")
        for a in aliases:
            lines.append(f'    - "{a}"')
    lines.append("")
    if kb_doc_needed:
        lines.append(f"**KB doc to create:** `{kb_file}`")
    else:
        lines.append(f"**KB doc needed:** No — existing content covers this (BM25 score > 2.0). Adding concept routes queries to it.")
    lines.append("")


def _render_missing_concept(lines: List[str], f: Dict[str, Any]) -> None:
    """Render a missing_concept finding as a concrete implementation checklist."""
    concept_id = f.get("proposed_concept_id") or f.get("concept_id") or "unknown"
    module = f.get("proposed_module") or f.get("gap_module") or "unknown"
    aliases = f.get("proposed_aliases", [])
    reasoning = f.get("reasoning", "")
    next_step = f.get("suggested_next_step", "")
    additional = f.get("additional_concepts", [])

    kb_doc_needed = f.get("kb_doc_needed", True)
    n_concepts = 1 + len(additional)
    needs_doc = kb_doc_needed
    if n_concepts > 1:
        lines.append(f"**Action required:** Create {n_concepts} new CONCEPT_REGISTRY entries" + (" + KB docs" if needs_doc else " (no new KB docs needed — content exists)"))
    else:
        lines.append("**Action required:** Create new CONCEPT_REGISTRY entry" + (" + KB doc" if needs_doc else " (no new KB doc needed — content exists)"))
    lines.append("")

    if n_concepts > 1:
        lines.append(f"**Concept 1 of {n_concepts}:**")
        lines.append("")
    _render_concept_entry(lines, concept_id, module, aliases, kb_doc_needed=needs_doc)

    for i, extra in enumerate(additional, start=2):
        ex_id = extra.get("proposed_concept_id", "unknown")
        ex_module = extra.get("proposed_module") or module
        ex_aliases = extra.get("proposed_aliases", [])
        ex_reasoning = extra.get("reasoning", "")
        ex_kb_doc_needed = extra.get("kb_doc_needed", kb_doc_needed)
        lines.append(f"**Concept {i} of {n_concepts}:**")
        if ex_reasoning:
            lines.append(f"*{ex_reasoning}*")
        lines.append("")
        _render_concept_entry(lines, ex_id, ex_module, ex_aliases, kb_doc_needed=ex_kb_doc_needed)

    if reasoning:
        lines.append(f"**Judge reasoning:** {reasoning}")
        lines.append("")
    if next_step:
        lines.append(f"**Suggested next step:** {next_step}")
        lines.append("")


def _fmt_aliases(aliases: List[str], max_show: int = 4) -> str:
    """Format alias list for display."""
    shown = [f'"{a}"' for a in aliases[:max_show]]
    rest = len(aliases) - max_show
    s = ", ".join(shown)
    if rest > 0:
        s += f" (+{rest} more)"
    return s


class ProposalsWriter:
    """Generate and read the async proposals document."""

    def __init__(self, output_dir: Path = Path("local/supervisor/proposals")):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ── 1. Load tasks from board ───────────────────────────────────────────────

    def load_tasks(self) -> List[Dict[str, Any]]:
        """Load all active tasks from the kb-gaps board, enriched with findings."""
        raw = _run_kb(["list"])
        if not raw:
            return []

        tasks = raw if isinstance(raw, list) else raw.get("tasks", [])
        enriched = []
        for t in tasks:
            status = t.get("status", "")
            if status in ("archived", "done"):
                continue
            detail = _run_kb(["show", t["id"]])
            finding = None
            comments = []
            if detail:
                comments = detail.get("comments", [])
                for c in reversed(comments):
                    if c.get("author") in ("kb-supervisor", "hermes"):
                        finding = _parse_finding(c.get("body", ""))
                        break
            enriched.append({**t, "finding": finding, "comments": comments})

        return enriched

    # ── 2. Write proposals document ───────────────────────────────────────────

    def write_document(self, tasks: List[Dict[str, Any]]) -> Path:
        """Write the tiered async decision document."""
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        out_path = self.output_dir / f"{date_str}.md"

        reg_ok, reg_summary = _run_regression()

        # Deduplicate by (finding_type, gap_module, gap_intent, near_miss_concepts)
        # Multiple supervisor runs create duplicate tasks for the same gap
        seen_sigs: set = set()
        deduped: List[Dict] = []
        for t in tasks:
            f = t.get("finding") or {}
            sig = (
                f.get("finding_type", ""),
                f.get("gap_module", ""),
                f.get("gap_intent", ""),
                tuple(sorted(f.get("near_miss_concepts", []))),
                f.get("root_cause", ""),
            )
            if sig in seen_sigs and sig != ("", "", "", (), ""):
                continue
            seen_sigs.add(sig)
            deduped.append(t)

        green, yellow, red, idk = [], [], [], []
        for t in deduped:
            tier = _tier(t.get("finding"), t)
            if tier == "idk":
                idk.append(t)
            elif tier == "green":
                green.append(t)
            elif tier == "yellow":
                yellow.append(t)
            else:
                red.append(t)

        actionable = len(green) + len(yellow) + len(red)
        total_raw = len(tasks)

        lines = [
            f"# KB Proposals — {date_str}",
            f"Board: kb-gaps | {total_raw} tasks ({actionable} after dedup) | Regression: {reg_summary}",
            "",
        ]

        # ── GREEN ──────────────────────────────────────────────────────────────
        lines += [
            "---",
            "",
            "## 🟢 GREEN — Batch approve",
            "*High confidence · alias-only · regression passed.*",
            "*Pre-ticked. Delete any line you don't want. Say \"apply proposals\" to commit.*",
            "",
        ]
        if green:
            for t in green:
                f = t.get("finding") or {}
                task_id = t["id"]
                failures = f.get("failure_count", "?")
                concepts = f.get("near_miss_concepts", [])
                concept_str = ", ".join(f"`{c}`" for c in concepts) if concepts else "`unknown`"
                aliases = f.get("proposed_aliases", [])
                module = f.get("gap_module", "?")
                intent = f.get("gap_intent", "?")
                lines.append(
                    f"- [x] #{task_id}  "
                    f"**{failures} failures** · {module}/{intent}  "
                    f"→ add aliases to {concept_str}  "
                    f"({len(aliases)} aliases: {_fmt_aliases(aliases, 3)})"
                )
        else:
            lines.append("*(none this run)*")
        lines.append("")

        # ── YELLOW ────────────────────────────────────────────────────────────
        lines += [
            "---",
            "",
            "## 🟡 YELLOW — Review individually",
            "*High confidence but requires investigation or new concept entry.*",
            "",
        ]
        if yellow:
            for t in yellow:
                f = t.get("finding") or {}
                task_id = t["id"]
                finding_type = f.get("finding_type", "unknown")
                failures = f.get("failure_count", "?")
                confidence = f.get("confidence", "unknown").upper()
                module = f.get("gap_module", "?")
                intent = f.get("gap_intent", "?")
                root_cause = f.get("root_cause", "")
                reasoning = f.get("reasoning", "")
                next_step = f.get("suggested_next_step", "")
                boost_changes = f.get("proposed_boost_changes", {})

                mismatch = f.get("gap_mismatch_detail", "")
                mismatch_str = f"  ⚠ **Routing mismatch:** {mismatch}" if mismatch else ""
                header_detail = (
                    f"Concept: `{f.get('proposed_concept_id', '?')}`"
                    if finding_type == "missing_concept"
                    else f"Root cause: {root_cause or '—'}"
                )
                lines += [
                    f"### #{task_id}  [{finding_type}]  {module}/{intent}",
                    f"**Failures:** {failures} | **Confidence:** {confidence} | **{header_detail}**{mismatch_str}",
                    "",
                ]
                examples = f.get("failure_examples", [])
                if examples:
                    lines.append("**Failing messages:**")
                    for ex in examples[:5]:
                        lines.append(f"  - _{ex}_")
                    lines.append("")
                if finding_type == "missing_concept":
                    _render_missing_concept(lines, f)
                else:
                    if reasoning:
                        lines.append(f"**Diagnosis:** {reasoning}")
                        lines.append("")
                    if next_step:
                        lines.append(f"**Suggested fix:** {next_step}")
                        lines.append("")
                    if boost_changes:
                        lines.append("**Proposed boost changes:**")
                        for src, val in boost_changes.items():
                            lines.append(f"  - `{src}`: {val:+.1f}")
                        lines.append("")
                lines += ["- [ ] approve   - [ ] reject", ""]
        else:
            lines += ["*(none this run)*", ""]

        # ── RED ───────────────────────────────────────────────────────────────
        lines += [
            "---",
            "",
            "## 🔴 RED — Explicit sign-off needed",
            "*Low confidence or ambiguous concept match. Review before approving.*",
            "",
        ]
        if red:
            for t in red:
                f = t.get("finding") or {}
                task_id = t["id"]
                finding_type = f.get("finding_type", "unknown")
                failures = f.get("failure_count", "?")
                confidence = f.get("confidence", "low").upper()
                module = f.get("gap_module", "?")
                intent = f.get("gap_intent", "?")
                aliases = f.get("proposed_aliases", [])
                concepts = f.get("near_miss_concepts", [])
                reasoning = f.get("reasoning", "")
                kb_evidence = f.get("kb_evidence", "")
                root_cause = f.get("root_cause", "")

                mismatch = f.get("gap_mismatch_detail", "")
                mismatch_str = f"  ⚠ **Routing mismatch:** {mismatch}" if mismatch else ""
                no_concept = f.get("no_concept_match_count", 0)
                no_concept_str = f" | **No concept match:** {no_concept} queries (pure BM25)" if no_concept else ""
                lines += [
                    f"### #{task_id}  [{finding_type}]  {module}/{intent}",
                    f"**Failures:** {failures} | **Confidence:** {confidence}{mismatch_str}{no_concept_str}",
                    "",
                ]

                examples = f.get("failure_examples", [])
                if examples:
                    lines.append("**Failing messages:**")
                    for ex in examples[:5]:
                        lines.append(f"  - _{ex}_")
                    lines.append("")

                if finding_type == "alias_candidate":
                    if concepts:
                        lines.append(f"**Near-miss concepts:** `{'`, `'.join(concepts)}`")
                    if kb_evidence:
                        # Render each concept's alias info on its own line for readability
                        lines.append("**Existing aliases:**")
                        for entry in kb_evidence.split("; "):
                            if entry.strip():
                                lines.append(f"  - {entry.strip()}")
                    if aliases:
                        # P5: filter out full-sentence aliases (>6 words) from display
                        short_aliases = [a for a in aliases if len(a.split()) <= 6]
                        long_count = len(aliases) - len(short_aliases)
                        if short_aliases:
                            lines.append("**Proposed aliases:**")
                            for a in short_aliases[:10]:
                                lines.append(f'  - `{a}`')
                            if long_count:
                                lines.append(f"  *(+ {long_count} full-sentence alias(es) stripped — judge needs calibration)*")
                        else:
                            lines.append(f"**Proposed aliases:** *(all {long_count} were full-sentence — judge needs calibration)*")
                    if reasoning:
                        lines.append(f"**Why {confidence}:**")
                        for part in reasoning.split("; "):
                            if part.strip():
                                lines.append(f"  - {part.strip()}")

                elif finding_type == "missing_concept":
                    _render_missing_concept(lines, f)
                elif finding_type == "needs_investigation":
                    if reasoning:
                        lines.append(f"**Diagnosis:** {reasoning}")
                    if kb_evidence:
                        lines.append(f"**KB files:** {kb_evidence}")
                    if root_cause:
                        lines.append(f"**Root cause:** {root_cause}")

                lines += ["", "- [ ] approve   - [ ] reject", ""]
        else:
            lines += ["*(none this run)*", ""]

        # ── IDK ───────────────────────────────────────────────────────────────
        lines += [
            "---",
            "",
            "## ⚫ IDK — No action needed",
            "*Judge confirmed IDK is correct behavior. No KB content exists for these queries.*",
            "",
        ]
        if idk:
            for t in idk:
                f = t.get("finding") or {}
                task_id = t["id"]
                failures = f.get("failure_count", "?")
                module = f.get("gap_module", "?")
                intent = f.get("gap_intent", "?")
                reasoning = f.get("reasoning", "") or f.get("root_cause", "")
                examples = f.get("failure_examples", [])
                lines += [
                    f"### #{task_id}  {module}/{intent}  ({failures} failures)",
                ]
                if reasoning:
                    lines += [f"**Why IDK is correct:** {reasoning}", ""]
                if examples:
                    lines.append("**Example queries (all correctly returned IDK):**")
                    for ex in examples[:5]:
                        lines.append(f"  - _{ex}_")
                    lines.append("")
        else:
            lines.append("*(none this run)*")
        lines.append("")

        lines += [
            "---",
            "",
            "## ⏭ Skipped",
            "*(ALREADY_FIXED / OUT_OF_SCOPE / CONTENT_GAP — see supervisor report)*",
            "",
            "---",
            "",
            "<!-- Say \"apply proposals\" to commit all [x] items -->",
        ]

        out_path.write_text("\n".join(lines))
        logger.info("Proposals written to %s", out_path)
        return out_path

    # ── 3. Read approved items back ───────────────────────────────────────────

    def read_approved(self, date_str: Optional[str] = None) -> Dict[str, str]:
        """Parse the proposals file and return {task_id: 'approve'|'reject'}."""
        if date_str is None:
            date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        path = self.output_dir / f"{date_str}.md"
        if not path.exists():
            logger.warning("No proposals file for %s", date_str)
            return {}

        text = path.read_text()
        decisions: Dict[str, str] = {}

        # GREEN: - [x] #t_XXXXXXXX or - [ ] #t_XXXXXXXX
        for m in re.finditer(r"- \[(x| )\] #(t_[a-z0-9]+)", text):
            checked, task_id = m.group(1), m.group(2)
            decisions[task_id] = "approve" if checked == "x" else "reject"

        # YELLOW / RED: - [ ] approve or - [x] approve after a task header
        current_task = None
        for line in text.splitlines():
            hdr = re.match(r"### #(t_[a-z0-9]+)", line)
            if hdr:
                current_task = hdr.group(1)
            if current_task:
                if re.search(r"\[x\]\s+approve", line):
                    decisions[current_task] = "approve"
                elif re.search(r"\[x\]\s+reject", line):
                    decisions[current_task] = "reject"

        return decisions

    # ── 4. Archive task after decision ────────────────────────────────────────

    def mark_applied(self, task_id: str, committed: bool) -> None:
        """Archive task and post outcome comment."""
        outcome = "applied and committed" if committed else "rejected by user"
        _run_kb_no_json(["comment", task_id, f"Outcome: {outcome}", "--author", "claude"])
        _run_kb_no_json(["archive", task_id])
