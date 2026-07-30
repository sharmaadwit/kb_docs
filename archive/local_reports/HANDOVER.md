# KB Docs — Handover Document

**Purpose**: Enable any model / environment to resume work on this project with full context.
**Last Updated**: 2026-07-07
**Author**: Claude (Opus 4.8) session

---

## 1. Project Overview

**Repo**: `kb_docs` — a Knowledge Base + retrieval skill for Gupshup product documentation.
**Working dir**: `/Users/adwit.sharma/kb_docs`
**Primary language**: Python (the skill), Markdown (KB content), JSONL (chunk index).

The system answers product questions by:
1. Detecting which **product module** a query belongs to (`_detect_module()`).
2. Retrieving + scoring chunks from `kb/kb_chunks.jsonl`.
3. Applying a **module-scoping fence** to prevent cross-product contamination.
4. Returning an answer + Langfuse telemetry.

---

## 2. Repository Layout

```
kb_docs/
├── CLAUDE.md                      # Agent rules — READ FIRST (governs what you may change)
├── skill/
│   └── kb_answer.py               # THE core skill — module routing, scoring, answering
├── kb/
│   ├── kb_chunks.jsonl            # Chunk index — 6,674 chunks (source of retrieval)
│   ├── bizai/                     # BizAI product docs (6 files)
│   ├── whatsapp/                  # WhatsApp / Meta Business Agent docs (5 files)
│   ├── superagent/                # SuperAgent docs
│   ├── agent-assist/              # Agent Assist docs
│   ├── bot-studio-analytics/      # Analytics docs
│   └── analytics/                 # KB usage NDJSON logs
├── local/
│   ├── reports/                   # Test reports, dashboards (safe to commit)
│   └── scripts/                   # Test + dashboard scripts (safe to commit)
```

---

## 3. Git & Remotes — CRITICAL RULES

**Two remotes, both must be kept in sync:**
- `origin`  → GitHub:  `https://github.com/sharmaadwit/kb_docs.git`
- `gitlab`  → GitLab:  `https://gitlab.gupshup.io/adwit.sharma/gupshup_guide.git` (**source of truth**)

**Push order**: GitLab is source of truth. Both remotes must receive every change.

**⛔ HARD RULE — NEVER push without explicit user approval.**
- Commit locally freely (per CLAUDE.md: `local/`, `kb/`, and `skill/` are all commit-approved this session).
- **Always ask "Ready to push?" and wait for an explicit "yes" / "git push" before pushing.**
- This was violated once in a prior session — do not repeat.

**Push procedure** (both remotes usually need a rebase first — history diverges frequently):
```bash
git pull --rebase origin main && git push origin main
git pull --rebase gitlab main && git push gitlab main
```
Rebases show many "skipped previously applied commit" warnings — this is normal (the two remotes cherry-pick each other's commits).

**Current state**: `main` HEAD = `4b8c622f`. Both remotes in sync at this commit.

---

## 4. What Was Done in Recent Sessions

### 4a. KB Content Ingestion (earlier session)
- Ingested BizAI Partner API whitepaper + external Meta/WhatsApp docs.
- Created 6 `kb/bizai/*.md` + 5 `kb/whatsapp/*.md` files.
- Added 12 chunks to `kb/kb_chunks.jsonl` (now 6,674 total).

### 4b. Module Routing Guardrails (main focus)
**Problem**: BizAI, SuperAgent, Agent Assist, and Meta Business Agent have overlapping
semantic space ("agent" appears everywhere). Queries were cross-contaminating.

**Solution**: Priority-ordered rules in `_detect_module()` (skill/kb_answer.py, ~line 3908)
plus a module-scoping fence (STRICT_SCOPED_MODULES, +5.0 in-module / -4.0 off-module).

**Guardrail fixes applied (all committed + pushed):**
| Fix | Query that failed | Rule added | Location |
|-----|-------------------|-----------|----------|
| P1 #1 | "third-party integrations does SuperAgent support?" | `integration + superagent → SuperAgent` | line ~3926 |
| P1 #2 | "access agent analytics and insights?" | `analytics + agent/team/routing → Agent Assist` | line ~3934 |
| P2 #3 | "create and register custom skills?" | `"skill" in q → SuperAgent` | line ~3975 |
| P2 #4 | "how does conversation routing work?" | `"routing" in q → Agent Assist` | line ~3981 |

**Result**: Comprehensive 20-query test → **100% accuracy (20/20)**, zero cross-contamination.

### 4c. Telemetry / Email Hygiene (most recent commits)
- Removed hardcoded test email default from kb_answer.
- Scoped `user_email` default to `TRACE_ENV=LOCAL`, now read from `USER_EMAIL` env var.
- Filter test email `adwit.sharma@gupshup.io` from sales reports.

---

## 5. `_detect_module()` Rule Order (skill/kb_answer.py ~line 3908)

Rules are evaluated top-to-bottom; **first match wins**. Order matters.

1. `campaign` → Campaign Manager;  `rcs` → Channels
2. deploy verbs (deploy/embed/publish/launch/go live) + agent → **SuperAgent**
3. `integration` + superagent → **SuperAgent**  *(P1 #1)*
4. `analytics` + (agent assist | team | routing | insights) → **Agent Assist**  *(P1 #2)*
5. `meta business agent` / `business agent` → **WhatsApp**
6. `whatsapp agent` / `whatsapp ai agent` → **WhatsApp**
7. agent + `template` → **Agent Assist**
8. build verbs (build/create/make/design/skills/recipe) + agent (excl. whatsapp/waba/meta/template) → **SuperAgent**
9. `skill` → **SuperAgent**  *(P2 #3)*
10. `routing` → **Agent Assist**  *(P2 #4)*
11. EXPLICIT_MODULES dict loop (~line 865, multi-word keys FIRST, `overview` LAST)
12. bare `agent` → **SuperAgent** (low-confidence default)
13. fallback → **General**

**Key invariant**: multi-word keys must precede single-word keys in `EXPLICIT_MODULES`
(else "Meta Business Agent overview" mis-routes to Overview).

---

## 6. How to Test

**Environment for local testing**: set `trace_env=LOCAL` (avoids Langfuse ingest;
missing-credential warnings are expected and harmless).

**Run the full guardrails regression (20 queries):**
```bash
python3 local/scripts/test_full_guardrails_post_fixes.py
```
Expected: `OVERALL ACCURACY: 20/20 (100.0%)`.

**Other test scripts** (all in `local/scripts/`):
- `test_priority1_fixes.py` — unit tests for `_detect_module()` (10 cases)
- `test_priority1_comprehensive.py` — end-to-end via `kb_answer()` (2 cases)
- `test_p0_regression_suite.py`, `test_p1_regression.py` — earlier regression suites

**Calling the skill directly:**
```python
import sys; sys.path.insert(0, "skill")
from kb_answer import kb_answer
r = kb_answer({"query": "your question", "trace_env": "LOCAL"})
# module label lives at: r["langfuse"]["module_label"]
# top source at:        r["langfuse"]["metadata"]["top_source"]
```
Note: `kb_answer` returns module info under `r["langfuse"]["module_label"]`, NOT a
top-level `detected_module` key (common mistake).

---

## 7. Key Reports (local/reports/)

- `FINAL_GUARDRAILS_VALIDATION_REPORT.md` — 100% accuracy, full rule breakdown
- `GUARDRAILS_TEST_FINDINGS.md` — original 90% test + issue analysis
- `PRIORITY1_FIXES_REPORT.md` — P1 fix details

---

## 8. Agent Role / Permission Rules (from CLAUDE.md — MUST FOLLOW)

- **Primary role**: Analytics & Telemetry agent (dashboards, traces, reports).
- **This session mode**: "Code Change Session" — skill/ modifications + commits are approved.
- ✅ May commit to `skill/`, `kb/`, `local/` without asking.
- ⛔ May NOT push to remote without explicit approval (ask every time).
- ⛔ May NOT force-push or do destructive ops without approval.
- When ambiguous about scope → STOP and ask, don't assume.

---

## 9. Open / Backlog Items

- **P3**: Confidence-based response strategy (>0.8 answer, 0.3–0.8 answer+disclaimer, <0.3 IDK).
- **P3**: Expand WhatsApp/Meta Business Agent KB content (currently minimal — several
  queries correctly route to WhatsApp but return "I don't know" for lack of chunks).
- **P3**: Add more Agent Assist team/routing/analytics content.
- **Monitor**: Langfuse production traces for real-world routing edge cases.
- **Note**: Uncommitted working-tree files exist (see `git status`) — pollution-analysis
  reports under `local/reports/` and `local/scripts/fix_polluted_traces.py`. Unrelated to
  guardrails; review before committing.

---

## 10. Quick-Start for a New Model/Environment

```bash
cd /Users/adwit.sharma/kb_docs
cat CLAUDE.md                                   # 1. Read the rules
cat local/reports/HANDOVER.md                   # 2. This doc
cat local/reports/FINAL_GUARDRAILS_VALIDATION_REPORT.md  # 3. Latest state
python3 local/scripts/test_full_guardrails_post_fixes.py # 4. Confirm 20/20 baseline
git log --oneline -10                           # 5. See recent history
```
Then: make changes in `skill/kb_answer.py` (routing) or `kb/` (content), test, commit,
and **ask before pushing**.
