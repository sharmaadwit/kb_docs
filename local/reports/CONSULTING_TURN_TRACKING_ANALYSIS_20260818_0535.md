# Consulting Mode + Turn-Tracking Fix Analysis (Broadened)

Generated: 2026-08-18T05:35:31.884915+00:00
Scope: ALL traces carrying the new turn-tracking fields (session_id_source, turn_number_source,
parent_trace_id_provided) — this is a natural post-fix boundary, no manual date/identity filter needed.
Source: local trace cache (2469 total traces, 90-day backfill).

## Sample size
- Post-fix traces (have new fields): **73**
- Real-email traces: 22
- Scrubbed/missing-email traces: 51

## Field coverage (confirms fix is deployed and behaving as designed)
- session_id_source = "client": 41.1%
- session_id_source = "correlation_fallback": 58.9%
- turn_number_source = "client": 0.0%
- turn_number_source = "missing_client_support": 100.0%
- parent_trace_id_provided = true: 0.0%

## Overall answer quality (post-fix traffic)
- Answer rate: 80.8%
- Avg confidence: 0.5172

## Answer mode split
{
  "consulting": 23,
  "standard": 50
}

## Consulting vs Standard mode
- Consulting: n=23 (31.5% adoption)
- Standard: n=50
- Consulting answer rate: 87.0%
- Standard answer rate: 78.0%
- Consulting avg confidence: 0.5621
- Standard avg confidence: 0.4966

## trace_env split
{
  "PROD_EXT": 21,
  "PROD": 51,
  "INT": 1
}

## Conversation clustering (real-email traces only, email + 10-min proximity)
- Unique real emails: 9
- Total clusters: 12
- Multi-turn clusters (2+): 5
- First-position: n=5, answered=100.0%, avg_conf=0.4693
- Later-position: n=10, answered=80.0%, avg_conf=0.4878
