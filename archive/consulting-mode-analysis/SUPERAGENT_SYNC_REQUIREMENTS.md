# SuperAgent Sync Requirements
**Date:** 2026-08-13  
**Status:** ✅ READY FOR SYNC (chunks already in kb_chunks.jsonl)

---

## 📦 What SuperAgent Needs to Sync

### **RUNTIME SYNC (GitLab Fetch)**

SuperAgent reads chunks from GitLab at runtime. Two files to pull:

1. **`skill/kb_answer.py`** (352 KB)
   - Consulting-tone routing logic
   - Lines 19-24: `CONSULTING_TONE_CONFIG` dict
   - Lines 6494-7856: New consulting functions
   - Telemetry tags for A/B analysis

2. **`kb/kb_chunks.jsonl`** (7,126 chunks total)
   - ✅ **75 new consulting chunks** (already appended + committed + pushed)
   - 7,051 existing base chunks
   - All chunks tagged with `intent`, `version`, `update_date`, `audience_level`

### No kb_ingest Needed

Since SuperAgent reads chunks from JSONL at runtime, the 14 consulting markdown files are **reference only**. The work of converting them to chunks is already done:

- ✓ 14 markdown files created (3,223 lines)
- ✓ 75 chunks extracted and added to kb_chunks.jsonl
- ✓ Each chunk tagged with `intent: "consulting"` for A/B segmentation
- ✓ All pushed to GitLab (source of truth)

---

## 📋 Chunk Details

### Consulting Chunks Added (75 total)

| File | Chunks | Module |
|------|--------|--------|
| consulting-conditional-branching.md | 6 | Bot Studio |
| consulting-loop-prevention.md | 6 | Bot Studio |
| consulting-when-to-build.md | 6 | Bot Studio |
| rcs-readiness-diagnosis.md | 5 | RCS |
| rcs-prerequisites-checklist.md | 5 | RCS |
| rcs-setup-paths.md | 5 | RCS |
| rcs-fallback-strategy.md | 5 | RCS |
| rcs-setup-comprehensive.md | 7 | RCS |
| error-handling-diagnosis.md | 5 | Error Handling |
| error-handling-http.md | 5 | Error Handling |
| error-handling-timeouts.md | 5 | Error Handling |
| error-handling-retry.md | 5 | Error Handling |
| error-handling-fallback.md | 5 | Error Handling |
| error-handling-production-checklist.md | 5 | Error Handling |

### Chunk Schema

```json
{
  "id": "kb/bot-studio/consulting-conditional-branching.md::chunk_0",
  "source": "kb/bot-studio/consulting-conditional-branching.md",
  "chunk": 0,
  "section": 0,
  "heading": "Diagnosis: What's Your Routing Scenario?",
  "heading_path": ["Conditional Branching in Bot Studio: Choosing Your Routing Strategy", "Diagnosis: What's Your Routing Scenario?"],
  "section_type": "concept",
  "is_reference": false,
  "local_chunk": 0,
  "text": "# Conditional Branching in Bot Studio...",
  "version": "1.0",
  "update_date": "2026-08-13",
  "intent": "consulting",
  "audience_level": "beginner"
}
```

All 75 new chunks have:
- ✅ `intent: "consulting"` (for telemetry segmentation)
- ✅ `version: "1.0"`
- ✅ `update_date: "2026-08-13"`
- ✅ `audience_level: "beginner"`

---

## 🚀 SuperAgent Deployment Steps

### Step 1: Pull Latest kb_chunks.jsonl from GitLab
```bash
git fetch gitlab
git checkout gitlab/main -- kb/kb_chunks.jsonl
```

This brings in all 7,126 chunks (7,051 base + 75 consulting) with metadata.

### Step 2: Verify Consulting Chunks Present
```bash
grep -c '"intent".*"consulting"' kb/kb_chunks.jsonl
# Should output: 75
```

### Step 3: Deploy skill/kb_answer.py
Update SuperAgent's `skill/kb_answer.py` with consulting-tone routing logic.

**Key changes:**
- Lines 19-24: `CONSULTING_TONE_CONFIG` (enabled, modules, traffic %, force_mode)
- Line 6494: `_compose_consulting_answer()` function
- Line 7546: `_resolve_answer_mode()` routing logic
- Line 7856: Telemetry tag `policy_meta["answer_mode"]`

### Step 4: Verify Runtime Behavior
When SuperAgent queries kb_chunks.jsonl:
1. Retrieves chunks (50% consulting, 50% standard for Bot Studio/RCS)
2. Routes to appropriate composer based on `_resolve_answer_mode()`
3. Logs `answer_mode` in Langfuse for A/B analysis

---

## 📊 What SuperAgent Will See at Runtime

### Chunk Retrieval
- **Standard queries** (non-Bot Studio/RCS): Get existing chunks (7,051 base)
- **Bot Studio queries**: 50% get consulting chunks + 50% get standard chunks
- **RCS queries**: 50% get consulting chunks + 50% get standard chunks
- **Other modules**: Only standard chunks (consulting disabled)

### Telemetry
- **Langfuse trace field**: `policy_meta["answer_mode"]`
- **Values**: `"consulting"` or `"standard"`
- **Segmentation**: Can filter traces by answer_mode for A/B metrics

### Answer Format
- **Consulting-tone**: Diagnosis → Context → Options → Recommended → Follow-up
- **Standard**: Problem → Solution (existing format)

---

## ✅ What's Already Done

- [x] 14 consulting markdown files created (3,223 lines)
- [x] 75 chunks extracted from markdown
- [x] All chunks added to kb/kb_chunks.jsonl
- [x] All chunks tagged with `intent: "consulting"`
- [x] All chunks committed to GitLab
- [x] All chunks pushed to GitLab (source of truth)
- [x] GitHub mirrored
- [x] skill/kb_answer.py updated with routing logic
- [x] Code committed and pushed

---

## 🔄 Git Status

**Latest commits:**
```
dd238600  Add 75 consulting-tone chunks to kb_chunks.jsonl for SuperAgent runtime loading
5e53c87b  Add deployment checklist: 72% accuracy validated, consulting KB ready
47c0fbad  Execution complete: KB cleanup + Phase 1 consulting chunks
```

**Push status:**
- ✅ GitLab: Pushed (dd238600)
- ✅ GitHub: Pushed (dd238600, mirror)

---

## 📊 Expected Accuracy Post-Deploy

| Module | Accuracy | Status |
|--------|----------|--------|
| Bot Studio | 78% | High confidence |
| RCS | 74% | Monitor closely |
| Error Handling | 66% | Acceptable baseline |

---

## 🔗 Related Documents

- `local/reports/DEPLOYMENT_CHECKLIST.md` — Step-by-step verification
- `local/reports/PUSH_COMPLETE.md` — What was pushed and when
- `local/reports/FULL_EXECUTION_SUMMARY.md` — Complete transformation overview
- `local/reports/live_validation_results.json` — Accuracy breakdown

---

**Summary**: Pull `kb/kb_chunks.jsonl` (has 75 consulting chunks) + deploy `skill/kb_answer.py` (has routing logic). No kb_ingest needed—chunks already in JSONL format for runtime loading.

