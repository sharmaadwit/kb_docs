"""Hermes-backed LLM judge for hard/ambiguous KB-gap classification.

Mirrors the proven pattern in the sibling "hermes" project's
`hermes_runner.py::run_hermes_z()`: shell out to the `hermes` CLI, ask it to
write a JSON verdict to a scratch file, read that file back, and validate it.

Key differences from `hermes_runner.py` (documented, not accidental):
  - Synchronous, not async. `local/supervisor/` is a plain sequential script
    (see qwen_interface.py's plain `requests.post` calls) -- there is no
    asyncio event loop running here, so this module uses `subprocess.run`
    with a timeout instead of `asyncio.create_subprocess_exec` +
    `asyncio.wait_for`.
  - No LLM-API fallback. `hermes_runner.py` falls back to a direct
    `requests.post` against a Qwen proxy when the hermes binary/subprocess
    fails. This judge call is an *optional* refinement on top of an already
    -computed deterministic classification (see `judge_gap`'s docstring) --
    there is no equivalent "make sure we always get an answer" requirement,
    so on any failure this returns a well-defined degraded-mode dict instead
    of silently calling out to a second LLM backend. This also means one
    fewer network dependency for local dev tooling.
  - `is_hermes_available()` is a new module-level helper (not present in
    hermes_runner.py) so `supervisor_agent.py` can check once per run instead
    of once per gap.
  - `-p kb-supervisor` profile flag: locks the judge to the local Qwen proxy
    instead of the default Hermes profile (which may point to Claude/OpenRouter).
  - CONCEPT_REGISTRY context: the prompt now includes the full current-state
    source_boosts for the matched entity so Qwen can propose concrete numeric
    boost changes (e.g. raise agent-transfer-node 5→7, add penalty -5.0 on
    superagent/concepts/agents). This context is regenerated from the live
    CONCEPT_REGISTRY at call time, so it always reflects post-code-change state.
"""

import json
import logging
import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

_REQUIRED_KEYS = {
    "root_cause": str,
    "confidence": (int, float),
    "reasoning": str,
    "suggested_next_step": str,
}

_VALID_ROOT_CAUSES = {
    "wrong_source_doc",   # entity matched but answer from wrong KB file → boost/penalty fix
    "missing_boost",      # correct doc exists but not boosted enough
    "code_bug",           # retrieval/composition logic bug (not a config fix)
    "missing_kb_content", # no doc covers this topic
    "out_of_scope",       # pricing / account-support / not our KB
    "insufficient_evidence",  # can't tell from the case alone
}

_PROFILE = "kb-supervisor"


def _semantic_relevance_check(query: str, answer_snippet: str, source: str, timeout: int = 30) -> bool:
    """Ask Hermes whether the answer snippet actually addresses the query topic.

    Returns True if the snippet is topically relevant to the query, False otherwise.
    Falls back to False (conservative) on any error — prevents cross-domain keyword
    matches from being treated as valid content, which is the dominant failure mode.
    """
    hermes_bin = shutil.which("hermes")
    if hermes_bin is None:
        return False  # degraded: assume NOT relevant — conservative prevents false any_content=True

    snippet_trunc = answer_snippet[:500].replace('"', "'")
    query_trunc = query[:200].replace('"', "'")

    _REPO_ROOT = Path(__file__).resolve().parents[3]
    out_dir = _REPO_ROOT / "local" / "supervisor" / "judge_outputs" / f"sem_{int(time.time())}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = str(out_dir / "relevance.json")

    prompt = (
        "You are a relevance checker. Given a user query and a KB document snippet, "
        "decide whether the snippet actually addresses the query's specific topic.\n\n"
        f"Query: \"{query_trunc}\"\n\n"
        f"Document: {source}\n"
        f"Snippet: \"{snippet_trunc}\"\n\n"
        "A snippet is RELEVANT if it contains information that would help answer this specific query.\n"
        "A snippet is NOT RELEVANT if it merely shares keywords but covers a different topic "
        "(e.g. query is about coexistence eligibility, snippet is about pricing).\n\n"
        f'Write ONLY a valid JSON object to the file at: {out_path}\n'
        'Format: {"relevant": true} or {"relevant": false}'
    )

    env = {**os.environ, "PATH": f"/Users/adwit.sharma/.local/bin:{os.environ.get('PATH', '')}"}

    try:
        proc = subprocess.run(
            ["hermes", "-p", _PROFILE, "-z", prompt, "--yolo"],
            timeout=timeout,
            capture_output=True,
            env=env,
        )
        if proc.returncode != 0:
            return False  # degraded: conservative
        with open(out_path, "r", encoding="utf-8") as fh:
            data = json.loads(fh.read())
        return bool(data.get("relevant", False))
    except Exception as exc:
        logger.debug("_semantic_relevance_check failed: %s", exc)
        return False  # degraded: assume NOT relevant


def is_hermes_available() -> bool:
    """Check once whether the `hermes` binary is on PATH."""
    return shutil.which("hermes") is not None


def _degraded(reason: str) -> Dict[str, Any]:
    return {
        "root_cause": "unknown",
        "confidence": 0.0,
        "reasoning": f"Hermes judge unavailable: {reason}",
        "suggested_next_step": "Re-run once Hermes is available",
        "proposed_boost_changes": {},
        "degraded": True,
    }


def _get_concept_context(entity_id: str, bridge) -> Dict[str, Any]:
    """Pull the live CONCEPT_REGISTRY entry for entity_id for Qwen context."""
    if bridge is None:
        return {}
    try:
        import kb
        for entry in kb.CONCEPT_REGISTRY:
            if entry.get("id") == entity_id:
                return {
                    "id": entry["id"],
                    "aliases": entry.get("aliases", []),
                    "source_boosts": entry.get("source_boosts", {}),
                    "module": entry.get("module", ""),
                }
    except Exception:
        pass
    # fallback: just use bridge's source_boosts lookup
    boosts = bridge.get_concept_source_boosts(entity_id) if bridge else {}
    return {"id": entity_id, "source_boosts": boosts}


def _alias_format_rules() -> str:
    """Strict alias format rules injected into every prompt that asks for aliases."""
    return (
        "## ALIAS FORMAT RULES — strictly enforced\n"
        "1. Each alias must be 2-6 words. Aliases longer than 6 words are AUTOMATICALLY REJECTED.\n"
        "2. All lowercase, no punctuation (no question marks, commas, colons, slashes, etc.).\n"
        "3. Each alias must be a CONCEPT LABEL — a short keyword phrase that names the TOPIC,\n"
        "   NOT a restatement or paraphrase of the user's question.\n"
        "   Ask yourself: 'What TOPIC is the user asking about?' — write that topic as a noun phrase.\n"
        '   Wrong: "how do I register my account for SMS sending"  ← paraphrase of query, 9 words, rejected\n'
        '   Wrong: "registering an account to enable SMS message delivery"  ← still a sentence fragment, rejected\n'
        '   Right: "sms account registration"\n'
        '   Right: "sms sender registration"\n'
        "4. Producing a sentence paraphrase is a format error equivalent to exceeding 6 words — it will be rejected.\n"
        "5. Language: always English, even when failing queries are in Portuguese, Spanish, or Arabic.\n"
        "6. Do not include filler words: 'how', 'what', 'when', 'does', 'can I', 'is there a'."
    )


def _taxonomy_block(gap_module: str = "", bridge=None) -> str:
    """Build taxonomy from live CONCEPT_REGISTRY.

    For the gap's own module (and any near-miss modules), include 3-5 sample
    aliases per concept so the judge can tell what each concept already covers.
    All other modules show concept IDs only.
    """
    registry = None
    try:
        # bridge.kb is the live kb_answer module loaded by SkillPipelineBridge
        if bridge is not None:
            registry = bridge.kb.CONCEPT_REGISTRY
    except Exception:
        pass
    if registry is None:
        return "## CONCEPT_REGISTRY unavailable"

    # Group by module
    by_module: Dict[str, list] = {}
    for entry in registry:
        mod = entry.get("module", "Unknown")
        by_module.setdefault(mod, []).append(entry)

    # Modules to show with aliases (gap module + frequently confused ones)
    detail_modules = {gap_module, "Overview", "General"}

    lines = [
        "## Existing CONCEPT_REGISTRY concepts (live)",
        "Concepts marked with aliases show what each concept currently covers.",
        "BEFORE proposing a new concept, verify your proposed_concept_id does NOT",
        "duplicate or near-duplicate any concept listed below. If a close match",
        "exists, your verdict MUST be alias_candidate on that existing concept —",
        "never missing_concept. Name the closest existing concept in your reasoning.",
        "",
    ]
    for mod in sorted(by_module.keys()):
        entries = by_module[mod]
        lines.append(f"\n{mod}:")
        for e in entries:
            cid = e.get("id", "?")
            if mod in detail_modules:
                aliases = e.get("aliases", [])[:5]
                alias_str = ", ".join(f'"{a}"' for a in aliases)
                lines.append(f"  {cid} — aliases: {alias_str}")
            else:
                lines.append(f"  {cid}")
    return "\n".join(lines)


def _content_availability_block(failure_examples: List[str], bridge) -> str:
    """Run up to 3 sample queries through BM25 and report best-matching doc scores.

    Injected into the prompt so the judge can distinguish:
      - content exists, concept missing → missing_concept
      - no content matches → idk_correct (concept cannot fix a content gap)
    """
    if bridge is None or not failure_examples:
        return ""

    # Cross-domain doc families that must never be treated as content for other domains
    _CROSS_DOMAIN_PATTERNS = (
        "pricing", "billing", "promotional-restrictions", "account-support",
    )

    lines = [
        "## KB content availability (computed — trust this)",
        "These are the best-matching KB docs for the sample failing queries,",
        "scored by the real BM25 retrieval pipeline BEFORE any concept boost.",
        "A score ≤ 3.5 means no meaningful KB content exists for that query.",
        "",
        "KEY RULE: A CONCEPT_REGISTRY entry is a retrieval router, not content.",
        "Adding a concept/alias only helps if a KB doc ALREADY answers the question.",
        "If no doc scores above ~3.5, there is no content to route to — the correct",
        "verdict is idk_correct, NOT missing_concept.",
        "(Evidence from past fix 3d804b23: MFA aliases were added but IDK persisted",
        "because no MFA content exists in the KB. Aliases alone cannot fill a content gap.)",
        "",
    ]

    samples = failure_examples[:3]
    any_content = False
    for query in samples:
        try:
            result = bridge.run_query(query)
            top_score = result.get("top_score", 0)
            sources = result.get("evidence_sources", [])
            top_src = sources[0] if sources else "none"
            answer_snippet = result.get("answer", "")
            q_short = query[:80] + ("…" if len(query) > 80 else "")

            if top_score > 3.5:
                # P1-C: hard cross-domain pre-check — pricing/billing docs never count as
                # content for non-pricing queries regardless of BM25 score
                cross_domain = any(pat in top_src.lower() for pat in _CROSS_DOMAIN_PATTERNS)
                if cross_domain:
                    lines.append(f"  Query: \"{q_short}\"")
                    lines.append(
                        f"  Best doc: {top_src} (score: {top_score}) "
                        f"✗ cross-domain mismatch — pricing/billing doc matched non-pricing query"
                    )
                else:
                    # Semantic check: does the top doc actually address this query?
                    relevant = _semantic_relevance_check(query, answer_snippet, top_src)
                    if relevant:
                        any_content = True
                        lines.append(f"  Query: \"{q_short}\"")
                        lines.append(f"  Best doc: {top_src} (score: {top_score}) ✓ semantically relevant")
                    else:
                        lines.append(f"  Query: \"{q_short}\"")
                        lines.append(
                            f"  Best doc: {top_src} (score: {top_score}) "
                            f"✗ NOT relevant — doc covers a different topic"
                        )
            else:
                lines.append(f"  Query: \"{q_short}\"")
                lines.append(f"  Best doc: {top_src} (score: {top_score})")
            lines.append("")
        except Exception as exc:
            logger.debug("content_availability_block: run_query failed: %s", exc)

    if not any_content:
        lines.append(
            "⚠ No query scored above 3.5 (or all high-scoring docs are cross-domain/irrelevant) "
            "— no KB content currently covers this gap."
        )
        lines.append(
            "   Use idk_correct unless you have strong evidence a KB doc should be authored."
        )
        lines.append('   → Set "kb_doc_needed": true in your output.')
    else:
        lines.append(
            "✓ At least one query found matching KB content (score > 3.5, semantically relevant) "
            "— content EXISTS in the KB."
        )
        lines.append(
            "   Adding a concept will ROUTE queries to the existing doc. "
            "No new KB doc is needed."
        )
        lines.append('   → Set "kb_doc_needed": false in your output.')
    return "\n".join(lines)


def _decision_log_block() -> str:
    """Load past human-approved fix decisions with before/after trace proof."""
    log_path = Path(__file__).resolve().parents[1] / "context" / "decision_log.json"
    try:
        with open(log_path, "r", encoding="utf-8") as fh:
            entries = json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return ""

    lines = [
        "## Past human-approved fixes (calibration examples)",
        "These are real gaps that were identified, fixed, and verified via production traces.",
        "Use them to calibrate your verdict — especially on how many concepts to propose.",
        "",
    ]
    for e in entries:
        lines.append(f"### [{e['sha']}] {e['date']} — {e['fix_type']}")
        lines.append(f"Gap: {e['gap_description']}")
        lines.append(f"Module: {e['gap_module']}")
        lines.append(f"Fix applied: {e['fix_detail']}")
        lines.append(f"Key lesson: {e['key_lesson']}")
        if e.get("proof"):
            p = e["proof"]
            lines.append(f"Before fix: {p.get('before_answer_rate', '')} | {p.get('example_before_failure', '')}")
            lines.append(f"After fix:  {p.get('after_answer_rate', '')} | {p.get('example_after_success', '')}")
        lines.append("")
    return "\n".join(lines)


def _build_prompt(gap_summary: Dict[str, Any], output_path: str, bridge=None) -> str:
    """Build a gap-type-aware prompt including live CONCEPT_REGISTRY context."""
    det = (gap_summary.get("deterministic_classification") or "").upper()
    entities_matched = gap_summary.get("entities_matched") or []

    # Route by deterministic_classification first — entity presence alone is not
    # sufficient because NEEDS_INVESTIGATION gaps always have entities matched.
    if "NEEDS_INVESTIGATION" in det or "INVESTIGATION" in det:
        gap_type = "needs_investigation"
    elif "ALIAS" in det:
        gap_type = "alias_candidate"
    elif "NO_CONCEPT" in det or "MISSING" in det:
        gap_type = "needs_investigation"
    elif "WRONG_SOURCE" in det or "BOOST" in det:
        gap_type = "wrong_source_doc"
    elif entities_matched:
        # Fallback: entity matched but no clear classification → alias_candidate
        gap_type = "alias_candidate"
    else:
        gap_type = "wrong_source_doc"

    # Pass up to 5 failure examples — enough to detect mixed-signal gaps
    gap_summary_trimmed = dict(gap_summary)
    if gap_summary_trimmed.get("failure_examples"):
        gap_summary_trimmed["failure_examples"] = gap_summary_trimmed["failure_examples"][:5]
    gap_json = json.dumps(gap_summary_trimmed, indent=2, default=str)

    decision_log = _decision_log_block()
    gap_module = gap_summary.get("module", "")
    failure_examples = gap_summary_trimmed.get("failure_examples", [])

    # ── 1. ALIAS CANDIDATE ───────────────────────────────────────────────────
    if gap_type == "alias_candidate":
        entity_id = entities_matched[0] if entities_matched else None
        concept_ctx = _get_concept_context(entity_id, bridge) if entity_id else {}

        framing = (
            "You are a senior engineer reviewing a KB-gap case for a customer-support "
            "knowledge-base retrieval system. The deterministic classifier flagged a "
            "CONCEPT_REGISTRY near-miss for the failing queries — a concept whose keyword "
            "list had exactly 1 hit against the query.\n\n"
            "CRITICAL FIRST STEP — evaluate whether the near-miss is meaningful:\n"
            "  • Look at 'near_miss_concepts' in the gap case and the matched_keywords.\n"
            "  • If the matched keyword is generic (e.g. 'api', 'whatsapp', 'message', "
            "'available', 'setup') and the failing queries are clearly about a DIFFERENT topic "
            "than what the concept covers, this is a FALSE near-miss — noise from keyword overlap.\n"
            "  • FALSE near-miss → set finding_type to 'idk_correct' or 'out_of_scope'. "
            "Do NOT propose aliases for a concept that doesn't match the query topic.\n"
            "  • GENUINE near-miss → the concept genuinely covers the query topic, but the "
            "user's specific phrasing isn't in the alias list. Only then propose new aliases.\n\n"
            "If this IS a genuine near-miss, propose 2-4 SHORT CONCEPT LABELS (2-6 word noun "
            "phrases) that name the topic. These are keyword triggers — topic labels a search "
            "index would use, NOT paraphrases of user sentences.\n\n"
            "IMPORTANT: If you believe IDK is the CORRECT response for these queries — i.e. "
            "the user is asking about something that has no documentation and should not be "
            "documented (e.g. troubleshooting account access, contacting support, VAPT reports, "
            "sales decks, account-specific issues) — set finding_type to \"idk_correct\". "
            "Do NOT force an alias_candidate verdict when IDK is appropriate."
        )

        concept_section = ""
        if concept_ctx:
            concept_section = (
                f"\n## Current CONCEPT_REGISTRY entry for '{entity_id}'\n"
                + json.dumps(concept_ctx, indent=2)
                + "\n"
                "The 'aliases' list above is what CONCEPT_REGISTRY currently has. "
                "Your proposed_aliases must be NEW entries not already in that list."
            )

        alias_rules = _alias_format_rules()
        case = f"## Gap case\n{gap_json}"
        instructions = (
            "Output a JSON object with exactly these keys:\n"
            '  "finding_type": "alias_candidate" — or "idk_correct" if IDK is the correct response\n'
            '  "concept_id": the matched concept id string (from the case), or null if idk_correct\n'
            '  "proposed_aliases": list of 2-4 new alias strings — CONCEPT LABELS ONLY, '
            "2-6 words each, lowercase, no punctuation. Each entry must name a topic "
            '(e.g. "api node timeout", "sms account registration"), NOT paraphrase the user query. '
            "Aliases exceeding 6 words are automatically rejected and count as format errors.\n"
            '  "confidence": float 0-1\n'
            '  "reasoning": 2-4 sentences explaining what TOPIC the failing queries are about '
            "and why the existing aliases missed them (or why IDK is correct)\n"
            '  "ready_for_code_change": true if confidence >= 0.75 and aliases are unambiguous, '
            "else false (always false if idk_correct)\n"
            '  "suggested_next_step": one concrete action sentence\n\n'
            f"Write ONLY a valid JSON object to the file at: {output_path}. "
            "No markdown fences, no prose."
        )
        # alias_rules before decision_log so format rules are top-of-mind
        return "\n\n".join(filter(bool, [framing, alias_rules, decision_log, concept_section, case, instructions]))

    # ── 2. NEEDS INVESTIGATION / MISSING CONCEPT ─────────────────────────────
    if gap_type == "needs_investigation":
        framing = (
            "You are a senior engineer reviewing a KB-gap case for a customer-support "
            "knowledge-base retrieval system built on CONCEPT_REGISTRY concept matching. "
            "The deterministic classifier found NO concept match for the failing queries — "
            "they fell through to pure BM25. Your job: decide whether this gap represents "
            "(a) an alias_candidate (a concept already exists but is missing aliases), "
            "(b) a missing_concept (a genuinely new topic that should be added to "
            "CONCEPT_REGISTRY), (c) out_of_scope (pricing / billing / account-support / "
            "topics deliberately excluded from this KB), or (d) idk_correct (IDK is the "
            "correct behavior — the user is asking about something that has no documentation "
            "and should not be documented). "
            "If you decide missing_concept, propose a concept_id (snake_case, concise), "
            "the correct module from the taxonomy below, and 3-5 seed aliases.\n\n"
            "IMPORTANT: If you believe IDK is the CORRECT response for these queries — i.e. "
            "the user is asking about something that has no documentation and should not be "
            "documented (e.g. troubleshooting account access, contacting support, "
            "account-specific issues) — set finding_type to \"idk_correct\". Do NOT force an "
            "alias_candidate or missing_concept verdict when IDK is appropriate."
        )

        alias_rules = _alias_format_rules()
        taxonomy_section = _taxonomy_block(gap_module, bridge=bridge)
        content_check = _content_availability_block(failure_examples, bridge)
        case = f"## Gap case\n{gap_json}"
        instructions = (
            "Output a JSON object with exactly these keys:\n"
            '  "finding_type": one of "alias_candidate", "missing_concept", "out_of_scope", "idk_correct"\n'
            "    idk_correct = IDK is the correct behavior; no KB content exists and no alias/boost change can fix this\n"
            '  "proposed_concept_id": snake_case concept id string, or null if out_of_scope or idk_correct\n'
            '  "proposed_module": module name from the taxonomy above, or null if out_of_scope or idk_correct\n'
            '  "proposed_aliases": list of 3-5 seed alias strings if missing_concept or '
            "alias_candidate, else []\n"
            '  "confidence": float 0-1\n'
            '  "reasoning": 2-4 sentences explaining the classification and why this is or '
            "is not in scope (or why IDK is correct)\n"
            '  "ready_for_code_change": true if finding_type is missing_concept or '
            "alias_candidate and confidence >= 0.75, else false (always false if idk_correct)\n"
            '  "kb_doc_needed": true ONLY if ALL sample queries score <= 1.0 in the BM25 content check above — '
            "meaning no KB doc currently covers this topic. If ANY query scored > 2.0, set to false: "
            "the content exists and adding the concept will route to it. Do NOT recommend authoring a new doc "
            "just because the query returns IDK — IDK with a high BM25 score means a routing gap, not a content gap.\n"
            '  "suggested_next_step": one concrete action sentence\n'
            '  "additional_concepts": OPTIONAL — include ONLY if the failure examples clearly '
            "represent 2 or more DISTINCT missing topics (not just different phrasings of the same topic). "
            "Each element must be an object with keys: "
            '"proposed_concept_id" (snake_case), "proposed_module" (from taxonomy), '
            '"proposed_aliases" (3-5 strings), "reasoning" (1-2 sentences). '
            "Omit this key (or set to []) if all failures point to a single concept.\n\n"
            f"Write ONLY a valid JSON object to the file at: {output_path}. "
            "No markdown fences, no prose."
        )
        return "\n\n".join(filter(bool, [framing, decision_log, alias_rules, taxonomy_section, content_check, case, instructions]))

    # ── 3. WRONG SOURCE DOC / MISSING BOOST (existing logic) ─────────────────
    entity_id = entities_matched[0] if entities_matched else None
    concept_ctx = _get_concept_context(entity_id, bridge) if entity_id else {}

    framing = (
        "You are a senior engineer reviewing a KB-gap case for a customer-support "
        "knowledge-base retrieval system built on BM25-style scoring with per-concept "
        "source_boosts (positive values promote a source; negative values penalise it). "
        "A deterministic classifier flagged this case as CODE_GAP_NEEDS_INVESTIGATION "
        "because the entity was matched but the answer came from the wrong source document. "
        "Your job: decide the root cause and propose CONCRETE source_boost changes "
        "(numeric deltas on specific source keys) that will fix the misrouting. "
        "Do NOT give generic advice. Reference the exact source keys below.\n\n"
        "IMPORTANT: If you believe IDK is the CORRECT response for these queries — i.e. "
        "the user is asking about something that has no documentation and should not be "
        "documented (e.g. troubleshooting account access, contacting support, "
        "account-specific issues) — set finding_type to \"idk_correct\". Do NOT force an "
        "alias_candidate or missing_concept verdict when IDK is appropriate."
    )

    source_boosts_schema = (
        "## How source_boosts work\n"
        "source_boosts is a dict on each CONCEPT_REGISTRY entry: {source_key: float}.\n"
        "  positive float → boost that source document's BM25 score for this concept\n"
        "  negative float → penalise that source document's score (push it down)\n"
        "The current source_boosts for the matched concept are shown in the concept context below.\n"
        "When the top source is wrong, the fix is usually:\n"
        "  a) raise the boost on the CORRECT source key (or add it if missing)\n"
        "  b) add a NEGATIVE boost (penalty) on the WRONG source key\n"
        "  c) or both\n"
        "Propose the minimum delta needed: e.g. raise agent-transfer-node from 5.0 to 7.0 (+2)\n"
        "and add superagent/concepts/agents: -5.0 (new penalty)."
    )

    concept_section = ""
    if concept_ctx:
        concept_section = (
            f"\n## Current CONCEPT_REGISTRY entry for '{entity_id}'\n"
            + json.dumps(concept_ctx, indent=2)
            + "\n"
        )

    case = f"## Gap case\n{gap_json}"
    instructions = (
        "Respond by writing ONLY a valid JSON object (no markdown fences, no prose) "
        f"to the file at this exact path: {output_path}\n\n"
        "The JSON object must contain exactly these keys:\n"
        '  "root_cause": one of '
        '"wrong_source_doc", "missing_boost", "code_bug", "missing_kb_content", '
        '"out_of_scope", "insufficient_evidence"\n'
        "    OR if IDK is the correct response, use finding_type instead (see below)\n"
        '  "confidence": float 0-1\n'
        '  "reasoning": 2-4 sentences referencing specific source paths and score values from this case\n'
        '  "suggested_next_step": one concrete action sentence\n'
        '  "proposed_boost_changes": a JSON object of {source_key: new_absolute_value} '
        "representing the updated source_boosts dict for this concept after the fix. "
        "Use the CURRENT values from the concept context above as your baseline and apply your proposed deltas. "
        "If the root_cause is not wrong_source_doc or missing_boost, set this to {}.\n\n"
        "SPECIAL CASE — if IDK is the correct response, emit finding_type instead of root_cause:\n"
        '  "finding_type": "idk_correct"\n'
        '  "confidence": float 0-1\n'
        '  "reasoning": why IDK is correct here\n'
        '  "suggested_next_step": "No action needed."\n'
        '  "proposed_boost_changes": {}'
    )
    return "\n\n".join(filter(bool, [framing, source_boosts_schema, concept_section, case, instructions]))


def _validate(raw: Any) -> Dict[str, Any]:
    """Validate parsed JSON. Supports alias_candidate, needs_investigation, and wrong_source_doc paths."""
    if not isinstance(raw, dict):
        raise ValueError(f"hermes output is not a JSON object (got {type(raw).__name__})")

    has_finding_type = "finding_type" in raw
    has_root_cause = "root_cause" in raw

    if not has_finding_type and not has_root_cause:
        raise ValueError(
            "hermes output must contain either 'finding_type' (alias/missing-concept paths) "
            "or 'root_cause' (wrong-source-doc path)"
        )

    # Keys required by all paths
    for key, expected_type in {"confidence": (int, float), "reasoning": str, "suggested_next_step": str}.items():
        if key not in raw:
            raise ValueError(f"hermes output missing required key: {key}")
        if not isinstance(raw[key], expected_type):
            raise ValueError(
                f"hermes output key '{key}' has wrong type "
                f"(expected {expected_type}, got {type(raw[key]).__name__})"
            )

    confidence = float(raw["confidence"])
    if not (0.0 <= confidence <= 1.0):
        raise ValueError(f"hermes output 'confidence' out of range [0,1]: {confidence}")

    # ── alias_candidate / needs_investigation path ───────────────────────────
    if has_finding_type:
        _valid_finding_types = {"alias_candidate", "missing_concept", "out_of_scope", "needs_investigation", "idk_correct"}
        if raw["finding_type"] not in _valid_finding_types:
            raise ValueError(
                f"hermes output 'finding_type' is not valid: {raw['finding_type']!r}. "
                f"Must be one of: {sorted(_valid_finding_types)}"
            )

        proposed_aliases = raw.get("proposed_aliases", [])
        if not isinstance(proposed_aliases, list):
            proposed_aliases = []
        # P3: strip aliases that violate format rules (>6 words or non-string)
        valid_aliases = [a for a in proposed_aliases if isinstance(a, str) and len(a.split()) <= 6]
        stripped = len(proposed_aliases) - len(valid_aliases)
        if stripped:
            logger.info("_validate: stripped %d alias(es) exceeding 6-word limit", stripped)
        proposed_aliases = valid_aliases

        result = {
            "finding_type": raw["finding_type"],
            "confidence": confidence,
            "reasoning": raw["reasoning"],
            "suggested_next_step": raw["suggested_next_step"],
            "proposed_aliases": proposed_aliases,
            "ready_for_code_change": bool(raw.get("ready_for_code_change", False)),
            "kb_doc_needed": bool(raw.get("kb_doc_needed", True)),
            "degraded": False,
        }
        if raw["finding_type"] == "alias_candidate":
            result["concept_id"] = raw.get("concept_id", "")
        if raw["finding_type"] == "missing_concept":
            result["proposed_concept_id"] = raw.get("proposed_concept_id")
            result["proposed_module"] = raw.get("proposed_module")
        # Pass through additional_concepts if present and valid
        additional = raw.get("additional_concepts")
        if isinstance(additional, list) and additional:
            result["additional_concepts"] = [
                c for c in additional
                if isinstance(c, dict) and c.get("proposed_concept_id")
            ]
        return result

    # ── wrong_source_doc / missing_boost path (backward-compat) ─────────────
    if not isinstance(raw["root_cause"], str):
        raise ValueError(
            f"hermes output key 'root_cause' has wrong type "
            f"(expected str, got {type(raw['root_cause']).__name__})"
        )
    if raw["root_cause"] not in _VALID_ROOT_CAUSES:
        raise ValueError(
            f"hermes output 'root_cause' is not a valid category: {raw['root_cause']!r}"
        )

    proposed = raw.get("proposed_boost_changes", {})
    if not isinstance(proposed, dict):
        proposed = {}

    return {
        "root_cause": raw["root_cause"],
        "confidence": confidence,
        "reasoning": raw["reasoning"],
        "suggested_next_step": raw["suggested_next_step"],
        "proposed_boost_changes": proposed,
        "degraded": False,
    }


def _run_conversation_turn(
    prompt: str,
    session_id: str | None,
    env: dict,
    timeout: int,
) -> tuple[str | None, str]:
    """Send one turn to hermes chat and return (new_session_id, stdout_text).

    Uses `hermes chat -Q --oneshot` so it exits after answering.
    Resumes an existing session when session_id is provided.
    Returns (None, "") on any failure.
    """
    cmd = ["hermes", "-p", _PROFILE, "chat", "-Q", "--oneshot", "--yolo"]
    if session_id:
        cmd += ["--resume", session_id]
    cmd += ["-q", prompt]

    try:
        proc = subprocess.run(cmd, timeout=timeout, capture_output=True, env=env)
    except subprocess.TimeoutExpired:
        logger.warning("_run_conversation_turn timed out after %ds", timeout)
        return None, ""
    except Exception as exc:
        logger.warning("_run_conversation_turn subprocess error: %s", exc)
        return None, ""

    if proc.returncode != 0:
        stderr_tail = proc.stderr.decode(errors="replace")[:300] if proc.stderr else ""
        logger.warning("hermes chat turn exited %d: %s", proc.returncode, stderr_tail)
        return None, ""

    stdout = proc.stdout.decode(errors="replace")
    # Extract session_id from "session_id: <id>" line
    new_sid = session_id
    for line in stdout.splitlines():
        if line.startswith("session_id:"):
            new_sid = line.split(":", 1)[1].strip()
            break
    return new_sid, stdout


def _conv_turn1_analysis(gap_summary: Dict[str, Any], bridge=None) -> str:
    """Turn 1: present the raw gap data and ask Qwen to reason aloud — no JSON yet."""
    gap_summary_trimmed = dict(gap_summary)
    if gap_summary_trimmed.get("failure_examples"):
        gap_summary_trimmed["failure_examples"] = gap_summary_trimmed["failure_examples"][:5]
    gap_json = json.dumps(gap_summary_trimmed, indent=2, default=str)

    gap_module = gap_summary.get("module", "")
    failure_examples = gap_summary_trimmed.get("failure_examples", [])

    decision_log = _decision_log_block()
    taxonomy = _taxonomy_block(gap_module, bridge=bridge)
    content_check = _content_availability_block(failure_examples, bridge)

    return "\n\n".join(filter(bool, [
        (
            "You are a senior engineer reviewing a KB-gap case for a customer-support "
            "knowledge-base retrieval system built on CONCEPT_REGISTRY concept matching.\n\n"
            "Read the gap data below carefully. Then reason aloud:\n"
            "1. What topic(s) are the failing queries actually about?\n"
            "2. Does the BM25 content check confirm relevant KB content EXISTS for this topic, "
            "or is this a genuine content gap?\n"
            "   IMPORTANT: A high BM25 score only confirms content exists IF the snippet "
            "topic matches the query topic. If the top doc covers a different subject "
            "(e.g. pricing when the query is about coexistence), content does NOT exist.\n"
            "3. Does an existing concept already cover this, or is a new concept needed?\n"
            "4. Is this in scope for the KB (not pricing / billing / account-support)?\n\n"
            "Do NOT produce JSON yet. Think step by step in plain prose."
        ),
        decision_log,
        taxonomy,
        content_check,
        f"## Gap case\n{gap_json}",
    ]))


def _conv_turn2_proposal(gap_summary: Dict[str, Any]) -> str:
    """Turn 2: based on the analysis, ask for a concrete proposal — still no JSON."""
    gap_module = gap_summary.get("module", "")
    alias_rules = _alias_format_rules()
    return "\n\n".join(filter(bool, [
        (
            "Good. Now based on your analysis above, propose the specific fix:\n\n"
            "- What is the finding_type? "
            "(alias_candidate / missing_concept / out_of_scope / idk_correct)\n"
            "- If missing_concept: what concept_id (snake_case), module, and 3-5 seed aliases?\n"
            "- If alias_candidate: which existing concept_id, and which new aliases?\n"
            "- Is kb_doc_needed true or false? Only true if the BM25 content check confirmed "
            "the top doc does NOT actually cover the query topic (wrong subject matter).\n"
            "- Confidence (0-1)?\n\n"
            "Explain your reasoning for each choice in 2-4 sentences. "
            "Still no JSON — prose only."
        ),
        alias_rules,
    ]))


def _conv_turn3_commit(output_path: str, gap_summary: Dict[str, Any]) -> str:
    """Turn 3: commit the verdict to JSON at output_path."""
    entities_matched = gap_summary.get("entities_matched") or []
    entity_id = entities_matched[0] if entities_matched else None
    return (
        "Now write your final verdict as a JSON object.\n\n"
        "Output a JSON object with exactly these keys:\n"
        '  "finding_type": one of "alias_candidate", "missing_concept", "out_of_scope", "idk_correct"\n'
        '  "proposed_concept_id": snake_case concept id, or null\n'
        '  "proposed_module": module name from the taxonomy, or null\n'
        '  "proposed_aliases": list of 3-5 seed alias strings (2-6 words, lowercase, no punctuation), or []\n'
        '  "concept_id": the matched concept id if alias_candidate, else null\n'
        '  "confidence": float 0-1\n'
        '  "reasoning": 2-4 sentences summarising your analysis above\n'
        '  "ready_for_code_change": true if confidence >= 0.75 and finding is unambiguous, else false\n'
        '  "kb_doc_needed": true only if the BM25 top doc does NOT cover the query topic — '
        "false if a relevant doc exists (even if the query currently returns IDK)\n"
        '  "suggested_next_step": one concrete action sentence\n'
        '  "additional_concepts": [] unless failures clearly cover 2+ distinct topics\n\n'
        f"Write ONLY a valid JSON object to the file at: {output_path}\n"
        "No markdown fences, no prose, no explanation — just the JSON object."
    )


class HermesJudge:
    """Wraps the `hermes` CLI to get an LLM-judged root-cause classification for a KB gap."""

    def __init__(self, bridge=None):
        """
        Args:
            bridge: SkillPipelineBridge instance. If provided, used to fetch live
                    CONCEPT_REGISTRY context for the prompt.
        """
        self._bridge = bridge

    def judge_gap_conversation(self, gap_summary: Dict[str, Any], timeout: int = 120) -> Dict[str, Any]:
        """Multi-turn conversation judge for needs_investigation / missing_concept gaps.

        Turn 1 — Qwen reasons aloud about root cause and content availability.
        Turn 2 — Qwen proposes a specific fix in prose.
        Turn 3 — Qwen commits the verdict as JSON to output_path.

        Falls back to single-shot judge_gap on any conversation failure.
        """
        hermes_bin = shutil.which("hermes")
        if hermes_bin is None:
            return _degraded("hermes binary not found on PATH")

        run_id = f"{os.getpid()}_{int(time.time())}"
        gap_key = "_".join(
            str(gap_summary.get(k, "unknown")) for k in ("module", "intent")
        ).replace("/", "-").replace(" ", "_")[:64]
        _REPO_ROOT = Path(__file__).resolve().parents[3]
        judge_out_dir = _REPO_ROOT / "local" / "supervisor" / "judge_outputs" / run_id
        try:
            judge_out_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return _degraded(f"could not create judge output dir {judge_out_dir}: {e}")
        output_path = str(judge_out_dir / f"{gap_key}.json")
        env = {**os.environ, "PATH": f"/Users/adwit.sharma/.local/bin:{os.environ.get('PATH', '')}"}

        # Turn 1: reason aloud
        t1_prompt = _conv_turn1_analysis(gap_summary, bridge=self._bridge)
        session_id, t1_out = _run_conversation_turn(t1_prompt, None, env, timeout)
        if not session_id:
            logger.warning("conv judge: turn 1 failed — falling back to single-shot")
            return self._single_shot_judge(gap_summary, output_path, env, timeout)
        logger.debug("conv judge turn 1 done, session=%s", session_id)

        # Turn 2: propose fix in prose
        t2_prompt = _conv_turn2_proposal(gap_summary)
        session_id, t2_out = _run_conversation_turn(t2_prompt, session_id, env, timeout)
        if not session_id:
            logger.warning("conv judge: turn 2 failed — falling back to single-shot")
            return self._single_shot_judge(gap_summary, output_path, env, timeout)
        logger.debug("conv judge turn 2 done, session=%s", session_id)

        # Turn 3: commit JSON verdict
        t3_prompt = _conv_turn3_commit(output_path, gap_summary)
        session_id, _ = _run_conversation_turn(t3_prompt, session_id, env, timeout)
        if not session_id:
            logger.warning("conv judge: turn 3 failed — falling back to single-shot")
            return self._single_shot_judge(gap_summary, output_path, env, timeout)
        logger.debug("conv judge turn 3 done, reading verdict from %s", output_path)

        return self._read_and_validate(output_path, gap_summary)

    def _single_shot_judge(
        self, gap_summary: Dict[str, Any], output_path: str, env: dict, timeout: int
    ) -> Dict[str, Any]:
        """Original one-shot path — used as fallback."""
        prompt = _build_prompt(gap_summary, output_path, bridge=self._bridge)
        try:
            proc = subprocess.run(
                ["hermes", "-p", _PROFILE, "-z", prompt, "--yolo"],
                timeout=timeout, capture_output=True, env=env,
            )
        except subprocess.TimeoutExpired:
            self._cleanup(output_path)
            return _degraded(f"subprocess timed out after {timeout}s")
        except Exception as exc:
            self._cleanup(output_path)
            return _degraded(f"subprocess raised an exception: {exc}")
        if proc.returncode != 0:
            self._cleanup(output_path)
            return _degraded(f"hermes exited with non-zero code {proc.returncode}")
        return self._read_and_validate(output_path, gap_summary)

    def _read_and_validate(self, output_path: str, gap_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Read JSON from output_path, validate, apply P3b downgrade, return result."""
        try:
            with open(output_path, "r", encoding="utf-8") as fh:
                raw_text = fh.read()
        except FileNotFoundError:
            return _degraded(f"output file {output_path} not found")
        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            self._cleanup(output_path)
            return _degraded(f"output file was not valid JSON: {exc}")
        try:
            result = _validate(parsed)
        except ValueError as exc:
            logger.warning("hermes output failed validation: %s", exc)
            self._cleanup(output_path)
            return _degraded(f"output failed validation: {exc}")

        # P3b: auto-downgrade missing_concept → alias_candidate if concept already exists
        if result.get("finding_type") == "missing_concept" and self._bridge is not None:
            proposed_id = (result.get("proposed_concept_id") or "").lower().replace("-", "_")
            try:
                registry = self._bridge.kb.CONCEPT_REGISTRY
                existing_ids = {str(e.get("id", "")).lower() for e in registry}
                if proposed_id and proposed_id in existing_ids:
                    logger.info(
                        "P3b: proposed_concept_id '%s' already exists — downgrading to alias_candidate",
                        proposed_id,
                    )
                    result["finding_type"] = "alias_candidate"
                    result["concept_id"] = proposed_id
                    result["ready_for_code_change"] = False
                    result["reasoning"] = (
                        f"[auto-downgraded: '{proposed_id}' already in CONCEPT_REGISTRY] "
                        + result.get("reasoning", "")
                    )
            except Exception as exc:
                logger.debug("P3b concept_id check failed: %s", exc)

        logger.debug("hermes judge output persisted to %s", output_path)
        return result

    def judge_gap(self, gap_summary: Dict[str, Any], timeout: int = 120) -> Dict[str, Any]:
        """Ask Hermes (kb-supervisor profile / Qwen) to judge a KB-gap case.

        Routes needs_investigation gaps to judge_gap_conversation (3-turn reasoning).
        Routes alias_candidate and wrong_source_doc gaps to the single-shot path.
        Falls back to single-shot on any conversation failure.

        On any failure returns degraded-mode dict — never raises.
        """
        det = (gap_summary.get("deterministic_classification") or "").upper()
        is_needs_investigation = (
            "NEEDS_INVESTIGATION" in det
            or "INVESTIGATION" in det
            or "NO_CONCEPT" in det
            or "MISSING" in det
        )
        # Alias-only and wrong-source cases don't benefit from multi-turn reasoning
        if is_needs_investigation:
            return self.judge_gap_conversation(gap_summary, timeout=timeout)

        # Single-shot path for alias_candidate / wrong_source_doc
        hermes_bin = shutil.which("hermes")
        if hermes_bin is None:
            return _degraded("hermes binary not found on PATH")

        run_id = f"{os.getpid()}_{int(time.time())}"
        gap_key = "_".join(
            str(gap_summary.get(k, "unknown")) for k in ("module", "intent")
        ).replace("/", "-").replace(" ", "_")[:64]
        _REPO_ROOT = Path(__file__).resolve().parents[3]
        judge_out_dir = _REPO_ROOT / "local" / "supervisor" / "judge_outputs" / run_id
        try:
            judge_out_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return _degraded(f"could not create judge output dir {judge_out_dir}: {e}")
        output_path = str(judge_out_dir / f"{gap_key}.json")
        env = {**os.environ, "PATH": f"/Users/adwit.sharma/.local/bin:{os.environ.get('PATH', '')}"}

        return self._single_shot_judge(gap_summary, output_path, env, timeout)

    def _build_kb_inventory(self) -> str:
        """Build KB inventory with top-level title + all ## section headings per file."""
        kb_dir = Path(__file__).resolve().parents[3] / "kb"
        lines = []
        for md_file in sorted(kb_dir.rglob("*.md")):
            rel = md_file.relative_to(kb_dir)
            title = ""
            subheadings: List[str] = []
            try:
                for line in md_file.read_text(errors="ignore").splitlines():
                    if line.startswith("# ") and not title:
                        title = line[2:].strip()
                    elif line.startswith("## "):
                        subheadings.append(line[3:].strip())
            except Exception:
                pass
            entry = f"  kb/{rel}  —  {title}" if title else f"  kb/{rel}"
            if subheadings:
                entry += f"  [sections: {' | '.join(subheadings[:6])}]"
            lines.append(entry)
        return "\n".join(lines)

    def _build_pipeline_signal(self, classification: Dict[str, Any]) -> str:
        """Build a per-query pipeline signal block from GapClassifier results.

        Shows the judge exactly which queries IDK vs answered, what docs were
        retrieved, and what entities matched — so it doesn't guess from filenames.
        """
        per_query = (classification.get("per_query_results") or [])[:15]
        if not per_query:
            return "  (no per-query pipeline data available)"

        kb_dir = Path(__file__).resolve().parents[3] / "kb"
        lines = []
        for r in per_query:
            q = (r.get("query") or "")[:100]
            cat = r.get("category", "?")
            ev = r.get("evidence") or {}
            is_idk = cat not in ("ALREADY_FIXED",)
            status = "IDK" if is_idk else "ANSWERED"
            entities = ev.get("entities") or ev.get("near_miss_concepts") or []
            sources = ev.get("evidence_sources") or []
            score = ev.get("top_score", 0)
            lines.append(f"  [{status}] {q}")
            lines.append(f"    category={cat} | entities={entities[:2]} | top_score={score:.2f}")
            if sources:
                lines.append(f"    retrieved: {sources[:2]}")
                # Grab first 400 chars of the top retrieved doc + relevance check
                top_src = sources[0] if sources else None
                if top_src:
                    src_path = kb_dir.parent / top_src
                    try:
                        content = src_path.read_text(errors="ignore")
                        snippet_lines = []
                        for ln in content.splitlines():
                            if ln.startswith("source_url:") or ln.startswith("<!--"):
                                continue
                            if ln.strip():
                                snippet_lines.append(ln.strip())
                            if len(" ".join(snippet_lines)) > 800:
                                break
                        snippet = " ".join(snippet_lines)[:800]
                        lines.append(f"    doc snippet: {snippet}")
                        # Check if key query terms appear in the full doc content
                        # If not, flag as false-positive retrieval so judge doesn't
                        # assume the doc covers the topic just because it was retrieved
                        import re as _re
                        q_terms = set(_re.findall(r'[a-z]{5,}', q.lower()))
                        q_terms -= {
                            "that", "this", "with", "from", "have", "what",
                            "where", "when", "which", "does", "will", "should",
                            "gupshup", "whatsapp", "account", "business",
                            "setup", "using", "about", "their", "there",
                            "number", "message", "messages", "platform",
                            "console", "integration", "integrations",
                        }
                        content_lower = content.lower()
                        missing = [t for t in sorted(q_terms)[:8] if t not in content_lower]
                        if q_terms and len(missing) > len(q_terms) * 0.4:
                            lines.append(
                                f"    ⚠ FALSE-POSITIVE RETRIEVAL: doc does not contain "
                                f"key query terms {missing[:5]} — this doc does NOT cover "
                                f"the query topic. Classify as NO_DOCS_IN_SCOPE."
                            )
                    except Exception:
                        pass
            reason = ev.get("reason", "")
            if reason:
                lines.append(f"    reason: {reason[:120]}")
        return "\n".join(lines)

    def judge_gap_4bucket(
        self,
        gap,
        classification: Dict[str, Any],
        traces_for_gap,
        timeout: int = 300,
    ) -> Dict[str, Any]:
        """Classify a gap into one of 4 buckets: HAS_DOCS_FAILS, NO_DOCS_IN_SCOPE, OUT_OF_SCOPE, NOISE.

        Uses a single-shot Qwen call with rich pipeline signal context:
        - Per-query IDK/answered status from GapClassifier (up to 10 queries)
        - Actual retrieved doc names + content snippets (800 chars)
        - Deterministic pre-classification verdict
        - Adversarial second-pass for medium/low confidence verdicts
        Returns a parsed dict, or a degraded result on failure.
        """
        hermes_bin = shutil.which("hermes")
        if hermes_bin is None:
            return {
                "bucket": "HAS_DOCS_FAILS",
                "confidence": "low",
                "reasoning": "Hermes not available — degraded mode",
                "matching_doc": None,
                "root_cause": None,
                "keywords_to_add": [],
                "doc_to_create": None,
                "doc_outline": None,
                "doc_priority": None,
                "reason_ignored": None,
                "degraded": True,
            }

        kb_inventory = self._build_kb_inventory()
        pipeline_signal = self._build_pipeline_signal(classification)
        deterministic_verdict = classification.get("category", "unknown")
        deterministic_confidence = classification.get("confidence", "unknown")
        # Show up to 15 failure examples in the prompt
        failing_queries_list = (gap.failure_examples or [])[:15]

        json_schema = json.dumps({
            "bucket": "HAS_DOCS_FAILS | NO_DOCS_IN_SCOPE | OUT_OF_SCOPE | NOISE",
            "confidence": "high | medium | low",
            "reasoning": "one paragraph explaining the decision, referencing specific query results",
            "matching_doc": "kb/path/to/doc.md or null",
            "root_cause": "keyword_gap | routing_miss | retrieval_rank | answer_quality | content_thin | null",
            "keywords_to_add": ["specific term from queries not in doc headings"],
            "doc_to_create": "kb/module/suggested-filename.md or null",
            "doc_outline": "markdown outline or null",
            "doc_priority": "high | medium | low | null",
            "reason_ignored": "explanation if OUT_OF_SCOPE or NOISE, else null",
            "per_query_notes": {"query_text_prefix": "IDK|ANSWERED — one-line reason"},
        }, indent=2)

        run_id = f"{os.getpid()}_{int(time.time())}"
        gap_key = f"{gap.module}_{gap.intent}".replace("/", "-").replace(" ", "_")[:64]
        _REPO_ROOT = Path(__file__).resolve().parents[3]
        judge_out_dir = _REPO_ROOT / "local" / "supervisor" / "judge_outputs" / run_id
        try:
            judge_out_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return {
                "bucket": "HAS_DOCS_FAILS",
                "confidence": "low",
                "reasoning": f"Could not create output dir: {e}",
                "matching_doc": None,
                "root_cause": None,
                "keywords_to_add": [],
                "doc_to_create": None,
                "doc_outline": None,
                "doc_priority": None,
                "reason_ignored": None,
                "degraded": True,
            }
        output_path = str(judge_out_dir / f"4bucket_{gap_key}.json")

        prompt = f"""You are the KB supervisor judge for the Gupshup Guide skill.

The Gupshup Guide answers questions ONLY about Gupshup's products:
WhatsApp Business API, Bot Studio, Campaign Manager, SuperAgent, Agent Assist, CTX,
BizAI/Meta Business Agent, Channels (RCS, Instagram, Viber, Telegram), Integrations,
AI Admin, Personalize, Wallet, Goals. It does NOT answer general knowledge questions.

## Gap Being Analyzed
Module: {gap.module}
Intent: {gap.intent}
Total failures: {gap.failure_count}
Answer rate: {gap.answer_rate:.1%}
Deterministic pre-classification: {deterministic_verdict} (confidence: {deterministic_confidence})

## Per-Query Pipeline Results
IMPORTANT: This shows exactly what happened when each query was run through the live skill pipeline.
Use this as your PRIMARY evidence — it tells you which queries actually IDK, what docs were retrieved,
what entities matched, and a snippet of the top retrieved doc's content.

{pipeline_signal}

## KB File Inventory (for reference)
{kb_inventory}

## Classification Rules

HAS_DOCS_FAILS: A KB doc EXISTS and was RETRIEVED for the IDK queries (check the retrieved: lines above),
  but the skill still IDKed. The doc covers the topic but retrieval score was too low, or the entity
  keyword didn't match, or the doc content is too thin to compose an answer.
  → Only use this if retrieved: shows the relevant doc for the IDK queries.
  → Root cause options: keyword_gap (doc exists but query terms don't match its keywords),
    routing_miss (wrong module detected), retrieval_rank (right doc retrieved but scored too low),
    content_thin (doc retrieved but content too sparse to answer), answer_quality (answer composed wrong).
  → keywords_to_add: SPECIFIC terms from the IDK queries that are absent from the doc's headings/keywords.

NO_DOCS_IN_SCOPE: The queries are about a legitimate Gupshup product topic but the retrieved: docs
  above are NOT relevant to the query (wrong topic), or no docs were retrieved at all.
  → Use this when the IDK queries ask about a Gupshup product topic with no matching KB file.
  → doc_to_create: suggest a specific file path. doc_outline: a real content outline based on the queries.

OUT_OF_SCOPE: The queries are NOT about Gupshup products. This includes: general knowledge, competitor
  products, architecture/security questions beyond Gupshup's documented features (stateless architecture,
  VAPT, RAM processing, BYOA billing), meta-requests (write me a script/PPT), or already-ANSWERED queries
  where the skill is working correctly.
  → If most queries in the pipeline signal show ANSWERED, classify as OUT_OF_SCOPE (gap is not real).

NOISE: Queries are malformed, too short, test traffic, or cannot be classified.

CRITICAL: A gap where most queries show ANSWERED in the pipeline signal is NOT a real gap.
Do not classify it as HAS_DOCS_FAILS — classify as OUT_OF_SCOPE with reason "most queries already answered".

Respond with ONLY valid JSON matching this schema exactly:
{json_schema}

Write the JSON to the file at: {output_path}
No markdown fences, no prose."""

        env = {**os.environ, "PATH": f"/Users/adwit.sharma/.local/bin:{os.environ.get('PATH', '')}"}
        _degraded_4bucket = {
            "bucket": "HAS_DOCS_FAILS",
            "confidence": "low",
            "reasoning": "judge call failed — degraded mode",
            "matching_doc": None,
            "root_cause": None,
            "keywords_to_add": [],
            "doc_to_create": None,
            "doc_outline": None,
            "doc_priority": None,
            "reason_ignored": None,
            "degraded": True,
        }

        try:
            proc = subprocess.run(
                ["hermes", "-p", _PROFILE, "-z", prompt, "--yolo"],
                timeout=timeout, capture_output=True, env=env,
            )
        except subprocess.TimeoutExpired:
            self._cleanup(output_path)
            return {**_degraded_4bucket, "reasoning": f"judge timed out after {timeout}s"}
        except Exception as exc:
            self._cleanup(output_path)
            return {**_degraded_4bucket, "reasoning": f"subprocess error: {exc}"}

        if proc.returncode != 0:
            self._cleanup(output_path)
            return {**_degraded_4bucket, "reasoning": f"hermes exited {proc.returncode}"}

        try:
            with open(output_path, "r", encoding="utf-8") as fh:
                raw_text = fh.read()
        except FileNotFoundError:
            return {**_degraded_4bucket, "reasoning": f"output file {output_path} not found"}

        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            self._cleanup(output_path)
            return {**_degraded_4bucket, "reasoning": f"output not valid JSON: {exc}"}

        # Validate bucket value
        valid_buckets = {"HAS_DOCS_FAILS", "NO_DOCS_IN_SCOPE", "OUT_OF_SCOPE", "NOISE"}
        if parsed.get("bucket") not in valid_buckets:
            return {**_degraded_4bucket, "reasoning": f"invalid bucket: {parsed.get('bucket')}"}

        result = {
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

        # Adversarial second pass for medium/low confidence — challenge the verdict.
        # Self-hosted Qwen: no cost, always worth running for uncertain calls.
        if result["confidence"] in ("medium", "low") and not result.get("degraded"):
            logger.debug(
                "4-bucket: %s/%s confidence=%s — running adversarial challenge",
                gap.module, gap.intent, result["confidence"],
            )
            challenge_out = str(judge_out_dir / f"4bucket_{gap_key}_challenge.json")
            challenge_prompt = f"""You are an adversarial reviewer challenging a KB gap classification verdict.

Original verdict:
  Gap: {gap.module} / {gap.intent}
  Bucket: {result['bucket']}
  Confidence: {result['confidence']}
  Reasoning: {result['reasoning']}
  Matching doc: {result.get('matching_doc')}

Pipeline evidence that led to this verdict:
{pipeline_signal}

Your job: CHALLENGE this verdict. Find the strongest argument AGAINST it.
- If bucket=HAS_DOCS_FAILS: is there any evidence the doc doesn't actually cover the topic (⚠ FALSE-POSITIVE lines)?
- If bucket=NO_DOCS_IN_SCOPE: is there a KB file that DOES cover this? Check the KB inventory carefully.
- If bucket=OUT_OF_SCOPE: are any of the IDK queries actually about a real Gupshup product?

After challenging, output the FINAL verdict — either confirm the original or correct it.

Write ONLY valid JSON to: {challenge_out}
Schema: {{"bucket": "...", "confidence": "high|medium|low", "reasoning": "...", "challenge_note": "what you found", "overturned": true/false}}
No prose, no fences."""

            try:
                proc2 = subprocess.run(
                    ["hermes", "-p", _PROFILE, "-z", challenge_prompt, "--yolo"],
                    timeout=timeout, capture_output=True, env=env,
                )
                if proc2.returncode == 0:
                    with open(challenge_out, "r", encoding="utf-8") as fh2:
                        challenged = json.loads(fh2.read())
                    if challenged.get("overturned") and challenged.get("bucket") in valid_buckets:
                        logger.info(
                            "  4-bucket: %s/%s verdict OVERTURNED by challenge: %s → %s",
                            gap.module, gap.intent, result["bucket"], challenged["bucket"],
                        )
                        result["bucket"] = challenged["bucket"]
                        result["confidence"] = challenged.get("confidence", "medium")
                        result["reasoning"] = challenged.get("reasoning", result["reasoning"])
                        result["challenge_note"] = challenged.get("challenge_note", "")
                    else:
                        result["challenge_note"] = challenged.get("challenge_note", "verdict confirmed")
                        result["confidence"] = "high"  # confirmed by adversarial pass → upgrade
            except Exception as exc:
                logger.debug("adversarial challenge failed (non-fatal): %s", exc)

        logger.debug("4-bucket verdict for %s/%s: %s", gap.module, gap.intent, result["bucket"])
        return result

    @staticmethod
    def _cleanup(output_path: str) -> None:
        try:
            os.remove(output_path)
        except FileNotFoundError:
            pass
        except OSError as exc:
            logger.debug("failed to clean up hermes output file %s: %s", output_path, exc)
