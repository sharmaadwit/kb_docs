#!/usr/bin/env python3
"""
Analyze span-events structure and telemetry shape from latest Langfuse traces.
"""

import os
import json
import sys
from datetime import datetime
from collections import defaultdict
from langfuse import Langfuse

def flatten_dict(d, parent_key='', sep='.'):
    """Flatten nested dict for field discovery."""
    items = []
    if not isinstance(d, dict):
        return items
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, (list, tuple)):
            # Note list presence but don't expand
            items.append((new_key, f"[{type(v[0]).__name__}]" if v else "[]"))
        else:
            items.append((new_key, type(v).__name__))
    return dict(items)

def main():
    # Setup Langfuse
    langfuse_key = os.getenv('LANGFUSE_SECRET_KEY')
    langfuse_public = os.getenv('LANGFUSE_PUBLIC_KEY')
    langfuse_host = os.getenv('LANGFUSE_HOST', 'https://cloud.langfuse.com')

    if not langfuse_key or not langfuse_public:
        print("ERROR: LANGFUSE_SECRET_KEY and LANGFUSE_PUBLIC_KEY not set", file=sys.stderr)
        sys.exit(1)

    client = Langfuse(
        secret_key=langfuse_key,
        public_key=langfuse_public,
        host=langfuse_host
    )

    print("Fetching latest 30 traces from Langfuse...")

    # Use the Langfuse API directly for fetching traces
    import requests

    auth = (langfuse_public, langfuse_key)
    url = f"{langfuse_host}/api/public/traces?limit=30"

    response = requests.get(url, auth=auth)
    response.raise_for_status()

    data = response.json()
    traces = data.get('data', [])

    if not traces:
        print("No traces found", file=sys.stderr)
        sys.exit(1)

    print(f"Retrieved {len(traces)} traces\n")

    # Analysis containers
    observations_by_type = defaultdict(int)
    span_event_types = set()
    metadata_fields = defaultdict(int)
    critical_fields = defaultdict(int)
    null_counts = defaultdict(int)
    trace_details = []

    # Analyze each trace
    for idx, trace in enumerate(traces):
        trace_id = trace.get('id', f'trace_{idx}')
        timestamp = trace.get('timestamp')

        trace_info = {
            'id': trace_id,
            'timestamp': timestamp,
            'observation_count': 0,
            'observations': [],
            'metadata_fields': set(),
            'missing_fields': []
        }

        # Check observations (fetch detailed trace with observations)
        observations = trace.get('observations', [])
        if observations:
            trace_info['observation_count'] = len(observations)

            for obs in observations:
                obs_type = obs.get('type', 'unknown')
                observations_by_type[obs_type] += 1

                # Detect span vs event structure
                has_start = 'start_time' in obs and obs['start_time'] is not None
                has_end = 'end_time' in obs and obs['end_time'] is not None

                if has_start and has_end:
                    span_event_types.add('span (start_time + end_time)')
                elif has_start and not has_end:
                    span_event_types.add('event (point-in-time)')

                # Extract observation details
                obs_detail = {
                    'name': obs.get('name'),
                    'type': obs_type,
                    'has_start_time': has_start,
                    'has_end_time': has_end,
                    'has_input': obs.get('input') is not None,
                    'has_output': obs.get('output') is not None,
                }
                trace_info['observations'].append(obs_detail)

        # Analyze metadata
        metadata = trace.get('metadata') or {}
        if isinstance(metadata, dict):
            flat_meta = flatten_dict(metadata)
            trace_info['metadata_fields'] = set(flat_meta.keys())

            # Count field occurrence
            for field in trace_info['metadata_fields']:
                metadata_fields[field] += 1

            # Check critical fields
            critical = ['answer_mode', 'case_studies_count', 'case_studies_fetched',
                       'video_count', 'video_selected', 'confidence', 'intent',
                       'module_label', 'policy_meta']
            for field in critical:
                if field in metadata or any(field in f for f in trace_info['metadata_fields']):
                    critical_fields[field] += 1
                else:
                    trace_info['missing_fields'].append(field)

        trace_details.append(trace_info)

    # Generate report
    print("=" * 80)
    print("TRACE STRUCTURE ANALYSIS REPORT")
    print("=" * 80)
    print(f"Analysis Date: {datetime.now().isoformat()}")
    print(f"Traces Analyzed: {len(traces)}\n")

    print("1. OBSERVATION STRUCTURE")
    print("-" * 80)
    print(f"Observation Types Found: {dict(observations_by_type)}")
    print(f"Span/Event Pattern: {span_event_types}")

    avg_obs = sum(t['observation_count'] for t in trace_details) / len(trace_details) if trace_details else 0
    print(f"Average observations per trace: {avg_obs:.1f}")
    print(f"Max observations in single trace: {max(t['observation_count'] for t in trace_details) if trace_details else 0}")

    print("\nSample Observations (first 3 traces):")
    for idx, trace_info in enumerate(trace_details[:3]):
        print(f"\n  Trace {idx+1} ({trace_info['id'][:8]}...):")
        print(f"    Total observations: {trace_info['observation_count']}")
        if trace_info['observations']:
            for obs_idx, obs in enumerate(trace_info['observations'][:3]):
                print(f"      [{obs_idx+1}] {obs['name']} ({obs['type']})")
                print(f"          - Span: start_time={obs['has_start_time']}, end_time={obs['has_end_time']}")
                print(f"          - Data: input={obs['has_input']}, output={obs['has_output']}")

    print("\n\n2. TELEMETRY PAYLOAD SHAPE")
    print("-" * 80)
    print(f"Total unique metadata fields: {len(metadata_fields)}")
    print(f"\nMost common metadata fields (top 20):")
    sorted_fields = sorted(metadata_fields.items(), key=lambda x: x[1], reverse=True)
    for field, count in sorted_fields[:20]:
        pct = (count / len(traces)) * 100
        print(f"  {field:<40} {count:>3} traces ({pct:>5.1f}%)")

    print("\n\n3. CRITICAL FIELD COMPLETENESS")
    print("-" * 80)
    expected_critical = ['answer_mode', 'case_studies_count', 'case_studies_fetched',
                        'video_count', 'video_selected', 'confidence', 'intent',
                        'module_label', 'policy_meta']

    for field in expected_critical:
        count = critical_fields.get(field, 0)
        pct = (count / len(traces)) * 100
        status = "✓" if pct >= 80 else "⚠" if pct >= 50 else "✗"
        print(f"  {status} {field:<30} {count:>3} traces ({pct:>5.1f}%)")

    # Null field analysis
    print("\n\n4. PAYLOAD COMPLETENESS & CONSISTENCY")
    print("-" * 80)

    traces_with_missing = sum(1 for t in trace_details if t['missing_fields'])
    print(f"Traces with missing critical fields: {traces_with_missing}/{len(traces)}")

    if traces_with_missing > 0:
        missing_summary = defaultdict(int)
        for trace_info in trace_details:
            for field in trace_info['missing_fields']:
                missing_summary[field] += 1

        print("\nMissing field frequency:")
        for field, count in sorted(missing_summary.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {field:<30} absent in {count} traces")

    # Consistency check
    field_sets = [t['metadata_fields'] for t in trace_details if t['metadata_fields']]
    if field_sets:
        consistent_fields = set.intersection(*field_sets) if field_sets else set()
        print(f"\nConsistent field set (in ALL traces): {len(consistent_fields)} fields")
        if len(consistent_fields) <= 10:
            print(f"  Fields: {sorted(consistent_fields)}")

    # Export detailed JSON
    output_file = '/Users/adwit.sharma/kb_docs/local/reports/trace_structure_analysis.json'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    export_data = {
        'timestamp': datetime.now().isoformat(),
        'traces_analyzed': len(traces),
        'observation_types': dict(observations_by_type),
        'span_event_patterns': list(span_event_types),
        'metadata_fields': dict(sorted_fields),
        'critical_field_completeness': {field: critical_fields.get(field, 0) for field in expected_critical},
        'sample_traces': trace_details[:5]
    }

    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2, default=str)

    print(f"\n\nDetailed report exported to: {output_file}")

if __name__ == '__main__':
    main()
