# Code Fix Effectiveness Analysis

Generated: 2026-08-17T06:13:53.704931+00:00
Scope: real-identity traces only (scrubbed/placeholder emails excluded), last 4 days
Fix: commit a60b9e49 (session_id/turn_number/parent_trace_id provenance), assumed live from ~2026-08-17T05:00:00+00:00

## Sample sizes
- Total kb_answer traces scanned: 600
- Real-email traces in window: 246
- Pre-fix (in window, before deploy): 216
- Post-fix: 30

## Post-fix field coverage (real-identity traffic only)
- session_id_source = "client": 0.0%
- session_id_source = "correlation_fallback": 100.0%
- turn_number_source = "client": 0.0%
- turn_number_source = "missing_client_support": 100.0%
- parent_trace_id_provided = true: 0.0%
- Answered rate: 60.0%
- Avg confidence: 0.4479
- Answer mode split: {'consulting': 6, 'standard': 24}

## Pre-fix comparison (same window, real-identity traffic)
- Answered rate: 52.8%
- Avg confidence: 0.3816
- Answer mode split: {'standard': 186, 'setup': 6, 'consulting': 18, 'overview': 6}

## Email-based conversation clustering (post-fix, real identity — clean signal, no PII-scrubbing noise)
- Unique real emails: 1
- Total conversation clusters (10-min proximity): 1
- Multi-turn clusters (2+): 1
- First-position traces: 1 | answered rate: 100.0% | avg confidence: 0.5333
- Later-position traces: 29 | answered rate: 58.6% | avg confidence: 0.4449
