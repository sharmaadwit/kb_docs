# Claude Handoff — Gupshup KB Skill (`kb_docs`)

Give this file (and task-specific specs like `local/docs/idk-fix-instructions.md`) to Claude
at the start of a session. It explains what this repo is, how the system works, and how to
act on the user's inputs without breaking production behavior.

---

## 1. What we are building

A **grounded documentation assistant** for **Gupshup Console** (Conversation Cloud). It
answers product questions **only from indexed Markdown KB** — no invented features, no
guessing from nearby pages when docs don't exist.

The user-facing agent is deployed on **Gupshup** as skill **"Gupshup Guide"**. This repo
(`sharmaadwit/kb_docs`, branch `main`) is the **dev/source-of-truth** for skill Python and
KB content that the deployed skill reads at runtime via GitHub.

**Recent milestone (shipped):** IDK regression fix — curated test pass rate **7/26 → 24/26**
with **zero wrong-page answers**. Commit `216cf08` on `main`. User pasted `kb_answer.py` +
`kb_video.py` into the skill and re-ran `kb_ingest` (377 markdown files → 6,184 chunks).

---

## 2. Architecture (three zones)

| Zone | Path | Role |
|------|------|------|
| **Skill code** | `skill/` in repo → **flat root** in deployed Gupshup skill | Answer gates, search, ingest, video selection, analytics hook |
| **KB content** | `kb/` | Markdown docs, `kb_chunks.jsonl`, `kb_index.json`, `video_manifest.json` — fetched/ingested from GitHub at runtime |
| **Local dev** | `local/` | Tests, analytics scripts, regression harness, reports — **never deployed** |

At **request time**, the skill loads KB data from the **content repo** (`GITHUB_REPO`, typically
`product-introduction-kb` or this mirror), not from the developer's laptop.

---

## 3. Deployed Gupshup skill — ONLY these files may live there

The skill UI is a **flat root** (no `skill/` prefix):

```
Gupshup Guide/
├── docs/                 ← UX_RULES.md, README.md, etc.
├── SKILL.md              ← agent system prompt (v3.9)
├── kb_analytics.py
├── kb_answer.py          ← main answer pipeline + gates + video attach
├── kb_ingest.py          ← chunk markdown → kb_chunks.jsonl + kb_index.json
├── kb_search.py
├── kb_storage.py         ← GitHub fetch abstraction
└── kb_video.py           ← video selection / catalog
```

**Not in the skill:** `kb/**`, `kb_chunks.jsonl`, `kb_index.json`, `video_manifest.json`,
anything under `local/`. Those live in the GitHub content repo and are updated via ingest.

**Deploy sequence after code + content changes:**

1. Push skill-relevant changes to `main` on `sharmaadwit/kb_docs`.
2. **Paste** updated skill Python into Gupshup (usually `kb_answer.py` and/or `kb_video.py`;
   paste others only if they changed).
3. Run **`kb_ingest`** on the agent (regenerates `kb/kb_chunks.jsonl` + `kb/kb_index.json`).
4. Spot-check or let the analytics agent run the regression harness.

---

## 4. How answers work (mental model)

```
User question
    → Gupshup agent calls kb_answer (or kb_search)
        → load chunks from GitHub (kb_storage)
        → score + rank chunks (kb_answer._score_chunk, concept registry boosts)
        → intent: setup | definition | overview | schema | …
        → gate: _has_explicit_support — refuse if evidence weak/wrong topic
        → compose answer (templates, PLATFORM_OVERVIEW_ANSWER, evidence lines)
        → attach video(s): select_video | select_videos | catalog_videos (kb_video)
    → Agent renders tool output (SKILL.md + docs/UX_RULES.md: show ALL videos proactively)
```

**Important behaviors already in place:**

- **Proactive videos:** Agent must call KB tools for product questions; all returned video
  links must appear in the user-visible answer.
- **Multi-video:** Broad/platform asks get catalog walkthroughs; module-scoped "all features"
  get module videos; explicit "all videos" gets full catalog.
- **Graceful decline:** Undocumented products (e.g. CC Express, LeadSquared) →
  `"I don't have documentation on …"` — not IDK from a wrong page.
- **Defer stays IDK:** Topics with no doc (webhook platform SLA, catalog API, etc.) must
  **not** answer from Agent Assist chat SLA or other wrong pages.

Key constants/files:

| Concern | Where |
|---------|--------|
| Gates, scoring, concept registry | `skill/kb_answer.py` |
| Video relevance / catalog | `skill/kb_video.py`, `kb/video_manifest.json` |
| Agent prompt + UX | `skill/SKILL.md`, `skill/docs/UX_RULES.md` |
| Chunk index | `kb/kb_chunks.jsonl` (from ingest) |
| TF-IDF search index | `kb/kb_index.json` (from ingest) |

---

## 5. Two-agent split (how to route user requests)

The user runs **two separate Claude/Cursor agents** with different scopes:

### A. Skill enhancement agent (code + KB content)

**Does:**

- Edit `skill/*.py` (gates, scoring, registry, video logic).
- Reframe **existing** `kb/**/*.md` (add headings; surface buried facts — **no new facts**).
- Edit `kb/video_manifest.json` (`also_sources`, pitch flags).
- Push to git when asked.
- Produce handoff specs under `local/docs/` for large fixes.

**Does not:**

- Own analytics dashboards, Langfuse pulls, or regression reporting (hand off to B).
- Invent documentation for undocumented topics (those stay IDK/decline).

**After markdown edits:** rebuild chunks — production uses `kb_ingest` on the agent; locally
you can regenerate subset rows via `local/scripts/ingest_local.py --prefix kb/...`.

### B. Analytics agent (local-only)

**Does:**

- Run `python3 local/scripts/idk_regression.py --label after`
- Langfuse / NDJSON usage analysis (`local/scripts/usage_analytics.py`, `lf` CLI)
- Reports under `local/reports/`
- Edit tooling under `local/` only
- Local git commit (no push)

**Never:**

- Edit `skill/`
- Edit `kb/**` or `video_manifest.json` for behavior changes
- `git push`

When the user says *"use the analytics agent"*, do not implement skill fixes — analyze and
write specs (e.g. `local/docs/idk-fix-instructions.md`) for the skill agent.

---

## 6. How to move forward with user inputs

Use this decision tree:

| User asks for… | Action |
|--------------|--------|
| "Fix wrong answers / too many IDKs / bad video match" | Skill agent: trace query in `kb_answer.py` gates + concept registry; check top chunk in harness; fix; re-run regression |
| "Add video for module X" | `video_manifest.json` + possibly `kb_video.py`; ensure SKILL.md still says show all videos |
| "New product doc" | Content repo / KB team — **not** skill agent inventing facts; may reframe once page exists |
| "Measure pass rate / usage / Langfuse" | Analytics agent only |
| "Push to git" | Skill agent: commit skill + kb changes; **exclude** `local/` secrets/analytics unless user asks |
| "What do I paste in Gupshup?" | Only changed files from **§3** flat list; KB data flows via git + ingest |

**Before claiming done (skill changes):**

```bash
python3 local/scripts/idk_regression.py --label after
```

Target: maintain **≥ 22/26** on the curated set; **zero wrong-page answers** on defer items.
Report: `local/reports/idk_regression_<label>.json`.

Curated questions live in `local/scripts/idk_regression.py` (`QUESTIONS` list).

---

## 7. Hard rules (do not break)

1. **Do not invent facts** in KB markdown or answers. Reframing = reorganize text already on
   the page.
2. **Do not create new `.md` files** for IDK fixes unless the user explicitly expands scope.
3. **Wrong-page answers are worse than IDK** — especially SLA, catalog API, webhook V3 mapping.
4. **Undocumented products** → graceful decline (`UNDOCUMENTED_TOPICS` in `kb_answer.py`), not
   nearest-page guess.
5. **Deployed skill file whitelist** — only the 7 `kb_*.py` + `SKILL.md` + `docs/`; see §3.
6. **Parallelize safely** — follow `.cursor/rules/parallel-and-cost.mdc`: parallel independent
   work; sequential dependent edits; verify with harness.
7. **Git:** do not commit `.env`, local analytics code, or `kb/analytics/` unless user
   explicitly wants them tracked (currently local-only).

---

## 8. Repo map (quick reference)

```
kb_docs/
├── skill/                    → paste into Gupshup skill root
│   ├── kb_answer.py          ← gates, concepts, compose, langfuse
│   ├── kb_search.py
│   ├── kb_video.py
│   ├── kb_ingest.py
│   ├── kb_storage.py
│   ├── kb_analytics.py
│   ├── SKILL.md
│   └── docs/UX_RULES.md
├── kb/                       → content mirror; ingest outputs
│   ├── **/*.md
│   ├── kb_chunks.jsonl
│   ├── kb_index.json
│   └── video_manifest.json
├── local/                    → dev/analytics only
│   ├── docs/                 ← handoff specs (this file, idk-fix-instructions.md)
│   ├── scripts/idk_regression.py
│   └── reports/
└── .cursor/rules/            ← agent scope rules
```

---

## 9. Typical workflows

### Fix a failing regression question

1. Analytics agent (or you): identify `id` + `top_source` in `idk_regression_after.json`.
2. Skill agent: classify failure — decline vs gate vs wrong boost vs missing reframe.
3. Change minimal code and/or reframe existing page.
4. Rebuild chunks if markdown changed; run harness.
5. User pastes changed `.py` files; runs `kb_ingest` on Gupshup.

### User reports live bug ("SuperAgent shows Console video")

1. Reproduce with `kb_answer` locally or harness query.
2. Check intent routing, `_detect_module`, concept registry, `kb_video._row_is_relevant`.
3. Fix; push; tell user exactly which skill files to paste.

### User wants new capability overview / all videos

- Usually prompt + pitch routing (`_is_platform_pitch_query`, `catalog_videos`) already
  handled — confirm agent calls `kb_answer` and UX rules show all links.

---

## 10. What to ask the user when unclear

- **Skill paste vs ingest only?** (Did `kb_answer.py` / `kb_video.py` change?)
- **Skill agent or analytics agent** for this task?
- **OK to reframe existing KB page** or is the gap truly missing documentation (stay defer)?
- **Push to git?** (User must ask explicitly.)

---

## 11. Related docs in this repo

| File | Purpose |
|------|---------|
| `local/docs/idk-fix-instructions.md` | Example task spec for skill agent (IDK regression) |
| `local/docs/video-integration.md` | Video architecture notes |
| `local/docs/analytics-dashboard.md` | Analytics tooling overview |
| `README.md` | Repo zones summary |
| `.cursor/rules/analytics-only-agent.mdc` | Analytics agent hard limits |
| `.cursor/rules/parallel-and-cost.mdc` | Execution style |

---

## 12. Current status (as of handoff)

- **Regression:** 24/26 pass locally after IDK fix; 2 known graceful IDKs:
  `inapp_support_nodes` (multi-node summary), `external_event_pt` (Portuguese query tokens).
- **Production:** User pasted `kb_answer.py` + `kb_video.py`; ingest confirmed
  **377 files / 6,184 chunks** aligned with `main`.
- **Next improvements:** User will drive via analytics agent findings → new specs in
  `local/docs/` → skill agent implements → paste + ingest → analytics verifies.

When starting a session, ask the user: **"Are we doing skill changes or analytics today?"**
Then follow §5 and §6.
