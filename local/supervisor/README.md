# KB Supervisor Agent

On-demand KB gap analysis and recommendations using Qwen LLM and Langfuse trace data.

## Overview

The supervisor agent:
1. Fetches new traces from Langfuse (delta since last run)
2. Appends to local cache (cumulative dataset)
3. Groups traces by (module, intent)
4. Calculates answer rates and identifies gaps
5. Calls Qwen LLM for root-cause analysis
6. Generates markdown report with recommendations

**Key:** No time-based cutoff — fetches everything since last cached timestamp. Works whether you run supervisor daily, weekly, or irregularly.

## Quick Start

### Direct Python (Recommended)

```bash
cd /Users/adwit.sharma/kb_docs
python3 -m local.supervisor.supervisor_agent --report
```

Output:
- Report: `local/reports/supervisor_<timestamp>.md`
- Logs: `local/supervisor/logs/supervisor_<timestamp>.log`
- Cache: `local/cache/langfuse_traces_cache.json` (updated if new traces fetched)

### Via Docker

Docker image is pre-built and can be used for CI/CD or remote execution:

```bash
cd local/supervisor
docker-compose run --rm supervisor-agent --report
```

Note: Docker volume mounts work best when cache is pre-populated locally.

### Custom Options

```bash
python3 -m local.supervisor.supervisor_agent --report --max-gaps 10 --min-severity 0.5
```

## Configuration

### Environment Variables (.env)

```bash
# Qwen Proxy (from sales-supervisor .env)
ANTHROPIC_BASE_URL=https://llmproxy.gupshup.io/
ANTHROPIC_AUTH_TOKEN=sk-Mng_Nvqv-3s8DKfvTmkHDQ
ANTHROPIC_MODEL=Qwen3-Coder-480B

# Langfuse (for trace fetching, same as skill)
LANGFUSE_PUBLIC_KEY=<your-key>
LANGFUSE_SECRET_KEY=<your-key>

# Optional: Defaults are sensible
# ANTHROPIC_TEMPERATURE=0.3
# ANTHROPIC_MAX_TOKENS=1500
# QWEN_TIMEOUT_SECONDS=60
# MAX_GAPS=10
# MIN_SEVERITY=0.0
```

### Paths

- **Reports:** `local/reports/supervisor_<timestamp>.md`
- **Logs:** `local/supervisor/logs/supervisor_<timestamp>.log`
- **Cache:** `local/cache/langfuse_traces_cache.json` (shared with dashboard)

## Architecture

### Input
- Langfuse traces via SDK (delta fetch from last cached timestamp)
- Local trace cache (JSON, pre-populated by dashboard refresh)

### Process
1. **TraceLoader** — Read cache, extract last timestamp, fetch new traces, append
2. **TraceAnalyzer** — Group by (module, intent), calculate metrics (answer_rate, confidence)
3. **GapIdentifier** — Rank by severity, select top N gaps
4. **ReportGenerator** — Call Qwen for gap analysis, format markdown

### Output
- Markdown report with Qwen analysis (root cause, KB gap, recommendation)
- Local logs (structured, per run)
- Updated cache (new traces appended)

## Report Format

```markdown
# KB Supervisor Analysis Report

## Summary
- Traces Analyzed: N
- Total Failures: N
- Overall Answer Rate: X%
- Gaps Identified: N

## Gap #1: Module / Intent
**Severity:** N failures, X% answer rate
**Sample Failures:**
- Query 1
- Query 2

**Root Cause:** [From Qwen]
**KB File:** `kb/module/intent.md`
**Recommendation:** [From Qwen]

## Metrics
**Modules Most Affected:**
- Module A: X% answer rate
- Module B: Y% answer rate

## Action Items
- [ ] Gap #1: Module team - Review and implement
- [ ] Gap #2: Module team - Review and implement
```

## Troubleshooting

### No Traces Found
- Verify `local/cache/langfuse_traces_cache.json` exists (run dashboard refresh first)
- Check Langfuse credentials in `.env`

### Qwen LLM Calls Failing
- Verify `ANTHROPIC_AUTH_TOKEN` is set correctly
- Check `ANTHROPIC_BASE_URL` is reachable
- Increase `QWEN_TIMEOUT_SECONDS` if network is slow

### Docker Build Issues
- Ensure `.env` file exists in project root
- Verify `local/cache/` directory exists
- Check Docker is running: `docker ps`

### Viewing Logs
```bash
# Latest supervisor logs
tail -f local/supervisor/logs/supervisor_*.log

# Or from within container
docker logs kb-supervisor
```

## Files

```
local/supervisor/
├── __init__.py
├── config.py                    # Settings management
├── supervisor_agent.py          # Main CLI entry point
├── Dockerfile                   # Container image
├── docker-compose.yml           # Docker Compose config
├── requirements-supervisor.txt  # Python dependencies
├── README.md                    # This file
├── logs/                        # Logs directory (created at runtime)
└── utils/
    ├── __init__.py
    ├── qwen_interface.py        # Qwen LLM client (Bearer auth)
    ├── trace_loader.py          # Langfuse fetch + cache management
    ├── trace_analyzer.py        # Group traces, calculate metrics
    ├── gap_identifier.py        # Rank and select top gaps
    └── report_generator.py      # Format markdown + call Qwen
```

## Development

### Install dependencies locally
```bash
pip install -r local/supervisor/requirements-supervisor.txt
```

### Run directly (for testing)
```bash
python3 local/supervisor/supervisor_agent.py --report --max-gaps 5 --min-severity 0.0
```

### View logs
```bash
tail -f local/supervisor/logs/supervisor_*.log
```

## Production Deployment

- **Manual Execution:** Run `docker-compose up` whenever you want analysis
- **Scheduled (Future):** Can add cron job or CI/CD trigger
- **No Auto-Deploy:** Recommendations are local; KB updates managed by teams

## Cost & Resources

- **Qwen API:** Internal proxy cost (included in company budget)
- **Compute:** ~1GB RAM, 1 CPU (configurable in docker-compose.yml)
- **Execution Time:** ~2-5 minutes per run (depends on gap count and Qwen latency)
- **Storage:** Cache grows with trace count (~few MB per 1000 traces)

## Next Steps

1. Ensure `.env` file has Langfuse + Qwen credentials
2. Run dashboard refresh to populate initial cache
3. Execute supervisor: `docker-compose up --build supervisor-agent`
4. Review report in `local/reports/`
5. Forward recommendations to respective KB teams
