# Daily Supervisor Report Agent for gupshup_guide KB Skill

**Plan ID:** steady-weaving-robin  
**Status:** Ready for review & approval  
**Estimated effort:** 8-12 hours setup + 0.5 hours/day operational review  
**Budget:** $0 (local Qwen models, no API costs)  
**Timeline:** 1 week setup, then daily autonomous operation

---

## Context & Motivation

The gupshup_guide kb_answer skill has been validated at scale:
- Dashboard shows 72.2% answer rate (Standalone, with consulting mode)
- 2,602 real production traces analyzed
- Per-module/per-intent metrics are clean and actionable

**The opportunity:** Deploy a local **supervisor agent** (inspired by Hermes pattern) that runs **daily** to:
1. Fetch last 24 hours of traces from Langfuse
2. Identify KB gaps (IDK responses, low confidence, repeating failure patterns)
3. Group gaps by (module, intent, domain)
4. Generate **actionable report** with evidence and recommendations
5. Human (you) reviews report, forwards recommendations to respective KB teams
6. Teams implement KB changes; impact tracked on dashboard week-to-week

**Rationale:**
- Uses **local Qwen models** (no API costs, full privacy)
- **Report-only** (humans control KB changes via respective teams)
- **Daily frequency** (highest-signal failures caught immediately)
- **Zero infrastructure** (no PostgreSQL, no A/B testing, no auto-deploy)
- **Lightweight operational overhead** (~30 min/day review)

---

## Architecture: On-Demand Supervisor Loop

**Single agent, runs manually whenever you want:**

```
supervisor_agent.py (Python + Qwen proxy):
  
  INPUT:
    - Fetch NEW traces from Langfuse (only since last cached trace timestamp)
    - Append to existing langfuse_traces_cache.json (delta update)
    - All answered=TRUE and FALSE, all confidence levels
  
  PROCESS:
    1. Read existing trace cache (local/cache/langfuse_traces_cache.json)
    2. Extract timestamp of last trace in cache
    3. Fetch from Langfuse: traces.created_at > last_cached_timestamp
    4. Append new traces to cache (deduplicate by trace_id)
    5. Analyze complete dataset:
       - Calculate answer_rate by (module, intent)
       - Identify gaps: lowest answer_rate combinations
       - Identify successes: highest answer_rate combinations
    6. For each gap:
       - Extract 3-5 representative failing queries
       - Call Qwen: "Compare this failure against successful patterns. What's missing?"
       - Get root cause hypothesis
    7. Rank gaps by impact (failure count × severity)
    8. Select up to 10 gaps (if 10+ exist and severity supports it)
    9. For each gap: call Qwen to generate recommendation
       - What's missing from KB?
       - What should be added/fixed?
       - Example content
  
  OUTPUT:
    Markdown report: local/reports/supervisor_YYYYMMDD_HHMMSS.md
    Local logs: local/supervisor/logs/supervisor_YYYYMMDD_HHMMSS.log
    Updated cache: local/cache/langfuse_traces_cache.json (new traces appended)
    
    Report Format:
    ─────────────────────────────────────────────
    # Supervisor Analysis Report — YYYY-MM-DD HH:MM
    
    ## Summary
    - 2,140 traces analyzed (cumulative cache)
    - 47 new traces fetched since last run
    - 47 failures, 2,093 successes (total)
    - Overall answer rate: 71.8%
    - Top [N] gaps identified (N = 1-10, severity-driven)
    
    ## Gap #1: WhatsApp / Setup / Pricing
    **Severity:** 7 failures, 14% of WhatsApp setup queries
    **Sample failures:**
      - "What's SMS pricing in India?" → IDK
      - "Do you offer volume discounts?" → IDK
      - "SMS rate for non-GST businesses?" → IDK
    **Root cause:** KB missing pricing section (regional rates, discounts, compliance)
    **KB gap:** `kb/whatsapp/pricing.md` needs:
      - Regional pricing table (India, US, EU, etc.)
      - Volume discount tiers
      - GST compliance FAQ
    
    ## Gap #2: Bot Studio / API Node / Timeout Handling
    ... (similar structure)
    
    ## Gap #3-10: ...
    
    ## Metrics
    - Answer rate: 71.8% (baseline: 72.2%)
    - Modules most affected: WhatsApp (58%), Bot Studio (61%), General (65%)
    - Total gaps analyzed: [count]
    - Gaps selected: [N]/10
    
    ## Notes
    [Your personal observations, patterns, recommendations]
    ─────────────────────────────────────────────
  
  COST: ~$0.10-0.50/run (Qwen proxy, internal budget, no external API cost)
```

---

## Implementation: Files & Setup

```
local/supervisor/
├── __init__.py
├── supervisor_agent.py              # Main CLI entry point (argparse + orchestration)
├── config.py                        # Qwen proxy config (from .env)
├── docker-compose.yml               # Docker Compose: supervisor-agent service
├── Dockerfile                       # Container: python:3.11-slim + minimal deps
├── requirements-supervisor.txt      # Deps: requests, click, pydantic
├── logs/                            # Local log directory
│   └── (created at runtime)
├── utils/
│   ├── trace_loader.py             # Read existing cache (local/cache/langfuse_traces_cache.json)
│   ├── trace_analyzer.py           # Group by (module, intent), calculate answer rates
│   ├── gap_identifier.py           # Rank gaps by severity × volume
│   ├── report_generator.py         # Format markdown output
│   └── qwen_interface.py           # HTTP client (Qwen proxy, Bearer auth)
└── README.md                        # Setup instructions

Reports output:
  local/reports/supervisor_2026-08-28_143022.md
  local/reports/supervisor_2026-08-28_150145.md
  ... (timestamped, one per run)

Logs output:
  local/supervisor/logs/supervisor_2026-08-28_143022.log
  local/supervisor/logs/supervisor_2026-08-28_150145.log
  ... (per run, includes all Qwen calls + analysis steps)

Cache (read-write):
  local/cache/langfuse_traces_cache.json (initially from dashboard refresh, updated by supervisor with new traces)
```

**Environment Variables (.env):**
```
# Qwen Proxy (from sales-supervisor .env)
ANTHROPIC_BASE_URL=https://llmproxy.gupshup.io/
ANTHROPIC_AUTH_TOKEN=sk-Mng_Nvqv-3s8DKfvTmkHDQ
ANTHROPIC_MODEL=Qwen3-Coder-480B

# Langfuse (for delta fetch only — same credentials as skill)
LANGFUSE_PUBLIC_KEY=<your-key>
LANGFUSE_SECRET_KEY=<your-key>
LANGFUSE_HOST=https://cloud.langfuse.com

# Paths
REPORTS_DIR=local/reports
CACHE_DIR=local/cache
LOGS_DIR=local/supervisor/logs
```

### Qwen Model Integration via Company Proxy

**Configuration (from sales-supervisor):**
```
ANTHROPIC_BASE_URL=https://llmproxy.gupshup.io/
ANTHROPIC_AUTH_TOKEN=sk-Mng_Nvqv-3s8DKfvTmkHDQ
ANTHROPIC_MODEL=Qwen3-Coder-480B
ANTHROPIC_TEMPERATURE=0.3
ANTHROPIC_MAX_TOKENS=1500
```

**Access Pattern:**
- HTTP POST to `{ANTHROPIC_BASE_URL}/v1/chat/completions` (OpenAI-compatible)
- Authentication: Bearer token in Authorization header
- Request format:
```python
headers = {
    "Authorization": f"Bearer {ANTHROPIC_AUTH_TOKEN}",
    "Content-Type": "application/json",
}
payload = {
    "model": ANTHROPIC_MODEL,
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.3,
    "max_tokens": 1500,
}
```

**Reusable LLM Client Pattern** (from `hermes/workers/interview.py`):
```python
def call_llm_api(prompt: str, max_tokens: int = 1500, temperature: float = 0.3) -> Optional[str]:
    """Call Gupshup LLM proxy via HTTPS. Returns response text or None on failure."""
    try:
        headers = {
            "Authorization": f"Bearer {ANTHROPIC_AUTH_TOKEN}",
            "Content-Type": "application/json",
        }
        data = {
            "model": ANTHROPIC_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        url = f"{ANTHROPIC_BASE_URL}/v1/chat/completions"
        resp = requests.post(url, json=data, headers=headers, timeout=60)
        resp.raise_for_status()
        message = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        return message or None
    except Exception as exc:
        logger.error(f"LLM API call failed: {exc}")
        return None
```

---

## Docker Setup & Deployment

**docker-compose.yml (for KB supervisor):**
```yaml
version: '3.8'

services:
  supervisor-agent:
    build:
      context: .
      dockerfile: ./local/supervisor/Dockerfile
    container_name: kb-supervisor
    environment:
      - ANTHROPIC_BASE_URL=https://llmproxy.gupshup.io/
      - ANTHROPIC_AUTH_TOKEN=${ANTHROPIC_AUTH_TOKEN}
      - ANTHROPIC_MODEL=Qwen3-Coder-480B
      - LOG_DIR=/logs
      - REPORTS_DIR=/reports
      - CACHE_DIR=/cache
    volumes:
      - ./local/reports:/reports              # Output markdown reports
      - ./local/supervisor/logs:/logs         # Local supervisor logs
      - ./local/cache:/cache                  # Trace cache (read-only, shared with dashboard)
    working_dir: /app
    command: python3 -m local.supervisor.supervisor_agent --report
```

**Dockerfile (local/supervisor/Dockerfile):**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements-supervisor.txt .

# Install deps: requests (LLM proxy), click (CLI), pydantic (validation)
RUN pip install --no-cache-dir -r requirements-supervisor.txt

# Copy project
COPY local/supervisor ./local/supervisor
COPY local/cache ./local/cache
COPY skill ./skill

# Create log directory
RUN mkdir -p ./local/supervisor/logs

# Non-root user (hardening)
RUN useradd -m supervisor && chown -R supervisor:supervisor /app
USER supervisor

# Run supervisor agent on-demand
ENTRYPOINT ["python3"]
CMD ["-m", "local.supervisor.supervisor_agent", "--report"]
```

**requirements-supervisor.txt:**
```
requests==2.31.0
langfuse==2.1.0
python-dotenv==1.0.0
click==8.1.3
pydantic==2.0.0
```

## Manual Workflow

### When You Want (On-Demand):
```bash
# Option 1: Run via Docker Compose (recommended)
cd local/supervisor && docker-compose up --build supervisor-agent

# Option 2: Run directly (no Docker)
python3 local/supervisor/supervisor_agent.py --report

# Option 3: Run with custom options
python3 local/supervisor/supervisor_agent.py --report --max-gaps 10 --min-severity 0.5
```

This triggers:
  - Read existing trace cache (local/cache/langfuse_traces_cache.json)
  - Extract timestamp of last cached trace
  - Fetch new traces from Langfuse (since last cached timestamp)
  - Append new traces to cache (deduplicate by trace_id)
  - Analyze complete dataset (all cached traces)
  - Call Qwen for gap analysis + recommendations
  - Save updated cache to local/cache/langfuse_traces_cache.json
  - Save markdown report to local/reports/supervisor_YYYYMMDD_HHMMSS.md
  - Save logs to local/supervisor/logs/supervisor_YYYYMMDD_HHMMSS.log
  - Print summary to console

**Output:**
```
✓ Cache loaded: 2,093 traces
✓ New traces fetched: 47 (since last run)
✓ Cache updated: 2,140 traces total
✓ Gaps identified: 47 total, 8 selected (severity-driven)
✓ Report saved: local/reports/supervisor_2026-08-28_143022.md
✓ Logs saved: local/supervisor/logs/supervisor_2026-08-28_143022.log
```

**Key:** No time-based cutoff — always fetches everything since last cached timestamp. Works whether you run supervisor daily, weekly, or irregularly.

### After Running (Async, No Timeline Pressure):
```
Whenever you have time:
  - Read local/reports/supervisor_YYYYMMDD_HHMMSS.md
  - Identify actionable gaps
  - Forward to respective KB teams:
    - WhatsApp team: "Gap #1: pricing docs need expansion"
    - Bot Studio team: "Gap #2: add error handling section"
    - etc.
  - Track implementations (spreadsheet, GitHub issues, or notes)
  
Weekly (or whenever):
  - Refresh dashboard (already automated)
  - Compare answer rate before/after team implementations
  - Measure which recommendations had impact
  - Identify patterns (same teams repeatedly? same gaps resurface?)
  
Note: No pressure to run daily. Run whenever makes sense for you — could be 2-3 times/week, or daily if your laptop is on. Agent adapts to whatever cadence you want.
```

---

## Report Structure & Content

Each daily report includes:

1. **Summary Section:**
   - Total failures captured (24h)
   - Top 5 gaps identified
   - Which teams affected
   - Trend vs yesterday (up/down in answer rate)

2. **Per-Gap Sections:**
   - Gap title: `[Module] / [Intent] / [Domain]`
   - Severity: count + % of module traffic affected
   - Root cause hypothesis (what's missing?)
   - 3-5 example failing queries
   - Recommendation for KB team (what to add/fix)
   - Suggested content (example: "Add section: X, include: Y, FAQ: Z")

3. **Metrics This Round:**
   - Answer rate today vs 7-day average
   - Confidence score today vs baseline
   - Modules most affected (sorted by failure count)

4. **Action Items Checklist:**
   - Checkboxes per team: `[ ] WhatsApp: Review Gap #1`

5. **Tracking Links:**
   - Dashboard link (to measure impact)
   - Prior supervisor reports (see history)

---

## Success Criteria & Measurement

### Week 1 (Setup):
- ✅ Qwen model configured and tested locally
- ✅ Supervisor agent runs on-demand via `bash local/supervisor/run.sh`
- ✅ 3+ reports generated, readable format (no errors)
- ✅ Cache integration working (traces appended correctly)

### Week 2+ (Ongoing):
- ✅ Reports generated on-demand with consistent quality
- ✅ Gaps identified are **actionable** (teams can implement)
- ✅ Recommendations are **specific** (not vague, include example content)
- ✅ After teams implement top recommendations, answer rate improves by 1-2% per report cycle
- ✅ Repeated gaps → identify systematic issues (broken retrieval? missing chunk? poor prompt fit?)

### Monthly Review:
- Answer rate: 72.2% → target 75%+ (month 1), 78%+ (month 2)
- Gap categories: Which types repeated most? (pricing → retrieval issue? vs API nodes → feature gap?)
- Team responsiveness: Which teams acted fastest? Which gaps stalled?

---

## Known Assumptions & Constraints

| Item | Status |
|------|--------|
| KB updates come from respective teams (not auto-deploy) | ✅ You manage |
| Qwen model available in sales-supervisor .env | ✅ Reuse existing |
| Langfuse API access (already in place for dashboard) | ✅ Reuse existing |
| No PostgreSQL, no A/B testing infrastructure | ✅ Simpler |
| No auto-rollback / circuit breakers needed | ✅ Reports only |
| Human reviews report daily (async, ~30 min/day) | ✅ You manage |

---

## Critical Files & Locations

**This project (gupshup_guide):**
- `skill/kb_answer.py` — Main skill (read-only)
- `local/cache/langfuse_traces_cache.json` — Trace cache (reuse for supervisor)
- `local/reports/supervisor_YYYYMMDD.md` — Daily reports (new)

**Sales-supervisor (reference, for Qwen model):**
- `.env` — QWEN_MODEL_PATH, model config
- `hermes/` — Qwen integration (reference, adapt for local inference)

---

## Reuse from sales-supervisor

Minimal reuse, focused on infrastructure only:

| Aspect | Sales Supervisor | KB Supervisor |
|--------|------------------|---------------|
| LLM | Claude API + Qwen (proxy-based) | Qwen proxy only |
| Trace storage | PostgreSQL (complex) | Read-only cache (simple) |
| Tracing | Langfuse + local logs | Local logs only |
| Deployment | Auto via CI/CD | Manual via Docker |
| Effort | 2-3 hours/week | ~30 min/run |

**Code to copy:**

1. **Qwen HTTP Client** (Bearer auth + OpenAI-compatible API)
   - Source: `/Users/adwit.sharma/sales supervisor/hermes/workers/interview.py:43-68` (`call_llm_api()`)
   - Copy as-is: bearer token auth, `/v1/chat/completions`, 60s timeout, markdown fence stripping
   - No changes needed (pattern proven in production)

2. **Docker Setup** (python:3.11-slim, non-root user)
   - Source: `/Users/adwit.sharma/sales supervisor/Dockerfile`
   - Adapt: Remove FastAPI/uvicorn, keep base image + non-root user + env var injection
   - Simpler: Just Python CLI entry point, no HTTP API

3. **Environment Variable Pattern**
   - Source: sales-supervisor `.env.example` + `load_dotenv(override=True)` in scripts
   - Copy: Same `ANTHROPIC_*` vars, same override pattern
   - Know why: Claude Code sets its own ANTHROPIC_* for local development → must override

**What NOT to reuse:**
- ❌ Langfuse SDK (unused here — no telemetry load)
- ❌ PostgreSQL (unused here — stateless agent)
- ❌ FastAPI/uvicorn (unused here — CLI only)

---

## Open Questions for User Approval

1. **Gap count per report:** Top 5 gaps? Top 10?
   - **Recommendation:** Top 5-8 (actionable, not overwhelming)

2. **Low-confidence threshold:** Include all traces or filter low-signal queries?
   - Include all traces (complete signal)?
   - Or exclude very low confidence (<3.0)?
   - **Recommendation:** Include all (better for comparative analysis)

3. **Report retention:** Save all reports to git?
   - Or keep locally, archive periodically?
   - **Recommendation:** Commit reports to git (one per run, full history)

4. **Team routing:** How do you want to forward recommendations?
   - Email to teams?
   - GitHub issues in kb/ repo?
   - Slack message?
   - Just read locally and manage yourself?
   - **Recommendation:** You decide based on priority (manual routing)

---

## Next Steps (Upon Approval)

### Phase 1: Setup (2-3 hours)
1. User approves plan + Docker approach
2. Create `local/supervisor/` folder structure:
   - `supervisor_agent.py` (CLI entry point, argparse)
   - `config.py` (load ANTHROPIC_* from .env with override)
   - `Dockerfile` + `docker-compose.yml` + `requirements-supervisor.txt`
   - `logs/` directory (created at runtime)
   - `utils/` subdirectory with 4 modules:
     - `qwen_interface.py` (HTTP POST client, Bearer auth, copy from sales-supervisor)
     - `trace_loader.py` (read `local/cache/langfuse_traces_cache.json`)
     - `trace_analyzer.py` (group by module×intent, calculate answer_rate)
     - `gap_identifier.py` (rank gaps by severity×volume, select up to 10)
     - `report_generator.py` (format markdown)

3. Implement `qwen_interface.py` — copy `call_llm_api()` from sales-supervisor as-is

4. Implement `trace_loader.py`:
   - Read JSON cache file (local/cache/langfuse_traces_cache.json)
   - Extract last trace timestamp (if cache exists)
   - Fetch new traces from Langfuse SDK: `traces.startTime > last_timestamp`
   - Append new traces to cache (deduplicate by trace_id)
   - Write updated cache back to file
   - Parse all traces (module, intent, answered, confidence, query, response)
   - Return structured data (complete dataset)

5. Implement `trace_analyzer.py`:
   - Group traces by (module, intent)
   - Calculate: success_count, failure_count, answer_rate, avg_confidence
   - Return ranked list of combinations

6. Implement `gap_identifier.py`:
   - Sort by answer_rate ascending
   - Calculate severity score (failure_count × volume_impact)
   - Select top N gaps where N = min(10, count of gaps above severity threshold)
   - For each gap: extract 3-5 failing queries

7. Implement `report_generator.py`:
   - For each gap: call Qwen with gap details + successful examples
   - Parse Qwen response → recommendation markdown
   - Aggregate into final report

8. Implement `supervisor_agent.py`:
   - argparse: `--report` (main), `--max-gaps 10`, `--min-severity 0.5`
   - Load config (ANTHROPIC_* from .env)
   - Call trace_loader → trace_analyzer → gap_identifier → report_generator
   - Write report to `local/reports/supervisor_YYYYMMDD_HHMMSS.md`
   - Write logs to `local/supervisor/logs/supervisor_YYYYMMDD_HHMMSS.log`

### Phase 2: Testing (1-2 hours)
1. Test locally (no Docker):
   ```bash
   python3 local/supervisor/supervisor_agent.py --report
   ```
   - Verify cache loads correctly
   - Verify Qwen calls succeed (Bearer auth, timeouts)
   - Verify report markdown is readable
   - Check logs for any errors

2. Test via Docker:
   ```bash
   cd local/supervisor && docker-compose up --build supervisor-agent
   ```
   - Verify volume mounts work (reports + logs written)
   - Verify environment vars passed correctly
   - Verify non-root user execution

### Phase 3: Deployment & Monitoring (Week 1)
1. Commit plan + all code to git (to `local/supervisor/`)
2. Run supervisor manually 3-5 times via Docker
3. Review first few reports — refine gap detection + Qwen prompts if needed
4. Iterate on analyzer logic based on real data quality
5. Once satisfied → ready for operational use

### Manual Execution (Ongoing)
- Run whenever you want: `cd local/supervisor && docker-compose up --build supervisor-agent`
- Read report + logs locally
- Forward recommendations to KB teams manually

---

**Status:** Plan complete. Ready for implementation approval.
