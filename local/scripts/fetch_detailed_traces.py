#!/usr/bin/env python3
"""
Fetch detailed traces with full observations/spans/events structure.
"""

import os
import json
import sys
import requests
from datetime import datetime

def main():
    langfuse_key = os.getenv('LANGFUSE_SECRET_KEY')
    langfuse_public = os.getenv('LANGFUSE_PUBLIC_KEY')
    langfuse_host = os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')

    if not langfuse_key or not langfuse_public:
        print("ERROR: LANGFUSE credentials not set", file=sys.stderr)
        sys.exit(1)

    auth = (langfuse_public, langfuse_key)

    def _trace_to_shape(trace):
        inp = trace.get("input") or {}
        meta = (inp.get("_meta") if isinstance(inp, dict) else None) or trace.get("metadata") or {}
        return {
            "id": trace.get("id"),
            "timestamp": trace.get("timestamp"),
            "name": trace.get("name"),
            "userId": trace.get("userId"),
            "metadata": meta,
            "input": inp,
            "output": trace.get("output"),
        }

    # Fetch list of traces using legacy GET /api/public/traces
    print("Fetching trace list...")
    url = f"{langfuse_host}/api/public/traces?name=kb_answer&limit=30&page=1"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    traces_list = [_trace_to_shape(t) for t in response.json().get('data', [])]

    print(f"Retrieved {len(traces_list)} traces. Fetching detailed data...\n")

    detailed_traces = []
    for idx, trace_header in enumerate(traces_list[:5]):  # Get first 5 in detail
        trace_id = trace_header.get('id')
        print(f"[{idx+1}] Fetching detail for traceId: {str(trace_id)[:30]}...")

        # Fetch the individual trace via GET /api/public/traces/{id}
        detail_url = f"{langfuse_host}/api/public/traces/{trace_id}"
        detail_response = requests.get(detail_url, auth=auth)
        detail_response.raise_for_status()

        trace_detail = _trace_to_shape(detail_response.json())
        detailed_traces.append(trace_detail)

        # Print structure
        print(f"    Trace ID: {trace_detail.get('id')}")
        print(f"    Timestamp: {trace_detail.get('timestamp')}")
        print(f"    Observations count: {len(trace_detail.get('observations', []))}")
        print(f"    Metadata fields: {len(trace_detail.get('metadata', {}))}")

        # Show observations structure
        observations = trace_detail.get('observations', [])
        if observations:
            print(f"\n    Observations Details:")
            for obs_idx, obs in enumerate(observations[:3]):
                print(f"      [{obs_idx+1}] {obs.get('name', 'N/A')}")
                print(f"          Type: {obs.get('type', 'N/A')}")
                print(f"          Start: {obs.get('start_time')}")
                print(f"          End: {obs.get('end_time')}")
                print(f"          Level: {obs.get('level', 'N/A')}")
                if 'input' in obs and obs['input']:
                    print(f"          Input: {type(obs['input']).__name__} ({len(str(obs['input']))} chars)")
                if 'output' in obs and obs['output']:
                    print(f"          Output: {type(obs['output']).__name__} ({len(str(obs['output']))} chars)")
            if len(observations) > 3:
                print(f"      ... and {len(observations) - 3} more observations")

        print()

    # Export full details
    output_file = '/Users/adwit.sharma/kb_docs/local/reports/detailed_traces_sample.json'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'traces_count': len(detailed_traces),
            'traces': detailed_traces
        }, f, indent=2, default=str)

    print(f"\nDetailed traces exported to: {output_file}")

if __name__ == '__main__':
    main()
