# Test Video Matching Script

## Overview

`test_video_matching.py` generates fresh traces through the kb_answer skill to test if DemoForge video selection now matches module intent correctly.

## Test Coverage

The script tests **15 queries** across **5 key modules**:

### 1. Bot Studio (3 queries)
- Overview: "What is Bot Studio and how do I use it?"
- How-to: "How do I create a bot using Bot Studio?"
- How-to: "How do I set up bot flows and integrate them?"

### 2. CTX / Click-to-Chat (3 queries)
- Overview: "What is Click-to-Chat and how does it work?"
- How-to: "How do I implement Click-to-Chat on my website?"
- Setup: "How do I set up Click-to-Chat for lead generation?"

### 3. AI Admin (3 queries)
- Overview: "What is AI Admin and what can I do with it?"
- How-to: "How do I configure AI models in AI Admin?"
- Setup: "How do I set up admin controls and permissions?"

### 4. Campaign Manager (3 queries)
- Overview: "What is Campaign Manager and how does it work?"
- How-to: "How do I create and execute a campaign in Gupshup?"
- Setup: "How do I set up campaign scheduling and targeting?"

### 5. Personalize (3 queries)
- Overview: "What is the Personalize module and how does personalization work?"
- How-to: "How do I personalize messages for different user segments?"
- Setup: "How do I set up dynamic content personalization rules?"

## Usage

### Basic run (silent)
```bash
cd /Users/adwit.sharma/kb_docs
python3 local/scripts/test_video_matching.py
```

### Verbose mode (detailed output for each query)
```bash
python3 local/scripts/test_video_matching.py --verbose
```

### With output file
```bash
python3 local/scripts/test_video_matching.py --output-file local/reports/video_matching_results.json
```

### Limit queries
```bash
python3 local/scripts/test_video_matching.py --limit 5
```

### Combined
```bash
python3 local/scripts/test_video_matching.py --verbose --output-file local/reports/video_matching_results.json --limit 10
```

## What It Does

1. **Executes each test query** through kb_answer skill via MockContext
2. **Captures response metadata** including:
   - Video title and platform (YouTube, DemoForge, etc.)
   - DemoForge demo ID and name (if matched)
   - DemoForge API latency
   - Fallback reason (if applicable)
   - Query latency
3. **Generates correlation IDs** for Langfuse trace lookup
4. **Prints structured output** with query results and video matches
5. **Optionally writes JSON report** for detailed analysis

## Output Format

### Console Output
```
[1] BOT STUDIO - OVERVIEW
✓ Query executed successfully
  Status: success
  Latency: 245.3ms
  Video: Bot Studio Overview (demoforge)
  DemoForge Demo: Bot Studio - Create a Bot (ID: demo_123)
  DemoForge API Latency: 150ms
  Langfuse Trace: trace_abc123
  Correlation ID: video_match_bot_studio_overview_1_1234567890_a1b2c3d4
```

### JSON Output (with `--output-file`)
```json
{
  "timestamp": "2026-07-03T10:36:00Z",
  "test_run_summary": {
    "total_queries": 15,
    "successful": 15,
    "failed": 0,
    "with_video": 12,
    "with_demoforge": 8
  },
  "results": [
    {
      "index": 1,
      "module": "Bot Studio",
      "intent": "overview",
      "query": "What is Bot Studio and how do I use it?",
      "status": "success",
      "video_attached": true,
      "video_title": "Bot Studio Overview",
      "video_platform": "demoforge",
      "demoforge_demo_name": "Bot Studio - Create a Bot",
      "demoforge_api_latency_ms": 150,
      "correlation_id": "video_match_bot_studio_overview_1_1234567890_a1b2c3d4",
      "langfuse_trace_id": "trace_abc123",
      "latency_ms": 245.3
    }
    // ... more results
  ],
  "modules": {
    "Bot Studio": {
      "total": 3,
      "with_video": 2,
      "with_demoforge": 1
    }
    // ... more modules
  }
}
```

## Langfuse Trace Lookup

After running the script, use the printed correlation IDs to fetch traces:

```bash
# Look up a single trace
lf traces --filter 'correlation_id=video_match_bot_studio_overview_1_1234567890_a1b2c3d4'

# Or search in Langfuse UI
# https://cloud.langfuse.com
# Search by correlation_id tag
```

## Verification Checklist

After running the test:

- [ ] All 15 queries executed successfully
- [ ] Video metadata captured for expected modules
- [ ] DemoForge demos matched for appropriate intents
- [ ] Correlation IDs appear in Langfuse traces
- [ ] Video titles match module context
- [ ] DemoForge API latency is reasonable (<500ms)
- [ ] No error responses or fallback failures

## Environment Requirements

The script requires:
- Python 3.7+
- `.env` file with Langfuse and DemoForge credentials
- `skill/kb_answer.py` available in parent directory
- Network access to DemoForge API (for demo matching)
- Langfuse cloud connection (for trace recording)

## Troubleshooting

### Import Error
```
ERROR: Could not import kb_answer skill
```
Make sure you're running from `/Users/adwit.sharma/kb_docs` directory.

### Missing .env
```
KeyError: 'LANGFUSE_SECRET_KEY'
```
Ensure `.env` file exists with required credentials.

### DemoForge Connection Error
If DemoForge API is unreachable, videos will fall back to YouTube with fallback_reason noted.

### No Videos Attached
Check if module/intent mapping exists in kb_answer.py select_video() function.

## Next Steps

1. Run the test with `--verbose --output-file`
2. Review Langfuse traces for each correlation ID
3. Verify video selection logic in select_video() function
4. Compare DemoForge performance metrics
5. Iterate on module/intent mappings if needed
