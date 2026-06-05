# IDK Fix Instructions — SKILL CODE + EXISTING-DOC REFRAMING

For the **skill code-change agent**. Allowed scope:
- **`skill/` Python** (gates, scoring, concept registry, graceful decline, pitch routing).
- **Reframing EXISTING `kb/**.md` pages** — restructure/clarify facts that are **already
  documented** on that page (add headings, surface a definition that's buried, add aliases).
- `kb/video_manifest.json` `also_sources` additions (JSON).

**Hard limits:**
- **Do NOT create any new files** (no new `.md`, no new modules).
- **Do NOT invent facts.** Reframing may only re-organize/clarify content already present in
  that page's source. If a fact isn't in the docs, the question stays **defer** (IDK/decline).
- After editing any markdown, **rebuild `kb/kb_chunks.jsonl`** so retrieval reflects the change.

**Execution rule (required):** Follow `.cursor/rules/parallel-and-cost.mdc`.
- Parallelize independent work across subagents launched in a single message (e.g. inspect
  the gate constants, the concept registry, and the manifest concurrently; reframe independent
  markdown pages concurrently). Keep only dependent steps sequential.
- Optimize cost: scope reads with `Grep`/`Glob`/semantic search before opening whole files,
  give subagents tight self-contained prompts, reuse gathered context, right-size effort.
- Never compromise correctness: verify with `python3 local/scripts/idk_regression.py --label after`
  before reporting done; if a cheaper path is riskier (e.g. multilingual/multi-entity hacks that
  threaten passing defer items), flag it rather than silently taking it.

Measurement is done by the analytics agent via `local/scripts/idk_regression.py`
(do not edit anything under `local/`).

Baseline: **7/26 pass** (`local/reports/idk_regression_baseline.json`).
Target after these skill-only changes: **≥ 22/26 pass**.

Retest after changes:

```bash
python3 local/scripts/idk_regression.py --label after
```

The harness scores three expectations:
- **answer** (14): doc content already exists in the index → must produce a substantive answer.
- **decline** (3): undocumented product → must decline gracefully.
- **defer** (9): no doc yet → must stay IDK or decline; must **NOT** answer from a wrong page.

---

## Files you will edit
- `skill/kb_answer.py` (gates, scoring, concept registry, graceful decline, pitch routing)
- `skill/kb_video.py` (video relevance relaxation)
- `kb/video_manifest.json` (`also_sources` additions — JSON)
- Existing `kb/**.md` pages listed in **Part D** (reframe only; no new files)
- Rebuild `kb/kb_chunks.jsonl` after markdown edits

---

## PART A — Graceful decline for undocumented products

**File:** `skill/kb_answer.py`

We have **no documentation** for **CC Express** and **LeadSquared**. Decline cleanly instead
of guessing a nearby page.

1. Add near the guardrail section (~line 2127, by `_guardrail_answer`):

```python
# Products/topics with no KB coverage. Decline cleanly instead of guessing a
# nearby page. Keys are normalized-query substrings; value is the display name.
UNDOCUMENTED_TOPICS = {
    "cc express": "CC Express",
    "ccexpress": "CC Express",
    "leadsquared": "LeadSquared",
    "lead squared": "LeadSquared",
}

def _undocumented_topic_decline(query: str) -> str:
    qn = _normalize_query_for_match(query)
    for needle, display in UNDOCUMENTED_TOPICS.items():
        if needle in qn:
            return (
                f"I don't have documentation on {display}, so I can't help with that "
                f"specific question. I can help with documented Gupshup Console topics "
                f"like Bot Studio, Agent Assist, Campaign Manager, Channels, AI Admin, "
                f"CTX, and Integrations."
            )
    return ""
```

2. In `kb_answer()`, call it **after** the `_guardrail_answer` block and **before** chunk
   loading/scoring, mirroring the existing guardrail return + telemetry:

```python
    undocumented = _undocumented_topic_decline(query)
    if undocumented:
        latency_ms = int((datetime.now(timezone.utc) - started).total_seconds() * 1000)
        langfuse = _send_langfuse(
            "kb_answer", query, undocumented, [], "General",
            ["unsupported"], "refusal", False, latency_ms, context, params,
        )
        return {
            "ok": True,
            "query": _redact_secrets_in_query_echo(query),
            "answer": undocumented,
            "citations": [],
            "langfuse": langfuse,
        }
```

**Acceptance:** `ccx_roles`, `ccx_arabic`, `leadsquared` → `declined`.
The message must keep the substring **"don't have documentation"** (harness marker).

---

## PART B — Confidence scoring & gate changes

**File:** `skill/kb_answer.py`. Constants at ~lines 202–205:
`MIN_TEMPLATE_SCORE=2.5`, `MIN_EVIDENCE_SCORE=1.2`, `MIN_CHUNK_SCORE=0.3`,
`MIN_EVIDENCE_SCORE_UNBOOSTED=4.0`.

### B1. Hedged-answer band (near-miss scores)
In `_has_explicit_support(...)` (~line 3885), after `strong_overlap` is computed, add:

```python
    # Clearly on-topic but modest absolute score -> allow a hedged answer
    # instead of refusing. Composer should phrase as "The documentation indicates...".
    hedged_ok = (
        (top1_overlap >= 0.7 and top1.get("score", 0.0) >= 0.5)      # high overlap
        or (top1_overlap >= 0.5 and top1.get("score", 0.0) >= 0.85)  # moderate both
    )
```

Update the score-floor early return to also allow `hedged_ok`:

```python
    if top1.get("score", 0.0) < effective_min and not strong_overlap and not hedged_ok:
        return False
```

### B2. Unboosted multi-source ceiling
Add a constant and use it when 2+ sources agree:

```python
MIN_EVIDENCE_SCORE_UNBOOSTED = 4.0
MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI = 2.5  # when len(evidence) >= 2 and top1_overlap >= 0.25
```

In the unboosted branch (the `MIN_EVIDENCE_SCORE_UNBOOSTED` check), use
`MIN_EVIDENCE_SCORE_UNBOOSTED_MULTI` when `len(evidence) >= 2 and top1_overlap >= 0.25`,
and also bypass that branch when `hedged_ok`.

### B3. Definition gate: accept noun-phrase match without marker words
Add a small helper:

```python
def _query_head_tokens(query: str) -> List[str]:
    return [
        t for t in re.findall(r"[a-z0-9]+", _normalize_query_for_match(query))
        if len(t) >= 4 and t not in SCORING_STOP_WORDS
    ]
```

In the `definition` branch of `_has_explicit_support`, before the marker-term check:

```python
    if intent == "definition":
        if _query_topic_not_in_evidence(query, joined):
            return False
        src_head = (str(top1.get("source") or "") + " " + str(top1.get("heading") or "")).lower()
        if top1_overlap >= 0.45 and any(t in src_head for t in _query_head_tokens(query)):
            return True
        return top1_overlap >= 0.2 and any(term in joined for term in [ ...existing list... ])
```

Fixes `flow_id` (5.55) and `inapp_support_nodes` (10.05) from existing chunks.

### B4. Setup gate: accept Steps/Procedure pages
In the `setup` branch, treat a numbered Steps/Procedure block as action-oriented:

```python
    has_steps_block = any(
        ("steps" in (c.get("heading") or "").lower()
         or "procedure" in (c.get("heading") or "").lower())
        for c in evidence
    )
    ...
    return ((has_action or has_steps_block) and top1_overlap >= 0.2) or top1_overlap >= 0.45
```

Fixes `webhook_server_setup` (9.75), `external_event_pt` (7.15), `ai_admin_tools`,
`mo_callback_gg`, `template_ops_guidelines` (overlap 0.83).

### B5. Schema gate: accept payload/field pages
```python
    if intent == "schema":
        if any(t in joined for t in ("payload", "fields", "parameter", "event", "json", "key")):
            return top1_overlap >= 0.2
```

Fixes `webhooks_fields` (6.25).

### B6. SLA / off-topic disambiguation (FIX THE 2 WRONG ANSWERS)
`gupshup_sla` and `webhook_sla_latency` currently answer from
`agent-assist/chat-management-sla.md`, which is the wrong SLA. Since there is **no**
webhook/platform SLA doc, these must **NOT** answer.

In `_score_chunk` (or a filter in `_select_evidence`): when the query contains
`webhook`/`latency`/`endpoint`/`delivering`/`inbound` and lacks Agent-Assist chat terms,
apply a strong penalty to sources matching `agent-assist/chat-management-sla`. With the page
removed, the normal gate yields IDK (acceptable `defer`).

Optionally add `"gupshup sla"` (bare) and `"webhook sla"` style asks to a soft-decline, but
IDK is acceptable for these `defer` items — the only requirement is **no wrong-page answer**.

**Acceptance:** `gupshup_sla`, `webhook_sla_latency` → `idk` (not `answered`).

### B7. Pitch/demo routing (+ video)
`retail_demo` is misrouted to `setup`. Extend the broad/pitch detection so it routes to the
overview path. In `_is_broad_query` / `_is_platform_pitch` / `_wants_full_catalog`, add
patterns: `demo`, `show me`, `retail client`, `features for a`, `including ... videos`.

In `_compose_answer` overview path (already returns `PLATFORM_OVERVIEW_ANSWER` for pitches),
ensure these queries reach it, and ensure `kb_answer()` calls
`kb_video.catalog_videos(...)` for pitch/broad queries so module videos attach.

**Acceptance:** `retail_demo` → `answered` **with video**.

---

## PART C — Concept registry boosts (route to the RIGHT existing page)

**File:** `skill/kb_answer.py`, `CONCEPT_REGISTRY` (~line 223).

Several questions flip to "answered" but from the **wrong page** unless boosted. Add entries
that boost the correct **existing** source slug. Use the established schema
(`aliases`, `source_boosts`, `module`, optional `templates`).

| Concept | aliases | source_boosts (existing files) | module |
|---------|---------|--------------------------------|--------|
| Console roles | "console roles", "org admin", "org owner", "user roles in console" | `overview/manage-organisation`: +6, `overview/invite-org-admins`: +4 | Overview |
| Customer 360 | "customer 360", "customer360" | `bot-studio/customer-360-node`: +6 | Bot Studio |
| Retained chat history | "retained chat history", "chat history", "returning web widget" | `channels/retain-customer-chat-history`: +6 | Channels |
| Delivery status/logs | "delivered status", "message status", "conversation logs", "delivery logs" | `channels/inbound-messages-and-events`: +5, `campaign-manager/campaign-analytics`: +3 | Channels |
| Analytics overview | "analytics overview", "bot analytics", "journey analytics", "analytics in gupshup" | `bot-studio-analytics/dashboard`: +5, `bot-studio-analytics/journey-tracking`: +3 | Analytics |
| AI Admin tools | "ai admin tool", "ai admin tools" | `ai-admin/tools-developer-mode`: +5 | AI Admin |

Do **not** add concepts for CC Express / LeadSquared (Part A).
Do **not** add concepts for the deferred topics (catalog API, webhook V3 mapping, etc.).

> After adding boosts, `console_roles`, `customer_360`, `retained_history`,
> `wa_delivery_logs`, `analytics_overview`, `ai_admin_tools` answer from the correct page.

---

## PART D — Reframe EXISTING pages (no new files; facts must already be on the page)

Restructure existing content so the buried answer surfaces and matches how users ask.
**Only re-organize/clarify text already present** in each page's source. Do not add facts
that aren't documented. Rebuild `kb/kb_chunks.jsonl` afterward.

| File (existing) | Reframe (using content already on the page) |
|-----------------|---------------------------------------------|
| `kb/bot-studio/customer-360-node.md` | Add a top **`## What is Customer 360`** section summarizing the page's existing definition (the "businesses can view these interactions on the Customer 360 module" content) so the product question answers from the right page. |
| `kb/bot-studio/whatsapp-flows-static-dynamic.md` | Add **`## What is a Flow ID`** that states the Flow-ID definition already implied on the page (generated in Meta BM, used to trigger the WhatsApp Flow node). |
| `kb/overview/manage-organisation.md` | Add heading **`## Console roles (Org Owner, Org Admin)`** pulling the existing Org Owner/Org Admin capability text under an explicit "roles" heading. |
| `kb/integrations/webhooks.md` | Add **`## Fields`** (existing `externalId`, `eventType`, etc.), and a **`## Server / callback setup`** heading over the existing "How To Configure" steps. (Do **not** invent V3 mode→Meta mapping or SLA — those stay deferred.) |
| `kb/ai-admin/tools-developer-mode.md` | Add **`## AI Admin tools — overview`** summarizing the page's existing tool description. |
| `kb/agent-assist/sending-templates-after-the-24-hour-window.md` | Add **`## Operational guidelines`** heading over the page's existing rules for sending templates after the 24h window. |
| `kb/bot-studio-analytics/dashboard.md` | Add **`## Analytics overview`** summarizing the page's existing live-metrics/dashboard description (and that it lives under Bot Studio Analytics). |
| `kb/bot-studio/callback-url-event-on-starting-node.md` | Add aliases in body text: "MO (mobile-originated)", "GG accounts" so the existing callback steps match the query phrasing. |
| `kb/channels/retain-customer-chat-history.md` | Ensure the definition line uses explicit "retained customer chat history … returning web widget users" phrasing (content already present). |

> Reframing strengthens the Part B/C flips and improves answer correctness, but the
> answer/decline/defer split is unchanged. Topics needing **new** facts
> (catalog API, webhook V3 mapping, error 4006, import contacts, post-deploy Meta BM,
> template→AI journey, journey-complete email, webhook SLA) remain **defer** — do not
> fabricate pages for them.

---

## PART E — Video attach (skill only)

**File:** `skill/kb_video.py`
- `_row_is_relevant(...)`: also return True when the matched page is among the top results and
  the query/page token overlap is high (≥ 0.4), even without a single shared distinctive token.

**File:** `kb/video_manifest.json` (JSON only — allowed)
- Add to the nearest relevant module video entry's `also_sources` (so answers now flipping to
  "answered" can attach a video):
  - `channels/retain-customer-chat-history.md`
  - `integrations/webhooks.md`
  - `overview/manage-organisation.md`
  - `bot-studio/customer-360-node.md`

---

## PART F — Acceptance criteria (run the harness)

```bash
python3 local/scripts/idk_regression.py --label after
```

Required outcomes:
- **decline (3):** `ccx_roles`, `ccx_arabic`, `leadsquared`.
- **answer (14):** `console_roles`, `retail_demo` (+video), `flow_id`, `customer_360`,
  `inapp_support_nodes`, `webhooks_fields`, `webhook_server_setup`, `retained_history`,
  `wa_delivery_logs`, `mo_callback_gg`, `external_event_pt`, `ai_admin_tools`,
  `template_ops_guidelines`, `analytics_overview`.
- **defer (9):** `meta_bm_postdeploy`, `template_then_ai`, `catalog_api`,
  `journey_complete_email`, `gupshup_sla`, `import_contacts`, `webhook_v3_modes`,
  `ctx_error_4006`, `webhook_sla_latency` → must remain `idk`/`declined`, **never** answer
  from a wrong page (especially the two SLA items).

Target: **≥ 22/26 pass** with **zero** off-topic answers.

Do not touch anything under `local/`. Do not create new files. Reframe existing `kb/**.md`
pages only (Part D) and rebuild `kb/kb_chunks.jsonl`. The analytics agent re-runs the harness
and reports the before/after delta per question.
