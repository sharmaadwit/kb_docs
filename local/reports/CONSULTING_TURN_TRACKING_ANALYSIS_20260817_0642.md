# Consulting Mode + Turn-Tracking Fix Analysis (Broadened)

Generated: 2026-08-17T06:42:00.647090+00:00
Scope: ALL traces carrying the new turn-tracking fields (session_id_source, turn_number_source,
parent_trace_id_provided) — this is a natural post-fix boundary, no manual date/identity filter needed.
Source: local trace cache (2404 total traces, 90-day backfill).

## Sample size
- Post-fix traces (have new fields): **8**
- Real-email traces: 5
- Scrubbed/missing-email traces: 3

## Field coverage (confirms fix is deployed and behaving as designed)
- session_id_source = "client": 25.0%
- session_id_source = "correlation_fallback": 75.0%
- turn_number_source = "client": 0.0%
- turn_number_source = "missing_client_support": 100.0%
- parent_trace_id_provided = true: 0.0%

## Overall answer quality (post-fix traffic)
- Answer rate: 75.0%
- Avg confidence: 0.5483

## Answer mode split
{
  "consulting": 1,
  "standard": 7
}

## Consulting vs Standard mode
- Consulting: n=1 (12.5% adoption)
- Standard: n=7
- Consulting answer rate: 0.0%
- Standard answer rate: 85.7%
- Consulting avg confidence: 0.3824
- Standard avg confidence: 0.572

## trace_env split
{
  "PROD_EXT": 5,
  "PROD": 3
}

## Conversation clustering (real-email traces only, email + 10-min proximity)
- Unique real emails: 1
- Total clusters: 1
- Multi-turn clusters (2+): 1
- First-position: n=1, answered=100.0%, avg_conf=0.5333
- Later-position: n=4, answered=50.0%, avg_conf=0.4265
