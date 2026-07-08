# Existing Traces Email Fix Report

**Date**: 2026-07-09
**Scope**: Live Langfuse traces, 2026-07-03 to 2026-07-09 (151 `kb_answer` traces fetched)
**Trigger**: `user_email` hardcoded fallback bug in `skill/kb_answer.py` (fixed separately, commit `49a88d5d`)

---

## Key Finding: `user_id` Is Not a Reliable Identifier

Before patching anything, I cross-checked `userId` against trace history and found it is **reused across unrelated accounts** — e.g. `userId=30` has been tied to at least 8 different real emails over time (nishchal.motwani@ampdlocal.com, hello@rapchai.com, admin@reworks.in, sales@indiatradersagra.com, adityagupta318@gmail.com, admin@bloomerce.ai, devendra@apporbits.com, mohyeldein.elbaroudy@gupshup.io). Likewise `userId=2` is a shared bucket for anonymous CC Express visitors with random per-session placeholder addresses.

**Consequence**: the pre-existing `local/reports/userid_email_map.json` and `resolution_map.json` (built by mapping `user_id → email`) are **not safe to trust wholesale**. I instead resolved each trace by its exact `user_name` string, and only accepted a match when that exact string had **zero conflicting emails** across all available trace history.

---

## Scope of Pollution

Out of 151 `kb_answer` traces fetched (2026-07-03 → 2026-07-09):
- **50 traces** carried `user_email = adwit.sharma@gupshup.io`
- This confirms the hardcoded-fallback bug was **still active in production** right up until today's code fix — not limited to the originally-reported 2-hour window on 2026-07-03.

---

## Fixed (9 traces) — Patched in Langfuse ✅

Resolved by exact `user_name` match with no conflicting candidate email anywhere in trace history, cross-verified against 3 independent internal maps (`userid_email_map.json`, `uid_map_out.json`, `resolution_map.json`) where available.

| Trace ID | user_name | userId | Corrected email | Verified |
|---|---|---|---|---|
| kb-kb_answer-ff620d77853c4447 | Ankit Kanwara | 181 | ankit.kanwara@gupshup.io | ✅ |
| kb-kb_answer-a7a273ae80a4485b | manvendra_22 | 30 | admin@reworks.in | ✅ |
| kb-kb_answer-21bb357ebfd24342 | manvendra_22 | 30 | admin@reworks.in | ✅ |
| kb-kb_answer-79032d55f13f4ad6 | manvendra_22 | 30 | admin@reworks.in | ✅ |
| kb-kb_answer-33e3f27786504c19 | manvendra_22 | 30 | admin@reworks.in | ✅ |
| kb-kb_answer-0791b341fd044a3e | projectleads2026 | 30 | admin@reworks.in | ✅ |
| kb-kb_answer-17505871f3d3467e | Joseph Cobbinah | 273 | joseph.cobbinah@gupshup.io | ✅ |
| kb-kb_answer-1dad7c3edddc44e0 | Fernando Reynoso | 133 | fernando.reynoso@gupshup.io | ✅ |
| kb-kb_answer-7761b9eb64b44b4b | Abhijit Chatterjee | 688 | abhijit.chatterjee@gupshup.io | ✅ |

**Method**: Re-submitted a `trace-create` ingestion event with the same trace `id` (Langfuse upserts by ID), preserving original `input`/`output`/all other metadata, only overwriting `user_email` and top-level `userId`. All 9 verified via follow-up GET after ~10s propagation delay.

---

## Not Found / Unresolvable (14 traces) — Reported, Not Patched ⚠️

Checked against: live trace history (151 traces + earlier 7-day export), all 3 internal maps, **and** `/Users/adwit.sharma/superagent-waitlist-funnel/output/waitlist_export.xlsx` (all 4 populated sheets: Daily_log, Master, ICP, Outreach_nurture — 1138+ leads).

**Zero exact matches found in the waitlist export for any of the names below** — that funnel's leads don't overlap with these KB trace identities.

| user_name | userId | Traces | Why unresolved |
|---|---|---|---|
| accounts.youlab | 30 | 3 | No match in any source (traces, maps, or waitlist) |
| Renan Mazoroski | 333 | 2 | No match in any source |
| harish | 30 | 1 | Only a weak email-substring hit in waitlist (`harishmanekscorpion@gmail.com`) — different person, rejected as unreliable |
| Roneeta Basak | 567 | 1 | No match in any source |
| *(anonymous)* | 2 | 6 | `userId=2` is a shared CC Express anonymous-visitor bucket; existing records show **different random UUID placeholder addresses** per occurrence — no way to attribute this specific trace |
| marketing | 30 | 1 | **Ambiguous** — this exact username has 3 conflicting emails in history (admin@reworks.in, hello@rapchai.com, marketing@upgradsot.com); genuinely a shared/generic login, unsafe to guess |

**Recommendation for these 14**: leave as-is until a more authoritative identity source is available (e.g. the actual product/console user table, not a marketing waitlist). Do not guess.

---

## Left Alone (Not Actually Polluted)

| Category | Count | Reason |
|---|---|---|
| `user_id=None`, `environment=LOCAL` | 25 | Your own local dev-test runs — genuinely you, not a real customer. Kept as `adwit.sharma@gupshup.io` per your direction. |
| `user_id=43` (`test` / `adwit.sharma`) | 2 | Your own account — already correct. |

---

## Files Produced

- `local/reports/all_traces_jul3_to_jul9.json` — raw Langfuse export used for this analysis (151 traces)
- `local/reports/traces_to_patch.json` — the 9 resolved traces with before/after emails
- This report

## Related

- Root-cause code fix: `skill/kb_answer.py` commit `49a88d5d` — removed the hardcoded `adwit.sharma@gupshup.io` fallback so new traces stop being mislabeled.
- Earlier partial investigation: `local/reports/POLLUTION_ANALYSIS.md`, `local/reports/TRACE_MISMATCH_REPORT_2DAY.md` (superseded by this report — those undercounted the pollution window and used the now-disproven `user_id`-only matching for some entries).
