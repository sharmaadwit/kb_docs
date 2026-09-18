"""HermesCoordinator — parallel multi-agent gap judgment via Hermes workers.

Architecture
------------
1. Coordinator posts each gap as a kanban task (full context embedded in body).
2. N worker threads spin up simultaneously, one per gap.
3. Each worker runs a 3-turn Hermes conversation:
     Turn 1 — deep analysis: pipeline signal, KB inventory, all queries
     Turn 2 — adversarial self-challenge: attack the Turn 1 verdict
     Turn 3 — final conclusion: resolve challenge, write JSON verdict to file
4. Worker posts the final JSON verdict as a comment on its kanban task.
5. Coordinator aggregates all findings and returns four_bucket_verdicts dict.

Since Hermes runs a self-hosted Qwen model (no API cost), every worker runs at
full depth: max queries, full KB inventory, full doc snippets, deep reasoning.
"""

import json
import logging
import os
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

_PROFILE = "kb-supervisor"
_ENV = {**os.environ, "PATH": f"/Users/adwit.sharma/.local/bin:{os.environ.get('PATH', '')}"}

_VALID_BUCKETS = {"HAS_DOCS_FAILS", "NO_DOCS_IN_SCOPE", "OUT_OF_SCOPE", "NOISE", "UNKNOWN"}

# ---------------------------------------------------------------------------
# KB chunk search
# ---------------------------------------------------------------------------

_CHUNKS_CACHE: Optional[List[Dict]] = None
_KB_CHUNKS_PATH = Path(__file__).resolve().parents[3] / "kb" / "kb_chunks.jsonl"


def _tokenize(text: str) -> set:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _search_kb_chunks(query_tokens: set, top_k: int = 5) -> List[Dict]:
    """Search kb/kb_chunks.jsonl by token overlap, returning top_k results."""
    global _CHUNKS_CACHE
    if _CHUNKS_CACHE is None:
        chunks = []
        try:
            with open(_KB_CHUNKS_PATH, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        try:
                            chunks.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
        except FileNotFoundError:
            logger.debug("kb_chunks.jsonl not found at %s", _KB_CHUNKS_PATH)
        _CHUNKS_CACHE = chunks

    if not _CHUNKS_CACHE or not query_tokens:
        return []

    scored = []
    for chunk in _CHUNKS_CACHE:
        text = chunk.get("text") or chunk.get("content") or ""
        chunk_tokens = _tokenize(text)
        score = len(query_tokens & chunk_tokens) / max(len(query_tokens), 1)
        if score > 0:
            source = chunk.get("source") or chunk.get("file") or chunk.get("path") or ""
            scored.append({
                "source": source,
                "score": score,
                "snippet": text[:120],
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


_DEGRADED = {
    "bucket": "UNKNOWN",
    "confidence": "low",
    "reasoning": "worker failed — degraded",
    "matching_doc": None,
    "root_cause": None,
    "keywords_to_add": [],
    "doc_to_create": None,
    "doc_outline": None,
    "doc_priority": None,
    "reason_ignored": None,
    "per_query_notes": {},
    "degraded": True,
}


# ---------------------------------------------------------------------------
# Hermes conversation helper
# ---------------------------------------------------------------------------

def _hermes_turn(
    prompt: str,
    session_id: Optional[str],
    timeout: int = 300,
) -> Tuple[Optional[str], str]:
    """Send one turn to `hermes chat`. Returns (session_id, stdout_text)."""
    cmd = ["hermes", "-p", _PROFILE, "chat", "-Q", "--oneshot", "--yolo"]
    if session_id:
        cmd += ["--resume", session_id]
    cmd += ["-q", prompt]
    try:
        proc = subprocess.run(cmd, timeout=timeout, capture_output=True, env=_ENV)
    except subprocess.TimeoutExpired:
        logger.warning("hermes turn timed out after %ds", timeout)
        return None, ""
    except Exception as exc:
        logger.warning("hermes turn subprocess error: %s", exc)
        return None, ""
    if proc.returncode != 0:
        logger.warning("hermes turn exited %d", proc.returncode)
        return None, ""
    stdout = proc.stdout.decode(errors="replace")
    sid = session_id
    for line in stdout.splitlines():
        if line.startswith("session_id:"):
            sid = line.split(":", 1)[1].strip()
            break
    return sid, stdout


def _hermes_single(prompt: str, timeout: int = 300) -> str:
    """Single-shot hermes call (-z). Returns stdout text."""
    try:
        proc = subprocess.run(
            ["hermes", "-p", _PROFILE, "-z", prompt, "--yolo"],
            timeout=timeout, capture_output=True, env=_ENV,
        )
        if proc.returncode == 0:
            return proc.stdout.decode(errors="replace")
    except Exception as exc:
        logger.warning("hermes single-shot error: %s", exc)
    return ""


# ---------------------------------------------------------------------------
# Worker
# ---------------------------------------------------------------------------

class GapWorker:
    """One Hermes worker agent handling a single gap judgment task."""

    def __init__(self, gap, old_key: str, classification: Dict[str, Any],
                 judge, kanban, output_dir: Path):
        self.gap = gap
        self.old_key = old_key
        self.classification = classification
        self.judge = judge        # HermesJudge instance (for KB inventory + pipeline signal)
        self.kanban = kanban
        self.output_dir = output_dir

    def run(self, task_id: str, timeout_per_turn: int = 300) -> Dict[str, Any]:
        gap = self.gap
        gap_key = f"{gap.module}/{gap.intent}"
        logger.info("  worker[%s] starting: %s", task_id, gap_key)

        # Build shared context once
        pipeline_signal = self.judge._build_pipeline_signal(self.classification)
        kb_inventory = self.judge._build_kb_inventory()
        det_verdict = self.classification.get("category", "unknown")
        det_confidence = self.classification.get("confidence", "unknown")
        failing_queries = "\n".join(
            f"  {i+1}. {q}" for i, q in enumerate((gap.failure_examples or [])[:15])
        )

        output_path = str(self.output_dir / f"worker_{task_id}.json")

        # ── KB chunk search (pre-computed) ───────────────────────────────────
        all_query_tokens: set = set()
        for q in (gap.failure_examples or [])[:15]:
            all_query_tokens |= _tokenize(q)
        kb_chunks = _search_kb_chunks(all_query_tokens, top_k=5)

        kb_search_section = "## Local KB Search Results (pre-computed before judge runs)\n"
        kb_search_section += "These docs scored highest against this gap's query tokens.\n"
        kb_search_section += "Use this as ground truth for whether relevant docs exist:\n\n"
        if kb_chunks:
            for ch in kb_chunks:
                kb_search_section += f"  score={ch['score']:.2f}  {ch['source']}\n"
                kb_search_section += f"              \"{ch['snippet']}\"\n"
            top_score = kb_chunks[0]["score"]
            if top_score > 0.4:
                kb_search_section += "\nNOTE: High-scoring docs found — verify carefully before calling NO_DOCS_IN_SCOPE."
            elif top_score < 0.2:
                kb_search_section += "\nNOTE: No strong KB matches found — NO_DOCS_IN_SCOPE likely correct."
        else:
            kb_search_section += "  (No results — kb_chunks.jsonl unavailable or no token overlap found)\n"
            kb_search_section += "\nNOTE: No strong KB matches found — NO_DOCS_IN_SCOPE likely correct."

        json_schema = json.dumps({
            "bucket": "HAS_DOCS_FAILS | NO_DOCS_IN_SCOPE | OUT_OF_SCOPE | NOISE",
            "confidence": "high | medium | low",
            "reasoning": "paragraph referencing specific query results and doc evidence",
            "matching_doc": "kb/path/to/doc.md or null",
            "root_cause": "keyword_gap | routing_miss | retrieval_rank | content_thin | answer_quality | null",
            "keywords_to_add": ["specific missing term from IDK queries"],
            "doc_to_create": "kb/module/filename.md or null",
            "doc_outline": None,
            "doc_priority": "high | medium | low | null",
            "reason_ignored": "explanation if OUT_OF_SCOPE or NOISE, else null",
            "per_query_notes": {"query_prefix": "IDK|ANSWERED — one-line diagnosis"},
        }, indent=2)

        # ── Turn 1: Deep Analysis ────────────────────────────────────────────
        t1_prompt = f"""You are a KB gap analysis agent for the Gupshup Guide skill.

The Gupshup Guide answers questions ONLY about Gupshup's products:
WhatsApp Business API, Bot Studio, Campaign Manager, SuperAgent, Agent Assist,
CTX, BizAI/Meta Business Agent, Channels (RCS, Instagram, Viber, Telegram),
Integrations, AI Admin, Personalize, Wallet, Goals.

## Your Task
Analyze this gap and determine which of 4 buckets it belongs to:

  HAS_DOCS_FAILS   — KB doc exists AND covers this topic AND was retrieved, but skill IDKed.
                     Fix: add keywords or fix routing in kb_answer.py.
  NO_DOCS_IN_SCOPE — Legitimate Gupshup product question, no KB doc exists.
                     Fix: create a new KB document.
  OUT_OF_SCOPE     — Not about Gupshup products, OR most queries already ANSWERED.
                     Action: ignore.
  NOISE            — Malformed, too short, test traffic.
                     Action: ignore.

## Gap Details
Module: {gap.module}
Intent: {gap.intent}
Total failures: {gap.failure_count}
Answer rate: {gap.answer_rate:.1%}
Deterministic pre-classification: {det_verdict} (confidence: {det_confidence})

## All Failing Queries (up to 15)
{failing_queries}

## Per-Query Live Pipeline Results
PRIMARY EVIDENCE. Shows exactly what happened for each query in the live skill:
  [IDK] = skill returned "I don't know"
  [ANSWERED] = skill gave an answer
  ⚠ FALSE-POSITIVE RETRIEVAL = retrieved doc does NOT cover the query topic

{pipeline_signal}

{kb_search_section}

## KB File Inventory (title + section headings)
{kb_inventory}

## Key Rules
- HAS_DOCS_FAILS ONLY if: (a) query is IDK AND (b) retrieved doc COVERS the topic (no ⚠ flag)
- If ⚠ FALSE-POSITIVE RETRIEVAL appears → doc doesn't cover it → NO_DOCS_IN_SCOPE
- If most queries show [ANSWERED] → gap is not real → OUT_OF_SCOPE
- For HAS_DOCS_FAILS: give SPECIFIC keywords from the IDK queries that are absent in the doc

Think step by step. Analyze each IDK query individually. Name the specific docs and why."""

        sid, t1_out = _hermes_turn(t1_prompt, None, timeout_per_turn)
        if not sid:
            logger.warning("  worker[%s] turn 1 failed, falling back to single-shot", task_id)
            return self._single_shot_fallback(output_path, t1_prompt, json_schema, gap_key, task_id)

        logger.debug("  worker[%s] turn 1 complete (session=%s)", task_id, sid)

        # ── Turn 2: Adversarial Challenge ────────────────────────────────────
        t2_prompt = f"""Now challenge your own analysis from Turn 1. Be adversarial.

For each conclusion you reached:
1. If you said HAS_DOCS_FAILS: verify the retrieved doc actually covers the query.
   Look for ⚠ FALSE-POSITIVE RETRIEVAL flags. If present → switch to NO_DOCS_IN_SCOPE.
2. If you said NO_DOCS_IN_SCOPE: scan the KB inventory carefully for any file whose
   section headings match the query topic. Did you miss a doc?
3. If you said OUT_OF_SCOPE: are any IDK queries genuinely about a Gupshup product?
4. Check: are there ANSWERED queries mixed in? Those should not count as failures.
5. The local KB search found these docs (from Turn 1 context). If you called
   NO_DOCS_IN_SCOPE but a high-scoring doc exists above, you must explain why it
   doesn't cover the queries before confirming that bucket.

After challenging, state your final verdict with high confidence.
Name the single bucket. Explain what evidence you're basing it on."""

        sid, t2_out = _hermes_turn(t2_prompt, sid, timeout_per_turn)
        if not sid:
            logger.warning("  worker[%s] turn 2 failed, using turn 1 output for conclusion", task_id)
            t2_out = t1_out  # fall through to turn 3 with turn 1 context

        logger.debug("  worker[%s] turn 2 complete", task_id)

        # ── Turn 3: Final Verdict → JSON ─────────────────────────────────────
        t3_prompt = f"""Based on your analysis and challenge, produce the final verdict.

Requirements:
- keywords_to_add (if HAS_DOCS_FAILS): list the EXACT terms from the IDK queries that
  are absent from the matching doc's headings/keywords — not generic terms.
- reasoning: reference specific query results and doc evidence from the pipeline signal.
- per_query_notes: one line per query explaining why it IDKs or answers.

Write ONLY valid JSON to the file: {output_path}
Schema:
{json_schema}

No prose, no markdown fences. Only JSON."""

        sid, t3_out = _hermes_turn(t3_prompt, sid, timeout_per_turn)
        if not sid:
            logger.warning("  worker[%s] turn 3 failed, single-shot fallback", task_id)
            return self._single_shot_fallback(output_path, t1_prompt, json_schema, gap_key, task_id)

        logger.debug("  worker[%s] turn 3 complete", task_id)

        # ── Parse output ─────────────────────────────────────────────────────
        verdict = self._parse_output(output_path, gap_key, task_id)

        # ── Post to kanban ───────────────────────────────────────────────────
        if task_id and not verdict.get("degraded"):
            try:
                self.kanban.post_hermes_finding(task_id, verdict)
                logger.info("  worker[%s] posted finding: %s → %s (%s)",
                            task_id, gap_key, verdict["bucket"], verdict["confidence"])
            except Exception as exc:
                logger.warning("  worker[%s] kanban post failed: %s", task_id, exc)

        return verdict

    def _parse_output(self, output_path: str, gap_key: str, task_id: str) -> Dict[str, Any]:
        try:
            with open(output_path, "r", encoding="utf-8") as fh:
                raw = fh.read().strip()
            # Strip markdown fences if model wrapped despite instructions
            if raw.startswith("```"):
                raw = "\n".join(
                    ln for ln in raw.splitlines()
                    if not ln.startswith("```")
                ).strip()
            parsed = json.loads(raw)
        except FileNotFoundError:
            logger.warning("  worker[%s] output file not found: %s", task_id, output_path)
            return {**_DEGRADED, "reasoning": "output file not found"}
        except json.JSONDecodeError as exc:
            logger.warning("  worker[%s] JSON parse error: %s", task_id, exc)
            return {**_DEGRADED, "reasoning": f"JSON parse error: {exc}"}

        if parsed.get("bucket") not in _VALID_BUCKETS:
            return {**_DEGRADED, "reasoning": f"invalid bucket: {parsed.get('bucket')}"}

        return {
            "bucket": parsed.get("bucket"),
            "confidence": parsed.get("confidence", "low"),
            "reasoning": parsed.get("reasoning", ""),
            "matching_doc": parsed.get("matching_doc"),
            "root_cause": parsed.get("root_cause"),
            "keywords_to_add": parsed.get("keywords_to_add") or [],
            "doc_to_create": parsed.get("doc_to_create"),
            "doc_outline": parsed.get("doc_outline"),
            "doc_priority": parsed.get("doc_priority"),
            "reason_ignored": parsed.get("reason_ignored"),
            "per_query_notes": parsed.get("per_query_notes") or {},
            "degraded": False,
        }

    def _single_shot_fallback(self, output_path: str, context_prompt: str,
                               json_schema: str, gap_key: str, task_id: str) -> Dict[str, Any]:
        """Fallback: single hermes -z call if conv turns fail."""
        logger.info("  worker[%s] single-shot fallback for %s", task_id, gap_key)
        prompt = f"{context_prompt}\n\nWrite ONLY valid JSON to: {output_path}\n{json_schema}\nNo prose, no fences."
        _hermes_single(prompt, timeout=300)
        return self._parse_output(output_path, gap_key, task_id)


# ---------------------------------------------------------------------------
# Coordinator
# ---------------------------------------------------------------------------

class HermesCoordinator:
    """Fans out gap judgment to parallel GapWorker agents.

    Each worker runs a 3-turn Hermes conversation (analyze → challenge → conclude)
    and posts findings to its kanban task. Coordinator aggregates all verdicts.
    """

    def __init__(self, judge, kanban):
        self.judge = judge
        self.kanban = kanban
        _REPO_ROOT = Path(__file__).resolve().parents[3]
        self.output_dir = _REPO_ROOT / "local" / "supervisor" / "judge_outputs" / f"coord_{os.getpid()}_{int(time.time())}"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(
        self,
        gaps: list,
        classifications: Dict[str, Any],
        all_traces: list,
        max_workers: int = 8,
    ) -> Dict[str, Any]:
        """Run all gap workers in parallel. Returns four_bucket_verdicts dict."""
        import shutil
        if not shutil.which("hermes"):
            logger.warning("Hermes not available — returning degraded verdicts for all gaps")
            return {
                f"{gap.module}/{gap.intent}": {**_DEGRADED, "reasoning": "hermes not available"}
                for gap in gaps
            }

        # 1. Post all gaps to kanban and record task IDs
        logger.info("  coordinator: posting %d gaps to kanban board", len(gaps))
        self.kanban.clear_board()
        task_ids: Dict[str, str] = {}  # gap_key -> task_id
        for idx, gap in enumerate(gaps):
            old_key = f"Gap #{idx + 1}"
            classification = classifications.get(old_key, {})
            task_id = self._post_gap_task(idx + 1, gap, classification)
            if task_id:
                gap_key = f"{gap.module}/{gap.intent}"
                task_ids[gap_key] = task_id
                logger.info("  coordinator: posted %s → task %s", gap_key, task_id)

        # 2. Fan out workers in parallel
        logger.info("  coordinator: spinning up %d workers (max_workers=%d)",
                    len(gaps), max_workers)

        four_bucket_verdicts: Dict[str, Any] = {}

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            future_to_gap: dict = {}
            for idx, gap in enumerate(gaps):
                old_key = f"Gap #{idx + 1}"
                classification = classifications.get(old_key, {})
                gap_key = f"{gap.module}/{gap.intent}"
                task_id = task_ids.get(gap_key, "")

                worker = GapWorker(
                    gap=gap,
                    old_key=old_key,
                    classification=classification,
                    judge=self.judge,
                    kanban=self.kanban,
                    output_dir=self.output_dir,
                )
                future = pool.submit(worker.run, task_id)
                future_to_gap[future] = (gap, gap_key)

            for future in as_completed(future_to_gap):
                gap, gap_key = future_to_gap[future]
                try:
                    verdict = future.result()
                    four_bucket_verdicts[gap_key] = verdict
                    logger.info("  coordinator: %s → %s (%s)",
                                gap_key, verdict.get("bucket"), verdict.get("confidence"))
                except Exception as exc:
                    logger.warning("  coordinator: worker error for %s: %s", gap_key, exc)
                    four_bucket_verdicts[gap_key] = {
                        **_DEGRADED,
                        "reasoning": f"worker exception: {exc}",
                    }

        logger.info("  coordinator: all %d workers complete", len(gaps))
        return four_bucket_verdicts

    def _post_gap_task(self, gap_idx: int, gap, classification: Dict[str, Any]) -> Optional[str]:
        """Post one gap as a kanban task (always, regardless of actionability). Returns task_id or None."""
        try:
            task_id = self.kanban._create_gap_task(
                gap_index=gap_idx,
                gap=gap,
                category=classification.get("category", "unknown"),
                failure_examples=gap.failure_examples or [],
                per_query_results=classification.get("per_query_results") or [],
                confidence=classification.get("confidence", "low"),
            )
            return task_id
        except Exception as exc:
            logger.warning("  coordinator: kanban post failed for Gap #%d: %s", gap_idx, exc)
        return None
