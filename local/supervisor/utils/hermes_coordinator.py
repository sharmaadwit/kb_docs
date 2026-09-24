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
# Skill context preamble — injected into every Turn 1 prompt
# ---------------------------------------------------------------------------

_SKILL_CONTEXT_PREAMBLE = """## Skill Context & Principles

### What this skill answers
The Gupshup Guide answers questions about Gupshup Console products only:
  - WhatsApp Business API / WABA setup, templates, flows, sandbox, inbound webhooks
  - Bot Studio / Journey Builder (same product — Journey Builder IS Bot Studio)
    Docs live in kb/bot-studio/: journey-builder-setup.md, journey-builder-nodes.md,
    consulting-loop-prevention.md (infinite loops), consulting-conditional-branching.md,
    consulting-when-to-build.md, manage-variables.md, api-node.md, manage-api.md
  - Campaign Manager, RCS, SMS/DLT, Instagram, Viber, Telegram
  - Integrations (webhooks, Shopify, MoEngage, CleverTap, custom integrations)
  - SuperAgent, Agent Assist, AI Admin, Personalize, Wallet, Goals, CTX
  - CC Express (silent alias for Gupshup Console — same features)

### What the skill REFUSES by design (these are NOT KB gaps — do NOT recommend docs)

1. PRICING QUERIES — bucket=OUT_OF_SCOPE always
   The skill intentionally does NOT answer pricing. Pricing IDK is a sales signal.
   Applies to: cost, price, pricing, per-message rate, plan tiers, billing, tariffs,
   monthly fee, mensalidade, mensualidad, tarifa, custo, costo, charges, fees.
   reason_ignored="pricing queries refused by design — sales signal"
   EXCEPTION: BizAI pricing IS answered (BizAI pricing docs are boosted in the skill).

2. GENERAL KNOWLEDGE / OFF-TOPIC — bucket=OUT_OF_SCOPE
   Anything not about Gupshup products: geography, sports, jokes, food, weather,
   competitor-only questions (Salesforce, HubSpot, Zoho), personal queries.
   reason_ignored="general knowledge / off-topic — not a Gupshup product question"

3. INTERNAL INFRASTRUCTURE ALERTS — bucket=OUT_OF_SCOPE
   AWS alerts, OpenSearch node storage warnings, internal monitoring events.
   These are IT issues, not product questions.
   reason_ignored="internal infrastructure alert — not a product question"

4. COMPETITOR COMPARISONS — evaluate carefully
   "Gupshup vs Kaleyra vs ValueFirst": if there is a genuine Gupshup product question
   embedded, classify as NO_DOCS_IN_SCOPE. If purely competitor comparison with no
   Gupshup angle, classify OUT_OF_SCOPE.

### Video & demo content (check BEFORE calling NO_DOCS_IN_SCOPE for demo/walkthrough queries)
The skill has a video manifest at kb/video_manifest.json covering 18 product topics:
  Gupshup Console Overview, Message Templates, Campaign Manager, Bot Studio Journey,
  Agent Assist Overview, Click-to-WhatsApp Ads (CTX), Personalize Module,
  Analytics Dashboard, SuperAgent Overview, WhatsApp Flows, Bot Studio Journey Analytics,
  AI Admin Agentic AI Journeys, Goals in Bot Studio, Agent Assist Analytics,
  Agent Assist Settings, Enterprise WhatsApp Extension, Enterprise SMS Extension, RCS Extension.
If a query asks for a "demo", "walkthrough", "show me how", "overview video", "how does X work"
AND a matching video exists → bucket=HAS_DOCS_FAILS, root_cause=routing_miss,
matching_doc=kb/video_manifest.json. Do NOT create a new doc for demo/video queries.

### Consulting mode (check BEFORE calling NO_DOCS_IN_SCOPE for build/architecture queries)
The skill has consulting-mode docs at:
  kb/bot-studio/consulting-conditional-branching.md
  kb/bot-studio/consulting-loop-prevention.md
  kb/bot-studio/consulting-when-to-build.md
Queries like "how do I build X", "when should I use X vs Y", "what approach for X",
"prevent infinite loops" are answered by consulting docs.
If such a query IDKed → bucket=HAS_DOCS_FAILS, root_cause=routing_miss. Do NOT create new docs.

### Bot Studio variable/API/database docs (already exist — verify before NO_DOCS_IN_SCOPE)
  kb/bot-studio/manage-variables.md — storing user input in variables
  kb/bot-studio/api-node.md — calling external APIs/databases from bots
  kb/bot-studio/manage-api.md — managing API configurations
A FALSE-POSITIVE RETRIEVAL flag means the LIVE skill retrieved the WRONG doc — NOT
that no doc exists. If the topic is covered by a different existing doc, classify
HAS_DOCS_FAILS with root_cause=routing_miss, NOT NO_DOCS_IN_SCOPE.
"""

# ---------------------------------------------------------------------------
# Deployed fixes log
# ---------------------------------------------------------------------------

_DEPLOYED_FIXES_PATH = Path(__file__).resolve().parents[1] / "deployed_fixes.json"


def _load_deployed_fixes_data() -> list:
    """Return raw list of fix entries from deployed_fixes.json."""
    try:
        with open(_DEPLOYED_FIXES_PATH) as f:
            return json.load(f).get("fixes", [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _load_deployed_fixes() -> str:
    """Load deployed_fixes.json and format as a prompt section for the judge.

    Returns a string ready for injection into Turn 1 prompt. The judge uses
    this to avoid re-flagging gaps that are already fixed in production — the
    old trace data still shows failures even after a fix ships.
    """
    try:
        with open(_DEPLOYED_FIXES_PATH) as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return ""

    fixes = data.get("fixes", [])
    if not fixes:
        return ""

    lines = ["## ⚠ Already-Deployed Fixes — DO NOT re-flag these as new gaps"]
    lines.append(
        "The following gaps have ALREADY been fixed in skill/kb_answer.py and deployed.\n"
        "Historical traces still show failures (the fix ships after the trace), so you WILL\n"
        "see old IDK results for these queries. IGNORE them — they are not new gaps.\n"
        "Only flag a gap as Fix Now if it DIFFERS from the queries listed below.\n"
    )
    for fix in fixes:
        if not fix.get("queries_fixed"):
            # revert/no-fix entries — still useful context
            lines.append(
                f"- [{fix['fix_id']}] {fix['gap_signature']}: {fix['description']}"
                + (f" (NOTE: {fix['note']})" if fix.get("note") else "")
            )
            continue
        queries_str = "; ".join(f'"{q[:80]}"' for q in fix["queries_fixed"])
        lines.append(
            f"- [{fix['fix_id']} {fix['deployed_at']}] {fix['gap_signature']}: "
            f"{fix['description']}\n"
            f"  Fixed queries: {queries_str}"
        )
    return "\n".join(lines)


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
    stderr = proc.stderr.decode(errors="replace")
    sid = session_id
    # session_id may appear in stdout OR stderr depending on hermes version
    for line in (stdout + "\n" + stderr).splitlines():
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
        # Filter inventory to gap module + general — full inventory is ~26k tokens and causes timeouts
        kb_inventory = self.judge._build_kb_inventory(module_filter=gap.module)
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
            if top_score > 0.35:
                kb_search_section += "\nNOTE: High-scoring docs found — PREFER HAS_DOCS_FAILS. Only call NO_DOCS_IN_SCOPE if you can prove the doc doesn't cover the queries."
            elif top_score > 0.2:
                kb_search_section += "\nNOTE: Medium-scoring docs found — check if keyword/routing fix would work before calling NO_DOCS_IN_SCOPE."
            else:
                kb_search_section += "\nNOTE: No strong KB matches — NO_DOCS_IN_SCOPE likely correct."
        else:
            kb_search_section += "  (No results — kb_chunks.jsonl unavailable or no token overlap found)\n"
            kb_search_section += "\nNOTE: No strong KB matches found — NO_DOCS_IN_SCOPE likely correct."

        json_schema = json.dumps({
            "bucket": "HAS_DOCS_FAILS | NO_DOCS_IN_SCOPE | OUT_OF_SCOPE | NOISE",
            "confidence": "high | medium | low",
            "reasoning": "paragraph referencing specific query results and doc evidence",
            "matching_doc": "kb/path/to/doc.md or null",
            "root_cause": "keyword_gap | routing_miss | retrieval_rank | content_thin | answer_quality | null",
            "doc_evidence": "REQUIRED for HAS_DOCS_FAILS: direct quote from matching_doc proving it covers the query. null for other buckets.",
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

{_SKILL_CONTEXT_PREAMBLE}

## Your Task
Classify this gap into ONE bucket. Evaluate in this order:

  OUT_OF_SCOPE     — Not a Gupshup product question, pricing/billing, general knowledge,
                     or most queries already ANSWERED.
  NOISE            — Malformed, too short, test traffic.
  HAS_DOCS_FAILS   — A relevant KB doc exists but the skill IDKed (keyword/routing miss).
                     PREFER this over NO_DOCS_IN_SCOPE — it's a faster fix.
  NO_DOCS_IN_SCOPE — Legitimate question, no existing doc covers it even with routing.
                     Only use this if HAS_DOCS_FAILS is genuinely impossible.

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
- HAS_DOCS_FAILS ONLY if: (a) query is IDK AND (b) a doc COVERS the topic AND (c) doc is NOT marked ⚠ NOT INGESTED
- ⚠ NOT INGESTED docs → skill cannot retrieve them → do NOT recommend routing to them → use NO_DOCS_IN_SCOPE
- If ⚠ FALSE-POSITIVE RETRIEVAL appears → doc doesn't cover it → look for another doc or NO_DOCS_IN_SCOPE
- If most queries show [ANSWERED] → gap is not real → OUT_OF_SCOPE
- For HAS_DOCS_FAILS: REQUIRED — provide doc_evidence: a direct quote from the matching doc
  that proves it covers the query. If you cannot quote it, you cannot call HAS_DOCS_FAILS.

## Additional rules

### Rule 1 — Each query is independent (no bundling)
A gap may contain queries that need DIFFERENT verdicts. Classify EACH query on its own:
- If query A has a doc that covers it AND query B does not → query A = HAS_DOCS_FAILS, query B = NO_DOCS_IN_SCOPE.
- Do NOT force all queries into one bucket to produce a single recommendation.
- If the queries map to 3 different topics, say so. The final bucket should reflect the MAJORITY of IDK queries, and per_query_notes must call out every outlier.

### Rule 2 — Identify the CONCEPT_REGISTRY concept, not just the doc
Keywords attach to CONCEPT_REGISTRY concepts, not to markdown files directly. For HAS_DOCS_FAILS:
- Name the concept (e.g., `whatsapp_templates`, `custom_integrations`) whose `source_boosts` already includes or should include the target doc.
- If NO existing concept boosts the target doc, the fix is CREATE a new concept — say so explicitly.
- Do NOT recommend keyword additions without naming the concept target.
- If you can't identify a concept target, HAS_DOCS_FAILS is not valid → use NO_DOCS_IN_SCOPE instead.

### Rule 3 — root_cause=routing_miss requires the doc to COVER the topic
routing_miss is only valid if the doc CONTAINS the answer. Checklist:
- Quote a passage that answers the query. If you cannot quote it → it's a content gap (NO_DOCS_IN_SCOPE), NOT routing_miss.
- If the doc only covers a related topic area but not the specific question → NO_DOCS_IN_SCOPE.
- matching_doc="?" is never valid for HAS_DOCS_FAILS. If you don't know which doc covers it → NO_DOCS_IN_SCOPE.

### Rule 4 — Pricing / sales / internal-process queries → always OUT_OF_SCOPE
Do not recommend keyword fixes for:
- Pricing, billing, cost, volume discounts, deal desk, discount approval processes
- Internal processes (deal approval, BSUID, token cost definitions for sales)
- Queries about contacting support / account registration WITHOUT a product context
These are sales signals / by-design IDK. Keyword patching cannot substitute for a sales response.

### Rule 5 — Reject generic keywords that would pollute multiple concepts
Before adding a keyword, ask: would this term match unrelated queries?
- Single generic words (`callbacks`, `logs`, `testing`, `payments`) → REJECT — too broad.
- Full sentences verbatim from queries → REJECT — no user types them exactly that way.
- Terms already present in another concept's aliases → REJECT — would create routing conflicts.
- Valid keywords are: specific product terms, error message substrings, feature names the user typed.

### Rule 6 — Never recommend non-English keywords
SuperAgent normalises and translates ALL queries before they reach kb_answer. The skill only sees
English text. Adding Portuguese, Spanish, Hindi, or any other language keywords to CONCEPT_REGISTRY
is always wrong — they will NEVER be matched because routing happens on the translated query.
- If a failing query is in Portuguese/Spanish/Hindi/etc.: the language is NOT the root cause.
- Diagnose what the English translation would be, then check if the English keyword/doc is missing.
- The correct fix type for non-English IDKs is one of: content_thin (doc exists but lacks depth),
  routing_miss (English keyword missing from the concept), or NO_DOCS_IN_SCOPE (no doc at all).
- Do NOT include any non-English strings in keywords_to_add.

Think step by step. Analyze each IDK query individually. Name the specific docs and concept targets."""

        sid, t1_out = _hermes_turn(t1_prompt, None, timeout_per_turn)
        if not sid:
            # Retry once before giving up — transient hermes failures are common
            logger.warning("  worker[%s] turn 1 failed, retrying once", task_id)
            sid, t1_out = _hermes_turn(t1_prompt, None, timeout_per_turn)
        if not sid:
            logger.error("  worker[%s] turn 1 failed after retry — marking DEGRADED (no single-shot fallback)", task_id)
            return {**_DEGRADED, "reasoning": "turn 1 failed after retry"}

        logger.debug("  worker[%s] turn 1 complete (session=%s)", task_id, sid)

        # ── Turn 2: Adversarial Challenge ────────────────────────────────────
        t2_prompt = f"""Challenge your Turn 1 analysis. Be adversarial.

FIRST: Could an existing KB doc answer these queries with better keywords/routing?
Keyword fixes are faster than creating new docs. Only call NO_DOCS_IN_SCOPE if
you can prove NO existing doc covers the topic even with routing improvements.

1. If NO_DOCS_IN_SCOPE: re-scan KB inventory. Any file with matching section headings?
   Even a medium-scoring KB search result (0.2+) → try HAS_DOCS_FAILS instead.
   But SKIP any file marked ⚠ NOT INGESTED — the skill cannot retrieve it.
2. If HAS_DOCS_FAILS:
   a. Is matching_doc marked ⚠ NOT INGESTED? If yes → switch to NO_DOCS_IN_SCOPE.
   b. Check for ⚠ FALSE-POSITIVE RETRIEVAL flags. If present AND no other doc covers it
      → switch to NO_DOCS_IN_SCOPE.
   c. Can you quote a passage from the doc that answers the query? If not → NO_DOCS_IN_SCOPE.
   d. Does the doc contain the SPECIFIC answer (not just the topic area)? If not → NO_DOCS_IN_SCOPE.
   e. Does an existing CONCEPT_REGISTRY concept already boost this doc? If yes, root cause is scoring/floor, not missing aliases.
   f. Did you name the CONCEPT_REGISTRY concept to add keywords to? If not → the recommendation is incomplete; identify it or switch to NO_DOCS_IN_SCOPE.
   g. Are the proposed keywords specific (exact product terms / error substrings) or generic (single common words, full sentences)? Generic keywords → reject them and find specific ones.
3b. If HAS_DOCS_FAILS with multiple queries: re-check each query independently. Are 2+ queries actually about DIFFERENT topics? If yes → the gap is bundled incorrectly → split per_query_notes clearly and mark the outlier queries as NO_DOCS_IN_SCOPE or OUT_OF_SCOPE.
3. If OUT_OF_SCOPE: are any IDK queries genuinely about a Gupshup product?
4. ANSWERED queries do not count as failures.
5. PRICING queries → always OUT_OF_SCOPE (sales signal, never create pricing docs).
6. Demo/video queries → check kb/video_manifest.json (18 topics) → HAS_DOCS_FAILS if match.
7. General knowledge, infrastructure alerts, off-topic → OUT_OF_SCOPE.
8. Bot Studio DB/variable queries: manage-variables.md + api-node.md may cover them.
   ⚠ FALSE-POSITIVE = wrong doc retrieved, not missing doc.

State final verdict with one bucket and your evidence."""

        sid, t2_out = _hermes_turn(t2_prompt, sid, timeout_per_turn)
        if not sid:
            logger.warning("  worker[%s] turn 2 failed, retrying once", task_id)
            sid, t2_out = _hermes_turn(t2_prompt, sid, timeout_per_turn)
        if not sid:
            logger.error("  worker[%s] turn 2 failed after retry — marking DEGRADED", task_id)
            return {**_DEGRADED, "reasoning": "turn 2 failed after retry"}

        logger.debug("  worker[%s] turn 2 complete", task_id)

        # ── Turn 3: Final Verdict → JSON ─────────────────────────────────────
        t3_prompt = f"""Based on your analysis and challenge, produce the final verdict.

Requirements:
- keywords_to_add (if HAS_DOCS_FAILS): EXACT terms lifted from the IDK query text itself
  (substring-matchable). Non-English queries: include same-language terms.
  REJECT: single generic words, full verbatim query sentences, terms already in another concept's aliases.
- concept_target: name the CONCEPT_REGISTRY concept to add keywords to (e.g., "whatsapp_templates").
  If no existing concept boosts the target doc → write "NEW: <suggested_concept_name>".
  If you cannot identify a concept target → you MUST use NO_DOCS_IN_SCOPE, not HAS_DOCS_FAILS.
- root_cause: only use routing_miss if you can quote the doc passage that answers the query.
  If the doc covers the topic area but not the specific question → use content_thin or null.
- per_query_notes: one line per query — if queries need different buckets, say so explicitly.
- reasoning: reference specific query results and doc evidence from the pipeline signal.

Write ONLY valid JSON to the file: {output_path}
Schema:
{json_schema}

No prose, no markdown fences. Only JSON."""

        sid, t3_out = _hermes_turn(t3_prompt, sid, timeout_per_turn)
        if not sid:
            logger.warning("  worker[%s] turn 3 failed, retrying once", task_id)
            sid, t3_out = _hermes_turn(t3_prompt, sid, timeout_per_turn)
        if not sid:
            logger.error("  worker[%s] turn 3 failed after retry — marking DEGRADED", task_id)
            return {**_DEGRADED, "reasoning": "turn 3 failed after retry"}

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
        """Fallback: single hermes -z call if conv turns fail.

        Hermes writes to stdout, not files — capture stdout and write the file ourselves.
        """
        logger.info("  worker[%s] single-shot fallback for %s", task_id, gap_key)
        prompt = f"{context_prompt}\n\nRespond with ONLY valid JSON matching this schema. No prose, no markdown fences:\n{json_schema}"
        stdout = _hermes_single(prompt, timeout=300)
        if stdout.strip():
            text = stdout.strip()
            # Strip markdown fences
            if text.startswith("```"):
                text = "\n".join(
                    ln for ln in text.splitlines()
                    if not ln.startswith("```")
                ).strip()
            # Extract first {...} JSON object — handles prose before/after JSON
            import re as _re
            m = _re.search(r'\{.*\}', text, _re.DOTALL)
            if m:
                text = m.group(0)
            # Write to the expected output file so _parse_output can read it
            try:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                Path(output_path).write_text(text, encoding="utf-8")
                logger.info("  worker[%s] single-shot wrote %d bytes to %s", task_id, len(text), output_path)
            except Exception as exc:
                logger.warning("  worker[%s] failed to write single-shot output: %s", task_id, exc)
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

        four_bucket_verdicts: Dict[str, Any] = {}

        # 1. Pre-filter already-fixed gaps before sending to workers
        deployed_fixes = _load_deployed_fixes_data()
        fixed_signatures = {f["gap_signature"] for f in deployed_fixes if f.get("queries_fixed")}
        fixed_queries: set = set()
        for f in deployed_fixes:
            for q in f.get("queries_fixed", []):
                fixed_queries.add(q[:60].lower())  # prefix match

        def _gap_is_already_fixed(gap) -> bool:
            gap_key = f"{gap.module}/{gap.intent}"
            if gap_key in fixed_signatures:
                # Only skip if ALL failing queries are covered by the fix
                gap_qs = {(q or "")[:60].lower() for q in (gap.failure_examples or [])}
                if gap_qs and gap_qs.issubset(fixed_queries):
                    return True
            return False

        gaps_pre_fixed = [g for g in gaps if _gap_is_already_fixed(g)]
        for g in gaps_pre_fixed:
            gap_key = f"{g.module}/{g.intent}"
            four_bucket_verdicts[gap_key] = {
                **_DEGRADED,
                "bucket": "OUT_OF_SCOPE",
                "confidence": "high",
                "reasoning": "Pre-filtered: all failing queries already fixed per deployed_fixes.json",
                "degraded": False,
            }
            logger.info("  coordinator: pre-filtered already-fixed gap: %s", gap_key)

        gaps = [g for g in gaps if not _gap_is_already_fixed(g)]

        # 2. Post all gaps to kanban and record task IDs (skip pre-classified)
        gaps_to_judge = [g for g in gaps if not g.pre_classified_bucket]
        skipped = len(gaps) - len(gaps_to_judge)
        if skipped:
            logger.info("  coordinator: skipping %d pre-classified gaps (pricing/coexistence)", skipped)
        logger.info("  coordinator: posting %d gaps to kanban board", len(gaps_to_judge))
        self.kanban.clear_board()
        task_ids: Dict[str, str] = {}  # gap_key -> task_id
        for idx, gap in enumerate(gaps_to_judge):
            old_key = f"Gap #{idx + 1}"
            classification = classifications.get(old_key, {})
            task_id = self._post_gap_task(idx + 1, gap, classification)
            if task_id:
                gap_key = f"{gap.module}/{gap.intent}"
                task_ids[gap_key] = task_id
                logger.info("  coordinator: posted %s → task %s", gap_key, task_id)

        # 2. Fan out workers in parallel
        logger.info("  coordinator: spinning up %d workers (max_workers=%d)",
                    len(gaps_to_judge), max_workers)

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            future_to_gap: dict = {}
            for idx, gap in enumerate(gaps_to_judge):
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
