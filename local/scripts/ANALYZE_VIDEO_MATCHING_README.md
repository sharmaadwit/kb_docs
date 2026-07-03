# Video Matching Analysis Script

## Overview

`analyze_video_matching.py` fetches recent `kb_answer` traces from Langfuse (PROD_EXT environment) and analyzes how well video attachments align with the user's query module/intent.

## What It Does

1. **Fetches 20 most recent kb_answer traces** from Langfuse API
2. **Extracts per-trace data**:
   - query
   - module_label (or inferred from query)
   - video_title
   - video_platform
   - demoforge_demo_id
   - confidence score
   - timestamp

3. **Analyzes module-video matching**:
   - Checks if video_platform matches expected platform for module
   - Checks if video_title contains module-specific keywords
   - Calculates confidence score (0-1)
   - Flags mismatches

4. **Generates summary report**:
   - Total traces analyzed
   - Video attachment rate (%)
   - Module-video matching accuracy (%)
   - Per-module statistics
   - Top 10 mismatches with details
   - Actionable recommendations

## Requirements

- Python 3.7+
- Langfuse credentials in `.env`:
  ```
  LANGFUSE_HOST=https://cloud.langfuse.com
  LANGFUSE_PUBLIC_KEY=pk-lf-...
  LANGFUSE_SECRET_KEY=sk-lf-...
  ```

## Usage

```bash
# Basic run (outputs JSON to stdout + saves to local/reports/)
python3 /Users/adwit.sharma/kb_docs/local/scripts/analyze_video_matching.py

# Pipe to jq for pretty filtering
python3 /Users/adwit.sharma/kb_docs/local/scripts/analyze_video_matching.py | jq '.summary'

# Save to custom location
python3 /Users/adwit.sharma/kb_docs/local/scripts/analyze_video_matching.py > /tmp/analysis.json
```

## Output Structure

```json
{
  "summary": {
    "analysis_timestamp": "2026-07-03T...",
    "total_traces_analyzed": 20,
    "traces_with_video": 18,
    "traces_with_module": 19,
    "video_attachment_rate_percent": 90.0,
    "traces_with_video_module_match": 16,
    "module_video_matching_accuracy_percent": 88.89
  },
  "module_stats": {
    "Bot Studio": {
      "total_traces": 5,
      "with_video": 5,
      "matching_count": 5,
      "accuracy": 100.0,
      "avg_confidence": 0.95
    },
    ...
  },
  "traces": [
    {
      "trace_id": "...",
      "timestamp": "...",
      "query": "How do I create a bot?",
      "module": "Bot Studio",
      "video_title": "Creating Bots with Bot Studio",
      "video_platform": "demo_videos",
      "demoforge_demo_id": "demo_123",
      "confidence_score": 4.2,
      "match_result": {
        "matches": true,
        "reason": "platform_match + title_marker_found",
        "confidence": 1.0
      }
    },
    ...
  ],
  "top_mismatches": [
    {
      "query": "How to set up email campaigns?",
      "module": "Campaign Manager",
      "current_video": "General Demo Video",
      "issue": "no_match",
      "expected_platform": "demo_videos",
      "current_platform": "demo_videos"
    }
  ],
  "recommendations": [
    "Module-video matching accuracy is below 80%. Review video selection logic...",
    ...
  ]
}
```

## Module-Video Matching Logic

The script validates that:

1. **Platform matches**: Expected platform for module == actual video_platform
2. **Title marker found**: Video title contains module-specific keywords

Example:
- Module: "Bot Studio"
- Expected platform: "demo_videos"
- Video title: "Creating Bots with Bot Studio"
- Confidence: 1.0 (both platform and title marker match)

## Modules Supported

| Module | Keywords | Video Markers | Expected Platform |
|--------|----------|---------------|-------------------|
| Bot Studio | bot, studio, automation, conversation, workflow | bot, studio | demo_videos |
| CTX | ctx, context, customer, context exchange | context, ctx | demo_videos |
| AI Admin | ai, admin, administration, settings, configuration | ai, admin | demo_videos |
| Campaign Manager | campaign, manager, marketing, email, message | campaign | demo_videos |
| Personalize | personalize, personalization, segment, dynamic | personalize | demo_videos |

## Troubleshooting

### "LANGFUSE_PUBLIC_KEY or LANGFUSE_SECRET_KEY not set"
- Ensure `.env` file exists at `/Users/adwit.sharma/kb_docs/.env`
- Credentials must be set as environment variables or in `.env`

### No traces returned
- Check Langfuse credentials are valid
- Verify kb_answer traces exist in PROD_EXT environment
- Check network connectivity to cloud.langfuse.com

### Video platform mismatches
- Review kb_answer logic for video_platform assignment
- Verify DemoForge integration populates correct platform values
- Check that video metadata is properly serialized in trace output

## Integration with KB Dashboard

This script feeds data into the comprehensive KB analytics dashboard for:
- Video attachment monitoring
- Module-video alignment tracking
- Quality metrics for video recommendations
- Trend analysis of video effectiveness

## Next Steps

1. Run script to generate baseline report
2. Review top_mismatches to identify problematic pairings
3. Implement recommendations in kb_answer logic
4. Re-run script to verify improvements
5. Set up scheduled runs for continuous monitoring
