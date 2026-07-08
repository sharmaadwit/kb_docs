# Trace Mismatch Report — Last 2 Days

**Generated:** 2026-07-07

---

## Summary

| Metric | Count |
|--------|-------|
| Traces fetched (last 2 days) | 34 |
| Waitlist name→email entries | 1138 |
| Clean userId→email entries from traces | 3 |
| Already correctly tagged | 26 |
| Mismatches found | 1 |
| Successfully patched | 1 |
| Patch errors | 0 |
| Unresolvable (no name/userId match) | 7 |

---

## Fixed Traces

| Trace ID | Wrong Email | Correct Email | Source |
|----------|-------------|---------------|--------|
| `kb-kb_answer-a1c397a8711444a2` | adwit.sharma@gupshup.io | admin@reworks.in | userId=30 in clean traces |

---

## Unresolvable Traces

These traces had mismatched emails but could not be resolved — no matching name or userId was found in the waitlist or clean trace set.

| Trace ID | userId | Name | Env | Current Email |
|----------|--------|------|-----|---------------|
| `kb-kb_answer-50f75def038943ca` | 165 | Nidhi Shridhar | PROD | adwit.sharma@gupshup.io |
| `kb-kb_answer-9bfc0bbea3a245c3` | 337 | Rodrigo Girard | PROD_EXT | adwit.sharma@gupshup.io |
| `kb-kb_answer-a517611eb10f4aa2` | 424 | Henrique Proenca | PROD_EXT | adwit.sharma@gupshup.io |
| `kb-kb_answer-2d72258582cb45dd` | 424 | Henrique Proenca | PROD_EXT | adwit.sharma@gupshup.io |
| `kb-kb_answer-96055b572fd449f4` | 424 | Henrique Proenca | PROD_EXT | adwit.sharma@gupshup.io |
| `kb-kb_answer-0c2e92d89b6649ff` | 424 | Henrique Proenca | PROD_EXT | adwit.sharma@gupshup.io |
| `kb-kb_answer-89ce7d0f2a3f459a` | 600 | Bruno Montoro | PROD_EXT | adwit.sharma@gupshup.io |

**Note:** Henrique Proenca (userId=424) appears 4 times across PROD_EXT traces, all unresolvable. Bruno Montoro and Rodrigo Girard are single occurrences. Nidhi Shridhar is the only unresolvable trace from PROD (non-EXT).

---

## Errors

None.
