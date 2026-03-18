# Runtime Redesign Plan

Goal: reduce dependence on growing exact-case patches in `kb_answer.py` and move toward a stable runtime that generalizes across paraphrases without turning into a brittle rule engine.

## Constraints

- Do not make large behavior changes in one step.
- Ship in small phases with regression gates after each phase.
- Keep the current patched runtime as the baseline until replacements are proven.
- Prefer architectural seams over immediate routing changes.

## Current Runtime Shape

- `kb_ingest.py`
- `kb_search.py`
- `kb_answer.py`
- `kb_analytics.py`

Recommended long-term ownership:

- `kb_ingest.py`: chunk quality, metadata enrichment, page typing
- `kb_search.py`: retrieval and ranking
- `kb_answer.py`: intent detection, evidence assembly, answer formatting
- `kb_analytics.py`: evaluation and debug metrics

## Problem Summary

The current runtime is overusing exact-case handling as the main accuracy lever. That helps short-term regressions but creates these issues:

- fragile paraphrase handling
- repeated answer text and duplicated logic
- compare-style questions handled as one-offs
- cross-module troubleshooting handled via string matching instead of intent
- `kb_answer` compensating for weak retrieval and weak ranking
- `kb_search` lagging well behind `kb_answer`

## Target Runtime Pipeline

The redesigned runtime should look like this:

1. query normalization
2. intent-family detection
3. retrieval and ranking
4. evidence bundle assembly
5. answer composition
6. clarification or fallback

Today, too much logic is compressed into step 5.

## Baseline Before Redesign

Keep the current local patched version as the baseline and preserve artifacts for:

- `regression_250`
- `regression_500`
- `regression_1000`
- local `18` paraphrase set
- focused `150` weak-topic bundle

Every phase below should compare against these.

## Intent Families

Start with a small set of intent families instead of many page-specific exact-cases:

- `exact_page`
- `which_node`
- `general_how_to`
- `compare_pages`
- `cross_module_troubleshooting`
- `analytics_decision`
- `troubleshooting`
- `unsupported_or_unknown`

These should become the main routing layer for most supported questions.

## Phased Plan

### Phase 0: Freeze Baseline

Purpose:
- make redesign measurable

Tasks:
- keep the current local patched runtime unchanged
- save baseline metrics for all core regressions
- note which current wins are from exact-cases versus more general behavior

Acceptance:
- reproducible baseline numbers exist before refactor work starts

### Phase 1: Intent Signals Layer

Purpose:
- add architectural structure without changing behavior

Files:
- `kb_answer.py`

Tasks:
- add `_query_signals(query)`
- add `_detect_intent_family(query)`
- add `_build_query_context(query)`
- compute them inside `kb_answer()`
- do not use them to change answer routing yet

Acceptance:
- no behavior drift
- same results on `regression_250`, `18`, and `150`

### Phase 2: Formatter Extraction

Purpose:
- reduce duplicated answer text and repetitive formatting logic

Files:
- `kb_answer.py`

Tasks:
- extract repeated formatters such as:
  - `_format_exact_page_answer(...)`
  - `_format_compare_answer(...)`
  - `_format_node_choice_answer(...)`
  - `_format_troubleshooting_answer(...)`
  - `_format_partial_doc_answer(...)`
- replace repeated inline strings with helper calls
- do not change routing logic

Acceptance:
- answers remain functionally unchanged
- no drop on `250`, `18`, or `150`

### Phase 3: Evidence Bundle Assembly

Purpose:
- stop composing answers directly from raw chunk lines

Files:
- `kb_answer.py`

Tasks:
- create a small evidence normalizer from selected chunks
- each evidence object should capture:
  - `page_slug`
  - `page_title`
  - `module`
  - `page_type`
  - `concepts`
  - `confidence`
- answer formatting should begin to consume evidence objects rather than raw lines

Acceptance:
- exact-page answers stay stable
- evidence objects are inspectable in local debug

### Phase 4: Compare and Cross-Module Handlers

Purpose:
- remove the highest-volume exact-case sprawl

Files:
- primarily `kb_answer.py`

Target themes:
- `Business Hours` vs `Auto Replies`
- `Test your Bot` vs `Save Vs Save & Deploy`
- `Campaign Analytics` vs `Goal Analytics`
- `Assignment Rules` + `Agent Transfer Node`
- `Webhooks` vs `Response file` / `Link Tracking Report`

Tasks:
- add reusable compare handlers
- add reusable cross-module troubleshooting handlers
- migrate repeated compare-style exact-cases into these handlers

Acceptance:
- local `18` paraphrase set stays green
- focused `150` weak-topic bundle stays green
- compare logic moves out of one-off exact-case blocks

### Phase 5: Retrieval and Ranking Redesign

Purpose:
- fix the real root cause behind answer-layer hardcoding

Files:
- `kb_search.py`
- possibly metadata improvements in `kb_ingest.py`

Tasks:
- make ranking aware of intent family
- support multi-page evidence bundles
- reward complementary page pairs for compare questions
- reward module-pair evidence for cross-module troubleshooting
- downrank visually similar but semantically wrong pages

Key pair targets:
- `Business Hours` + `Auto Replies`
- `Test your Bot` + `Save Vs Save & Deploy`
- `Campaign Analytics` + `Goal Analytics`
- `Assignment Rules` + `Agent Transfer Node`

Acceptance:
- `kb_search` accuracy improves materially on `500` and `1000`
- not just `kb_answer`

### Phase 6: Exact-Case Reduction

Purpose:
- shrink the brittle rules layer after replacement logic is proven

Files:
- `kb_answer.py`

Tasks:
- remove exact-cases that are fully covered by:
  - compare handler
  - node-selection handler
  - analytics-decision handler
  - cross-module troubleshooting handler
- keep only:
  - safety and guardrail exceptions
  - truly ambiguous documentation cases
  - a small number of precision exceptions

Acceptance:
- exact-case count is reduced
- no regression on `250`, `500`, or `1000`

### Phase 7: Clarification Strategy

Purpose:
- replace premature `I don’t know` with structured partial answers and focused follow-ups

Files:
- `kb_answer.py`

Tasks:
- add clarification path selection
- prefer:
  1. direct answer
  2. compare answer
  3. partial answer plus follow-up
  4. unknown
- use partial-doc answers when evidence is adjacent but incomplete

Acceptance:
- fewer dead-end unknowns
- no hallucinated completions

### Phase 8: Analytics and Debuggability

Purpose:
- make future failures easier to diagnose

Files:
- `kb_analytics.py`

Tasks:
- add internal debug-only metrics:
  - detected intent family
  - selected evidence pages
  - whether compare handler was used
  - whether clarification path was used
- keep user-facing telemetry changes out of scope unless explicitly requested later

Acceptance:
- easier diagnosis of regressions without changing user-facing behavior

## Test Gates

### Gate A
After Phase 1 and Phase 2:

- `regression_250`
- local `18` paraphrase set
- focused `150` weak-topic bundle

Expectation:
- no behavior change

### Gate B
After Phase 3 and Phase 4:

- `regression_250`
- local `18`
- focused `150`

Expectation:
- same or better than baseline

### Gate C
After Phase 5:

- `regression_500`
- `regression_1000`

Expectation:
- meaningful `kb_search` improvement

### Gate D
After Phase 6 and Phase 7:

- `regression_250`
- `regression_500`
- `regression_1000`
- local `18`
- focused `150`

Expectation:
- fewer exact-cases
- no material accuracy drop

## Recommended Subtask Order

Best execution order:

1. Phase 0
2. Phase 1
3. Phase 2
4. Phase 3
5. Phase 4
6. Phase 5
7. Phase 6
8. Phase 7
9. Phase 8

## What Not To Do

- do not redesign ingest first
- do not touch retrieval before intent and evidence seams exist
- do not remove exact-cases before replacement handlers are proven
- do not validate only one regression set
- do not let `kb_answer.py` grow more one-off routing branches while redesign is in progress

## Immediate Next Step

Implement Phase 1 only:

- add query signal helpers
- add intent-family detection
- wire them in read-only mode
- confirm no behavior drift on `250`, `18`, and `150`

This is the safest first move because it creates the future architecture without changing live answer behavior.
