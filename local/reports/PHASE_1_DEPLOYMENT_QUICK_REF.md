# Phase 1 Deployment Quick Reference

## Files Modified

**Single file change:** `skill/kb_answer.py`

### Copy-Paste the Functions

You can extract these independently if needed:

```python
# Add to skill/kb_answer.py
# Line 7: import hashlib

# Lines 6483–6568: _compose_consulting_answer()
# Lines 7511–7527: _gate_module_for_consulting()
# Lines 7529–7564: _resolve_answer_mode()
# Lines 7567–7588: _route_answer_composer()

# Line 7832: Replace call-site
# Lines 7834–7835: Add answer_mode tagging
```

### Quick Diff Check

After pulling from GitLab:
```bash
# See all changes
git diff HEAD~2 HEAD -- skill/kb_answer.py | less

# Just count lines
git diff --stat HEAD~2 HEAD -- skill/kb_answer.py
# Expected: 181 insertions(+), 1 deletion(-)
```

---

## Environment Variables for Test Deployment

Copy-paste into your test environment (e.g., `.env`, Docker secrets, etc.):

```bash
# Master switch: enable consulting-tone router
export KB_CONSULTING_TONE_ENABLED=1

# Module allowlist: only RCS + Bot Studio in Phase 1
# (WhatsApp, Channels, Agent Assist excluded)
export KB_CONSULTING_TONE_MODULES="RCS,Bot Studio"

# Traffic split: 50/50 consulting vs control (A/B test)
export KB_CONSULTING_TONE_PCT=50

# Optional: force override for testing (testing only, don't use in prod)
# export KB_ANSWER_MODE=consulting  # or "standard"
```

---

## What to Look for in Traces

### Langfuse Dashboard

After deploying and sending queries, check:

1. **Field Present**
   - Traces should have `metadata.answer_mode` = "consulting" or "standard"
   - If absent, flag is not enabled

2. **Consulting vs Control Segments**
   - Consulting-mode answers are longer, multi-paragraph
   - Start with diagnostic framing: "Let's figure out...", "To set this up..."
   - Contain structured sections: diagnosis, context, options, recommended, follow-up
   - End with follow-up question for low-confidence queries

3. **Standard-Mode Answers** (control arm)
   - Shorter, traditional problem-solution format
   - No diagnostic framing
   - Typical answer structure: problem → solution → additional context

### Example Queries to Test

```bash
# Bot Studio (primary gate — should hit consulting-tone if lucky with 50/50 split)
Query: "how do I build a journey with conditional branching"
Expected module: Bot Studio
Expected mode: consulting OR standard (50/50)

# RCS (secondary gate — campaign-driven traffic, tracked directionally)
Query: "should I use RCS or WhatsApp for my campaign"
Expected module: Campaign Manager (detected as RCS via _gate_module_for_consulting)
Expected mode: consulting OR standard (50/50)

# Control (not in Phase 1 allowlist)
Query: "how do I send a WhatsApp template"
Expected module: WhatsApp
Expected mode: standard (always, WhatsApp excluded from Phase 1)
```

---

## Langfuse Query Examples

### Filter for Consulting-Tone Answers (Bot Studio)

```
metadata.module = "Bot Studio" AND metadata.answer_mode = "consulting"
```

### Filter for Control Arm (Bot Studio Standard)

```
metadata.module = "Bot Studio" AND metadata.answer_mode = "standard"
```

### Compare Side-by-Side

```
# Consulting arm query metrics
SELECT metadata.answer_mode, COUNT(*), AVG(metadata.confidence)
WHERE metadata.module = "Bot Studio"
GROUP BY metadata.answer_mode

# Expected output:
# consulting | 47 | 0.412
# standard   | 48 | 0.428
```

### Track RCS Directional (secondary signal)

```
# RCS traffic (may come from Channels or Campaign Manager module bucket)
SELECT metadata.answer_mode, COUNT(*)
WHERE (metadata.module = "Channels" OR metadata.module = "Campaign Manager")
  AND query LIKE "%rcs%"
GROUP BY metadata.answer_mode
```

---

## Monitoring During Pilot

### Day 1-3: Early Signal Check
- [ ] Consulting traces appearing (answer_mode = "consulting")
- [ ] Control traces appearing (answer_mode = "standard")
- [ ] ~50/50 split within each module
- [ ] No crashes or errors in consulting-tone code

### Day 4-5: Gate Metrics
- [ ] Bot Studio answer rate ≥ 76% (vs 100% baseline, acceptable ~5.7pp regression)
- [ ] Multi-turn conversations up ≥ 20% vs control arm
- [ ] No accuracy cliff drop

### Day 6-7: Full Week Assessment
- [ ] RCS directional signal reviewed (logged, not gated)
- [ ] Decision: continue scaling or rollback
- [ ] If passing: scale to 100% RCS + Bot Studio traffic
- [ ] If not passing: unset KB_CONSULTING_TONE_ENABLED to rollback

---

## Rollback (1-Line Env Change)

If anything breaks:

```bash
# Unset the flag
unset KB_CONSULTING_TONE_ENABLED

# Or set to empty
export KB_CONSULTING_TONE_ENABLED=""
```

Restart the service. All new traces will be 100% standard-mode (old code path).

---

## Success Signals

You'll know Phase 1 is working when:

1. ✅ **Consulting traces are present** — metadata.answer_mode = "consulting" visible in Langfuse
2. ✅ **Answers are longer and diagnostic** — multi-paragraph, framed as "Let's figure out...", etc.
3. ✅ **Bot Studio accuracy holds** — ≥76% (can accept ~5.7pp regression from 100% baseline)
4. ✅ **Multi-turn engagement increases** — % conversations with 2+ turns +20% vs control
5. ✅ **RCS signal logged** — directional tracking working, no errors

---

## Troubleshooting

### No `answer_mode` field in traces
- **Cause:** Flag not enabled or env var not loaded
- **Fix:** Verify `KB_CONSULTING_TONE_ENABLED=1` is set and service restarted

### All answers in standard mode (no consulting)
- **Cause:** Module not in allowlist or deterministic hash landed in control
- **Fix:** Check `KB_CONSULTING_TONE_MODULES` includes your module, or increase `KB_CONSULTING_TONE_PCT` to 100 for testing

### Consulting-tone errors / incomplete answers
- **Cause:** Evidence insufficient or evidence format mismatch
- **Fix:** Check `_has_explicit_support()` logic, ensure evidence dict has heading/text/score keys

### RCS queries not hitting consulting-tone gate
- **Cause:** Module detection landed in different bucket (Campaign Manager vs Channels)
- **Fix:** Verify `_gate_module_for_consulting()` is checking both "Channels" and "Campaign Manager"

---

## Files You Need

After `git pull` from GitLab:

1. ✅ **skill/kb_answer.py** — the modified code (copy functions 6483–7588)
2. ✅ **local/reports/BASELINE_PRE_PHASE1.md** — control baseline (954 traces, 30 days)
3. ✅ **local/reports/baseline_metrics_pre_phase1.json** — raw data for dashboard
4. ✅ **local/reports/PHASE_1_CODE_CHANGES.md** — detailed line-by-line reference
5. ✅ **local/reports/PHASE_1_GATES_AND_MONITORING.md** — monitoring gates and thresholds

---

**Ready to deploy:** `git pull gitlab main` then set env vars above

**Questions?** Check `local/reports/PHASE_1_CODE_CHANGES.md` for detailed tracing reference
