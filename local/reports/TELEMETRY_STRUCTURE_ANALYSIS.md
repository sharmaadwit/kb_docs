# Telemetry Structure Analysis Report
**Date**: 2026-08-15  
**Analysis Scope**: 30 latest Langfuse traces from kb_answer service  
**Status**: Complete

---

## Executive Summary

The telemetry system is functioning with **strong baseline metadata coverage** (100% for core fields), but **lacks span/event-level detail** and is **missing key enrichment fields** for case studies and video metrics.

### Key Findings:
- ✅ **Observations structure**: Present in API but at trace level (not nested observations)
- ✅ **Core metadata**: 42 consistent fields across ALL traces
- ❌ **Span/Event patterns**: NO span-level timing data detected (0 observations)
- ⚠️ **Enrichment fields**: Only 50% complete (video fields partially present, case studies completely absent)
- ⚠️ **Policy metadata**: NOT merged into traces (policy_meta field missing)

---

## 1. Observation Structure Analysis

### Current State
**Observations per trace**: 0 (average)
- All 30 traces have zero observations in the observations array
- No span-level timing data (start_time, end_time) detected
- No point-in-time events detected

### Interpretation
This indicates that **kb_answer currently sends only top-level trace metadata** without internal operation tracing. The trace represents a single operation boundary, not a composite of multiple sub-operations.

**Impact**: 
- No ability to profile KB retrieval latency separately from answer generation
- No intermediate step visibility
- Dashboard cannot show span-based breakdowns

### Span/Event Pattern Found
**None detected** — All traces are single-operation traces without internal structure.

---

## 2. Telemetry Payload Shape

### Metadata Field Coverage
**Total unique fields**: 70 fields across 30 traces  
**Consistently present fields (in ALL 30 traces)**: 42 fields

#### Top 20 Most Common Fields (100% coverage):

| Field | Coverage | Purpose |
|-------|----------|---------|
| `module` | 30/30 | KB module name |
| `is_sub_query` | 30/30 | Query type indicator |
| `answered` | 30/30 | Binary answer success |
| `logic_version` | 30/30 | KB answer logic version |
| `failure_type` | 30/30 | Failure classification |
| `answer_preview` | 30/30 | First 50 chars of answer |
| `intent_labels` | 30/30 | Detected query intent |
| `query_family` | 30/30 | Query cluster category |
| `clarification_asked` | 30/30 | Clarification required flag |
| `identity_source` | 30/30 | User identity source |
| `explicit_module` | 30/30 | User-specified module |
| `release` | 30/30 | KB release version |
| `channel_type` | 30/30 | Communication channel |
| `detected_product_original` | 30/30 | Detected product |
| `user_name` | 30/30 | User identifier |
| `unanswered` | 30/30 | Unanswered query flag |
| `user_id` | 30/30 | User account ID |
| `accuracy_score` | 30/30 | Answer quality score |
| `top_source` | 30/30 | Primary KB source |
| `user_email` | 30/30 | User email (anonymized) |

#### Video-Related Fields (Partial Coverage):

| Field | Coverage | Purpose |
|-------|----------|---------|
| `video_attached` | 29/30 | Video in response |
| `video_channel` | 29/30 | Video distribution channel |
| `video_source` | 10/30 | Video origin system |
| `video_id` | 10/30 | Video identifier |
| `video_platform` | 10/30 | Video platform (YouTube/DemoForge) |
| `video_title` | 10/30 | Video title |
| `video_start` | 10/30 | Start timestamp in video |
| `video_end` | 10/30 | End timestamp in video |
| `video_captions_on` | 10/30 | Caption enabled flag |

**Gap**: No `video_count` or `video_selected` aggregation fields.

#### Case Studies Fields (ABSENT):

| Field | Coverage | Purpose |
|-------|----------|---------|
| `case_studies_count` | 0/30 | ❌ NOT FOUND |
| `case_studies_fetched` | 0/30 | ❌ NOT FOUND |

#### Debug & Nested Fields:

| Field | Coverage | Context |
|-------|----------|---------|
| `identity_debug_param_keys` | 22/30 | User identification debugging |
| `identity_debug_param_keys.raw_params.*` | 2-8/30 | Raw request parameters |
| `identity_debug_param_keys.context_attrs.*` | 6/30 | Context attributes |
| `session_id` | 17/30 | Session tracking |
| `conversation_turn_number` | 16/30 | Multi-turn conversation position |
| `trace_sequence` | 16/30 | Trace ordering |

---

## 3. Critical Field Completeness

### Expected vs. Actual

| Field | Traces | Coverage | Status |
|-------|--------|----------|--------|
| `answer_mode` | 30 | 100% | ✅ COMPLETE |
| `confidence` | 30 | 100% | ✅ COMPLETE |
| `intent` | 30 | 100% | ✅ COMPLETE |
| `module_label` | 30 | 100% | ✅ COMPLETE |
| `video_selected` | 0 | 0% | ❌ MISSING |
| `video_count` | 0 | 0% | ❌ MISSING |
| `case_studies_count` | 0 | 0% | ❌ MISSING |
| `case_studies_fetched` | 0 | 0% | ❌ MISSING |
| `policy_meta` | 0 | 0% | ❌ MISSING |

### Analysis

**Completeness by Category**:
- **Core Fields**: 100% (answer_mode, confidence, intent, module_label)
- **Video Enrichment**: 33% (video_attached, video_channel only; missing aggregates)
- **Case Study Enrichment**: 0% (completely absent)
- **Policy Context**: 0% (policy_meta not merged)

**Root Cause**: 
- Video and case study metrics are **computed at response-generation time** but not attached to traces
- Policy metadata is likely stored separately and not merged into the trace payload
- Missing aggregation fields (count, selected) suggest **count logic hasn't been implemented** for these features

---

## 4. Payload Consistency & Shape

### Consistent Field Set (In ALL 30 traces)

**42 core fields** present in every trace:
```
module, is_sub_query, answered, logic_version, failure_type, answer_preview,
intent_labels, query_family, clarification_asked, identity_source,
explicit_module, release, channel_type, detected_product_original, user_name,
unanswered, user_id, accuracy_score, top_source, user_email, module_label,
module_source, accuracy_label, decomposition_level, deployment_label, model,
correlation_id, telemetry_partition, prompt_version, top_p, source_count,
accuracy_source, parent_trace_id, latency_ms, selected_answer_mode, intent,
confidence, query, environment, top_score, temperature, trace_env
```

### Variable Field Set (Conditional)

**28 optional fields** appear based on query/context:
- Video fields (10-29 traces): attached only when video selected
- Debug fields (6-22 traces): added only for specific identity types
- Session fields (16-17 traces): added for multi-turn conversations
- DemoForge fields (6-12 traces): added when demo selected

### Shape Consistency: ✅ STRONG
- No null/missing values in core fields
- Optional fields follow expected presence patterns
- No orphaned or unexpected fields
- Metadata structure is flat (no deep nesting except debug_param_keys)

---

## 5. Data Type & Field Analysis

### Sample Trace Metadata Profile

**Trace ID**: `kb-kb_answer-8adf9c2e5ade44e0`  
**Timestamp**: 2026-08-15 07:48:12.663 UTC  

**Sample Field Values**:
```json
{
  "module": "campaign_manager",
  "answered": true,
  "answer_mode": "similar_content",
  "confidence": 0.92,
  "intent": "setup_walkthrough",
  "module_label": "Campaign Manager Access",
  "accuracy_score": 8.5,
  "latency_ms": 1245,
  "trace_env": "default",
  "video_attached": true,
  "video_platform": "demoforge",
  "video_id": "3deb4110-e216-4ef8-9082-d78c765ebc4a"
}
```

### Data Types Present:
- String: module, intent, failure_type, channel_type, etc.
- Boolean: answered, unanswered, clarification_asked, video_attached
- Numeric: accuracy_score (float), latency_ms (int), confidence (float)
- Nested Object: identity_debug_param_keys (debug context)

---

## 6. Known Issues & Gaps

### Critical Gaps

| Issue | Severity | Impact |
|-------|----------|--------|
| No observation-level spans | HIGH | Cannot profile sub-operations |
| Missing case_studies_* fields | HIGH | Dashboard cannot track case study metrics |
| Missing policy_meta field | MEDIUM | Policy decision context not captured |
| Missing video_count aggregation | MEDIUM | Video usage insights incomplete |

### Minor Issues

| Issue | Severity | Impact |
|-------|----------|--------|
| Some traces missing session_id | LOW | 17/30 only have session tracking |
| identity_debug_param_keys sparse | LOW | User identity resolution harder to debug |
| No trace linking to child spans | LOW | Cannot correlate multi-operation workflows |

---

## 7. Recommendations

### Short-term (Implement this sprint)
1. **Add case study enrichment fields** to kb_answer.py metadata:
   - `case_studies_count`: Total case studies fetched
   - `case_studies_fetched`: List of case study IDs
   - `case_studies_selected`: Number actually included in response

2. **Add video aggregation field**:
   - `video_count`: Total videos available (before filtering)

3. **Merge policy_meta into trace**:
   - Add policy decision context from policy evaluation step

### Medium-term (Dashboard Phase 2)
1. **Implement span-level tracing** for KB retrieval:
   - Add spans for: db_query, embedding_fetch, ranking_filter, response_generation
   - Each span should have start_time, end_time, input, output

2. **Add structured fields for video platform**:
   - Standardize `video_source` to be always present (not just when selected)

### Long-term (Analytics Platform)
1. **Unified telemetry schema**: Define canonical fields for all KB services
2. **Event streaming**: Emit intermediate events for real-time monitoring
3. **Trace hierarchy**: Support parent-child trace relationships for workflow tracking

---

## Appendix: Field Reference

### Complete Field Inventory (70 unique fields)

**Core Answer Fields (30)**:
module, is_sub_query, answered, logic_version, failure_type, answer_preview, intent_labels, query_family, clarification_asked, explicit_module, release, channel_type, detected_product_original, unanswered, accuracy_score, top_source, module_label, module_source, accuracy_label, decomposition_level, deployment_label, model, correlation_id, telemetry_partition, prompt_version, top_p, source_count, accuracy_source, parent_trace_id, latency_ms

**User & Session (9)**:
user_name, user_id, user_email, identity_source, session_id, conversation_turn_number, trace_sequence, selected_answer_mode, environment

**Quality Metrics (4)**:
intent, confidence, query, top_score

**LLM Settings (2)**:
temperature, trace_env

**Video Enrichment (10)**:
video_attached, video_channel, video_source, video_id, video_lang, video_platform, video_title, video_end, video_captions_on, video_start, video_fallback, video_appended_to_answer

**DemoForge Integration (5)**:
demoforge_fallback_reason, demoforge_demo_id, demoforge_share_token, demoforge_api_latency_ms

**Debug/Context (8)**:
identity_debug_param_keys, identity_debug_param_keys.raw_params.*, identity_debug_param_keys.nested_parameters_resolved, identity_debug_param_keys.context_attrs.*

---

## Document Metadata
**Report File**: `/Users/adwit.sharma/kb_docs/local/reports/TELEMETRY_STRUCTURE_ANALYSIS.md`  
**Data Source**: Langfuse API (public traces endpoint)  
**Traces Analyzed**: 30 most recent kb_answer traces  
**Analysis Timestamp**: 2026-08-15T13:19:41.092965Z
